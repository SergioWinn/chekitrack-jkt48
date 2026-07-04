import pandas as pd
import streamlit as st

from utils.auth import (
    current_profile,
    get_auth_client,
    hydrate_auth_session,
    is_authenticated,
    sign_in_with_username,
    sign_up_with_username,
)
from utils.collections import (
    add_collection_quantity,
    count_pending_slots,
    delete_collection_entry,
    load_collectible_slots,
    load_user_collection_entries,
    update_collection_quantity,
)
from utils.supabase_client import get_supabase
from utils.styles import (
    ARCHIVE_THEME_CSS,
    DARK_THEME_CSS,
    format_event_date,
    format_event_time,
    render_avatar_markup,
    render_event_chip,
    render_navbar,
    safe_text,
)


def render_collection_card(entry):
    dt = pd.to_datetime(entry["start_time"]) if entry.get("start_time") else None
    end_dt = pd.to_datetime(entry["end_time"]) if entry.get("end_time") else None
    event_date = format_event_date(dt) if dt is not None else "Archived date"
    event_time = format_event_time(dt, end_dt) if dt is not None else "Archived time"
    slot_label = entry.get("slot_key", "A")
    event_name = safe_text(entry.get('event_name', 'Archived event'))
    return f"""
    <article class="ckt-surface ckt-collection-card">
      <div class="ckt-collection-card-top">
        <div class="ckt-collection-identity">
          {render_avatar_markup(entry.get('member_avatar_url'), entry.get('member_name', 'Unknown member'), class_name='ckt-collection-avatar')}
          <div class="ckt-collection-identity-copy">
            <div class="ckt-collection-member-name">{safe_text(entry.get('member_name', 'Unknown member'))}</div>
            <div class="ckt-small">{safe_text(f"Gen {entry['member_generasi']}") if entry.get('member_generasi') else 'Generation unknown'}</div>
          </div>
        </div>
        <div class="ckt-collection-qty">{int(entry.get('quantity') or 0)}x</div>
      </div>
      <div class="ckt-collection-copy">
        <div class="ckt-meta">{safe_text(entry.get('event_type', 'Roulette'))}</div>
        <h3 class="ckt-collection-event" title="{event_name}">{event_name}</h3>
      </div>
      <div class="ckt-small">{safe_text(event_date)} | {safe_text(event_time)}</div>
      <div class="ckt-meta-row" style="margin:10px 0 12px">
        <span class="ckt-chip ckt-chip-team">Slot {safe_text(slot_label)}</span>
        {render_event_chip(entry.get('event_type', 'Roulette'))}
      </div>
    </article>
    """


def render_selected_slot_card(slot):
    start_dt = pd.to_datetime(slot["start_time"])
    end_dt = pd.to_datetime(slot["end_time"]) if slot.get("end_time") else None
    return f"""
    <section class="ckt-surface ckt-panel" style="margin-top:10px">
      <div class="ckt-panel-head">
        <div>
          <div class="ckt-meta">Selected result</div>
          <h2 class="ckt-panel-title">{safe_text(slot['event_name'])}</h2>
        </div>
        <div class="ckt-panel-note">{safe_text(slot['slot_label'])}</div>
      </div>
      <div class="ckt-small">{safe_text(format_event_date(start_dt))} | {safe_text(format_event_time(start_dt, end_dt))}</div>
      <div class="ckt-meta-row" style="margin-bottom:10px">
        {render_event_chip(slot['event_type'])}
        <span class="ckt-chip ckt-chip-team">{safe_text(slot['slot_label'])}</span>
      </div>
      <div class="ckt-member-line" style="margin-top:0">
        {render_avatar_markup(slot.get('member_avatar_url'), slot['member_name'])}
        <span>{safe_text(slot['member_name'])}</span>
      </div>
    </section>
    """


def render_collection_shelf(entries, columns_count: int = 4):
    for start in range(0, len(entries), columns_count):
        row_entries = entries[start:start + columns_count]
        cols = st.columns(columns_count, gap="small")
        for col, entry in zip(cols, row_entries):
            with col:
                st.markdown(render_collection_card(entry), unsafe_allow_html=True)
        st.markdown('<div class="ckt-collection-row-spacer"></div>', unsafe_allow_html=True)


