# 第 08 课　受控动作与对账

目标：完整观察提案、可信批准、幂等执行、响应丢失与跨进程恢复。对应书籍第 11、13、17 章。

## 正常执行与响应丢失

```console
python -m ontology_lab actions --scenario normal
python -m ontology_lab actions --scenario timeout
```

每次默认使用新目录。正常场景首次与重试都返回 `executed`。超时场景首次为 `outcome_unknown`，同键重试仍未知，对账后为 `executed`。两个独立演示各自只创建 1 份外部草稿。

注意 `proposal.state: awaiting_approval` 是初次创建时返回的提案快照；演示随后由可信合成计划员进行批准。输出不是模型自行批准的过程。

## 分两个进程恢复

先停在未知状态，并保存报告。目录名必须尚未用于动作演示：

```console
python -m ontology_lab actions --scenario timeout --no-reconcile --workdir .runs/action-step --output .runs/action-step/result.json
```

此时 `final.state` 仍未知，但外部模拟系统已经有一份草稿。Windows PowerShell 可读取操作 ID，再启动新的对账进程：

```powershell
$actionRun = Get-Content -Raw -Encoding UTF8 .runs/action-step/result.json | ConvertFrom-Json
python -m ontology_lab reconcile --workdir .runs/action-step --operation ($actionRun.first_attempt.operation_id)
```

其他环境可从 JSON 中复制 `first_attempt.operation_id`，替换下面的占位值：

```console
python -m ontology_lab reconcile --workdir .runs/action-step --operation OP-REPLACE-WITH-ACTUAL-ID
```

预期返回 `state: executed` 及 `receipt.status: DRAFT`。再次对账仍取得同一回执。

## 解释

提案绑定对象版本、观测、程序内容哈希和策略。批准绑定提案及有效期。首次写入之前，系统复核当前状态；外部模拟器也检查其对象版本，避免读取与写入之间的数据变化被忽略。

本地请求幂等避免相同请求重复派发，同提案唯一性避免通过换键重复执行，外部请求 ID 用于确认实际效果。若外部提交成功但网络响应丢失，系统必须承认“结果未知”，不能直接判定失败后重发。

动作记录与外部模拟器分别使用独立 SQLite 文件。重启 `ActionService` 后状态仍存在，体现的是持久化机制；它不是跨机高可用系统。

## 常见失败

`RUN_EXISTS` 保护已有记录。要学习重试，使用原服务状态与请求 ID；要重跑全新演示，使用新目录。`RUN_MISSING` 表示对账没有指向已有动作目录。

批准失效、对象版本变化、文档变化或只读身份都应阻止首次写入。已确认成功的记录不能被晚到的未知结果覆盖。相关反例已经包含在测试中。

## 练习

解释为什么本地请求表去重仍需要外部幂等或对账。再设计“两个不同提案对应同一次异常”的案例：现有同提案去重不够，需要业务事件 ID、活动工单唯一约束或人工合并策略。

下一课：[评估](09-evaluation.md)。
