#!/usr/bin/env python3
"""Check revision-bound evidence coverage, never release or independent QA approval."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_file(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('expected project-relative file path')
    candidate = root / value
    if '..' in Path(value).parts or not candidate.resolve().is_relative_to(root):
        raise ValueError('file escapes project root')
    # Files in a trusted, quiescent project only; this is not a filesystem sandbox.
    if any(part.is_symlink() for part in (candidate, *candidate.parents) if part != root):
        raise ValueError('symlink evidence/input is not supported')
    if not candidate.is_file():
        raise ValueError('referenced file is missing')
    return candidate


def records(value, key, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f'{label} must be a nonempty list')
    result = {}
    for row in value:
        if not isinstance(row, dict) or not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError(f'{label} needs nonempty {key}')
        if row[key] in result:
            raise ValueError(f'duplicate {label} ID')
        result[row[key]] = row
    return result


def check(contract, ledger, root, source_revision, contract_digest):
    """Return missing evidence; validate IDs against the supplied canonical Task."""
    if not isinstance(contract, dict) or not isinstance(ledger, dict):
        raise ValueError('contract and ledger must be objects')
    if not isinstance(source_revision, str) or not source_revision.strip():
        raise ValueError('current source revision is required')
    if contract.get('schema_version') != 2:
        raise ValueError('a canonical v2 Task is required; normalize legacy Tasks first')
    for key in ('task_id', 'contract_revision'):
        if not isinstance(contract.get(key), (str, int)) or isinstance(contract.get(key), bool):
            raise ValueError(f'contract needs {key}')
        if not str(contract[key]).strip() or str(ledger.get(key, '')) != str(contract[key]):
            raise ValueError(f'{key} does not match canonical Task')
    if ledger.get('contract_sha256') != contract_digest:
        raise ValueError('ledger refers to different canonical contract bytes')
    criteria = records(contract.get('acceptance_criteria'), 'id', 'acceptance criteria')
    tests = records(contract.get('required_tests'), 'id', 'required tests')
    if not isinstance(ledger.get('criteria'), list):
        raise ValueError('ledger criteria must be a list')
    supplied = records(ledger['criteria'], 'id', 'ledger criteria') if ledger['criteria'] else {}
    if set(supplied) - set(criteria):
        raise ValueError('ledger contains unknown acceptance ID')
    gaps = []
    verified = []
    seen_tests = set()
    stale_ledger = ledger.get('source_revision') != source_revision
    if stale_ledger:
        gaps.append('ledger source revision is stale')
    for criterion_id in criteria:
        row = supplied.get(criterion_id)
        if row is None:
            gaps.append(f'{criterion_id}: missing evidence record')
            continue
        state = row.get('declared_state')
        if state not in ('PLANNED', 'IMPLEMENTED', 'PARTIAL', 'SKIP', 'UNKNOWN'):
            raise ValueError('unknown declared state')
        cases = row.get('cases')
        if not isinstance(cases, list):
            raise ValueError('criterion cases must be a list')
        missing = []
        criterion_tests = set()
        if state != 'IMPLEMENTED':
            missing.append(f'declared {state}; cannot waive canonical acceptance')
        if not cases:
            missing.append('no executed case evidence')
        for case in cases:
            if not isinstance(case, dict) or case.get('test_id') not in tests:
                raise ValueError('case must reference a canonical required test ID')
            test_id = case['test_id']
            if case.get('status') not in ('PASS', 'FAIL', 'NOT_RUN'):
                raise ValueError('unknown case status')
            if case.get('status') != 'PASS':
                missing.append(f'{test_id}: {case["status"]}')
                continue
            if case.get('source_revision') != source_revision:
                missing.append(f'{test_id}: stale source revision')
                continue
            digest = case.get('sha256')
            if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
                raise ValueError('PASS case needs sha256 evidence digest')
            evidence = local_file(root, case.get('path'))
            if evidence.stat().st_size == 0 or sha256(evidence) != digest:
                missing.append(f'{test_id}: empty or changed evidence')
                continue
            seen_tests.add(test_id)
            criterion_tests.add(test_id)
        # Existing Task templates use `validation` for a canonical test ID.
        planned = criteria[criterion_id].get('validation')
        if isinstance(planned, str) and planned in tests and planned not in criterion_tests:
            missing.append(f'{planned}: canonical criterion validation evidence is missing')
        if missing or stale_ledger:
            gaps.extend(f'{criterion_id}: {item}' for item in missing)
        else:
            verified.append(criterion_id)
    gaps.extend(f'{test_id}: required test has no current PASS evidence'
                for test_id in tests if test_id not in seen_tests)
    return {
        'task_id': contract['task_id'], 'contract_revision': str(contract['contract_revision']),
        'source_revision': source_revision,
        'status': 'EVIDENCE_PRESENT' if not gaps else 'INCOMPLETE',
        'criteria_with_evidence': verified, 'required_criteria': list(criteria),
        'gaps': gaps, 'release_authorized': False,
        'limitation': 'Integrity/coverage only; test execution, semantics and independent owner approval are not certified.',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--contract', required=True)
    parser.add_argument('--ledger', required=True)
    parser.add_argument('--source-revision', required=True)
    args = parser.parse_args(argv)
    try:
        root = Path(args.project_root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError('project root is not a directory')
        contract_path = local_file(root, args.contract)
        ledger_path = local_file(root, args.ledger)
        contract = json.loads(contract_path.read_text(encoding='utf-8'))
        ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
        report = check(contract, ledger, root, args.source_revision, sha256(contract_path))
    except (ValueError, OSError, TypeError) as exc:
        print(f'coverage: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'EVIDENCE_PRESENT' else 1


if __name__ == '__main__':
    sys.exit(main())
