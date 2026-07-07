# 通达信 TDX(TdxQuant)字段手册

> **合法来源**:官方随终端附带的《TdxQuant接口说明文档》(231页 PDF),
> 用 PyMuPDF `find_tables()` 结构化抽取,**非爬取、非指标树遍历**(零封控风险)。
> 生成脚本:`scripts/catalog/extract_tdx.py` + `gen_md_tdx.py`;原始 PDF 见 `docs/catalog/tdx/_raw/`。

- 覆盖接口:**49** 个  字段/参数行:**1115** 条
- `kind=PARAM` 为入参,`kind=RETURN` 为返回字段/常量
- **代码格式** `600519.SH`,**日期** `YYYYMMDD`(与 EM/iFinD/Wind 的 `YYYY-MM-DD` 不同)
- 财务/经济类(FN/SC 指标)需先在客户端**下载对应数据包**才能取数

---

## 目录

- [`get_market_data`](#getmarketdata) K线行情 — 18 项
- [`get_market_snapshot`](#getmarketsnapshot) 行情快照 — 27 项
- [`get_stock_info`](#getstockinfo) 股票基础信息 — 64 项
- [`get_more_info`](#getmoreinfo) 更多股票信息 — 89 项
- [`get_pricevol`](#getpricevol) 量价数据 — 4 项
- [`get_divid_factors`](#getdividfactors) 除权因子 — 8 项
- [`get_relation`](#getrelation) 关联品种 — 5 项
- [`get_ipo_info`](#getipoinfo) 新股IPO信息 — 9 项
- [`get_gb_info`](#getgbinfo) 股本信息 — 6 项
- [`get_gb_info_by_date`](#getgbinfobydate) 指定日期股本 — 6 项
- [`get_match_stkinfo`](#getmatchstkinfo) 证券信息检索 — 3 项
- [`get_report_data`](#getreportdata) 行情订阅推送 — 3 项
- [`get_trading_dates`](#gettradingdates) 交易日历 — 9 项
- [`get_trackzs_etf_info`](#gettrackzsetfinfo) 跟踪指数ETF — 8 项
- [`get_kzz_info`](#getkzzinfo) 可转债信息 — 27 项
- [`get_financial_data`](#getfinancialdata) 专业财务数据(FN指标) — 445 项
- [`get_financial_data_by_date`](#getfinancialdatabydate) 指定日期财务 — 4 项
- [`get_gp_one_data`](#getgponedata) 股票单个财务数据 — 49 项
- [`get_gpjy_value`](#getgpjyvalue) 股票经济指标 — 50 项
- [`get_gpjy_value_by_date`](#getgpjyvaluebydate) 指定日期股票经济指标 — 4 项
- [`get_bkjy_value`](#getbkjyvalue) 板块经济指标 — 19 项
- [`get_bkjy_value_by_date`](#getbkjyvaluebydate) 指定日期板块经济指标 — 4 项
- [`get_scjy_value`](#getscjyvalue) 市场经济指标(SC指标) — 45 项
- [`get_scjy_value_by_date`](#getscjyvaluebydate) 指定日期市场经济指标 — 3 项
- [`get_stock_list`](#getstocklist) 股票列表 — 2 项
- [`get_sector_list`](#getsectorlist) 板块列表 — 1 项
- [`get_stock_list_in_sector`](#getstocklistinsector) 板块成分股 — 3 项
- [`send_user_block`](#senduserblock) 自选/板块写入 — 9 项
- [`stock_account`](#stockaccount) 获取资金账户句柄 — 2 项
- [`query_stock_asset`](#querystockasset) 查询账户资产 — 12 项
- [`query_stock_orders`](#querystockorders) 查询委托 — 15 项
- [`query_stock_positions`](#querystockpositions) 查询持仓 — 13 项
- [`order_stock`](#orderstock) 下单 — 10 项
- [`cancel_order_stock`](#cancelorderstock) 撤单 — 5 项
- [`send_message`](#sendmessage) 发送消息 — 1 项
- [`send_warn`](#sendwarn) 发送预警 — 9 项
- [`send_file`](#sendfile) 发送文件 — 1 项
- [`send_bt_data`](#sendbtdata) 回测数据 — 7 项
- [`refresh_cache`](#refreshcache) 刷新缓存 — 2 项
- [`refresh_kline`](#refreshkline) 刷新K线 — 2 项
- [`exec_to_tdx`](#exectotdx) 执行到客户端 — 1 项
- [`formula_get_all`](#formulagetall) 公式列表 — 4 项
- [`formula_get_info`](#formulagetinfo) 公式信息 — 14 项
- [`formula_format_data`](#formulaformatdata) 公式格式化 — 1 项
- [`formula_set_data`](#formulasetdata) 公式写数据 — 5 项
- [`formula_set_data_info`](#formulasetdatainfo) 公式数据信息 — 6 项
- [`formula_zb`](#formulazb) 公式指标 — 3 项
- [`formula_process_mul_zb`](#formulaprocessmulzb) 批量指标计算 — 11 项
- [`常量枚举`](#常量枚举) 常量枚举(市场/交易/委托状态) — 67 项


## <a id="getmarketdata"></a>`get_market_data` K线行情

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `field_list` | N | List[str] | 字段筛选，传空则返回全部 |
| `stock_list` | Y | List[str] | 证券代码列表 |
| `period` | Y | str | 周期 |
| `start_time` | N | str | 起始时间 |
| `end_time` | N | str | 结束时间 |
| `count` | N | int | 返回数据个数（每只股票） |
| `dividend_type` | N | str | 复权类型 ：none不复权、front 前复权、back后复权 |
| `fill_data` | N | bool | 是否向后填充空缺数据 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Date` | Y | str | 日期 |
| `Time` | Y | str | 时间 |
| `Open` | Y | str | 开盘价 |
| `High` | Y | str | 最高价 |
| `Low` | Y | str | 最低价 |
| `Close` | Y | str | 收盘价 |
| `Volume` | Y | str | 成交量 |
| `Amount` | Y | str | 成交额 |
| `ForwardFactor` | Y | str | 前复权因子，当 dividend type=none时候返回有 _ 效值 |
| `VolInStock` | N | str | 持仓量 |


## <a id="getmarketsnapshot"></a>`get_market_snapshot` 行情快照

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 证券代码 |
| `field_list` | N | List[str] | 字段筛选，传空则返回全部 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `ItemNum` | Y | str | 快照笔数 |
| `LastClose` | Y | str | 前收盘价 |
| `Open` | Y | str | 开盘价 |
| `Max` | Y | str | 最高价 |
| `Min` | Y | str | 最低价 |
| `Now` | Y | str | 现价 |
| `Volume` | Y | str | 总手 |
| `NowVol` | Y | str | 现手 |
| `Amount` | Y | str | 总成交金额 |
| `Inside` | Y | str | 内盘 板块指数时为跌停家数 |
| `Outside` | Y | str | 外盘 板块指数时为涨停家数 |
| `TickDiff` | Y | str | 笔涨跌 |
| `InOutFlag` | Y | str | 内外盘标志 0:Buy 1:Sell 2:Unknown |
| `Jjjz` | Y | str | 基金净值 |
| `Buyp` | Y | List[str] | 五个买价 |
| `Buyv` | Y | List[str] | 对应的五个买盘量 |
| `Sellp` | Y | List[str] | 五个卖价 |
| `Sellv` | Y | List[str] | 对应的五个卖盘量 |
| `UpHome` | Y | str | 上涨家数 对于指数有效 |
| `DownHome` | Y | str | 下跌家数 对于指数有效 |
| `Before5MinNow` | Y | str | 5分钟前价格 |
| `Average` | Y | str | 均价 |
| `XsFlag` | Y | str | 小数位数 |
| `Zangsu` | Y | str | 涨速 |
| `ZAFPre3` | Y | str | 3日涨幅 |


## <a id="getstockinfo"></a>`get_stock_info` 股票基础信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 证券代码 |
| `field_list` | Y | List[str] | 字段筛选，不能为空 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Name` | Y | str | 证券名称 |
| `Unit` | Y | str | 交易单位 |
| `VolBase` | Y | str | 量比的基量 |
| `MinPrice` | Y | str | 最小价格变动 |
| `XsFlag` | Y | str | 价格小数位数 |
| `Fz[8]` | Y | List[str] | 开收市时间（4段） |
| `DelayMin` | Y | str | 延时分钟数 |
| `QHVolBaseRate` | Y | str | 期货期权的每手乘数 |
| `HKVolBaseRate` | Y | str | 港股/日股/新加坡股 每手股数 |
| `BelongHS300` | Y | str | 是否属于沪深300 |
| `BelongHasKQZ` | Y | str | 是否含可转债 |
| `BelongRZRQ` | Y | str | 是否是融资融券标的 |
| `BelongHSGT` | Y | str | 是否属于沪深股通 |
| `IsHKGP` | Y | str | 是否是港股 |
| `IsQH` | Y | str | 是否是期货 |
| `IsQQ` | Y | str | 是否是期权 |
| `IsSTGP` | Y | str | 是否是ST股票 |
| `IsQuitGP` | Y | str | 是否是退市整理板股票 |
| `TodayDRFlag` | Y | str | 当天是否有除权除息(沪深京) |
| `HSStockKind` | Y | str | 沪深京品种类型 0:指数,1:A股主 板,2:北证A股,3:创业板,4:科创 板,5:B股,6:债券,7:基金,8:权证,9:其 它,10:非沪深京品种 |
| `ActiveCapital` | Y | str | 流通股本(万股) |
| `J_zgb` | Y | str | 总股本(万股) |
| `J_bg` | Y | str | B股(万股) |
| `J_hg` | Y | str | H股(万股) |
| `J_zzc` | Y | str | 总资产(万元) |
| `J_ldzc` | Y | str | 流动资产(万元) |
| `J_gdzc` | Y | str | 固定资产(万元) |
| `J_wxzc` | Y | str | 无形资产(万元) |
| `J_ldfz` | Y | str | 流动负债(万元) |
| `J_cqfz` | Y | str | 少数股东权益(万元) |
| `J_zbgjj` | Y | str | 资本公积金(万元) |
| `J_jzc` | Y | str | 股东权益/净资产(万元) |
| `J_yysy` | Y | str | 营业收入(万元) |
| `J_yycb` | Y | str | 营业成本(万元) |
| `J_yszk` | Y | str | 应收账款(万元) |
| `J_yyly` | Y | str | 营业利润(万元) |
| `J_tzsy` | Y | str | 投资收益(万元) |
| `J_jyxjl` | Y | str | 经营现金净流量(万元) |
| `J_zxjl` | Y | str | 总现金净流量(万元) |
| `J_ch` | Y | str | 存货(万元) |
| `J_lyze` | Y | str | 利润总额(万元) |
| `J_shly` | Y | str | 税后利润(万元) |
| `J_jly` | Y | str | 净利润(万元) |
| `J_wfply` | Y | str | 未分配利益(万元) |
| `J_jyl` | Y | str | 净资产收益率 |
| `J_mgwfp` | Y | str | 每股未分配 |
| `J_mgsy` | Y | str | 每股收益（折算为全年） |
| `J_mgsy2` | Y | str | 季报每股收益 (财报中提供的每股 收益) |
| `J_mggjj` | Y | str | 每股公积金 |
| `J_mgjzc` | Y | str | 每股净资产 |
| `J_mgjzc2` | Y | str | 季报每股净资产 (财报中提供的每 股收益) |
| `J_gdqyb` | Y | str | 股东权益比 |
| `J_gdrs` | Y | str | 股东人数 |
| `J_HalfYearFlag` | Y | str | 报告期月份(3,6,9,12) |
| `J_start` | Y | str | 上市日期 |
| `tdx_dycode` | Y | str | 通达信地域代码 |
| `tdx_dyname` | Y | str | 通达信地域 |
| `rs_hycode_sim` | Y | str | 通达信行业代码 |
| `rs_hyname` | Y | str | 通达信行业 |
| `blockzscode` | Y | str | 所属的行业板块指数代码 |
| `underly_setcode` | Y | str | 标的市场代码(比如：当前ETF跟踪 的指数市场) |
| `underly_code` | Y | str | 标的代码(比如：当前ETF跟踪的指 数代码) |


## <a id="getmoreinfo"></a>`get_more_info` 更多股票信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |
| `field_list` | N | List[str] | 字段筛选，传空则返回全部 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `MainBusiness` | Y | str | 主营构成 |
| `SafeValue` | Y | str | 安全分 |
| `ShineValue` | Y | str | 亮点数 |
| `ShapeValue` | Y | str | 短期形态+中期形态+长期形态 编 号 |
| `TPFlag` | Y | str | 停牌标识 |
| `ZTPrice` | Y | str | 涨停价 |
| `DTPrice` | Y | str | 跌停价 |
| `HqDate` | Y | str | 行情日期 |
| `fHSL` | Y | str | 换手率 |
| `fLianB` | Y | str | 量比 |
| `Wtb` | Y | str | 委比 |
| `Zsz` | Y | str | 总市值(亿) |
| `Ltsz` | Y | str | 流通市值(亿) |
| `vzangsu` | Y | str | 量涨速 |
| `Fzhsl` | Y | str | 分钟换手率 |
| `FzAmo` | Y | str | 2分钟金额(万元) |
| `VOpenZAF` | Y | str | 抢筹涨幅 |
| `ZAF` | Y | str | 涨幅 |
| `ZAFYesterday` | Y | str | 昨日涨幅 |
| `ZAFPre2D` | Y | str | 前天涨幅 |
| `ZAFPre5` | Y | str | 5日涨幅 |
| `ZAFPre10` | Y | str | 10日涨幅 |
| `ZAFPre20` | Y | str | 20日涨幅 |
| `ZAFPre30` | Y | str | 30日涨幅 |
| `ZAFPre60` | Y | str | 60日涨幅 |
| `ZAFYear` | Y | str | 年初至今涨幅 |
| `ZAFPreMyMonth` | Y | str | 涨幅(本月来) |
| `ZAFPreOneYear` | Y | str | 涨幅(一年来) |
| `Zjl` | Y | str | 主买净额(万元) |
| `Zjl_HB` | Y | str | 主力净流入(万元) |
| `TotalBVol` | Y | str | 总买量 |
| `TotalSVol` | Y | str | 总卖量 |
| `BCancel` | Y | str | 总撤买量 |
| `SCancel` | Y | str | 总撤卖量 |
| `L2TicNum` | Y | str | L2逐笔成交数 |
| `L2OrderNum` | Y | str | L2逐笔委托数 |
| `FCAmo` | Y | str | 封单额(万元) |
| `FCb` | Y | str | 封成比 |
| `OpenAmo` | Y | str | 开盘金额(万元)(A股和板块指数有 效) |
| `OpenZTBuy` | Y | str | 竞价涨停买入金额(万元) |
| `OpenAmoPre1` | Y | str | 昨开盘金额(万元) |
| `OpenVolPre1` | Y | str | 昨开盘量 |
| `CJJEPre1` | Y | str | 昨成交额(万元) |
| `CJJEPre3` | Y | str | 3日成交额(万元) |
| `FDEPre1` | Y | str | 昨封单额(万元) |
| `FDEPre2` | Y | str | 前封单额(万元) |
| `ZTGPNum` | Y | str | 板块指数的涨停家数 |
| `LastStartZT` | Y | str | 几天 |
| `LastZTHzNum` | Y | str | 几板 |
| `EverZTCount` | Y | str | 连板天 |
| `ConZAFDateNum` | Y | str | 连涨天数 |
| `YearZTDay` | Y | str | 年涨停天数 |
| `MA5Value` | Y | str | 5日均价 |
| `HisHigh` | Y | str | 52周最高 |
| `HisLow` | Y | str | 52周最低 |
| `IPO_Price` | Y | str | 发行价 |
| `More_YJL` | Y | str | ETF,LOF溢价率 |
| `BetaValue` | Y | str | 贝塔系数 |
| `DynaPE` | Y | str | 动态市盈率 |
| `MorePE` | Y | str | 市盈率(港股:动,其他扩展:静) |
| `StaticPE_TTM` | Y | str | 市盈率(TTM) |
| `DYRatio` | Y | str | 股息率 |
| `PB_MRQ` | Y | str | 市净率(MRQ) |
| `IsT0Fund` | Y | str | 是否是T+0基金 |
| `IsZCZGP` | Y | str | 是否是注册制A股 |
| `IsKzz` | Y | str | 是否是可转债 |
| `Kzz_HSCode` | Y | str | 可转债对应的正股代码 |
| `QHMainYYMM` | Y | str | 主力合约关联的月份(期货),主力和 次主力 |
| `FreeLtgb` | Y | str | 自由流通股本(万) |
| `Yield` | Y | str | 应计利息(债券),占款天数(回购) |
| `KfEarnMoney` | Y | str | 扣非净利润(万元) |
| `RDInputFee` | Y | str | 研发费用(万元) |
| `CashZJ` | Y | str | 货币资金(万元) |
| `PreReceiveZJ` | Y | str | 合同负债(万元) |
| `OtherQYJzc` | Y | str | 其它权益工具(万元) |
| `StaffNum` | Y | str | 员工人数 |
| `RecentGGJYDate` | Y | str | 最近北上大额交易日 |
| `RecentHGDate` | Y | str | 最近回购预案日 |
| `RecentIncentDate` | Y | str | 最近股权激励预案日 |
| `NoticeDate_Recent` | Y | str | 最近业绩预告日 |
| `RecentReleaseDate` | Y | str | 最近解禁日 |
| `RecentDZDate` | Y | str | 最近定增日 |
| `ReportDate` | Y | str | 最近财报公告日期 |
| `ZTDate_Recent` | Y | str | 近2年最近涨停板日期 |
| `DTDate_Recent` | Y | str | 近2年最近跌停板日期 |
| `TopDate_Recent` | Y | str | 近2年最近龙虎榜日期 |
| `StopJYDate_Recent` | Y | str | 最近停牌日期 |


## <a id="getpricevol"></a>`get_pricevol` 量价数据

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `LastClose` | Y | str | 前收盘价 |
| `Now` | Y | str | 现价 |
| `Volume` | Y | str | 成交量 |


## <a id="getdividfactors"></a>`get_divid_factors` 除权因子

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 证券代码 |
| `start_time` | N | str | 起始时间 |
| `end_time` | N | str | 结束时间 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Type` | Y | str | 类型 1:除权除息 11:扩缩股 15:重 新调整 |
| `Bonus` | Y | str | 红利 |
| `AlloPrice` | Y | str | 配股价 |
| `ShareBonus` | Y | str | 送股/扩缩股比例 |
| `Allotment` | Y | str | 配股 |


## <a id="getrelation"></a>`get_relation` 关联品种

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `BlockCode` | Y | str | 板块代码 |
| `BlockName` | Y | str | 板块名称 |
| `BlockType` | Y | str | 板块类型 |
| `GPNume` | Y | str | 成份股数量 |


## <a id="getipoinfo"></a>`get_ipo_info` 新股IPO信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `ipo_type` | Y | str | 自定义板块简称 |
| `ipo_date` | Y | int | 自定义板块名称 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Code` | Y | str | 证券代码 |
| `Name` | Y | str | 证券名称 |
| `SGDate` | Y | str | 申购日期 |
| `SGPrice` | Y | str | 申购价格 |
| `SGCode` | Y | str | 申购代码 |
| `MaxSG` | Y | str | 申购上限 |
| `PE_Issue` | Y | str | 发行市盈率 |


## <a id="getgbinfo"></a>`get_gb_info` 股本信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |
| `date_list` | Y | List[str] | 日期数组 |
| `count` | Y | int | 日期有效个数 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `Date` | double | 日期 |
| `Zgb` | double | 总股本 |
| `Ltgb` | double | 流通股本 |


## <a id="getgbinfobydate"></a>`get_gb_info_by_date` 指定日期股本

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |
| `start_date` | Y | str | 开始日期 |
| `end_date` | Y | str | 截止日期 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `Date` | double | 日期 |
| `Zgb` | double | 总股本 |
| `Ltgb` | double | 流通股本 |


## <a id="getmatchstkinfo"></a>`get_match_stkinfo` 证券信息检索

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `key_word` | Y | str | 关键词 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Code` | Y | str | 证券代码 |
| `Name` | Y | str | 证券名称 |


## <a id="getreportdata"></a>`get_report_data` 行情订阅推送

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 订阅的证券代码 |
| `callback` | Y | str | 回调函数 |
| `stock_list` | Y | List[str] | 证券代码 |


## <a id="gettradingdates"></a>`get_trading_dates` 交易日历

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `market` | Y | str | 市场代码（暂固定为SH） |
| `start_time` | N | str | 起始日期 |
| `end_time` | N | str | 结束日期 |
| `count` | N | int | 返回最近的count个交易日 |
| `df_list` | Y | list[pd.DataFrame] | 多组数据的DataF 表，每组table对应 DataFrame；每个 DataFrame非空且 日期（datetime64 符串类型），后续列 因子名称；列表长 组数 |
| `sp_name` | N | str | 生成.sp文件的名称 空时默认生成pyth |
| `xml_filename` | N | str | 生成的xml文件名 含.xml后缀），为空 达信面板配置关联 填 |
| `jsn_filenames` | Y | list[str] | 每组数据对应的.js 表，列表非空且长 组数（与df list一 _ 名建议包含.jsn后缀 |
| `vertical` | N | int | 纵向排列的table组 （≥1），与horizo 一，horizontal优先 |


## <a id="gettrackzsetfinfo"></a>`get_trackzs_etf_info` 跟踪指数ETF

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `zs_code` | Y | str | 指数代码 |

**返回字段**

| 字段 | 类型 | 取值 | 说明 |
|---|---|---|---|
| `Code` | str | 证券代码 |  |
| `Name` | str | 证券名称 |  |
| `NowPrice` | str | 现价 |  |
| `PreClose` | str | 昨收 |  |
| `IOPV` | str | 净值 |  |
| `Zgb` | str | 净额（万份） |  |
| `Sz` | str | 规模（亿元） |  |


## <a id="getkzzinfo"></a>`get_kzz_info` 可转债信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 可转债代码 |
| `field_list` | N | List[str] | 字段筛选，传空则返回全部 |

**返回字段**

| 字段 | 类型 | 取值 | 说明 |
|---|---|---|---|
| `SetCode` | str | 证券市场 |  |
| `KZZCode` | str | 可转债代码 |  |
| `HSCode` | str | 正股代码 |  |
| `ZGPrice` | str | 转股价格 |  |
| `CurRate` | str | 当期利率 |  |
| `RestScope` | str | 剩余规模(万) |  |
| `PutBack` | str | 回售触发价 |  |
| `ForceRedeem` | str | 强赎触发价 |  |
| `ZGDate` | str | 转股日 |  |
| `EndPrice` | str | 到期价 |  |
| `EndDate` | str | 到期日期 |  |
| `ZGRate` | str | 转股比率% |  |
| `RealValue` | str | 纯债价值 |  |
| `ExpireYield` | str | 到期收益率% |  |
| `KZZScore` | str | 可转债评级 |  |
| `HSScore` | str | 主体评级 |  |
| `RedeemDate` | str | 赎回登记日期 |  |
| `RedeemPrice` | str | 赎回价格 |  |
| `PutDate` | str | 回售申报起始日期 |  |
| `PutPrice` | str | 回售价格 |  |
| `ZGCode` | str | 转股代码 |  |
| `AGPrice` | str | 正股当前价格 |  |
| `KZZPrice` | str | 可转债当前价格 |  |
| `KZZYj` | str | 溢价率 |  |
| `ZGValue` | str | 转股价值 |  |


## <a id="getfinancialdata"></a>`get_financial_data` 专业财务数据(FN指标)

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表例如 ["600519.SH"] |
| `field_list` | Y | List[str] | 字段筛选，不能为空，字段名须与 系统定义一致（如 FN193 ） |
| `start_time` | Y | str | 起始时间，格式 YYYYMMDD ，如 '20250101' |
| `end_time` | N | str | 结束时间，格式 YYYYMMDD ，为 空表示无结束限制 |
| `report_type` | N | bool | 按截止日期还是公告日期筛选，可 选值： 'announce time' （按公 _ 告日期筛选）或 'tag time' （按 _ 报告期筛选） |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `announce_time` | int | 公告日期 |
| `tag_time` | int | 报告期 |
| `FN1` | double | 基本每股收益 |
| `FN2` | double | 扣除非经常性损益每股收益 |
| `FN3` | double | 每股未分配利润 |
| `FN4` | double | 每股净资产 |
| `FN5` | double | 每股资本公积金 |
| `FN6` | double | 净资产收益率 |
| `FN7` | double | 每股经营现金流量 |
| `FN8` | double | 货币资金 |
| `FN9` | double | 交易性金融资产 |
| `FN10` | double | 应收票据 |
| `FN11` | double | 应收账款 |
| `FN12` | double | 预付款项 |
| `FN13` | double | 其他应收款 |
| `FN14` | double | 应收关联公司款 |
| `FN15` | double | 应收利息 |
| `FN16` | double | 应收股利 |
| `FN17` | double | 存货 |
| `FN18` | double | 其中：消耗性生物资产 |
| `FN19` | double | 一年内到期的非流动资产 |
| `FN20` | double | 其他流动资产 |
| `FN21` | double | 流动资产合计 |
| `FN22` | double | 可供出售金融资产 |
| `FN23` | double | 持有至到期投资 |
| `FN24` | double | 长期应收款 |
| `FN25` | double | 长期股权投资 |
| `FN26` | double | 投资性房地产 |
| `FN27` | double | 固定资产 |
| `FN28` | double | 在建工程 |
| `FN29` | double | 工程物资 |
| `FN30` | double | 固定资产清理 |
| `FN31` | double | 生产性生物资产 |
| `FN32` | double | 油气资产 |
| `FN33` | double | 无形资产 |
| `FN34` | double | 开发支出 |
| `FN35` | double | 商誉 |
| `FN36` | double | 长期待摊费用 |
| `FN37` | double | 递延所得税资产 |
| `FN38` | double | 其他非流动资产 |
| `FN39` | double | 非流动资产合计 |
| `FN40` | double | 资产总计 |
| `FN41` | double | 短期借款 |
| `FN42` | double | 交易性金融负债 |
| `FN43` | double | 应付票据 |
| `FN44` | double | 应付账款 |
| `FN45` | double | 预收款项 |
| `FN46` | double | 应付职工薪酬 |
| `FN47` | double | 应交税费 |
| `FN48` | double | 应付利息 |
| `FN49` | double | 应付股利 |
| `FN50` | double | 其他应付款 |
| `FN51` | double | 应付关联公司款 |
| `FN52` | double | 一年内到期的非流动负债 |
| `FN53` | double | 其他流动负债 |
| `FN54` | double | 流动负债合计 |
| `FN55` | double | 长期借款 |
| `FN56` | double | 应付债券 |
| `FN57` | double | 长期应付款 |
| `FN58` | double | 专项应付款 |
| `FN59` | double | 预计负债 （非流动负债） |
| `FN60` | double | 递延所得税负债 |
| `FN61` | double | 其他非流动负债 |
| `FN62` | double | 非流动负债合计 |
| `FN63` | double | 负债合计 |
| `FN64` | double | 实收资本（或股本） |
| `FN65` | double | 资本公积 |
| `FN66` | double | 盈余公积 |
| `FN67` | double | 减：库存股 |
| `FN68` | double | 未分配利润 |
| `FN69` | double | 少数股东权益 |
| `FN70` | double | 外币报表折算价差 |
| `FN71` | double | 非正常经营项目收益调整 |
| `FN72` | double | 所有者权益（或股东权益）合计 |
| `FN73` | double | 负债和所有者（或股东权益）合计 |
| `FN98` | double | 销售商品、提供劳务收到的现金 |
| `FN99` | double | 收到的税费返还 |
| `FN100` | double | 收到其他与经营活动有关的现金 |
| `FN101` | double | 经营活动现金流入小计 |
| `FN102` | double | 购买商品、接受劳务支付的现金 |
| `FN103` | double | 支付给职工以及为职工支付的现金 |
| `FN104` | double | 支付的各项税费 |
| `FN105` | double | 支付其他与经营活动有关的现金 |
| `FN106` | double | 经营活动现金流出小计 |
| `FN107` | double | 经营活动产生的现金流量净额 |
| `FN108` | double | 收回投资收到的现金 |
| `FN109` | double | 取得投资收益收到的现金 |
| `FN110` | double | 处置固定资产、无形资产和其他长期资 产收回的现金净额 |
| `FN111` | double | 处置子公司及其他营业单位收到的现金 净额 |
| `FN112` | double | 收到其他与投资活动有关的现金 |
| `FN113` | double | 投资活动现金流入小计 |
| `FN114` | double | 购建固定资产、无形资产和其他长期资 产支付的现金 |
| `FN115` | double | 投资支付的现金 |
| `FN116` | double | 取得子公司及其他营业单位支付的现金 净额 |
| `FN117` | double | 支付其他与投资活动有关的现金 |
| `FN118` | double | 投资活动现金流出小计 |
| `FN119` | double | 投资活动产生的现金流量净额 |
| `FN120` | double | 吸收投资收到的现金 |
| `FN121` | double | 取得借款收到的现金 |
| `FN122` | double | 收到其他与筹资活动有关的现金 |
| `FN123` | double | 筹资活动现金流入小计 |
| `FN124` | double | 偿还债务支付的现金 |
| `FN125` | double | 分配股利、利润或偿付利息支付的现金 |
| `FN126` | double | 支付其他与筹资活动有关的现金 |
| `FN127` | double | 筹资活动现金流出小计 |
| `FN128` | double | 筹资活动产生的现金流量净额 |
| `FN129` | double | 四、汇率变动对现金的影响 |
| `FN130` | double | 四(2)、其他原因对现金的影响 |
| `FN131` | double | 五、现金及现金等价物净增加额 |
| `FN132` | double | 期初现金及现金等价物余额 |
| `FN133` | double | 期末现金及现金等价物余额 |
| `FN134` | double | 净利润 |
| `FN135` | double | 加：资产减值准备 |
| `FN136` | double | 固定资产折旧、油气资产折耗、生产性 生物资产折旧 |
| `FN137` | double | 无形资产摊销 |
| `FN138` | double | 长期待摊费用摊销 |
| `FN139` | double | 处置固定资产、无形资产和其他长期资 产的损失 |
| `FN140` | double | 固定资产报废损失 |
| `FN141` | double | 公允价值变动损失 |
| `FN142` | double | 财务费用 |
| `FN143` | double | 投资损失 |
| `FN144` | double | 递延所得税资产减少 |
| `FN145` | double | 递延所得税负债增加 |
| `FN146` | double | 存货的减少 |
| `FN147` | double | 经营性应收项目的减少 |
| `FN148` | double | 经营性应付项目的增加 |
| `FN149` | double | 其他 |
| `FN150` | double | 经营活动产生的现金流量净额2 |
| `FN151` | double | 债务转为资本 |
| `FN152` | double | 一年内到期的可转换公司债券 |
| `FN153` | double | 融资租入固定资产 |
| `FN154` | double | 现金的期末余额 |
| `FN155` | double | 减：现金的期初余额 |
| `FN156` | double | 加：现金等价物的期末余额 |
| `FN157` | double | 减：现金等价物的期初余额 |
| `FN158` | double | 现金及现金等价物净增加额 |
| `FN159` | double | 流动比率(非金融类指标) |
| `FN160` | double | 速动比率(非金融类指标) |
| `FN161` | double | 现金比率(%)(非金融类指标) |
| `FN162` | double | 利息保障倍数(非金融类指标) |
| `FN163` | double | 非流动负债比率(%)(非金融类指标) |
| `FN164` | double | 流动负债比率(%)(非金融类指标) |
| `FN166` | double | 有形资产净值债务率(%) |
| `FN167` | double | 权益乘数(%) |
| `FN168` | double | 股东的权益/负债合计(%) |
| `FN169` | double | 有形资产/负债合计(%) |
| `FN170` | double | 经营活动产生的现金流量净额/负债合计 (%)(非金融类指标) |
| `FN171` | double | EBITDA/负债合计(%)(非金融类指标) |
| `FN172` | double | 应收帐款周转率(非金融类指标) |
| `FN173` | double | 存货周转率(非金融类指标) |
| `FN174` | double | 运营资金周转率(非金融类指标) |
| `FN175` | double | 总资产周转率(非金融类指标) |
| `FN176` | double | 固定资产周转率(非金融类指标) |
| `FN177` | double | 应收帐款周转天数(非金融类指标) |
| `FN178` | double | 存货周转天数(非金融类指标) |
| `FN179` | double | 流动资产周转率(非金融类指标) |
| `FN180` | double | 流动资产周转天数(非金融类指标) |
| `FN181` | double | 总资产周转天数(非金融类指标) |
| `FN182` | double | 股东权益周转率(非金融类指标) |
| `FN183` | double | 营业收入增长率(%) |
| `FN184` | double | 净利润增长率(%) |
| `FN185` | double | 净资产增长率(%) |
| `FN186` | double | 固定资产增长率(%) |
| `FN187` | double | 总资产增长率(%) |
| `FN188` | double | 投资收益增长率(%) |
| `FN189` | double | 营业利润增长率(%) |
| `FN190` | double | 扣非每股收益同比(%) |
| `FN191` | double | 扣非净利润同比(%) |
| `FN192` | double | 暂无 |
| `FN193` | double | 成本费用利润率(%) |
| `FN194` | double | 营业利润率(非金融类指标) |
| `FN195` | double | 营业税金率(非金融类指标) |
| `FN196` | double | 营业成本率(非金融类指标) |
| `FN197` | double | 净资产收益率 |
| `FN198` | double | 投资收益率 |
| `FN199` | double | 销售净利率(%) |
| `FN200` | double | 总资产净利率 |
| `FN201` | double | 净利润率(非金融类指标) |
| `FN202` | double | 销售毛利率(%)(非金融类指标) |
| `FN203` | double | 三费比重(非金融类指标) |
| `FN204` | double | 管理费用率(非金融类指标) |
| `FN205` | double | 财务费用率(非金融类指标) |
| `FN206` | double | 扣除非经常性损益后的净利润 |
| `FN207` | double | 息税前利润(EBIT) |
| `FN208` | double | 息税折旧摊销前利润(EBITDA) |
| `FN209` | double | EBITDA/营业总收入(%)(非金融类指标) |
| `FN210` | double | 资产负债率(%) |
| `FN211` | double | 流动资产比率(非金融类指标) |
| `FN212` | double | 货币资金比率(非金融类指标) |
| `FN213` | double | 存货比率(非金融类指标) |
| `FN214` | double | 固定资产比率 |
| `FN215` | double | 负债结构比(非金融类指标) |
| `FN216` | double | 归属于母公司股东权益/全部投入资本(%) |
| `FN217` | double | 股东的权益/带息债务(%) |
| `FN218` | double | 有形资产/净债务(%) |
| `FN219` | double | 每股经营性现金流(元) |
| `FN220` | double | 营业收入现金含量(%)(非金融类指标) |
| `FN221` | double | 经营活动产生的现金流量净额/经营活动 净收益(%) |
| `FN222` | double | 销售商品提供劳务收到的现金/营业收入 (%) |
| `FN223` | double | 经营活动产生的现金流量净额/营业收入 |
| `FN224` | double | 资本支出/折旧和摊销 |
| `FN225` | double | 每股现金流量净额(元) |
| `FN226` | double | 经营净现金比率（短期债务）(非金融类 指标) |
| `FN227` | double | 经营净现金比率（全部债务） |
| `FN228` | double | 经营活动现金净流量与净利润比率 |
| `FN229` | double | 全部资产现金回收率 |
| `FN230` | double | 营业收入 |
| `FN231` | double | 营业利润 |
| `FN232` | double | 归属于母公司所有者的净利润 |
| `FN233` | double | 扣除非经常性损益后的净利润 |
| `FN234` | double | 经营活动产生的现金流量净额 |
| `FN235` | double | 投资活动产生的现金流量净额 |
| `FN236` | double | 筹资活动产生的现金流量净额 |
| `FN237` | double | 现金及现金等价物净增加额 |
| `FN238` | double | 总股本 |
| `FN239` | double | 已上市流通A股 |
| `FN240` | double | 已上市流通B股 |
| `FN241` | double | 已上市流通H股 |
| `FN242` | double | 股东人数(户) |
| `FN243` | double | 第一大股东的持股数量 |
| `FN244` | double | 十大流通股东持股数量合计(股) |
| `FN245` | double | 十大股东持股数量合计(股) |
| `FN246` | double | 机构总量（家） |
| `FN247` | double | 机构持股总量(股) |
| `FN248` | double | QFII机构数 |
| `FN249` | double | QFII持股量 |
| `FN250` | double | 券商机构数 |
| `FN251` | double | 券商持股量 |
| `FN252` | double | 保险机构数 |
| `FN253` | double | 保险持股量 |
| `FN254` | double | 基金机构数 |
| `FN255` | double | 基金持股量 |
| `FN256` | double | 社保机构数 |
| `FN257` | double | 社保持股量 |
| `FN258` | double | 私募机构数 |
| `FN259` | double | 私募持股量 |
| `FN260` | double | 财务公司机构数 |
| `FN261` | double | 财务公司持股量 |
| `FN262` | double | 年金机构数 |
| `FN263` | double | 年金持股量 |
| `FN264` | double | 十大流通股东持有的流通A股合计(股)[ 注：2019半年报之前，季度报告中，若 股东持股除了流通A股、还有流通B股或 流通H股，指标264取的是包含流通B股或 流通H股的流通股数] |
| `FN265` | double | 第一大流通股东持股量(股) |
| `FN266` | double | 自由流通股(股)[注：1.自由流通股=已流 通A股-持股5%以上股东的流通A股（一 致行动人算一起）；2.指标按报告期展 示，新股在上市日的下个报告期才有数 据] |
| `FN267` | double | 受限流通A股(股) |
| `FN268` | double | 一般风险准备(金融类) |
| `FN269` | double | 其他综合收益(利润表) |
| `FN270` | double | 综合收益总额(利润表) |
| `FN271` | double | 归属于母公司股东权益(资产负债表) |
| `FN272` | double | 银行机构数(家)(机构持股) |
| `FN273` | double | 银行持股量(股)(机构持股) |
| `FN274` | double | 一般法人机构数(家)(机构持股) |
| `FN275` | double | 一般法人持股量(股)(机构持股) |
| `FN276` | double | 近一年净利润(元) |
| `FN277` | double | 信托机构数(家)(机构持股) |
| `FN278` | double | 信托持股量(股)(机构持股) |
| `FN279` | double | 特殊法人机构数(家)(机构持股) |
| `FN280` | double | 特殊法人持股量(股)(机构持股) |
| `FN281` | double | 加权净资产收益率(每股指标) |
| `FN282` | double | 扣非每股收益(单季度财务指标) |
| `FN283` | double | 最近一年营业收入(万元) |
| `FN284` | double | 国家队持股数量（万股)[注：本指标统计 包含汇金公司、证金公司、外汇管理局 旗下投资平台、国家队基金、国开、养 老金以及中科汇通等国家队机构持股数 量] |
| `FN285` | double | 业绩预告-本期归母净利润同比增幅下 限%[注：指标285至294展示未来一个报 告期的数据。例，3月31日至6月29日这 段时间内展示的是中报的数据；如果最 新的财务报告后面有多个报告期的业绩 预告/快报，只能展示最新的财务报告后 面的一个报告期的业绩预告/快报] |
| `FN286` | double | 业绩预告-本期归母净利润同比增幅上 限% |
| `FN287` | double | 业绩快报-归母净利润 |
| `FN288` | double | 业绩快报-扣非净利润 |
| `FN289` | double | 业绩快报-总资产 |
| `FN290` | double | 业绩快报-净资产 |
| `FN291` | double | 业绩快报-每股收益 |
| `FN292` | double | 业绩快报-摊薄净资产收益率 |
| `FN293` | double | 业绩快报-加权净资产收益率 |
| `FN294` | double | 业绩快报-每股净资产 |
| `FN295` | double | 应付票据及应付账款(资产负债表) |
| `FN296` | double | 应收票据及应收账款(资产负债表) |
| `FN297` | double | 递延收益(资产负债表-非流动负债) |
| `FN298` | double | 其他综合收益(资产负债表) |
| `FN299` | double | 其他权益工具(资产负债表) |
| `FN300` | double | 其他收益(利润表) |
| `FN301` | double | 资产处置收益(利润表) |
| `FN302` | double | 持续经营净利润(利润表) |
| `FN303` | double | 终止经营净利润(利润表) |
| `FN304` | double | 研发费用(利润表) |
| `FN305` | double | 其中:利息费用(利润表-财务费用) |
| `FN306` | double | 其中:利息收入(利润表-财务费用) |
| `FN307` | double | 近一年经营活动现金流净额 |
| `FN308` | double | 近一年归母净利润(万元) |
| `FN309` | double | 近一年扣非净利润(万元) |
| `FN310` | double | 近一年现金净流量(万元) |
| `FN311` | double | 基本每股收益（单季度） |
| `FN312` | double | 营业总收入(单季度)(万元) |
| `FN313` | double | 业绩预告公告日期 [注：本指标展示未来 一个报告期的数据。例,3月31日至6月29 日这段时间内展示的是中报的数据；如 果最新的财务报告后面有多个报告期的 业绩预告/快报，只能展示最新的财务报 告后面的一个报告期的业绩预告/快报的 数据；公告日期格式为YYMMDD，例： 190101代表2019年1月1日] |
| `FN314` | double | 财报公告日期 [注：日期格式为 YYMMDD,例：190101代表2019年1月1 日] |
| `FN315` | double | 业绩快报公告日期 [注：本指标展示未来 一个报告期的数据。例,3月31日至6月29 日这段时间内展示的是中报的数据；如 果最新的财务报告后面有多个报告期的 业绩预告/快报，只能展示最新的财务报 告后面的一个报告期的业绩预告/快报的 数据；公告日期格式为YYMMDD，例： 190101代表2019年1月1日] |
| `FN316` | double | 近一年投资活动现金流净额(万元) |
| `FN317` | double | 业绩预告-本期归母净利润下限(万元) [注：指标317至318展示未来一个报告期 的数据。例，3月31日至6月29日这段时 间内展示的是中报的数据；如果最新的 财务报告后面有多个报告期的业绩预告/ 快报，只能展示最新的财务报告后面的 一个报告期的业绩预告/快报] |
| `FN318` | double | 业绩预告-本期归母净利润上限(万元) |
| `FN319` | double | 营业总收入TTM(万元) |
| `FN320` | double | 员工总数(人) |
| `FN321` | double | 每股企业自由现金流 |
| `FN322` | double | 每股股东自由现金流 |
| `FN323` | double | 近一年营业利润(万元) |
| `FN324` | double | 净利润（单季度）(万元) |
| `FN325` | double | 北上资金数（家）(机构持股） |
| `FN326` | double | 北上资金持股量（股）(机构持股） |
| `FN327` | double | 有息负债率 |
| `FN328` | double | 营业成本（单季度）(万元) |
| `FN329` | double | 投入资本回报率（ROIC）(获利能力分析) |
| `FN330` | double | 业绩快报-营业收入（本期） |
| `FN331` | double | 业绩快报-营业收入（上期） |
| `FN332` | double | 业绩快报-营业利润（本期） |
| `FN333` | double | 业绩快报-营业利润（上期） |
| `FN334` | double | 业绩快报-利润总额（本期） |
| `FN335` | double | 业绩快报-利润总额（上期） |
| `FN336` | double | 审计意见 [注：0-未审计,1-无保留意见,2- 带强调事项段的无保留意见,3-保留意 见,4-无法表示意见,5-否定意见及其他] |
| `FN337` | double | 股利支付率（%） |
| `FN338` | double | 近一年营业成本-非金融类(万元) |
| `FN339` | double | 近一年营业成本-金融类(万元) |
| `FN340` | double | 业绩预告-本期扣非后净利润下限(万元) |
| `FN341` | double | 业绩预告-本期扣非后净利润上限(万元) |
| `FN342` | double | 业绩预告-本期扣非后净利润同比增长下 限（%） |
| `FN343` | double | 业绩预告-本期扣非后净利润同比增长上 限（%） |
| `FN344` | double | 业绩预告-预告基本每股收益下限(元) |
| `FN345` | double | 业绩预告-预告基本每股收益上限(元) |
| `FN346` | double | 业绩预告-预告基本每股收益同比增长下 限（%） |
| `FN347` | double | 业绩预告-预告基本每股收益同比增长上 限（%） |
| `FN348` | double | 业绩预告-预告扣非后基本每股收益下限 (元) |
| `FN349` | double | 业绩预告-预告扣非后基本每股收益上限 (元) |
| `FN350` | double | 业绩预告-预告扣非后基本每股收益同比 增长下限（%） |
| `FN351` | double | 业绩预告-预告扣非后基本每股收益同比 增长上限（%） |
| `FN352` | double | 业绩预告-预告营业收入下限(万元) |
| `FN353` | double | 业绩预告-预告营业收入上限(万元) |
| `FN354` | double | 业绩预告-预告营业收入同比增长下限 （%） |
| `FN355` | double | 业绩预告-预告营业收入同比增长上限 （%） |
| `FN356` | double | 业绩预告-预告扣除后营业收入下限(万 元) |
| `FN357` | double | 业绩预告-预告扣除后营业收入上限(万 元) |
| `FN358` | double | 主营业务收入(内销)(万元) |
| `FN359` | double | 主营业务收入(外销)(万元) |
| `FN360` | double | 资管计划机构数(家) |
| `FN361` | double | 资管计划持股量(股) |
| `FN362` | double | 财务总评分 |
| `FN401` | double | 专项储备(万元) |
| `FN402` | double | 结算备付金(万元) |
| `FN403` | double | 拆出资金(万元) |
| `FN404` | double | 发放贷款及垫款(万元)(流动资产科目) |
| `FN405` | double | 衍生金融资产(万元) |
| `FN406` | double | 应收保费(万元) |
| `FN407` | double | 应收分保账款(万元) |
| `FN408` | double | 应收分保合同准备金(万元) |
| `FN409` | double | 买入返售金融资产(万元) |
| `FN410` | double | 划分为持有待售的资产(万元) |
| `FN411` | double | 发放贷款及垫款(万元)(非流动资产科目) |
| `FN412` | double | 向中央银行借款(万元) |
| `FN413` | double | 吸收存款及同业存放(万元) |
| `FN414` | double | 拆入资金(万元) |
| `FN415` | double | 衍生金融负债(万元) |
| `FN416` | double | 卖出回购金融资产款(万元) |
| `FN417` | double | 应付手续费及佣金(万元) |
| `FN418` | double | 应付分保账款(万元) |
| `FN419` | double | 保险合同准备金(万元) |
| `FN420` | double | 代理买卖证券款(万元) |
| `FN421` | double | 代理承销证券款(万元) |
| `FN422` | double | 划分为持有待售的负债(万元) |
| `FN423` | double | 预计负债(万元) （流动负债） |
| `FN424` | double | 递延收益(万元)（流动负债科目，公告此 科目的股票较少，大部分公司没有此数 据） |
| `FN425` | double | 其中:优先股(万元)(非流动负债科目) |
| `FN426` | double | 永续债(万元)(非流动负债科目) |
| `FN427` | double | 长期应付职工薪酬(万元) |
| `FN428` | double | 其中:优先股(万元)(所有者权益科目) |
| `FN429` | double | 永续债(万元)(所有者权益科目) |
| `FN430` | double | 债权投资(万元) |
| `FN431` | double | 其他债权投资(万元) |
| `FN432` | double | 其他权益工具投资(万元) |
| `FN433` | double | 其他非流动金融资产(万元) |
| `FN434` | double | 合同负债(万元) |
| `FN435` | double | 合同资产(万元) |
| `FN436` | double | 其他资产(万元) |
| `FN437` | double | 应收款项融资(万元) |
| `FN438` | double | 使用权资产(万元) |
| `FN439` | double | 租赁负债(万元) |
| `FN440` | double | 发放贷款及垫款(万元) [注：金融类科目] |
| `FN441` | double | 应收款项(万元) [注：证券类指标] |
| `FN442` | double | 存出保证金(万元) [注：证券类指标] |
| `FN443` | double | 现金及存放中央银行款项(万元) [注：金 融类科目] |
| `FN444` | double | 贵金属(万元) [注：金融类科目] |
| `FN445` | double | 以公允价值计量且其变动计入当期损益 的金融资产(万元) [注：金融类科目] |
| `FN446` | double | 代理业务资产(万元) [注：金融类科目] |
| `FN447` | double | 应收款项类投资(万元) [注：金融类科目] |
| `FN448` | double | 同业及其它金融机构存放款项(万元) [注：金融类科目] |
| `FN449` | double | 以公允价值计量且其变动计入当期损益 的金融负债(万元) [注：金融类科目] |
| `FN450` | double | 吸收存款(万元) [注：金融类科目] |
| `FN451` | double | 代理业务负债(万元) [注：金融类科目] |
| `FN452` | double | 其他负债(万元) [注：金融类科目] |
| `FN453` | double | 发放贷款及垫款(万元) [注：金融类科目] |
| `FN501` | double | 稀释每股收益(元) |
| `FN502` | double | 营业总收入(万元) |
| `FN503` | double | 汇兑收益(万元) |
| `FN504` | double | 其中:归属于母公司综合收益(万元) |
| `FN505` | double | 其中:归属于少数股东综合收益(万元) |
| `FN506` | double | 利息收入(万元) |
| `FN507` | double | 已赚保费(万元) |
| `FN508` | double | 手续费及佣金收入(万元) |
| `FN509` | double | 利息支出(万元) |
| `FN510` | double | 手续费及佣金支出(万元) |
| `FN511` | double | 退保金(万元) |
| `FN512` | double | 赔付支出净额(万元) |
| `FN513` | double | 提取保险合同准备金净额(万元) |
| `FN514` | double | 保单红利支出(万元) |
| `FN515` | double | 分保费用(万元) |
| `FN516` | double | 其中:非流动资产处置利得(万元) |
| `FN517` | double | 信用减值损失(万元) |
| `FN518` | double | 净敞口套期收益(万元) |
| `FN519` | double | 营业总成本(万元) |
| `FN520` | double | 信用减值损失(万元、2019格式) |
| `FN521` | double | 资产减值损失(万元、2019格式) |
| `FN522` | double | 其他业务收入(万元) [注：金融类科目] |
| `FN523` | double | 业务及管理费(万元) [注：金融类科目] |
| `FN524` | double | 其他业务成本(万元) [注：金融类科目] |
| `FN561` | double | 加:其他原因对现金的影响2(万元)(现金的 期末余额科目) |
| `FN562` | double | 客户存款和同业存放款项净增加额(万元) |
| `FN563` | double | 向中央银行借款净增加额(万元) |
| `FN564` | double | 向其他金融机构拆入资金净增加额(万元) |
| `FN565` | double | 收到原保险合同保费取得的现金(万元) |
| `FN566` | double | 收到再保险业务现金净额(万元) |
| `FN567` | double | 保户储金及投资款净增加额(万元) |
| `FN568` | double | 处置以公允价值计量且其变动计入当期 损益的金融资产净增加额(万元) |
| `FN569` | double | 收取利息、手续费及佣金的现金(万元) |
| `FN570` | double | 拆入资金净增加额(万元) |
| `FN571` | double | 回购业务资金净增加额(万元) |
| `FN572` | double | 客户贷款及垫款净增加额(万元) |
| `FN573` | double | 存放中央银行和同业款项净增加额(万元) |
| `FN574` | double | 支付原保险合同赔付款项的现金(万元) |
| `FN575` | double | 支付利息、手续费及佣金的现金(万元) |
| `FN576` | double | 支付保单红利的现金(万元) |
| `FN577` | double | 其中:子公司吸收少数股东投资收到的现 金(万元) |
| `FN578` | double | 其中:子公司支付给少数股东的股利、利 润(万元) |
| `FN579` | double | 投资性房地产的折旧及摊销(万元) |
| `FN580` | double | 信用减值损失(万元) |
| `FN581` | double | 使用权资产折旧（万元） |
| `FN582` | double | 收取利息和手续费净增加额(万元) [注： 金融类科目] |
| `FN583` | double | 支付手续费的现金(万元) [注：金融类科 目] |
| `FN584` | double | 发行债券支付的现金(万元) [注：金融类 科目] |


## <a id="getfinancialdatabydate"></a>`get_financial_data_by_date` 指定日期财务

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空（如 FN193 ） |
| `year` | Y | int | 指定年份 |
| `mmdd` | Y | int | 指定月日 |


## <a id="getgponedata"></a>`get_gp_one_data` 股票单个财务数据

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空（如 GO47 表示是第47号个股数据最新业绩 预告 本期扣非净利润预计同比增 减幅上限%）这个值，GO为gp one的首字母大写 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `GO1` | double | 发行价(元) |
| `GO2` | double | 总发行数量(万股) |
| `GO3` | double | 一致预期目标价(元)[注：一致预期值均为近半年内各家机构预 测数值的平均值] |
| `GO4` | double | 一致预期T年度 |
| `GO5` | double | 一致预期T年每股收益 |
| `GO6` | double | 一致预期T+1年每股收益 |
| `GO7` | double | 一致预期T+2年每股收益 |
| `GO8` | double | 一致预期T年净利润(万元) |
| `GO9` | double | 一致预期T+1年净利润(万元) |
| `GO10` | double | 一致预期T+2年净利润(万元) |
| `GO11` | double | 一致预期T年营业收入(万元) |
| `GO12` | double | 一致预期T+1年营业收入(万元) |
| `GO13` | double | 一致预期T+2年营业收入(万元) |
| `GO14` | double | 一致预期T年营业利润(万元) |
| `GO15` | double | 一致预期T+1年营业利润(万元) |
| `GO16` | double | 一致预期T+2年营业利润(万元) |
| `GO17` | double | 一致预期T年每股净资产(元) |
| `GO18` | double | 一致预期T+1年每股净资产(元) |
| `GO19` | double | 一致预期T+2年每股净资产(元) |
| `GO20` | double | 一致预期T年净资产收益率(%) |
| `GO21` | double | 一致预期T+1年净资产收益率(%) |
| `GO22` | double | 一致预期T+2年净资产收益率(%) |
| `GO23` | double | 一致预期T年PE |
| `GO24` | double | 一致预期T+1年PE |
| `GO25` | double | 一致预期T+2年PE |
| `GO26` | double | 最新解禁日(YYMMDD格式) |
| `GO27` | double | 最新解禁数量（万股） |
| `GO28` | double | 下一报告期的预约披露时间 |
| `GO29` | double | 最新持股机构家数 |
| `GO30` | double | 最新机构持股总量（万股） |
| `GO31` | double | 最新持股基金家数 |
| `GO32` | double | 最新基金持股量（万股） |
| `GO33` | double | 最新总股本（万股） |
| `GO34` | double | 最新实际流通A股（万股） |
| `GO35` | double | 最新业绩预告 报告期(YYMMDD格式) |
| `GO36` | double | 最新业绩预告 本期归母净利润下限（万元） |
| `GO37` | double | 最新业绩预告 本期归母净利润上限（万元） |
| `GO38` | double | 最新业绩预告 本期归母净利润预计同比增减幅下限% |
| `GO39` | double | 最新业绩预告 本期归母净利润预计同比增减幅上限% |
| `GO40` | double | 最新业绩快报 报告期 |
| `GO41` | double | 最新业绩快报 归母净利润（万元） |
| `GO42` | double | 分红募资 派现总额（万元） |
| `GO43` | double | 分红募资 募资总额（万元） |
| `GO44` | double | 最新业绩预告 本期扣非净利润下限(万元) |
| `GO45` | double | 最新业绩预告 本期扣非净利润上限(万元) |
| `GO46` | double | 最新业绩预告 本期扣非净利润预计同比增减幅下限% |
| `GO47` | double | 最新业绩预告 本期扣非净利润预计同比增减幅上限% |


## <a id="getgpjyvalue"></a>`get_gpjy_value` 股票经济指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `start_time` | N | str | 起始时间 |
| `end_time` | N | str | 结束时间 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `GP01` | double | 股东人数 股东户数(户) |
| `GP02` | double | 龙虎榜 买入总计(万元) 卖出总计(万元)[注：该指标展示 20230717日之后的数据] |
| `GP03` | double | 融资融券1 融资余额(万元) 融券余量(股) |
| `GP04` | double | 大宗交易 成交均价(元) 成交额(万元) |
| `GP05` | double | 增减持1 成交均价(元) 变动股数(股) |
| `GP06` | double | 陆股通持股量 持股数量(股)[注：该指标展示20170317日之后的 数据] |
| `GP07` | double | 陆股通市场成交净额 陆股通市场净买入(万元)[注：官方只公布 了每日的前十名数据] |
| `GP08` | double | 龙虎榜机构(卖方)数据 卖方机构个数 机构卖出金额(万元) |
| `GP09` | double | 龙虎榜机构(买方)数据 买方机构个数 机构买入金额(万元) |
| `GP10` | double | 近3月机构调研情况 近3月机构调研次数 近3月调研机构数量 |
| `GP11` | double | 融资融券2 融资买入额(万元) 融资偿还额(万元) |
| `GP12` | double | 融资融券3 融券卖出量(股) 融券偿还量(股) |
| `GP13` | double | 融资融券4 融资净买入(万元) 融券净卖出(股) |
| `GP14` | double | 涨停数据 涨停金额(即板上成交,万元) 开板次数[注：该指标展示 20180319日之后的数据] |
| `GP15` | double | 涨跌停 涨跌停状态 封单金额(万元)[注：涨停取2,曾涨停取1,跌停 取-2,曾跌停取-1;跌停和曾跌停时,封单金额取负值 该指标展示 20160926日之后的数据] |
| `GP16` | double | 总市值 总市值(万元) |
| `GP17` | double | 龙虎榜营业部数据 买入金额(万元) 卖出金额(万元) |
| `GP18` | double | 龙虎榜沪深股通数据 买入金额(万元) 卖出金额(万元) |
| `GP19` | double | 每周股票质押数量 无限售股份质押数(万) 有限售股份质押数(万) [注：该指标展示20180316日之后的数据] |
| `GP20` | double | 每周股票质押比例 质押比例(%)[注：该指标展示20180316日之 后的数据] |
| `GP21` | double | 股息率 股息率(%) |
| `GP22` | double | 涨跌停 封成比 封流比[注：该指标展示20180319日之后的数据] |
| `GP23` | double | 拟增减持 拟增持数量(万股) 拟减持数量(万股) |
| `GP24` | double | 涨停 首次涨停时间 涨停最大封单额(万) [注：首次涨停时间展示 20160301之后的数据，涨停最大封单额展示20200730之后的数 据] |
| `GP25` | double | 盘前盘后成交量 开盘成交量(手) 盘后固定成交量(手) [注：盘后 固定成交量只包含科创板和创业板] |
| `GP26` | double | 拟增减持金额 拟增持金额(万元) 拟减持金额(万元) |
| `GP27` | double | 人气排名 市场人气排名 行业人气排名 [注：行业排名为通达信 二级研究行业排名] |
| `GP28` | double | 股票回购 回购均价(元) 回购数量(万股) |
| `GP29` | double | 证券信息 是否复牌日 是否更名日 [注：是否复牌日说明：0-不是 复牌日，n(n>0)-停牌n个交易日之后的复牌日；是否更名日说 明：0-未更名，1-常规更名，2-加ST，3-加*ST，4-摘帽，5-其 他] |
| `GP30` | double | 分红送转 派息金额(万元) 送转数量(股) [注：对应展示日期为除 权除息日] |
| `GP31` | double | 转融券 期初余量(股) 期末余量(股) |
| `GP32` | double | 转融券 融出数量(股) 融出市值(元) |
| `GP33` | double | 跌停数据 跌停金额(万元) 开板次数 [注：该指标展示20180319日 之后的数据,暂无跌停金额数据] |
| `GP34` | double | 跌停 首次跌停时间 跌停最大封单额(万) [注：首次跌停时间展示 20160301之后的数据，跌停最大封单额展示20200730之后的数 据] |
| `GP35` | double | 增减持2 增持数量(股) 减持数量(股) |
| `GP36` | double | 竞价涨停买 买入金额(万元) [注：该指标展示20241101日之后的 数据] |
| `GP37` | double | 龙虎榜2 上榜类型连续交易日(天) [注：该指标展示上榜类型中指 代的连续交易日类型] |
| `GP38` | double | 涨停相关1 近1年涨停次数 近1年溢价5%次数 |
| `GP39` | double | 涨停相关2 近1年首板封板率(%) 近1年次日红盘率(%) |
| `GP40` | double | 涨停相关3 近1年连板率(%) 最后涨停时间 |
| `GP41` | double | 股权登记日 配股股权登记日 |
| `GP42` | double | 龙虎榜专业机构买卖净额 买方成交净额(万元) 卖方成交净额(万 元) |
| `GP43` | double | 配股实施 配股价格(元) 配股数量(万股) |
| `GP44` | double | 股票评分 综合评分 |
| `GP45` | double | 评级系数 评级系数 |
| `GP46` | double | 拟询价转让 拟转让股数(万股) 拟转让占总股本(%) |


## <a id="getgpjyvaluebydate"></a>`get_gpjy_value_by_date` 指定日期股票经济指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `year` | Y | int | 指定年份 |
| `mmdd` | Y | int | 指定月日 |


## <a id="getbkjyvalue"></a>`get_bkjy_value` 板块经济指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `start_time` | N | str | 起始时间 |
| `end_time` | N | str | 结束时间 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `BK5` | double | 市盈率TTM 整体法 算术平均 |
| `BK6` | double | 市净率MRQ 整体法 算术平均 |
| `BK7` | double | 市销率TTM 整体法 算术平均 |
| `BK8` | double | 市现率TTM 整体法 算术平均 |
| `BK9` | double | 涨跌数 上涨家数 下跌家数 |
| `BK10` | double | 板块总市值(亿元) 整体法 算术平均 |
| `BK11` | double | 板块流通市值(亿元) 整体法 算术平均 |
| `BK12` | double | 涨停数 涨停家数 曾涨停家数[注：该指标展示20160926日之后的 数据] |
| `BK13` | double | 跌停数 跌停家数 曾跌停家数[注：该指标展示20160926日之后的 数据] |
| `BK14` | double | 涨停数据 市场高度(不含ST股和未开板新股) 2板及以上涨停个数 (不含ST股和未开板新股)[注：该指标展示20180319日之后的数 据] |
| `BK15` | double | 融资融券 沪深京融资余额(万元) 沪深京融券余额(万元) |
| `BK16` | double | 陆股通资金流入 沪股通流入金额(亿元) 深股通流入金额(亿元) [注：该指标展示20170320日之后的数据] |
| `BK17` | double | 开盘成交数 开盘成交额(万元) 开盘成交量(万股) |
| `BK18` | double | 板块股息率(%) 算数平均 整体法 |
| `BK19` | double | 板块自由流通市值(亿元) 整体法 算术平均 |


## <a id="getbkjyvaluebydate"></a>`get_bkjy_value_by_date` 指定日期板块经济指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `year` | Y | int | 指定年份 |
| `mmdd` | Y | int | 指定月日 |


## <a id="getscjyvalue"></a>`get_scjy_value` 市场经济指标(SC指标)

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `start_time` | N | str | 起始时间 |
| `end_time` | N | str | 结束时间 |

**返回字段**

| 字段 | 类型 | 说明 |
|---|---|---|
| `SC01` | double | 融资融券 沪深京融资余额(万元) 沪深京融券余额(万元) |
| `SC02` | double | 陆股通资金流入 沪股通流入金额(亿元) 深股通流入金额(亿元) [注：沪股通限制展示2000条数据，深股通展示自20161205以后 的数据] |
| `SC03` | double | 沪深京涨停股个数 涨停股个数 曾涨停股个数 [注：该指标展示 20160926日之后的数据] |
| `SC04` | double | 沪深京跌停股个数 跌停股个数 曾跌停股个数 [注：该指标展示 20160926日之后的数据] |
| `SC05` | double | 上证50股指期货 净持仓(手)[注：该指标展示20171009日之后的 数据] |
| `SC06` | double | 沪深300股指期货 净持仓(手) [注：该指标展示20171009日之后 的数据] |
| `SC07` | double | 中证500股指期货 净持仓(手) [注：该指标展示20171009日之后 的数据] |
| `SC08` | double | ETF基金规模份额数据 ETF基金规模(亿份) ETF净申赎(亿份) |
| `SC09` | double | 沪月新开A股账户 沪月新开A股账户(万户) |
| `SC10` | double | 增减持统计 增持额(万元) 减持额(万元)[注：部分公司公告滞后, 造成每天查看的数据可能会不一样] |
| `SC11` | double | 大宗交易 溢价的大宗交易额(万元) 折价的大宗交易额(万元) |
| `SC12` | double | 限售解禁 限售解禁计划额(亿元) 限售解禁股份实际上市金额(亿 元)[注：该指标展示201802月之后的数据;部分股票的解禁日期延 后，造成不同日期提取的某天的计划额可能不同] |
| `SC13` | double | 分红 市场总分红额(亿元)[注：除权派息日的A股市场总分红额] |
| `SC14` | double | 募资 市场总募资额(亿元)[注：发行日期/除权日期的首发、配股 和增发的总募资额] |
| `SC15` | double | 打板资金 封板成功资金(亿元) 封板失败资金(亿元) [注：该指标 展示20160926日之后的数据] |
| `SC16` | double | 龙虎榜 买入总金额(亿元) 卖出总金额(亿元) |
| `SC17` | double | 龙虎榜机构数据 买入金额(亿元) 卖出金额(亿元) |
| `SC18` | double | 龙虎榜营业部数据 买入金额(亿元) 卖出金额(亿元) |
| `SC19` | double | 龙虎榜沪深股通数据 买入金额(亿元) 卖出金额(亿元) |
| `SC20` | double | 陆股通净买入 沪股通净买入额(亿元) 深股通净买入额(亿元) |
| `SC21` | double | 每周无限售质押率 深市质押率(%) 沪市质押率(%)[注：该指标展 示20180128日之后的数据] |
| `SC22` | double | 每周有限售质押率 深市质押率(%) 沪市质押率(%)[注：该指标展 示20180128日之后的数据] |
| `SC23` | double | 连板家数 连板股个数(包含ST和未开板新股) 连板股个数(不含ST 股和未开板新股）[注：该指标展示20180319日之后的数据] |
| `SC24` | double | 沪深京涨跌停股个数 涨停股个数(不含ST股和未开板新股) 跌停 股个数（不含ST股）[注：该指标展示20160926日之后的数据] |
| `SC25` | double | 融资融券 沪深京融资买入额（万元）沪深京融券卖出量（万股） |
| `SC26` | double | 每周市场质押比 每周市场质押比例（%）[注：该指标展示 20180316日之后的数据] |
| `SC27` | double | 央行公开市场净投放 央行公开市场净投放 (亿元) |
| `SC28` | double | 历史A股新高新低数 历史新高A股股票个数 历史新低A股股票个 数(上市满一年的股票) |
| `SC29` | double | 120天A股新高新低数 120天新高A股股票个数 120天新低A股股 票个数(上市满一年的股票) |
| `SC30` | double | 涨停数据 市场高度(不含ST股和未开板新股) 2板以上涨停个数(不 含ST股和未开板新股)[注：该指标展示20180319日之后的数据] |
| `SC31` | double | 涨跌家数 涨家数（剔除停牌） 跌家数（剔除停牌） |
| `SC32` | double | 20天A股新高新低数 20天新高A股股票个数 20天新低A股股票个 数(上市满一年的股票) |
| `SC33` | double | 市场总封单金额 涨停封单金额（亿元）跌停封单金额（亿元） [注：该指标展示20160926日之后的数据] |
| `SC34` | double | 涨跌股成交量 上涨股成交量(万手) 下跌股成交量(万手) |
| `SC35` | double | 涨停数据 换手板家数 回封率(%) [注：两个指标都剔除了未开板 新股，换手板家数展示20190605日之后的数据，回封率展示 20180927日之后的数据] |
| `SC36` | double | 曾涨跌停股个数 曾涨停股个数(剔除ST股和未开板新股) 曾跌停 股个数(剔除ST股) [注：该指标展示20160926日之后的数据] |
| `SC37` | double | 转融券 融出市值(亿元) 期末余额(亿元) |
| `SC38` | double | ETF基金规模金额数据 ETF基金规模(亿元) ETF净申赎(亿元) |
| `SC39` | double | 涨跌5%家数 涨幅大于等于5%家数 跌幅大于等于5%家数 |
| `SC40` | double | 陆股通成交 陆股通成交总额(亿元) 陆股通成交总笔(万笔) |
| `SC41` | double | 中证1000股指期货 净持仓(手) [注：该指标展示20220722日之后 的数据] |
| `SC42` | double | 沪深股通成交金额 沪股通成交总额(亿元) 深股通成交总额(亿元) |


## <a id="getscjyvaluebydate"></a>`get_scjy_value_by_date` 指定日期市场经济指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `field_list` | Y | List[str] | 字段筛选，不能为空 |
| `year` | Y | int | 指定年份 |
| `mmdd` | Y | int | 指定月日 |


## <a id="getstocklist"></a>`get_stock_list` 股票列表

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `market` | Y | str | 指定代码 |
| `list_type` | Y | int | 返回数据类型 |


## <a id="getsectorlist"></a>`get_sector_list` 板块列表

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `list_type` | Y | int | 返回数据类型 |


## <a id="getstocklistinsector"></a>`get_stock_list_in_sector` 板块成分股

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `block_code` | Y | str | 板块代码 |
| `block_type` | N | str | 板块类型 |
| `list_type` | Y | int | 返回数据类型 |


## <a id="senduserblock"></a>`send_user_block` 自选/板块写入

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `block_code` | Y | str | 自定义板块简称 |
| `stock_list` | Y | List[str] | 添加的自选股 |
| `show` | N | bool | 客户端是否切换至对应板块界面 |
| `block_code` | Y | str | 自定义板块简称 |
| `block_code` | Y | str | 自定义板块简称 |
| `block_name` | Y | str | 自定义板块名称 |
| `block_code` | Y | str | 自定义板块简称 |
| `block_code` | Y | str | 自定义板块简称 |
| `block_name` | Y | str | 重命名后的自定义板块名称 |


## <a id="stockaccount"></a>`stock_account` 获取资金账户句柄

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account` | Y | str | 资金账号 |
| `account_type` | Y | str | 账号类型 |


## <a id="querystockasset"></a>`query_stock_asset` 查询账户资产

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account_id` | Y | int | 资金账号句柄 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Currency` | Y | str | 币种 |
| `Balance` | Y | str | 余额 |
| `Cash` | Y | str | 可用余额 |
| `Asset` | Y | str | 资产 |
| `MarketValue` | Y | str | 总市值 |
| `TotalFreeze` | Y | str | 期货冻结资金 |
| `CloseProfit` | Y | str | 期货平仓盈亏 |
| `CurrentEquity` | Y | str | 期货动态权益 |
| `PreviousEquity` | Y | str | 期货静态权益 |
| `ProfitLoss` | Y | str | 期货持仓盈亏 |
| `TotalMargin` | Y | str | 期货持仓保证金 |


## <a id="querystockorders"></a>`query_stock_orders` 查询委托

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account_id` | Y | int | 资金账号句柄 |
| `stock_code` | Y | str | 证券代码 |
| `cancelable_only` | Y | str | 是否仅查询可撤委托（暂未生效） |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Wtbh` | Y | str | 委托编号 |
| `Code` | Y | str | 股票代码 |
| `Time` | Y | str | 时间，HHMMSS |
| `BSFlag` | Y | int | 买卖标志,0买 1卖 -1撤单 |
| `KPFlag` | Y | int | 开平标志，0开仓1平仓2平今 |
| `WTFS` | Y | str | 市价方式，根据沪深市场不一样 |
| `Status` | Y | int | 委托状态 |
| `WtDate` | Y | int | 撤单标志，为1表示已撤,为2表示是夜盘单 |
| `CjPric` | Y | str | 成交价 |
| `CJVol` | Y | str | 成交数量 如果是撤,则为负值 |
| `WtPrice` | Y | str | 委托价 |
| `WtVol` | Y | str | 委托数量 如果是撤,则为负值 |


## <a id="querystockpositions"></a>`query_stock_positions` 查询持仓

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account_id` | Y | int | 资金账号句柄 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Code` | Y | str | 证券代码 |
| `Cbj` | Y | str | 成本价 |
| `TotalVol` | Y | str | 总持仓 |
| `CanUseVol` | Y | str | 可用持仓 |
| `BuyPosition` | Y | str | 多头持仓（期货或期权） |
| `BuyAvgPrice` | Y | str | 多头持仓均价（期货或期权） |
| `BuyProfitLoss` | Y | str | 多头持仓盈亏（期货或期权） |
| `SellPosition` | Y | str | 空头持仓（期货或期权） |
| `SellAvgPrice` | Y | str | 空头持仓均价（期货或期权） |
| `SellProfitLoss` | Y | str | 空头持仓盈亏（期货或期权） |
| `TodayBuyPosition` | Y | str | 当日买入持仓（期货或期权） |
| `TodaySellPosition` | Y | str | 当日卖出持仓（期货或期权） |


## <a id="orderstock"></a>`order_stock` 下单

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account_id` | Y | int | 资金账号句柄 |
| `stock_code` | Y | str | 证券代码 |
| `order_type` | Y | int | 委托类型 |
| `order_volume` | Y | int | 委托数量 |
| `price_type` | Y | int | 报价类型 |
| `price` | Y | float | 委托价格 |
| `notify` | Y | int | 是否手动确认 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Value` | Y | int | 成功标志，0失败，1待用户确认，2成功 |
| `Wtbh` | Y | str | 委托编号，只有成功时才会返回 |
| `Msg` | Y | str | 返回提示信息 |


## <a id="cancelorderstock"></a>`cancel_order_stock` 撤单

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `account_id` | Y | int | 资金账号句柄 |
| `stock_code` | Y | str | 证券代码 |
| `order_id` | Y | int | 委托编号 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `Value` | Y | int | 成功标志，0失败，1成功 |
| `Msg` | Y | str | 返回提示信息 |


## <a id="sendmessage"></a>`send_message` 发送消息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `msg_str` | Y | str | 消息字符串 |


## <a id="sendwarn"></a>`send_warn` 发送预警

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表 |
| `time_list` | Y | List[str] | 时间列表 |
| `price_list` | N | List[str] | 现价列表 |
| `close_list` | N | List[str] | 收盘价列表 |
| `volum_list` | N | List[str] | 成交额列表 |
| `bs_flag_list` | N | List[str] | 买卖标志：0买1卖2未知 |
| `warn_type_list` | N | List[str] | 预警类型：0常规预警（目前仅支 持） |
| `reason_list` | N | List[str] | 预警原因 |
| `count` | N | int | 有效数据个数 |


## <a id="sendfile"></a>`send_file` 发送文件

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `file` | Y | str | 文件路径 |


## <a id="sendbtdata"></a>`send_bt_data` 回测数据

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | List[str] | 证券代码 |
| `time_list` | Y | List[str] | 时间列表 |
| `data_list` | N | List[List[str]] | 回测数据列表 |
| `count` | N | int | 有效数据个数 |
| `stock_code` | Y | List[str] | 证券代码 |
| `down_time` | Y | List[str] | 指定日期 |
| `down_type` | Y | List[str] | 指定下载类型 |


## <a id="refreshcache"></a>`refresh_cache` 刷新缓存

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `force` | Y | bool | 是否强制刷新 |
| `market` | Y | str | 指定刷新的市场 |


## <a id="refreshkline"></a>`refresh_kline` 刷新K线

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_list` | Y | List[str] | 证券代码列表，证券代码格式为6 位数+市场后缀（.SH/.SZ/.BJ等） |
| `period` | Y | str | 周期 1d为日线、1m为一分钟线、 5m为五分钟线，只支持这三种， 其它周期的数据均由这三种数据生 成 |


## <a id="exectotdx"></a>`exec_to_tdx` 执行到客户端

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `url` | Y | str | 功能调用串或网址 |


## <a id="formulagetall"></a>`formula_get_all` 公式列表

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `formula_type` | Y | int | 公式种类标识 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `acCode` | Y | str | 公式代码 |
| `acName` | Y | str | 公式名称 |
| `isSys` | Y | int | 是否为系统公式 |


## <a id="formulagetinfo"></a>`formula_get_info` 公式信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `formula_type` | Y | int | 公式种类标识 |
| `formula_code` | Y | int | 公式代码 |

**返回字段**

| 字段 | 默认返回 | 类型 | 说明 |
|---|---|---|---|
| `acCode` | Y | str | 公式代码 |
| `acName` | Y | str | 公式名称 |
| `isSys` | Y | int | 是否为系统公式 |
| `ParaNum` | Y | int | 入参数量 |
| `Para` | Y | Set | 公式入参参数 |
| `ParaName` | Y | Set | 公式入参名称 |
| `Min` | Y | Set | 公式入参最小值 |
| `Max` | Y | Set | 公式入参最大值 |
| `Default` | Y | Set | 公式入参默认值 |
| `LineNum` | Y | int | 出参数量 |
| `Line` | Y | Set | 公式出参参数 |
| `LineName` | Y | Set | 公式出参名称 |


## <a id="formulaformatdata"></a>`formula_format_data` 公式格式化

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `data_dict` | Y | Dict | get market data获取格式的K线Dict _ _ |


## <a id="formulasetdata"></a>`formula_set_data` 公式写数据

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |
| `stock_period` | Y | str | K线周期 |
| `stock_data` | Y | List | 指定格式的K线数据 |
| `count` | Y | int | 选取的K线数量 |
| `dividend_type` | Y | int | 复权类型 |


## <a id="formulasetdatainfo"></a>`formula_set_data_info` 公式数据信息

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `stock_code` | Y | str | 股票代码 |
| `stock_period` | Y | str | K线周期 |
| `start_time` | Y | str | 起始时间 |
| `end_time` | Y | str | 结束时间 |
| `count` | Y | int | 截取K线数量 |
| `dividend_type` | Y | int | 复权类型 |


## <a id="formulazb"></a>`formula_zb` 公式指标

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `formula_name` | Y | str | 公式名称 |
| `formula_arg` | Y | str | 公式参数 |
| `xsflag` | Y | int | 数据精度 |


## <a id="formulaprocessmulzb"></a>`formula_process_mul_zb` 批量指标计算

**入参**

| 参数 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `formula_name` | Y | str | 公式名称 |
| `formula_arg` | Y | str | 公式参数 |
| `xsflag` | Y | int | 数据精度 |
| `retrun_count` | Y | int | 设置每个返回值的返回数 |
| `formula_arg` | Y | bool | 设置是否返回日期 |
| `stock_list` | Y | List[str] | 股票代码列表 |
| `stock_period` | Y | str | K线周期 |
| `start_time` | Y | str | 起始时间 |
| `end_time` | Y | str | 结束时间 |
| `count` | Y | int | 截取K线数量 |
| `dividend_type` | Y | int | 复权类型 |


## <a id="常量枚举"></a>`常量枚举` 常量枚举(市场/交易/委托状态)

**返回字段**

| 字段 | 类型 | 取值 | 说明 |
|---|---|---|---|
| `.SZ` | int | 0 | 深圳交易所 |
| `.SH` | int | 1 | 上海交易所 |
| `.BJ` | int | 2 | 北京交易所 |
| `.NQ` | int | 44 | 新三板 |
| `.SHO` | int | 8 | 上海个股期权 |
| `.SZO` | int | 9 | 深圳个股期权 |
| `.HK` | int | 31 | 香港交易所 |
| `.US` | int | 74 | 美国股票 |
| `.CSI` | int | 62 | 中证指数 |
| `.CNI` | int | 102 | 国证指数 |
| `.HG` | int | 38 | 国内宏观指标 |
| `.CFF` | int | 47 | 中金期货 |
| `.CZC` | int | 28 | 郑州期货 |
| `.DCE` | int | 29 | 大连期货 |
| `.SHF` | int | 30 | 上海期货 |
| `.GFE` | int | 66 | 广州期货 |
| `.INE` | int | 30 | 上海能源 |
| `.HI` | int | 27 | 港股指数 |
| `.OF` | int | 33 | 开放式基金净值 |
| `.CFFO` | int | 7 | 中金所期权 |
| `.CZCO` | int | 4 | 郑州期货期权 |
| `.DCEO` | int | 5 | 大连期货期权 |
| `.SHFO` | int | 6 | 上海期货期权 |
| `.GFEO` | int | 67 | 广州期货期权 |
| `.QHZ` | int | 42 | 期货类指数 |
| `type` | str | none | 不复权 |
| `type` | str | front | 前复权 |
| `type` | str | back | 后复权 |
| `period` | str | 1m | 1分钟 |
| `period` | str | 5m | 5分钟 |
| `period` | str | 15m | 15分钟 |
| `period` | str | 30m | 30分钟 |
| `period` | str | 1h | 60分钟（1小时） |
| `period` | str | 1d | 1天 |
| `period` | str | 1w | 1周 |
| `period` | str | 1mon | 1月 |
| `period` | str | 1q | 1季 |
| `period` | str | 1y | 1年 |
| `period` | str | tick | 分笔 |
| `STOCK_BUY` | int | 0 | 买 |
| `STOCK_SELL` | int | 1 | 卖 |
| `CREDIT_BUY` | int | 0 | 担保品买入 |
| `CREDIT_SELL` | int | 1 | 担保品卖出 |
| `CREDIT_FIN_BUY` | int | 69 | 融资买入 |
| `CREDIT_SLO_SELL` | int | 70 | 融券卖出 |
| `CREDIT_COV_BUY` | int | 71 | 买券还券 |
| `CREDIT_STK_REPAY` | int | 76 | 卖券还款 |
| `ETF_PURCHASE` | int | 45 | 基金申购 |
| `ETF_REDEMPTION` | int | 46 | 基金赎回 |
| `FUTURE_OPEN_LONG` | int | 101 | 期货开多 |
| `FUTURE_OPEN_SHORT` | int | 102 | 期货开空 |
| `FUTURE_CLOSE_LONG` | int | 103 | 期货平多 |
| `FUTURE_CLOSE_SHORT` | int | 104 | 期货平空 |
| `OPTION_OPEN_LONG` | int | 201 | 期权开多 |
| `OPTION_OPEN_SHORT` | int | 202 | 期权开空 |
| `OPTION_CLOSE_LONG` | int | 203 | 期权平多 |
| `OPTION_CLOSE_SHORT` | int | 204 | 期权平空 |
| `PRICE_MY` | int | 0 | 自填价 |
| `PRICE_SJ` | int | 1 | 市价 |
| `PRICE_ZTJ` | int | 2 | 涨停价/笼子上限 |
| `PRICE_DTJ` | int | 3 | 跌停价/笼子下限 |
| `WTSTATUS_NULL` | int | 0 | 无效单 |
| `WTSTATUS_NOCJ` | int | 1 | 未成交 |
| `WTSTATUS_PARTCJ` | int | 2 | 部分成交 |
| `WTSTATUS_ALLCJ` | int | 3 | 全部成交 |
| `WTSTATUS_BCBC` | int | 4 | 部分成交部分撤单 |
| `WTSTATUS_ALLCD` | int | 5 | 全部撤单 |
