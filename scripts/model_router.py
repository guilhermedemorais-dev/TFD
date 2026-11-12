# Contexto TFD · 1375 palavras · 2844 tokens (o200k_base)

"""Select an authorized TFD model and check the effective Codex execution separately."""

import argparse
import json
import re
import sys
from pathlib import Path


COMPLEXITIES = {"trivial", "normal", "complex"}
AVAILABILITY = {"AVAILABLE", "UNCONFIGURED", "CONFIGURED", "DEGRADED", "UNAVAILABLE", "ADAPTER_REQUIRED"}
LOCAL_PROVIDERS = {"ollama", "lmstudio"}
MAX_ATTEMPTS = 3
IDENTITY = ("task_id", "contract_revision", "microtask_id", "sector")
ROUTE = ("profile", "provider", "model", "effort")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/@+-]*")


def name(value, field):
    if not isinstance(value, str) or not NAME.fullmatch(value):
        raise ValueError(f"{field} must be a nonempty identifier")
    return value


def evidence(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} requires a nonempty observation or evidence pointer")
    return value


def integer(value, field, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")
    return value


def names(values, field):
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list of identifiers")
    return {name(value, field) for value in values}


def rows(values, field):
    if not isinstance(values, list) or any(not isinstance(value, dict) for value in values):
        raise ValueError(f"{field} must be a list of objects")
    return values


def identity(record):
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    return {key: integer(record.get(key), key, 1) if key == "contract_revision"
            else name(record.get(key), key) for key in IDENTITY}


def read_profiles(values):
    profiles = {}
    routes = set()
    for row in rows(values, "profiles"):
        profile = name(row.get("id"), "profile ID")
        provider, model, effort = (name(row.get(key), key) for key in ROUTE[1:])
        complexities = names(row.get("complexities"), "profile complexities")
        if not complexities or complexities - COMPLEXITIES:
            raise ValueError(f"{profile}: invalid profile complexities")
        if profile in profiles or (provider, model, effort) in routes:
            raise ValueError(f"duplicate authorized profile: {profile}")
        profiles[profile] = dict(provider=provider, model=model, effort=effort, complexities=complexities)
        routes.add((provider, model, effort))
    return profiles


def read_catalog(values):
    catalog = {}
    for row in rows(values, "catalog"):
        key = (name(row.get("provider"), "catalog provider"), name(row.get("model"), "catalog model"))
        if key in catalog:
            raise ValueError(f"duplicate catalog model: {'/'.join(key)}")
        availability = name(row.get("availability"), "availability")
        if availability not in AVAILABILITY:
            raise ValueError(f"invalid availability: {availability}")
        if availability == "AVAILABLE":
            launch = name(row.get("launch"), "launch")
            catalog[key] = dict(availability=availability, launch=launch,
                                evidence=evidence(row.get("evidence"), "catalog evidence"),
                                capabilities=names(row.get("capabilities"), "catalog capabilities"),
                                context_tokens=integer(row.get("context_tokens"), "context_tokens", 1),
                                efforts=names(row.get("efforts"), "catalog efforts"))
        else:
            catalog[key] = dict(availability=availability)
    return catalog


def read_attempts(values, profiles):
    attempts = {}
    for row in rows(values, "attempts"):
        profile = name(row.get("profile"), "attempt profile")
        if profile in attempts or profile not in profiles:
            raise ValueError(f"duplicate or unauthorized attempted profile: {profile}")
        attempts[profile] = evidence(row.get("reason"), "attempt reason")
    return attempts


def supports_launch(launch, provider, coordinator):
    if launch == "native":
        return provider == coordinator
    if launch == "codex_oss":
        return provider in LOCAL_PROVIDERS
    return launch == "codex_provider" and provider != coordinator and provider not in LOCAL_PROVIDERS


def rejection(profile, model, coordinator, complexity, capabilities, minimum):
    if complexity not in profile["complexities"]:
        return "COMPLEXITY_NOT_AUTHORIZED"
    if not model:
        return "MODEL_NOT_OBSERVED"
    if model["availability"] != "AVAILABLE":
        return model["availability"]
    if not supports_launch(model["launch"], profile["provider"], coordinator):
        return "ADAPTER_REQUIRED"
    if not capabilities <= model["capabilities"]:
        return "REQUIRED_CAPABILITY_MISSING"
    if model["context_tokens"] < minimum:
        return "CONTEXT_TOO_SMALL"
    if profile["effort"] not in model["efforts"]:
        return "EFFORT_UNSUPPORTED"
    return None


def select(request):
    result = identity(request)
    complexity = name(request.get("complexity"), "complexity")
    if complexity not in COMPLEXITIES:
        raise ValueError(f"invalid complexity: {complexity}")
    coordinator = name(request.get("coordinator_provider"), "coordinator_provider")
    capabilities = names(request.get("capabilities"), "required capabilities")
    minimum = integer(request.get("min_context_tokens"), "min_context_tokens", 0)
    profiles = read_profiles(request.get("profiles"))
    catalog = read_catalog(request.get("catalog"))
    attempts = read_attempts(request.get("attempts", []), profiles)
    maximum = integer(request.get("max_attempts", MAX_ATTEMPTS), "max_attempts", 1)
    if maximum > MAX_ATTEMPTS:
        raise ValueError(f"max_attempts cannot exceed {MAX_ATTEMPTS}")
    excluded = [dict(profile=profile, reason="PREVIOUS_ATTEMPT", observation=reason)
                for profile, reason in attempts.items()]
    result.update(attempt=len(attempts) + 1, excluded=excluded)
    if len(attempts) >= maximum:
        return {**result, "status": "RETRY_LIMIT", "reason": "ATTEMPT_LIMIT_REACHED", "retryable": False}

    candidates = {key: "COORDINATOR_PROVIDER" for key, value in profiles.items()
                  if value["provider"] == coordinator}
    if "suggested" in request:
        suggested = name(request["suggested"], "suggested profile")
        if suggested in candidates:
            candidates = {suggested: "COORDINATOR_SUGGESTION", **{
                key: reason for key, reason in candidates.items() if key != suggested}}
        else:
            excluded.append(dict(profile=suggested, reason="SUGGESTION_NOT_AUTHORIZED_FOR_COORDINATOR"))
    elif not attempts:
        preferred = (name(request["preferred"], "preferred profile") if "preferred" in request else
                     next((key for key, value in profiles.items() if complexity in value["complexities"]), None))
        if preferred in profiles:
            candidates.pop(preferred, None)
            candidates = {preferred: "PREFERRED_PROFILE", **candidates}
        elif preferred is not None:
            excluded.append(dict(profile=preferred, reason="PROFILE_NOT_AUTHORIZED"))

    for candidate, reason in candidates.items():
        if candidate in attempts:
            continue
        profile = profiles[candidate]
        model = catalog.get((profile["provider"], profile["model"]))
        problem = rejection(profile, model, coordinator, complexity, capabilities, minimum)
        if problem:
            excluded.append(dict(profile=candidate, reason=problem))
            continue
        return {**result, "status": "SELECTED", "profile": candidate, "reason": reason,
                **{key: profile[key] for key in ROUTE[1:]},
                "launch": model["launch"], "catalog_evidence": model["evidence"]}
    return {**result, "status": "UNAVAILABLE", "reason": "NO_ELIGIBLE_PROFILE", "retryable": True}


def verify(selection, observation):
    result = identity(selection)
    if selection.get("status") != "SELECTED":
        raise ValueError("verification requires a selected route")
    result["attempt"] = integer(selection.get("attempt"), "attempt", 1)
    expected = {key: name(selection.get(key), key) for key in ROUTE}
    if not isinstance(observation, dict):
        raise ValueError("observation must be an object")
    missing = [key for key in (*IDENTITY, "attempt", *ROUTE, "evidence") if not observation.get(key)]
    if missing:
        return {**result, "status": "UNCONFIRMED", "missing": missing}
    if identity(observation) != identity(selection) or integer(observation["attempt"], "attempt", 1) != result["attempt"]:
        raise ValueError("observation must match the task, revision, microtask, sector and attempt")
    observed = {key: name(observation[key], key) for key in ROUTE}
    pointer = evidence(observation["evidence"], "host evidence")
    mismatches = [key for key in ROUTE if expected[key] != observed[key]]
    return {**result, "status": "MISMATCH" if mismatches else "VERIFIED", "expected": expected,
            "observed": observed, "mismatches": mismatches, "evidence": pointer}


def observe_codex(selection, path, thread_id, turn_id):
    thread_id, turn_id = name(thread_id, "thread ID"), name(turn_id, "turn ID")
    providers = set()
    routes = set()
    completed = False
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError as exc:
                raise ValueError(f"invalid Codex session JSON on line {number}") from exc
            payload = record.get("payload") if isinstance(record, dict) else None
            if not isinstance(payload, dict):
                continue
            if record.get("type") == "session_meta":
                if payload.get("id") != thread_id:
                    raise ValueError("Codex session does not match the specified thread")
                if payload.get("model_provider") is not None:
                    providers.add(name(payload["model_provider"], "effective provider"))
            elif record.get("type") == "turn_context" and payload.get("turn_id") == turn_id:
                if payload.get("model") is not None and payload.get("effort") is not None:
                    routes.add((name(payload["model"], "effective model"), name(payload["effort"], "effective effort")))
            elif record.get("type") == "event_msg" and payload.get("turn_id") == turn_id:
                if payload.get("type") in {"task_complete", "turn_aborted"}:
                    completed = payload["type"] == "task_complete"
    if len(providers) > 1 or len(routes) > 1:
        raise ValueError("Codex session has conflicting route observations")
    model, effort = next(iter(routes), (None, None)) if completed else (None, None)
    observation = {**identity(selection), "attempt": selection.get("attempt"), "profile": selection.get("profile"),
                   "provider": next(iter(providers), None), "model": model, "effort": effort,
                   "evidence": f"codex:{thread_id}:{turn_id}"}
    return verify(selection, observation)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    choose = commands.add_parser("select")
    choose.add_argument("request", type=Path)
    check = commands.add_parser("verify")
    check.add_argument("selection", type=Path)
    check.add_argument("observation", type=Path, help="normalized host observation or Codex session JSONL")
    check.add_argument("--thread-id", help="expected Codex thread ID for session JSONL")
    check.add_argument("--turn-id", help="expected Codex turn ID for session JSONL")
    args = parser.parse_args()
    try:
        if args.action == "select":
            result = select(load(args.request))
        elif args.thread_id is None and args.turn_id is None:
            result = verify(load(args.selection), load(args.observation))
        else:
            if not args.thread_id or not args.turn_id:
                raise ValueError("Codex session verification requires both --thread-id and --turn-id")
            result = observe_codex(load(args.selection), args.observation, args.thread_id, args.turn_id)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result["status"] in {"SELECTED", "VERIFIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
