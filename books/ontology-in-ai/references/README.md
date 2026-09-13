# 资料目录与核验说明

本目录收录本书使用的 40 项资料，核验日期为 **2026 年 9 月 14 日（Asia/Shanghai）**。来源抓取时间以 UTC 单独保存在[机器可读目录](registry.json)。官方规范用于语义依据，厂商文档用于能力定位；本书的交付安排、选型建议和教学模型由本书提出。

R26、R27、R29 仅核读作者或出版机构的摘要页，未据此宣称已读论文全文或复现实验。其余来源按书中所需主题核对，访问成功不等于逐字通读。未公开源网页全文或原始 PDF；摘要和引用用于追溯论述。

教程采用明确版本基线：RDF 1.1、RDFS、OWL 2、SPARQL 1.1 与 SHACL。在线文档会变化，URL 可访问也不保证内容保持原版本。所有 40 项本次抓取均返回 HTTP 200；页面更新后仍应核对标题、版本与具体结论。

## 建议阅读路线

- 建立概念与方法：R38、R01、R04、R06、R28。
- 实现查询、推理与校验：R02、R07—R11、R18—R22。
- 来源、时间与领域复用：R13—R17、R40。
- 与生成式 AI 结合：R25—R32。
- 选型与治理：R23—R24、R33—R39。

## 逐项资料

<a id="r01"></a>

### R01　RDF 1.1 Concepts and Abstract Syntax

