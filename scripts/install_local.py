# Contexto TFD · 1256 palavras · 2592 tokens (o200k_base)

"""Preserve installed local TFD extensions while applying a reviewed Git delta."""
import copy
import difflib
import hashlib
import json
import re
import subprocess
import tempfile
import uuid
from pathlib import Path, PurePosixPath

PACKAGE = {'.agents', '.codex-plugin', 'agents', 'docs', 'examples', 'hosts', 'integrations', 'library', 'schemas', 'scripts', 'skills'}


def patch_bytes(old, new, current):
    if current == new:
        return new
    if old is None:
        if current is not None:
            raise ValueError('new source file conflicts with an installed file')
        return new
    if current is None:
        raise ValueError('existing source file is missing from installed package')
    try:
        old, new, actual = [value.decode('utf-8').replace('\r\n', '\n') for value in (old, new, current)]
    except UnicodeDecodeError:
        if current == old:
            return new
        raise ValueError('binary file conflicts with installed content')
    if actual == new:
        return new.encode('utf-8')
    before, after = old.splitlines(True), new.splitlines(True)
    for tag, a, b, c, d in reversed(difflib.SequenceMatcher(a=before, b=after, autojunk=False).get_opcodes()):
        if tag == 'equal':
            continue
        previous, replacement = ''.join(before[a:b]), ''.join(after[c:d])
        if replacement and actual.count(replacement) == 1 and (not previous or not re.search('(?m)^' + re.escape(previous), actual)):
            continue  # This approved block is already applied; retain installed extensions.
        if previous:
            matches = list(re.finditer('(?m)^' + re.escape(previous), actual))
            if len(matches) != 1:
                raise ValueError('ambiguous or conflicting installed block')
            match = matches[0]
            actual = actual[:match.start()] + replacement + actual[match.end():]
        else:
            if a == 0:
                at = 0
            elif a == len(before):
                at = len(actual)
            else:
                prior, following = ''.join(before[max(0, a-3):a]), ''.join(before[a:a+3])
                left = list(re.finditer('(?m)^' + re.escape(prior), actual))
                right = list(re.finditer('(?m)^' + re.escape(following), actual))
                if len(left) == 1:
                    at = left[0].end()
                elif len(right) == 1:
                    at = right[0].start()
                else:
                    raise ValueError('ambiguous installed insertion')
            actual = actual[:at] + replacement + actual[at:]
    return actual.encode('utf-8')


