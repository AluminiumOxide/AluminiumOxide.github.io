---
title: "deep_decoder_note_1"
date: "2022-09-19"
categories: 
  - "blog"
---

直接看fit

右键evaluate expression在调试中常见看图的备份

```
import matplotlib.pyplot as plt
plt.imshow(out[0][0].detach().cpu().numpy())
plt.show()
plt.close()
```

添加环境变量啊误！
