from calendar import monthrange
from datetime import datetime, time, timedelta

import pandas as pd
import streamlit as st

from utils.auth import hydrate_auth_session, is_admin
from utils.collections import count_pending_slots
from utils.supabase_client import get_supabase
from utils.styles import ARCHIVE_THEME_CSS, DARK_THEME_CSS, format_event_date, format_event_time, render_navbar, safe_text


def load_event_presets(supabase_client):
    try:
        response = (
            supabase_client.table("event_presets")
            .select("id, event_name, event_type, event_image_url, sort_order, is_active")
            .eq("is_active", True)
            .order("sort_order")
            .order("event_name")
            .execute()
        )
        return response.data or []
    except Exception:
        return []


def single_member_event(event_type: str | None) -> bool:
    return event_type in {"Birthday", "Graduation"}


def get_event_duration_minutes(event_type: str) -> int:
    return 60 if event_type in {"Birthday", "Graduation"} else 15


STATUS_OPTIONS = ["LOVE", "DREAM", "PASSION", "TRAINEE", "GRADUATED"]
GENERATION_OPTIONS = [3] + list(range(6, 15))
TIME_STEP_MINUTES = 1


def duplicate_member_labels(members, nickname: str, full_name: str, exclude_id=None):
    nickname_key = nickname.strip().casefold()
    full_name_key = full_name.strip().casefold()
    duplicates = []
    for member in members:
        if exclude_id and member["id"] == exclude_id:
            continue
        member_nickname = str(member.get("nickname") or "").strip().casefold()
        member_full_name = str(member.get("full_name") or "").strip().casefold()
        if nickname_key and member_nickname == nickname_key:
            duplicates.append(f'Nickname already used by {member.get("full_name") or member.get("nickname")}.')
        if full_name_key and member_full_name == full_name_key:
            duplicates.append(f'Full name already exists for {member.get("nickname") or member.get("full_name")}.')
    return duplicates


def member_usage_count(supabase_client, member_id) -> int:
    rows = (
        supabase_client.table("chekicha")
        .select("id")
        .or_(f"member_id_a.eq.{member_id},member_id_b.eq.{member_id}")
        .execute()
        .data
        or []
    )
    return len(rows)


def event_collection_usage_count(supabase_client, event_id) -> int | None:
    try:
        rows = (
            supabase_client.table("user_collection_entries")
            .select("id")
            .eq("event_id", event_id)
            .execute()
            .data
            or []
        )
        return len(rows)
    except Exception:
        return None


def get_default_event_start() -> datetime:
    current = datetime.now().replace(second=0, microsecond=0)
    remainder = current.minute % TIME_STEP_MINUTES
    if remainder:
        current += timedelta(minutes=TIME_STEP_MINUTES - remainder)
    return current


def load_event_rows(supabase_client):
    return (
        supabase_client.table("chekicha")
        .select("id, event_name, event_type, start_time, end_time, event_image_url, slot_mode, member_id_a, member_id_b")
        .order("start_time", desc=True)
        .execute()
        .data
        or []
    )


def resolve_preset(presets, event_name: str, fallback_event=None):
    for preset in presets:
        if preset["event_name"] == event_name:
            return preset
    if fallback_event:
        return {
            "event_name": fallback_event.get("event_name") or event_name,
            "event_type": fallback_event.get("event_type") or "Other",
            "event_image_url": fallback_event.get("event_image_url") or "",
        }
    return None


def set_event_picker_state(prefix: str, start_dt: datetime):
    st.session_state[f"{prefix}_year"] = start_dt.year
    st.session_state[f"{prefix}_month"] = start_dt.month
    st.session_state[f"{prefix}_day"] = start_dt.day
    st.session_state[f"{prefix}_hour"] = start_dt.hour
    st.session_state[f"{prefix}_minute"] = start_dt.minute


