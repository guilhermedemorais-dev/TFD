"""Package the complete pinned REAP repository without executing upstream code."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REAP = ROOT / "integrations" / "reap"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def git(source, *args):
    result = subprocess.run(
        ["git", "-C", str(source), "--no-pager", *args],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError("Git source inspection failed: " + result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def safe_parts(name):
    """Reject Git paths that escape or alias another file on Windows."""
    parts = name.split("/")
    reserved = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
    if any(
        not part or part in {".", ".."} or part.endswith((".", " "))
        or any(char in part for char in '\\:<>"|?*')
        or any(ord(char) < 32 for char in part)
        or part.split(".", 1)[0].casefold() in reserved
        for part in parts
    ):
        raise ValueError("Unsafe upstream path: " + repr(name))
    return parts


def read_files(source, revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Source revision must be an immutable Git SHA-1")
    if git(source, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("Source HEAD differs from the pinned revision")
    files, aliases = {}, set()
    for entry in git(source, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if not entry:
            continue
        metadata, raw_name = entry.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        name = raw_name.decode("utf-8")
        safe_parts(name)
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError("Unsupported upstream special file: " + name)
        if name.casefold() in aliases:
            raise ValueError("Case-colliding upstream paths: " + name)
        aliases.add(name.casefold())
        files[name] = git(source, "cat-file", "blob", object_id)
    if not files:
        raise ValueError("Pinned source contains no files")
    return files


def normalize_skill(content, folder):
    """Quote only the description scalar; retain original body bytes exactly."""
    lines = content.decode("utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("Skill lacks frontmatter: " + folder)
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("Unclosed skill frontmatter: " + folder)
    names = [line[len("name:"):].strip() for line in lines[1:end] if line.startswith("name:")]
    descriptions = [i for i in range(1, end) if lines[i].startswith("description:")]
    if names != [folder] or len(descriptions) != 1:
        raise ValueError("Ambiguous skill name/description: " + folder)
    position = descriptions[0]
    original = lines[position]
    value = original[len("description:"):].strip()
    if not value or value[:1] in "'\"|>":
        raise ValueError("Expected upstream plain single-line description: " + folder)
    newline = "\r\n" if original.endswith("\r\n") else "\n" if original.endswith("\n") else ""
    lines[position] = "description: " + json.dumps(value, ensure_ascii=False) + newline
    body = "".join(lines[end + 1:]).encode("utf-8")
    return "".join(lines).encode("utf-8"), digest(body)


def reject_linked_parents(path):
    for parent in [path, *path.parents]:
        if not parent.exists() and not parent.is_symlink():
            continue
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Output path has a symlink or reparse-point ancestor")


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def build(source, output, metadata=None, manifest=None):
    metadata = metadata if metadata is not None else json.loads((REAP / "source.json").read_text(encoding="utf-8"))
    manifest = manifest if manifest is not None else json.loads((REAP / "plugin.json").read_text(encoding="utf-8"))
    source = Path(source).resolve()
    output = Path(os.path.abspath(output))
    reject_linked_parents(output)
    if output.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Output must remain outside the TFD bundle")
    if output.exists():
        raise ValueError("Output already exists; existing files were preserved")
    if not output.parent.is_dir():
        raise ValueError("Output parent must already exist")
    if output.is_relative_to(source):
        raise ValueError("Output must remain outside the upstream Git source")
    if manifest.get("skills") != "./skills/" or manifest.get("name") != metadata["plugin"]:
        raise ValueError("Manifest must expose the complete active skills directory")
    if set(manifest) - {"name", "description", "skills", "interface"}:
        raise ValueError("Unexpected plugin execution or integration fields")
    files = read_files(source, metadata["revision"])
    prefix = metadata["upstream_skills_path"] + "/"
    skills = {}
    for name, content in files.items():
        if not name.startswith(prefix):
            continue
        relative = name[len(prefix):]
        parts = safe_parts(relative)
        if len(parts) != 2 or parts[1] != "SKILL.md":
            raise ValueError("Unreviewed skill resource layout: " + name)
        normalized, body_hash = normalize_skill(content, parts[0])
        skills[relative] = (normalized, body_hash, name)
    if len(skills) != metadata["upstream_skill_count"]:
        raise ValueError("Complete upstream skill count does not match the reviewed source")
    if "LICENSE" not in files:
        raise ValueError("Pinned source license is missing")
    provenance = {
        "repository": metadata["repository"], "revision": metadata["revision"],
        "license": metadata["license"],
        "upstream_files": {name: digest(content) for name, content in files.items()},
        "active_skills": {
            name: {"upstream_path": original, "upstream_sha256": digest(files[original]),
                   "active_sha256": digest(content), "body_sha256": body_hash,
                   "normalization": "Quote frontmatter description only; body and name unchanged"}
            for name, (content, body_hash, original) in skills.items()
        },
    }
    temporary = Path(tempfile.mkdtemp(prefix=".reap-build-", dir=output.parent))
    try:
        plugin = temporary / "plugin"
        for name, content in files.items():
            write(plugin.joinpath("upstream", *safe_parts(name)), content)
        for name, (content, _, _) in skills.items():
            write(plugin.joinpath("skills", *safe_parts(name)), content)
        write(plugin / "LICENSE", files["LICENSE"])
        write(plugin / ".codex-plugin/plugin.json", json_bytes(manifest))
        write(plugin / "provenance.json", json_bytes(provenance))
        write(temporary / ".agents/plugins/marketplace.json", json_bytes({
            "name": metadata["marketplace"],
            "interface": {"displayName": "Complete REAP local"},
            "plugins": [{"name": metadata["plugin"], "source": {"source": "local", "path": "./plugin"}}],
        }))
        # Windows rename fails rather than replacing an existing output directory.
        if output.exists():
            raise ValueError("Output appeared during build; existing files were preserved")
        temporary.rename(output)
    except BaseException:
        # Delete only the freshly created, checked sibling directory, never output.
        if (temporary.exists() and temporary.parent == output.parent
                and temporary.resolve().parent == output.parent.resolve()
                and temporary.name.startswith(".reap-build-")):
            reject_linked_parents(temporary)
            shutil.rmtree(temporary)
        raise
    return {"status": "BUILT_NOT_INSTALLED", "marketplace": str(output),
            "plugin": str(output / "plugin"), "revision": metadata["revision"],
            "upstream_files": len(files), "active_skills": len(skills),
            "provenance_sha256": digest(json_bytes(provenance))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.source, args.output), ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
