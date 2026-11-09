# Contexto TFD · 640 palavras · 1332 tokens (o200k_base)

"""Query the shared TFD graph through a reviewed local runtime; never auto-rebuild."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROFILE = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
MAX_OUTPUT = 15998  # Reserve up to two bytes for the host newline.


def settings(path):
    if not path.exists():
        return {}
    if path.is_symlink() or path.stat().st_size > 4096:
        raise ValueError('invalid runtime configuration')
    result = json.loads(path.read_text(encoding='utf-8'))
    python = result.get('python', '')
    distro = result.get('wsl_distribution')
    query_python = result.get('query_python')
    if not isinstance(python, str) or not python.startswith('/') or '\x00' in python:
        raise ValueError('runtime requires an absolute POSIX Python path')
    if distro is not None and (not isinstance(distro, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', distro)):
        raise ValueError('invalid WSL distribution')
    if query_python is not None and (not isinstance(query_python, str) or '\x00' in query_python
                                    or not (query_python.startswith('/') or re.match(r'^[A-Za-z]:[/\\]', query_python))):
        raise ValueError('query runtime requires an absolute Python path')
    return result


def posix_path(path):
    text = str(path).replace('\\', '/')
    if re.match(r'^[A-Za-z]:/', text):
        return '/mnt/' + text[0].lower() + text[2:]
    if not text.startswith('/'):
        raise ValueError('absolute local path required')
    return text


def command(config, action, bundle, index, question):
    if action == 'query' and config.get('query_python'):
        prefix, python = [], config['query_python']
        bundle_path, index_path = str(bundle), str(index)
        adapter = str(bundle / 'integrations/graphify/tfd_graph.py')
    else:
        prefix = ['wsl.exe', '-d', config['wsl_distribution'], '--exec'] if config.get('wsl_distribution') else []
        python = config['python']
        bundle_path, index_path = posix_path(bundle), posix_path(index)
        adapter = bundle_path + '/integrations/graphify/tfd_graph.py'
    result = prefix + [python, '-B', '-X', 'utf8', adapter, action,
                       '--bundle', bundle_path, '--index', index_path, '--graphify-python', python]
    if action == 'query':
        result += ['--query', question]
    return result


def fallback(bundle, index, question):
    spec = importlib.util.spec_from_file_location('tfd_graph_adapter', ROOT / 'integrations/graphify/tfd_graph.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.query(bundle, index, question)


def execute(config, action, bundle, index, question):
    if not config:
        if action == 'rebuild':
            raise ValueError('configure an isolated Graphify runtime before rebuilding')
        return fallback(bundle, index, question)
    try:
        process = subprocess.run(command(config, action, bundle, index, question), capture_output=True,
                                 text=True, encoding='utf-8', errors='replace', timeout=200 if action == 'rebuild' else 35)
        if process.returncode or len(process.stdout.encode('utf-8')) > 16002:
            raise ValueError('nonzero exit or oversized runtime output')
        result = json.loads(process.stdout)
        if not isinstance(result, dict) or 'status' not in result:
            raise ValueError('invalid runtime response')
        return result
    except (OSError, ValueError, RecursionError, subprocess.TimeoutExpired):
        if action == 'rebuild':
            raise ValueError('Graphify runtime failed; index was not confirmed')
        return {**fallback(bundle, index, question), 'runtime_status': 'UNAVAILABLE'}


def render(result):
    value = dict(result)
    if 'sources' in value:
        value['sources'] = list(value['sources'])
    output = json.dumps(value)
    if len(output) <= MAX_OUTPUT:
        return output
    value['output_truncated'] = True
    while value.get('sources') and len(json.dumps(value)) > MAX_OUTPUT:
        value['sources'].pop()
    context = value.get('graph_context', '')
    low, high = 0, len(context)
    while low < high:
        middle = (low + high + 1) // 2
        value['graph_context'] = context[:middle]
        if len(json.dumps(value)) <= MAX_OUTPUT:
            low = middle
        else:
            high = middle - 1
    value['graph_context'] = context[:low]
    output = json.dumps(value)
    if len(output) > MAX_OUTPUT:
        raise ValueError('result metadata exceeds output limit')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('query', 'rebuild'))
    parser.add_argument('question', nargs='?')
    parser.add_argument('--config', type=Path, default=PROFILE / 'tfd-graphify.json')
    parser.add_argument('--bundle', type=Path, default=ROOT)
    parser.add_argument('--index', type=Path, default=PROFILE / 'tfd-graphify/index.json')
    args = parser.parse_args()
    if args.action == 'query' and not args.question:
        parser.error('query requires a question')
    try:
        result = execute(settings(args.config), args.action, args.bundle.absolute(), args.index.absolute(), args.question)
        print(render(result))
    except (OSError, ValueError, TypeError, AttributeError, RecursionError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