def render_event_datetime_fields(prefix: str, default_start: datetime):
    year_options = list(range(default_start.year - 1, default_start.year + 4))
    month_options = list(range(1, 13))
    minute_options = list(range(0, 60, TIME_STEP_MINUTES))

    current_year = st.session_state.get(f"{prefix}_year", default_start.year)
    if current_year not in year_options:
        year_options.append(current_year)
        year_options.sort()
    current_month = st.session_state.get(f"{prefix}_month", default_start.month)
    current_month = current_month if current_month in month_options else default_start.month
    day_options = list(range(1, monthrange(current_year, current_month)[1] + 1))
    current_day = st.session_state.get(f"{prefix}_day", default_start.day)
    if current_day not in day_options:
        current_day = day_options[-1]
        st.session_state[f"{prefix}_day"] = current_day
    current_hour = st.session_state.get(f"{prefix}_hour", default_start.hour)
    current_hour = current_hour if current_hour in range(24) else default_start.hour
    current_minute = st.session_state.get(f"{prefix}_minute", default_start.minute)
    current_minute = current_minute if current_minute in minute_options else default_start.minute

    date_col_year, date_col_month, date_col_day = st.columns([0.9, 1, 0.8])
    event_year = date_col_year.selectbox(
        "Year",
        year_options,
        index=year_options.index(current_year),
        key=f"{prefix}_year",
    )
    event_month = date_col_month.selectbox(
        "Month",
        month_options,
        index=month_options.index(current_month),
        format_func=lambda value: datetime(2000, value, 1).strftime("%B"),
        key=f"{prefix}_month",
    )
    refreshed_day_options = list(range(1, monthrange(event_year, event_month)[1] + 1))
    selected_day = st.session_state.get(f"{prefix}_day", current_day)
    if selected_day not in refreshed_day_options:
        selected_day = refreshed_day_options[-1]
        st.session_state[f"{prefix}_day"] = selected_day
    event_day = date_col_day.selectbox(
        "Day",
        refreshed_day_options,
        index=refreshed_day_options.index(selected_day),
        format_func=lambda value: f"{value:02d}",
        key=f"{prefix}_day",
    )

    time_col_hour, time_col_minute = st.columns(2)
    event_hour = time_col_hour.selectbox(
        "Hour",
        list(range(24)),
        index=current_hour,
        format_func=lambda value: f"{value:02d}",
        key=f"{prefix}_hour",
    )
    event_minute = time_col_minute.selectbox(
        "Minute",
        minute_options,
        index=minute_options.index(current_minute),
        format_func=lambda value: f"{value:02d}",
        key=f"{prefix}_minute",
    )

    event_date = datetime(event_year, event_month, event_day).date()
    start_time = time(event_hour, event_minute)
    st.caption(f"Scheduled for {event_date.strftime('%d %b %Y')} at {start_time.strftime('%H:%M')}")
    return event_date, start_time


def build_event_payload(event_date, start_time, preset, slot_mode: int, member_id_a=None, member_id_b=None):
    event_type = preset["event_type"]
    is_single_member = single_member_event(event_type)
    duration_minutes = get_event_duration_minutes(event_type)
    start_dt_obj = datetime.combine(event_date, start_time)
    end_dt_obj = start_dt_obj + timedelta(minutes=duration_minutes)
    return {
        "start_time": start_dt_obj.isoformat(),
        "end_time": end_dt_obj.isoformat(),
        "event_name": preset["event_name"],
        "event_type": event_type,
        "event_image_url": (preset.get("event_image_url") or None),
        "slot_mode": 1 if is_single_member else slot_mode,
        "member_id_a": member_id_a,
        "member_id_b": None if is_single_member or slot_mode != 2 else member_id_b,
    }, is_single_member, duration_minutes


def sync_edit_event_state(selected_event):
    selected_id = selected_event["id"]
    if st.session_state.get("admin_edit_event_loaded_id") == selected_id:
        return
    st.session_state["admin_edit_event_loaded_id"] = selected_id
    st.session_state["admin_edit_event_name"] = selected_event.get("event_name") or ""
    st.session_state["admin_edit_event_slot_label"] = "2 slots" if (selected_event.get("slot_mode") or 1) == 2 else "1 slot"
    st.session_state["admin_edit_event_member_a"] = selected_event.get("member_id_a")
    st.session_state["admin_edit_event_member_b"] = selected_event.get("member_id_b")
    start_dt = pd.to_datetime(selected_event["start_time"]).to_pydatetime().replace(second=0, microsecond=0)
    set_event_picker_state("admin_edit_event", start_dt)