st.set_page_config(
    page_title="My Collection · Chekicha Timeline",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(DARK_THEME_CSS + ARCHIVE_THEME_CSS, unsafe_allow_html=True)

public_supabase = get_supabase()
pending_rows = public_supabase.table("chekicha").select("slot_mode, member_id_a, member_id_b").execute().data or []
pending_count = count_pending_slots(pending_rows)

hydrate_auth_session()
render_navbar("collection", pending_count)
st.markdown('<div class="ct-content ct-archive">', unsafe_allow_html=True)

st.markdown(
    """
    <section class="ckt-compact-intro">
      <div class="ckt-surface ckt-panel ckt-intro-panel">
        <div class="ckt-kicker">My collection</div>
        <h1 class="ckt-member-title">Your cheki shelf comes first.</h1>
        <p class="ckt-body">Open your saved archive first, then add or correct entries from resolved event results when you need to.</p>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if not is_authenticated():
    signin_tab, signup_tab = st.tabs(["Sign in", "Create account"])

    with signin_tab:
        with st.form("collection_signin"):
            signin_username = st.text_input("Username", key="collection_signin_username")
            signin_password = st.text_input("Password", type="password", key="collection_signin_password")
            signin_submit = st.form_submit_button("Sign in", use_container_width=True)
        if signin_submit:
            ok, message = sign_in_with_username(signin_username, signin_password)
            if ok:
                st.success(message)
                st.rerun()
            st.error(message)

    with signup_tab:
        with st.form("collection_signup"):
            signup_username = st.text_input("Username", key="collection_signup_username")
            signup_password = st.text_input("Password", type="password", key="collection_signup_password")
            signup_confirm = st.text_input("Confirm password", type="password", key="collection_signup_confirm")
            signup_submit = st.form_submit_button("Create account", use_container_width=True)
        if signup_submit:
            if signup_password != signup_confirm:
                st.error("Passwords do not match.")
            else:
                ok, message = sign_up_with_username(signup_username, signup_password)
                if ok:
                    st.success(message)
                    st.rerun()
                st.error(message)

    st.markdown(
        '<div class="ckt-empty">Use a simple username and password. No email is shown to the public, but Supabase email confirmation should be disabled for this login flow.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

profile = current_profile()
auth_supabase = get_auth_client()

try:
    collectible_slots = load_collectible_slots(public_supabase)
    collection_entries = load_user_collection_entries(auth_supabase, public_supabase)
except Exception as exc:
    st.error(
        "Collection tables are not ready yet. Run the Supabase auth + collection SQL setup first."
    )
    st.caption(str(exc))
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

total_quantity = sum(int(entry.get("quantity") or 0) for entry in collection_entries)
unique_members = len({entry.get("member_id") for entry in collection_entries})
unique_events = len({entry.get("event_id") for entry in collection_entries})

entry_options = [
    {
        "id": entry["id"],
        "label": f"{entry['event_name']} | Slot {entry.get('slot_key', 'A')} | {entry['member_name']}",
        "entry": entry,
    }
    for entry in collection_entries
]

st.markdown(
    f"""
    <section class="ckt-mini-strip">
      <div class="ckt-mini-cell">
        <div class="ckt-meta">Signed in</div>
        <strong class="ckt-mini-value">@{safe_text(profile.get('username') if profile else 'collector')}</strong>
      </div>
      <div class="ckt-mini-cell">
        <div class="ckt-meta">Total cheki</div>
        <strong class="ckt-mini-value">{total_quantity}</strong>
      </div>
      <div class="ckt-mini-cell">
        <div class="ckt-meta">Tracked members</div>
        <strong class="ckt-mini-value">{unique_members}</strong>
        <div class="ckt-small">Across {unique_events} archived event slots.</div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="ckt-surface ckt-panel">
      <div class="ckt-kicker">Stored collection</div>
      <h2 class="ckt-panel-title">Your saved cheki</h2>
      <p class="ckt-body">This shelf is read-only on purpose. Scan what you already own first, then use the desk below to add, update, or remove entries.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

collection_filter_widget = getattr(st, "segmented_control", None)
collection_filter_options = ["All", "Roulette", "Birthday", "Graduation"]
if collection_filter_widget:
    collection_filter = collection_filter_widget(
        "Collection type",
        collection_filter_options,
        default="All",
    )
else:
    collection_filter = st.selectbox("Collection type", collection_filter_options)

visible_collection_entries = (
    collection_entries
    if collection_filter == "All"
    else [entry for entry in collection_entries if entry.get("event_type") == collection_filter]
)

if not collection_entries:
    st.markdown(
        '<div class="ckt-empty">No collection entries yet. Use the collection desk below to add your first saved event slot.</div>',
        unsafe_allow_html=True,
    )
else:
    if not visible_collection_entries:
        st.markdown(
            f'<div class="ckt-empty">No saved entries match the {safe_text(collection_filter)} filter yet.</div>',
            unsafe_allow_html=True,
        )
    else:
        render_collection_shelf(visible_collection_entries)

tool_cols = st.columns([1, 1, 2.4], gap="small")

with tool_cols[0]:
    with st.popover("Add entry", use_container_width=True):
        if not collectible_slots:
            st.markdown('<div class="ckt-empty">No resolved event slots are ready for collection yet.</div>', unsafe_allow_html=True)
        else:
            event_map = {}
            for slot in collectible_slots:
                dt = pd.to_datetime(slot["start_time"])
                end_dt = pd.to_datetime(slot["end_time"]) if slot.get("end_time") else None
                event_map.setdefault(
                    slot["event_id"],
                    {
                        "event_id": slot["event_id"],
                        "label": f'{slot["event_name"]} | {dt.day} {dt:%b %Y} | {format_event_time(dt, end_dt)} | {slot["event_type"]}',
                    },
                )

            event_options = list(event_map.values())
            selected_event = st.selectbox(
                "Event",
                event_options,
                format_func=lambda item: item["label"],
                key="collection_event_picker",
            )

            selected_slots = [slot for slot in collectible_slots if slot["event_id"] == selected_event["event_id"]]
            active_slot = selected_slots[0]
            if len(selected_slots) > 1:
                active_slot = st.selectbox(
                    "Result slot",
                    selected_slots,
                    format_func=lambda item: f'{item["slot_label"]} | {item["member_name"]}',
                    key="collection_slot_picker",
                )

            st.markdown(render_selected_slot_card(active_slot), unsafe_allow_html=True)
            add_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="collection_add_quantity")
            if st.button("Add to collection", key="collection_add_submit", use_container_width=True):
                try:
                    action = add_collection_quantity(auth_supabase, active_slot, int(add_quantity))
                    st.success("Collection updated." if action == "updated" else "Added to collection.")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

with tool_cols[1]:
    with st.popover("Edit / remove", use_container_width=True):
        if not entry_options:
            st.markdown('<div class="ckt-empty">Your shelf is still empty, so there is nothing to edit yet.</div>', unsafe_allow_html=True)
        else:
            selected_entry_option = st.selectbox(
                "Saved entry",
                entry_options,
                format_func=lambda item: item["label"],
                key="collection_edit_picker",
            )
            selected_entry = selected_entry_option["entry"]
            st.markdown(render_collection_card(selected_entry), unsafe_allow_html=True)
            updated_quantity = st.number_input(
                "New quantity",
                min_value=1,
                value=int(selected_entry.get("quantity") or 1),
                step=1,
                key=f"entry_qty_manage_{selected_entry['id']}",
            )
            action_cols = st.columns([1, 1], gap="small")
            if action_cols[0].button("Save quantity", key=f"save_manage_{selected_entry['id']}", use_container_width=True):
                update_collection_quantity(auth_supabase, selected_entry["id"], int(updated_quantity))
                st.success("Quantity saved.")
                st.rerun()
            if action_cols[1].button("Remove entry", key=f"delete_manage_{selected_entry['id']}", use_container_width=True):
                delete_collection_entry(auth_supabase, selected_entry["id"])
                st.success("Entry removed.")
                st.rerun()

with tool_cols[2]:
    st.markdown(
        """
        <section class="ckt-surface ckt-panel" style="padding:12px 14px">
          <div class="ckt-kicker">Quick tools</div>
          <div class="ckt-small">Open only when you need to add a new event result or correct a saved quantity.</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
