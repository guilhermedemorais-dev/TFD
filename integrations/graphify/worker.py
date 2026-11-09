# Contexto TFD · 769 palavras · 1627 tokens (o200k_base)

# MIT License
#
# Copyright (c) 2026 Guilherme de Morais
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Pinned upstream API bridge. Executed only in an explicitly selected venv."""
import contextlib
import ctypes
from ctypes import wintypes
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys


class JobBasicLimits(ctypes.Structure):
    _fields_ = [('PerProcessUserTimeLimit', ctypes.c_longlong),
                ('PerJobUserTimeLimit', ctypes.c_longlong), ('LimitFlags', wintypes.DWORD),
                ('MinimumWorkingSetSize', ctypes.c_size_t), ('MaximumWorkingSetSize', ctypes.c_size_t),
                ('ActiveProcessLimit', wintypes.DWORD), ('Affinity', ctypes.c_size_t),
                ('PriorityClass', wintypes.DWORD), ('SchedulingClass', wintypes.DWORD)]


class IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in
                ('ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
                 'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]


class JobExtendedLimits(ctypes.Structure):
    _fields_ = [('BasicLimitInformation', JobBasicLimits), ('IoInfo', IoCounters),
                ('ProcessMemoryLimit', ctypes.c_size_t), ('JobMemoryLimit', ctypes.c_size_t),
                ('PeakProcessMemoryUsed', ctypes.c_size_t), ('PeakJobMemoryUsed', ctypes.c_size_t)]


def windows_limits(kernel=None):
    """Apply real Job Object limits; retain the returned handle until process exit."""
    if kernel is None:
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.SetInformationJobObject.restype = wintypes.BOOL
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise ValueError('Windows resource limits could not be created')
    limits = JobExtendedLimits()
    # JOB_OBJECT_LIMIT_PROCESS_TIME | JOB_OBJECT_LIMIT_PROCESS_MEMORY.
    limits.BasicLimitInformation.LimitFlags = 0x00000002 | 0x00000100
    limits.BasicLimitInformation.PerProcessUserTimeLimit = 120 * 10_000_000
    limits.ProcessMemoryLimit = 2_000_000_000
    if not kernel.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
        kernel.CloseHandle(job)
        raise ValueError('Windows resource limits could not be configured')
    if not kernel.AssignProcessToJobObject(job, kernel.GetCurrentProcess()):
        kernel.CloseHandle(job)
        raise ValueError('Windows resource limits could not be assigned')
    # No KILL_ON_JOB_CLOSE: the worker owns this handle and the OS closes it on exit.
    return job


def apply_limits():
    if os.name == 'nt':
        return windows_limits()
    import resource
    resource.setrlimit(resource.RLIMIT_FSIZE, (64_000_000, 64_000_000))
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    return None


def validate_operation(request):
    if not isinstance(request, dict) or request.get('operation') not in ('build', 'query'):
        raise ValueError('unsupported operation')
    if os.name == 'nt' and request['operation'] != 'query':
        raise ValueError('native Windows worker is query-only; rebuild requires POSIX')


def verify_pin():
    pin = json.loads(Path(__file__).with_name("pin.json").read_text())
    distribution = importlib.metadata.distribution(pin['distribution'])
    package = Path(distribution.locate_file('graphify'))
    if package.is_symlink() or package.resolve() != package:
        raise ValueError('Graphify package symlinks are forbidden')
    if distribution.version != pin["version"]:
        raise ValueError("unsupported Graphify version")
    actual = hashlib.sha256()
    for path in sorted(package.rglob("*.py")):
        if path.is_symlink() or path.resolve() != path:
            raise ValueError('Graphify source symlinks are forbidden')
        actual.update(path.relative_to(package).as_posix().encode() + b"\0" + path.read_bytes())
    if actual.hexdigest() != pin["python_source_sha256"]:
        raise ValueError("Graphify source differs from reviewed pin")


def main():
    job_handle = apply_limits()  # Kept alive for the entire worker process.
    request = json.load(sys.stdin)
    validate_operation(request)
    verify_pin()  # All installed Python sources are hashed before any Graphify import.
    with contextlib.redirect_stdout(sys.stderr):
        result = execute(request)
    if request['operation'] == 'query':
        if not isinstance(result, str):
            raise ValueError('unsupported query result')
        result = result.encode('utf-8')[:6000].decode('utf-8', errors='ignore')
    json.dump(result, sys.stdout, ensure_ascii=False)


def execute(request):
    validate_operation(request)
    from networkx.readwrite import json_graph
    if request["operation"] == "build":
        from graphify.extract import extract
        from graphify.build import build
        root = Path(request["root"])
        extracted = extract([root / p for p in request["paths"]], root=root,
                            cache_root=Path(request["cache"]), parallel=False)
        graph = build([extracted], directed=True, dedup=False, root=root)
        result = json_graph.node_link_data(graph, edges="links")
    else:
        from graphify.serve import _query_graph_text
        graph = json_graph.node_link_graph(request["graph"], edges="links")
        result = _query_graph_text(graph, request["query"], depth=2, token_budget=1200)
    return result


if __name__ == "__main__":
    main()
