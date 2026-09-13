# 资料来源与核验说明

**核验截止：2026-09-13。** 本目录收录 49 项已获取并核读相关正文的资料，包含厂商官方文档、公司公告、政府文件、主办机构报道和项目官方文档。技术文档没有稳定发布日期时记为“动态文档”，不以网页版权年份推定发布年份。

来源编号与[完整指南](../docs/fde-engineer-guide.md)对应。这里保存原文链接、事实摘要、边界和机器可读核验记录；不重新发布原始网页全文。抓取内容的摘要哈希用于追溯本次核对版本，不代表页面未来不会变化。

## 先读这几项

| 需要核实的内容 | 优先资料 |
| --- | --- |
| Foundry / AIP / Apollo 与 FDE 方法 | [P01](#p01)、[P02](#p02)、[P18](#p18) |
| 本体怎样设计和执行动作 | [P03](#p03)、[P07](#p07)、[P19](#p19)、[P23](#p23) |
| DeployCo 的组织与交付模式 | [O01](#o01)、[O02](#o02) |
| OpenAI 产品生命周期变化 | [O04](#o04) 的 2026-06-03 更新 |
| 上海“百千万”和培养矩阵 | [S01](#s01)、[S02](#s02) |
| 政策依据及报名入口 | [S03](#s03)、[S05](#s05)、[S07](#s07) |

## 核验边界和未确认事项

- **事实、建议、示例分开。** 8 周工期、90 天学习安排、团队配置、评分权重、阈值、ROI 和订单案例均为本指南建议或合成示例，不是任何厂商的标准承诺。
- **计划与完成状态分开。** 未查到足以确认上海“百千万”目标全部完成的官方汇总；也未用 DeployCo 发布公告确认 Tomoro 收购已经最终交割。
- **平台与账号状态分开。** 没有登录客户的 Foundry、OpenAI 或其他商业产品账号，不声称某项能力对所有地区和账号开放。
- **API 参考的访问限制。** 本次部分 developers.openai.com / platform.openai.com 页面返回访问错误，因此用已读取的 OpenAI 官方发布说明核对产品定位和退役更新；未按未能读取的页面编造最新参数、价格和配额。正文没有提供声称已验证运行的 OpenAI SDK 代码。
- **公众号可复查性。** S02 正文位于页面的静态文章载荷，本次已解码核读，未执行网页脚本。来源链接带签名，未来可能需要重新检索文章标题或在微信打开；关键数量同时由学院官网 S01 支持。
- **未采纳的二手数字。** 招聘暴涨倍数、薪资、企业 AI 失败率、案例节省比例等未有足够原始证据支持的说法，没有转为本指南的结论。官方转载中的引用数字也不自动成为独立验证。
- **培训日期优先原始报道。** 对首期培训起点的转述存在差异，采用学院 2025-12-09 正文中“11 月 29 日正式开班、12 月 6 日专题课”的细分时间口径。

## 更新方法

新增资料先检查发布者和日期，再打开正文，记录它实际支持的结论及不支持的外推。政策记录文号；公司事项记录宣布、签约和完成状态；技术资料记录版本或核验日期。发现冲突时在这里说明取舍，并同步修改指南，而不是只往链接清单追加。

建议在新项目选型时重新检查模型、SDK、产品退役、商业许可、部署地区和培训招募；涉及本体、权限或业务动作的版本变更要回放本项目的评估集。

## Palantir：平台、本体与交付

<a id="p01"></a>
### P01 · Architecture center overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/architecture-center/overview/) · **支持：** Forward Deployed Engineering 与核心研发的反馈关系；Foundry、AIP、Apollo 的平台分工。

**边界：** 平台自身的架构说明；不是独立性能测试。

<a id="p02"></a>
### P02 · Ontology overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology/overview/) · **支持：** Ontology 作为组织运营层；语义要素与动作、函数、安全要素相结合。

**边界：** 不能据此宣称任何数据库或知识图谱天然等价于 Foundry Ontology。

<a id="p03"></a>
### P03 · Ontology core concepts

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology/core-concepts/) · **支持：** 对象、属性、关系、动作、函数和接口的定义。

**边界：** 概念解释；不构成某个客户本体设计的正确性证明。

<a id="p04"></a>
### P04 · Data Connection overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/data-connection/overview/) · **支持：** 外部数据同步、连接器及接入原则；通过 Webhooks 和导出配置外部写回。

**边界：** 连接器存在不保证客户系统所有字段、认证和写回要求均已覆盖。

<a id="p05"></a>
### P05 · Pipeline Builder overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/pipeline-builder/overview/) · **支持：** 可视化数据转换、输出检查、版本及批流处理能力。

**边界：** 部分功能随部署环境变化；不应把架构说明当作具体性能承诺。

<a id="p06"></a>
### P06 · Code Repositories overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/code-repositories/overview/) · **支持：** Git 协作、数据转换和 Functions 代码开发。

**边界：** 不同仓库、语言和版本的功能支持需要分别核验。

<a id="p07"></a>
### P07 · Action types overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/action-types/overview/) · **支持：** 动作修改本体对象、属性和关系，可有副作用；动作体现完整业务操作。

**边界：** 本体内事务不能外推为所有外部系统的分布式原子事务。

<a id="p08"></a>
### P08 · Functions overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/functions/overview/) · **支持：** 服务端业务逻辑、对象查询及编辑；TypeScript 与 Python Functions。

**边界：** 不同语言的特性和权限仍需查阅具体版本说明。

<a id="p09"></a>
### P09 · Workshop overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/workshop/overview/) · **支持：** 基于对象层构建业务应用；Actions 写回、Functions 逻辑和交互任务界面。

**边界：** 界面可构建不等于用户已采用或流程已改善。

<a id="p10"></a>
### P10 · Ontology SDK overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology-sdk/overview/) · **支持：** 从自定义应用访问类型化本体能力；令牌范围与用户权限共同约束读取。

**边界：** 读取过滤不会自动约束应用收到数据后的全部行为，需结合 P23。

<a id="p11"></a>
### P11 · AIP overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/aip/overview/) · **支持：** AI 与企业数据、运营流程及治理的集成；AIP 工具组合。

**边界：** 官方明确功能可得性可能因客户环境不同而变化。

<a id="p12"></a>
### P12 · AIP Logic overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/logic/overview/) · **支持：** 构建、测试和发布利用本体的 LLM 函数；本体编辑可自动应用或暂存供人审查。

**边界：** 自动应用需要实际授权；输出和下游传播仍须治理。

<a id="p13"></a>
### P13 · AIP Evals overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/aip-evals/overview/) · **支持：** 测试用例、评估函数、版本比较、模型比较及重复运行方差。

**边界：** 不等同于 OpenAI 的同名 Evals 平台产品；评估质量仍取决于样本及评分。

<a id="p14"></a>
### P14 · AIP Chatbot Studio overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/chatbot-studio/overview/) · **支持：** 结合本体、文档和工具构建交互助手；当前文档说明其旧称为 AIP Agent Studio。

**边界：** 新旧名称可见于不同版本资料，不应当作完全不同的产品重复计算。

<a id="p15"></a>
### P15 · Automate overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/automate/overview/) · **支持：** 按时间和对象条件触发动作、函数及通知。

**边界：** 触发自动化仍需考虑执行身份、幂等、外部副作用和回执。

<a id="p16"></a>
### P16 · Security and governance overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/security/overview/) · **支持：** 身份与授权、强制和自主访问控制、治理框架。

**边界：** 平台安全功能不能替代客户实际配置、数据分级与应用审查。

<a id="p17"></a>
### P17 · Marketplace overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/marketplace/overview/) · **支持：** 发布产品的发现、安装和版本更新机制。

**边界：** 打包可复用不等于无需客户配置、验证或迁移。

<a id="p18"></a>
### P18 · Delivering a use case

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/getting-started/delivering-a-use-case/) · **支持：** 以结果、数据和工具组织用例交付；记录决策并评估其后续影响。

**边界：** 指南中的 8 周安排由本文提出，并非该文档承诺。

<a id="p19"></a>
### P19 · Ontology design: Best practices

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology/ontology-best-practices/) · **支持：** 领域驱动、减少重复、扩展与组合的设计原则；按真实业务建模并通过任务验证。

**边界：** 原则需结合组织实际；不存在统一最优对象数量。

<a id="p20"></a>
### P20 · Ontology design: Anti-patterns

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology/ontology-anti-patterns/) · **支持：** 源系统孤岛、字段堆砌、万能对象和动作膨胀等反模式。

**边界：** 用于设计审查，不应机械照搬示例数据模型。

<a id="p21"></a>
### P21 · Getting started with Palantir

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/getting-started/overview/) · **支持：** 学习、用例和试用申请入口。

**边界：** 未核实个人账号资格、所在地区可得性、收费或审批结果。

<a id="p22"></a>
### P22 · Ontology scenarios overview

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/ontology/overview-ontology-scenario/) · **支持：** what-if 分析和隔离动作模拟；当前为 Beta，且不用于历史数据快照。