[W3C 原文](https://www.w3.org/TR/rdf11-concepts/)

- 版本与日期：RDF 1.1；明确记录的发布日期：2014-02-25。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：三元组、IRI、字面量、空白节点、图与数据集的抽象模型。
- 使用边界：用于数据模型定义，不自动规定业务身份或访问控制。

<a id="r02"></a>

### R02　RDF 1.1 Turtle

[W3C 原文](https://www.w3.org/TR/turtle/)

- 版本与日期：RDF 1.1 Turtle；明确记录的发布日期：2014-02-25。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：Turtle 前缀、缩写、字面量与三元组书写方式。
- 使用边界：序列化文本顺序或空白节点标签不是稳定业务身份。

<a id="r03"></a>

### R03　RDF 1.1 Semantics

[W3C 原文](https://www.w3.org/TR/rdf11-mt/)

- 版本与日期：RDF 1.1 Semantics；明确记录的发布日期：2014-02-25。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：RDF 与 RDFS 的解释和蕴含；图表示与语义的区别。
- 使用边界：不能把未出现三元组直接解释为否定事实。

<a id="r04"></a>

### R04　RDF Schema 1.1

[W3C 原文](https://www.w3.org/TR/rdf-schema/)

- 版本与日期：RDF Schema 1.1；明确记录的发布日期：2014-02-25。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：类、子类、domain、range 与属性语义。
- 使用边界：domain/range 不等同于数据输入校验规则。

<a id="r05"></a>

### R05　OWL 2 Web Ontology Language Document Overview

[W3C 原文](https://www.w3.org/TR/owl2-overview/)

- 版本与日期：OWL 2 Second Edition；明确记录的发布日期：2012-12-11。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：OWL 2 的语言结构、文档体系和正式语义定位。
- 使用边界：语言表达能力与某个推理器实际支持范围不同。

<a id="r06"></a>

### R06　OWL 2 Web Ontology Language Primer

[W3C 原文](https://www.w3.org/TR/owl2-primer/)

- 版本与日期：OWL 2 Primer Second Edition；明确记录的发布日期：2012-12-11。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：类、个体、限制、同一性及开放世界下的建模。
- 使用边界：教程说明不替代各语义规范；没有记录不等于存在约束被违反。

<a id="r07"></a>

### R07　OWL 2 Web Ontology Language Profiles

[W3C 原文](https://www.w3.org/TR/owl2-profiles/)

- 版本与日期：OWL 2 Profiles Second Edition；明确记录的发布日期：2012-12-11。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：EL、QL、RL 的受限语言范围与实现取向。
- 使用边界：OWL-RL 软件包的行为应以所用版本验证，不可称作完整 OWL 2 DL。

<a id="r08"></a>

### R08　Shapes Constraint Language (SHACL)

[W3C 原文](https://www.w3.org/TR/shacl/)

- 版本与日期：SHACL Recommendation；明确记录的发布日期：2017-07-20。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：形状、目标、属性约束、闭合形状与校验报告。
- 使用边界：校验结果依赖输入图、目标选择、推理与功能配置。

<a id="r09"></a>

### R09　SPARQL 1.1 Query Language

[W3C 原文](https://www.w3.org/TR/sparql11-query/)

- 版本与日期：SPARQL 1.1 Query；明确记录的发布日期：2013-03-21。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：图模式、属性路径、聚合、命名图与查询语义。
- 使用边界：查询语言能力不自动构成权限或资源边界。

<a id="r10"></a>

### R10　SPARQL 1.1 Update

[W3C 原文](https://www.w3.org/TR/sparql11-update/)

- 版本与日期：SPARQL 1.1 Update；明确记录的发布日期：2013-03-21。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：INSERT、DELETE 等 RDF 更新操作。
- 使用边界：本教程小型迁移不是分布式在线迁移系统。

<a id="r11"></a>

### R11　RDF 1.1 TriG

[W3C 原文](https://www.w3.org/TR/trig/)

- 版本与日期：RDF 1.1 TriG；明确记录的发布日期：2014-02-25。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：RDF 数据集与命名图的文本表达。
- 使用边界：图名不自动证明来源或提供隔离。

<a id="r12"></a>

### R12　JSON-LD 1.1

[W3C 原文](https://www.w3.org/TR/json-ld11/)

- 版本与日期：JSON-LD 1.1；明确记录的发布日期：2020-07-16。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：上下文、术语映射与关联数据的 JSON 表示。
- 使用边界：远程上下文可带来网络访问；受控解析需另行配置。

<a id="r13"></a>

### R13　SKOS Simple Knowledge Organization System Reference

[W3C 原文](https://www.w3.org/TR/skos-reference/)

- 版本与日期：SKOS Reference；明确记录的发布日期：2009-08-18。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：概念、标签及 broader/narrower 等知识组织关系。
- 使用边界：SKOS 概念关系不应随意当作 OWL 类等价或个体同一性。

<a id="r14"></a>

### R14　PROV-O: The PROV Ontology

[W3C 原文](https://www.w3.org/TR/prov-o/)

- 版本与日期：PROV-O；明确记录的发布日期：2013-04-30。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：实体、活动、参与者及来源关系的表达。
- 使用边界：本教程仅保存有限来源信息，未实现完整 PROV 工作流。

<a id="r15"></a>

### R15　Time Ontology in OWL

[W3C 原文](https://www.w3.org/TR/owl-time/)

- 版本与日期：Time Ontology in OWL，所读推荐页；明确记录的发布日期：2022-11-15。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：时间点、区间及时间关系的建模词汇。
- 使用边界：词汇不替应用决定新鲜度阈值或源时钟可信度。

<a id="r16"></a>

### R16　Semantic Sensor Network Ontology

[W3C / OGC 原文](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/)

- 版本与日期：SOSA/SSN 2017 固定推荐版；明确记录的发布日期：2017-10-19。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：传感器、观测、采样与执行器相关建模。
- 使用边界：为可重复引用采用 2017 固定版本；不声称这是唯一或最新工作。

<a id="r17"></a>

### R17　R2RML: RDB to RDF Mapping Language

[W3C 原文](https://www.w3.org/TR/r2rml/)

- 版本与日期：R2RML Recommendation；明确记录的发布日期：2012-09-27。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：从关系数据库到 RDF 的映射语言。
- 使用边界：本教程是自定义 CSV 导入器，不是 R2RML 实现。

<a id="r18"></a>

### R18　RDFLib documentation

[RDFLib project 原文](https://rdflib.readthedocs.io/en/stable/)

- 版本与日期：stable 文档；运行锁定 RDFLib 7.1.4；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：Python RDF 图构造、解析、序列化与查询工具链。
- 使用边界：文档入口可随版本变化；内存库不是已验证的生产数据库方案。

<a id="r19"></a>

### R19　OWL-RL documentation

[OWL-RL project 原文](https://owl-rl.readthedocs.io/en/latest/)

- 版本与日期：页面标题 5.2.2；运行锁定 OWL-RL 7.1.4；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：DeductiveClosure 与基于规则的 RDF/OWL RL 扩展路线。
- 使用边界：文档标题与运行版本不同；精确行为依照锁定环境及测试。

<a id="r20"></a>

### R20　pySHACL 0.30.1 README

[RDFLib project 原文](https://raw.githubusercontent.com/RDFLib/pySHACL/v0.30.1/README.md)

- 版本与日期：pySHACL v0.30.1 README；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：pySHACL 的输入、推理选项与验证结果接口。
- 使用边界：使用固定版本 README；高级功能或性能需按配置另测。

<a id="r21"></a>

### R21　Apache Jena inference support

[Apache Software Foundation 原文](https://jena.apache.org/documentation/inference/)

- 版本与日期：在线项目文档，核验于 2026-09-14；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：Jena 推理支持、规则引擎与不同配置的能力范围。
- 使用边界：未安装、部署或跑 Jena 性能实验。

<a id="r22"></a>

### R22　Apache Jena Fuseki

[Apache Software Foundation 原文](https://jena.apache.org/documentation/fuseki2/)

- 版本与日期：Fuseki 在线文档，核验于 2026-09-14；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：SPARQL 服务与 Jena 工具链的集成定位。
- 使用边界：生产部署、权限、容量和高可用未实测。

<a id="r23"></a>

### R23　Graph database concepts

[Neo4j 原文](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)

- 版本与日期：在线概念文档，核验于 2026-09-14；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：属性图的节点、关系、标签和属性。
- 使用边界：不据此推断自动支持 RDF/OWL 语义，也未做产品性能排名。

<a id="r24"></a>

### R24　GraphDB reasoning

[Ontotext 原文](https://graphdb.ontotext.com/documentation/11.0/reasoning.html)

- 版本与日期：GraphDB 11.0；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：数据库的规则集、推理与派生结果管理。
- 使用边界：仅覆盖所读 11.0 文档；许可、集群与后续版本需再核对。

<a id="r25"></a>

### R25　GraphRAG indexing overview

[Microsoft 原文](https://microsoft.github.io/graphrag/index/overview/)

- 版本与日期：GraphRAG 在线索引概览；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：文本到图的索引流程及相关摘要产物。
- 使用边界：未安装或复现 Microsoft GraphRAG；不等同于本教程固定关系检索。

<a id="r26"></a>

### R26　From Local to Global: A Graph RAG Approach to Query-Focused Summarization

[Darren Edge et al. / Microsoft Research 原文](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/)

- 版本与日期：Microsoft Research 论文摘要页；明确记录的发布日期：2024-04-24。
- 核读范围：仅核读摘要页。
- 支持内容：面向局部与整体问题的图辅助检索和查询聚焦摘要研究方向。
- 使用边界：仅核读摘要页，未核读论文全文或复现实验；不采用其结果作本项目成绩。

<a id="r27"></a>

### R27　Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

[Patrick Lewis et al. / NeurIPS 2020 原文](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)

- 版本与日期：NeurIPS 2020 论文摘要页；明确记录的发布日期：2020。
- 核读范围：仅核读摘要页。
- 支持内容：检索增强生成结合检索知识与参数化生成的研究背景。
- 使用边界：仅核读出版机构摘要，不对论文实现细节或指标作再现声明。

<a id="r28"></a>

### R28　Knowledge Graphs

[Aidan Hogan et al. / author-hosted book 原文](https://kgbook.org/)

- 版本与日期：作者托管 Knowledge Graphs 全文 HTML；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：图数据模型、查询、逻辑、学习与应用的系统性背景。
- 使用边界：网页可读全文；本书用于相关主题核对，不声明复现其中所有方法。

<a id="r29"></a>

### R29　Unifying Large Language Models and Knowledge Graphs: A Roadmap

[Shirui Pan et al. / author publication page 原文](https://shiruipan.github.io/publication/llm-kg-23/)

- 版本与日期：作者论文摘要页，页面含 2024 年信息；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：仅核读摘要页。
- 支持内容：知识图谱增强模型、模型辅助图谱及协作路线。
- 使用边界：仅核读摘要，页面时间不被当作唯一论文出版日期；未复现实验。

<a id="r30"></a>

### R30　Structured outputs

[Ollama 原文](https://docs.ollama.com/capabilities/structured-outputs)

- 版本与日期：Ollama Structured Outputs 在线文档；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：通过 format 传入 JSON Schema，以及结构化输出的使用方式。
- 使用边界：核读时官方注明 Ollama Cloud 不支持 structured outputs；本版无真实模型实测。

<a id="r31"></a>

### R31　Generate a response

[Ollama 原文](https://docs.ollama.com/api/generate)

- 版本与日期：Ollama /api/generate 在线文档；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：生成请求、stream=false、format 与响应字段。
- 使用边界：仅用本地 HTTP 测试桩验证协议和错误处理；不是模型效果测评。

<a id="r32"></a>

### R32　JSON Schema Draft 2020-12

[JSON Schema project 原文](https://json-schema.org/draft/2020-12)

- 版本与日期：JSON Schema Draft 2020-12；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：JSON 结构、字段、枚举和条件约束。
- 使用边界：结构校验不能证明来源支持、权限或自由文本真实性。

<a id="r33"></a>

### R33　Ontology overview

[Palantir 原文](https://www.palantir.com/docs/foundry/ontology/overview/)

- 版本与日期：Palantir Ontology 在线概览；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：Ontology 连接数据、业务对象和操作的产品定位。
- 使用边界：厂商文档，不是独立效果评价；未连接 Foundry 租户验证。

<a id="r34"></a>

### R34　Ontology core concepts

[Palantir 原文](https://www.palantir.com/docs/foundry/ontology/core-concepts/)

- 版本与日期：Palantir Ontology Core concepts；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：对象类型、属性、链接等平台核心概念。
- 使用边界：同名本体概念不意味着自动采用 OWL 标准推理。

<a id="r35"></a>

### R35　Action types overview

[Palantir 原文](https://www.palantir.com/docs/foundry/action-types/overview/)

- 版本与日期：Palantir Action Types 在线文档；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：动作类型表达对象、属性或链接变更等操作。
- 使用边界：外部系统幂等、回执和业务完成定义需单独设计与验证。

<a id="r36"></a>

### R36　Access control propagation

[Palantir 原文](https://www.palantir.com/docs/foundry/security/access-control-propagation/)

- 版本与日期：Palantir Access control propagation 在线文档；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：强制控制与行列读时过滤的传播边界；派生内容需分别处理。
- 使用边界：读时过滤不自动传播到所有下游值；具体配置与外部输出边界需核查。

<a id="r37"></a>

### R37　Protégé documentation

[Stanford Protégé project 原文](https://protegeproject.github.io/protege/)

- 版本与日期：Protégé 5 Documentation；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：本体编辑器的文档、导航和扩展入口。
- 使用边界：未安装验证编辑器或推理器插件，不把其定位为业务执行平台。

<a id="r38"></a>

### R38　Ontology Development 101: A Guide to Creating Your First Ontology

[Natalya F. Noy and Deborah L. McGuinness / Stanford 原文](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)

- 版本与日期：Stanford 原始 PDF；经典方法教程；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：从用途和能力问题出发、迭代建模、复用词汇及不存在唯一正确模型的原则。
- 使用边界：已抽取并核对相关原文，渲染检查第 4 页；不使用其中旧工具描述判断当前产品。

<a id="r39"></a>

### R39　RDFLib security considerations

[RDFLib project 原文](https://rdflib.readthedocs.io/en/stable/security_considerations/)

- 版本与日期：RDFLib 在线安全说明；明确记录的发布日期：本次未统一确认，不作推断。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：解析与查询可能触发网络或文件访问，需约束不可信输入与执行环境。
- 使用边界：说明风险路径，不证明本教程已实现完整沙箱。

<a id="r40"></a>

### R40　RDF Dataset Canonicalization

[W3C 原文](https://www.w3.org/TR/rdf-canon/)

- 版本与日期：RDF Dataset Canonicalization Recommendation；明确记录的发布日期：2024-05-21。
- 核读范围：核对与书中论述有关的原文内容。
- 支持内容：RDF 数据集规范化以及确定性处理空白节点的标准路线。
- 使用边界：本教程只对文件和 JSON 载荷做摘要，未实现 RDF 数据集规范化算法。
