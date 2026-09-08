---
name: 1088-search
description: Use when the user wants to search products on the DMACNS P2P network via their local 1088 node. Returns structured product listings with prices, suppliers, and credit ratings.
version: 1.0.0
author: 鼎脉数字 (DMACNS)
license: MIT
metadata:
  hermes:
    tags: [dmacns, 1088, search, discovery]
    related_skills: [1088-setup, 1088-order]
---

# 1088 Search — 搜索商品

## Overview

教 Agent 通过本地 1088.exe 搜索 P2P 网络上的商品，返回结构化结果（商品名、价格、供应商、信用评级）。

## When to Use

- 用户说"帮我搜XX商品"、"找XX货源"、"有什么XX卖"
- 用户想比价——多次搜索不同关键词
- 用户想了解某个品类的供应商情况

## Prerequisites

- 已通过 `1088-setup` 登录，`~/.dmacns/cookie.txt` 已保存
- `1088-setup` Skill 已加载

## How to Run

### 核心命令（复制即用）

将以下 Python 脚本写入临时文件后执行（中文参数用 Python，不用 curl）：

```python
import json, urllib.request, http.cookiejar, os

BASE = "http://localhost:18088"
COOKIE_FILE = os.path.expanduser("~/.dmacns/cookie.txt")

cj = http.cookiejar.MozillaCookieJar()
cj.load(COOKIE_FILE, ignore_discard=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def api(method, path, data=None):
    url = BASE + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    resp = opener.open(req)
    return json.loads(resp.read().decode())

# 搜索商品
QUERY = "苹果"   # ← 替换为用户的搜索词
r = api("POST", "/api/market", {"query": QUERY})
results = r.get("results") or []

print(f"搜索 '{QUERY}': {len(results)} 条结果\n")
for item in results:
    print(f"  {item.get('name')}")
    print(f"    价格: ¥{item.get('price')} | 起订: {item.get('min_order',0)} | 库存: {item.get('stock',0)}")
    print(f"    供应商: {item.get('supplier_name','?')}")
    print(f"    信用: {item.get('credit_level','?')} | 评分: {item.get('score','?')}")
    print(f"    SKU: {item.get('sku')} | 卖家DID: {item.get('seller_did','?')}")
    print()
```

### 搜索结果字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 商品名称 | 烟台红富士苹果 |
| `price` | 单价（元） | 5.5 |
| `min_order` | 最低起订量 | 10 |
| `stock` | 库存数量 | 1000 |
| `supplier_name` | 供应商名称 | 烟台苹果贸易 |
| `credit_level` | 信用等级 | LV5 |
| `score` | 综合评分 | 4.8 |
| `sku` | 商品编码（下单时用） | bf167478 |
| `seller_did` | 卖家 DID（下单时用） | did:user:a_sale |

### 无结果时

如果搜索返回 0 条，告知用户：
1. 可能是关键词太具体——建议用更宽泛的词（如"苹果"而非"烟台红富士苹果"）
2. 可能是 P2P 网络上暂无此品类——建议让卖家先用 1088 Web 控制台上架商品

## Common Pitfalls

1. **中文关键词用 curl 会乱码** — 必须用 Python。如果必须用 curl，走 `cmd.exe /c curl` 绕过 MSYS。
2. **SKU 和 seller_did 是下单的关键参数** — 搜索结果中必须记录这两个字段，下单时需要。
3. **搜索范围** — `POST /api/market` 搜索的是 P2P 全球网络（通过 Seed 发现），不只是本地数据库。
4. **空结果不等于没商品** — 可能 P2P 节点暂时不可达。可以隔几秒重试。

## Verification Checklist

- [ ] 登录态有效（cookie 未过期）
- [ ] 搜索返回了结构化结果（含 sku/seller_did/price）
- [ ] 中文关键词正常搜索（无乱码）
- [ ] 记录了至少一个商品的 sku 和 seller_did 供下单使用
