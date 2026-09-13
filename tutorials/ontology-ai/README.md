# 本体与 AI：10 课可运行教程

配套书籍：[《本体在 AI 中的应用：原理、工程与实战》](../../books/ontology-in-ai/README.md)。从 CSV 开始，完成 RDF 建模、查询、推理、校验、授权检索、结构化建议、批准与业务对账。

所有设备与身份都是合成数据。唯一业务动作是在本地独立 SQLite 模拟系统中创建维修工单草稿。核心课程安装依赖后可离线运行，不需要 Foundry 账号或模型服务；真实模型调用是第 07 课的显式可选步骤。

## 环境准备

实测环境为 Windows、Python 3.11.0。建议使用 Python 3.11 创建独立环境，其他系统和 Python 版本需要自行验证。先克隆仓库，再进入本教程目录：

```console
git clone https://github.com/tanghama-aol/fde.git
cd fde/tutorials/ontology-ai
```

Windows PowerShell：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\Activate.ps1
python -m ontology_lab doctor
```

如果本机策略不允许激活脚本，无需修改系统策略；将后续命令中的 `python` 替换为 `.\.venv\Scripts\python.exe` 即可。

macOS / Linux：

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m ontology_lab doctor
```

[requirements.txt](requirements.txt)列出直接依赖，[requirements-lock.txt](requirements-lock.txt)锁定实测环境的完整版本，也包含电子书构建所用的 Markdown 解析库。安装通常需要网络；版本锁定不等于所有平台二进制包均已验证。

## 先跑完整案例

```console
python -m ontology_lab demo
python -m unittest discover -s tests -v
```

`demo` 创建新的 `.runs/demo-...` 目录，保存报告、导入图、迁移结果及模拟业务数据库。验证范围与原始结果见[实测记录](reports/verification.md)。本版实测 40 项测试通过；真实模型调用数与生产系统调用数均为 0。

所有子命令都支持 `--output 文件名.json`。`actions`、`ingest`、`migrate`、`demo` 可通过 `--workdir` 指定输出目录；动作和完整案例不覆盖已有执行状态。重复学习时使用新目录，已有目录留作对账和比较。

## 课程路线

维护者和希望一次复现全部结果的读者，可运行 `python run_verification.py`。它在新目录运行行为测试与逐课命令，生成完整记录，详见[验证脚本](run_verification.py)。

| 课程 | 核心操作 | 完成后应理解 |
| --- | --- | --- |
| [01 环境与案例](lessons/01-environment-and-case.md) | doctor、查看输入 | 身份、时间、合成数据边界 |
| [02 RDF 与 SPARQL](lessons/02-rdf-and-sparql.md) | rdf | 三元组、命名图、路径查询 |
| [03 逻辑推理](lessons/03-reasoning.md) | reason | 类型、逆关系、传递关系及开放世界 |
| [04 SHACL 校验](lessons/04-shacl.md) | validate | 形状、焦点节点、违反报告 |
| [05 数据导入](lessons/05-ingestion.md) | ingest | 复合身份、单位、时间、来源摘要 |
| [06 授权检索](lessons/06-retrieval.md) | retrieve | 词项基线与程序关系、权限边界 |
| [07 结构化生成](lessons/07-structured-generation.md) | generate | 模板、人工样本、真实模型与验证 |
| [08 受控动作](lessons/08-controlled-actions.md) | actions、reconcile | 批准、幂等、响应丢失、跨进程恢复 |
| [09 评估](lessons/09-evaluation.md) | evaluate、测试 | 指标分母、反例、实验边界 |
| [10 迁移与综合项目](lessons/10-migration-and-capstone.md) | migrate、demo | 版本、重复迁移、交付验收 |

建议按顺序完成。只想了解本体语义可先做前五课；已有知识图谱经验的读者，可从第六课开始，再回查数据模型。

## 文件与职责

| 位置 | 内容 |
| --- | --- |
| [data/ontology.ttl](data/ontology.ttl) | 类、关系、公理、领域本体版本 |
| [data/assets.csv](data/assets.csv)、[data/observations.csv](data/observations.csv) | 设备与观测源数据 |
| [data/shapes.ttl](data/shapes.ttl)、[data/invalid.ttl](data/invalid.ttl) | SHACL 合同与故意错误数据 |
| [data/documents.json](data/documents.json) | 有权限、有效期与程序关联的文档 |
| [data/recommendation.schema.json](data/recommendation.schema.json) | 建议输出合同 |
| [ontology_lab/graph.py](ontology_lab/graph.py) | 导入、推理、校验、授权图查询、迁移 |
| [ontology_lab/retrieval.py](ontology_lab/retrieval.py) | 文档过滤、排序和证据包 |
| [ontology_lab/generation.py](ontology_lab/generation.py) | 基线、样本验证、Ollama 适配器 |
| [ontology_lab/actions.py](ontology_lab/actions.py) | 提案、批准、执行、外部模拟器和对账 |
| [tests](tests/) | 已知行为与故障分支验证 |
| [reports](reports/) | 可发布的实际运行记录 |

## 固定业务时钟

案例的“现在”固定为 `2026-09-01T09:02:00Z`；设备和观测快照为 `09:00:00Z`，允许新鲜度为 300 秒。这样不同日期运行课程会得到相同业务判断。报告仍记录实际运行时间。真实系统应使用可信实时时钟，而不是照搬教学时间常量。

## 常见问题

`No module named ontology_lab` 通常表示当前目录错误，应进入 `tutorials/ontology-ai`。依赖导入失败时，检查安装依赖和运行代码是否使用同一个 Python。Windows 控制台中文显示异常，可使用 `python -X utf8 -m ontology_lab ...`。

`RUN_EXISTS` 表示已有运行状态被保留，换用新的 `--workdir`，不要为了重跑而清空原请求记录。`NOT_FOUND_OR_FORBIDDEN` 是预期权限行为，不能据此区分对象不存在还是无权访问。真实模型服务不可用时只影响 `generate --mode live`，不会转成执行业务动作。

## 从教程到生产的差距

固定 `Principal` 是身份系统替身；本地文件可被操作者直接读取，文件布局不构成多租户隔离。RDFLib 内存图与 SQLite 用于小规模教学，没有验证生产负载或高可用。输出校验只覆盖结构及若干关键字段，不证明自由文本每句话都正确。跨租户、过期、异常回执等测试验证已知边界，不构成完整安全认证。

把案例接入真实系统前，应重新建立领域标准、身份服务、数据质量、评估集、动作合同与运维责任，详见书籍第 13—17 章。
