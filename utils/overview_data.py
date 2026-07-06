import pandas as pd


SPECIAL_EVENT_TYPES = {"Birthday", "Graduation"}


def relation_to_member(value):
    if isinstance(value, list):
        return value[0] if value else {}
    return value or {}


def is_show_event(event_type: str | None) -> bool:
    return event_type not in SPECIAL_EVENT_TYPES


def build_overview_snapshot(event_rows, recent_limit: int = 5):
    show_event_sessions = 0
    birthday_sessions = 0
    graduation_sessions = 0
    pending_slots = 0
    assignments = []
    latest_show_event = None

    for row in event_rows:
        event_type = row.get("event_type")
        slot_mode = row.get("slot_mode") or 1
        start_time = pd.to_datetime(row["start_time"])

        if event_type == "Birthday":
            birthday_sessions += 1
        elif event_type == "Graduation":
            graduation_sessions += 1
        else:
            show_event_sessions += 1
            if latest_show_event is None or start_time > latest_show_event:
                latest_show_event = start_time

        member_a = relation_to_member(row.get("member_a"))
        member_b = relation_to_member(row.get("member_b"))

        if not row.get("member_id_a"):
            pending_slots += 1
        elif is_show_event(event_type):
            assignments.append(
                {
                    "member_id": row.get("member_id_a") or row.get("id") or row.get("event_name"),
                    "nickname": member_a.get("nickname", "Unknown member"),
                    "avatar_url": member_a.get("avatar_url"),
                    "generasi": member_a.get("generasi"),
                    "event_name": row.get("event_name", "Untitled event"),
                    "event_type": event_type or "Roulette",
                    "start_time": row.get("start_time"),
                    "start_dt": start_time,
                    "slot_key": "A",
                }
            )

        if slot_mode == 2:
            if not row.get("member_id_b"):
                pending_slots += 1
            elif is_show_event(event_type):
                assignments.append(
                    {
                        "member_id": row.get("member_id_b") or row.get("id") or row.get("event_name"),
                        "nickname": member_b.get("nickname", "Unknown member"),
                        "avatar_url": member_b.get("avatar_url"),
                        "generasi": member_b.get("generasi"),
                        "event_name": row.get("event_name", "Untitled event"),
                        "event_type": event_type or "Roulette",
                        "start_time": row.get("start_time"),
                        "start_dt": start_time,
                        "slot_key": "B",
                    }
                )

    leaderboard_map = {}
    for item in assignments:
        entry = leaderboard_map.setdefault(
            item["member_id"],
            {
                "member_id": item["member_id"],
                "nickname": item["nickname"],
                "avatar_url": item.get("avatar_url"),
                "generasi": item.get("generasi"),
                "count": 0,
                "last_seen": item["start_dt"],
            },
        )
        entry["count"] += 1
        if item["start_dt"] > entry["last_seen"]:
            entry["last_seen"] = item["start_dt"]
            entry["avatar_url"] = item.get("avatar_url")
            entry["generasi"] = item.get("generasi")
            entry["nickname"] = item["nickname"]

    leaderboard = sorted(
        leaderboard_map.values(),
        key=lambda item: (-item["count"], -item["last_seen"].timestamp(), item["nickname"]),
    )
    recent_assignments = sorted(assignments, key=lambda item: item["start_dt"], reverse=True)[:recent_limit]

    return {
        "show_event_sessions": show_event_sessions,
        "birthday_sessions": birthday_sessions,
        "graduation_sessions": graduation_sessions,
        "assigned_show_event_slots": len(assignments),
        "pending_slots": pending_slots,
        "latest_show_event": latest_show_event,
        "leaderboard": leaderboard,
        "recent_assignments": recent_assignments,
    }
