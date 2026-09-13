# 本体在 AI 中的应用

## 原理、工程与实战

**第一版 · 中文 · 资料核验日期：2026-09-14**

本书回答一个工程问题：怎样让 AI 使用一致的业务概念、可追溯的事实和受约束的动作，完成真实任务。内容从本体与知识表示出发，逐步进入 RDF、OWL、SHACL、知识图谱、RAG、结构化抽取、智能体、生产治理与系统评估。

读者可以按章阅读，也可以跟随配套的设备维修案例，把语义模型、推理、校验、检索和受控执行实际跑起来。

- [前言与阅读方法](preface.md)
- [全书单文件版](book.md)
- [下载 EPUB 电子书](dist/ontology-in-ai.epub)
- [10 课配套教程与代码](../../tutorials/ontology-ai/README.md)
- [资料目录](references/README.md) · [术语表](glossary.md) · [习题参考答案](exercise-answers.md)
- [编排与校验记录](quality-report.md) · [教程实测记录](../../tutorials/ontology-ai/reports/verification.md)

## 全书目录

| 部分 | 章节 | 核心问题 |
| --- | --- | --- |
| 一：建立语义基础 | [01 本体为什么对 AI 有用](chapters/01-ontology-and-ai.md) | 本体解决什么，什么时候值得使用 |
| | [02 从业务问题到能力问题](chapters/02-competency-questions.md) | 怎样确定建模范围与验收标准 |
| | [03 RDF、标识与图数据](chapters/03-rdf-and-identity.md) | 如何表达可交换、可追溯的事实 |
| | [04 RDFS、OWL 与逻辑推理](chapters/04-rdfs-owl-and-reasoning.md) | 能推出什么，不能推出什么 |
| | [05 SHACL 与数据质量](chapters/05-shacl-and-data-quality.md) | 怎样检查缺失、错误和不合约束的数据 |
| 二：建立可维护的知识层 | [06 本体工程与领域建模](chapters/06-ontology-engineering.md) | 怎样组织概念、关系、复用与评审 |
| | [07 数据集成、时间与来源](chapters/07-data-integration-and-provenance.md) | 如何处理身份、单位、冲突和版本 |
| | [08 SPARQL、存储与查询](chapters/08-sparql-and-storage.md) | 如何选择数据库与设计可控查询 |
| 三：把本体接入 AI | [09 本体辅助的 RAG](chapters/09-ontology-aware-rag.md) | 如何利用关系找到更合适的证据 |
| | [10 大模型抽取与实体对齐](chapters/10-llm-extraction-and-alignment.md) | 怎样把候选信息变成可信知识 |
| | [11 智能体与业务动作](chapters/11-agents-and-business-actions.md) | 怎样从建议走向经批准的执行 |
| | [12 神经符号系统设计](chapters/12-neuro-symbolic-design.md) | 模型、规则、推理和优化怎样分工 |
| 四：进入生产环境 | [13 安全与治理](chapters/13-security-and-governance.md) | 怎样保护完整的数据与执行路径 |
| | [14 评估与可观测性](chapters/14-evaluation-and-observability.md) | 怎样证明收益并定位失败 |
| | [15 平台、工具与选型](chapters/15-platforms-and-selection.md) | Foundry、RDF 工具链和属性图怎样取舍 |
| | [16 交付与持续演进](chapters/16-delivery-and-evolution.md) | 怎样发布、迁移、交接和控制成本 |
| 五：综合实践与扩展 | [17 设备维修助手完整案例](chapters/17-capstone-maintenance-assistant.md) | 从 CSV 到可审核建议及工单回执 |
| | [18 行业应用与研究前沿](chapters/18-industry-patterns-and-frontiers.md) | 哪些设计可以迁移，哪些仍需验证 |

## 使用范围

本书中的标准语义与厂商能力都有对应来源；架构安排、工期和选择建议由本书提出。所有设备、温度阈值、工单及用户身份均为合成教学数据。配套业务系统使用本地模拟器；是否调用真实模型由教程的显式选项决定，验证记录会说明实际运行范围。

这本书与[《FDE 工程师实施指南》](../../docs/fde-engineer-guide.md)相互补充：后者侧重现场交付与组织方式，本书深入知识表示及其在 AI 系统中的技术实现。

## 维护与重新构建

分章 Markdown 是书稿源文件。`book.md` 和 EPUB 由同一份源文件生成，电子书同时收录 10 课教程文字；代码、输入数据与完整实测记录通过仓库链接提供。

安装教程锁定依赖后，在仓库根目录运行：

```console
python books/ontology-in-ai/tools/build_book.py
python books/ontology-in-ai/tools/check_book.py
```

构建过程不访问网络，生成单文件书稿、EPUB 和[构建记录](build-report.json)，并在被忽略的 `.cache/ontology-book/preview` 中提供 XHTML 预览。检查工具核对章节、习题、来源、链接与电子书内部结构。发布版另使用 EPUBCheck 5.3.0 检查，详见编排与校验记录。

修改原文后请重新构建，不要直接编辑合并文件。变更引用时同步维护资料目录与机器可读来源记录；更新代码或数据后重新生成教程实测记录。
