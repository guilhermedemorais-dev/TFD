# Contexto TFD · 540 palavras · 1299 tokens (o200k_base)

"""Native worker resource limits and query-only operation guards."""
import importlib.util
import io
import json
import mmap
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, call, patch


MODULE = Path(__file__).resolve().parents[1] / 'integrations/graphify/worker.py'
spec = importlib.util.spec_from_file_location('graphify_worker', MODULE)
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)


class GraphifyWorkerTests(unittest.TestCase):
    def test_windows_build_rejected_before_importing_upstream(self):
        with patch.object(worker.os, 'name', 'nt'):
            with self.assertRaisesRegex(ValueError, 'query-only'):
                worker.execute({'operation': 'build'})

    def test_unknown_operation_rejected_before_importing_upstream(self):
        with self.assertRaisesRegex(ValueError, 'unsupported operation'):
            worker.execute({'operation': 'install'})

    def test_query_output_capped_before_json_dump(self):
        for text in ('x' * 12000, '\N{EURO SIGN}' + '\N{SLIGHTLY SMILING FACE}' * 4000):
            with self.subTest(multibyte=not text.isascii()):
                output = io.StringIO()
                with (patch.object(worker, 'apply_limits', return_value=123),
                      patch.object(worker, 'verify_pin'),
                      patch.object(worker, 'execute', return_value=text),
                      patch.object(worker.sys, 'stdin', io.StringIO('{"operation":"query"}')),
                      patch.object(worker.sys, 'stdout', output)):
                    worker.main()
                self.assertLessEqual(len(json.loads(output.getvalue()).encode('utf-8')), 6000)

    def test_limit_failure_prevents_pin_verification_and_execution(self):
        with (patch.object(worker, 'apply_limits', side_effect=ValueError('limit failed')),
              patch.object(worker, 'verify_pin') as verify,
              patch.object(worker, 'execute') as execute):
            with self.assertRaisesRegex(ValueError, 'limit failed'):
                worker.main()
        verify.assert_not_called()
        execute.assert_not_called()

    def test_pin_failure_prevents_upstream_execution(self):
        with (patch.object(worker, 'apply_limits', return_value=123),
              patch.object(worker, 'verify_pin', side_effect=ValueError('source differs')),
              patch.object(worker.sys, 'stdin', io.StringIO('{"operation":"query"}')),
              patch.object(worker, 'execute') as execute):
            with self.assertRaisesRegex(ValueError, 'source differs'):
                worker.main()
        execute.assert_not_called()

    def test_posix_keeps_all_three_existing_limits(self):
        resource = Mock(RLIMIT_FSIZE=1, RLIMIT_AS=2, RLIMIT_CPU=3)
        with patch.object(worker.os, 'name', 'posix'), patch.dict(sys.modules, resource=resource):
            self.assertIsNone(worker.apply_limits())
        self.assertEqual(resource.setrlimit.call_args_list, [call(1, (64_000_000, 64_000_000)),
                         call(2, (2_000_000_000, 2_000_000_000)), call(3, (120, 120))])

    def test_windows_job_creation_configuration_assignment_fail_closed(self):
        for failed in ('CreateJobObjectW', 'SetInformationJobObject', 'AssignProcessToJobObject'):
            with self.subTest(failed=failed):
                kernel = Mock()
                kernel.CreateJobObjectW.return_value = 123
                kernel.SetInformationJobObject.return_value = 1
                kernel.AssignProcessToJobObject.return_value = 1
                kernel.GetCurrentProcess.return_value = 456
                getattr(kernel, failed).return_value = 0
                with self.assertRaisesRegex(ValueError, 'Windows resource limits'):
                    worker.windows_limits(kernel)
                if failed == 'CreateJobObjectW':
                    kernel.CloseHandle.assert_not_called()
                else:
                    kernel.CloseHandle.assert_called_once_with(123)

    @unittest.skipUnless(os.name == 'nt', 'native Windows Job Object test')
    def test_native_child_has_real_memory_and_cpu_limits(self):
        program = '''
import ctypes, importlib.util, json, sys
spec = importlib.util.spec_from_file_location('worker', sys.argv[1])
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
job = worker.windows_limits()
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
kernel.QueryInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p]
kernel.QueryInformationJobObject.restype = ctypes.c_int
limits = worker.JobExtendedLimits()
assert kernel.QueryInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits), None)
print(json.dumps({'flags': limits.BasicLimitInformation.LimitFlags, 'memory': limits.ProcessMemoryLimit,
                  'cpu': limits.BasicLimitInformation.PerProcessUserTimeLimit}))
'''
        result = subprocess.run([sys.executable, '-I', '-c', program, str(MODULE)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        limits = json.loads(result.stdout)
        self.assertEqual(limits['flags'] & 0x102, 0x102)
        self.assertEqual(limits['memory'], 2_000_000_000 // mmap.PAGESIZE * mmap.PAGESIZE)
        self.assertEqual(limits['cpu'], 120 * 10_000_000)

    @unittest.skipUnless(os.name == 'nt', 'native Windows operation guard')
    def test_native_build_process_exits_without_loading_graphify(self):
        result = subprocess.run([sys.executable, '-I', str(MODULE)], input='{"operation":"build"}',
                                capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('query-only', result.stderr)
        self.assertNotIn('PackageNotFoundError', result.stderr)


if __name__ == '__main__':
    unittest.main()
