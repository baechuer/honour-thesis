---
name: product-search
identifier: dmacns-dmacns-skills-product-search
description: Use when the user wants to search for product suppliers, find sourcing options, or discover manufacturers for a specific product category. Searches across major B2B and B2C platforms and returns structured supplier information.
version: 1.0.0
author: 鼎脉数字 (Dingmai Digital)
license: MIT
metadata:
  hermes:
    tags: [business, procurement, sourcing, supply-chain]
    related_skills: [multi-sourcing, credit-check]
---

# Product Search — 智能货源搜索

## 触发条件

用户表达以下意图时加载此技能：
- "帮我找 XX 的供应商"
- "哪里有 XX 的货源"
- "搜一下 XX 批发"
- "我想采购 XX"

## 执行流程

### 1. 确认需求

从用户消息中提取关键参数：
- **商品名称**：必填
- **品类/规格**：选填，越精确越好
- **预算范围**：选填，如"200以内"
- **最小起订量**：选填
- **产地偏好**：选填，如"义乌""深圳"

如果商品名称模糊，向用户确认后再搜索。

### 2. 多渠道搜索

依次搜索以下平台（至少搜索 2 个）：

| 平台 | 适合 | URL/方式 |
|------|------|----------|
| 1688 | 批发采购 | `web_search` 搜索 `site:1688.com <商品名> 批发` |
| 义乌购 | 小商品 | `web_search` 搜索 `site:yiwugo.com <商品名>` |
| 淘宝 | 零售/小批 | `web_search` 搜索 `<商品名> 批发 淘宝` |
| 拼多多 | 低价批量 | `web_search` 搜索 `<商品名> 拼多多 批发` |

### 3. 结构化输出

将结果整理为表格：

```
🔍 "<商品名>" 搜索结果

| # | 供应商 | 价格 | 起订量 | 所在地 | 平台 |
|---|--------|------|--------|--------|------|
| 1 | XX公司 | ¥XX | X件 | 义乌 | 1688 |
| 2 | ... | ... | ... | ... | ... |
```

附加信息：
- 价格区间（最低-最高）
- 推荐理由（如"3年老店""100+成交"）
- 如果搜索结果为空，建议扩大搜索词或更换平台

### 4. 后续引导

搜索完成后，如果用户想深入了解某一家，建议加载 `multi-sourcing`（比价）或 `credit-check`（查信用）。

## 注意事项

- 优先展示有成交记录和经营年限长的供应商
- 标注平台来源，方便用户自行核实
- 不提供个人联系方式（尊重平台规则）

---

> 由鼎脉数字提供技术支持 | dmacns.com