def git(source, *args):
    result = subprocess.run(['git', '-C', str(source), *args], capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout


def snapshot(root):
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'symlink not supported in local package: {path}')
        if path.is_file() and '.git' not in path.relative_to(root).parts:
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def strict_compatibility(files):
    script, schema_path = 'scripts/workflow_contract.py', 'schemas/workflow.json'
    if script not in files or schema_path not in files:
        return
    schema = json.loads(files[schema_path])
    defs = schema['$defs']
    defs['workflow']['properties']['preparation'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['mode', 'authorization'],
        'properties': {'mode': {'enum': ['reviewed_task']}, 'authorization': {'type': 'string', 'pattern': r'\S'}}}
    defs['complete'] = copy.deepcopy(defs['approve'])
    defs['complete']['properties']['action'] = {'enum': ['complete']}
    defs['complete']['properties']['gate'] = {'enum': ['G2', 'G3', 'G4', 'G5']}
    text = files[script].decode('utf-8')
    old, new = '("submit", "review", "approve", "block")', '("submit", "review", "approve", "block", "complete")'
    if old in text:
        if text.count(old) != 1:
            raise ValueError('ambiguous strict workflow adapter')
        text = text.replace(old, new, 1)
    elif new not in text:
        raise ValueError('unsupported installed strict workflow adapter')
    files[script] = text.encode('utf-8')
    files[schema_path] = (json.dumps(schema, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def prepare(source, base, origin, cache):
    source, origin, cache = [Path(path).resolve() for path in (source, origin, cache)]
    for root in (source, origin, cache):
        manifest = json.loads((root / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        if manifest['name'] != 'the-factory-developer':
            raise ValueError('unexpected local package identity')
    base = git(source, 'rev-parse', '--verify', base + '^{commit}').decode().strip()
    original, installed = snapshot(origin), snapshot(cache)
    files = {**original, **installed}
    changed = git(source, 'diff', base, '--name-only', '-z').decode().split('\0')
    changed += git(source, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    selected = []
    for name in sorted(set(changed)):
        path = PurePosixPath(name)
        if not name or path.is_absolute() or '..' in path.parts or '\\' in name:
            continue
        if path.parts[0] not in PACKAGE and name not in {'README.md', 'LICENSE', 'requirements.txt'}:
            continue
        if name.startswith('docs/office/') or '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        src = source / path
        if src.is_symlink() or not src.resolve().is_relative_to(source):
            raise ValueError('unsafe source path')
        if not src.is_file():
            raise ValueError('local update does not delete package files: ' + name)
        if name == 'library/indexes/resources.json':
            continue
        old_result = subprocess.run(['git', '-C', str(source), 'show', base + ':' + name], capture_output=True)
        old = old_result.stdout if old_result.returncode == 0 else None
        left, right = original.get(name), installed.get(name)
        normalize = lambda value: value.replace(b'\r\n', b'\n') if value is not None else None
        if left != right and left is not None and right is not None:
            if normalize(left) == normalize(old):
                current = right
            elif normalize(right) == normalize(old):
                current = left
            elif normalize(left) == normalize(right):
                current = right
            else:
                raise ValueError('origin/cache customizations conflict: ' + name)
        else:
            current = right if right is not None else left
        try:
            files[name] = patch_bytes(old, src.read_bytes(), current)
        except ValueError as exc:
            raise ValueError(name + ': ' + str(exc)) from exc
        selected.append(name)
    strict_compatibility(files)
    index_path = 'library/indexes/resources.json'
    index = json.loads(files[index_path])
    for resource in index['resources']:
        name = 'library/' + resource['path']
        if name in selected:
            resource['sha256'] = hashlib.sha256(files[name]).hexdigest()
    files[index_path] = (json.dumps(index, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    changes = [(root / name, previous.get(name), data) for root, previous in ((origin, original), (cache, installed))
               for name, data in files.items() if previous.get(name) != data]
    return changes, base, files


def atomic_bytes(path, data):
    if path.is_symlink():
        raise ValueError('refusing symlink overwrite: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(data)
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def update_local(profile, source, base, codex, dry_run=False):
    profile, source = Path(profile).resolve(), Path(source).resolve()
    rows = codex('list')['installed']
    row = next((row for row in rows if row['pluginId'] == 'the-factory-developer@tfd-local'), None)
    if not row or row.get('source', {}).get('source') != 'local':
        raise ValueError('local update requires an installed local tfd-local plugin')
    origin = Path(row['source']['path']).resolve()
    cache_parent = profile / 'plugins/cache/tfd-local/the-factory-developer'
    cache = (cache_parent / row['version']).resolve()
    if not cache.is_relative_to(cache_parent.resolve()):
        raise ValueError('unsafe installed version path')
    changes, base, files = prepare(source, base, origin, cache)
    digest = hashlib.sha256(''.join(name + hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())).encode()).hexdigest()
    result = {'status': 'LOCAL_PLAN' if dry_run else 'LOCAL_INSTALLED', 'installed_path': str(cache),
              'version': row['version'], 'installed_revision': git(source, 'rev-parse', 'HEAD').decode().strip(),
              'local_source': str(source), 'local_base': base, 'content_sha256': digest,
              'changed_files': [str(path) for path, _, _ in changes]}
    if dry_run:
        return result
    backup = profile / 'tfd-local-backups' / uuid.uuid4().hex
    backup.mkdir(parents=True)
    old_receipt = profile / 'tfd-installation.json'
    receipt_before = old_receipt.read_bytes() if old_receipt.exists() else None
    for index, (_, before, _) in enumerate(changes):
        if before is not None:
            (backup / str(index)).write_bytes(before)
    manifest = [{'path': str(path), 'backup': str(index) if before is not None else None,
                 'before_sha256': hashlib.sha256(before).hexdigest() if before is not None else None,
                 'after_sha256': hashlib.sha256(after).hexdigest()} for index, (path, before, after) in enumerate(changes)]
    (backup / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    for path, before, _ in changes:
        if (path.read_bytes() if path.exists() else None) != before:
            raise ValueError('installation changed during preparation: ' + str(path))
    applied = []
    try:
        for path, before, after in changes:
            applied.append((path, before))
            atomic_bytes(path, after)
        result['backup_path'] = str(backup)
        atomic_bytes(old_receipt, (json.dumps(result, indent=2) + '\n').encode('utf-8'))
    except Exception:
        for path, before in reversed(applied):
            if before is None:
                path.unlink(missing_ok=True)
            else:
                atomic_bytes(path, before)
        if receipt_before is None:
            old_receipt.unlink(missing_ok=True)
        else:
            atomic_bytes(old_receipt, receipt_before)
        raise
    return result
