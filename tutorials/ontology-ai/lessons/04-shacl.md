# 第 04 课　SHACL 校验

目标：读取有效与无效图的校验报告，判断错误发生在哪个节点与属性。对应书籍第 05 章。

## 操作

```console
python -m ontology_lab validate
```

应看到 `valid_fixture.conforms: true`、`deliberately_invalid_fixture.conforms: false` 和 `expected_behavior: true`。因为拒绝故意错误数据本身就是成功结果，该演示整体正常退出。

打开[shapes.ttl](../data/shapes.ttl)和[invalid.ttl](../data/invalid.ttl)。报告里的每条违反包含：

| 字段 | 含义 |
| --- | --- |
| focus | 被检查且违反约束的节点 |
| path | 出问题的属性路径 |
| component | 触发的 SHACL 约束类型 |
| message | 校验器生成的说明 |

## 解释

错误样本包含缺少设备版本、错误单位和非 decimal 的观测值。一个错误值可能同时违反数据类型与数值范围，因此违反条目数不等于错误对象数。

本教程向校验器显式传入已解析的 RDF 图，并指定 `inference="rdfs"`。形状目标、类层级和推理配置共同决定哪些节点接受校验；不应省略配置后假设所有引擎给出相同结果。

静态校验通过只说明这个图在当前形状与配置下符合合同。它没有验证温度传感器是否校准正确，也不能保证十分钟后记录仍然新鲜。

## 常见失败

`sh:datatype xsd:decimal` 对 RDF 字面量类型有要求，不能仅凭显示值“像数字”判断合格。排查时同时看词法值与 datatype。若引入闭合形状，原本合法的来源字段也可能被拒绝，需要先明确允许字段及演进方式。

## 练习

复制错误样本，在副本中补齐版本、改为 decimal 值及摄氏度单位，用 `validate_graph` 校验副本。说明哪些修改是在修复表示，哪些需要回到源系统核实。不能为了通过校验随意编造缺失版本或测量值。

下一课：[数据导入](05-ingestion.md)。
