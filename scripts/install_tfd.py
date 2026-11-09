# Contexto TFD · 835 palavras · 1823 tokens (o200k_base)

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
MARKETPLACE = "tfd-local"
PLUGIN = f"the-factory-developer@{MARKETPLACE}"
PACKAGE_DIRS = (
    ".agents", ".codex-plugin", "agents", "docs", "examples",
    "hosts", "library", "schemas", "scripts", "skills",
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


def remote_revision():
    revision, ref = run("git", "ls-remote", "--exit-code", REPOSITORY, "refs/heads/main").split()
    if ref != "refs/heads/main" or not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("GitHub did not return a valid main revision")
    return revision


def setup_source(expected_revision):
    entries = codex("marketplace", "list")["marketplaces"]
    entry = next((item for item in entries if item["name"] == MARKETPLACE), {})
    source = entry.get("marketplaceSource") or {}
    if source.get("sourceType") == "git":
        canonical = source["source"].removesuffix(".git").casefold()
        if canonical not in {REPOSITORY.removesuffix(".git").casefold(), "guilhermedemorais-dev/tfd"}:
            raise ValueError(f"{MARKETPLACE} points to a different Git repository")
        result = codex("marketplace", "upgrade", MARKETPLACE)
        if result["errors"] or len(result["upgradedRoots"]) != 1:
            raise ValueError(f"Could not refresh {MARKETPLACE}: {result['errors']}")
        root = Path(result["upgradedRoots"][0])
    else:
        sparse = [item for path in PACKAGE_DIRS for item in ("--sparse", path)]
        result = codex("marketplace", "add", REPOSITORY, "--ref", "main", *sparse)
        root = Path(result["installedRoot"])

    actual_revision = run("git", "-C", str(root), "rev-parse", "HEAD")
    if actual_revision != expected_revision:
        raise ValueError(f"Marketplace has {actual_revision}, expected {expected_revision}. Check its ref or retry.")
    if (root / "tests").exists():
        raise ValueError(f"{MARKETPLACE} needs a sparse checkout without tests/")
    changes = run("git", "-C", str(root), "status", "--porcelain", "--untracked-files=all")
    if any(line != "?? .codex-marketplace-install.json" for line in changes.splitlines()):
        raise ValueError(f"{MARKETPLACE} contains local changes")
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


def install(profile, venv, revision):
    source = setup_source(revision)
    run(sys.executable, "-B", str(source / "scripts/install_python.py"), "--venv", str(venv))
    run(sys.executable, "-B", str(source / "scripts/install_codex_agents.py"), "--agents-dir", str(profile / "agents"))
    instructions = configure_instructions(profile, (source / RULE).read_text(encoding="utf-8"))
    result = codex("add", PLUGIN)
    installed = Path(result["installedPath"])
    if not (installed / MANIFEST).is_file() or (installed / "tests").exists():
        raise ValueError("Codex did not install the expected TFD package")
    return {
        "installed_revision": revision,
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
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")

    profile = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()
    receipt = profile / "tfd-installation.json"
    try:
        latest = remote_revision()
        status = inspect_installation(receipt, latest)
        if args.action == "install" or (args.action == "update" and status["status"] != "UP_TO_DATE"):
            installed = install(profile, args.venv.expanduser().resolve(), latest)
            atomic_write(receipt, json.dumps(installed, indent=2) + "\n")
            status = {**installed, "status": "INSTALLED", "latest_revision": latest}
        print(json.dumps(status, ensure_ascii=False))
    except (AttributeError, OSError, KeyError, TypeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"TFD setup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