**边界：** 具体可用性及行为随环境和版本变化；不能替代评估输入快照。

<a id="p23"></a>
### P23 · Access control propagation

**发布者：** Palantir。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.palantir.com/docs/foundry/security/access-control-propagation/) · **支持：** 强制控制与行列读取过滤的传播差异；函数、模型、OSDK、写回及导出中的控制边界。

**边界：** 平台内强制控制的传播说明不等于导出的外部文件仍受同一平台强制控制。

## OpenAI：部署组织与开发工具

<a id="o01"></a>
### O01 · OpenAI launches the OpenAI Deployment Company to help businesses build around intelligence

**发布者：** OpenAI。**日期：** 2026-05-11。

[原文](https://openai.com/index/openai-launches-the-deployment-company/) · **支持：** DeployCo 的控制权、超过 40 亿美元初始投资及合作生态；价值诊断、少数优先工作流、嵌入客户组织并交付生产系统；同意收购 Tomoro，拟带来约 150 名 FDE 和部署专家。

**边界：** 公告仍包含交割条件；未据此确认收购最终完成、标准报价、统一周期或已完成客户数。

<a id="o02"></a>
### O02 · Introducing Frontier Alliances

**发布者：** OpenAI。**日期：** 2026-02-23。

[原文](https://openai.com/index/frontier-alliance-partners) · **支持：** Frontier 的技术基础角色；BCG、McKinsey、Accenture、Capgemini 与内部 FDE 的协作分工。

**边界：** 发布时的可得性说明不是 2026-09 的账号授权承诺；未据此声称所有 DeployCo 项目强制采用 Frontier。

<a id="o03"></a>
### O03 · New tools for building agents

**发布者：** OpenAI。**日期：** 2025-03-11。

[原文](https://openai.com/index/new-tools-for-building-agents/) · **支持：** Responses API、Agents SDK、内置工具与工作流可观测能力的发布及定位。

**边界：** 历史发布说明，未用其中早期模型、价格、工具参数或 Assistants 退役预告代表当前 API 规范。

<a id="o04"></a>
### O04 · Introducing AgentKit — updated June 3, 2026

**发布者：** OpenAI。**日期：** 2025-10-06；重要更新 2026-06-03。

[原文](https://openai.com/index/introducing-agentkit/) · **支持：** 更新说明 Agent Builder 与 Evals 平台产品将于 2026-11-30 停止提供；对需要以代码继续的工作流建议使用 Agents SDK。

**边界：** 优先采用页首更新，不沿用正文旧的可得性描述；不能外推为所有评估能力、所有同名 API 或 Agents SDK 一并停用。

## 上海：培养目标、政策与实践

<a id="s01"></a>
### S01 · 打通AI落地“最后一公里”！上海首期FDE专题培训创智开讲

**发布者：** 上海创智学院。**日期：** 2025-12-09。

[原文](https://www.sii.edu.cn/2025/1208/c22a620/page.htm) · **支持：** 正文记载 11 月 29 日正式开班、12 月 6 日专题课；百家企业、千个智能体、万名开发者转型及超千人储备库目标；培训强调业务现场、需求拆解、流程优化和实时迭代。

**边界：** 目标不是完成统计；页面路径中的日期不能替代正文显示的发布日期。

<a id="s02"></a>
### S02 · 上海首期FDE专题培训圆满收官

**发布者：** 上海规划资源（转载上海创智学院供稿）。**日期：** 正文事件日期 2025-12-20。

[原文](https://mp.weixin.qq.com/s?src=11&timestamp=1789299991&ver=6964&signature=MDpYrZqeOXPYyIgYylS6ZV8qdAIGBaT68*38LFEf-lm3q2TV8WItr59ody1fyzzqsUR0rWLrSzEXNXn63mnMKd3rEsaf-SCpffua-*9J-tOXyqmgHFMZPX6UyTFAzQBE&new=1) · **支持：** 首期培训收官和联合组织单位；三类人群、三个阶段、三类能力的 3+3+3 矩阵；2026 年分行业招募方向、基础条件与报名入口。

**边界：** 已从页面静态文章载荷核读正文；公众号签名链接可能失效。关键数量与 S01 交叉核对，未核实当前批次名额及完成统计。

<a id="s03"></a>
### S03 · 上海市支持先进制造业转型升级三年行动方案（2026—2028年）

**发布者：** 上海市人民政府办公厅。**日期：** 2026-01-09；沪府办规〔2025〕20号。

[原文](https://www.shanghai.gov.cn/nw12344/20260109/3c4f820bca7b46cd878efcb121337bdd.html) · **支持：** 第七项深化数智转型：AI+制造、培育 FDE 队伍、行业模型和工业智能体；方案自 2026-01-01 实施，有效期至 2028-12-31。

**边界：** 没有把方案其他补贴条款解读为 FDE 培训统一补贴或个人资质。

<a id="s04"></a>
### S04 · 打造AI落地“特种兵”，徐汇首期FDE专题培训创智开讲

**发布者：** 徐汇区人民政府 / 上海市政府网站。**日期：** 2026-02-13。

[原文](https://www.shanghai.gov.cn/nw15343/20260213/57783c983a3b4e0194dd6e350a38bdb1.html) · **支持：** 政企融合编班、大班授课、小班研讨和项目实训；区级培训与真实产业场景对接。

**边界：** 区级项目目标与全市百千万目标分别记录；未把开班参加人数当作合格 FDE 人数。

<a id="s05"></a>
### S05 · 上海市战略性新兴产业发展“十五五”规划

**发布者：** 上海市人民政府办公厅。**日期：** 2026-08-26；沪府办发〔2026〕19号。

[原文](https://www.shanghai.gov.cn/nw12344/20260826/0f32f0c1379a4e949a1ca414b0be25b5.html) · **支持：** 人工智能章节提出培养 FDE 团队；政策支持校企协同育人、驻企实训等模式。

**边界：** 宏观产业规划，不是课程报名简章，也不证明具体培养数量已完成。

<a id="s06"></a>
### S06 · FDE企业AI落地班上海专场在虹口举办！规上企业参与AI场景共创

**发布者：** 虹口区人民政府 / 上海市政府网站。**日期：** 2026-08-27。

[原文](https://www.shanghai.gov.cn/nw15343/20260827/7e015e8fb2dd407f887bc72a844bb2d0.html) · **支持：** 企业问题诊断、专家匹配、现场方案共创的活动方式；虹口与 Datawhale 的企业场景对接。

**边界：** 未将文中引述的岗位需求增幅用作本指南的就业结论；行业认证不能直接等同国家职业资格。

<a id="s07"></a>
### S07 · FDE专项培训报名表

**发布者：** GDPS 报名平台（S02 指向的入口）。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://form.gdps.org.cn/fde) · **支持：** 核验日表单可访问，列有企业、个人、技能和项目经历字段。

**边界：** 仅核对页面可访问性和字段，未提交申请；不证明当期名额、费用、课程安排或录取资格。

## 工程工具：接入、编排、评估与运行

<a id="t01"></a>
### T01 · Architecture overview

**发布者：** Model Context Protocol。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://modelcontextprotocol.io/docs/learn/architecture) · **支持：** MCP 的客户端、服务端、工具、资源和提示等概念；协议负责上下文交换，不决定应用如何使用模型。

**边界：** 未将某个协议版本的全部握手和认证细节固化进教程；实际集成应锁定双方版本。

<a id="t02"></a>
### T02 · LangGraph overview

**发布者：** LangChain。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.langchain.com/oss/python/langgraph/overview) · **支持：** 有状态智能体、确定性和模型步骤组合、持久化与人工介入。

**边界：** 框架能力需要正确配置持久化和恢复；不意味着外部业务副作用天然幂等。

<a id="t03"></a>
### T03 · Temporal Workflow Execution overview

**发布者：** Temporal。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.temporal.io/workflow-execution) · **支持：** 持久执行、事件历史、重放及与 Activity 的分工。

**边界：** 工作流可恢复不能单独保证外部系统业务效果恰好执行一次。

<a id="t04"></a>
### T04 · pgvector README

**发布者：** pgvector 项目。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://github.com/pgvector/pgvector) · **支持：** 精确和近似向量检索；HNSW、IVFFlat 与过滤条件的取舍。

**边界：** 召回与性能取决于数据、索引参数、过滤和负载；未做具体环境基准测试。

<a id="t05"></a>
### T05 · Row Security Policies

**发布者：** PostgreSQL。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) · **支持：** 行级策略及默认拒绝行为；超级用户、BYPASSRLS 和表所有者等例外。

**边界：** 应按部署版本核验；仅有策略定义不能证明服务实际使用了受限身份。

<a id="t06"></a>
### T06 · Add data tests to your DAG

**发布者：** dbt Labs。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.getdbt.com/docs/build/data-tests) · **支持：** 非空、唯一性、关系、允许值和自定义数据测试。

**边界：** 数据测试应反映业务断言；通过测试不等于全部数据正确。

<a id="t07"></a>
### T07 · Signals

**发布者：** OpenTelemetry。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://opentelemetry.io/docs/concepts/signals/) · **支持：** Traces、metrics、logs 等观测信号的职责。

**边界：** 收集日志要服从数据保护和保留要求；可观测性不能替代业务评估。

<a id="t08"></a>
### T08 · Dify Documentation

**发布者：** Dify。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.dify.ai/en/use-dify/getting-started/introduction) · **支持：** AI 应用、工作流、数据接入和 API 发布定位；云端及社区自托管路径。

**边界：** 未核验所有版本、企业功能或许可场景；采购及商用需另查适用条款。

<a id="t09"></a>
### T09 · Airbyte Protocol

**发布者：** Airbyte。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.airbyte.com/platform/understanding-airbyte/airbyte-protocol) · **支持：** Source、Destination、Stream、Catalog 及数据接入协议概念。

**边界：** 未为具体客户验证连接器的字段覆盖、删除语义和增量一致性。

<a id="t10"></a>
### T10 · Debezium Architecture

**发布者：** Debezium。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://debezium.io/documentation/reference/stable/architecture.html) · **支持：** 数据库变更捕获及 Kafka Connect、Server、Engine 部署方式。

**边界：** 不必强制使用 Kafka；选择方式取决于客户现有基础设施。

<a id="t11"></a>
### T11 · n8n Docs

**发布者：** n8n。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.n8n.io/) · **支持：** 结合 AI 和业务流程的工作流自动化定位。

**边界：** 官方自述采用 fair-code 许可，不能笼统写成无限制开源商用。

<a id="t12"></a>
### T12 · vLLM documentation

**发布者：** vLLM。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://docs.vllm.ai/en/latest/) · **支持：** 大模型推理与服务框架，批处理、缓存和多种模型适配。

**边界：** 硬件与模型组合的可用性、显存、延迟、许可及成本均需具体评估。

<a id="t13"></a>
### T13 · Langfuse Overview

**发布者：** Langfuse。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://langfuse.com/docs) · **支持：** LLM 轨迹、提示版本、评估、成本和延迟观测。

**边界：** 自托管与商业服务功能边界、数据保留和成本需按实际版本核验。

<a id="t14"></a>
### T14 · Open Policy Agent documentation

**发布者：** Open Policy Agent。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://www.openpolicyagent.org/docs) · **支持：** 用策略代码进行决策，将策略决策与执行点分离。

**边界：** OPA 的输入必须可信，调用方必须真正执行决策结果。

<a id="t15"></a>
### T15 · FastAPI documentation

**发布者：** FastAPI。**日期：** 动态文档 / 页面未标稳定发布日期。

[原文](https://fastapi.tiangolo.com/) · **支持：** 基于 Python 类型提示构建 API，支持 OpenAPI 和 JSON Schema。

**边界：** 未采用页面上的开发速度和缺陷下降宣传数字作为本指南收益承诺。
