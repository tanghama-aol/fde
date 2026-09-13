# 术语表

本表采用本书工程语境。遇到标准术语，应以对应规范为准；厂商同名功能不一定采用完全相同的语义。

| 中文 / 缩写 | 英文 | 本书中的含义与易混点 |
| --- | --- | --- |
| 本体 | Ontology | 对用途相关概念、关系及语义的显式表示；并非任何画成图的数据结构 |
| 能力问题 | Competency question | 用于限定建模范围和验收的具体问题，需有输入、预期答案和边界 |
| 领域 | Domain of discourse | 建模所讨论的业务范围；与 RDFS 属性的 domain 声明不同 |
| 类 | Class | 用于描述一组个体的概念；实例属于类，子类约束类之间的包含关系 |
| 个体 / 实例 | Individual / instance | 领域中的具体对象，如甲公司北厂 P-101 |
| 属性 | Property | 表达关系或数值；OWL 区分对象属性与数据属性等 |
| 公理 | Axiom | 在选定逻辑语义下接受的陈述，如子类、逆属性或等价定义 |
| 逻辑蕴含 | Entailment | 某结论在满足前提的解释中成立；不同于概率很高的预测 |
| 开放世界假设 | Open-world assumption | 缺少事实不自动等于事实为假 |
| 唯一名称假设 | Unique name assumption | 不同名字必指不同对象的假设；OWL 不普遍默认该假设 |
| RDF | Resource Description Framework | 以三元组为基础的数据模型及相关规范 |
| 三元组 | Triple | 主语、谓语、宾语；图是三元组的集合，不靠记录顺序表达含义 |
| IRI | Internationalized Resource Identifier | 国际化资源标识符；稳定身份与展示名称应分离 |
| 字面量 | Literal | 带词法形式、数据类型或语言信息的值 |
| 空白节点 | Blank node | 没有全局 IRI 的节点；局部标签不是跨文件业务主键 |
| 命名图 | Named graph | RDF 数据集中带名称的图；名称本身不强制授权或来源真实性 |
| 数据集 | RDF dataset | 包含默认图和命名图的结构；默认图是否合并命名图取决于明确配置 |
| Turtle | Terse RDF Triple Language | RDF 图的文本序列化格式 |
| TriG | RDF Dataset Language | 可表示 RDF 数据集及命名图的文本格式 |
| JSON-LD | JSON for Linking Data | 使用上下文等机制表达关联数据的 JSON 格式 |
| RDFS | RDF Schema | 提供类、子类、属性等基本语义 |
| domain / range | Property domain / range | 与属性主语、宾语类型相关的语义声明；不是表单输入限制 |
| OWL 2 | Web Ontology Language | 具有多种语义与实现范围的本体语言体系 |
| OWL 2 RL | Rule Language profile | 便于基于规则实现的受限配置；不等于完整 OWL 2 DL |
| 逆属性 | Inverse property | 方向相反但表达对应关系的属性，如 partOf 与 hasPart |
| 传递属性 | Transitive property | 若 x 关联 y 且 y 关联 z，则 x 关联 z；必须符合实际含义 |
| 函数属性 | Functional property | 一个主体至多关联一个值；涉及对象时可能导出同一性，而非输入报错 |
| 同一性 | owl:sameAs | 强语义的个体相同断言；不是名称近似或普通业务关联 |
| 物化 | Materialization | 预先计算并保存推理结果；源事实撤回后需要维护派生结果 |
| 闭包 | Closure | 在选定规则与输入下扩展得到的结果集合 |
| SHACL | Shapes Constraint Language | 针对 RDF 数据图表达与检查约束的语言 |
| 形状 | Shape | 指定目标与约束的结构；其覆盖范围和推理配置需明确 |
| 焦点节点 | Focus node | 某次形状验证的被检查节点 |
| 闭合形状 | Closed shape | 限制允许属性的形状；不是将整个知识世界变成完整信息 |
| SPARQL | SPARQL Protocol and RDF Query Language | 查询 RDF 的语言及相关协议；Update 用于图更新 |
| 属性路径 | Property path | SPARQL 中沿指定关系组合查找的路径表达式 |
| R2RML | RDB to RDF Mapping Language | 从关系数据库映射到 RDF 的标准语言 |
| SKOS | Simple Knowledge Organization System | 组织受控概念、标签与语义关系的词汇 |
| PROV-O | PROV Ontology | 表达实体、活动、参与者及来源关系的本体 |
| SOSA / SSN | Sensor, Observation, Sample, and Actuator / Semantic Sensor Network | 观测、传感器、采样及相关系统建模词汇 |
| 知识图谱 | Knowledge graph | 组织实体、关系及其上下文的知识表示；不必都采用 RDF 或 OWL |
| 属性图 | Property graph | 节点和关系可具有属性的图模型；不自动提供 OWL 语义 |
| 实体对齐 / 链接 | Entity alignment / linking | 确定不同记录或文本提及对应何种实体，需保留歧义和证据 |
| RAG | Retrieval-augmented generation | 先检索相关资料，再用其辅助生成的路线 |
| GraphRAG | Graph retrieval-augmented generation | 图辅助检索与生成的多种路线统称，也可指具体项目；应说明实现 |
| 结构化输出 | Structured output | 按给定结构产生结果；结构合格不保证事实正确 |
| JSON Schema | JSON Schema | 约束 JSON 结构与取值的规范；与 RDF 的 SHACL 分工不同 |
| 神经符号 | Neuro-symbolic | 学习系统与显式符号表示、推理或约束的协作方式 |
| 证据包 | Evidence bundle | 本次任务获准使用的事实、文档、版本及来源集合，本书的工程概念 |
| 提案 | Proposal | 等待审核的具体业务变更建议，不等于已授权执行 |
| 幂等 | Idempotency | 重复请求不重复产生约定效果；需要定义键的范围、保存期与业务含义 |
| 条件写入 | Conditional write | 仅在版本或状态等前提满足时修改数据 |
| 对账 | Reconciliation | 按稳定请求与回执核对外部实际效果，处理结果未知 |
| 补偿 | Compensation | 用后续业务操作纠正已有效果；不一定能恢复成从未发生过 |
| 新鲜度 | Freshness | 数据距可信业务时钟的可接受年龄；导入时间不等于观测时间 |
| 来源 / 血缘 | Provenance / lineage | 数据由何来源、处理和活动产生，便于追溯与影响分析 |
| Hit@k | Hit at k | 前 k 个结果中是否包含指定相关目标的案例比例，分母必须明确 |
| 消融实验 | Ablation study | 移除或增加特定组件，判断其独立贡献的实验 |
| FDE | Forward Deployed Engineer | 嵌入业务现场，把技术系统交付为可运行工作流的工程角色 |

返回[书籍目录](README.md)。
