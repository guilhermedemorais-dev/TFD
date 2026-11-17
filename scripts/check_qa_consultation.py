"""Validate QA declarations and local bindings, never source truth or reading compliance."""

import hashlib
import json
from urllib.parse import urlsplit


KINDS = {"business_decision", "guide", "primary"}
STATUSES = {"VERIFIED", "NOT_VERIFIED", "CONTRADICTED", "N/A"}
GUIDE = "/MatthewKerns/software-development-best-practices-guide/"


def text(value):
    return isinstance(value, str) and bool(value.strip())


def ids(value, label):
    if (not isinstance(value, list) or any(not text(item) for item in value)
            or len(set(value)) != len(value)):
        raise ValueError(f"consultation: {label} requires unique nonempty ID strings")
    return set(value)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_consultation(event, root, require_file, target, references, inventory, prd_revision,
                         historical_task=False):
    """references are receipts from real G1/current submissions, not reviewer choices."""
    if not text(event.get("consultation")):
        raise ValueError("consultation: project-relative JSON receipt is required")
    path = require_file(event.get("consultation"), root)
    if digest(path) != event.get("consultation_sha256"):
        raise ValueError("consultation: file hash mismatch")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("consultation: unsupported version")
    if (not text(data.get("reviewed_by"))
            or data["reviewed_by"].strip().casefold() != event["actor"].strip().casefold()
            or data.get("artifact") != target or data.get("revision") != event["revision"]):
        raise ValueError("consultation: reviewer, artifact and revision must match current review")
    if data.get("findings_sha256") != digest(require_file(event.get("evidence"), root)):
        raise ValueError("consultation: findings hash mismatch")
    rows = data.get("references")
    if not isinstance(rows, list):
        raise ValueError("consultation: references must be a list")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not text(row.get("kind")):
            raise ValueError("consultation: reference requires kind")
        kind = row["kind"]
        if kind not in references or kind in seen or not text(row.get("locator")):
            raise ValueError("consultation: invalid/duplicate reference kind or missing locator")
        seen.add(kind)
        if (row.get("path"), row.get("sha256")) != references[kind]:
            raise ValueError(f"consultation: {kind} must match actual approved/current artifact")
        # Task paths are intentionally updated in place after REWORK. Earlier hashes
        # remain submission receipts; only the latest active task can be re-read.
        if not (historical_task and kind == "task"):
            if digest(require_file(row["path"], root)) != row["sha256"]:
                raise ValueError(f"consultation: {kind} reference changed")
    if seen != references.keys():
        raise ValueError("consultation: missing required references")
    approved = data.get("approved_inventory")
    if not isinstance(approved, dict) or set(approved) != {"requirement_ids", "business_rule_ids"}:
        raise ValueError("consultation: approved inventory requires requirements and business rules")
    approved = {key: ids(value, key) for key, value in approved.items()}
    passed = event["verdict"] == "PASS"
    if passed and inventory is not None and any(approved[k] != set(inventory[k]) for k in approved):
        raise ValueError("consultation: target must match independent approved inventory")
    comparison = data.get("comparison")
    if not isinstance(comparison, dict) or not text(comparison.get("observation")):
        raise ValueError("consultation: comparison observation is required")
    for key in ("omitted_ids", "extra_ids", "contradicted_ids"):
        differences = ids(comparison.get(key), key)
        if passed and differences:
            raise ValueError("consultation: PASS cannot have inventory differences or contradictions")
    checks = data.get("checks")
    if not isinstance(checks, list):
        raise ValueError("consultation: checks must be a list")
    seen, business = set(), set()
    for check in checks:
        if not isinstance(check, dict) or any(not text(check.get(key)) for key in
                ("kind", "source", "revision", "locator", "status", "observation", "limits")):
            raise ValueError("consultation: check fields must be nonempty")
        kind, status = check["kind"], check["status"]
        if kind not in KINDS or status not in STATUSES:
            raise ValueError("consultation: invalid check kind/status")
        seen.add(kind)
        claims = ids(check.get("claim_ids"), "claim_ids")
        if (status != "N/A" and not claims) or not claims <= set.union(*approved.values()):
            raise ValueError("consultation: checks must identify approved claim IDs")
        if passed and status not in ("VERIFIED", "N/A"):
            raise ValueError("consultation: unresolved or contradicted required check cannot PASS")
        source = check["source"]
        if source.startswith("https://"):
            parsed = urlsplit(source)
            if (not parsed.hostname or parsed.username or parsed.password or parsed.port
                    or ".." in parsed.path.split("/") or "\\" in source or any(c.isspace() for c in source)):
                raise ValueError("consultation: unsafe source URL")
        else:
            require_file(source, root)
            parsed = None
        if kind == "business_decision":
            if status == "N/A" and approved["business_rule_ids"]:
                raise ValueError("consultation: applicable business rules cannot be N/A")
            if (source not in (references["prd"][0], references["approval"][0])
                    or check["revision"] != prd_revision):
                raise ValueError("consultation: business decision must cite approved G1 revision")
            if status == "VERIFIED":
                business.update(claims)
        if kind == "guide" and status == "VERIFIED":
            revision = check["revision"]
            if (len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision)
                    or parsed is None or parsed.hostname != "github.com"
                    or not any(parsed.path == GUIDE + route + revision
                               or parsed.path.startswith(GUIDE + route + revision + "/")
                               for route in ("blob/", "tree/"))):
                raise ValueError("consultation: guide requires pinned GitHub revision and section locator")
        if kind == "primary" and status == "VERIFIED" and parsed is None:
            raise ValueError("consultation: decisive primary check requires original HTTPS documentation")
    if seen != KINDS:
        raise ValueError("consultation: business_decision, guide and primary checks are required")
    if passed and not approved["business_rule_ids"] <= business:
        raise ValueError("consultation: every approved business rule needs a verified decision check")
