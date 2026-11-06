import io
import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from token_usage import summarize


def stream(*events):
    return io.StringIO("\n".join(json.dumps(event) for event in events))


def usage(input_tokens, cached, output, reasoning):
    return dict(input_tokens=input_tokens, cached_input_tokens=cached,
                output_tokens=output, reasoning_output_tokens=reasoning)


def session(kind, **fields):
    return {"type": "event_msg", "payload": {"type": kind, **fields}}


def sample(total, last):
    return session("token_count", info={"total_token_usage": total,
                                       "last_token_usage": last, "model_context_window": 1000})


class TestTokenUsage(unittest.TestCase):
    def test_cli_totals_do_not_double_count_cached_or_reasoning_tokens(self):
        events = stream({"type": "turn.completed", "usage": usage(100, 80, 20, 5)},
                        {"type": "turn.completed", "usage": usage(40, 10, 7, 2)})
        receipt = summarize(events, "COM-1", "G6", 2)
        self.assertEqual(receipt["status"], "measured")
        self.assertEqual(receipt["usage"], {
            **usage(140, 90, 27, 7), "uncached_input_tokens": 50, "total_tokens": 167})

    def test_desktop_uses_deltas_and_skips_duplicate_cumulative_events(self):
        first = usage(100, 80, 20, 5)
        last = usage(40, 10, 7, 2)
        update = sample(usage(140, 90, 27, 7), last)
        events = stream(session("task_started", turn_id="a"), sample(first, first),
                        session("task_complete", turn_id="a"),
                        session("task_started", turn_id="b"), update, update,
                        session("task_complete", turn_id="b"))
        receipt = summarize(events, "COM-1", "G7", 1, "b")
        self.assertEqual(receipt["usage"]["total_tokens"], 47)
        self.assertEqual(receipt["turns"][0]["peak_reported_input_tokens"], 40)
        self.assertEqual(receipt["turns"][0]["model_context_window"], 1000)

    def test_unmeasured_and_aborted_turns_are_not_reported_as_complete(self):
        missing = summarize(stream({"type": "turn.failed"}), "COM-1", "G6", 1)
        self.assertEqual(missing["status"], "unavailable")
        self.assertIsNone(missing["usage"])
        first = usage(100, 80, 20, 5)
        aborted = summarize(stream(session("task_started", turn_id="a"), sample(first, first),
                                   session("turn_aborted", turn_id="a")), "COM-1", "G6", 2, "a")
        self.assertEqual(aborted["status"], "partial")
        self.assertEqual(aborted["usage"]["total_tokens"], 120)

    def test_desktop_requires_selection_across_multiple_turns(self):
        events = stream(session("task_started", turn_id="a"),
                        session("task_complete", turn_id="a"), session("task_started", turn_id="b"))
        with self.assertRaisesRegex(ValueError, "--turn-id"):
            summarize(events, "COM-1", "G7", 1)

    def test_context_warning_uses_last_request_and_rounded_occupancy(self):
        first, last = usage(780, 700, 10, 0), usage(796, 750, 20, 0)
        events = stream(session("task_started", turn_id="a"), sample(first, first),
                        sample(usage(1576, 1450, 30, 0), last),
                        session("task_complete", turn_id="a"), session("task_started", turn_id="b"))
        receipt = summarize(events, "chat", "reply", 1, "b")
        self.assertEqual(receipt["status"], "unavailable")
        self.assertIsNone(receipt["usage"])
        self.assertEqual(receipt["context_window"], {
            "last_input_tokens": 796, "capacity_tokens": 1000, "percent": 80,
            "warn_handoff": True, "observed_turn_id": "a",
        })

    def test_context_warning_clears_after_a_smaller_request(self):
        large, small = usage(900, 800, 10, 0), usage(600, 550, 20, 0)
        events = stream(session("task_started", turn_id="a"), sample(large, large),
                        sample(usage(1500, 1350, 30, 0), small))
        receipt = summarize(events, "chat", "reply", 1, "a")
        self.assertEqual(receipt["usage"]["total_tokens"], 1530)
        self.assertEqual(receipt["context_window"]["percent"], 60)
        self.assertFalse(receipt["context_window"]["warn_handoff"])