def render_member_preview(title: str, nickname: str, full_name: str, status: str, generation: int, avatar_url: str):
    preview = (
        f'<div class="ckt-preset-thumb" style="aspect-ratio:1 / 1"><img src="{safe_text(avatar_url)}" alt="{safe_text(nickname or full_name or "Member")} avatar" loading="lazy"></div>'
        if avatar_url else '<div class="ckt-empty" style="margin-top:10px">No avatar URL yet.</div>'
    )
    return f"""
    <section class="ckt-surface ckt-panel ckt-preset-summary">
      <div class="ckt-preset-copy">
        <div class="ckt-kicker">{safe_text(title)}</div>
        <h2 class="ckt-panel-title">{safe_text(nickname or 'Nickname')}</h2>
        <p class="ckt-body" style="margin-top:0">{safe_text(full_name or 'Full name')}</p>
        <div class="ckt-meta-row">
          <span class="ckt-chip ckt-chip-team">{safe_text(status)}</span>
          <span class="ckt-chip ckt-chip-team">Gen {int(generation)}</span>
        </div>
      </div>
      <div>{preview}</div>
    </section>
    """


def render_admin_tool_intro(kicker: str, title: str, body: str):
    return f"""
    <section class="ckt-surface ckt-panel ckt-admin-tool-head">
      <div class="ckt-kicker">{safe_text(kicker)}</div>
      <h2 class="ckt-panel-title">{safe_text(title)}</h2>
      <p class="ckt-body">{safe_text(body)}</p>
    </section>
    """


def event_has_waiting_slot_a(event) -> bool:
    return not event.get("member_id_a")


def event_has_waiting_slot_b(event) -> bool:
    return (event.get("slot_mode") or 1) == 2 and not event.get("member_id_b")


def sync_edit_member_state(selected_member):
    selected_id = selected_member["id"]
    if st.session_state.get("admin_edit_member_loaded_id") == selected_id:
        return
    st.session_state["admin_edit_member_loaded_id"] = selected_id
    st.session_state["admin_edit_nickname"] = selected_member.get("nickname") or ""
    st.session_state["admin_edit_full_name"] = selected_member.get("full_name") or ""
    st.session_state["admin_edit_status"] = selected_member.get("status") or STATUS_OPTIONS[0]
    current_generation = int(selected_member.get("generasi") or GENERATION_OPTIONS[0])
    st.session_state["admin_edit_generation"] = current_generation if current_generation in GENERATION_OPTIONS else GENERATION_OPTIONS[0]
    st.session_state["admin_edit_avatar"] = selected_member.get("avatar_url") or ""


