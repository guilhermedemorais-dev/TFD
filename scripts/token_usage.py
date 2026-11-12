# Contexto TFD · 1193 palavras · 2545 tokens (o200k_base)

"""Export observed Codex token usage as a task/stage receipt."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


COUNTERS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
CONTEXT_WARNING_PERCENT = 80


def counts(usage):
    if not isinstance(usage, dict):
        raise ValueError("missing usage counters")
    result = {key: usage.get(key) for key in COUNTERS}
    if any(type(value) is not int or value < 0 for value in result.values()):
        raise ValueError("usage counters must be nonnegative integers")
    if result["cached_input_tokens"] > result["input_tokens"]:
        raise ValueError("cached input exceeds input")
    return result


def blank(turn_id=None):
    return {"turn_id": turn_id, "status": "incomplete", "usage": None,
            "model_context_window": None, "peak_reported_input_tokens": None, "context_window": None}


def read_turns(stream):
    source = None
    turns = []
    active = None
    previous = None
    unmetered_prefix = False
    for number, line in enumerate(stream, 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise ValueError(f"invalid JSON on line {number}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"expected JSON object on line {number}")
        kind = event.get("type")
        payload = event.get("payload")
        if kind in ("turn.started", "turn.completed", "turn.failed"):
            if source not in (None, "codex_exec"):
                raise ValueError("mixed event formats")
            source = "codex_exec"
            if kind == "turn.started":
                active = blank()
                turns.append(active)
                continue
            if active is None:
                active = blank()
                turns.append(active)
            active["status"] = "completed" if kind == "turn.completed" else "failed"
            if event.get("usage") is not None:
                active["usage"] = counts(event["usage"])
            active = None
        elif kind == "compacted" and isinstance(payload, dict) and active is not None and source == "codex_session":
            active["compaction_events"] = active.get("compaction_events", 0) + 1
            active["context_precedes_compaction"] = True
        elif kind == "event_msg" and isinstance(payload, dict):
            name = payload.get("type")
            if name not in ("task_started", "task_complete", "turn_aborted", "token_count"):
                continue
            if source not in (None, "codex_session"):
                raise ValueError("mixed event formats")
            source = "codex_session"
            if name == "task_started":
                active = blank(payload.get("turn_id"))
                turns.append(active)
                continue
            if name in ("task_complete", "turn_aborted"):
                if active is not None:
                    active["status"] = "completed" if name == "task_complete" else "aborted"
                active = None
                continue
            info = payload.get("info")
            if not isinstance(info, dict) or info.get("total_token_usage") is None:
                continue
            current = counts(info["total_token_usage"])
            last = counts(info["last_token_usage"]) if info.get("last_token_usage") is not None else None
            if previous is None:
                delta = last or current
                if active is not None and last is not None and current != last:
                    active["usage_is_partial"] = True
                elif active is not None and unmetered_prefix and last is None:
                    active["usage_is_partial"] = True
            else:
                delta = {key: current[key] - previous[key] for key in COUNTERS}
                counts(delta)
            previous = current
            if active is not None:
                accumulated = active["usage"] or dict.fromkeys(COUNTERS, 0)
                active["usage"] = {key: accumulated[key] + delta[key] for key in COUNTERS}
                active["model_context_window"] = info.get("model_context_window")
                if last is not None:
                    active["peak_reported_input_tokens"] = max(
                        active["peak_reported_input_tokens"] or 0, last["input_tokens"])
                    window = active["model_context_window"]
                    fresh_request = last["input_tokens"] > 0 and any(delta.values())
                    if (type(window) is int and window > 0
                            and (fresh_request or not active.get("context_precedes_compaction"))):
                        observed = last["input_tokens"]
                        percent = (observed * 100 + window // 2) // window
                        active.pop("context_precedes_compaction", None)
                        active["context_window"] = {
                            "last_input_tokens": observed, "capacity_tokens": window,
                            "percent": percent, "warn_handoff": percent >= CONTEXT_WARNING_PERCENT,
                            "observed_turn_id": active["turn_id"],
                        }
        if turns and active is None and previous is None:
            unmetered_prefix = True
    return source, turns


def summarize(stream, task, stage, attempt, turn_id=None, *, compact_threshold_percent=None):
    if compact_threshold_percent is not None and (
        type(compact_threshold_percent) is not int or not 0 <= compact_threshold_percent <= 100
    ):
        raise ValueError("post-turn compaction threshold must be an integer from 0 to 100")
    source, turns = read_turns(stream)
    context = None
    context_precedes_compaction = False
    if turn_id is not None:
        latest_context = None
        latest_context_precedes_compaction = False
        for turn in turns:
            if turn["context_window"] is not None:
                latest_context = turn["context_window"]
                latest_context_precedes_compaction = False
            latest_context_precedes_compaction |= turn.get("context_precedes_compaction", False)
            if turn["turn_id"] == turn_id:
                context = latest_context
                context_precedes_compaction = latest_context_precedes_compaction
        turns = [turn for turn in turns if turn["turn_id"] == turn_id]
    elif source == "codex_session" and len(turns) > 1:
        raise ValueError("Desktop session has multiple turns; select one with --turn-id")
    elif turns:
        context = turns[-1]["context_window"]
        context_precedes_compaction = turns[-1].get("context_precedes_compaction", False)
    warning_threshold = compact_threshold_percent or CONTEXT_WARNING_PERCENT
    guidance = None
    if context is not None:
        warn = not context_precedes_compaction and context["percent"] >= warning_threshold
        context = {**context, "warn_handoff": warn}
        if warn:
            guidance = "native_configured" if compact_threshold_percent else "manual"
    totals = {key: sum(turn["usage"][key] for turn in turns if turn["usage"] is not None)
              for key in COUNTERS}
    measured = any(turn["usage"] is not None for turn in turns)
    status = "unavailable"
    if measured:
        status = "partial" if any(
            turn["status"] != "completed" or turn["usage"] is None or turn.get("usage_is_partial")
            for turn in turns
        ) else "measured"
    return {
        "schema_version": 1, "source": source, "task": task, "stage": stage,
        "attempt": attempt, "status": status, "turns": turns, "context_window": context,
        "compaction": {
            "post_turn_threshold_percent": compact_threshold_percent,
            "warning_threshold_percent": warning_threshold,
            "observed_events": sum(turn.get("compaction_events", 0) for turn in turns),
            "context_precedes_compaction": context_precedes_compaction and context is not None,
            "guidance": guidance,
        },
        "usage": {
            **totals,
            "uncached_input_tokens": totals["input_tokens"] - totals["cached_input_tokens"],
            "total_tokens": totals["input_tokens"] + totals["output_tokens"],
        } if measured else None,
    }


def read_quota(reader=None, *, live=False):
    if reader is None:
        home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
        readers = list((home / "plugins" / "cache").glob(
            "*/ai-codex-usage/*/skills/codex-usage/scripts/codex_usage.py"))
        if len(readers) != 1:
            raise ValueError("install AI Codex Usage or select its installed script with --quota-reader")
        reader = readers[0]
    command = [sys.executable, "-B", str(reader.resolve()), "--json"]
    if live:
        command.append("--live")
    return subprocess.run(command, check=False, timeout=45).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, nargs="?")
    parser.add_argument("--task")
    parser.add_argument("--stage")
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--turn-id", help="Select one Desktop turn in a session")
    parser.add_argument("--compact-threshold-percent", type=int,
                        help="Confirmed Codex post-turn setting (0 disables it)")
    parser.add_argument("--list-turns", action="store_true", help="List turn IDs and status only")
    parser.add_argument("--quota", action="store_true", help="run the installed AI Codex Usage reader")
    parser.add_argument("--quota-reader", type=Path, help="path to the installed reader if discovery is ambiguous")
    parser.add_argument("--live", action="store_true", help="query account rate limits in quota mode")
    args = parser.parse_args()
    if args.quota:
        if (args.events or args.task or args.stage or args.turn_id or args.list_turns
                or args.compact_threshold_percent is not None):
            parser.error("quota mode is separate from per-run token receipts")
        try:
            return read_quota(args.quota_reader, live=args.live)
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    if args.quota_reader or args.live or args.events is None:
        parser.error("provide an events file or use --quota")
    if args.attempt < 1:
        parser.error("--attempt must be at least 1")
    if args.compact_threshold_percent is not None and (
        args.list_turns or not 0 <= args.compact_threshold_percent <= 100
    ):
        parser.error("--compact-threshold-percent requires a receipt and a value from 0 to 100")
    if not args.list_turns and not (args.task and args.stage):
        parser.error("--task and --stage are required for a receipt")
    try:
        with args.events.open(encoding="utf-8-sig") as stream:
            if args.list_turns:
                _, turns = read_turns(stream)
                print(json.dumps([{key: turn[key] for key in ("turn_id", "status")} for turn in turns]))
                return 0
            receipt = summarize(stream, args.task, args.stage, args.attempt, args.turn_id,
                                compact_threshold_percent=args.compact_threshold_percent)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, ensure_ascii=True, indent=2))
    return 0 if receipt["status"] == "measured" else 2


if __name__ == "__main__":
    raise SystemExit(main())
