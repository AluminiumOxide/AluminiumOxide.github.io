---
title: "Graphviz_2_Examples"
date: "2022-10-09"
categories: 
  - "allophane"
  - "extracurricular"
---

[示例 — 图形 0.20.1 文档 (graphviz.readthedocs.io)](https://graphviz.readthedocs.io/en/stable/examples.html)

提示: 以下代码示例包含在[源存储库/分发](https://github.com/xflr6/graphviz/tree/master/examples/)版的目录中。`examples/`  
注意: 他们中的大多数从 [graphviz.org 库](https://www.graphviz.org/gallery/)或 [graphviz.org 文档中](https://www.graphviz.org/documentation/)重新创建示例。

hello.py

```
import graphviz

g = graphviz.Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()
```

process.py

```
import graphviz

g = graphviz.Graph('G', filename='process.gv', engine='sfdp')

g.edge('run', 'intr')
g.edge('intr', 'runbl')
g.edge('runbl', 'run')
g.edge('run', 'kernel')
g.edge('kernel', 'zombie')
g.edge('kernel', 'sleep')
g.edge('kernel', 'runmem')
g.edge('sleep', 'swap')
g.edge('swap', 'runswap')
g.edge('runswap', 'new')
g.edge('runswap', 'runmem')
g.edge('new', 'runmem')
g.edge('sleep', 'runmem')

g.view()
```
