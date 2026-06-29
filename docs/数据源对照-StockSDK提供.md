# 数据源对照 — StockSDK 提供什么（给 STS-codex 消费方）

> 把 `docs/数据激活.md`（激活手册）里的字段链路,映射到 **StockSDK 实际端点 + 指标码**。
> STS-codex 侧 Agent 只读本表即可写出正确的 fetch adapter,**无需猜端点**。
>
> 本仓库只「提供数据」,不实现 source-priority resolver。resolver / Choice provider / SQLite
> 都在 STS-codex。本表只回答:**这个字段,StockSDK 用哪个端点 + 哪个指标码取得到?**

## 端点速查

| 端点 | 用途 | 关键参数 |
|---|---|---|
| `GET /ths/history` | iFinD 历史行情（OHLCV 等序列） | `codes, indicators(分号), begin, end, params` |
| `GET /ths/basic` | iFinD 基础/截面数据 | `codes, indicators, params` |
| `GET /ths/realtime` | iFinD 实时行情 | `codes, indicators` |
| `POST /ths/call/{func}` | iFinD 任意 `THS_*` 函数透传（如 EDB、data_pool） | body: `{args, kwargs}` |
| `GET /em/csd` | EM 序列数据 | `codes, indicators, startdate, enddate, options` |
| `GET /em/css` | EM 截面数据 | `codes, indicators, options` |
| `POST /em/call/{method}` | EM 任意 `c.*` 方法透传（如 edb） | body: `{args, options_pandas}` |
| `GET /wind/wsd` | Wind 日序列数据 | `codes, fields, startdate, enddate, options` |
| `GET /wind/wss` | Wind 日截面数据 | `codes, fields, options` |
| `POST /wind/call/{method}` | Wind 任意 `w.*` 方法透传（如 edb、wset、tdays） | body: `{args, usedf}` |

> 🔴 **Wind 只读取数**:`/wind/call/{method}` 对交易/写操作类（`tlogon/tlogout/torder/tcancel/tquery/wupf`）**硬拦截 403**;
> `wsq` 实时为异步回调,HTTP 同步端点不暴露。Wind 字段名用小写（如 `close`、`sec_name`），与 iFinD/EM 的指标码不同名,
> 三源择一即可,无需跨源拼字段。

> ⚠ **最大的坑**:OHLCV（open/high/low/close/volume/amount）**必须走 `/ths/history`**,
> 不要用 `ths_open_price_stock` 这类 `ths_*_stock` 码打 `/ths/basic`——多数账号 BasicData
> 取这些字段返回 `errorcode:0 + null`（合法指标但无该字段数据权限）。
> 实测 `/ths/history?codes=000636.SZ&indicators=open;close;volume&begin=2026-06-18&end=2026-06-19`
> → open=71.5 close=74.6 volume=136338666,codes 流通正常。

## 字段 → 端点映射

| 激活手册字段 | StockSDK 主路（iFinD） | 备路（EM/Choice） | 状态 | 备注 |
|---|---|---|---|---|
| `daily_bar`(日K/OHLCV) | `/ths/history` indicators=`open;high;low;close;volume;amount` | `/em/csd` indicators=`OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT` | ✅ 提供 | 走 history,**勿用 basic**;Wind 备路 `/wind/wsd` fields=`open,high,low,close,volume,amt` |
| `latest_quote`(最新价) | `/ths/realtime` indicators=`latest`（+`preClose,open,high,low,volume`） | `/em/css` 截面快照 | ✅ 提供 | 强实时只认实时端点,勿用日频伪装 |
| `turnover_rate`(换手率) | `/ths/realtime` 或 `/ths/history`,指标名按字段字典 | `/em/css` 换手率指标 | ⚠ 部分 | 按 `docs/catalog/ths/*_fields.csv` 确认规范名 + param |
| `market_cap`(市值/流通市值) | `/ths/basic` 基础数据服务指标 | `/em/css` 市值指标 | ⚠ 部分 | 单位统一为人民币元;按字段字典确认 |
| `stock_moneyflow`(个股资金流) | `/ths/call/{func}` moneyflow 族 | `/em/call/edb` 或对应方法 | ⚠ 部分 | 需确认账号权限;取不到标 partial/stale |
| `concept_membership`(概念/行业成员) | `/ths/call/{func}` data_pool 族 | — | ⚠ 部分 | 透传 THS data_pool 函数 |
| `sector_moneyflow`(板块资金流) | `/ths/call/{func}` sector_flow 族 | — | ⚠ 部分 | 同上,需权限确认 |
| `margin_financing`(融资净流入) | `/ths/call/{func}` margin 族 | `/em/call` 对应方法 | ⚠ 部分 | 按字段字典 |
| `etf_net_creation_inflow`(ETF申购净流入) | — | — | ❌ 不提供 | 需 PCF/申赎清单;StockSDK 当前不出,留给 STS-codex 用 Tushare 估算并标 partial |
| EDB 宏观指标 | `/ths/call/EDB` args=`["指标码","","起","止"]` | `/em/call/edb` args=`["EMM...","Ispandas=1"]` | ✅ 提供 | 通用经济指标;Wind 备路 `/wind/call/edb` args=`["指标码","起","止"]` |

图例:✅ 可直接提供 · ⚠ 能提供但需按字段字典确认指标名/权限 · ❌ 本仓库不提供

## 字段名/参数怎么查

- iFinD 指标规范名 + 各指标的 param 含义 → `docs/catalog/ths/*_fields.csv`
  （如「开盘价」的 param 是「复权方式」而非日期,搞错会取错值）。
- EM ↔ iFinD 指标对照 → `docs/catalog/EM-iFinD对照表.md`。
- 全量字段手册 → `docs/catalog/同花顺iFinD指标字段手册.md`。

## 给 STS-codex 的接入约定

- 每个字段命中要带 `source`（如 `ifind:history` / `em:css`）+ `status`（ok/stale/partial）+ `as_of`。
- 强实时字段（latest_quote）只在实时端点命中才标 ok;日频不得伪装成实时。
- 取到 `errorcode:0 + null` 不是 wiring bug,是该账号无此字段数据权限——换端点（history）或标 partial。
- StockSDK 不做源优先级裁决;哪个源主、哪个备由 STS-codex 的 resolver 决定。
