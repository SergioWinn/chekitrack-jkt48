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


def render_collection_entry(entry):
    dt = pd.to_datetime(entry["start_time"]) if entry.get("start_time") else None
    event_date = format_event_date(dt) if dt is not None else "Archived date"
    slot_label = entry.get("slot_key", "A")
    return f"""
    <section class="ckt-surface ckt-panel" style="margin-bottom:10px">
      <div class="ckt-panel-head">
        <div>
          <div class="ckt-meta">Collection entry</div>
          <h2 class="ckt-panel-title">{safe_text(entry.get('event_name', 'Archived event'))}</h2>
        </div>
        <div class="ckt-panel-note">{safe_text(event_date)}</div>
      </div>
      <div class="ckt-meta-row" style="margin-bottom:10px">
        {render_event_chip(entry.get('event_type', 'Roulette'))}
        <span class="ckt-chip ckt-chip-team">Slot {safe_text(slot_label)}</span>
        <span class="ckt-chip ckt-chip-completed">Qty {int(entry.get('quantity') or 0)}</span>
      </div>
      <div class="ckt-member-line" style="margin-top:0">
        {render_avatar_markup(entry.get('member_avatar_url'), entry.get('member_name', 'Unknown member'))}
        <span>{safe_text(entry.get('member_name', 'Unknown member'))}</span>
      </div>
    </section>
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
      <p class="ckt-body">This shelf is the main view. Update quantities here first, then open the collection desk below when you want to add more.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

if not collection_entries:
    st.markdown(
        '<div class="ckt-empty">No collection entries yet. Use the collection desk below to add your first saved event slot.</div>',
        unsafe_allow_html=True,
    )
else:
    for entry in collection_entries:
        st.markdown(render_collection_entry(entry), unsafe_allow_html=True)
        control_cols = st.columns([1.1, 0.9, 0.9], gap="small")
        updated_quantity = control_cols[0].number_input(
            f"Quantity for {entry['event_name']} {entry['slot_key']}",
            min_value=1,
            value=int(entry.get("quantity") or 1),
            step=1,
            key=f"entry_qty_{entry['id']}",
            label_visibility="collapsed",
        )
        if control_cols[1].button("Save quantity", key=f"save_entry_{entry['id']}", use_container_width=True):
            update_collection_quantity(auth_supabase, entry["id"], int(updated_quantity))
            st.success("Quantity saved.")
            st.rerun()
        if control_cols[2].button("Remove", key=f"delete_entry_{entry['id']}", use_container_width=True):
            delete_collection_entry(auth_supabase, entry["id"])
            st.success("Entry removed.")
            st.rerun()

desk_expanded = not collection_entries
with st.expander("Open collection desk", expanded=desk_expanded):
    st.markdown(
        """
        <section class="ckt-surface ckt-panel">
          <div class="ckt-kicker">Collection desk</div>
          <h2 class="ckt-panel-title">Add or correct an event result</h2>
          <p class="ckt-body">Only resolved event slots appear here, so member assignment always follows the archive. Use this desk after you review the shelf above.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

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

        form_col, preview_col = st.columns([0.95, 1.05], gap="large")
        with form_col:
            add_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="collection_add_quantity")
            if st.button("Add to collection", use_container_width=True):
                try:
                    action = add_collection_quantity(auth_supabase, active_slot, int(add_quantity))
                    st.success("Collection updated." if action == "updated" else "Added to collection.")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))
        with preview_col:
            st.markdown(render_selected_slot_card(active_slot), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
