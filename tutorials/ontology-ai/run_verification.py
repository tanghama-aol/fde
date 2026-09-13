"""Reproduce the published checks; default output goes to a new ignored run directory."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from ontology_lab.common import write_json
from ontology_lab.evaluation import implementation_hash


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path)
    args = parser.parse_args()
    report_dir = (args.report_dir or ROOT / '.runs' / ('verification-' + uuid.uuid4().hex[:8])).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    stream = io.StringIO()
    test_start = time.perf_counter()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    elapsed = time.perf_counter() - test_start
    (report_dir / 'unit-tests.txt').write_bytes(stream.getvalue().encode('utf-8'))
    if not result.wasSuccessful():
        raise SystemExit('Behavior tests failed; inspect unit-tests.txt.')

    records = []
    scratch_root = ROOT / '.runs'
    scratch_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='verification-work-', dir=scratch_root) as temporary:
        work = Path(temporary)
        if not work.resolve().is_relative_to(scratch_root.resolve()):
            raise RuntimeError('Verification scratch path escaped its intended directory.')

        def call(name: str, arguments: list[str], expected_exit: int = 0) -> dict:
            completed = subprocess.run([sys.executable, '-X', 'utf8', '-m', 'ontology_lab', *arguments],
                cwd=ROOT, capture_output=True, encoding='utf-8', timeout=60,
                env={**os.environ, 'PYTHONUTF8': '1'})
            if completed.returncode != expected_exit:
                raise RuntimeError(f'{name}: exit {completed.returncode}: {completed.stderr}')
            output = json.loads(completed.stdout if expected_exit == 0 else completed.stderr)
            records.append({'name': name, 'arguments': [a.replace(str(work), '<temporary>') for a in arguments],
                            'exit_code': completed.returncode, 'expected_exit_code': expected_exit, 'output': output})
            return output

        doctor = call('environment', ['doctor'])
        rdf = call('rdf', ['rdf'])
        reason = call('reasoning', ['reason'])
        validation = call('validation', ['validate'])
        ingestion = call('ingestion', ['ingest', '--workdir', str(work / 'ingestion')])
        lexical = call('lexical_retrieval', ['retrieve', '--mode', 'lexical', '--top-k', '1'])
        graph = call('graph_retrieval', ['retrieve', '--mode', 'graph', '--top-k', '1'])
        forbidden = call('forbidden_asset', ['retrieve', '--asset', 'P-201'], expected_exit=2)
        baseline = call('baseline_generation', ['generate', '--mode', 'baseline'])
        fixture = call('fixture_generation', ['generate', '--mode', 'fixture'])
        normal_temperature = call('normal_temperature', ['generate', '--mode', 'baseline', '--asset', 'P-102'])
        normal_action = call('normal_action', ['actions', '--scenario', 'normal', '--workdir', str(work / 'normal')])
        timeout = call('unknown_action', ['actions', '--scenario', 'timeout', '--no-reconcile', '--workdir', str(work / 'unknown')])
        operation = timeout['first_attempt']['operation_id']
        recovery = call('new_process_reconciliation', ['reconcile', '--workdir', str(work / 'unknown'), '--operation', operation])
        repeat = call('repeated_reconciliation', ['reconcile', '--workdir', str(work / 'unknown'), '--operation', operation])
        with closing(sqlite3.connect(work / 'unknown' / 'work-orders.sqlite')) as database:
            drafts = database.execute('SELECT COUNT(*) FROM drafts').fetchone()[0]
        evaluation = call('evaluation', ['evaluate'])
        migration = call('migration', ['migrate', '--workdir', str(work / 'migration')])
        demo = call('full_demo', ['demo', '--workdir', str(work / 'capstone')])

        checks = {
            'environment_data_present': doctor['data_present'],
            'administrative_rdf_rows': len(rdf['assets']) == 3,
            'type_inverse_transitive': all(reason[k] for k in ('inferred_asset_type','inferred_inverse','inferred_transitive_part')),
            'valid_and_invalid_data': validation['expected_behavior'],
            'fahrenheit_normalization': ingestion['p102_temperature_c'] == 72,
            'lexical_catalog': lexical['documents'][0]['id'] == 'CATALOG-N-1',
            'graph_manual': graph['documents'][0]['id'] == 'MANUAL-N-1',
            'forbidden_region': forbidden['error'] == 'NOT_FOUND_OR_FORBIDDEN',
            'baseline_requires_approval': baseline['recommendation']['requires_approval'],
            'fixture_is_not_model_run': fixture['run']['live_llm_calls'] == 0,
            'normal_temperature_no_action': normal_temperature['recommendation']['decision'] == 'no_action',
            'normal_action_one_draft': normal_action['total_external_drafts'] == 1,
            'timeout_stays_unknown_until_reconciliation': timeout['final']['state'] == 'outcome_unknown',
            'fresh_process_recovers': recovery['state'] == 'executed',
            'repeated_reconciliation_same_receipt': recovery['receipt'] == repeat['receipt'],
            'one_external_draft_after_recovery': drafts == 1,
            'evaluation_guards': all(row['passed'] for row in evaluation['guard_cases']),
            'migration_repeat_is_noop': migration['first_run']['moved_edges'] == 1 and migration['repeat_run']['moved_edges'] == 0,
            'complete_demo_one_draft': demo['actions']['total_external_drafts'] == 1,
        }
        if not all(checks.values()):
            raise RuntimeError(f'CLI acceptance failed: {checks}')

    asset_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for folder in ('data', 'queries') for p in sorted((ROOT / folder).iterdir()) if p.is_file()}
    summary = {'schema_version': '1.0', 'executed_at': started, 'platform': platform.system(),
               'python': platform.python_version(), 'dependencies': doctor['dependencies'],
               'implementation_sha256': implementation_hash(), 'input_sha256': asset_hashes,
               'unit_tests': {'run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
                              'skipped': len(result.skipped), 'duration_seconds': round(elapsed, 3)},
               'cli_processes': len(records), 'acceptance_checks': checks,
               'cross_process_recovery': {'before': timeout['final']['state'], 'after': recovery['state'], 'external_drafts': drafts},
               'live_llm_calls': 0, 'production_system_calls': 0,
               'model_adapter_validation': 'Local loopback HTTP test double only; no live model inference.'}
    write_json(report_dir / 'verification.json', summary)
    write_json(report_dir / 'cli-results.json', records)
    write_json(report_dir / 'evaluation.json', evaluation)
    write_json(report_dir / 'demo-report.json', demo)
    text = f'''# 实测记录

本记录由 [run_verification.py](../run_verification.py) 在锁定依赖环境中实际生成。全部输入为合成数据；没有调用真实模型或生产业务系统。

- 实际运行时间（UTC）：`{started}`。
- 环境：{platform.system()}，Python {platform.python_version()}。
- 行为测试：{result.testsRun} 项，失败 {len(result.failures)}，错误 {len(result.errors)}，跳过 {len(result.skipped)}。
- 命令行验证：{len(records)} 个独立进程，{len(checks)} 项结果检查全部通过。
- 实现 SHA-256：`{summary['implementation_sha256']}`。

## 关键结果

| 项目 | 实际结果 |
| --- | --- |
| 原始图 → OWL RL 闭包 | {reason['asserted_triples']} → {reason['closure_triples']} 条三元组 |
| 单位转换 | 161.6 F → {ingestion['p102_temperature_c']} C |
| 有效 / 故意无效数据 | SHACL 通过 / 拒绝 |
| 词项基线 Hit@1 | {evaluation['retrieval_metrics']['lexical']['hits']} / {evaluation['retrieval_metrics']['lexical']['cases']} |
| 关系辅助 Hit@1 | {evaluation['retrieval_metrics']['graph']['hits']} / {evaluation['retrieval_metrics']['graph']['cases']} |
| 跨进程对账 | {timeout['final']['state']} → {recovery['state']} |
| 对账后外部草稿数 | {drafts} |
| 迁移首次 / 再次移动关系 | {migration['first_run']['moved_edges']} / {migration['repeat_run']['moved_edges']} |

## 原始记录

- [行为测试输出](unit-tests.txt)
- [完整验证元数据与输入摘要](verification.json)
- [逐命令 JSON 输出](cli-results.json)
- [检索评估明细](evaluation.json)
- [完整案例报告](demo-report.json)

执行中产生的 SQLite 与临时图文件用于验证后清理，发布的是合成结果与元数据。每次运行的请求 ID 和实际时间可以不同，预期业务行为保持一致。

## 复现

在教程目录、已安装依赖的环境中运行：

```console
python run_verification.py
```

默认写入新的 `.runs/verification-...` 目录。维护者可用 `--report-dir reports` 更新发布记录。该命令运行实际测试和命令行场景，没有替换为预制输出。

## 解释边界

四条检索案例为人工设计的机制实验，基线是词项重合，两个方法均获得显式设备编号。没有测量向量检索、自然语言实体链接、模型事实正确率、生产延迟或真实故障率。40 项测试验证已定义行为，不是独立业务样本的成功率。

模型适配器只使用本地 HTTP 测试桩核验协议、非法响应、错误返回和远程地址选择。本机没有运行中的 Ollama 服务，未进行真实模型推理。动作系统使用独立 SQLite 模拟外部业务系统，草稿回执不代表派工或设备修复。
'''
    (report_dir / 'verification.md').write_bytes(text.encode('utf-8'))
    print(json.dumps({'report_directory': str(report_dir), 'tests': result.testsRun,
                      'cli_processes': len(records), 'acceptance_checks': len(checks), 'passed': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
