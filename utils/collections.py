import pandas as pd

from utils.auth import current_user


def count_pending_slots(rows):
    pending = 0
    for row in rows:
        slot_mode = row.get("slot_mode") or 1
        if not row.get("member_id_a"):
            pending += 1
        if slot_mode == 2 and not row.get("member_id_b"):
            pending += 1
    return pending


def load_collectible_slots(supabase_client):
    rows = (
        supabase_client.table("chekicha")
        .select(
            "id, event_name, event_type, start_time, event_image_url, slot_mode, "
            "member_id_a, member_id_b, "
            "member_a:member_id_a(nickname, avatar_url, generasi), "
            "member_b:member_id_b(nickname, avatar_url, generasi)"
        )
        .order("start_time", desc=True)
        .execute()
        .data
        or []
    )

    slots = []
    for row in rows:
        dt = pd.to_datetime(row["start_time"])
        slot_mode = row.get("slot_mode") or 1
        member_a = row.get("member_a")
        member_b = row.get("member_b")

        if member_a:
            slot_label = "Member" if row.get("event_type") in {"Birthday", "Graduation"} else "Slot A"
            slots.append(
                {
                    "slot_uid": f'{row["id"]}:A',
                    "event_id": row["id"],
                    "slot_key": "A",
                    "slot_label": slot_label,
                    "event_name": row.get("event_name", "Untitled event"),
                    "event_type": row.get("event_type", "Roulette"),
                    "start_time": row["start_time"],
                    "event_image_url": row.get("event_image_url"),
                    "member_id": row.get("member_id_a"),
                    "member_name": member_a.get("nickname", "Unknown member"),
                    "member_avatar_url": member_a.get("avatar_url"),
                    "member_generasi": member_a.get("generasi"),
                    "display_label": f'{row.get("event_name", "Untitled event")} | {dt.day} {dt:%b %Y} | {slot_label} | {member_a.get("nickname", "Unknown member")}',
                }
            )

        if slot_mode == 2 and member_b:
            slots.append(
                {
                    "slot_uid": f'{row["id"]}:B',
                    "event_id": row["id"],
                    "slot_key": "B",
                    "slot_label": "Slot B",
                    "event_name": row.get("event_name", "Untitled event"),
                    "event_type": row.get("event_type", "Roulette"),
                    "start_time": row["start_time"],
                    "event_image_url": row.get("event_image_url"),
                    "member_id": row.get("member_id_b"),
                    "member_name": member_b.get("nickname", "Unknown member"),
                    "member_avatar_url": member_b.get("avatar_url"),
                    "member_generasi": member_b.get("generasi"),
                    "display_label": f'{row.get("event_name", "Untitled event")} | {dt.day} {dt:%b %Y} | Slot B | {member_b.get("nickname", "Unknown member")}',
                }
            )

    return slots


def load_user_collection_entries(auth_client, public_client):
    user = current_user()
    if user is None:
        return []

    rows = (
        auth_client.table("user_collection_entries")
        .select("id, event_id, slot_key, member_id, quantity, created_at, updated_at")
        .eq("user_id", user.id)
        .order("updated_at", desc=True)
        .execute()
        .data
        or []
    )
    if not rows:
        return []

    event_ids = list({row["event_id"] for row in rows})
    member_ids = list({row["member_id"] for row in rows})

    event_rows = (
        public_client.table("chekicha")
        .select("id, event_name, event_type, start_time")
        .in_("id", event_ids)
        .execute()
        .data
        or []
    )
    member_rows = (
        public_client.table("members")
        .select("id, nickname, avatar_url, generasi")
        .in_("id", member_ids)
        .execute()
        .data
        or []
    )

    events_by_id = {row["id"]: row for row in event_rows}
    members_by_id = {row["id"]: row for row in member_rows}

    entries = []
    for row in rows:
        event = events_by_id.get(row["event_id"], {})
        member = members_by_id.get(row["member_id"], {})
        entries.append(
            {
                **row,
                "event_name": event.get("event_name", "Archived event"),
                "event_type": event.get("event_type", "Roulette"),
                "start_time": event.get("start_time"),
                "member_name": member.get("nickname", "Unknown member"),
                "member_avatar_url": member.get("avatar_url"),
                "member_generasi": member.get("generasi"),
            }
        )
    return entries


def add_collection_quantity(auth_client, slot, quantity: int):
    user = current_user()
    if user is None:
        raise ValueError("User session is missing.")

    response = (
        auth_client.table("user_collection_entries")
        .select("id, quantity")
        .eq("user_id", user.id)
        .eq("event_id", slot["event_id"])
        .eq("slot_key", slot["slot_key"])
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if rows:
        entry = rows[0]
        auth_client.table("user_collection_entries").update(
            {
                "quantity": int(entry.get("quantity") or 0) + quantity,
            }
        ).eq("id", entry["id"]).execute()
        return "updated"

    auth_client.table("user_collection_entries").insert(
        {
            "user_id": user.id,
            "event_id": slot["event_id"],
            "slot_key": slot["slot_key"],
            "member_id": slot["member_id"],
            "quantity": quantity,
        }
    ).execute()
    return "created"


def update_collection_quantity(auth_client, entry_id, quantity: int):
    user = current_user()
    if user is None:
        raise ValueError("User session is missing.")
    auth_client.table("user_collection_entries").update({"quantity": quantity}).eq("id", entry_id).eq("user_id", user.id).execute()


def delete_collection_entry(auth_client, entry_id):
    user = current_user()
    if user is None:
        raise ValueError("User session is missing.")
    auth_client.table("user_collection_entries").delete().eq("id", entry_id).eq("user_id", user.id).execute()
