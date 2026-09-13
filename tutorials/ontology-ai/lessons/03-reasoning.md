# 第 03 课　逻辑推理

目标：观察类型、逆关系和传递关系的物化结果，理解逻辑推理的前提。对应书籍第 04、12 章。

## 操作

```console
python -m ontology_lab reason
```

锁定数据与依赖下，输出的重要字段为：

```json
{
  "asserted_triples": 125,
  "closure_triples": 451,
  "added_triples": 326,
  "asserted_asset_type": false,
  "inferred_asset_type": true,
  "inferred_inverse": true,
  "inferred_transitive_part": true
}
```

查看[graph.py](../ontology_lab/graph.py)中的 `infer`。它复制输入图，然后调用 OWL RL 闭包扩展，保留原始图不变。

## 解释

P-101 显式类型为 `CentrifugalPump`。通过 `CentrifugalPump → Pump → Asset` 得到 Asset 类型。设备 `partOf` 产线，产线 `partOf` 厂区；`partOf` 被声明为传递属性，所以得到设备属于厂区。`hasPart` 是逆属性，因此产线包含设备。

增加 326 条三元组不等于发现 326 条新的业务事实，其中包含规则物化产生的模式与语义相关语句。结果还会受依赖版本和数据内容影响。最重要的检查是预期蕴含是否出现、输入图是否保持不变。

本教程使用 OWL RL 规则物化，不是完整 OWL 2 DL 推理器，未生成推理证明树。缺少某条记录，也不能依照开放世界语义直接推断其否定。

## 常见失败

把 `rdfs:range ex:Asset` 当成拒绝输入的规则，会误解输出：推理器可能给目标节点补上 Asset 类型。希望报错时，应定义数据合同并校验，见下一课。

## 练习

在一份临时本体中移除 `owl:TransitiveProperty`，保持其他事实不变，再比较目标关系是否仍会被推导。解释为什么两个源关系存在，不代表所有谓词都允许传递；“与某人认识”就不能默认具有这种性质。

下一课：[SHACL 校验](04-shacl.md)。
