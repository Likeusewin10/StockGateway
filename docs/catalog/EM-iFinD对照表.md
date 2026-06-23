# EM (东方财富/Choice) ↔ iFinD (同花顺) 指标维度对照表

> 本表对照两套数据源的**维度组织方式**与**覆盖能力**,便于在两个 SDK 间迁移取数逻辑。
>
> - **EM 手册**:`docs/catalog/东方财富EM指标字段手册.md`(按 CSS 截面 / CSD 序列 / CTR 报表三大接口组织,5400+ 指标)
> - **iFinD 手册**:`docs/catalog/同花顺iFinD指标字段手册.md`(按业务维度组织,502 字段)
> - 字段表:`docs/catalog/em/*.csv` 与 `docs/catalog/ths/*_fields.csv`

## 一、接口模型差异(根本区别)

| 维度 | EM / Choice | iFinD MCP |
|---|---|---|
| 取数方式 | 指标代码 + 参数,程序化批量 | 自然语言问答,单证券逐问 |
| 字段标识 | 有**指标代码**(如 `CLOSE`/`OPEN`/`ROEAVG`) | 仅**中文规范名**(问答接口不暴露代码) |
| 接口拆分 | CSS(截面)/CSD(序列)/CTR(报表)三类函数 | 按业务维度的多个 MCP 工具 |
| 字段全集 | 可枚举(指标体系固定) | 不可枚举(问答式,只能铺主流) |
| 宏观数据 | EDB(独立指标库,带 index_id) | `get_edb_data`(带 index_id,与 EM 对齐) |

> **迁移要点**:EM 用指标代码定位字段,iFinD 用中文名问答。两者字段**语义高度重叠**,但 iFinD 无法像 EM 那样穷举字段,且单次只能查一只证券。

## 二、维度级对照

### A股股票

| 业务维度 | EM 对应分类(CSS/CTR) | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 基本资料 | CSS 证券资料 / 行业分类 | `get_stock_info` / 16 | iFinD 偏精简,EM 含专利/违规等长尾 |
| 财务三表+分析 | CTR 资产负债表/利润表/现金流量表 + CSS 财务分析 | `get_stock_financials` / 86 | 双方均覆盖三表与衍生比率;EM 报表字段更细 |
| 行情/技术 | CSD 日/周/月/年行情 + 技术指标 | `get_stock_performance` / 38 | iFinD 技术指标用"指标选项"参数复用;EM 用独立代码 |
| 股本股东 | CSS 报告期股东指标/机构持股/股东户数 | `get_stock_shareholders` / 24 | 双方均覆盖前十大股东、机构持股、户数 |
| 事件 | CSS 限售解禁/股本变动/增减持 + CTR 分红 | `get_stock_events` / 26 | 覆盖 IPO/分红/解禁/增减持 |
| ESG | CSS ESG 评级类 | `get_esg_data` / 8 | iFinD 多家评级机构(华证/中诚信/商道融绿/秩鼎) |
| 风险/定量 | CSS 标准参数指标/自定义参数指标 | `get_risk_indicators` / 17 | beta/夏普/波动率/VaR/最大回撤,参数化区间 |
| 估值 | CSS 预测估值/企业价值/估值百分位 | 并入 `get_stock_financials`/`get_stock_performance` | PE/PB/PS/股息率/市值;EM 估值百分位更系统 |

### 债券

| 业务维度 | EM 对应 | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 发行要素 | CSS 债券-证券资料 | `bond_basic_info` / 26 | 发行人/期限/票面/评级/付息 |
| 估值与行情 | CSD 债券行情 + CSS 债券估值 | `bond_market_data` / 33 | 全价净价/YTM/久期/凸性/多源利差 |
| 发行人财务 | CTR(发行人财报) | `bond_financial_data` / 15 | 发行人财务穿透 |
| 可转债条款 | CSS 可转债专项 | `bond_special_data` / 21 | 转股价/溢价率/赎回回售条款全文 |

### 基金

| 业务维度 | EM 对应 | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 基本资料+费率+经理 | CSS 基金资料 | `get_fund_profile` / 32 | 含基金经理任职/费率分档 |
| 净值收益 | CSD 基金净值序列 | `get_fund_market_performance` / 5 | iFinD 绩效类(夏普/回撤)对场外基金部分返空 |
| 资产配置+持仓 | CSS 基金持仓/资产配置 | `get_fund_portfolio` / 35 | 大类资产占比 + 前十大重仓股 |

### 指数与板块

| 业务维度 | EM 对应 | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 指数行情估值 | CSD 指数行情 + CSS 指数估值 | `index_data` / 18 | 点位/PE/PB/股息率/成分数 |
| 板块统计 | CSS 板块汇总(`sector_seeds.csv`) | `sector_data` / 8 | 板块涨跌/市值/PE,加权口径多样 |

### 港美股

| 业务维度 | EM 对应 | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 基本资料 | CSS 港美股资料 | `global_stock_profile` / 27 | 含营收按业务构成(前5) |
| 财务+盈利预测 | CTR 港美股报表 + CSS 盈利预测 | `global_stock_financial` / 36(预测类归并) | iFinD 盈利预测统计值用"统计口径"参数归并 |
| 行情风险 | CSD 港美股行情 | `global_stock_quotes` / 22 | 量价 + beta/波动率(多周期) |

### 宏观经济

| 业务维度 | EM 对应 | iFinD 对应(工具 / 字段数) | 覆盖对照 |
|---|---|---|---|
| 宏观时序 | EDB 指标库(带 index_id) | `get_edb_data` / 11 | **两者 index_id 体系一致**(如 M002826730=CPI同比),可直接互换 |

## 三、迁移建议

1. **字段映射**:按中文规范名做 EM↔iFinD 映射;EM 侧用 `em/css_indicators.csv`(含指标代码),iFinD 侧用 `ths/*_fields.csv`(中文名),按语义对齐。
2. **宏观数据**:两侧 `index_id` 一致,EDB 维度可无损互换,无需重新映射。
3. **批量 vs 单查**:EM 支持多证券批量;iFinD MCP 单次一只证券,批量场景需循环调用。
4. **长尾字段**:EM 在专利/违规/质押/调研/盈利预测明细等长尾维度更全;iFinD 覆盖主流交易/财务/估值字段,长尾需逐次问答补充。
5. **技术指标**:EM 每个分量独立代码;iFinD 同一指标用"指标选项/周期"参数切换分量——迁移时注意参数映射。
