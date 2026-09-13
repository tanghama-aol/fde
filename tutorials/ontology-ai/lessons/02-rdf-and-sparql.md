# 第 02 课　RDF 与 SPARQL

目标：把源数据理解为带身份的图，并区分管理员教学查询与最终用户的授权查询。对应书籍第 03、08 章。

## 操作

```console
python -m ontology_lab rdf
```

`assets` 中应有甲公司三台设备：P-101、P-102、P-201；`named_graphs` 列出两个租户图；`default_union` 为 `false`。这条命令是管理员视角的合成数据教学演示，故意没有按北厂用户过滤 P-201。最终用户访问边界在第 06 课演示。

阅读[本体](../data/ontology.ttl)与[查询](../queries/assets.rq)。关键模式为：

```sparql
?asset rdf:type/rdfs:subClassOf* ex:Asset ;
       ex:assetId ?assetId ;
       ex:region ?region ;
       ex:version ?version .
```

## 解释

这里从对象的显式类型出发，沿零次或多次 `subClassOf` 找到 Asset。它是 SPARQL 属性路径查询，本身不代表已经运行完整 OWL 推理。程序可以在没有预先物化所有父类类型的图上查到离心泵。

`https://example.org/data/TENANT-A/asset/P-101` 是设备身份；“北厂循环泵”是带中文语言标签的名称。命名图组织租户数据，但图名不会自动拒绝越权请求。应用必须决定哪个用户能查询哪个图及哪些对象。

结果行不是天然的实体计数。一台设备若有多种标签和多条观测，连接查询可能返回多行，统计时应明确去重与最新记录规则。

## 常见失败

把图数据库中的默认图误当成所有命名图的并集，可能导致查询为空或查询范围扩大。本教程显式关闭默认并集。把所有关系替换为简单字符串，也会丢失稳定身份与可连接性。

## 练习

复制查询为自己的实验文件，给模式加入 `FILTER(?region = "NORTH")`。预期甲公司剩两台设备。说明为什么固定区域筛选仍不能替代可信身份授权：用户可否选择其他区域，必须由服务端决定。

下一课：[逻辑推理](03-reasoning.md)。
