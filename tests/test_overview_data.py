import unittest

from utils.overview_data import build_overview_snapshot


class OverviewDataTests(unittest.TestCase):
    def test_build_overview_snapshot_filters_special_events_and_breaks_ties_by_latest_start_time(self):
        rows = [
            {
                "id": "event-1",
                "event_name": "Ramune",
                "event_type": "Roulette",
                "start_time": "2026-06-01T10:00:00",
                "slot_mode": 2,
                "member_id_a": "member-a",
                "member_id_b": "member-b",
                "member_a": {"nickname": "Alice", "avatar_url": "alice.png", "generasi": "1"},
                "member_b": {"nickname": "Bella", "avatar_url": "bella.png", "generasi": "2"},
            },
            {
                "id": "event-2",
                "event_name": "Cara Meminum Ramune",
                "event_type": "Roulette",
                "start_time": "2026-06-05T10:00:00",
                "slot_mode": 1,
                "member_id_a": "member-a",
                "member_id_b": None,
                "member_a": {"nickname": "Alice", "avatar_url": "alice.png", "generasi": "1"},
                "member_b": None,
            },
            {
                "id": "event-3",
                "event_name": "Aturan Anti Cinta",
                "event_type": "Roulette",
                "start_time": "2026-06-07T10:00:00",
                "slot_mode": 1,
                "member_id_a": "member-b",
                "member_id_b": None,
                "member_a": {"nickname": "Bella", "avatar_url": "bella.png", "generasi": "2"},
                "member_b": None,
            },
            {
                "id": "event-4",
                "event_name": "Birthday Momo",
                "event_type": "Birthday",
                "start_time": "2026-06-09T10:00:00",
                "slot_mode": 1,
                "member_id_a": "member-c",
                "member_id_b": None,
                "member_a": {"nickname": "Cindy", "avatar_url": "cindy.png", "generasi": "3"},
                "member_b": None,
            },
            {
                "id": "event-5",
                "event_name": "Graduation Gala",
                "event_type": "Graduation",
                "start_time": "2026-06-10T10:00:00",
                "slot_mode": 1,
                "member_id_a": None,
                "member_id_b": None,
                "member_a": None,
                "member_b": None,
            },
        ]

        snapshot = build_overview_snapshot(rows)

        self.assertEqual(snapshot["show_event_sessions"], 3)
        self.assertEqual(snapshot["birthday_sessions"], 1)
        self.assertEqual(snapshot["graduation_sessions"], 1)
        self.assertEqual(snapshot["assigned_show_event_slots"], 4)
        self.assertEqual(snapshot["pending_slots"], 1)

        leaderboard = snapshot["leaderboard"]
        self.assertEqual([row["nickname"] for row in leaderboard[:2]], ["Bella", "Alice"])
        self.assertEqual([row["count"] for row in leaderboard[:2]], [2, 2])

        recent = snapshot["recent_assignments"]
        self.assertEqual([row["nickname"] for row in recent], ["Bella", "Alice", "Alice", "Bella"])
        self.assertEqual(
            [row["event_name"] for row in recent],
            ["Aturan Anti Cinta", "Cara Meminum Ramune", "Ramune", "Ramune"],
        )

    def test_build_overview_snapshot_keeps_both_slots_from_same_event_in_recent_items(self):
        rows = [
            {
                "id": "event-6",
                "event_name": "Pajama Drive",
                "event_type": "Roulette",
                "start_time": "2026-06-11T20:00:00",
                "slot_mode": 2,
                "member_id_a": "member-a",
                "member_id_b": "member-b",
                "member_a": {"nickname": "Alice", "avatar_url": None, "generasi": None},
                "member_b": {"nickname": "Bella", "avatar_url": None, "generasi": None},
            }
        ]

        snapshot = build_overview_snapshot(rows)

        self.assertEqual(len(snapshot["recent_assignments"]), 2)
        self.assertEqual({row["slot_key"] for row in snapshot["recent_assignments"]}, {"A", "B"})


if __name__ == "__main__":
    unittest.main()
