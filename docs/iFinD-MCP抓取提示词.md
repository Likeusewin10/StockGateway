# iFinD 全量指标字段抓取（MCP 反查版）—— 本地新会话提示词

> 在**本地配了 iFinD MCP（`mcp__hexin-ifind-ds-*` 工具）的电脑**上开新会话，
> 把下面【提示词】整段贴给 Claude 即可。MCP 自带鉴权，不碰网页登录，无 IP 封锁问题。

---

## 背景（为什么用这个方案）

- 目标：拿到同花顺 iFinD 各维度的指标字段（指标规范名 / 参数 / 单位），整理成给客户做产品设计用的
  Markdown 手册，并和已完成的东方财富 EM 版（18512 字段）做对照。
- iFinD 全量字典的其他路都堵死了：网页登录被 IP 风控拦、SDK 无目录函数、SDK 字典文件加密。
- **iFinD MCP 是唯一干净可行的路**：它是"自然语言问答取数"接口，每次返回数据表 + 一段
  `# 指标参数信息` JSON（含指标规范名/参数/单位）。它不直接"列出全部指标"，但靠"多维度多角度提问"
  能把每个维度的字段尽量铺满，且每次返回都自带字段元数据。

## 关键省 token 技巧（务必照做）

MCP 返回的数据表很长（一堆数值），但**我们只要 `# 指标参数信息` 那段 JSON**（字段名/参数/单位），
数据值不要。所以：
- 每次提问只用**1 个代表性证券**（如贵州茅台 600519.SH），不要批量代码，避免返回几千行。
- 解析返回时**只提取 `指标参数信息` JSON 里的字段名 + params + unit**，丢弃数据表。
- 每个维度多问几组（按下面骨架的分类逐组问），把收集到的字段去重汇总。

---

## 【提示词】（整段复制给本地 Claude）

```
我要抓取同花顺 iFinD 的指标字段字典，用你这边配的 iFinD MCP 工具（mcp__hexin-ifind-ds-* 系列）。
这是"自然语言问答取数"接口，每次返回会附一段 `# 指标参数信息` JSON，含指标规范名/参数/单位，
这就是我要的字段元数据。请按下面流程做：

【目标产出】
1. docs/catalog/ths/<维度>_fields.csv —— 每维度的字段表，列：维度, 指标规范名, 参数, 单位
2. docs/catalog/同花顺iFinD指标字段手册.md —— 按维度→指标组织的手册
3. docs/catalog/EM-iFinD对照表.md —— 和东方财富 EM 的维度对照（EM 手册在
   docs/catalog/东方财富EM指标字段手册.md，可读取参考其维度划分）

【省 token 铁律】
- 每次提问只用 1 个代表性证券，不要批量代码。
- 只从返回的 `# 指标参数信息` JSON 提取 字段名/params/unit，丢弃数据表数值。
- 每问一次就把字段并入对应维度的集合，去重（按字段名）。

【要覆盖的维度 + 用哪个 MCP 工具 + 代表证券 + 提问角度】
A 股股票（代表证券：贵州茅台 600519.SH）：
- 财务：get_stock_financials —— 分多组问：①三表(资产/负债/所有者权益/营业收入/成本/利润/现金流)
  ②盈利能力(ROE/ROA/毛利率/净利率) ③偿债(资产负债率/流动比率/速动比率) ④成长(营收/净利同比增长)
  ⑤每股指标(EPS/BPS/每股现金流) ⑥营运(周转率) ⑦杜邦分析
- 行情/技术：get_stock_performance —— 问：开高低收/成交量额/换手率/涨跌幅/MACD/KDJ/RSI/均线/布林带
- 基本资料：get_stock_info —— 问：上市日期/所属行业(申万/同花顺)/概念/公司性质/注册资本/主营
- 股本股东：get_stock_shareholders —— 问：总股本/流通股本/前十大股东/前十大流通股东/机构持股/股东户数
- 事件：get_stock_events —— 问：IPO/增发/配股/分红送转/解禁/股权激励/诉讼/股东增减持
- ESG：get_esg_data —— 问：ESG评级/各家评级机构得分
- 风险：get_risk_indicators —— 问：beta/波动率/夏普比率/最大回撤/VaR/年化收益
- 估值：get_stock_financials 或 get_stock_performance —— 问：PE/PB/PS/PCF/股息率/市值/企业价值
其他证券品种：
- 债券：bond_basic_info + bond_financial_data + bond_market_data + bond_special_data
  代表券任选一只活跃券，问：发行要素/估值(全价净价收益率久期凸性)/信用评级/转股条款
- 基金：get_fund_profile + get_fund_market_performance + get_fund_portfolio + get_fund_financials
  代表基金任选一只，问：基本资料/净值收益率/绩效(alpha/beta/夏普)/资产配置/持仓/费率
- 指数板块：index_data + sector_data 代表：沪深300 000300.SH，问：点位/估值(PE/PB/股息率)/成分
- 港美股：global_stock_profile + global_stock_financial + global_stock_quotes
  代表：苹果 AAPL.O 或腾讯 00700.HK，问：基本资料/财务/行情
宏观 EDB：
- get_edb_data —— 分领域问：GDP/CPI/PPI/M0M1M2/社融/PMI/进出口/利率(LPR/SHIBOR)/汇率/工业增加值
  （这是宏观时间序列，每个领域问一组，收集指标名即可）

【执行方式】
- 一个维度一个维度做：对该维度按上面的提问角度逐组调 MCP，每次解析出字段并入集合。
- 每个维度做完，把该维度字段写一个 CSV（docs/catalog/ths/<维度>_fields.csv）。
- 全部维度做完，生成 同花顺iFinD指标字段手册.md 和 EM-iFinD对照表.md。
- 注意：MCP 是问答式，拿不到某维度"绝对全集"，目标是尽量铺满主流字段。
  如果某次返回字段和已有重复度很高，说明该维度差不多铺满了，可以收尾换下一维度。

先从"A股股票-财务"维度开始，调 get_stock_financials 问第①组(三表)，
把解析出的字段表给我看，我确认格式对了，你再继续后面所有维度。
```

---

## 备注

- 本地 Claude 若发现某些 MCP 工具名和上面不完全一致，以它实际可用的 `mcp__hexin-ifind-ds-*`
  工具为准（按"股票/债券/基金/指数/宏观/港美股"语义对应即可）。
- EM 手册（`docs/catalog/东方财富EM指标字段手册.md`）若本地没有，可不依赖它，先单独产出 iFinD 手册，
  对照表后续再补。
- 抓完提交一个 commit：`feat: iFinD 指标字段字典与手册（MCP 反查）`。
