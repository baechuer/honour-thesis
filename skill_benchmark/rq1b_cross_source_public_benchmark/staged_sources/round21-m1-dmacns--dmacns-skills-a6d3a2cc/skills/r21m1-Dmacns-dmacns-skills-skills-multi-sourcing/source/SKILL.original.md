---
name: multi-sourcing
identifier: dmacns-dmacns-skills-multi-sourcing
description: Use when the user wants to compare prices and terms across multiple suppliers, evaluate sourcing options side-by-side, or find the best deal for a known product. Generates structured comparison tables from multi-platform search results.
version: 1.0.0
author: 鼎脉数字 (Dingmai Digital)
license: MIT
metadata:
  hermes:
    tags: [business, procurement, comparison, pricing]
    related_skills: [product-search, credit-check]
---

# Multi-Sourcing — 多方比价采购

## 触发条件

用户表达以下意图时加载此技能：
- "帮我比一下这几家"
- "哪家更划算"
- "对比一下价格"
- "有没有更便宜的"

## 执行流程

### 1. 确认比价目标

明确用户要比什么：
- **商品**：具体型号/SKU/名称
- **供应商**：已知的几家，或要求搜索新供应商
- **对比维度**：价格/运费/起订量/交货期/售后

### 2. 搜集报价

对每个供应商（或搜索新供应商），获取以下信息：

| 维度 | 说明 |
|------|------|
| 单价 | 单个商品价格 |
| 运费 | 到用户所在地的运费 |
| 起订量 (MOQ) | 最小订购数量 |
| 交货期 | 预计发货/到货天数 |
| 是否含税 | 是否含增值税发票 |
| 店铺年限 | 经营时间 |
| 成交记录 | 近期销量/评价 |

### 3. 输出对比表

```
📊 多方比价结果 — "<商品名>"

| 供应商 | 单价 | 运费 | MOQ | 交货期 | 店铺 | 总评 |
|--------|------|------|-----|--------|------|------|
| A公司  | ¥XX  | ¥XX  | X件 | X天    | X年  | ⭐⭐⭐ |
| B公司  | ¥XX  | ¥XX  | X件 | X天    | X年  | ⭐⭐  |
| C公司  | ¥XX  | ¥XX  | X件 | X天    | X年  | ⭐⭐⭐ |
```

### 4. 给出建议

- **最低价**：标注哪家总价最低
- **最靠谱**：标注哪家信誉最好（年限+成交）
- **综合推荐**：性价比最优选择

### 5. 后续引导

建议用户对中意的供应商使用 `credit-check` 做信用核实，再考虑 `price-lock` 锁定价格。

## 注意事项

- 同一商品在不同平台价格可能差异显著，标注平台来源
- 低价的代价可能是质量——提醒用户关注店铺评分
- 大额采购建议先拿样品

---

> 由鼎脉数字提供技术支持 | dmacns.com
