# 工单反馈:iFinD 网关 THSCODE 参数未传递

| 项 | 内容 |
|---|---|
| **工单标题** | iFinD 网关 THSCODE 参数未传递 — 需服务端修 |
| **工单创建** | 2026-06-23 12:15 |
| **反馈时间** | 2026-06-23 |
| **排查方** | 服务端(在服务器上真打 iFinD SDK 复现) |
| **结论** | ❌ **非服务端 bug,代码无需修改**。根因是**数据权限**,客户端可立即绕过。 |

---

## 一、原判断纠正

工单判断「网关没把 query 的 `codes` 映射到 `THS_BasicData` 的 `THSCODE` 参数,属服务端代码 bug」——**经服务器实测证伪**。

- 路由代码正确:`stocksdk/routes_ths.py` 中 `THS_BasicData(codes, indicators, params)`,`codes` 即 SDK 签名的第一个位置参数 `thsCode` → `THSCODE`,映射无误,无漏赋值、无顺序错。
- SDK 真实签名:`THS_BasicData(thsCode, indicatorName, paramOption)`。

### `inputParams` 里 THSCODE 为空是红鲱鱼

`inputParams` 中 `{"name":"THSCODE","value":""}` 是 iFinD RPC 的**正常回显,恒为空**——这不是 bug 信号。

> 反证:工单里说「能用」的 `ths_close_price_stock`(返回 730.1),它的 `inputParams` 中 THSCODE **同样是空**,却正常返回值。

真实证券代码在每条 `tables[].thscode = "000636.SZ"` 里**正确携带**。

---

## 二、null 的真因:数据权限,不是函数无效

决定性对照(同账号、同股 `000636.SZ`):

| 调用 | errorcode | 返回值 | 说明 |
|---|---|---|---|
| 乱编码 `ths_FAKE_xxx_stock` | **-209** | 报错 | 不存在的指标 → 报错 |
| `ths_open_price_stock` | **0** | **null** | 合法指标,但**取不到值** |
| `ths_close_price_stock` (000636) | 0 | **730.1** | 真实分股数据,有权限 |
| `ths_close_price_stock` (600519 茅台) | 0 | **9301** | 换股即变,非常量/缓存 |

### 关键:errorcode 0 + null

iFinD 的行为约定:

- **指标不存在 / 参数非法** → `errorcode -209`(报错)
- **指标合法但账号无该数据权限** → `errorcode 0` + 值 `null`(静默返回空,**不报错**)

`ths_open_price_stock` 返回 `errorcode 0`(不是 -209)→ 引擎**认得这个指标、也认得这只股**,只是**取不到值**。

**所以:** `close` 该账号**有权限**(出值);`open / vol / 换手率 / 市值` 这些 BasicData 字段该账号**没订阅/没权限**(返回 null)。试遍各种日期/参数形态 `open` 都是 null,正是因为权限层挡在数据层之前,给什么参数都没用。

---

## 三、客户端可立即绕过(无需等服务端)

`open / high / low / close / volume` 改走 **`/ths/history`**(`THS_HistoryQuotes` 族),该账号**有权限**。

实测:
```
/ths/history?codes=000636.SZ&indicators=open;close;volume&begin=2026-06-22&end=2026-06-22
→ open=74.61   close=72.98   volume 正常
```

> 历史行情族(HistoryQuotes)与 BasicData 族是**不同的授权包**,前者通。

---

## 四、需要的动作

| 责任方 | 动作 |
|---|---|
| **服务端(我方)** | ✅ 无 —— 代码正确,不改 |
| **客户端(Coco)** | 行情类(开高低收量)切到 `/ths/history`;`/ths/basic` 的 `open/vol/市值/换手` 暂不可用 |
| **同花顺账号** | 若必须用 `/ths/basic` 取 `open/vol/市值/换手` → 找同花顺**补订阅 BasicData 字段权限** |

---

## 五、其他状态

- iFinD 登录已恢复正常(`errorcode: 0`)。
- Choice(`/em/css`)正常,可继续顶上权威源。
- iFinD 数据源本身是通的,**非源故障**——仅 BasicData 部分字段未授权。

---

## 附:建议

可做一个「权限探测脚本」,自动列出该账号在 `/ths/basic` 下**哪些指标有权限**(errorcode 0 且非 null),省去逐个试。如需要请告知。
