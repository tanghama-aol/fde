# 项目模板

这些是可复制修改的项目工作文件。YAML 为本指南定义的说明格式，**不是 Foundry、OpenAI、dbt 或其他平台可以直接导入执行的配置**。填写模板不会自动启用权限、连接系统或部署服务。

| 模板 | 何时使用 | 产物 |
| --- | --- | --- |
| [项目任务书](project-charter.md) | 决定是否启动试点 | 范围、责任、基线、验收与继续投入条件 |
| [现场访谈](discovery-interview.md) | 第一次接触真实业务流程 | 正常、异常、等待、判断及证据 |
| [数据契约](data-contract.yaml) | 接入和建模前 | 权威来源、主键、字段、时效与权限 |
| [动作契约](action-contract.yaml) | 开放写入工具前 | 参数、批准、幂等、回执与恢复 |
| [评估计划](evaluation-plan.md) | 原型前开始，贯穿交付 | 数据分层、评分、指标、门槛及复核 |
| [上线与交接](release-and-handover.md) | 试点和每次发布 | 发布清单、监控、停止、对账和责任 |
| [架构决策记录](architecture-decision.md) | 出现重要技术取舍时 | 约束、候选、证据、退出和复查条件 |

配套的[订单异常案例](../examples/order-exception/README.md)提供如何填写的上下文，[评估案例集](../examples/order-exception/eval-cases.jsonl)展示正常和失败情形。案例集尚未对任何模型或业务系统运行，不可当作通过报告。