st.set_page_config(
    page_title="Admin · Chekicha Timeline",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(DARK_THEME_CSS + ARCHIVE_THEME_CSS, unsafe_allow_html=True)

supabase = get_supabase()
pending_rows = (
    supabase.table("chekicha").select("slot_mode, member_id_a, member_id_b").execute().data or []
)
pending_count = count_pending_slots(pending_rows)

hydrate_auth_session()
if not is_admin():
    st.switch_page("pages/1_📊_Overview.py")

render_navbar("admin", pending_count)
st.markdown('<div class="ct-content ct-archive ckt-admin-stage">', unsafe_allow_html=True)

st.markdown(
    """
    <section class="ckt-compact-intro ckt-admin-hero">
      <div class="ckt-surface ckt-panel ckt-intro-panel ckt-admin-hero-panel">
        <div class="ckt-kicker">Admin console</div>
        <h1 class="ckt-member-title">Operate the archive, not the public showcase.</h1>
        <p class="ckt-body">Manage members, schedule archive rows, and resolve waiting roulette slots from one restricted workspace.</p>
      </div>
      <div class="ckt-admin-note">
        <div class="ckt-meta">Restricted workspace</div>
        <div class="ckt-body">This page is visible only to accounts with the <code>admin</code> role.</div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="ckt-admin-banner">Admin role active</div>', unsafe_allow_html=True)

if True:
    members_data = supabase.table("members").select("id, nickname, full_name, status, generasi, avatar_url").order("nickname").execute().data or []
    presets = load_event_presets(supabase)
    all_events = load_event_rows(supabase)

    st.markdown(
        f"""
        <section class="ckt-mini-strip ckt-admin-strip">
          <div class="ckt-mini-cell">
            <div class="ckt-meta">Waiting now</div>
            <strong class="ckt-mini-value {'is-hot' if pending_count else ''}">{pending_count}</strong>
          </div>
          <div class="ckt-mini-cell">
            <div class="ckt-meta">Event presets</div>
            <strong class="ckt-mini-value">{len(presets)}</strong>
          </div>
          <div class="ckt-mini-cell">
            <div class="ckt-meta">Members</div>
            <strong class="ckt-mini-value">{len(members_data)}</strong>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    member_options = {"None (Waiting for roulette)": None}
    member_labels = {}
    for member in members_data:
        label = f"{member['nickname']} ({member['full_name']})"
        member_options[label] = member["id"]
        member_labels[member["id"]] = label
    member_value_options = list(member_options.values())

    tab_update, tab_add, tab_member = st.tabs(["Fill Results", "Events", "Members"])

    with tab_member:
        st.markdown(render_admin_tool_intro("Member registry", "Manage collector roster", "Add a new member quickly or open the edit tool only when you need to change existing records."), unsafe_allow_html=True)

        member_tool_cols = st.columns([1, 1], gap="small")

        with member_tool_cols[0]:
            with st.popover("Add member", use_container_width=True):
                col_nickname, col_full_name = st.columns(2)
                nickname = col_nickname.text_input("Nickname", key="admin_member_nickname")
                full_name = col_full_name.text_input("Full name", key="admin_member_full_name")
                col_status, col_generation = st.columns([1.1, 0.9])
                status = col_status.selectbox("Team / status", STATUS_OPTIONS, key="admin_member_status")
                generation = col_generation.selectbox("Generation", GENERATION_OPTIONS, key="admin_member_generation")
                avatar_url = st.text_input("Avatar URL", key="admin_member_avatar")
                st.markdown(render_member_preview("Preview", nickname, full_name, status, int(generation), avatar_url.strip()), unsafe_allow_html=True)
                if st.button("Save member", key="admin_save_member", use_container_width=True):
                    cleaned_nickname = nickname.strip()
                    cleaned_full_name = full_name.strip()
                    cleaned_avatar_url = avatar_url.strip()

                    if not cleaned_nickname or not cleaned_full_name:
                        st.error("Nickname and full name are required.")
                    else:
                        duplicates = duplicate_member_labels(members_data, cleaned_nickname, cleaned_full_name)
                        if duplicates:
                            st.error(" ".join(dict.fromkeys(duplicates)))
                        else:
                            payload = {
                                "nickname": cleaned_nickname,
                                "full_name": cleaned_full_name,
                                "status": status,
                                "generasi": int(generation),
                                "avatar_url": cleaned_avatar_url or None,
                            }
                            supabase.table("members").insert(payload).execute()
                            st.success(f"{cleaned_nickname} added to the member registry.")
                            st.rerun()

        with member_tool_cols[1]:
            if members_data:
                with st.popover("Edit / delete member", use_container_width=True):
                    member_manage_options = {f"{member['nickname']} ({member['full_name']})": member for member in members_data}
                    selected_member_label = st.selectbox("Member record", list(member_manage_options.keys()), key="admin_edit_member_label")
                    selected_member = member_manage_options[selected_member_label]
                    sync_edit_member_state(selected_member)

                    edit_col_nickname, edit_col_full_name = st.columns(2)
                    edit_nickname = edit_col_nickname.text_input("Edit nickname", key="admin_edit_nickname")
                    edit_full_name = edit_col_full_name.text_input("Edit full name", key="admin_edit_full_name")

                    edit_col_status, edit_col_generation = st.columns([1.1, 0.9])
                    edit_status = edit_col_status.selectbox("Edit team / status", STATUS_OPTIONS, key="admin_edit_status")
                    edit_generation = edit_col_generation.selectbox("Edit generation", GENERATION_OPTIONS, key="admin_edit_generation")
                    edit_avatar_url = st.text_input("Edit avatar URL", key="admin_edit_avatar")

                    st.markdown(
                        render_member_preview("Edit preview", edit_nickname, edit_full_name, edit_status, int(edit_generation), edit_avatar_url.strip()),
                        unsafe_allow_html=True,
                    )

                    update_col, delete_col = st.columns(2)
                    if update_col.button("Update member", key="admin_update_member", use_container_width=True):
                        cleaned_nickname = edit_nickname.strip()
                        cleaned_full_name = edit_full_name.strip()
                        cleaned_avatar_url = edit_avatar_url.strip()
                        if not cleaned_nickname or not cleaned_full_name:
                            st.error("Nickname and full name are required.")
                        else:
                            duplicates = duplicate_member_labels(
                                members_data,
                                cleaned_nickname,
                                cleaned_full_name,
                                exclude_id=selected_member["id"],
                            )
                            if duplicates:
                                st.error(" ".join(dict.fromkeys(duplicates)))
                            else:
                                payload = {
                                    "nickname": cleaned_nickname,
                                    "full_name": cleaned_full_name,
                                    "status": edit_status,
                                    "generasi": int(edit_generation),
                                    "avatar_url": cleaned_avatar_url or None,
                                }
                                supabase.table("members").update(payload).eq("id", selected_member["id"]).execute()
                                st.success(f"{cleaned_nickname} updated.")
                                st.rerun()

                    confirm_delete = delete_col.checkbox("Confirm delete", key=f"confirm_delete_{selected_member['id']}")
                    if delete_col.button("Delete member", key="admin_delete_member", use_container_width=True):
                        if not confirm_delete:
                            st.error("Confirm delete first.")
                        else:
                            linked_sessions = member_usage_count(supabase, selected_member["id"])
                            if linked_sessions:
                                st.error("This member cannot be deleted because they already appear in archived sessions.")
                            else:
                                supabase.table("members").delete().eq("id", selected_member["id"]).execute()
                                st.success(f"{selected_member.get('nickname', 'Member')} deleted.")
                                st.rerun()

    with tab_add:
        st.markdown(render_admin_tool_intro("Schedule desk", "Create or edit archive rows", "Use the event tools below to schedule a new row or correct an existing one."), unsafe_allow_html=True)

        if not presets:
            st.warning(
                "No active rows were found in `event_presets`. Add the table and preset rows in Supabase first."
            )
        else:
            event_tool_cols = st.columns([1, 1], gap="small")

            with event_tool_cols[0]:
                with st.popover("Create event row", use_container_width=True):
                    preset_names = [preset["event_name"] for preset in presets]
                    default_start = get_default_event_start()
                    event_date, start_time = render_event_datetime_fields("admin_event", default_start)
                    selected_name = st.selectbox("Event / Setlist", preset_names, key="admin_event_name")
                    selected_preset = resolve_preset(presets, selected_name)
                    event_type = selected_preset["event_type"]
                    event_image_url = selected_preset.get("event_image_url") or ""
                    is_single_member = single_member_event(event_type)

                    st.markdown(
                        f"""
                        <section class="ckt-surface ckt-panel ckt-preset-summary">
                          <div class="ckt-preset-copy">
                            <div class="ckt-kicker">Event details</div>
                            <h2 class="ckt-panel-title">{safe_text(selected_name)}</h2>
                            <div class="ckt-meta-row">
                              <span class="ckt-chip ckt-chip-team">Type {safe_text(event_type)}</span>
                            </div>
                          </div>
                          <div>
                            {
                                f'<div class="ckt-preset-thumb"><img src="{safe_text(event_image_url)}" alt="{safe_text(selected_name)} banner" loading="lazy"></div>'
                                if event_image_url
                                else '<div class="ckt-empty">This preset exists, but its `event_image_url` is still empty in `event_presets`.</div>'
                            }
                          </div>
                        </section>
                        """,
                        unsafe_allow_html=True,
                    )

                    slot_label = "1 slot"
                    if is_single_member:
                        st.info("Birthday and Graduation events use a single member assignment. Slot A/B is not used for this event type.")
                    else:
                        slot_widget = getattr(st, "segmented_control", None)
                        if slot_widget:
                            slot_label = slot_widget(
                                "Slot count",
                                ["1 slot", "2 slots"],
                                default="1 slot",
                                help="Use 2 slots for historical A/B cheki entries in a single event row.",
                                key="admin_event_slot_label",
                            )
                        else:
                            slot_label = st.selectbox(
                                "Slot count",
                                ["1 slot", "2 slots"],
                                help="Use 2 slots for historical A/B cheki entries in a single event row.",
                                key="admin_event_slot_label",
                            )
                    slot_mode = 2 if slot_label == "2 slots" else 1

                    member_a_label = "Assign member" if is_single_member else "Assign Slot A"
                    member_a_help = (
                        "Leave empty if the event member has not been assigned yet."
                        if is_single_member else "Leave empty if Slot A is still waiting for roulette."
                    )
                    selected_member_a = st.selectbox(
                        member_a_label,
                        list(member_options.keys()),
                        help=member_a_help,
                        key="admin_event_member_a_label",
                    )
                    selected_member_b = None
                    if not is_single_member and slot_mode == 2:
                        selected_member_b = st.selectbox(
                            "Assign Slot B",
                            list(member_options.keys()),
                            help="Leave empty if Slot B is still waiting for roulette.",
                            key="admin_event_member_b_label",
                        )

                    if st.button("Save event", key="admin_save_event", use_container_width=True):
                        payload, is_single_member_payload, duration_minutes = build_event_payload(
                            event_date,
                            start_time,
                            selected_preset,
                            slot_mode,
                            member_options[selected_member_a],
                            member_options[selected_member_b] if selected_member_b else None,
                        )
                        supabase.table("chekicha").insert(payload).execute()
                        st.success(
                            f"{selected_name} saved with {'single member assignment' if is_single_member_payload else slot_label.lower()}. "
                            f"Duration set automatically to {duration_minutes} minutes."
                        )
                        st.rerun()

            with event_tool_cols[1]:
                with st.popover("Edit event row", use_container_width=True):
                    if not all_events:
                        st.markdown('<div class="ckt-empty">No saved event rows yet.</div>', unsafe_allow_html=True)
                    else:
                        event_manage_options = {}
                        for event in all_events:
                            start_dt = pd.to_datetime(event["start_time"])
                            label = f"{event['event_name']} | {format_event_date(start_dt)} | {format_event_time(start_dt)}"
                            event_manage_options[label] = event
                        selected_event_label = st.selectbox(
                            "Saved event row",
                            list(event_manage_options.keys()),
                            key="admin_edit_event_label",
                        )
                        selected_event = event_manage_options[selected_event_label]
                        sync_edit_event_state(selected_event)

                        event_start_dt = pd.to_datetime(selected_event["start_time"]).to_pydatetime().replace(second=0, microsecond=0)
                        edit_preset_names = [preset["event_name"] for preset in presets]
                        if selected_event["event_name"] not in edit_preset_names:
                            edit_preset_names = [selected_event["event_name"], *edit_preset_names]

                        edit_event_date, edit_start_time = render_event_datetime_fields("admin_edit_event", event_start_dt)
                        edit_event_name = st.selectbox(
                            "Event / Setlist",
                            edit_preset_names,
                            key="admin_edit_event_name",
                        )
                        edit_preset = resolve_preset(presets, edit_event_name, fallback_event=selected_event)
                        edit_event_type = edit_preset["event_type"]
                        edit_event_image_url = edit_preset.get("event_image_url") or ""
                        edit_is_single_member = single_member_event(edit_event_type)

                        st.markdown(
                            f"""
                            <section class="ckt-surface ckt-panel ckt-preset-summary">
                              <div class="ckt-preset-copy">
                                <div class="ckt-kicker">Editing row</div>
                                <h2 class="ckt-panel-title">{safe_text(edit_event_name)}</h2>
                                <div class="ckt-meta-row">
                                  <span class="ckt-chip ckt-chip-team">Type {safe_text(edit_event_type)}</span>
                                </div>
                              </div>
                              <div>
                                {
                                    f'<div class="ckt-preset-thumb"><img src="{safe_text(edit_event_image_url)}" alt="{safe_text(edit_event_name)} banner" loading="lazy"></div>'
                                    if edit_event_image_url
                                    else '<div class="ckt-empty">This row does not have a preview image yet.</div>'
                                }
                              </div>
                            </section>
                            """,
                            unsafe_allow_html=True,
                        )

                        edit_slot_label = "1 slot"
                        if edit_is_single_member:
                            st.info("Birthday and Graduation events use a single member assignment. Slot A/B is not used for this event type.")
                        else:
                            slot_widget = getattr(st, "segmented_control", None)
                            if slot_widget:
                                edit_slot_label = slot_widget(
                                    "Slot count",
                                    ["1 slot", "2 slots"],
                                    default=st.session_state.get("admin_edit_event_slot_label", "1 slot"),
                                    help="Use 2 slots for historical A/B cheki entries in a single event row.",
                                    key="admin_edit_event_slot_label",
                                )
                            else:
                                edit_slot_label = st.selectbox(
                                    "Slot count",
                                    ["1 slot", "2 slots"],
                                    index=0 if st.session_state.get("admin_edit_event_slot_label", "1 slot") == "1 slot" else 1,
                                    help="Use 2 slots for historical A/B cheki entries in a single event row.",
                                    key="admin_edit_event_slot_label",
                                )
                        edit_slot_mode = 2 if edit_slot_label == "2 slots" else 1

                        edit_member_a = st.selectbox(
                            "Assign member" if edit_is_single_member else "Assign Slot A",
                            member_value_options,
                            format_func=lambda value: member_labels.get(value, "None (Waiting for roulette)"),
                            key="admin_edit_event_member_a",
                        )
                        edit_member_b = None
                        if not edit_is_single_member and edit_slot_mode == 2:
                            edit_member_b = st.selectbox(
                                "Assign Slot B",
                                member_value_options,
                                format_func=lambda value: member_labels.get(value, "None (Waiting for roulette)"),
                                key="admin_edit_event_member_b",
                            )

                        linked_collection_entries = event_collection_usage_count(supabase, selected_event["id"])
                        if linked_collection_entries:
                            st.warning(
                                f"This event is currently referenced by {linked_collection_entries} collection entr{'y' if linked_collection_entries == 1 else 'ies'}, so deletion is blocked."
                            )

                        edit_action_cols = st.columns(2)
                        if edit_action_cols[0].button("Update event", key="admin_update_event", use_container_width=True):
                            payload, edit_is_single_member_payload, duration_minutes = build_event_payload(
                                edit_event_date,
                                edit_start_time,
                                edit_preset,
                                edit_slot_mode,
                                edit_member_a,
                                edit_member_b,
                            )
                            supabase.table("chekicha").update(payload).eq("id", selected_event["id"]).execute()
                            st.success(
                                f"{edit_event_name} updated with {'single member assignment' if edit_is_single_member_payload else edit_slot_label.lower()}. "
                                f"Duration set automatically to {duration_minutes} minutes."
                            )
                            st.rerun()

                        confirm_delete_event = edit_action_cols[1].checkbox(
                            "Confirm delete",
                            key=f"confirm_delete_event_{selected_event['id']}",
                        )
                        if edit_action_cols[1].button("Delete event", key="admin_delete_event", use_container_width=True):
                            if not confirm_delete_event:
                                st.error("Confirm delete first.")
                            elif linked_collection_entries:
                                st.error("This event cannot be deleted because it is already saved in user collections.")
                            else:
                                try:
                                    supabase.table("chekicha").delete().eq("id", selected_event["id"]).execute()
                                except Exception as exc:
                                    st.error(f"Delete failed: {exc}")
                                else:
                                    st.success(f"{selected_event.get('event_name', 'Event')} deleted.")
                                    st.rerun()

    with tab_update:
        st.markdown(
            """
            <section class="ckt-surface ckt-panel ckt-admin-tool-head">
              <div class="ckt-kicker">Primary queue</div>
              <h2 class="ckt-panel-title">Update Roulette Results</h2>
              <p class="ckt-body">Resolve waiting entries first. Slot assignment is the most time-sensitive admin task, so it stays at the front of this workspace.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        tbd_events = [
            event for event in reversed(all_events)
            if (not event.get("member_id_a")) or ((event.get("slot_mode") or 1) == 2 and not event.get("member_id_b"))
        ]

        if tbd_events and members_data:
            waiting_slot_a = sum(1 for event in tbd_events if event_has_waiting_slot_a(event))
            waiting_slot_b = sum(1 for event in tbd_events if event_has_waiting_slot_b(event))

            st.markdown(
                f"""
                <section class="ckt-mini-strip ckt-admin-strip" style="margin-bottom:12px">
                  <div class="ckt-mini-cell">
                    <div class="ckt-meta">Queue size</div>
                    <strong class="ckt-mini-value">{len(tbd_events)}</strong>
                  </div>
                  <div class="ckt-mini-cell">
                    <div class="ckt-meta">Waiting slot A</div>
                    <strong class="ckt-mini-value">{waiting_slot_a}</strong>
                  </div>
                  <div class="ckt-mini-cell">
                    <div class="ckt-meta">Waiting slot B</div>
                    <strong class="ckt-mini-value">{waiting_slot_b}</strong>
                  </div>
                </section>
                """,
                unsafe_allow_html=True,
            )

            option_labels = list(member_options.keys())
            for start_idx in range(0, len(tbd_events), 2):
                event_row = tbd_events[start_idx:start_idx + 2]
                grid_cols = st.columns(2, gap="small")
                for col, event in zip(grid_cols, event_row):
                    start_dt = pd.to_datetime(event["start_time"])
                    slot_mode = event.get("slot_mode") or 1
                    event_type = event.get("event_type")
                    is_single_member = single_member_event(event_type)
                    event_time_copy = safe_text(format_event_time(start_dt))
                    preview = (
                        f'<div class="ckt-admin-queue-thumb"><img src="{safe_text(event["event_image_url"])}" alt="{safe_text(event["event_name"])} banner" loading="lazy"></div>'
                        if event.get("event_image_url")
                        else '<div class="ckt-admin-queue-thumb is-empty"><span>No preview</span></div>'
                    )
                    slot_a_label = member_labels.get(event.get("member_id_a"), "Waiting for roulette")
                    slot_b_label = member_labels.get(event.get("member_id_b"), "Waiting for roulette")

                    with col:
                        st.markdown(
                            f"""
                            <section class="ckt-surface ckt-panel ckt-admin-tool-head ckt-admin-queue-card" style="margin-bottom:8px">
                              <div class="ckt-panel-head ckt-admin-queue-head">
                                <div class="ckt-admin-queue-copy">
                                  <div class="ckt-kicker">Waiting draw</div>
                                  <h2 class="ckt-panel-title">{safe_text(event['event_name'])}</h2>
                                  <div class="ckt-small">{safe_text(format_event_date(start_dt))} | {event_time_copy}</div>
                                </div>
                                {preview}
                              </div>
                              <div class="ckt-meta-row" style="margin-top:10px">
                                <span class="ckt-chip ckt-chip-team">{safe_text(('Member ' if is_single_member else 'Slot A ') + slot_a_label)}</span>
                                {
                                    f'<span class="ckt-chip ckt-chip-team">Slot B {safe_text(slot_b_label)}</span>'
                                    if (not is_single_member and slot_mode == 2) else ""
                                }
                              </div>
                            </section>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown('<div class="ckt-admin-queue-label">Assign result</div>', unsafe_allow_html=True)

                        default_a = member_labels.get(event.get("member_id_a"), "None (Waiting for roulette)")
                        winner_a = st.selectbox(
                            f"Select {'member' if is_single_member else 'Slot A winner'} for {event['event_name']}",
                            option_labels,
                            index=option_labels.index(default_a),
                            key=f"winner_a_{event['id']}",
                            label_visibility="collapsed",
                        )

                        winner_b = None
                        if not is_single_member and slot_mode == 2:
                            st.markdown('<div class="ckt-admin-queue-label">Assign Slot B</div>', unsafe_allow_html=True)
                            default_b = member_labels.get(event.get("member_id_b"), "None (Waiting for roulette)")
                            winner_b = st.selectbox(
                                f"Select Slot B winner for {event['event_name']}",
                                option_labels,
                                index=option_labels.index(default_b),
                                key=f"winner_b_{event['id']}",
                                label_visibility="collapsed",
                            )

                        if st.button("Save result", key=f"update_{event['id']}", use_container_width=True):
                            payload = {
                                "slot_mode": slot_mode,
                                "member_id_a": member_options[winner_a],
                                "member_id_b": member_options[winner_b] if not is_single_member and slot_mode == 2 and winner_b else None,
                            }
                            supabase.table("chekicha").update(payload).eq("id", event["id"]).execute()
                            st.success(f"{event['event_name']} updated. Refresh if you want to re-sort the list immediately.")
        else:
            st.info("No pending roulette events found.")

st.markdown("</div>", unsafe_allow_html=True)
