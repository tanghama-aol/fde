# 第 01 课　环境与案例

目标：运行环境检查，并能说清系统中的对象、身份、时间和动作。对应书籍第 01—02 章。

## 操作

先按[教程入口](../README.md)安装依赖。以下各课都在 `tutorials/ontology-ai` 目录执行：

```console
python -m ontology_lab doctor
```

报告应显示 `data_present: true`、四个核心库的版本、`network_needed_for_core_lessons: false`，以及固定业务时间。实测版本为 RDFLib 7.1.4、OWL-RL 7.1.4、pySHACL 0.30.1 和 jsonschema 4.25.1。

阅读[设备](../data/assets.csv)与[观测](../data/observations.csv)。先手工完成下表，再查看后续程序输出：

| 租户 | 设备 | 区域 | 观测 | 当前版本 |
| --- | --- | --- | --- | --- |
| TENANT-A | P-101 | NORTH | 92 C | 7 |
| TENANT-A | P-102 | NORTH | 161.6 F | 4 |
| TENANT-A | P-201 | SOUTH | 94 C | 5 |
| TENANT-B | P-101 | NORTH | 40 C | 2 |

## 解释

两个租户都存在 P-101，因此设备编号本身不能全局标识实物。程序默认使用甲公司北厂计划员身份，身份由服务端示例配置提供，不从问题文本或模型响应中读取。

系统的业务时间固定在观测后两分钟。后续过期测试会推进传入的时钟，验证缺少新数据时停止提案。唯一动作是创建草稿；温度超过 80 C 是教学核查规则，不表示已诊断故障。

## 常见失败

环境检查找不到模块时，先确认当前目录，再确认 Python 环境。`doctor` 不会安装依赖或启动模型，它只检查运行环境。不要把 `network_needed_for_core_lessons: false` 理解为首次安装也无需网络。

## 练习

写出本案例的三条能力问题，各给一个正常输入和一个不能直接回答的输入。参考：北厂设备当前温度；当前有效程序；某个执行请求是否已创建草稿。跨区域、观测缺失与外部结果未知应分别有明确处理。

下一课：[RDF 与 SPARQL](02-rdf-and-sparql.md)。
