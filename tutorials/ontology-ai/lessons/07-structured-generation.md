# 第 07 课　结构化建议与可选模型

目标：区分模板、人工样本与真实模型输出，并理解 JSON 合法和业务正确之间的差距。对应书籍第 10、12 章。

## 先运行无需模型的模式

```console
python -m ontology_lab generate --mode baseline
python -m ontology_lab generate --mode fixture
python -m ontology_lab generate --mode baseline --asset P-102
```

前两条针对 P-101，预期 `decision: propose`、`temperature_c: 92.0`、`requires_approval: true`，候选动作是 `createMaintenanceDraft`。第三条针对 P-102，预期 `decision: no_action`、72 C、无候选动作。

`run.mode` 分别说明规则模板与人工参考样本；它们的 `live_llm_calls` 都是 0。人工样本固定对应 P-101，不能改成其他资产后仍期待通过事实匹配。

## 接入自己准备的本地模型

本步骤可选。先安装、启动 Ollama，并准备支持所需输出能力的模型。用 `ollama list` 查看本地模型名称，然后把下面占位名称替换为实际名称：

```console
python -m ontology_lab generate --mode live --model YOUR_LOCAL_MODEL --timeout 120
```

默认地址是 `http://127.0.0.1:11434`。适配器调用 `/api/generate`，发送 JSON Schema，设置 `stream=false`，接收后再次进行客户端校验。配置远程地址需要显式 `--base-url` 和 `--allow-remote`；地址由操作者确定，不能来自模型输出或文档。

官方资料：[结构化输出](https://docs.ollama.com/capabilities/structured-outputs)、[生成接口](https://docs.ollama.com/api/generate)。本书核读时，官方说明 Ollama Cloud 暂不支持结构化输出，不能把本地步骤直接外推到云端。

本版实际验证未调用真实模型。本机没有运行中的 Ollama 服务；协议与错误处理使用本地 HTTP 测试桩验证，不是模型能力测试。

## 检查合同和事实

阅读[输出合同](../data/recommendation.schema.json)及 `validate_recommendation`。校验器限制字段与枚举，并复核资产、温度、程序、证据和动作前提。模型不能添加管理员角色或自己签发批准。

可以在 Python 交互环境中执行以下反例：

```python
from ontology_lab.common import DATA, NORTH_PLANNER, LabError, read_json
from ontology_lab.retrieval import Retriever
from ontology_lab.generation import validate_recommendation

bundle = Retriever().bundle(NORTH_PLANNER, "P-101", "P-101")
candidate = read_json(DATA / "recommendation.fixture.json")
candidate["temperature_c"] = 999
try:
    validate_recommendation(candidate, bundle)
except LabError as error:
    print(error.code)  # FACT_MISMATCH
```

## 常见失败

`MODEL_UNAVAILABLE` 表示服务错误或超时，不会转而创建业务记录。`OUTPUT_SCHEMA` 表示结构不合约；`UNKNOWN_EVIDENCE` 表示引用不属于本次证据包。格式合法但温度错误仍会被拒绝。

自由文本 `summary` 的每句话没有被全面验证。因此“关键字段通过”不能写成“生成完全正确”。这条命令也不会执行建议；模型接入与动作执行是独立步骤。

## 练习

在人工样本副本中添加 `approved: true`，再把摘要改为“设备已修复”。前者应被结构校验拒绝；后者可能通过有限字段检查。说明为何还需要陈述支持评价、人工审核或更受限的生成格式。

下一课：[受控动作](08-controlled-actions.md)。
