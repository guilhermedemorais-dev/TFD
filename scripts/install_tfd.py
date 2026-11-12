# Contexto TFD · 1230 palavras · 2567 tokens (o200k_base)

"""Install TFD for the active Codex profile or check its published revision."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPOSITORY = "https://github.com/guilhermedemorais-dev/TFD.git"
DEFAULT_REF = "main"
MARKETPLACE = "tfd-local"
PLUGIN = f"the-factory-developer@{MARKETPLACE}"
PACKAGE_DIRS = (
    ".agents", ".codex-plugin", "agents", "docs", "examples",
    "hosts", "integrations", "library", "schemas", "scripts", "skills",
)
MANIFEST = Path(".codex-plugin/plugin.json")
RULE = Path("hosts/codex/automatic-agents.md")
START = "<!-- tfd:begin -->"
END = "<!-- tfd:end -->"


def run(*command):
    result = subprocess.run(
        command, cwd=Path.home(), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=180,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[-1200:]
        raise ValueError(f"{Path(command[0]).name} exited {result.returncode}: {detail}")
    return result.stdout.strip()


def codex(*arguments):
    return json.loads(run("codex", "plugin", *arguments, "--json"))


def remote_revision(ref=DEFAULT_REF):
    branch = f"refs/heads/{ref}"
    run("git", "check-ref-format", branch)
    revision, actual_ref = run("git", "ls-remote", "--exit-code", REPOSITORY, branch).split()
    if actual_ref != branch or not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError(f"GitHub did not return a valid revision for {ref}")
    return revision


def check_marketplace_contents(root):
    if (root / "tests").exists():
        raise ValueError(f"{MARKETPLACE} needs a sparse checkout without tests/")
    changes = run("git", "-C", str(root), "status", "--porcelain", "--untracked-files=all")
    if any(line != "?? .codex-marketplace-install.json" for line in changes.splitlines()):
        raise ValueError(f"{MARKETPLACE} contains local changes; use a preserving update with --source")


def check_installed_cache(profile, root):
    from install_local import snapshot

    row = next((item for item in codex("list")["installed"] if item["pluginId"] == PLUGIN), None)
    if row is None:
        return
    cache_parent = (profile / "plugins/cache" / MARKETPLACE / "the-factory-developer").resolve()
    cache = (cache_parent / row["version"]).resolve()
    if not cache.is_relative_to(cache_parent) or cache == cache_parent:
        raise ValueError("unsafe installed version path")
    if cache.is_dir() and snapshot(cache) != snapshot(root):
        raise ValueError("installed files differ from the marketplace; use a preserving update with --source")


def setup_source(expected_revision, ref=DEFAULT_REF, profile=None):
    entries = codex("marketplace", "list")["marketplaces"]
    entry = next((item for item in entries if item["name"] == MARKETPLACE), {})
    source = entry.get("marketplaceSource") or {}
    if source.get("sourceType") == "git":
        canonical = source["source"].removesuffix(".git").casefold()
        if canonical not in {REPOSITORY.removesuffix(".git").casefold(), "guilhermedemorais-dev/tfd"}:
            raise ValueError(f"{MARKETPLACE} points to a different Git repository")
        current = Path(entry["root"])
        current_ref = run("git", "-C", str(current), "branch", "--show-current")
        if current_ref != ref:
            raise ValueError(f"{MARKETPLACE} is on {current_ref or 'a detached revision'}, expected {ref}; "
                             "use a preserving update with --source")
        check_marketplace_contents(current)
        if profile is not None:
            check_installed_cache(profile, current)
        result = codex("marketplace", "upgrade", MARKETPLACE)
        if result["errors"] or len(result["upgradedRoots"]) != 1:
            raise ValueError(f"Could not refresh {MARKETPLACE}: {result['errors']}")
        root = Path(result["upgradedRoots"][0])
    else:
        if entry:
            raise ValueError(f"{MARKETPLACE} uses a local source; use a preserving update with --source")
        sparse = [item for path in PACKAGE_DIRS for item in ("--sparse", path)]
        result = codex("marketplace", "add", REPOSITORY, "--ref", ref, *sparse)
        root = Path(result["installedRoot"])

    actual_revision = run("git", "-C", str(root), "rev-parse", "HEAD")
    if actual_revision != expected_revision:
        raise ValueError(f"Marketplace has {actual_revision}, expected {expected_revision}. Check its ref or retry.")
    check_marketplace_contents(root)
    return root


def atomic_write(path, contents):
    if path.is_symlink():
        raise ValueError(f"Refusing to replace symbolic link: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(contents.encode("utf-8"))
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def configure_instructions(profile, rule):
    override = profile / "AGENTS.override.md"
    path = override if override.is_file() and override.stat().st_size else profile / "AGENTS.md"
    current = path.read_bytes().decode("utf-8") if path.exists() else ""
    newline = "\r\n" if "\r\n" in current else "\n"
    block = newline.join((START, rule.strip().replace("\n", newline), END))
    before, start, remainder = current.partition(START)
    if start or END in current:
        previous, end, after = remainder.partition(END)
        if not start or not end or START in previous or START in after or END in before or END in after:
            raise ValueError(f"Malformed TFD markers in {path}")
        updated = before + block + after
    elif re.search(r"(?mi)^\ufeff?#{1,6}\s+Tradutor TFD\s*$", current):
        return "existing-section"
    else:
        separator = "" if not current or current.endswith(newline * 2) else newline
        if current and not current.endswith(newline):
            separator += newline
        updated = current + separator + block + newline
    if updated != current:
        atomic_write(path, updated)
    return "managed-section"


def inspect_installation(receipt, latest):
    details = json.loads(receipt.read_text(encoding="utf-8")) if receipt.is_file() else {}
    installed = details.get("installed_path")
    if not installed or not (Path(installed) / MANIFEST).is_file() or (Path(installed) / "tests").exists():
        return {"status": "INSTALL_REQUIRED", "latest_revision": latest}
    status = "UP_TO_DATE" if details["installed_revision"] == latest else "UPDATE_AVAILABLE"
    return {**details, "status": status, "latest_revision": latest}


def install(profile, venv, revision, ref=DEFAULT_REF):
    source = setup_source(revision, ref, profile)
    run(sys.executable, "-B", str(source / "scripts/install_python.py"), "--venv", str(venv))
    run(sys.executable, "-B", str(source / "scripts/install_codex_agents.py"), "--agents-dir", str(profile / "agents"))
    instructions = configure_instructions(profile, (source / RULE).read_text(encoding="utf-8"))
    result = codex("add", PLUGIN)
    installed = Path(result["installedPath"])
    if not (installed / MANIFEST).is_file() or (installed / "tests").exists():
        raise ValueError("Codex did not install the expected TFD package")
    return {
        "installed_revision": revision,
        "installed_ref": ref,
        "version": result["version"],
        "installed_path": str(installed),
        "instructions": instructions,
    }


def default_venv():
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData/Local") / "TFD/python"
    return Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "TFD/python"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "check", "update"))
    parser.add_argument("--venv", type=Path, default=default_venv())
    parser.add_argument("--ref", help="published Git branch to check or install")
    parser.add_argument("--source", type=Path, help="approved local Git source for update")
    parser.add_argument("--base", help="reviewed Git baseline for a preserving local update")
    parser.add_argument("--dry-run", action="store_true", help="plan local update without modifying installation")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")

    profile = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()
    receipt = profile / "tfd-installation.json"
    try:
        local = json.loads(receipt.read_text(encoding="utf-8")) if receipt.is_file() else {}
        if args.ref is not None and (not args.ref or args.source or args.base or args.dry_run):
            raise ValueError("--ref needs a branch and cannot be combined with local update options")
        if args.source or (args.ref is None and local.get("local_source") and args.action in ("check", "update")):
            if args.action == "check":
                print(json.dumps({**local, "status": "LOCAL_INSTALLED"}, ensure_ascii=False))
                return 0
            if args.action != "update":
                raise ValueError("--source is supported for update only")
            from install_local import update_local
            source = args.source or Path(local["local_source"])
            base = args.base or local.get("local_base")
            if not base:
                raise ValueError("local update requires --base with the reviewed baseline")
            result = update_local(profile, source, base, codex, args.dry_run)
            print(json.dumps(result, ensure_ascii=False))
            return 0
        if args.base or args.dry_run:
            raise ValueError("--base and --dry-run require a local --source")
        ref = args.ref or local.get("installed_ref") or DEFAULT_REF
        latest = remote_revision(ref)
        status = {**inspect_installation(receipt, latest), "latest_ref": ref}
        if args.action == "install" or (args.action == "update" and status["status"] != "UP_TO_DATE"):
            if local.get("local_source"):
                raise ValueError("existing local installation needs a preserving update with --source")
            installed = install(profile, args.venv.expanduser().resolve(), latest, ref)
            atomic_write(receipt, json.dumps(installed, indent=2) + "\n")
            status = {**installed, "status": "INSTALLED", "latest_revision": latest, "latest_ref": ref}
        print(json.dumps(status, ensure_ascii=False))
    except (AttributeError, OSError, KeyError, TypeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"TFD setup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
