# WindPy 字段手册（实测可用）

> 共 **5301 个字段**,**经 WindPy `wss` 真机逐字段批量验证认可**(Wind 字典层 `-40522006 invalid indicators` 是纯字段名级校验,与品种无关)。**本表字段代码可直接用于 `/wind/wsd`、`/wind/wss`**,是三套 Wind 字段口径里唯一「拿来即用」的那套。

> 🔴 **三套 Wind 字段口径区别(必读)**:
>
> | 口径 | 字段数 | 命名样例 | 用途 | 文件 |
> |---|---|---|---|---|
> | **WindPy 实测(本表)** | 5301 | `close`/`pe_ttm`/`roe` | **可直接喂 `/wind/wss`** | `windpy_fields.csv` |
> | Excel 插件(xla) | 9689 | `s_dq_close`/`s_val_pe` | 查中文名/找指标,**不能直接喂 wss** | `xla_fields.csv` / `Wind指标字段手册.md` |
> | 探测子集(早期) | 130 | `close`/`open` | 已并入本表 | `probed_fields.csv` |
>
> 本表由 xla 9689 码生成「原码 + 去 1 段前缀 + 去 2 段前缀」候选变体(25683 个),批量喂 wss、二分定位,留下 5301 个被 Wind 字典认可的名。中文名取生成该名的最短源 xla 码的中文名。

> ⚠ **口径残余风险**:去前缀变体的中文名来自 xla 源码,极少数「去前缀后撞名」的字段,其中文名可能与该 WindPy 名的真实语义略有出入;基础高频字段(行情/估值/财务)已交叉核对无误。生成脚本 `scripts/catalog/wind_verify_xla_fields.py`、`gen_md_windpy.py`。


## 总览

| 分类 | 字段数 | 跳转 |
|---|---|---|
| 可转债 | 17 | [↓](#分类-可转债) |
| ABS资产证券化 | 88 | [↓](#分类-ABS资产证券化) |
| 基金 | 5 | [↓](#分类-基金) |
| 基金净值 | 25 | [↓](#分类-基金净值) |
| 基金(专项) | 4 | [↓](#分类-基金专项) |
| 新股发行 | 237 | [↓](#分类-新股发行) |
| 分红 | 68 | [↓](#分类-分红) |
| 盈利预测 | 142 | [↓](#分类-盈利预测) |
| 一致预期 | 237 | [↓](#分类-一致预期) |
| ESG | 109 | [↓](#分类-ESG) |
| 股东 | 71 | [↓](#分类-股东) |
| 股本 | 86 | [↓](#分类-股本) |
| 货币基金 | 13 | [↓](#分类-货币基金) |
| 发行 | 37 | [↓](#分类-发行) |
| 利率/评级 | 23 | [↓](#分类-利率-评级) |
| 收益率 | 5 | [↓](#分类-收益率) |
| 融资融券 | 11 | [↓](#分类-融资融券) |
| 财务分析 | 90 | [↓](#分类-财务分析) |
| 单季财务 | 37 | [↓](#分类-单季财务) |
| 技术指标 | 4 | [↓](#分类-技术指标) |
| 风险指标 | 86 | [↓](#分类-风险指标) |
| 估值 | 51 | [↓](#分类-估值) |
| 交易 | 2 | [↓](#分类-交易) |
| 证券基础 | 4 | [↓](#分类-证券基础) |
| 回购 | 1 | [↓](#分类-回购) |
| 通用/行情/其他 | 3848 | [↓](#分类-通用-行情-其他) |

**合计 5301 个字段,26 个分类。**


<a id="分类-可转债"></a>

## 可转债（17 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `cb_issueamount` | 转债发行总额 |  | xla去前缀变体 |
| `cb_list_annocedate` | 转债发行结果公告日 |  | xla去前缀变体 |
| `cb_list_dateinstoff` | 转债网下向机构投资者发行日期 |  | xla去前缀变体 |
| `cb_list_dtonl` | 转债网上发行日期 |  | xla去前缀变体 |
| `cb_list_issuevolonl` | 网上发行数量(不含优先配售) |  | xla原码 |
| `cb_list_permitdate` | 转债发审委审批通过日期 |  | xla去前缀变体 |
| `cb_list_rationchkindate` | 转债老股东配售股权登记日 |  | xla去前缀变体 |
| `cb_list_rationdate` | 转债老股东配售日期 |  | xla去前缀变体 |
| `cb_list_rationpaymtdate` | 转债老股东配售缴款日 |  | xla去前缀变体 |
| `cb_list_rationvol` | 向老股东配售数量 |  | xla原码 |
| `cb_list_volinstoff` | 网下向机构投资者发行数量(不含优先配售) |  | xla原码 |
| `cb_pq_highclose` | 区间最高收盘价 | StartDate、EndDate | xla原码 |
| `cb_pq_lowclose` | 区间最低收盘价 | StartDate、EndDate | xla原码 |
| `cb_pq_stockavg` | 正股区间均价(新增) | TD1、TD2 | xla原码 |
| `cb_pq_stockchg` | 正股区间涨跌(新增) | TD1、TD2 | xla原码 |
| `cb_pq_stockpctchg` | 正股区间涨跌幅(新增) | TD1、TD2 | xla原码 |
| `cb_pq_swing` | 区间振幅 | StartDate、EndDate、PRICETYPE | xla原码 |

<a id="分类-ABS资产证券化"></a>

## ABS资产证券化（88 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `abs_12mavgdefaultrate` | 年化违约率(12月平均) | DEALDATE | xla去前缀变体 |
| `abs_12mavgprepayrate` | 年化早偿率(12月平均) | DEALDATE | xla去前缀变体 |
| `abs_actualrecoveryrate` | 不良ABS实际回收比率 | DEALDATE | xla去前缀变体 |
| `abs_agency_custodian` | 资金保管机构 |  | xla去前缀变体 |
| `abs_agency_trustee1` | 受托机构 |  | xla去前缀变体 |
| `abs_annualdefaultrate` | 年化违约率(单月年化) | DEALDATE | xla去前缀变体 |
| `abs_annualprepayrate` | 年化早偿率 | DEALDATE | xla去前缀变体 |
| `abs_assetserviceagency` | 资产服务机构 |  | xla去前缀变体 |
| `abs_borrower` | 基础债务人 |  | xla去前缀变体 |
| `abs_capyieldpertermofsub` | 次级每期收益率上限 |  | xla去前缀变体 |
| `abs_cdr_cbr` | ABS累计违约率(中债资信) | TRADEDATE | xla去前缀变体 |
| `abs_clrprchs` | 清仓回购条款 |  | xla去前缀变体 |
| `abs_codebtors` | 共同债务人 |  | xla去前缀变体 |
| `abs_collectionenddate` | 资产池归集时间 |  | xla去前缀变体 |
| `abs_compassetsrecovrate` | 不良ABS处置完毕资产回收率 | DEALDATE | xla去前缀变体 |
| `abs_coreindustry` | 基础债务人行业 |  | xla去前缀变体 |
| `abs_coreproperty` | 基础债务人性质 |  | xla去前缀变体 |
| `abs_coreprovince` | 基础债务人地区 |  | xla去前缀变体 |
| `abs_creditnormal` | 承销团成员 |  | xla去前缀变体 |
| `abs_creditsupport` | 信用支持 | DEALDATE | xla去前缀变体 |
| `abs_cumdefaultrate` | 累计违约率 | DEALDATE | xla去前缀变体 |
| `abs_cumulativedefaultrate` | 累计违约率 |  | xla去前缀变体 |
| `abs_currentloan` | 当前贷款笔数 |  | xla去前缀变体 |
| `abs_currentloans` | 当前贷款余额 |  | xla去前缀变体 |
| `abs_currentwarm` | 当前加权平均贷款剩余期限 |  | xla去前缀变体 |
| `abs_currentwtgavgrate` | 当前加权平均贷款利率 |  | xla去前缀变体 |
| `abs_cutoffdate` | 初始起算日 |  | xla去前缀变体 |
| `abs_dealbalance` | 项目发行规模 |  | xla去前缀变体 |
| `abs_dealout` | 项目存量规模 | DEALDATE | xla去前缀变体 |
| `abs_dealoutststandingamount` | 项目余额 | DEALDATE | xla去前缀变体 |
| `abs_defiguarantor` | 差额支付承诺人 |  | xla去前缀变体 |
| `abs_delinquencyrate` | 严重拖欠率 |  | xla去前缀变体 |
| `abs_delinquencyrate2` | 严重拖欠率 | DEALDATE | xla去前缀变体 |
| `abs_endborrower` | 期末剩余资产池借款人户数 | DEALDATE | xla去前缀变体 |
| `abs_enddateofassetclearing` | 清算结束日 |  | xla去前缀变体 |
| `abs_endnplbal` | 不良ABS期末本息余额 | DEALDATE | xla去前缀变体 |
| `abs_endpoolbalance` | 期末剩余资产池余额 | DEALDATE | xla去前缀变体 |
| `abs_endpoolnumber` | 期末剩余资产池笔数 | DEALDATE | xla去前缀变体 |
| `abs_endweightedaveragelife` | 期末资产池剩余期限 | DEALDATE | xla去前缀变体 |
| `abs_endweightedaveragerate` | 期末资产池加权平均利率 | DEALDATE | xla去前缀变体 |
| `abs_expectedmaturitywithprepay` | 早偿预期到期日 |  | xla去前缀变体 |
| `abs_expectrecoveramount` | 预计可回收金额 |  | xla去前缀变体 |
| `abs_expectrecoveryrate` | 不良ABS预期回收比率 | DEALDATE | xla去前缀变体 |
| `abs_expreconasset` | 不良ABS预期回收比率(占入池资产总额比) | DEALDATE | xla去前缀变体 |
| `abs_fiexdcapitalcostrate` | 固定资金成本 |  | xla去前缀变体 |
| `abs_finaladjdur` | 证券最终修正久期 |  | xla去前缀变体 |
| `abs_finalyiled` | 证券最终收益率 |  | xla去前缀变体 |
| `abs_firstpaymentdate` | 首次支付日 |  | xla去前缀变体 |
| `abs_fullnamepro` | 项目名称 |  | xla去前缀变体 |
| `abs_guarassetpool` | 担保人(对资产池) |  | xla去前缀变体 |
| `abs_industry` | 主体行业 |  | xla去前缀变体 |
| `abs_industry1` | 主体性质 |  | xla去前缀变体 |
| `abs_initialpoolbalance` | 初始资产池金额统计 | AMTTYPE | xla去前缀变体 |
| `abs_initialpoollife` | 初始资产池期限统计 | AMTTYPE | xla去前缀变体 |
| `abs_initialpoolnumber` | 初始资产池数量统计 | AMTTYPE | xla去前缀变体 |
| `abs_initialpoolrate` | 初始资产池利率统计 | AMTTYPE | xla去前缀变体 |
| `abs_issueprop` | 发行分层占比 | DEALDATE | xla去前缀变体 |
| `abs_legalmaturity` | 法定到期日 |  | xla去前缀变体 |
| `abs_liquiditysup` | 流动性支持承诺人(对资产池) |  | xla去前缀变体 |
| `abs_liquiguarantor` | 流动性支持承诺人 |  | xla去前缀变体 |
| `abs_namepro` | 项目简称 |  | xla去前缀变体 |
| `abs_nplcurpirecamt` | 不良ABS本期间本息回收金额 | DEALDATE | xla去前缀变体 |
| `abs_payback` | 还本方式 |  | xla去前缀变体 |
| `abs_paymentdate` | 支付日 |  | xla去前缀变体 |
| `abs_penetrateactrualdebtor` | 穿透信用主体 |  | xla去前缀变体 |
| `abs_penetrateactrualdebtor_abbr` | 穿透信用主体中文简称 |  | xla去前缀变体 |
| `abs_periodprepayrate` | 期间早偿率 | DEALDATE | xla去前缀变体 |
| `abs_prepayrate_cbr` | ABS早偿率预测(中债资信) | TRADEDATE、FN | xla去前缀变体 |
| `abs_principalbasis_cbr` | ABS本金因子(中债资信) | TRADEDATE | xla去前缀变体 |
| `abs_prinfinaldate` | 本金最终兑付日 |  | xla去前缀变体 |
| `abs_projectarrange` | 项目安排人 |  | xla去前缀变体 |
| `abs_projectcode` | 项目代码 |  | xla去前缀变体 |
| `abs_province` | 主体地区 |  | xla去前缀变体 |
| `abs_recommendcpr` | 早偿率 |  | xla去前缀变体 |
| `abs_recoverycash` | 不良AB期间合计本息回收金额 | DEALDATE | xla去前缀变体 |
| `abs_recoveryrate_cbr` | ABS回收率预测(中债资信) | TRADEDATE、FN | xla去前缀变体 |
| `abs_rectopool` | 不良ABS实际回收比率(占入池资产总额比) | DEALDATE | xla去前缀变体 |
| `abs_reinvestenddate` | 循环期截止日 |  | xla去前缀变体 |
| `abs_revstartdt` | 循环期起始日 |  | xla去前缀变体 |
| `abs_samepoolsize` | 同资产池发行规模 |  | xla去前缀变体 |
| `abs_selfsustainingproportion` | 自持比例 |  | xla去前缀变体 |
| `abs_shortfallpay` | 差额支付承诺人(对资产池) |  | xla去前缀变体 |
| `abs_spv` | 计划管理人 |  | xla去前缀变体 |
| `abs_startdateofassetclearing` | 清算起始日 |  | xla去前缀变体 |
| `abs_trustee` | 专项计划托管人 |  | xla去前缀变体 |
| `abs_underlyingtype` | ABS基础资产分类 | ABSType | xla去前缀变体 |
| `abs_wal_cbr` | ABS预计加权平均期限(中债资信) | TRADEDATE | xla去前缀变体 |
| `abs_weightedaveragematuritywithprepay` | 加权平均期限 | Cycle | xla去前缀变体 |

<a id="分类-基金"></a>

## 基金（5 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `fund_esg_tax_wind` | Wind ESG投资基金类型 |  | xla去前缀变体 |
| `fund_leveragemultiple` | 基金的杠杆倍数 |  | xla去前缀变体 |
| `fund_navcur` | 单位净值币种 |  | xla原码 |
| `fund_subshareproportion` | 分级份额占比 |  | xla原码 |
| `mf_netinflow` | 净流入额 | TRADEDATE | xla去前缀变体 |

<a id="分类-基金净值"></a>

## 基金净值（25 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `nav` | 期末基金份额净值 | REPORTDATE | xla去前缀变体 |
| `nav_accumulated_transform` | 累计单位净值(支持转型基金) | TRADEDATE | xla去前缀变体 |
| `nav_accumulated_transformnf` | 累计单位净值(支持转型基金,不前推) | TRADEDATE | xla去前缀变体 |
| `nav_adjfactor` | 基金净值复权因子 | TRADEDATE | xla去前缀变体 |
| `nav_adjusted_b` | 复权单位净值(前复权) | TRADEDATE | xla去前缀变体 |
| `nav_adjusted_transform` | 复权单位净值(支持转型基金) | TRADEDATE | xla去前缀变体 |
| `nav_adjusted_transformnf` | 复权单位净值(支持转型基金,不前推) | TRADEDATE | xla去前缀变体 |
| `nav_benchdevreturn` | 报告期净值增长率减基准增长率(新增) | D | xla去前缀变体 |
| `nav_benchreturn` | 报告期业绩比较基准增长率(新增) | D | xla去前缀变体 |
| `nav_benchstddev` | 报告期业绩比较基准增长率标准差(新增) | D | xla去前缀变体 |
| `nav_date` | 基金净值日期 |  | xla去前缀变体 |
| `nav_date2` | 基金净值日期 | DEALDATE | xla去前缀变体 |
| `nav_exrightdate` | 最新净值除权日 | DEALDATE | xla去前缀变体 |
| `nav_firstdate` | 净值披露首日 |  | xla去前缀变体 |
| `nav_iopv_discountratio` | IOPV溢折率 | TRADEDATE | xla去前缀变体 |
| `nav_publishtype` | 基金净值公布类型 |  | xla去前缀变体 |
| `nav_ranking_p` | 同类基金区间收益排名P值 | StartDate、EndDate | xla去前缀变体 |
| `nav_return` | 报告期净值增长率(新增) | D | xla去前缀变体 |
| `nav_sellprice` | 投连险卖出价 | DATE | xla去前缀变体 |
| `nav_stddevnavbench` | 报告期净值增长率标准差减基准标准差(新增) | D | xla去前缀变体 |
| `nav_stddevreturn` | 报告期净值增长率标准差(新增) | D | xla去前缀变体 |
| `nav_unit_transform` | 单位净值(支持转型基金) | TRADEDATE | xla去前缀变体 |
| `nav_updatecompleteness` | 基金净值完整度 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `nav_updatefrequency` | 基金净值更新频率 |  | xla去前缀变体 |
| `nav_winlossratio` | 基金盈利概率 | StartDate、EndDate、CalcTerm | xla去前缀变体 |

<a id="分类-基金专项"></a>

## 基金(专项)（4 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `fs_pq_change_settlement` | 区间涨跌（结算价） | BEGINDATE、EndDate | xla原码 |
| `fs_pq_highswing_date` | 区间最高结算价日 | BEGINDATE、EndDate | xla原码 |
| `fs_pq_lowswing_date` | 区间最低结算价日 | BEGINDATE、EndDate | xla原码 |
| `fs_pq_pctchange_settlement` | 区间涨跌幅（结算价） | BEGINDATE、EndDate | xla原码 |

<a id="分类-新股发行"></a>

## 新股发行（237 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `ipo_acpdt` | 证监会接收境外发行材料日期 |  | xla去前缀变体 |
| `ipo_allotmentsubjects` | 配售对象名称(新增) | InstitutionType、TYPE | xla去前缀变体 |
| `ipo_allotway` | 网下投资者分类配售方式 |  | xla去前缀变体 |
| `ipo_amount` | 首发数量 |  | xla去前缀变体 |
| `ipo_amount_est` | 预计发行股数 |  | xla去前缀变体 |
| `ipo_amttoinstinvestor` | 向战略投资者配售数量(新增) |  | xla去前缀变体 |
| `ipo_amttojur` | 向一般法人配售数量(新增) |  | xla去前缀变体 |
| `ipo_amttoother` | 其它发行数量(新增) |  | xla去前缀变体 |
| `ipo_anncedate` | 发行公告日(新增) |  | xla去前缀变体 |
| `ipo_anncelstdate` | 上市公告日 |  | xla去前缀变体 |
| `ipo_applicationdeadline` | 网下投资者报备截止日 |  | xla去前缀变体 |
| `ipo_applicationdeadline_time` | 网下投资者报备截止时间 |  | xla去前缀变体 |
| `ipo_apprtoreg` | 是否核准制平移至注册制 |  | xla去前缀变体 |
| `ipo_assetdate` | 新股申购资产规模报备日 |  | xla去前缀变体 |
| `ipo_assetdate_lstmon` | 新股申购资产规模报备日(最近一个月末) |  | xla去前缀变体 |
| `ipo_audit_cpa` | 首发签字会计师 |  | xla去前缀变体 |
| `ipo_auditfee` | 首发审计费用 |  | xla去前缀变体 |
| `ipo_auditor` | 首发审计机构 |  | xla去前缀变体 |
| `ipo_avgprice` | 上市首日成交均价(新增) |  | xla去前缀变体 |
| `ipo_backmechanism` | 是否触发回拨机制 |  | xla去前缀变体 |
| `ipo_bank` | 首发收款银行 |  | xla去前缀变体 |
| `ipo_beyondactualcollec` | 首发超募资金(新增) |  | xla去前缀变体 |
| `ipo_bfund` | 网上冻结资金 |  | xla去前缀变体 |
| `ipo_cappaydate` | 网上申购缴款日 |  | xla去前缀变体 |
| `ipo_cashamt` | 现金申购发行数量(新增) |  | xla去前缀变体 |
| `ipo_casheffacc` | 现金申购有效申购户数(新增) |  | xla去前缀变体 |
| `ipo_cashratio` | 现金申购中签率(新增) |  | xla去前缀变体 |
| `ipo_close` | 上市首日收盘价 |  | xla去前缀变体 |
| `ipo_collection` | 首发募集资金 |  | xla去前缀变体 |
| `ipo_collection_acct` | 首发募集资金监管银行账户 |  | xla去前缀变体 |
| `ipo_collection_bal` | 募集资金专项账户余额 | TRADEDATE | xla去前缀变体 |
| `ipo_collection_bank` | 首发募集资金监管银行名称 |  | xla去前缀变体 |
| `ipo_collection_oldshares` | 股东售股金额 |  | xla去前缀变体 |
| `ipo_collection_total` | 募集资金总额(含股东售股) |  | xla去前缀变体 |
| `ipo_collection_unused` | 首发未投入资金金额 |  | xla去前缀变体 |
| `ipo_commissionrate` | 新股配售经纪佣金费率 |  | xla去前缀变体 |
| `ipo_comppe_deducted` | 可比上市公司PE均值(扣非后) |  | xla去前缀变体 |
| `ipo_date` | 上市日期 |  | 探测法实测 |
| `ipo_deputyundr` | 副主承销商(新增) |  | xla去前缀变体 |
| `ipo_dilutedpe` | 首发市盈率(摊薄)(新增) |  | xla去前缀变体 |
| `ipo_distor` | 首发分销商(新增) |  | xla去前缀变体 |
| `ipo_draftsprospectusdate` | IPO申报稿首次报送时间 |  | xla去前缀变体 |
| `ipo_dtooratio_pl` | 申购一手中签率 |  | xla去前缀变体 |
| `ipo_expectedcollection` | 首发预计募集资金(新增) |  | xla去前缀变体 |
| `ipo_expectednetcollection` | 首发预计募集资金净额 |  | xla去前缀变体 |
| `ipo_expense` | 首发发行费用 |  | xla去前缀变体 |
| `ipo_feedbackdate` | IPO首次反馈日期 |  | xla去前缀变体 |
| `ipo_findt` | 证监会境外发行备案日期 |  | xla去前缀变体 |
| `ipo_firstinquirydate` | IPO首次问询日期 |  | xla去前缀变体 |
| `ipo_firstmrqdate` | 初始申报基准日 |  | xla去前缀变体 |
| `ipo_giveup` | 网上放弃认购数量 |  | xla去前缀变体 |
| `ipo_greenshoe` | 是否行使超额配售权 |  | xla去前缀变体 |
| `ipo_handlingdate` | IPO受理日期 |  | xla去前缀变体 |
| `ipo_handlingdate_s` | IPO首次受理日期 |  | xla去前缀变体 |
| `ipo_hearingdate` | 聆讯日期 |  | xla去前缀变体 |
| `ipo_high` | 上市首日最高价(新增) |  | xla去前缀变体 |
| `ipo_idc` | 首发信息披露费 |  | xla去前缀变体 |
| `ipo_iecresultdate` | IPO发审委审核通过公告日期 |  | xla去前缀变体 |
| `ipo_industrycons` | 首发行业顾问 |  | xla去前缀变体 |
| `ipo_industrype` | 首发时所属行业市盈率 |  | xla去前缀变体 |
| `ipo_initialexpense` | 初始发行费用 |  | xla去前缀变体 |
| `ipo_inq_anncedate` | 初步询价公告日 |  | xla去前缀变体 |
| `ipo_inq_enddate` | 初步询价截止日 |  | xla去前缀变体 |
| `ipo_inq_startdate` | 初步询价起始日 |  | xla去前缀变体 |
| `ipo_inqresultdate` | 初步询价结果公告日 |  | xla去前缀变体 |
| `ipo_inquiriesnum` | IPO问询次数 |  | xla去前缀变体 |
| `ipo_inquiry` | 初步询价参与询价总家数(新增) |  | xla去前缀变体 |
| `ipo_inquiry_excl` | 剔除无效和最高报价后询价对象家数 |  | xla去前缀变体 |
| `ipo_inquiry_inst` | 初步询价参与询价机构家数(新增) |  | xla去前缀变体 |
| `ipo_inquirydate_new` | IPO问询日期(最新轮次) |  | xla去前缀变体 |
| `ipo_inquirymv_caldate` | 询价市值计算参考日 |  | xla去前缀变体 |
| `ipo_inquirymv_min` | 网下询价市值门槛 |  | xla去前缀变体 |
| `ipo_inquirymv_min_a` | 网下询价市值门槛(A类) |  | xla去前缀变体 |
| `ipo_inquirymv_min_themestrt` | 网下询价市值门槛(主题与战略) |  | xla去前缀变体 |
| `ipo_instisdate` | 向战略投资者配售部分上市日期(新增) |  | xla去前缀变体 |
| `ipo_intercordtor` | 首发国际协调人(新增) |  | xla去前缀变体 |
| `ipo_intsubratio` | 国际发行有效申购倍数 |  | xla去前缀变体 |
| `ipo_intvsshares` | 国际发行有效申购数量 |  | xla去前缀变体 |
| `ipo_invention` | 发明专利个数 |  | xla去前缀变体 |
| `ipo_investamount` | 近三年研发投入累计额 |  | xla去前缀变体 |
| `ipo_investorrefunddate` | 投资者退款日期 |  | xla去前缀变体 |
| `ipo_invsshares_a` | 网下高于有效报价上限的申购量 |  | xla去前缀变体 |
| `ipo_invssharespct_a` | 网下高于有效报价上限的申购量比例 |  | xla去前缀变体 |
| `ipo_issuedate` | 首发发行日期(新增) |  | xla去前缀变体 |
| `ipo_issuingsystem` | 发行制度 |  | xla去前缀变体 |
| `ipo_issuvolplanned` | 计划发行总数 |  | xla去前缀变体 |
| `ipo_jurisdate` | 向一般法人配售上市日期(新增) |  | xla去前缀变体 |
| `ipo_lawer` | 首发经办律师 |  | xla去前缀变体 |
| `ipo_lawfee` | 首发法律费用 |  | xla去前缀变体 |
| `ipo_lawfirm` | 首发经办律所 |  | xla去前缀变体 |
| `ipo_leadundr` | 首发主承销商(新增) |  | xla去前缀变体 |
| `ipo_leadundr_n` | 主办券商(持续督导) |  | xla去前缀变体 |
| `ipo_leadundr_n1` | 主办券商(持续督导) | TRADEDATE | xla去前缀变体 |
| `ipo_legaladvisor` | 首发保荐人律师 |  | xla去前缀变体 |
| `ipo_legaladvisor_cmpy` | 首发发行人律师 |  | xla去前缀变体 |
| `ipo_limitupdays` | 新股未开板涨停板天数 |  | xla去前缀变体 |
| `ipo_limitupopendate` | 开板日 |  | xla去前缀变体 |
| `ipo_limitupopendate_avgprice` | 新股开板日成交均价 |  | xla去前缀变体 |
| `ipo_limitupopendate_close` | 新股开板日收盘价 |  | xla去前缀变体 |
| `ipo_limitupopendate_pctchange` | 新股开板日涨跌幅 |  | xla去前缀变体 |
| `ipo_liqdiscount` | 限售股流动性折扣 | TRADEDATE、RestrictedPeriod | xla去前缀变体 |
| `ipo_listdays` | 上市天数(新增) |  | xla去前缀变体 |
| `ipo_listdayvolume` | 上市首日成交量(新增) |  | xla去前缀变体 |
| `ipo_lotteryrate_abc` | 网下投资者中签率 | InstitutionType | xla去前缀变体 |
| `ipo_lotwinningnumber` | 询价机构获配数量(新增) | InstitutionType、TYPE | xla去前缀变体 |
| `ipo_low` | 上市首日最低价(新增) |  | xla去前缀变体 |
| `ipo_lstnum` | 首日上市数量(新增) |  | xla去前缀变体 |
| `ipo_marketmaker` | 做市商名称 | TRADEDATE | xla去前缀变体 |
| `ipo_medianprice` | 网下申报价格中位数 | InstitutionType | xla去前缀变体 |
| `ipo_minsubscription_pl` | 稳购1手最低申购股数 |  | xla去前缀变体 |
| `ipo_mrqdate` | 申报基准日 |  | xla去前缀变体 |
| `ipo_mvregdate` | 网上市值申购登记日 |  | xla去前缀变体 |
| `ipo_netcollection` | 首发实际募集资金 |  | xla去前缀变体 |
| `ipo_netcollection_est` | 预计募投项目投资总额 |  | xla去前缀变体 |
| `ipo_netcollection_ture` | 首发募集资金净额 |  | xla去前缀变体 |
| `ipo_newshares` | 新股发行数量 |  | xla去前缀变体 |
| `ipo_newshares_initial` | 新股初始发行数量 |  | xla去前缀变体 |
| `ipo_ninstitutional_abc` | 网下投资者获配家数 | InstitutionType | xla去前缀变体 |
| `ipo_nominator` | 首发上市推荐人(新增) |  | xla去前缀变体 |
| `ipo_nooa` | 网上发行获配户数 |  | xla去前缀变体 |
| `ipo_npctchange` | 上市后N日涨跌幅(新增) |  | xla去前缀变体 |
| `ipo_nturn` | 上市后N日换手率(新增) |  | xla去前缀变体 |
| `ipo_numoffplacements` | 网下配售数量 |  | xla去前缀变体 |
| `ipo_offsubpaydate` | 网下申购缴款日 |  | xla去前缀变体 |
| `ipo_oldshares` | 股东售股数量 |  | xla去前缀变体 |
| `ipo_oldsharesratio` | 老股转让比例 |  | xla去前缀变体 |
| `ipo_onsite` | IPO现场检查公告日期 |  | xla去前缀变体 |
| `ipo_op_amount` | 网下冻结资金 |  | xla去前缀变体 |
| `ipo_op_downlimit` | 网下申购下限 |  | xla去前缀变体 |
| `ipo_op_enddate` | 网下申购截止日期 |  | xla去前缀变体 |
| `ipo_op_minofchg` | 最低累进申购数量 |  | xla去前缀变体 |
| `ipo_op_numoffring` | 网下申购报价数量 |  | xla去前缀变体 |
| `ipo_op_numofinq` | 网下申购询价对象家数 |  | xla去前缀变体 |
| `ipo_op_numofpmt` | 网下申购配售对象家数 |  | xla去前缀变体 |
| `ipo_op_oversubratio` | 首发网下超额认购倍数 |  | xla去前缀变体 |
| `ipo_op_startdate` | 网下申购起始日期 |  | xla去前缀变体 |
| `ipo_op_uplimit` | 网下申购上限 |  | xla去前缀变体 |
| `ipo_op_volume` | 网下申购总量 |  | xla去前缀变体 |
| `ipo_op_volume_abc` | 网下投资者申购数量 | InstitutionType | xla去前缀变体 |
| `ipo_open` | 上市首日开盘价 |  | xla去前缀变体 |
| `ipo_or_startdate` | 网下报备起始日 |  | xla去前缀变体 |
| `ipo_otc_cash_pct` | 网下申购配售比例(新增) |  | xla去前缀变体 |
| `ipo_otherenddate` | 其它发行截止日期(新增) |  | xla去前缀变体 |
| `ipo_otherstartdate` | 其它发行起始日期(新增) |  | xla去前缀变体 |
| `ipo_overallot_prop_vol` | 拟超额配售数量 |  | xla去前缀变体 |
| `ipo_overallot_vol` | 超额配售数量 |  | xla去前缀变体 |
| `ipo_ovrsubratio` | 超额认购倍数(新增) |  | xla去前缀变体 |
| `ipo_par` | 发行时每股面值 |  | xla去前缀变体 |
| `ipo_pb` | 发行市净率 |  | xla去前缀变体 |
| `ipo_pb_overallotbf` | 发行市净率(超额配售前) |  | xla去前缀变体 |
| `ipo_pctchange` | 上市首日涨跌幅(新增) |  | xla去前缀变体 |
| `ipo_pdate` | 网下定价日 |  | xla去前缀变体 |
| `ipo_pebeforeoverallot` | 首发市盈率(超额配售前) |  | xla去前缀变体 |
| `ipo_placing_excl` | 剔除无效和最高报价后配售对象家数 |  | xla去前缀变体 |
| `ipo_placingdate` | 网下配售结果公告日 |  | xla去前缀变体 |
| `ipo_poc_offline` | 网下发行数量(回拨前) |  | xla去前缀变体 |
| `ipo_poc_online` | 网上发行数量(回拨前) |  | xla去前缀变体 |
| `ipo_posthearing` | 聆讯后资料公告日 |  | xla去前缀变体 |
| `ipo_preplacingdate` | 初步配售结果公告日 |  | xla去前缀变体 |
| `ipo_preprice` | 发行前均价 |  | xla去前缀变体 |
| `ipo_price` | 发行价 |  | 探测法实测 |
| `ipo_price2` | 首发价格 |  | xla去前缀变体 |
| `ipo_price_max` | 发行价格上限 |  | xla去前缀变体 |
| `ipo_price_min` | 发行价格下限(底价) |  | xla去前缀变体 |
| `ipo_pshare_restrictpct` | 网下投资者分类配售限售比例 |  | xla去前缀变体 |
| `ipo_pshares_abc` | 网下投资者获配数量 | InstitutionType | xla去前缀变体 |
| `ipo_pshares_if` | 网下保险资金获配数量 |  | xla去前缀变体 |
| `ipo_pshares_mf` | 网下公募基金获配数量 |  | xla去前缀变体 |
| `ipo_pshares_sp` | 网下企业年金获配数量 |  | xla去前缀变体 |
| `ipo_pshares_ssf` | 网下社保基金获配数量 |  | xla去前缀变体 |
| `ipo_psharespct_abc` | 网下投资者配售数量占比 | InstitutionType | xla去前缀变体 |
| `ipo_puboffrdate` | 招股公告日(新增) |  | xla去前缀变体 |
| `ipo_purchasecode` | 网上申购代码 |  | xla去前缀变体 |
| `ipo_qnum_inquiry` | IPO问询函中问题数量 |  | xla去前缀变体 |
| `ipo_rdperson` | 研发人员占比 |  | xla去前缀变体 |
| `ipo_reallocationpct` | 回拨比例 |  | xla去前缀变体 |
| `ipo_refunddate` | 网上申购款解冻日 |  | xla去前缀变体 |
| `ipo_regist_date` | 注册成功日 |  | xla去前缀变体 |
| `ipo_restrictedvalue` | 限售股价值 | TRADEDATE、RestrictedPeriod | xla去前缀变体 |
| `ipo_resultdate` | 首发发行结果公告日(新增) |  | xla去前缀变体 |
| `ipo_revenue` | 近一年营收额 |  | xla去前缀变体 |
| `ipo_revenuegrowth` | 近三年营收复合增长率 |  | xla去前缀变体 |
| `ipo_rsdate_e` | 现场推介截止日期 |  | xla去前缀变体 |
| `ipo_rsdate_s` | 现场推介起始日期 |  | xla去前缀变体 |
| `ipo_samt_uplimit` | 网上申购资金上限 |  | xla去前缀变体 |
| `ipo_sfee` | 首发保荐费用 |  | xla去前缀变体 |
| `ipo_siallotment` | 战略配售获配股份数 |  | xla去前缀变体 |
| `ipo_siallotmentratio` | 战略配售获配股份占比 |  | xla去前缀变体 |
| `ipo_sponsor` | 首发保荐机构 |  | xla去前缀变体 |
| `ipo_sponsor_member` | 首发保荐机构项目组成员 |  | xla去前缀变体 |
| `ipo_sponsorrepresentative` | 首发保荐人代表 |  | xla去前缀变体 |
| `ipo_sprice_max` | 初步询价上限 |  | xla去前缀变体 |
| `ipo_sprice_min` | 初步询价下限 |  | xla去前缀变体 |
| `ipo_sratio` | 初步询价申购倍数(回拨前) |  | xla去前缀变体 |
| `ipo_sshares_t` | 初步询价申购总量 |  | xla去前缀变体 |
| `ipo_sshares_uplimit` | 网上申购数量上限 |  | xla去前缀变体 |
| `ipo_stabilizingmanager` | 首发稳价人 |  | xla去前缀变体 |
| `ipo_starposi` | 科创属性评价标准 |  | xla去前缀变体 |
| `ipo_subbydistr` | 承销商认购余额(新增) |  | xla去前缀变体 |
| `ipo_submit_regist_date` | 提交注册日 |  | xla去前缀变体 |
| `ipo_subnum` | 公开发售申购人数 |  | xla去前缀变体 |
| `ipo_subnum_a` | 公开发售甲组申购人数 |  | xla去前缀变体 |
| `ipo_subnum_b` | 公开发售乙组申购人数 |  | xla去前缀变体 |
| `ipo_subratio` | 网上发行有效认购倍数 |  | xla去前缀变体 |
| `ipo_subscription_excl` | 剔除无效和最高报价后申购总量 |  | xla去前缀变体 |
| `ipo_subscriptionprice` | 初步询价申购价格量(新增) | InstitutionType、TYPE | xla去前缀变体 |
| `ipo_subscriptionshares` | 初步询价申购数量(新增) | InstitutionType、TYPE | xla去前缀变体 |
| `ipo_termdate` | IPO终止审查日期 |  | xla去前缀变体 |
| `ipo_totcapafterissue` | 首发后总股本(上市日)(新增) |  | xla去前缀变体 |
| `ipo_totcapafterissue_est` | 预计发行后总股本 |  | xla去前缀变体 |
| `ipo_totcapbeforeissue` | 首发前总股本(新增) |  | xla去前缀变体 |
| `ipo_tradedays` | 上市交易天数 | TRADEDATE | xla去前缀变体 |
| `ipo_turn` | 上市首日换手率(新增) |  | xla去前缀变体 |
| `ipo_tutor` | 挂牌企业上市辅导券商 |  | xla去前缀变体 |
| `ipo_tutoring_enddate` | 挂牌企业上市辅导结束日期 |  | xla去前缀变体 |
| `ipo_tutoring_startdate` | 挂牌企业上市辅导开始日期 |  | xla去前缀变体 |
| `ipo_type` | 首发发行方式(新增) |  | xla去前缀变体 |
| `ipo_ufee` | 首发承销费用 |  | xla去前缀变体 |
| `ipo_underwriterallotment` | 主承销商战略获配股份数 |  | xla去前缀变体 |
| `ipo_underwriterallotmentratio` | 主承销商战略获配股份占比 |  | xla去前缀变体 |
| `ipo_underwritingfees_shareholder` | 售股股东应摊承销与保荐费用 |  | xla去前缀变体 |
| `ipo_underwritingratio` | 包销比例 |  | xla去前缀变体 |
| `ipo_undrtype` | 首发承销方式(新增) |  | xla去前缀变体 |
| `ipo_usfeerate_fix` | 首发基础承销费率 |  | xla去前缀变体 |
| `ipo_usfeerate_float` | 首发浮动承销费率 |  | xla去前缀变体 |
| `ipo_usfees` | 首发承销保荐费用 |  | xla去前缀变体 |
| `ipo_volume` | 上市首日成交额(新增) |  | xla去前缀变体 |
| `ipo_vsprice_max` | 网下有效报价上限 |  | xla去前缀变体 |
| `ipo_vsprice_min` | 网下有效报价下限 |  | xla去前缀变体 |
| `ipo_vsratio` | 网下超额认购倍数(回拨前) |  | xla去前缀变体 |
| `ipo_vsshares` | 网下有效报价申购量 |  | xla去前缀变体 |
| `ipo_vsshares_s` | 网上发行有效申购数量 |  | xla去前缀变体 |
| `ipo_vssharespct` | 网下有效报价申购量比例 |  | xla去前缀变体 |
| `ipo_vssharespct_abc` | 网下投资者有效申购数量占比 | InstitutionType | xla去前缀变体 |
| `ipo_weightedpe` | 首发市盈率(加权)(新增) |  | xla去前缀变体 |
| `ipo_wgtavgprice` | 网下申报价格加权平均数 | InstitutionType | xla去前缀变体 |
| `ipo_wpipreleasingdate` | 网上预览资料公告日 |  | xla去前缀变体 |

<a id="分类-分红"></a>

## 分红（68 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `div_accmdivrpt` | 现金分红总额 | REPORTDATE | xla去前缀变体 |
| `div_accumulatedpayout` | 累计分红总额 |  | xla去前缀变体 |
| `div_accumulatedperunit` | 单位累计分红 |  | xla去前缀变体 |
| `div_accumulatedtimes` | 累计分红次数 |  | xla去前缀变体 |
| `div_aualaccmdiv` | 年度累计分红总额(新增) |  | xla去前缀变体 |
| `div_aualaccmdiv2` | 区间现金分红总额 | StartDate、DATE、CURTYPE | xla去前缀变体 |
| `div_aualaccmdiv_ard` | 年度累计分红总额(已宣告) |  | xla去前缀变体 |
| `div_aualaccmdiv_ex` | 年度累计分红总额(已宣告,剔除特别派息) | Year | xla去前缀变体 |
| `div_aualaccmdiv_i` | 年度累计分红总额 | Year | xla去前缀变体 |
| `div_aualaccmdivcpy` | 公司区间现金分红总额 | StartDate、DATE | xla去前缀变体 |
| `div_aualaccmdivpershare` | 年度累计单位分红(新增) |  | xla去前缀变体 |
| `div_aualcashdividend` | 年度现金分红总额 |  | xla去前缀变体 |
| `div_capitalization` | 每股转增股本 | REPORTDATE | xla去前缀变体 |
| `div_capitalization2` | 每股转增股本(已宣告) | REPORTDATE | xla去前缀变体 |
| `div_cashaftertax` | 每股股利(税后) | REPORTDATE | xla去前缀变体 |
| `div_cashaftertax2` | 每股股利(税后)(已宣告) | REPORTDATE | xla去前缀变体 |
| `div_cashandstock` | 每股分红送转 | REPORTDATE | xla去前缀变体 |
| `div_cashbeforetax` | 每股股利(税前) | REPORTDATE | xla去前缀变体 |
| `div_cashbeforetax2` | 每股股利(税前)(已宣告) | REPORTDATE | xla去前缀变体 |
| `div_cashbftax` | 每股股利(税前) | REPORTDATE | xla去前缀变体 |
| `div_cashbftax_ex` | 每股股利(税前,剔除特别派息) | REPORTDATE | xla去前缀变体 |
| `div_cashdivbb` | 年度累计分红总额(已宣告,含回购) | Year | xla去前缀变体 |
| `div_cashpaidaftertax` | 区间每股股利(税后) | StartDate、EndDate | xla去前缀变体 |
| `div_cashpaidbeforetax` | 区间每股股利(税前) | StartDate、EndDate | xla去前缀变体 |
| `div_ccyoptend` | 股东行使现金分红货币选择权截止日 | REPORTDATE | xla去前缀变体 |
| `div_ccyoptstart` | 股东行使现金分红货币选择权起始日 | REPORTDATE | xla去前缀变体 |
| `div_clause` | 分红条款 |  | xla去前缀变体 |
| `div_compindex` | 成份分红对指数影响 | TRADEDATE | xla去前缀变体 |
| `div_dividendratio` | 现金分红比例 |  | xla去前缀变体 |
| `div_divpct_3yaccubb` | 三年累计分红占比(含回购) | Year | xla去前缀变体 |
| `div_divpct_3yearaccu` | 三年累计分红占比(再融资条件)(新增) |  | xla去前缀变体 |
| `div_divpct_accu` | 上市以来分红率 | REPORTDATE | xla去前缀变体 |
| `div_exdate` | 除权除息日 | REPORTDATE | xla去前缀变体 |
| `div_exdivdate` | 最新分红日期 | DEALDATE | xla去前缀变体 |
| `div_firstyear` | 上市后首次分红年份 |  | xla去前缀变体 |
| `div_freq` | 年度现金分红次数 |  | xla去前缀变体 |
| `div_freqard` | 年度现金分红次数(已宣告) | Year | xla去前缀变体 |
| `div_fstdiscdate` | 现金分红首次披露日 | REPORTDATE | xla去前缀变体 |
| `div_ifdiv` | 是否分红(新增) | D | xla去前缀变体 |
| `div_impdate` | 分红实施公告日(新增) | D | xla去前缀变体 |
| `div_lasttrddateshareb` | B股最后交易日(新增) | D | xla去前缀变体 |
| `div_object` | 分红对象(新增) | D | xla去前缀变体 |
| `div_paydate` | 派息日 | REPORTDATE | xla去前缀变体 |
| `div_payout` | 年度分红总额 | RPTYEAR | xla去前缀变体 |
| `div_payoutratio` | 年度现金分红比例 | Year | xla去前缀变体 |
| `div_payoutratio_ex` | 年度现金分红比例(已宣告,剔除特别派息) | Year | xla去前缀变体 |
| `div_periodpayout` | 区间分红总额 |  | xla去前缀变体 |
| `div_periodperunit` | 单位区间分红 |  | xla去前缀变体 |
| `div_periodtimes` | 区间分红次数 |  | xla去前缀变体 |
| `div_perunit` | 单位年度分红 | RPTYEAR | xla去前缀变体 |
| `div_predisclosuredate` | 预披露公告日 | REPORTDATE | xla去前缀变体 |
| `div_prelandate` | 预案公告日(新增) | D | xla去前缀变体 |
| `div_profitdistall` | 年度利润分配合计 | Year | xla去前缀变体 |
| `div_profitdistcash` | 年度现金形式发放总额 | Year | xla去前缀变体 |
| `div_profitdistre` | 年度再投资形式发放总额 | Year | xla去前缀变体 |
| `div_progress` | 分红方案进度 | REPORTDATE | xla去前缀变体 |
| `div_ratiocs` | 普通股股东年度现金分红比例 | Year | xla去前缀变体 |
| `div_ratiocsa` | 普通股股东年度现金分红比例(公告) | Year | xla去前缀变体 |
| `div_ratiocsd` | 普通股股东年度现金分红比例(已宣告) | Year | xla去前缀变体 |
| `div_ratiocsd_ex` | 普通股股东年度现金分红比例(已宣告,剔除特别派息) | Year | xla去前缀变体 |
| `div_recdateshareb` | B股股权登记日(新增) | D | xla去前缀变体 |
| `div_recorddate` | 股权登记日 | REPORTDATE | xla去前缀变体 |
| `div_shares` | 分红基准股本 | REPORTDATE | xla去前缀变体 |
| `div_smtgdate` | 股东大会公告日(新增) | D | xla去前缀变体 |
| `div_stock` | 每股红股 | REPORTDATE | xla去前缀变体 |
| `div_stock2` | 每股红股(已宣告) | REPORTDATE | xla去前缀变体 |
| `div_times` | 年度分红次数 | RPTYEAR | xla去前缀变体 |
| `div_trddateshareb` | 红股上市交易日(新增) | D | xla去前缀变体 |

<a id="分类-盈利预测"></a>

## 盈利预测（142 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `est_avgbps` | 预测每股净资产(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgbps1` | 预测每股净资产(BPS)平均值 |  | xla去前缀变体 |
| `est_avgcps` | 预测每股现金流(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgcps1` | 预测每股现金流(CPS)平均值 |  | xla去前缀变体 |
| `est_avgdps` | 预测每股股利(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgdps1` | 预测每股股利(DPS)平均值 |  | xla去前缀变体 |
| `est_avgebit` | 预测息税前利润(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgebit1` | 预测息税前利润(EBIT)平均值 |  | xla去前缀变体 |
| `est_avgebitda` | 预测息税折旧摊销前利润(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgebitda1` | 预测息税折旧摊销前利润(EBITDA)平均值 |  | xla去前缀变体 |
| `est_avgebt` | 预测利润总额(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgebt1` | 预测利润总额平均值 |  | xla去前缀变体 |
| `est_avgoperatingprofit` | 预测营业利润(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgoperatingprofit1` | 预测营业利润平均值 |  | xla去前缀变体 |
| `est_avgroa` | 预测总资产收益率(综合值) | RPTYEAR | xla去前缀变体 |
| `est_avgroe` | 预测净资产收益率(综合值) | RPTYEAR | xla去前缀变体 |
| `est_cagr_np` | 未来3年净利润复合年增长率 |  | xla去前缀变体 |
| `est_cagr_sales` | 未来3年营业总收入复合年增长率 |  | xla去前缀变体 |
| `est_ebitda` | 机构预测EBITDA |  | xla去前缀变体 |
| `est_eps` | 预测每股收益(综合值) | RPTYEAR | xla去前缀变体 |
| `est_eps1` | 预测每股收益平均值 |  | xla去前缀变体 |
| `est_eps_inst` | 预测每股收益(明细值) | RPTYEAR | xla去前缀变体 |
| `est_estanalyst` | 预测研究员(新增) | RPTYEAR | xla去前缀变体 |
| `est_estnewtime_inst` | 机构最近预测时间(新增) | RPTYEAR | xla去前缀变体 |
| `est_event_date` | 大事日期(大事后预测) | DATE | xla去前缀变体 |
| `est_evtoebitda` | 机构预测EV/EBITDA |  | xla去前缀变体 |
| `est_frstratingtime_inst` | 机构首次评级时间(新增) |  | xla去前缀变体 |
| `est_highprice_inst` | 本次最低目标价 | EndDate | xla去前缀变体 |
| `est_instnum` | 预测机构家数 | RPTYEAR | xla去前缀变体 |
| `est_lowprice_inst` | 本次最高目标价 | EndDate | xla去前缀变体 |
| `est_maxbps` | 预测每股净资产(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxbps1` | 预测每股净资产(BPS)最大值 |  | xla去前缀变体 |
| `est_maxcps` | 预测每股现金流(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxcps1` | 预测每股现金流(CPS)最大值 |  | xla去前缀变体 |
| `est_maxdps` | 预测每股股利(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxdps1` | 预测每股股利(DPS)最大值 |  | xla去前缀变体 |
| `est_maxebit` | 预测息税前利润(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxebit1` | 预测息税前利润(EBIT)最大值 |  | xla去前缀变体 |
| `est_maxebitda` | 预测息税折旧摊销前利润(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxebitda1` | 预测息税折旧摊销前利润(EBITDA)最大值 |  | xla去前缀变体 |
| `est_maxebt` | 预测利润总额(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxebt1` | 预测利润总额最大值 |  | xla去前缀变体 |
| `est_maxeps` | 预测每股收益(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxeps1` | 预测每股收益最大值 |  | xla去前缀变体 |
| `est_maxnetprofit` | 预测净利润(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxnetprofit1` | 预测净利润最大值 |  | xla去前缀变体 |
| `est_maxoperatingprofit` | 预测营业利润(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxoperatingprofit1` | 预测营业利润最大值 |  | xla去前缀变体 |
| `est_maxroa` | 预测总资产收益率(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxroe` | 预测净资产收益率(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxsales` | 预测主营业务收入(最大值) | RPTYEAR | xla去前缀变体 |
| `est_maxsales1` | 预测营业收入最大值 |  | xla去前缀变体 |
| `est_medianbps` | 预测每股净资产(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianbps1` | 预测每股净资产(BPS)中值 |  | xla去前缀变体 |
| `est_mediancps` | 预测每股现金流(中值) | RPTYEAR | xla去前缀变体 |
| `est_mediancps1` | 预测每股现金流(CPS)中值 |  | xla去前缀变体 |
| `est_mediandps` | 预测每股股利(中值) | RPTYEAR | xla去前缀变体 |
| `est_mediandps1` | 预测每股股利(DPS)中值 |  | xla去前缀变体 |
| `est_medianebit` | 预测息税前利润(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianebit1` | 预测息税前利润(EBIT)中值 |  | xla去前缀变体 |
| `est_medianebitda` | 预测息税折旧摊销前利润(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianebitda1` | 预测息税折旧摊销前利润(EBITDA)中值 |  | xla去前缀变体 |
| `est_medianebt` | 预测利润总额(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianebt1` | 预测利润总额中值 |  | xla去前缀变体 |
| `est_medianeps` | 预测每股收益(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianeps1` | 预测每股收益中值 |  | xla去前缀变体 |
| `est_mediannetprofit` | 预测净利润(中值) | RPTYEAR | xla去前缀变体 |
| `est_mediannetprofit1` | 预测净利润中值 |  | xla去前缀变体 |
| `est_medianoperatingprofit` | 预测营业利润(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianoperatingprofit1` | 预测营业利润中值 |  | xla去前缀变体 |
| `est_medianroa` | 预测总资产收益率(中值) | RPTYEAR | xla去前缀变体 |
| `est_medianroe` | 预测净资产收益率(中值) | RPTYEAR | xla去前缀变体 |
| `est_mediansales` | 预测主营业务收入(中值) | RPTYEAR | xla去前缀变体 |
| `est_mediansales1` | 预测营业收入中值 |  | xla去前缀变体 |
| `est_minbps` | 预测每股净资产(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minbps1` | 预测每股净资产(BPS)最小值 |  | xla去前缀变体 |
| `est_mincps` | 预测每股现金流(最小值) | RPTYEAR | xla去前缀变体 |
| `est_mincps1` | 预测每股现金流(CPS)最小值 |  | xla去前缀变体 |
| `est_mindps` | 预测每股股利(最小值) | RPTYEAR | xla去前缀变体 |
| `est_mindps1` | 预测每股股利(DPS)最小值 |  | xla去前缀变体 |
| `est_minebit` | 预测息税前利润(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minebit1` | 预测息税前利润(EBIT)最小值 |  | xla去前缀变体 |
| `est_minebitda` | 预测息税折旧摊销前利润(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minebitda1` | 预测息税折旧摊销前利润(EBITDA)最小值 |  | xla去前缀变体 |
| `est_minebt` | 预测利润总额(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minebt1` | 预测利润总额最小值 |  | xla去前缀变体 |
| `est_mineps` | 预测每股收益(最小值) | RPTYEAR | xla去前缀变体 |
| `est_mineps1` | 预测每股收益最小值 |  | xla去前缀变体 |
| `est_minnetprofit` | 预测净利润(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minnetprofit1` | 预测净利润最小值 |  | xla去前缀变体 |
| `est_minoperatingprofit` | 预测营业利润(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minoperatingprofit1` | 预测营业利润最小值 |  | xla去前缀变体 |
| `est_minroa` | 预测总资产收益率(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minroe` | 预测净资产收益率(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minsales` | 预测主营业务收入(最小值) | RPTYEAR | xla去前缀变体 |
| `est_minsales1` | 预测营业收入最小值 |  | xla去前缀变体 |
| `est_netprofit` | 预测净利润(综合值) | RPTYEAR | xla去前缀变体 |
| `est_netprofit1` | 预测净利润平均值 |  | xla去前缀变体 |
| `est_netprofit_downgrade` | 一月内净利润调低家数 | RPTYEAR | xla去前缀变体 |
| `est_netprofit_inst` | 预测净利润(明细值) | RPTYEAR | xla去前缀变体 |
| `est_netprofit_maintain` | 一月内净利润维持家数 | RPTYEAR | xla去前缀变体 |
| `est_netprofit_upgrade` | 一月内净利润调高家数 | RPTYEAR | xla去前缀变体 |
| `est_newratingtime_inst` | 机构最近评级时间(新增) |  | xla去前缀变体 |
| `est_orgrating_inst` | 机构投资评级(原始)(新增) |  | xla去前缀变体 |
| `est_pctchange` | 预测涨跌幅(评级日,最低价) | TRADEDATE、TYPE | xla去前缀变体 |
| `est_prehighprice_inst` | 前次最低目标价 | EndDate | xla去前缀变体 |
| `est_prelowprice_inst` | 前次最高目标价 | EndDate | xla去前缀变体 |
| `est_ratinganalyst` | 评级研究员(新增) |  | xla去前缀变体 |
| `est_rptabstract_inst` | 内容 | EndDate | xla去前缀变体 |
| `est_rpttitle_inst` | 报告标题 | EndDate | xla去前缀变体 |
| `est_sales` | 预测主营业务收入(综合值) | RPTYEAR | xla去前缀变体 |
| `est_sales1` | 预测营业收入平均值 |  | xla去前缀变体 |
| `est_sales_downgrade` | 一月内主营业务收入调低家数 | RPTYEAR | xla去前缀变体 |
| `est_sales_inst` | 预测主营业务收入(明细值) | RPTYEAR | xla去前缀变体 |
| `est_sales_maintain` | 一月内主营业务收入维持家数 | RPTYEAR | xla去前缀变体 |
| `est_sales_upgrade` | 一月内主营业务收入调高家数 | RPTYEAR | xla去前缀变体 |
| `est_scorerating_inst` | 机构投资评级(标准化得分)(新增) |  | xla去前缀变体 |
| `est_stdbps` | 预测每股净资产(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdbps1` | 预测每股净资产(BPS)标准差 |  | xla去前缀变体 |
| `est_stdcps` | 预测每股现金流(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdcps1` | 预测每股现金流(CPS)标准差 |  | xla去前缀变体 |
| `est_stddps` | 预测每股股利(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stddps1` | 预测每股股利(DPS)标准差 |  | xla去前缀变体 |
| `est_stdebit` | 预测息税前利润(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdebit1` | 预测息税前利润(EBIT)标准差 |  | xla去前缀变体 |
| `est_stdebitda` | 预测息税折旧摊销前利润(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdebitda1` | 预测息税折旧摊销前利润(EBITDA)标准差 |  | xla去前缀变体 |
| `est_stdebt` | 预测利润总额(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdebt1` | 预测利润总额标准差 |  | xla去前缀变体 |
| `est_stdeps` | 预测每股收益(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdeps1` | 预测每股收益标准差 |  | xla去前缀变体 |
| `est_stdnetprofit` | 预测净利润(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdnetprofit1` | 预测净利润标准差 |  | xla去前缀变体 |
| `est_stdoperatingprofit` | 预测营业利润(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdoperatingprofit1` | 预测营业利润标准差 |  | xla去前缀变体 |
| `est_stdrating_inst` | 机构投资评级(标准化评级)(新增) |  | xla去前缀变体 |
| `est_stdroa` | 预测总资产收益率(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdroe` | 预测净资产收益率(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdsales` | 预测主营业务收入(标准差) | RPTYEAR | xla去前缀变体 |
| `est_stdsales1` | 预测营业收入标准差 |  | xla去前缀变体 |
| `est_yoynetprofit` | 预测净利润增长率 | RPTYEAR | xla去前缀变体 |
| `est_yoysales` | 预测主营业务收入增长率 | RPTYEAR | xla去前缀变体 |

<a id="分类-一致预期"></a>

## 一致预期（237 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `west_avgbps` | 预测每股净资产平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgbps1` | 预测每股净资产(BPS)平均值 |  | xla去前缀变体 |
| `west_avgbps_fy1` | 一致预测每股净资产(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgbps_fy2` | 一致预测每股净资产(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgbps_fy3` | 一致预测每股净资产(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgcps` | 预测每股现金流平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgcps1` | 预测每股现金流(CPS)平均值 |  | xla去前缀变体 |
| `west_avgcps_ftm` | 一致预测每股现金流(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgcps_fy1` | 一致预测每股现金流(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgcps_fy2` | 一致预测每股现金流(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgcps_fy3` | 一致预测每股现金流(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgdps` | 预测每股股利平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgdps1` | 预测每股股利(DPS)平均值 |  | xla去前缀变体 |
| `west_avgdps_fy1` | 一致预测每股股利(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgdps_fy2` | 一致预测每股股利(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgdps_fy3` | 一致预测每股股利(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgdps_yoy2` | 一致预测每股股利同比(FY2比FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgebit` | 预测息税前利润平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgebit1` | 预测息税前利润(EBIT)平均值 |  | xla去前缀变体 |
| `west_avgebit_cagr` | 一致预测息税前利润年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_avgebit_ftm` | 一致预测息税前利润(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgebit_fy1` | 一致预测息税前利润(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgebit_fy2` | 一致预测息税前利润(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgebit_fy3` | 一致预测息税前利润(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgebit_yoy` | 一致预测息税前利润同比 | TRADEDATE | xla去前缀变体 |
| `west_avgebitda` | 预测息税折旧摊销前利润平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgebitda1` | 预测息税折旧摊销前利润(EBITDA)平均值 |  | xla去前缀变体 |
| `west_avgebitda_cagr` | 一致预测息税折旧摊销前利润2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_avgebitda_ftm` | 一致预测息税折旧摊销前利润(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgebitda_fy1` | 一致预测息税折旧摊销前利润(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgebitda_fy2` | 一致预测息税折旧摊销前利润(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgebitda_fy3` | 一致预测息税折旧摊销前利润(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgebitda_yoy` | 一致预测息税折旧摊销前利润同比 | TRADEDATE | xla去前缀变体 |
| `west_avgebt` | 预测利润总额平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgebt1` | 预测利润总额平均值 |  | xla去前缀变体 |
| `west_avgebt_cagr` | 一致预测利润总额2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_avgebt_ftm` | 一致预测利润总额(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgebt_fy1` | 一致预测利润总额(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgebt_fy2` | 一致预测利润总额(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgebt_fy3` | 一致预测利润总额(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgebt_surprise` | 预测利润总额Surprise |  | xla去前缀变体 |
| `west_avgebt_surprise_pct` | 预测利润总额Surprise百分比 |  | xla去前缀变体 |
| `west_avgebt_yoy` | 一致预测利润总额同比 | TRADEDATE | xla去前缀变体 |
| `west_avggm` | 预测销售毛利率(GM)平均值(可选类型) |  | xla去前缀变体 |
| `west_avgnp_yoy` | 一致预测净利润同比(FY2比FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgoc` | 预测营业成本平均值 | Year、TRADEDATE | xla去前缀变体 |
| `west_avgoc1` | 预测营业成本平均值 | Year、TRADEDATE | xla去前缀变体 |
| `west_avgoc_cagr` | 一致预测营业成本2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_avgoc_ftm` | 一致预测营业成本(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgoc_fy1` | 一致预测营业成本(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgoc_fy2` | 一致预测营业成本(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgoc_fy3` | 一致预测营业成本(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgoc_surprise` | 预测营业成本Surprise |  | xla去前缀变体 |
| `west_avgoc_surprise_pct` | 预测营业成本Surprise百分比 |  | xla去前缀变体 |
| `west_avgoc_yoy` | 一致预测营业成本同比 | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit` | 预测营业利润平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgoperatingprofit1` | 预测营业利润平均值 |  | xla去前缀变体 |
| `west_avgoperatingprofit_cagr` | 一致预测营业利润2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit_ftm` | 一致预测营业利润(未来12个月) | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit_fy1` | 一致预测营业利润(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit_fy2` | 一致预测营业利润(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit_fy3` | 一致预测营业利润(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgoperatingprofit_surprise` | 预测营业利润Surprise |  | xla去前缀变体 |
| `west_avgoperatingprofit_surprise_pct` | 预测营业利润Surprise百分比 |  | xla去前缀变体 |
| `west_avgoperatingprofit_yoy` | 一致预测营业利润同比 | TRADEDATE | xla去前缀变体 |
| `west_avgopm` | 预测营业利润率(OPM)平均值(可选类型) |  | xla去前缀变体 |
| `west_avgroa` | 预测总资产收益率平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgroe` | 预测净资产收益率平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_avgroe_fy1` | 一致预测ROE(FY1) | TRADEDATE | xla去前缀变体 |
| `west_avgroe_fy2` | 一致预测ROE(FY2) | TRADEDATE | xla去前缀变体 |
| `west_avgroe_fy3` | 一致预测ROE(FY3) | TRADEDATE | xla去前缀变体 |
| `west_avgroe_yoy` | 一致预测ROE同比 | TRADEDATE | xla去前缀变体 |
| `west_avgshares` | 预测基准股本综合值 | TRADEDATE、Year | xla去前缀变体 |
| `west_bps_surprise` | 预测每股净资产Surprise |  | xla去前缀变体 |
| `west_bps_surprise_pct` | 预测每股净资产Surprise百分比 |  | xla去前缀变体 |
| `west_eps` | 预测每股收益平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_eps1` | 预测每股收益平均值 |  | xla去前缀变体 |
| `west_eps_ftm` | 预测EPS(FTM) |  | 探测法实测 |
| `west_eps_fy1` | 一致预测每股收益(FY1) | TRADEDATE | xla去前缀变体 |
| `west_eps_fy2` | 一致预测每股收益(FY2) | TRADEDATE | xla去前缀变体 |
| `west_eps_fy3` | 一致预测每股收益(FY3) | TRADEDATE | xla去前缀变体 |
| `west_eps_surprise` | 预测每股收益Surprise |  | xla去前缀变体 |
| `west_eps_surprise_pct` | 预测每股收益Surprise百分比 |  | xla去前缀变体 |
| `west_instnum` | 每股收益预测机构家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_instnum_bps` | 每股净资产预测机构家数 |  | xla去前缀变体 |
| `west_instnum_cps` | 每股现金流预测机构家数 |  | xla去前缀变体 |
| `west_instnum_dps` | 每股股利预测机构家数 |  | xla去前缀变体 |
| `west_instnum_ebit` | 息税前利润预测机构家数 |  | xla去前缀变体 |
| `west_instnum_ebitda` | 息税折旧摊销前利润预测机构家数 |  | xla去前缀变体 |
| `west_instnum_ebt` | 利润总额预测机构家数 |  | xla去前缀变体 |
| `west_instnum_gm` | 销售毛利率预测机构家数(可选类型) |  | xla去前缀变体 |
| `west_instnum_np` | 净利润预测机构家数 |  | xla去前缀变体 |
| `west_instnum_op` | 营业利润预测机构家数 |  | xla去前缀变体 |
| `west_instnum_opm` | 营业利润率(OPM)预测机构家数(可选类型) |  | xla去前缀变体 |
| `west_instnum_roa` | 总资产收益率预测机构家数 |  | xla去前缀变体 |
| `west_instnum_roe` | 净资产收益率预测机构家数 |  | xla去前缀变体 |
| `west_instnum_sales` | 营业收入预测机构家数 |  | xla去前缀变体 |
| `west_maxbps` | 预测每股净资产最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxbps1` | 预测每股净资产(BPS)最大值 |  | xla去前缀变体 |
| `west_maxcps` | 预测每股现金流最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxcps1` | 预测每股现金流(CPS)最大值 |  | xla去前缀变体 |
| `west_maxdps` | 预测每股股利最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxdps1` | 预测每股股利(DPS)最大值 |  | xla去前缀变体 |
| `west_maxebit` | 预测息税前利润最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxebit1` | 预测息税前利润(EBIT)最大值 |  | xla去前缀变体 |
| `west_maxebitda` | 预测息税折旧摊销前利润最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxebitda1` | 预测息税折旧摊销前利润(EBITDA)最大值 |  | xla去前缀变体 |
| `west_maxebt` | 预测利润总额最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxebt1` | 预测利润总额最大值 |  | xla去前缀变体 |
| `west_maxeps` | 预测每股收益最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxeps1` | 预测每股收益最大值 |  | xla去前缀变体 |
| `west_maxgm` | 预测销售毛利率(GM)最大值(可选类型) |  | xla去前缀变体 |
| `west_maxnetprofit` | 预测净利润最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxnetprofit1` | 预测净利润最大值 |  | xla去前缀变体 |
| `west_maxoc` | 预测营业成本最大值 | TRADEDATE、Year | xla去前缀变体 |
| `west_maxoc1` | 预测营业成本最大值 | TRADEDATE、Year | xla去前缀变体 |
| `west_maxoperatingprofit` | 预测营业利润最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxoperatingprofit1` | 预测营业利润最大值 |  | xla去前缀变体 |
| `west_maxopm` | 预测营业利润率(OPM)最大值(可选类型) |  | xla去前缀变体 |
| `west_maxroa` | 预测总资产收益率最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxroe` | 预测净资产收益率最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxsales` | 预测主营业务收入最大值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_maxsales1` | 预测营业收入最大值 |  | xla去前缀变体 |
| `west_mediagm` | 预测销售毛利率(GM)中值(可选类型) |  | xla去前缀变体 |
| `west_medianbps` | 预测每股净资产中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianbps1` | 预测每股净资产(BPS)中值 |  | xla去前缀变体 |
| `west_mediancps` | 预测每股现金流中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mediancps1` | 预测每股现金流(CPS)中值 |  | xla去前缀变体 |
| `west_mediandps` | 预测每股股利中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mediandps1` | 预测每股股利(DPS)中值 |  | xla去前缀变体 |
| `west_medianebit` | 预测息税前利润中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianebit1` | 预测息税前利润(EBIT)中值 |  | xla去前缀变体 |
| `west_medianebitda` | 预测息税折旧摊销前利润中值 | Year、DATE、Perild | xla去前缀变体 |
| `west_medianebitda1` | 预测息税折旧摊销前利润(EBITDA)中值 |  | xla去前缀变体 |
| `west_medianebt` | 预测利润总额中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianebt1` | 预测利润总额中值 |  | xla去前缀变体 |
| `west_medianeps` | 预测每股收益中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianeps1` | 预测每股收益中值 |  | xla去前缀变体 |
| `west_mediannetprofit` | 预测净利润中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mediannetprofit1` | 预测净利润中值 |  | xla去前缀变体 |
| `west_medianoperatingprofit` | 预测营业利润中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianoperatingprofit1` | 预测营业利润中值 |  | xla去前缀变体 |
| `west_medianroa` | 预测总资产收益率中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_medianroe` | 预测净资产收益率中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mediansales` | 预测主营业务收入中值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mediansales1` | 预测营业收入中值 |  | xla去前缀变体 |
| `west_mediaoc` | 预测营业成本中值 | TRADEDATE、Year | xla去前缀变体 |
| `west_mediaoc1` | 预测营业成本中值 | TRADEDATE、Year | xla去前缀变体 |
| `west_mediaopm` | 预测营业利润率(OPM)中值(可选类型) |  | xla去前缀变体 |
| `west_minbps` | 预测每股净资产最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minbps1` | 预测每股净资产(BPS)最小值 |  | xla去前缀变体 |
| `west_mincps` | 预测每股现金流最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mincps1` | 预测每股现金流(CPS)最小值 |  | xla去前缀变体 |
| `west_mindps` | 预测每股股利最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mindps1` | 预测每股股利(DPS)最小值 |  | xla去前缀变体 |
| `west_minebit` | 预测息税前利润最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minebit1` | 预测息税前利润(EBIT)最小值 |  | xla去前缀变体 |
| `west_minebitda` | 预测息税折旧摊销前利润最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minebitda1` | 预测息税折旧摊销前利润(EBITDA)最小值 |  | xla去前缀变体 |
| `west_minebt` | 预测利润总额最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minebt1` | 预测利润总额最小值 |  | xla去前缀变体 |
| `west_mineps` | 预测每股收益最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_mineps1` | 预测每股收益最小值 |  | xla去前缀变体 |
| `west_mingm` | 预测销售毛利率(GM)最小值(可选类型) |  | xla去前缀变体 |
| `west_minnetprofit` | 预测净利润最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minnetprofit1` | 预测净利润最小值 |  | xla去前缀变体 |
| `west_minoc` | 预测营业成本最小值 | TRADEDATE、Year | xla去前缀变体 |
| `west_minoc1` | 预测营业成本最小值 | TRADEDATE、Year | xla去前缀变体 |
| `west_minoperatingprofit` | 预测营业利润最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minoperatingprofit1` | 预测营业利润最小值 |  | xla去前缀变体 |
| `west_minopm` | 预测营业利润率(OPM)最小值(可选类型) |  | xla去前缀变体 |
| `west_minroa` | 预测总资产收益率最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minroe` | 预测净资产收益率最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minsales` | 预测主营业务收入最小值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_minsales1` | 预测营业收入最小值 |  | xla去前缀变体 |
| `west_netprofit` | 预测净利润平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_netprofit1` | 预测净利润平均值 |  | xla去前缀变体 |
| `west_netprofit_cagr` | 一致预测净利润2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_netprofit_downgrade` | 一月内净利润调低家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_netprofit_ftm` | 预测净利润(FTM) |  | 探测法实测 |
| `west_netprofit_fy1` | 一致预测净利润(FY1) | TRADEDATE | xla去前缀变体 |
| `west_netprofit_fy2` | 一致预测净利润(FY2) | TRADEDATE | xla去前缀变体 |
| `west_netprofit_fy3` | 一致预测净利润(FY3) | TRADEDATE | xla去前缀变体 |
| `west_netprofit_maintain` | 一月内净利润维持家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_netprofit_surprise` | 预测净利润Surprise |  | xla去前缀变体 |
| `west_netprofit_surprise_pct` | 预测净利润Surprise百分比 |  | xla去前缀变体 |
| `west_netprofit_upgrade` | 一月内净利润调高家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_netprofit_yoy` | 一致预测净利润同比 | TRADEDATE | xla去前缀变体 |
| `west_nproc_13w` | 一致预测净利润13周变化率 | TRADEDATE、Year | xla去前缀变体 |
| `west_nproc_1w` | 一致预测净利润1周变化率 | Year、TRADEDATE | xla去前缀变体 |
| `west_nproc_26w` | 一致预测净利润26周变化率 | TRADEDATE、Year | xla去前缀变体 |
| `west_nproc_4w` | 一致预测净利润4周变化率 | Year、TRADEDATE | xla去前缀变体 |
| `west_pe` | 预测PE(可选类型) | Year、DATE | xla去前缀变体 |
| `west_peg` | 预测PEG(可选类型) | Year、DATE | xla去前缀变体 |
| `west_return` | 估算涨跌幅 | TRADEDATE | xla去前缀变体 |
| `west_return_error` | 估算涨跌幅误差 | TRADEDATE | xla去前缀变体 |
| `west_sales` | 预测主营业务收入平均值 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_sales1` | 预测营业收入平均值 |  | xla去前缀变体 |
| `west_sales_cagr` | 一致预测营业收入2年复合增长率 | TRADEDATE | xla去前缀变体 |
| `west_sales_downgrade` | 一月内主营业务收入调低家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_sales_ftm` | 预测营收(FTM) |  | 探测法实测 |
| `west_sales_fy1` | 一致预测营业收入(FY1) | TRADEDATE | xla去前缀变体 |
| `west_sales_fy2` | 一致预测营业收入(FY2) | TRADEDATE | xla去前缀变体 |
| `west_sales_fy3` | 一致预测营业收入(FY3) | TRADEDATE | xla去前缀变体 |
| `west_sales_maintain` | 一月内主营业务收入维持家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_sales_surprise` | 预测营业收入Surprise |  | xla去前缀变体 |
| `west_sales_surprise_pct` | 预测营业收入Surprise百分比 |  | xla去前缀变体 |
| `west_sales_upgrade` | 一月内主营业务收入调高家数 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_sales_yoy` | 一致预测营业收入同比 | TRADEDATE | xla去前缀变体 |
| `west_stdbps` | 预测每股净资产标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdbps1` | 预测每股净资产(BPS)标准差 |  | xla去前缀变体 |
| `west_stdcps` | 预测每股现金流标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdcps1` | 预测每股现金流(CPS)标准差 |  | xla去前缀变体 |
| `west_stddps` | 预测每股股利标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stddps1` | 预测每股股利(DPS)标准差 |  | xla去前缀变体 |
| `west_stdebit` | 预测息税前利润标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdebit1` | 预测息税前利润(EBIT)标准差 |  | xla去前缀变体 |
| `west_stdebitda` | 预测息税折旧摊销前利润标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdebitda1` | 预测息税折旧摊销前利润(EBITDA)标准差 |  | xla去前缀变体 |
| `west_stdebt` | 预测利润总额标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdebt1` | 预测利润总额标准差 |  | xla去前缀变体 |
| `west_stdeps` | 预测每股收益标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdeps1` | 预测每股收益标准差 |  | xla去前缀变体 |
| `west_stdgm` | 预测销售毛利率(GM)标准差值(可选类型) |  | xla去前缀变体 |
| `west_stdnetprofit` | 预测净利润标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdnetprofit1` | 预测净利润标准差 |  | xla去前缀变体 |
| `west_stdoperatingprofit` | 预测营业利润标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdoperatingprofit1` | 预测营业利润标准差 |  | xla去前缀变体 |
| `west_stdopm` | 预测营业利润率(OPM)标准差值(可选类型) |  | xla去前缀变体 |
| `west_stdroa` | 预测总资产收益率标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdroe` | 预测净资产收益率标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdsales` | 预测主营业务收入标准差 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_stdsales1` | 预测营业收入标准差 |  | xla去前缀变体 |
| `west_stoc` | 预测营业成本标准差 | TRADEDATE、Year | xla去前缀变体 |
| `west_stoc1` | 预测营业成本标准差 | TRADEDATE、Year | xla去前缀变体 |
| `west_yoynetprofit` | 预测净利润增长率 | Year、DATE、PERIOD | xla去前缀变体 |
| `west_yoysales` | 预测主营业务收入增长率 | Year、DATE、PERIOD | xla去前缀变体 |

<a id="分类-ESG"></a>

## ESG（109 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `esg_approval` | ESG债券认证标准 |  | xla去前缀变体 |
| `esg_benefit_evaluation` | ESG债券效益评估 |  | xla去前缀变体 |
| `esg_conclusion` | ESG债券认证结论 |  | xla去前缀变体 |
| `esg_cr_wind` | 确定性等级 | REPORTDATE | xla去前缀变体 |
| `esg_eem01001` | SCOPE 1 温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_eem01002` | SCOPE 2 温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_eem01004` | 总温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_eem01008` | 温室气体减排量 | REPORTDATE | xla去前缀变体 |
| `esg_eem01011` | 是否就气候变化机会进行讨论 | REPORTDATE | xla去前缀变体 |
| `esg_eem01012` | 是否就气候变化风险进行讨论 | REPORTDATE | xla去前缀变体 |
| `esg_eem02001` | 氮氧化物排放 | REPORTDATE | xla去前缀变体 |
| `esg_eem02002` | 二氧化硫排放 | REPORTDATE | xla去前缀变体 |
| `esg_eem02003` | 悬浮粒子/颗粒物 | REPORTDATE | xla去前缀变体 |
| `esg_eem03001` | 有害废弃物量 | REPORTDATE | xla去前缀变体 |
| `esg_eem03002` | 无害废弃物量 | REPORTDATE | xla去前缀变体 |
| `esg_eem03003` | 废弃物总量 | REPORTDATE | xla去前缀变体 |
| `esg_eem03004` | 废弃物回收量 | REPORTDATE | xla去前缀变体 |
| `esg_em_wind` | 计算方法 | REPORTDATE | xla去前缀变体 |
| `esg_eot01003` | 是否重点排污单位 | REPORTDATE | xla去前缀变体 |
| `esg_eot02002` | 环保超标或其他违规次数 | REPORTDATE | xla去前缀变体 |
| `esg_ere01001` | 总能源消耗 | REPORTDATE | xla去前缀变体 |
| `esg_ere01002` | 耗电总量 | REPORTDATE | xla去前缀变体 |
| `esg_ere01003` | 节省用电量 | REPORTDATE | xla去前缀变体 |
| `esg_ere01004` | 煤碳使用量 | REPORTDATE | xla去前缀变体 |
| `esg_ere01005` | 天然气消耗 | REPORTDATE | xla去前缀变体 |
| `esg_ere01006` | 燃油消耗 | REPORTDATE | xla去前缀变体 |
| `esg_ere01007` | 节能量 | REPORTDATE | xla去前缀变体 |
| `esg_ere02001` | 纸消耗量 | REPORTDATE | xla去前缀变体 |
| `esg_ere02002` | 废纸回收量 | REPORTDATE | xla去前缀变体 |
| `esg_escore_wind` | 环境维度得分 | TRADEDATE | xla去前缀变体 |
| `esg_eventscore_wind` | ESG争议事件得分 | TRADEDATE | xla去前缀变体 |
| `esg_ewa01001` | 总用水量 | REPORTDATE | xla去前缀变体 |
| `esg_ewa01002` | 节省水量 | REPORTDATE | xla去前缀变体 |
| `esg_ewa01003` | 水循环与再利用的总量 | REPORTDATE | xla去前缀变体 |
| `esg_ewa01004` | 废水综合利用率 | REPORTDATE | xla去前缀变体 |
| `esg_ewa02002` | 废水/污水排放量 | REPORTDATE | xla去前缀变体 |
| `esg_ewa02003` | 废水处理量 | REPORTDATE | xla去前缀变体 |
| `esg_ewa02004` | 氨氮 | REPORTDATE | xla去前缀变体 |
| `esg_ewa02005` | 化学需氧量(COD) | REPORTDATE | xla去前缀变体 |
| `esg_gad01001` | 审计委员会会议次数 | REPORTDATE | xla去前缀变体 |
| `esg_gad01002` | 审计委员会会议出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gad02002` | 是否出具标准无保留意见 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01001` | 董事会规模 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01002` | 董事会出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01003` | 董事会召开数 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01004` | 参加少于75%会议的董事人数 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01005` | 监事会召开数 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01006` | 监事出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01007` | 是否设有监事委员会主席 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01008` | 提名委员会会议数 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01010` | 提名委员会会议出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01014` | 董事会成员受教育背景高于本科的比例 | REPORTDATE | xla去前缀变体 |
| `esg_gbo01015` | 女性董事占比 | REPORTDATE | xla去前缀变体 |
| `esg_gbo03001` | 独立董事董事会会议出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gbo03002` | 独立董事占董事会总人数的比例 | REPORTDATE | xla去前缀变体 |
| `esg_gcb_wind` | 绿色信贷余额 | Year | xla去前缀变体 |
| `esg_gcbtd_wind` | 绿色信贷余额 | REPORTDATE | xla去前缀变体 |
| `esg_ghg12_wind` | 温室气体排放总量(范围1和范围2) | REPORTDATE | xla去前缀变体 |
| `esg_ghg1_wind` | 直接(范围1)温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_ghg2_wind` | 能源间接(范围2)温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_ghgr12_wind` | 每百万元营收温室气体排放量(范围1和范围2) | REPORTDATE | xla去前缀变体 |
| `esg_ghgr1_wind` | 每百万元营收直接(范围1)温室气体排放 | REPORTDATE | xla去前缀变体 |
| `esg_ghgr2_wind` | 每百万元营收间接温室气体排放(范围2) | REPORTDATE | xla去前缀变体 |
| `esg_gpa02001` | 是否有股权激励计划 | REPORTDATE | xla去前缀变体 |
| `esg_gpa03002` | 薪酬委员会会议出席率 | REPORTDATE | xla去前缀变体 |
| `esg_gpa03003` | 薪酬委员会会议数 | REPORTDATE | xla去前缀变体 |
| `esg_gscore_wind` | 治理维度得分 | TRADEDATE | xla去前缀变体 |
| `esg_invention` | 有效专利总数 | TRADEDATE | xla去前缀变体 |
| `esg_mdc01002` | 公司是否有独立的公司社会责任报告 | REPORTDATE | xla去前缀变体 |
| `esg_mdc01003` | 第三方审查机构 | REPORTDATE | xla去前缀变体 |
| `esg_mdc01004` | 报告范围 | REPORTDATE | xla去前缀变体 |
| `esg_mdc01005` | 编制依据 | REPORTDATE | xla去前缀变体 |
| `esg_mdc01006` | 是否遵循/对照GRI标准 | REPORTDATE | xla去前缀变体 |
| `esg_mdc01007` | 是否遵循/对照联交所标准 | REPORTDATE | xla去前缀变体 |
| `esg_mgmtscore_wind` | ESG管理实践得分 | TRADEDATE | xla去前缀变体 |
| `esg_pplb_wind` | 普惠型小微企业贷款余额 | REPORTDATE | xla去前缀变体 |
| `esg_proportion` | ESG债券募集金额认定比例 |  | xla去前缀变体 |
| `esg_rating` | ESG评级 | TRADEDATE | xla去前缀变体 |
| `esg_rating_casvi` | 社会价值投资联盟ESG评级 | TRADEDATE | xla去前缀变体 |
| `esg_rating_ftserussell` | 富时罗素ESG评分 | TRADEDATE | xla去前缀变体 |
| `esg_rating_ssi` | 华证ESG评级 | TRADEDATE | xla去前缀变体 |
| `esg_rating_wind` | Wind ESG评级 | TRADEDATE | xla去前缀变体 |
| `esg_ratingdate_wind` | Wind ESG评级日期 | TRADEDATE | xla去前缀变体 |
| `esg_reptdate_wind` | ESG独立报告发布日期 | REPORTDATE | xla去前缀变体 |
| `esg_rpt_wind` | ESG独立报告名称 | REPORTDATE | xla去前缀变体 |
| `esg_sch01001` | 供应商数量 | REPORTDATE | xla去前缀变体 |
| `esg_sch01002` | 供应商本地化比例 | REPORTDATE | xla去前缀变体 |
| `esg_sch02001` | 本地化采购支出占比 | REPORTDATE | xla去前缀变体 |
| `esg_sch02002` | 接受ESG评估的供应商数量 | REPORTDATE | xla去前缀变体 |
| `esg_sco02001` | 志愿服务时长 | REPORTDATE | xla去前缀变体 |
| `esg_sco02002` | 注册志愿者人数 | REPORTDATE | xla去前缀变体 |
| `esg_score_wind` | Wind ESG综合得分 | TRADEDATE | xla去前缀变体 |
| `esg_sem01001` | 雇员总人数 | REPORTDATE | xla去前缀变体 |
| `esg_sem01002` | 员工流失率/离职率 | REPORTDATE | xla去前缀变体 |
| `esg_sem01003` | 兼职人员比例 | REPORTDATE | xla去前缀变体 |
| `esg_sem01004` | 劳动合同签订率 | REPORTDATE | xla去前缀变体 |
| `esg_sem01005` | 女性员工比例 | REPORTDATE | xla去前缀变体 |
| `esg_sem01006` | 少数裔员工比例 | REPORTDATE | xla去前缀变体 |
| `esg_sem02002` | 人均培训课时 | REPORTDATE | xla去前缀变体 |
| `esg_sem03001` | 工伤率 | REPORTDATE | xla去前缀变体 |
| `esg_sem03002` | 因工伤损失工作日数 | REPORTDATE | xla去前缀变体 |
| `esg_sem03003` | 职业病发生率 | REPORTDATE | xla去前缀变体 |
| `esg_sem03004` | 死亡事故数 | REPORTDATE | xla去前缀变体 |
| `esg_sem04001` | 医保覆盖率 | REPORTDATE | xla去前缀变体 |
| `esg_spc01001` | 客户投诉数量 | REPORTDATE | xla去前缀变体 |
| `esg_spc01002` | 客户满意度 | REPORTDATE | xla去前缀变体 |
| `esg_spc01003` | 是否有客户反馈系统 | REPORTDATE | xla去前缀变体 |
| `esg_spc02004` | 新增专利数 | REPORTDATE | xla去前缀变体 |
| `esg_sscore_wind` | 社会维度得分 | TRADEDATE | xla去前缀变体 |

<a id="分类-股东"></a>

## 股东（71 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `holder_amount` | 发行人债券机构持仓金额 | REPORTDATE、TYPE | xla去前缀变体 |
| `holder_avgholding` | 平均每户持有基金份额 | REPORTDATE | xla去前缀变体 |
| `holder_avgnum` | 户均持股 |  | 探测法实测 |
| `holder_avgpct` | 户均持股比例 | REPORTDATE | xla去前缀变体 |
| `holder_avgpctchange` | 相对上一报告期户均持股比例差 | REPORTDATE | xla去前缀变体 |
| `holder_controller` | 上市公司实际控制人名称(新增) | DEALDATE | xla去前缀变体 |
| `holder_controllerattr` | 实际控制人属性 | TRADEDATE | xla去前缀变体 |
| `holder_corp_holding` | 基金管理公司持有份额 | REPORTDATE | xla去前缀变体 |
| `holder_corp_holdingpct` | 基金管理公司持有比例 | REPORTDATE | xla去前缀变体 |
| `holder_detail` | 发行人债券机构持仓明细 | REPORTDATE、TYPE | xla去前缀变体 |
| `holder_feeder_holding` | ETF联接基金持有份额 | REPORTDATE | xla去前缀变体 |
| `holder_feeder_holdingpct` | ETF联接基金持有比例 | REPORTDATE | xla去前缀变体 |
| `holder_havgchange` | 户均持股数半年增长率(新增) | D | xla去前缀变体 |
| `holder_havgpctchange` | 户均持股比例半年增长率(新增) | D | xla去前缀变体 |
| `holder_minpb20_lyr` | 前20个交易日最低市净率(最近会计年度) | TRADEDATE | xla去前缀变体 |
| `holder_minpb20_mrq` | 前20个交易日最低市净率(最近报告期) | TRADEDATE | xla去前缀变体 |
| `holder_mngemp_holding` | 管理人员工持有份额(新增) | REPORTDATE | xla去前缀变体 |
| `holder_mngemp_holdingpct` | 管理人员工持有比例(新增) | REPORTDATE | xla去前缀变体 |
| `holder_mngemp_totalholding` | 管理人员工持有份额(合计) | REPORTDATE | xla去前缀变体 |
| `holder_mngemp_totalholdingpct` | 管理人员工持有比例(合计) | REPORTDATE | xla去前缀变体 |
| `holder_num` | 股东户数 |  | 探测法实测 |
| `holder_num2` | 股东户数 | REPORTDATE、Captype | xla去前缀变体 |
| `holder_pctbyfund` | 基金持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbygeneralcorp` | 一般法人持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbyhf` | 阳光私募持股比例 |  | xla原码 |
| `holder_pctbyinst` | 机构持股比例合计(新增) | D | xla去前缀变体 |
| `holder_pctbyinsur` | 保险公司持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbylnfcorp` | 非金融类上市公司持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbyqfii` | QFII持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbysec` | 券商持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbyssfund` | 社保基金持股比例(新增) | D | xla去前缀变体 |
| `holder_pctbytrustcorp` | 信托公司持股比例(新增) | D | xla去前缀变体 |
| `holder_pershld2` | 个人投资者持有份额(上市交易公告书) |  | xla去前缀变体 |
| `holder_pershldpct2` | 个人投资者持有比例(上市交易公告书) |  | xla去前缀变体 |
| `holder_personal_holding` | 个人投资者持有份额 | REPORTDATE | xla去前缀变体 |
| `holder_personal_holdingpct` | 个人投资者持有比例 | REPORTDATE | xla去前缀变体 |
| `holder_personal_totalholding` | 个人投资者持有份额(合计) | REPORTDATE | xla去前缀变体 |
| `holder_personal_totalholdingpct` | 个人投资者持有比例(合计) | REPORTDATE | xla去前缀变体 |
| `holder_price_esop` | 员工持股计划买入价格 | TRADEDATE | xla去前缀变体 |
| `holder_price_fellowon` | 定向增发价格 | TRADEDATE | xla去前缀变体 |
| `holder_price_majorshareholders` | 大股东增持价格 | TRADEDATE | xla去前缀变体 |
| `holder_price_mh` | 管理层增持价格 | TRADEDATE | xla去前缀变体 |
| `holder_price_stockbasedcompensation` | 股权激励行权价格 | TRADEDATE | xla去前缀变体 |
| `holder_qavgchange` | 户均持股数季度增长率(新增) | D | xla去前缀变体 |
| `holder_qavgpctchange` | 户均持股比例季度增长率(新增) | D | xla去前缀变体 |
| `holder_redmrptper` | 单一投资者报告期内赎回持有份额 | REPORTDATE、Year、InvestorType、Number | xla去前缀变体 |
| `holder_rptcontroller` | 公布实际控制人名称 | DEALDATE | xla去前缀变体 |
| `holder_sumt10quantity` | 前十大股东持股数量合计 | REPORTDATE | xla去前缀变体 |
| `holder_sumt5pct` | 前五大股东持股比例合计 | REPORTDATE | xla去前缀变体 |
| `holder_sumt5quantity` | 前五大股东持股数量合计 | REPORTDATE | xla去前缀变体 |
| `holder_tlttop10liqpct` | 前十大流通股东持股比例合计 | DEALDATE | xla去前缀变体 |
| `holder_top10liqquantity` | 前十大流通股东持股数量合计 |  | xla去前缀变体 |
| `holder_top10pct` | 前十大股东持股比例合计 |  | xla去前缀变体 |
| `holder_top10q_qoq` | 前十大流通股东持股数量环比 | REPORTDATE | xla去前缀变体 |
| `holder_top10quantity` | 前十大股东持股 |  | 探测法实测 |
| `holder_top5pct` | 前五大股东持股比例合计 | REPORTDATE | xla去前缀变体 |
| `holder_top5quantity` | 前五大股东持股数量合计 | REPORTDATE | xla去前缀变体 |
| `holder_totalbybank` | 银行持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbybysec` | 券商持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbybywmp` | 券商理财产品持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbycorppension` | 企业年金持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbyfinancecorp` | 财务公司持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbyfund` | 基金持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbygeneralcorp` | 一般法人持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbyhf` | 阳光私募持股数量 |  | xla原码 |
| `holder_totalbyinst` | 机构持股数量合计(新增) | D | xla去前缀变体 |
| `holder_totalbyinsur` | 保险公司持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbylnfcorp` | 非金融类上市公司持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbyqfii` | QFII持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbyssfund` | 社保基金持股数量(新增) | D | xla去前缀变体 |
| `holder_totalbytrustcorp` | 信托公司持股数量(新增) | D | xla去前缀变体 |

<a id="分类-股本"></a>

## 股本（86 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `share_cn` | 中资中介机构持股数量 | TRADEDATE | xla去前缀变体 |
| `share_cpct_cn` | 中资中介机构持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_cpct_hk` | 香港本地中介机构持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_cpct_hks` | 港股通持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_cpct_hksh` | 沪市港股通持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_cpct_hksz` | 深市港股通持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_cpct_os` | 国际中介机构持股/香港股 | TRADEDATE | xla去前缀变体 |
| `share_dr` | 已发行DR数量 | TRADEDATE | xla去前缀变体 |
| `share_freefloatshr_pct` | 自由流通股占总股本比例 | TRADEDATE | xla去前缀变体 |
| `share_h` | 香港上市股 |  | xla去前缀变体 |
| `share_hk` | 香港本地中介机构持股数量 | TRADEDATE | xla去前缀变体 |
| `share_hks` | 港股通持股数量 | TRADEDATE | xla去前缀变体 |
| `share_hksh` | 沪市港股通持股数量 | TRADEDATE | xla去前缀变体 |
| `share_hksz` | 深市港股通持股数量 | TRADEDATE | xla去前缀变体 |
| `share_issuing` | 已发行数量 | TRADEDATE | xla去前缀变体 |
| `share_issuing_mkt` | 流通股本 | TRADEDATE | xla去前缀变体 |
| `share_liqa_pct` | 流通A股占总股本比例 |  | xla去前缀变体 |
| `share_liqa_pledged` | 无限售股份质押数量 | TRADEDATE | xla去前缀变体 |
| `share_liqa_pledgedpct` | 无限售股份质押比例 | TRADEDATE | xla去前缀变体 |
| `share_liqb` | 流通B股 |  | xla去前缀变体 |
| `share_liqb_pct` | 流通B股占总股本比例 |  | xla去前缀变体 |
| `share_liqh_pct` | 流通H股占总股本比例 |  | xla去前缀变体 |
| `share_n` | 沪(深)股通持股数量 | TRADEDATE | xla去前缀变体 |
| `share_nontradable` | 股改前非流通股 |  | xla去前缀变体 |
| `share_nontradable_pct` | 非流通股合计占总股本比例 |  | xla去前缀变体 |
| `share_ntrd_prfshare` | 优先股(新增) | D | xla去前缀变体 |
| `share_ntrd_snormnger` | 高管股(新增) | D | xla去前缀变体 |
| `share_os` | 国际中介机构持股数量 | TRADEDATE | xla去前缀变体 |
| `share_otca` | 三板A股 |  | xla去前缀变体 |
| `share_otca_pct` | 三板A股占总股本比例(新增) | D | xla去前缀变体 |
| `share_otcb` | 三板B股 |  | xla去前缀变体 |
| `share_otcb_pct` | 三板B股占总股本比例(新增) | D | xla去前缀变体 |
| `share_otcrestricted` | 限售三板股 | TRADEDATE | xla去前缀变体 |
| `share_otcrestricted_backbone` | 限售股份(核心员工) | TRADEDATE | xla去前缀变体 |
| `share_otcrestricted_controller` | 限售股份(控股股东或实际控制人) | TRADEDATE | xla去前缀变体 |
| `share_otcrestricted_others` | 限售股份(其他) | TRADEDATE | xla去前缀变体 |
| `share_otctradable` | 流通三板股 | DATE | xla去前缀变体 |
| `share_otctradable_backbone` | 流通股(核心员工) | TRADEDATE | xla去前缀变体 |
| `share_otctradable_controller` | 流通股(控股股东或实际控制人) | TRADEDATE | xla去前缀变体 |
| `share_otctradable_others` | 流通股(其他) | TRADEDATE | xla去前缀变体 |
| `share_oversea` | 境外流通股 |  | xla去前缀变体 |
| `share_oversea_pct` | 海外上市股占总股本比例(新增) | D | xla去前缀变体 |
| `share_pct_cn` | 中资中介机构持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pct_hk` | 香港本地中介机构持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pct_hks` | 港股通持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pct_hksh` | 沪市港股通持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pct_hksz` | 深市港股通持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pct_n` | 沪(深)股通持股占比 | TRADEDATE | xla去前缀变体 |
| `share_pledgeda_pct_largestholder` | 大股东累计质押数占持股数比例 | TRADEDATE | xla去前缀变体 |
| `share_restricted_m` | 限售股份(高管持股) | TRADEDATE | xla去前缀变体 |
| `share_restricted_pct` | 股改限售股份占总股本比例 |  | xla去前缀变体 |
| `share_restricteda` | 限售A股 |  | xla去前缀变体 |
| `share_restricteda_pct` | 限售A股占总股本比例(新增) | D | xla去前缀变体 |
| `share_restricteda_pledged` | 有限售股份质押数量 | TRADEDATE | xla去前缀变体 |
| `share_restricteda_pledgedpct` | 有限售股份质押比例 | TRADEDATE | xla去前缀变体 |
| `share_restrictedb` | 限售B股 |  | xla去前缀变体 |
| `share_restrictedb_pct` | 限售B股占总股本比例(新增) | D | xla去前缀变体 |
| `share_rsp` | 有限售股份质押待购回余量 | TRADEDATE | xla去前缀变体 |
| `share_rtd_bance` | 未流通数量 | TRADEDATE | xla去前缀变体 |
| `share_rtd_datatype` | 解禁数据类型 | TRADEDATE | xla去前缀变体 |
| `share_rtd_datatype_fwd` | 指定日之后最近一次解禁数据类型 | TRADEDATE | xla去前缀变体 |
| `share_rtd_domesjur` | 限售股份(境内法人持股)(新增) | D | xla去前缀变体 |
| `share_rtd_domesnp` | 限售股份(境内自然人持股)(新增) | D | xla去前缀变体 |
| `share_rtd_frgnjur` | 限售股份(境外法人持股)(新增) | D | xla去前缀变体 |
| `share_rtd_frgnnp` | 限售股份(境外自然人持股)(新增) | D | xla去前缀变体 |
| `share_rtd_inst` | 限售股份(机构配售股份)(新增) | D | xla去前缀变体 |
| `share_rtd_state` | 限售股状态 |  | 探测法实测 |
| `share_rtd_statejur` | 限售股份(国有法人持股)(新增) | D | xla去前缀变体 |
| `share_rtd_subfrgn` | 限售股份(外资持股合计)(新增) | D | xla去前缀变体 |
| `share_rtd_subotherdomes` | 限售股份(其他内资持股合计)(新增) | D | xla去前缀变体 |
| `share_rtd_unlockingdate` | 限售解禁日期 | TRADEDATE | xla去前缀变体 |
| `share_rtd_unlockingdate_fwd` | 指定日之后最近一次解禁日期 | TRADEDATE | xla去前缀变体 |
| `share_shortamount` | 持有淡仓金额合计 | TRADEDATE | xla去前缀变体 |
| `share_shortshares` | 持有淡仓股数合计 | TRADEDATE | xla去前缀变体 |
| `share_totala` | A股总股本 |  | 探测法实测 |
| `share_totala_pct` | A股合计占总股本比例(新增) | D | xla去前缀变体 |
| `share_totalb` | B股合计 |  | xla去前缀变体 |
| `share_totalb_pct` | B股合计占总股本比例(新增) | D | xla去前缀变体 |
| `share_totalotc` | 三板合计 |  | xla去前缀变体 |
| `share_totalotc_pct` | 三板合计占总股本比例(新增) | D | xla去前缀变体 |
| `share_totalrestricted` | 限售股合计 |  | xla去前缀变体 |
| `share_totaltradable` | 流通股合计 |  | xla去前缀变体 |
| `share_totshares_pre` | 上市前总股本 |  | xla去前缀变体 |
| `share_tradable_current` | 本期解禁数量 | TRADEDATE | xla去前缀变体 |
| `share_tradable_current_fwd` | 指定日之后最近一次解禁数量 | TRADEDATE | xla去前缀变体 |
| `share_tradable_pct` | 流通股合计占总股本比例 |  | xla去前缀变体 |

<a id="分类-货币基金"></a>

## 货币基金（13 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `mmf_annualizedyield` | 7日年化收益率 |  | xla去前缀变体 |
| `mmf_avgannualizedyield` | 区间7日年化收益率均值 | BEGINDATE、EndDate | xla去前缀变体 |
| `mmf_avgunityield` | 区间万份基金单位收益均值 | BEGINDATE、EndDate | xla去前缀变体 |
| `mmf_bondtoasset` | 债券投资占基金资产总值的比例 | REPORTDATE | xla去前缀变体 |
| `mmf_carryover` | 份额结转方式 |  | xla去前缀变体 |
| `mmf_carryoverdate` | 份额结转日期类型 |  | xla去前缀变体 |
| `mmf_deposittoasset` | 银行存款和清算备付金合计占基金资产总值的比例 | REPORTDATE | xla去前缀变体 |
| `mmf_differentptmtonav` | 各期限资产占基金资产净值比例 | REPORTDATE | xla去前缀变体 |
| `mmf_reverserepotoasset` | 买入返售证券占基金资产总值的比例 | REPORTDATE | xla去前缀变体 |
| `mmf_totalunityield` | 区间万份基金单位收益总值 |  | xla去前缀变体 |
| `mmf_unityield` | 万份基金单位收益 |  | xla去前缀变体 |
| `mmf_varannualizedyield` | 区间7日年化收益率方差 | BEGINDATE、EndDate | xla去前缀变体 |
| `mmf_varunityield` | 区间万份基金单位收益方差 | BEGINDATE、EndDate | xla去前缀变体 |

<a id="分类-发行"></a>

## 发行（37 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `issue_amountmax` | 发行金额上限 |  | xla去前缀变体 |
| `issue_announcedate` | 发行公告日 |  | xla去前缀变体 |
| `issue_cef_inipurchase` | 封闭式基金认购数量(新增) |  | xla去前缀变体 |
| `issue_cef_oversub` | 封闭式基金超额认购倍数(新增) |  | xla去前缀变体 |
| `issue_cef_succratio` | 封闭式基金中签率(新增) |  | xla去前缀变体 |
| `issue_channel` | 产品发行渠道 |  | xla去前缀变体 |
| `issue_coordinator` | 基金发行协调人(新增) |  | xla去前缀变体 |
| `issue_date` | 发行日期(新增) |  | xla去前缀变体 |
| `issue_nominator` | 基金上市推荐人(新增) |  | xla去前缀变体 |
| `issue_object` | 发行对象(新增) |  | xla去前缀变体 |
| `issue_oef_confirmdate` | 认购比例确认公告日 |  | xla去前缀变体 |
| `issue_oef_confirmratio` | 认购份额确认比例 |  | xla去前缀变体 |
| `issue_oef_days` | 认购天数 |  | xla去前缀变体 |
| `issue_oef_dnddateinst` | 机构投资者设立认购终止日(新增) |  | xla去前缀变体 |
| `issue_oef_enddateind` | 个人投资者认购终止日(新增) |  | xla去前缀变体 |
| `issue_oef_maxamtind` | 个人投资者认购金额上限(新增) |  | xla去前缀变体 |
| `issue_oef_maxamtinst` | 封闭期机构投资者认购上限(新增) |  | xla去前缀变体 |
| `issue_oef_maxcollection` | 募集份额上限 |  | xla去前缀变体 |
| `issue_oef_minamtind` | 个人投资者认购金额下限(新增) |  | xla去前缀变体 |
| `issue_oef_minamtinst` | 封闭期机构投资者认购下限(新增) |  | xla去前缀变体 |
| `issue_oef_mthdind` | 个人投资者认购方式(新增) |  | xla去前缀变体 |
| `issue_oef_mthdinst` | 封闭期机构投资者认购方式(新增) |  | xla去前缀变体 |
| `issue_oef_numpurchasers` | 开放式基金认购户数(新增) |  | xla去前缀变体 |
| `issue_oef_startdateind` | 个人投资者认购起始日(新增) |  | xla去前缀变体 |
| `issue_oef_startdateinst` | 机构投资者设立认购起始日(新增) |  | xla去前缀变体 |
| `issue_officialdocdate` | 证监会/发改委批文日 |  | xla去前缀变体 |
| `issue_price` | 上市基金发行价格(新增) |  | xla去前缀变体 |
| `issue_rasing_isenddeferred` | 是否延长募集期 |  | xla去前缀变体 |
| `issue_rasing_isendearly` | 是否提前结束募集 |  | xla去前缀变体 |
| `issue_rasing_isstartdeferred` | 是否延期募集 |  | xla去前缀变体 |
| `issue_rasing_isstartearly` | 是否提前开始募集 |  | xla去前缀变体 |
| `issue_registrar` | 基金注册与过户登记人(新增) |  | xla去前缀变体 |
| `issue_terms` | 发行条款 |  | xla去前缀变体 |
| `issue_totalsize` | 发行总规模 |  | xla去前缀变体 |
| `issue_totalunit` | 发行总份额(新增) |  | xla去前缀变体 |
| `issue_type` | 发行方式(新增) |  | xla去前缀变体 |
| `issue_unit` | 发行份额 |  | xla去前缀变体 |

<a id="分类-利率-评级"></a>

## 利率/评级（23 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `rate_agencybond` | 债项评级机构 | TRADEDATE、RATINGAGENCY | xla去前缀变体 |
| `rate_agencyguarantor` | 担保人评级评级机构 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_agencyissuer` | 主体评级评级机构 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_beginguarantor` | 发行时担保人评级 |  | xla去前缀变体 |
| `rate_changesofrating` | 最新债项评级变动方向 |  | xla去前缀变体 |
| `rate_chngbond` | 债项评级变动方向 | TRADEDATE、RATINGAGENCY | xla去前缀变体 |
| `rate_chngguarantor` | 担保人评级变动方向 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_chngissuer` | 主体评级变动方向 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_default_csi` | 隐含违约率(中证指数) | TRADEDATE | xla去前缀变体 |
| `rate_fwdguarantor` | 担保人评级展望 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_fwdissuer` | 主体评级展望 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |
| `rate_historicalmir_cnbd` | 市场历史隐含评级(中债) |  | xla去前缀变体 |
| `rate_issuer` | 发债主体历史信用等级 |  | xla去前缀变体 |
| `rate_lateguarantorchng` | 担保人最新评级变动方向 |  | xla去前缀变体 |
| `rate_lateguarantordate` | 担保人最新评级日期 |  | xla去前缀变体 |
| `rate_lateguarantorfwd` | 担保人最新评级展望 |  | xla去前缀变体 |
| `rate_lateissuerchng` | 发行人最新评级变动方向 |  | xla去前缀变体 |
| `rate_latest1` | 最新债项评级日期(指定机构) | RATINGAGENCY | xla去前缀变体 |
| `rate_latestcredit_mainagency` | 债项评级(主评机构) |  | xla去前缀变体 |
| `rate_latestmir_cnbd` | 市场隐含评级(中债) | TRADEDATE | xla去前缀变体 |
| `rate_latestmir_csi` | 隐含评级(中证指数) | TRADEDATE | xla去前缀变体 |
| `rate_ratebond` | 债项评级 | TRADEDATE、RATINGAGENCY | xla去前缀变体 |
| `rate_rateguarantor` | 担保人评级 | TRADEDATE、RatedCompanyType、RATINGAGENCY | xla去前缀变体 |

<a id="分类-收益率"></a>

## 收益率（5 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `yield_cfets` | 估价收益率(中国货币网) | TRADEDATE | xla去前缀变体 |
| `yield_cnbd` | 估价收益率(%) |  | xla去前缀变体 |
| `yield_csi` | 估价收益率(中证指数) |  | xla去前缀变体 |
| `yield_csi1` | 估价收益率(中证指数) | DEALDATE、Credibility | xla去前缀变体 |
| `yield_shc` | 估价收益率(上海清算所) |  | xla去前缀变体 |

<a id="分类-融资融券"></a>

## 融资融券（11 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `margin` | 交易保证金 |  | xla去前缀变体 |
| `margin_guaranteedstocksmarketvalue` | 融资融券担保股票市值 | TRADEDATE | xla去前缀变体 |
| `margin_marketvalueratio` | 担保证券市值占该证券总市值比重 | TRADEDATE | xla去前缀变体 |
| `margin_new` | 交易保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `margin_purchasewithborrowedmoney_net` | 融资净买入额 | TRADEDATE | xla去前缀变体 |
| `margin_salerepayamount` | 融券偿还额 | TRADEDATE | xla去前缀变体 |
| `margin_saletradingamount` | 融券卖出额 | TRADEDATE | xla去前缀变体 |
| `margin_shortamountint` | 区间融券卖出额 | StartDate、EndDate | xla去前缀变体 |
| `margin_shortamountrepayint` | 区间融券偿还额 | StartDate、EndDate | xla去前缀变体 |
| `margin_shortselleopbal` | 转融券期末余额 | TRADEDATE | xla去前缀变体 |
| `margin_sinstccolltrlratio` | 单一股票担保物比例 | TRADEDATE | xla去前缀变体 |

<a id="分类-财务分析"></a>

## 财务分析（90 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `fa_abpturndays` | 应付账款及应付票据周转天数 | REPORTDATE | xla去前缀变体 |
| `fa_abrturndays` | 应收账款及应收票据周转天数 | REPORTDATE | xla去前缀变体 |
| `fa_adminexpense_ttm` | 管理费用(TTM) |  | xla去前缀变体 |
| `fa_adminexpensetogr_ttm` | 管理费用／营业总收入(TTM) |  | xla去前缀变体 |
| `fa_apnpturn` | 应付账款及应付票据周转率 | REPORTDATE | xla去前缀变体 |
| `fa_arnrturn` | 应收账款及应收票据周转率 | REPORTDATE | xla去前缀变体 |
| `fa_arturn_reserve` | 应收账款周转率(含坏账准备) | REPORTDATE | xla去前缀变体 |
| `fa_arturn_ttm` | 应收账款周转率(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_bps` | 每股净资产BPS | REPORTDATE | xla去前缀变体 |
| `fa_cagr_or` | 营业收入复合年增长率 | Year、N | xla去前缀变体 |
| `fa_cagr_ta` | 资产总计复合年增长率 | Year、N | xla去前缀变体 |
| `fa_cashflow_ttm` | 现金净流量(TTM) |  | xla去前缀变体 |
| `fa_cashturnratio` | 现金周转率 | REPORTDATE | xla去前缀变体 |
| `fa_caturn_ttm` | 流动资产周转率(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_cfps_ttm` | 每股现金流量净额(TTM) |  | xla去前缀变体 |
| `fa_crofll` | 长期债务资本化比率 | REPORTDATE | xla去前缀变体 |
| `fa_current` | 流动比率 | REPORTDATE | xla去前缀变体 |
| `fa_da` | 当期计提折旧与摊销 | REPORTDATE | xla去前缀变体 |
| `fa_debttoequity` | 产权比率(负债合计／归属母公司股东的权益) | REPORTDATE | xla去前缀变体 |
| `fa_debttoeqy` | 净资产负债率 | REPORTDATE | xla去前缀变体 |
| `fa_deductedprofit_1` | 扣除非经常性损益后归属母公司股东的净利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `fa_dps` | 每股派息 |  | xla去前缀变体 |
| `fa_ebit_ttm` | 息税前利润(TTM) |  | xla去前缀变体 |
| `fa_ebitda_ttm` | EBITDA(TTM反推法) | REPORTDATE | xla去前缀变体 |
| `fa_ebittointerest` | 已获利息倍数(EBIT／利息费用) | REPORTDATE | xla去前缀变体 |
| `fa_ebt_ttm` | 利润总额(TTM) |  | xla去前缀变体 |
| `fa_eps_basic` | 每股收益EPS-基本 | REPORTDATE | xla去前缀变体 |
| `fa_eps_diluted` | 每股收益EPS-稀释 | REPORTDATE | xla去前缀变体 |
| `fa_equitytointerestdebt` | 归属母公司股东的权益／带息债务 | REPORTDATE | xla去前缀变体 |
| `fa_errorcorrectiondate` | 会计差错更正披露日期 | REPORTDATE | xla去前缀变体 |
| `fa_errorcorrectionornot` | 是否存在会计差错更正 | REPORTDATE | xla去前缀变体 |
| `fa_expensetosales_ttm` | 销售期间费用率(TTM) |  | xla去前缀变体 |
| `fa_fcfe` | 股权自由现金流量FCFE | REPORTDATE | xla去前缀变体 |
| `fa_fcfeps` | 每股股东自由现金流量 | REPORTDATE | xla去前缀变体 |
| `fa_fcff` | 企业自由现金流量FCFF | REPORTDATE | xla去前缀变体 |
| `fa_fcffps` | 每股企业自由现金流量 | REPORTDATE | xla去前缀变体 |
| `fa_finaexpense_ttm` | 财务费用(TTM) |  | xla去前缀变体 |
| `fa_finaexpensetogr_ttm` | 财务费用／营业总收入(TTM) |  | xla去前缀变体 |
| `fa_gc_ttm` | 营业总成本(TTM) |  | xla去前缀变体 |
| `fa_gr_ttm` | 营业总收入(TTM) |  | xla去前缀变体 |
| `fa_grossprofitmargin_ttm` | 销售毛利率(TTM) |  | xla去前缀变体 |
| `fa_grps` | 每股营业总收入 | REPORTDATE | xla去前缀变体 |
| `fa_impairtogr_ttm` | 资产减值损失／营业总收入(TTM) |  | xla去前缀变体 |
| `fa_interestdebt` | 带息债务 | REPORTDATE | xla去前缀变体 |
| `fa_interestexpense_ttm` | 利息支出(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_investcapital` | 全部投入资本 | REPORTDATE | xla去前缀变体 |
| `fa_latelyyear2` | 最新年报年份 | TRADEDATE | xla去前缀变体 |
| `fa_lyr_bt` | 最新年报 | TRADEDATE | xla去前缀变体 |
| `fa_netdebt` | 净债务 | REPORTDATE | xla去前缀变体 |
| `fa_netdebtratio` | 净负债率 | REPORTDATE | xla去前缀变体 |
| `fa_netprofit_ttm` | 归属母公司股东的净利润(TTM) |  | xla去前缀变体 |
| `fa_netprofitcashcover` | 净利润现金含量 | REPORTDATE | xla去前缀变体 |
| `fa_netprofitmargin_ttm` | 销售净利率(TTM) |  | xla去前缀变体 |
| `fa_netprofittoor_ttm` | 归属母公司股东的净利润/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_netturndays2` | 净营业周期(含应收应付票据) | REPORTDATE | xla去前缀变体 |
| `fa_noneinterestdebt` | 无息负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `fa_ocfps_ttm` | 每股经营活动产生的现金流量净额(TTM) |  | xla去前缀变体 |
| `fa_ocftodebt` | 经营活动产生的现金流量净额／负债合计 | REPORTDATE | xla去前缀变体 |
| `fa_ocftoor` | 经营活动产生的现金流量净额／营业收入 | REPORTDATE | xla去前缀变体 |
| `fa_ocftoor_ttm` | 经营活动产生的现金流量净额／营业收入(TTM) |  | xla去前缀变体 |
| `fa_op_ttm` | 营业利润(TTM) |  | xla去前缀变体 |
| `fa_optogr_ttm` | 营业利润／营业总收入(TTM) |  | xla去前缀变体 |
| `fa_optoor_ttm` | 营业利润/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_or_ttm` | 营业收入(TTM) |  | xla去前缀变体 |
| `fa_orps` | 每股营业收入 | REPORTDATE | xla去前缀变体 |
| `fa_performancechan` | 业绩说明会召开渠道 | REPORTDATE | xla去前缀变体 |
| `fa_performanceform` | 业绩说明会召开形式 | REPORTDATE | xla去前缀变体 |
| `fa_profit_ttm` | 净利润(TTM) |  | xla去前缀变体 |
| `fa_profitpp` | 人均创利 |  | xla去前缀变体 |
| `fa_profittogr_ttm` | 净利润／营业总收入(TTM) |  | xla去前缀变体 |
| `fa_quick` | 速动比率 | REPORTDATE | xla去前缀变体 |
| `fa_rdexp_yoy` | 研发费用同比增长 | REPORTDATE | xla去前缀变体 |
| `fa_retainedps` | 每股留存收益 | REPORTDATE | xla去前缀变体 |
| `fa_revenuepp` | 人均创收 |  | xla去前缀变体 |
| `fa_roa_ttm` | 总资产净利率ROA(TTM) |  | xla去前缀变体 |
| `fa_roe_avg` | 净资产收益率ROE-增发条件 | REPORTDATE | xla去前缀变体 |
| `fa_roe_diluted` | 净资产收益率ROE(摊薄) | REPORTDATE | xla去前缀变体 |
| `fa_roe_exbasic` | 净资产收益率ROE(扣除／加权) | REPORTDATE | xla去前缀变体 |
| `fa_roe_exdiluted` | 净资产收益率ROE(扣除／摊薄) | REPORTDATE | xla去前缀变体 |
| `fa_roe_ttm` | 净资产收益率ROE(TTM) |  | xla去前缀变体 |
| `fa_roe_ttmavg` | 净资产收益率(TTM,平均) | REPORTDATE | xla去前缀变体 |
| `fa_roic_ttm` | 投入资本回报率(TTM) | REPORTDATE | xla原码 |
| `fa_salary` | 员工薪酬 | Year | xla去前缀变体 |
| `fa_salarypp` | 人均薪酬 |  | xla去前缀变体 |
| `fa_salarypp_cost` | 费用化人均薪酬 | Year | xla去前缀变体 |
| `fa_stdebtratio` | 现金短债比 | REPORTDATE | xla去前缀变体 |
| `fa_tangibleasset` | 有形资产 | REPORTDATE | xla去前缀变体 |
| `fa_tangibleassettonetdebt` | 有形资产／净债务 | REPORTDATE | xla去前缀变体 |
| `fa_tax_ttm` | 所得税(TTM) | REPORTDATE | xla去前缀变体 |
| `fa_undistributedps` | 每股未分配利润 | REPORTDATE | xla去前缀变体 |

<a id="分类-单季财务"></a>

## 单季财务（37 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `qfa_adminexpensetogr` | 单季度.管理费用／营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_adminexpensetogr2` | 单季度.管理费用/营业总收入(不含研发费用) | REPORTDATE | xla去前缀变体 |
| `qfa_cgrgr` | 单季度.营业总收入环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_cgrnetprofit` | 单季度.归属母公司股东的净利润环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_cgrop` | 单季度.营业利润环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_cgrprofit` | 单季度.净利润环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_cgrsales` | 单季度.营业收入环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_deductedprofit` | 单季度.扣除非经常损益后的净利润 | REPORTDATE | xla去前缀变体 |
| `qfa_deductedprofit_cgr` | 单季度.扣除非经常性损益后的净利润环比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_deductedprofitmargin` | 单季度.扣非销售净利率 | REPORTDATE | xla去前缀变体 |
| `qfa_deductedprofittoprofit` | 单季度.扣除非经常损益后的净利润／净利润 | REPORTDATE | xla去前缀变体 |
| `qfa_eps` | 单季度.每股收益EPS | REPORTDATE | xla去前缀变体 |
| `qfa_finaexpensetogr` | 单季度.财务费用／营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_gctogr` | 单季度.营业总成本／营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_grossmargin` | 单季度.毛利 | REPORTDATE、TYPE | xla去前缀变体 |
| `qfa_grossprofitmargin` | 单季度.销售毛利率 | REPORTDATE | xla去前缀变体 |
| `qfa_investincome` | 单季度.价值变动净收益 | REPORTDATE | xla去前缀变体 |
| `qfa_investincometoebt` | 单季度.价值变动净收益／利润总额 | REPORTDATE | xla去前缀变体 |
| `qfa_netprofitmargin` | 单季度.销售净利率 | REPORTDATE | xla去前缀变体 |
| `qfa_ocftoor` | 单季度.经营活动产生的现金流量净额／营业收入 | REPORTDATE | xla去前缀变体 |
| `qfa_operateincome` | 单季度.经营活动净收益 | REPORTDATE | xla去前缀变体 |
| `qfa_operateincometoebt` | 单季度.经营活动净收益／利润总额 | REPORTDATE | xla去前缀变体 |
| `qfa_optogr` | 单季度.营业利润／营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_profittogr` | 单季度.净利润／营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_rdetogr` | 单季度.研发费用/营业总收入 | REPORTDATE | xla去前缀变体 |
| `qfa_roa` | 单季度.总资产净利率ROA | REPORTDATE | xla去前缀变体 |
| `qfa_roe` | 单季度.净资产收益率ROE | REPORTDATE | xla去前缀变体 |
| `qfa_roe_deducted` | 单季度.净资产收益率(扣除非经常损益) | REPORTDATE | xla去前缀变体 |
| `qfa_salescashintoor` | 单季度.销售商品提供劳务收到的现金／营业收入 | REPORTDATE | xla去前缀变体 |
| `qfa_yoycf` | 单季度.现金净流量(同比增长率) | REPORTDATE | xla去前缀变体 |
| `qfa_yoyeps` | 单季度.每股收益(同比增长率) | REPORTDATE | xla去前缀变体 |
| `qfa_yoygr` | 单季度.营业总收入同比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_yoynetprofit` | 单季净利润同比 |  | 探测法实测 |
| `qfa_yoyocf` | 单季度.经营性现金净流量(同比增长率) | REPORTDATE | xla去前缀变体 |
| `qfa_yoyop` | 单季度.营业利润同比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_yoyprofit` | 单季度.净利润同比增长率 | REPORTDATE | xla去前缀变体 |
| `qfa_yoysales` | 单季营收同比 |  | 探测法实测 |

<a id="分类-技术指标"></a>

## 技术指标（4 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `tech_downnum` | 指数成份下跌数量 | TRADEDATE | xla去前缀变体 |
| `tech_limitdownnum` | 指数成份跌停数量 | TRADEDATE | xla去前缀变体 |
| `tech_limitupnum` | 指数成份涨停数量 | TRADEDATE | xla去前缀变体 |
| `tech_upnum` | 指数成份上涨数量 | TRADEDATE | xla去前缀变体 |

<a id="分类-风险指标"></a>

## 风险指标（86 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `risk_alpha` | Alpha(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_alpha_bm` | Alpha(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod | xla去前缀变体 |
| `risk_annualintervalyield` | 区间收益率(年化) | StartDate、EndDate | xla去前缀变体 |
| `risk_annualintervalyield_calc` | 7日年化收益率(计算) | TRADEDATE | xla去前缀变体 |
| `risk_annualintervalyield_inclph` | 7日年化收益率(含节假日) | TRADEDATE | xla去前缀变体 |
| `risk_annualintervalyield_tradedate` | 区间收益率(工作日年化) | StartDate、EndDate | xla去前缀变体 |
| `risk_annualpha` | Alpha(年化) | StartDate、EndDate、CT、CM、UI | xla去前缀变体 |
| `risk_annualpha_bm` | Alpha(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod | xla去前缀变体 |
| `risk_annualvolranking` | 年化波动率同类排名 | BEGINDATE、EndDate | xla去前缀变体 |
| `risk_annuinforatio` | 信息比率(年化) | StartDate、EndDate、CT、CM、NRY、UI | xla去前缀变体 |
| `risk_annujensen` | Jensen(年化) | StartDate、EndDate、CM、NRY、UI、CT | xla去前缀变体 |
| `risk_annujensen_bm` | Jensen(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield | xla去前缀变体 |
| `risk_annusharpe` | Sharpe(年化) | StartDate、EndDate、CT、CM、NRY | xla去前缀变体 |
| `risk_annusortino` | 索丁诺比率(年化) | StartDate、EndDate、CT、CM、NRY | xla去前缀变体 |
| `risk_annustdev` | 收益标准差(年化) | StartDate、EndDate、CT、CM | xla去前缀变体 |
| `risk_annutrackerror` | 跟踪误差(年化) | StartDate、EndDate、CT、CM、UI | xla去前缀变体 |
| `risk_annutrackerror_index` | 跟踪误差(跟踪指数,年化) | StartDate、EndDate | xla去前缀变体 |
| `risk_annutreynor` | Treynor(年化) | StartDate、EndDate、CT、CM、NRY、UI | xla去前缀变体 |
| `risk_annutreynor_bm` | Treynor(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield | xla去前缀变体 |
| `risk_avgreturn` | 平均收益率 |  | xla原码 |
| `risk_avgriskreturn` | 平均风险收益率 |  | xla去前缀变体 |
| `risk_avgtrackdeviation_benchmark` | 区间跟踪偏离度均值(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod | xla去前缀变体 |
| `risk_avgtrackdeviation_trackindex` | 区间跟踪偏离度均值(跟踪指数) | StartDate、EndDate、CalcTerm、CalcMethod | xla去前缀变体 |
| `risk_beta` | 波Beta | StartDate、EndDate、Period、TYPE、INDEX | xla原码 |
| `risk_beta_bm` | Beta(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod | xla去前缀变体 |
| `risk_betaunincometaxrate` | Beta(剔除所得税率) | StartDate、EndDate | xla去前缀变体 |
| `risk_correcoefficient` | 相关系数 | StartDate、EndDate、CT、CM、WINDCODE2 | xla去前缀变体 |
| `risk_correcoefficient_trackindex` | 相关系数(跟踪指数) | StartDate、EndDate | xla去前缀变体 |
| `risk_cvar` | 条件VaR | StartDate、EndDate | xla去前缀变体 |
| `risk_downside` | 回撤(相对前期高点) | TRADEDATE | xla去前缀变体 |
| `risk_downsiderisk` | 下行风险 |  | xla去前缀变体 |
| `risk_downsideriskranking` | 下行风险同类排名 | BEGINDATE、EndDate | xla去前缀变体 |
| `risk_downsidestdev` | 下行标准差(新增) | StartDate、EndDate、CT、CM、TY | xla去前缀变体 |
| `risk_drawdown` | 区间回撤(相对前期高点) | StartDate、EndDate | xla去前缀变体 |
| `risk_duration` | 基金组合久期 | REPORTDATE | xla去前缀变体 |
| `risk_durationupdate` | 基金组合久期(基于利率风险计算) | REPORTDATE | xla去前缀变体 |
| `risk_eshistorical` | 历史平均损失值ES | StartDate、EndDate | xla去前缀变体 |
| `risk_esparam` | 参数平均损失值ES | StartDate、EndDate | xla去前缀变体 |
| `risk_gemavgriskreturn` | 几何平均风险收益率 |  | xla去前缀变体 |
| `risk_gemreturn` | 几何平均收益率(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_hvar` | 历史VaR | StartDate、EndDate | xla去前缀变体 |
| `risk_inforatio` | 信息比率(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_inforatio_trackindex` | 信息比率(跟踪指数) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield | xla去前缀变体 |
| `risk_inforatioranking` | 信息比率同类排名(新增) | StartDate、EndDate | xla去前缀变体 |
| `risk_interestsensitivity` | 市场利率敏感性 | REPORTDATE | xla去前缀变体 |
| `risk_jensen` | Jensen(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_jensen_bm` | Jensen(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield | xla去前缀变体 |
| `risk_maxdownside` | 最大回撤 | StartDate、EndDate | xla去前缀变体 |
| `risk_maxdownside_date` | 最大回撤区间日期 | StartDate、EndDate | xla去前缀变体 |
| `risk_maxdownside_recoverdays` | 最大回撤恢复天数 | StartDate、EndDate | xla去前缀变体 |
| `risk_maxdownsidelistedfund` | 最大回撤(行情) | StartDate、EndDate | xla去前缀变体 |
| `risk_maxupside` | 最大上涨 | StartDate、EndDate | xla去前缀变体 |
| `risk_navoverbenchannualreturn` | 区间净值超越基准年化收益率 |  | xla去前缀变体 |
| `risk_nonsysrisk` | 非系统风险(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_premium` | 风险溢价 | TRADEDATE、No_Risk_Yield、Yield_Standard | xla去前缀变体 |
| `risk_premium2` | 风险溢价(倍) | TRADEDATE、No_Risk_Yield、Yield_Standard | xla去前缀变体 |
| `risk_r2` | 可决系数(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_returnyearly` | 年化收益率(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_returnyearly_naturalday` | 区间收益率(自然日年化) | StartDate、EndDate | xla去前缀变体 |
| `risk_returnyearly_tradedate` | 年化收益率(工作日) | StartDate | xla去前缀变体 |
| `risk_sharpe` | Sharpe(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_siml_avgalpha` | Alpha同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgannualpha` | Alpha(年化)同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgannusharpe` | Sharpe(年化)同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgannusortino` | Sortino(年化)同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgbeta` | Beta同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgdownsiderisk` | 下行风险同类平均 | StartDate、EndDate | xla去前缀变体 |
| `risk_siml_avgmaxdownside` | 最大回撤同类平均 | StartDate、EndDate | xla去前缀变体 |
| `risk_siml_avgsharpe` | Sharpe同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgsortino` | Sortino同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_siml_avgstdevyearly` | 年化波动率同类平均 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `risk_sortino` | 索丁诺比率 | BEGINDATE、EndDate | xla去前缀变体 |
| `risk_stdev` | 波动率 |  | xla原码 |
| `risk_stdevclose` | 收盘价标准差 | StartDate、EndDate、Cycle | xla去前缀变体 |
| `risk_stdevyearly` | 年化波动率(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_stock` | 选股能力(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_stockranking` | 选股能力同类排名(新增) | StartDate、EndDate | xla去前缀变体 |
| `risk_time` | 选时能力(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_timeranking` | 选时能力同类排名(新增) | StartDate、EndDate | xla去前缀变体 |
| `risk_trackdeviation_trackindex` | 日跟踪偏离度(跟踪指数) | TRADEDATE | xla去前缀变体 |
| `risk_trackerror` | 跟踪误差(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_trackerror_trackindex` | 跟踪误差(跟踪指数) | StartDate、EndDate | xla去前缀变体 |
| `risk_trackerrorranking` | 跟踪误差排名 | BEGINDATE、EndDate | xla去前缀变体 |
| `risk_treynor` | Treynor(新增) | TD1、TD2 | xla去前缀变体 |
| `risk_treynor_bm` | Treynor(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield | xla去前缀变体 |
| `risk_upsidestdev` | 上行标准差(新增) | StartDate、EndDate、CT、CM、TY | xla去前缀变体 |

<a id="分类-估值"></a>

## 估值（51 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `pe` | 市盈率PE |  | 探测法实测 |
| `pe_lyr` | 市盈率PE(LYR) |  | 探测法实测 |
| `pe_ttm` | 市盈率PE(TTM) |  | 探测法实测 |
| `val_bshrmarketvalue` | 流通B股市值(人民币) |  | xla去前缀变体 |
| `val_bshrmarketvalue2` | 流通B股市值(交易币种) |  | xla去前缀变体 |
| `val_bshrmarketvalue3` | B股市值(含限售股,折人民币) |  | xla去前缀变体 |
| `val_bshrmarketvalue4` | B股市值(含限售股,交易币种) |  | xla去前缀变体 |
| `val_dividend_percentile` | 股息率分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_dividendyield2_issuer` | 发布方股息率(近12个月) | TRADEDATE | xla去前缀变体 |
| `val_dividendyield2_issuer2` | 发布方股息率(近12个月,调整) | TRADEDATE | xla去前缀变体 |
| `val_dividendyield3` | 股息率TTM | TRADEDATE | xla去前缀变体 |
| `val_dividendyield4` | 股息率TTM(剔除特别派息) | TRADEDATE | xla去前缀变体 |
| `val_evebitda` | 企业倍数(TTM) | TRADEDATE | xla去前缀变体 |
| `val_evebitda2` | 企业倍数2(TTM) | TRADEDATE | xla去前缀变体 |
| `val_evtoebitda2` | 企业倍数2(EV2/EBITDA) | TRADEDATE | xla去前缀变体 |
| `val_mv` | 指数总市值 | TRADEDATE | xla去前缀变体 |
| `val_mv_ard` | 总市值 | TRADEDATE | xla去前缀变体 |
| `val_mvc` | 流通市值 | TRADEDATE | xla去前缀变体 |
| `val_pb_avg` | 区间平均PB(LF) | StartDate、EndDate | xla去前缀变体 |
| `val_pb_high` | 区间最高PB(LF) | StartDate、EndDate | xla去前缀变体 |
| `val_pb_lf_issuer` | 发布方市净率PB(LF) | TRADEDATE | xla去前缀变体 |
| `val_pb_low` | 区间最低PB(LF) | StartDate、EndDate | xla去前缀变体 |
| `val_pb_median` | 市净率PB(LF,中位数) | TRADEDATE | xla去前缀变体 |
| `val_pb_mrqwgt` | 市净率PB(MRQ,加权) | TRADEDATE | xla去前缀变体 |
| `val_pb_percentile` | 市净率分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_pcf_ocfttmwgt` | 市现率PCF(经营现金流TTM,加权) | TRADEDATE | xla去前缀变体 |
| `val_pcf_percentile` | 市现率分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_pe_deducted_lyr` | 市盈率PE(lyr,扣除非经常性损益) | DEALDATE | xla去前缀变体 |
| `val_pe_deducted_ttm` | 市盈率(扣非,TTM) |  | 探测法实测 |
| `val_pe_lyr_nongaap` | Non-gaap归母市盈率(LYR) | TRADEDATE | xla去前缀变体 |
| `val_pe_median` | 市盈率PE(TTM,中位数) | TRADEDATE | xla去前缀变体 |
| `val_pe_nonnegative` | 市盈率PE(TTM,剔除负值) | TRADEDATE | xla去前缀变体 |
| `val_pe_nonnegative_wgt` | 市盈率PE(TTM,剔除负值,加权) | TRADEDATE | xla去前缀变体 |
| `val_pe_percentile` | 市盈率分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_pe_ttm_issuer` | 发布方市盈率PE(TTM) | TRADEDATE | xla去前缀变体 |
| `val_pe_ttm_issuer2` | 发布方市盈率PE(TTM,调整) | TRADEDATE | xla去前缀变体 |
| `val_pe_ttmwgt` | 市盈率PE(TTM,加权) | TRADEDATE | xla去前缀变体 |
| `val_pe_wgt` | 市盈率PE(LYR,加权) | TRADEDATE | xla去前缀变体 |
| `val_penonngtv_percentile` | 市盈率PE(TTM,剔除负值)分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_pep` | 市盈率百分位 | StartDate、EndDate | xla去前缀变体 |
| `val_pep2` | 市盈率百分位 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_pettm_avg` | 区间平均PE(TTM) | StartDate、EndDate | xla去前缀变体 |
| `val_pettm_high` | 区间最高PE(TTM) | StartDate、EndDate | xla去前缀变体 |
| `val_pettm_low` | 区间最低PE(TTM) | StartDate、EndDate | xla去前缀变体 |
| `val_pettm_median1` | 区间中位数PE(TTM) | StartDate、EndDate | xla去前缀变体 |
| `val_ps_percentile` | 市销率分位数 | TRADEDATE、StartDate、EndDate | xla去前缀变体 |
| `val_ps_ttmwgt` | 市销率PS(TTM,加权) | TRADEDATE | xla去前缀变体 |
| `val_pslyr_avg` | 区间平均PS(LYR) | StartDate、EndDate | xla去前缀变体 |
| `val_pslyr_high` | 区间最高PS(LYR) | StartDate、EndDate | xla去前缀变体 |
| `val_pslyr_low` | 区间最低PS(LYR) | StartDate、EndDate | xla去前缀变体 |
| `val_psttm_avg` | 区间平均PS(TTM) | StartDate、EndDate | xla去前缀变体 |

<a id="分类-交易"></a>

## 交易（2 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `trade_code` | 交易代码 |  | 探测法实测 |
| `trade_status` | 交易状态 |  | 探测法实测 |

<a id="分类-证券基础"></a>

## 证券基础（4 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `sec_englishname` | 英文简称 |  | 探测法实测 |
| `sec_name` | 证券简称 |  | 探测法实测 |
| `sec_status` | 上市状态 |  | 探测法实测 |
| `sec_type` | 证券类型 |  | 探测法实测 |

<a id="分类-回购"></a>

## 回购（1 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `repo_briefing` | 品种简介 |  | xla去前缀变体 |

<a id="分类-通用-行情-其他"></a>

## 通用/行情/其他（3848 个字段）

| 字段代码 | 中文名 | 参数 | 来源 |
|---|---|---|---|
| `1stquartile` | N日收盘价1/4分位数 |  | xla去前缀变体 |
| `3rdquartile` | N日收盘价3/4分位数 |  | xla去前缀变体 |
| `abnormaltrade_netbuy` | 龙虎榜净买入额 | TRADEDATE | xla去前缀变体 |
| `absinv_interest` | 资产支持证券投资收益-利息收入 | REPORTDATE | xla去前缀变体 |
| `absinv_redemptionspread` | 资产支持证券投资收益-赎回差价收入 | REPORTDATE | xla去前缀变体 |
| `absinv_subscriptionspread` | 资产支持证券投资收益-申购差价收入 | REPORTDATE | xla去前缀变体 |
| `absinv_tradespread` | 资产支持证券投资收益-买卖资产支持证券差价收入 | REPORTDATE | xla去前缀变体 |
| `absolute_avgincome` | 平均收益 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_avgloss` | 平均损失 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_avgmonthlyreturn` | 平均月度回报 | StartDate、EndDate | xla去前缀变体 |
| `absolute_condownsmonth` | 连跌月数 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_conupsmonth` | 连涨月数 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_highestmonthlyreturn` | 最高单月回报 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_highestquatreturn` | 最高季度回报 | StartDate、EndDate | xla去前缀变体 |
| `absolute_highestreturnofconmonth` | 最高连续N月回报 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_longestcondownmonth` | 最长连续下跌月数 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_longestconupmonth` | 最长连续上涨月数 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_lowestmonthlyreturn` | 最低单月回报 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_lowestquatreturn` | 最低季度回报 | StartDate、EndDate | xla去前缀变体 |
| `absolute_lowestreturnofconmonth` | 最差连续N月回报 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_maxfallofdownmonth` | 最长连续下跌整月跌幅 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_maxincreaseofupmonth` | 最长连续上涨整月涨幅 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_monthlycompositereturn` | 月度复合回报 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_profitmonthper` | 上涨月份占比 | BEGINDATE、EndDate | xla去前缀变体 |
| `absolute_profitper` | 区间盈利百分比 | StartDate、EndDate、CalcTerm | xla去前缀变体 |
| `absolute_siml_avglowestmonthlyreturn` | 最低单月回报同类平均 | StartDate、EndDate | xla去前缀变体 |
| `absolute_updownmonthratio` | 上涨/下跌月数比 | BEGINDATE、EndDate | xla去前缀变体 |
| `abstract` | 公司一句话介绍 |  | xla去前缀变体 |
| `acceleratedornot` | 是否可加速到期 |  | xla去前缀变体 |
| `accounttreatment` | 会计处理 |  | xla去前缀变体 |
| `accrint_dayend_cnbd` | 日终应计利息 | TRADEDATE | xla原码 |
| `accrueddays` | 已计息天数 |  | xla去前缀变体 |
| `accruedinterest` | 应计利息 |  | 探测法实测 |
| `acct_rcv` | 应收账款 |  | 探测法实测 |
| `actissuer_area` | 国家或地区(穿透信用主体) |  | xla去前缀变体 |
| `active_atm_code` | 主力平值期权代码 | TRADEDATE、OptionType、UnderType | xla去前缀变体 |
| `active_op_undly` | 活跃期权标的代码 | TRADEDATE、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `actualbenchmark` | 计息基准 |  | xla去前缀变体 |
| `actualleverageratio` | 实际杠杆倍数 |  | xla去前缀变体 |
| `actualmaturitydate` | 实际到期日 |  | xla去前缀变体 |
| `additionalto` | 增发债对应原债券 |  | xla去前缀变体 |
| `address` | 注册地址 |  | xla去前缀变体 |
| `adjfactor` | 复权因子 |  | 探测法实测 |
| `admexptogr2` | 管理费用/营业总收入(不含研发费用) | REPORTDATE | xla去前缀变体 |
| `admincode` | 所属行政区划代码 | AdminLevelType、TRADEDATE | xla去前缀变体 |
| `adminexpense_ttm` | 管理费用(TTM) |  | xla去前缀变体 |
| `adminexpense_ttm2` | 管理费用(TTM) | REPORTDATE | xla去前缀变体 |
| `adminexpensetogr` | 管理费用／营业总收入 | REPORTDATE | xla去前缀变体 |
| `adminexpensetogr_ttm` | 管理费用／营业总收入(TTM) |  | xla去前缀变体 |
| `adminexpensetogr_ttm2` | 管理费用/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `administrativedivision` | 所属行政区划 | Level、TRADEDATE | xla去前缀变体 |
| `ado_actualissueamt` | 增发债实际发行额 | Batch | xla去前缀变体 |
| `ado_amountplan` | 增发债计划发行额 | Batch | xla去前缀变体 |
| `ado_anndate` | 增发债公告日 | Batch | xla去前缀变体 |
| `ado_bidcoverratio` | 增发债全场倍数 | Batch | xla去前缀变体 |
| `ado_biddernum` | 增发债投标家数 | Batch | xla去前缀变体 |
| `ado_bidmax` | 增发债投标上限 | Batch | xla去前缀变体 |
| `ado_bidmin` | 增发债投标下限 | Batch | xla去前缀变体 |
| `ado_bidspread` | 增发债中标利差 | Batch | xla去前缀变体 |
| `ado_bidstep` | 增发债投标步长 | Batch | xla去前缀变体 |
| `ado_continuousbidpos` | 增发债是否要求标位连续 | Batch | xla去前缀变体 |
| `ado_distend` | 增发债分销截止日 | Batch | xla去前缀变体 |
| `ado_diststart` | 增发债分销起始日 | Batch | xla去前缀变体 |
| `ado_fee` | 增发债手续费 | Batch | xla去前缀变体 |
| `ado_issuanceamtmax` | 增发债发行金额上限 | Batch | xla去前缀变体 |
| `ado_issueend` | 增发债发行截止日 | Batch | xla去前缀变体 |
| `ado_issuestart` | 增发债发行起始日 | Batch | xla去前缀变体 |
| `ado_listdate` | 增发债上市日 | Batch | xla去前缀变体 |
| `ado_marginalrate` | 增发债边际利率 | Batch | xla去前缀变体 |
| `ado_marginalratio` | 增发债边际倍数 | Batch | xla去前缀变体 |
| `ado_maxbidprice` | 增发债最高投标价位 | Batch | xla去前缀变体 |
| `ado_maxbidqty` | 增发债标位最高投标量 | Batch | xla去前缀变体 |
| `ado_minbidprice` | 增发债最低投标价位 | Batch | xla去前缀变体 |
| `ado_minbidqty` | 增发债标位最低投标量 | Batch | xla去前缀变体 |
| `ado_minbidunit` | 增发债最小投标单位 | Batch | xla去前缀变体 |
| `ado_payend` | 增发债缴款截止日 | Batch | xla去前缀变体 |
| `ado_paystart` | 增发债缴款起始日 | Batch | xla去前缀变体 |
| `ado_refyield` | 增发债参考收益率 | Batch | xla去前缀变体 |
| `ado_tendermethod` | 增发债招标方式 | Batch | xla去前缀变体 |
| `ado_tendertarget` | 增发债招标标的 | Batch | xla去前缀变体 |
| `ado_tendertime` | 增发债招标时间 | Batch | xla去前缀变体 |
| `ado_tendervenue` | 增发债招标场所 | Batch | xla去前缀变体 |
| `ado_totalbidamt` | 增发债投标总量 | Batch | xla去前缀变体 |
| `ado_totalvalidbidamt` | 增发债有效投标总量 | Batch | xla去前缀变体 |
| `ado_transferdate` | 增发债债券过户日 | Batch | xla去前缀变体 |
| `ado_underwritingmethod` | 增发债承销方式 | Batch | xla去前缀变体 |
| `ado_validbiddernum` | 增发债有效投标家数 | Batch | xla去前缀变体 |
| `ado_winprice` | 增发债中标价格 | Batch | xla去前缀变体 |
| `adtm` | ADTM动态买卖气指标 |  | xla原码 |
| `advancecredit_desc` | 信托项目关联企业名称 |  | xla原码 |
| `agency_bondtrustee` | 受托管理人 |  | xla去前缀变体 |
| `agency_bookkeeper` | 账簿管理人 |  | xla去前缀变体 |
| `agency_booksupporter` | 集中簿记建档系统技术支持机构 |  | xla去前缀变体 |
| `agency_certification` | 绿色债券认证机构 |  | xla去前缀变体 |
| `agency_coordinator` | 联席全球协调人(海外) |  | xla去前缀变体 |
| `agency_fundbank` | 募集资金专项账户开户行 |  | xla去前缀变体 |
| `agency_guarantor_abbr` | 担保人中文简称 |  | xla去前缀变体 |
| `agency_guarantorbriefing` | 担保人公司简介,b_agency_guarantorbriefing(新增) |  | xla去前缀变体 |
| `agency_guarantornature` | 担保人公司属性,b_agency_guarantornature(新增) |  | xla去前缀变体 |
| `agency_jointleadunder` | 联席主承销商 |  | xla去前缀变体 |
| `agency_leadunderwritersn` | 主承销商(简称) |  | xla去前缀变体 |
| `agency_management` | 存续期管理机构 |  | xla去前缀变体 |
| `agency_manaleadunder` | 牵头主承销商 |  | xla去前缀变体 |
| `agency_reguarantor` | 再担保人 |  | xla去前缀变体 |
| `agency_sblc` | 备用信用证提供方 |  | xla去前缀变体 |
| `agency_underwriter` | 牵头经办人 |  | xla去前缀变体 |
| `allreturndate` | 理论回售日 |  | xla去前缀变体 |
| `allstock_pb` | 全部持股平均市净率 | REPORTDATE | xla去前缀变体 |
| `allstock_pe` | 全部持股平均市盈率 | REPORTDATE | xla去前缀变体 |
| `amount` | 成交额 |  | xla去前缀变体 |
| `amount_aht` | 盘后成交额 | TRADEDATE | xla去前缀变体 |
| `amount_btin` | 成交额(含大宗交易) | TRADEDATE | xla去前缀变体 |
| `amount_fixedincome` | 上证固收平台成交金额 | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `amt` | 成交额 |  | 探测法实测 |
| `amtpropfdleundwt` | 主承销商自营资金获配金额 |  | xla去前缀变体 |
| `amtratio` | 成交额认沽认购比率 | SettlementMonth、TRADEDATE | xla去前缀变体 |
| `anal_avgnavreturn` | 基金加权平均净值利润率(新增) | REPORTDATE | xla去前缀变体 |
| `anal_avgnetincomeperunit` | 报告期加权平均份额利润(新增) | REPORTDATE | xla去前缀变体 |
| `anal_basepointvalue` | 平均基点价值 | TRADEDATE | xla去前缀变体 |
| `anal_basis` | 基差(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_basis_stkidx` | 基差(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_basisannualyield` | 基差年化收益率(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_basisannualyield_stkidx` | 基差年化收益率(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_basispercent` | 基差率(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_basispercent_stkidx` | 基差率(股指期货) | TRADEDATE | xla去前缀变体 |
| `anal_capconvexity` | 平均市值法凸性 | TRADEDATE | xla去前缀变体 |
| `anal_capduration` | 平均市值法久期 | TRADEDATE | xla去前缀变体 |
| `anal_capytm` | 平均市值法到期收益率 | TRADEDATE | xla去前缀变体 |
| `anal_cashflowconvexity` | 平均现金流法凸性 | TRADEDATE | xla去前缀变体 |
| `anal_cashflowduration` | 平均现金流法久期 | TRADEDATE | xla去前缀变体 |
| `anal_cashflowytm` | 平均现金流法到期收益率 | TRADEDATE | xla去前缀变体 |
| `anal_disratiodevi` | 折溢价比率偏离系数 |  | xla去前缀变体 |
| `anal_distributable` | 期末可供分配基金收益 | REPORTDATE | xla去前缀变体 |
| `anal_distributableperunit` | 期末可供分配基金份额收益 | REPORTDATE | xla去前缀变体 |
| `anal_downdiscount_pctchange` | 下折母基金需跌 | TRADEDATE | xla去前缀变体 |
| `anal_downdiscount_threshold` | 下折阈值 |  | xla去前缀变体 |
| `anal_impliedyield` | 隐含收益率 | TRADEDATE | xla去前缀变体 |
| `anal_income` | 报告期利润(新增) | REPORTDATE | xla去前缀变体 |
| `anal_ipratio` | 平均派息率 | TRADEDATE | xla去前缀变体 |
| `anal_navlever` | 净值杠杆 |  | xla去前缀变体 |
| `anal_netincome` | 报告期基金净收益 | REPORTDATE | xla去前缀变体 |
| `anal_nextaayield` | 下期约定年收益率 |  | xla去前缀变体 |
| `anal_nextdiscountdate` | 下一定期折算日 |  | xla去前缀变体 |
| `anal_period` | 平均待偿期 | TRADEDATE | xla去前缀变体 |
| `anal_precupn` | 上一付息日 | DEALDATE | xla去前缀变体 |
| `anal_pricelever` | 价格杠杆 |  | xla去前缀变体 |
| `anal_reits_actdist` | 实际分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `anal_reits_cashdist` | 现金分派率 | Year | xla去前缀变体 |
| `anal_reits_cashflowbalance` | 经营活动现金流量余额 | REPORTDATE | xla去前缀变体 |
| `anal_reits_depreciationandamortization` | 折旧和摊销 | REPORTDATE | xla去前缀变体 |
| `anal_reits_distributedamounts` | 可供分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `anal_reits_ebit` | 税息折旧及摊销前利润 | REPORTDATE | xla去前缀变体 |
| `anal_reits_fairvalue` | 期末基金份额公允价值参考净值 | Year | xla去前缀变体 |
| `anal_reits_income` | 本期收入 | REPORTDATE | xla去前缀变体 |
| `anal_reits_interestcost` | 利息支出 | REPORTDATE | xla去前缀变体 |
| `anal_reits_irr` | 内部收益率 | Year | xla去前缀变体 |
| `anal_reits_netprofit` | 本期净利润 | REPORTDATE | xla去前缀变体 |
| `anal_reits_taxcost` | 所得税费用 | REPORTDATE | xla去前缀变体 |
| `anal_reits_unitactdist` | 单位实际分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `anal_reits_unitdistributedamounts` | 单位可供分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `anal_smfbfactualcost` | 实际资金成本 |  | xla去前缀变体 |
| `anal_smfbnamedcost` | 名义资金成本 |  | xla去前缀变体 |
| `anal_smfearning` | 分级基金收益分配方式 |  | xla去前缀变体 |
| `anal_tdiscountratio` | 整体折溢价率 |  | xla去前缀变体 |
| `anal_updiscount_pctchange` | 上折母基金需涨 | TRADEDATE | xla去前缀变体 |
| `anal_updiscount_threshold` | 上折阈值 |  | xla去前缀变体 |
| `anchorbond` | 主债券代码 |  | xla去前缀变体 |
| `announcedateofcsrc` | 证监会核准公告日 |  | xla去前缀变体 |
| `anticipateyield_desc` | 信用增级情况 |  | xla原码 |
| `anyield_roll` | 期货合约展期年化收益率 | TRADEDATE | xla去前缀变体 |
| `apturn` | 应付账款周转率 | REPORTDATE | xla去前缀变体 |
| `apturndays` | 应付账款周转天数 | REPORTDATE | xla去前缀变体 |
| `ard_bs_perp_min` | 永续债_归属于少数股东 | REPORTDATE | xla去前缀变体 |
| `ard_bs_perp_par` | 永续债_归属于母公司股东 | REPORTDATE | xla去前缀变体 |
| `ard_bs_perpetual` | 永续债_合计 | REPORTDATE | xla去前缀变体 |
| `ard_is_investmentproperty` | 投资物业公允价值变动(公布值) | REPORTDATE、TYPE | xla去前缀变体 |
| `ard_is_sales` | 总营业收入(公布值) | REPORTDATE、TYPE | xla去前缀变体 |
| `area` | 注册地所在国家或地区 |  | xla去前缀变体 |
| `arturn` | 应收账款周转率 |  | 探测法实测 |
| `arturndays` | 应收账款周转天数 | REPORTDATE | xla去前缀变体 |
| `asharewindcode` | 同公司A股Wind代码 |  | xla去前缀变体 |
| `askrt_avg` | 报价卖出收益率(算数平均) |  | xla去前缀变体 |
| `askrt_bst` | 报价卖出收益率(最优) |  | xla去前缀变体 |
| `asset_mrq` | 资产总计(MRQ) |  | xla去前缀变体 |
| `assetmanagementshold_products` | 持有券商资管家数 | REPORTDATE | xla去前缀变体 |
| `assetstoequity` | 权益乘数 | REPORTDATE | xla去前缀变体 |
| `assetsturn` | 总资产周转率 |  | 探测法实测 |
| `atmcode` | 平值期权代码 | TRADEDATE、SettlementMonth | xla去前缀变体 |
| `atmiv_expiration` | 期权衍生剩余到期 | TRADEDATE | xla去前缀变体 |
| `atmiv_mapping` | 期权衍生对应关系 | TRADEDATE | xla去前缀变体 |
| `atr` | ATR真实波幅 |  | xla原码 |
| `audaccdate` | 债券审核受理日期 |  | xla去前缀变体 |
| `auditor` | 首发审计机构 |  | xla去前缀变体 |
| `auditor2` | 审计机构(支持历史) | TRADEDATE | xla去前缀变体 |
| `avgprice_fixedincome` | 上证固收平台平均价 | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `avgreturn` | 平均收益率 |  | xla去前缀变体 |
| `avgreturny` | 平均收益率(年化)(新增) | TD1、TD2 | xla去前缀变体 |
| `avgyiled_broker` | 均价收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `backdoor` | 是否借壳上市 |  | xla去前缀变体 |
| `backdoordate` | 借壳上市日期 |  | xla去前缀变体 |
| `balanceafterrepayment` | 违约偿还后债券余额 | TRADEDATE | xla去前缀变体 |
| `banks` | 主要往来银行 |  | xla去前缀变体 |
| `banktype` | 上市公司(银行)类型 |  | xla去前缀变体 |
| `basedate` | 基期 |  | xla去前缀变体 |
| `baserate` | 基准利率 |  | xla去前缀变体 |
| `baserate2` | 基准利率(发行时) |  | xla去前缀变体 |
| `baserate3` | 基准利率(指定日期) | TRADEDATE | xla去前缀变体 |
| `basevalue` | 基点 |  | xla去前缀变体 |
| `basevalue_ifexe` | 行权基点价值 | TRADEDATE | xla去前缀变体 |
| `basisannualyield` | 基差年化收益率(股指期货) | TRADEDATE | xla去前缀变体 |
| `bbi` | BBI多空指数 |  | xla原码 |
| `bbiboll` | BBIBOLL多空布林线 |  | xla原码 |
| `bclc` | 公司债对应上市公司代码(新增) |  | xla去前缀变体 |
| `bconvexity_ifexe` | 行权基准凸性 | TRADEDATE | xla去前缀变体 |
| `bduration` | 基准久期(新增) | TD | xla去前缀变体 |
| `bduration_ifexe` | 行权基准久期 | TRADEDATE | xla去前缀变体 |
| `beta` | 波Beta | StartDate、EndDate、Period、TYPE、INDEX | xla去前缀变体 |
| `betadf` | Beta(剔除财务杠杆)(新增) | TD1、TD2 | xla去前缀变体 |
| `bias` | BIAS乖离率 |  | xla原码 |
| `biaskrt_bst` | 双边卖出收益率(最优) |  | xla去前缀变体 |
| `biaskrt_wt` | 双边卖出收益率(加权平均) |  | xla去前缀变体 |
| `bibidrt_bst` | 双边买入收益率(最优) |  | xla去前缀变体 |
| `bibidrt_wt` | 双边买入收益率(加权平均) |  | xla去前缀变体 |
| `bidclosingyield_broker` | 买入收盘收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `bidrt_avg` | 报价买入收益率(算数平均) |  | xla去前缀变体 |
| `bidrt_bst` | 报价买入收益率(最优) |  | xla去前缀变体 |
| `bidyield_broker` | 买入平均价收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `binetask_bst` | 双边卖出净价(最优) |  | xla去前缀变体 |
| `binetask_wt` | 双边卖出净价(加权平均) |  | xla去前缀变体 |
| `binetbid_bst` | 双边买入净价(最优) |  | xla去前缀变体 |
| `binetbid_wt` | 双边买入净价(加权平均) |  | xla去前缀变体 |
| `biqtvolm` | 双边报价笔数 |  | xla去前缀变体 |
| `bissuingdate` | 发行人首次发债日 |  | xla去前缀变体 |
| `bndinv_accrintamount` | 买卖债券差价收入-应计利息总额 | REPORTDATE | xla去前缀变体 |
| `bndinv_bndamount` | 买卖债券差价收入-卖出债券(债转股及债券到期兑付)成交总额 | REPORTDATE | xla去前缀变体 |
| `bndinv_bndcost` | 买卖债券差价收入-卖出债券(债转股及债券到期兑付)成本总额 | REPORTDATE | xla去前缀变体 |
| `bndinv_interest` | 债券投资收益-利息收入 | REPORTDATE | xla去前缀变体 |
| `bndinv_redeemspread` | 债券投资收益-赎回差价收入 | REPORTDATE | xla去前缀变体 |
| `bndinv_spread` | 买卖债券差价收入-买卖债券差价收入 | REPORTDATE | xla去前缀变体 |
| `bndinv_subscribespread` | 债券投资收益-申购差价收入 | REPORTDATE | xla去前缀变体 |
| `bndinv_tradespread` | 债券投资收益-买卖债券差价收入 | REPORTDATE | xla去前缀变体 |
| `bndinv_transcost` | 买卖债券差价收入-交易费用 | REPORTDATE | xla去前缀变体 |
| `boardchairmen` | 董事长 | TRADEDATE | xla去前缀变体 |
| `boll` | BOLL布林带 |  | xla原码 |
| `bondcleanprice_cnbd` | 债底净价(中债) | TRADEDATE | xla去前缀变体 |
| `bondcnvxty_cnbd` | 债底凸性(中债) | TRADEDATE | xla去前缀变体 |
| `bondconsector` | 是否所属债券概念板块 | SectorID | xla去前缀变体 |
| `bonddirtyprice_cnbd` | 债底全价(中债) | TRADEDATE | xla去前缀变体 |
| `bondindexbuzhoumountain` | 债券非市场化发行指数 | TRADEDATE | xla去前缀变体 |
| `bondmodidura_cnbd` | 债底修正久期(中债) | TRADEDATE | xla去前缀变体 |
| `bondpre_cnbd` | 纯债溢价率(中债) | TRADEDATE | xla去前缀变体 |
| `bondscore` | 债券评分 | TRADEDATE | xla去前缀变体 |
| `bondyield_cnbd` | 债底收益率(中债) | TRADEDATE | xla去前缀变体 |
| `bookvaluetodebt` | 股东权益合计（含少数）／负债总计 | REPORTDATE | xla去前缀变体 |
| `bottom` | 筑底指标 |  | xla原码 |
| `bps` | 每股净资产BPS | REPORTDATE | xla去前缀变体 |
| `bps_adjust` | 每股净资产BPS-最新股本摊薄 | REPORTDATE | xla去前缀变体 |
| `bps_lyr` | 每股净资产BPS(最新年报,LYR) | TRADEDATE | xla去前缀变体 |
| `bps_new` | 每股净资产BPS(最新公告) |  | xla去前缀变体 |
| `briefing` | 公司简介 |  | xla去前缀变体 |
| `bs_crcassets` | 分出再保险合同资产 | YEARBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `bs_crcliab` | 分出再保险合同负债 | YEARBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `bs_ra` | 受限资产 | YEARBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `bsharecode` | 同公司B股代码(新增) |  | xla去前缀变体 |
| `bsharename` | 同公司B股简称(新增) |  | xla去前缀变体 |
| `bsharewindcode` | 同公司B股Wind代码 |  | xla去前缀变体 |
| `business` | 经营范围 |  | xla去前缀变体 |
| `cac_illegalityamount` | 区间违规处罚金额 | StartDate、DATE | xla去前缀变体 |
| `cac_illegalitynum` | 区间违规处罚次数 | StartDate、DATE | xla去前缀变体 |
| `cac_lawsuitamount` | 区间诉讼涉案金额 | StartDate、DATE | xla去前缀变体 |
| `cac_lawsuitnum` | 区间诉讼次数 | StartDate、DATE | xla去前缀变体 |
| `cac_repoamt` | 区间回购金额 | StartDate、DATE | xla去前缀变体 |
| `cac_repocshares` | 区间回购股份注销数量 | StartDate、DATE | xla去前缀变体 |
| `cac_reposhares` | 区间回购数量 | StartDate、DATE | xla去前缀变体 |
| `cagr_totalprofit` | 利润总额复合年增长率 |  | xla去前缀变体 |
| `calc_accrint` | 指定日应计利息 |  | xla去前缀变体 |
| `calc_accrued` | 应计利息 |  | xla去前缀变体 |
| `calc_adjyield` | 价格算票面调整收益率 | TRADEDATE、ExtraCoupon、BondPrice | xla去前缀变体 |
| `calc_askprice` | 计算卖出价格 |  | xla去前缀变体 |
| `calc_chinabond` | 收益率曲线(中债)3.0 | TRADEDATE、Term | xla去前缀变体 |
| `calc_clean` | 全价算净价 |  | xla去前缀变体 |
| `calc_conv` | 凸性 |  | xla去前缀变体 |
| `calc_dirty` | 净价算全价 |  | xla去前缀变体 |
| `calc_duration` | 麦考利久期 |  | xla去前缀变体 |
| `calc_floataddbp` | 计算浮息债隐含加息基点 |  | xla去前缀变体 |
| `calc_floatbench` | 计算浮息债隐含基准利率 |  | xla去前缀变体 |
| `calc_floatpv` | 计算浮息债全价 | TRADEDATE、Rate、Implied | xla去前缀变体 |
| `calc_hpy` | 持有期收益率 |  | xla去前缀变体 |
| `calc_mduration` | 修正久期 |  | xla去前缀变体 |
| `calc_price` | 收益率(Wind)算价格 |  | xla去前缀变体 |
| `calc_pv` | 收益率算价格(BC1) | TRADEDATE、IncomeRate、IncomeRateType、PRICETYPE | xla去前缀变体 |
| `calc_pvbp` | 基点价值 |  | xla去前缀变体 |
| `calc_yield` | 价格算到期收益率(Wind) |  | xla去前缀变体 |
| `calc_ytm` | 价格算收益率(BC1) | TRADEDATE、BondPrice、PRICETYPE、IncomeRateType | xla去前缀变体 |
| `callamount` | 认购成交额 | TRADEDATE | xla去前缀变体 |
| `calloi` | 认购持仓量 | TRADEDATE | xla去前缀变体 |
| `callrecdate` | 赎回登记日 |  | xla去前缀变体 |
| `callvolume` | 认购成交量 | TRADEDATE | xla去前缀变体 |
| `capital_ccontinent_security` | 是否COCO债 |  | xla去前缀变体 |
| `capitalflow` | 资金流向 | TRADEDATE | xla去前缀变体 |
| `capitalizedtoda` | 资本支出／折旧和摊销 | REPORTDATE | xla去前缀变体 |
| `carrydate` | 转债起息日期 |  | xla去前缀变体 |
| `carryenddate` | 计息截止日 |  | xla去前缀变体 |
| `cashflow_ttm` | 现金净流量(TTM) |  | xla去前缀变体 |
| `cashflow_ttm2` | 现金净流量(TTM) | REPORTDATE | xla去前缀变体 |
| `cashratio` | 现金比率 |  | 探测法实测 |
| `cashtocurrentdebt` | 现金比率 | REPORTDATE | xla去前缀变体 |
| `cashtostdebt` | 货币资金/短期债务 | REPORTDATE、TYPE | xla去前缀变体 |
| `catoassets` | 流动资产占比 |  | 探测法实测 |
| `caturn` | 流动资产周转率 | REPORTDATE | xla去前缀变体 |
| `cbissueornot` | 是否发行过可转债 | TRADEDATE | xla去前缀变体 |
| `cbname` | 同公司可转债简称 | TRADEDATE | xla去前缀变体 |
| `cbwindcode` | 同公司可转债Wind代码 | TRADEDATE | xla去前缀变体 |
| `cci` | CCI顺势指标 |  | xla原码 |
| `cdmonths` | 合约月份说明,fs_info_cdmonths |  | xla去前缀变体 |
| `cdp` | CDP逆势操作 |  | xla原码 |
| `cdrornot` | 是否CDR(沪伦通) |  | xla去前缀变体 |
| `ceo` | 总经理 | TRADEDATE | xla去前缀变体 |
| `cfo` | 财务总监 | TRADEDATE | xla去前缀变体 |
| `cfps` | 每股现金流量净额 | REPORTDATE | xla去前缀变体 |
| `cfps_ttm` | 每股现金流量净额(TTM) |  | xla去前缀变体 |
| `chain` | 所属产业链板块 |  | xla去前缀变体 |
| `chairman` | 法人代表 |  | xla去前缀变体 |
| `changelt` | 涨跌幅限制 |  | xla去前缀变体 |
| `changelt_new` | 涨跌幅限制(支持历史) | TRADEDATE | xla去前缀变体 |
| `chg` | 涨跌 |  | 探测法实测 |
| `chinabondl1type` | 中债债券一级分类,B_info_ChinabondL1type(新增) |  | xla去前缀变体 |
| `chinabondl2type` | 中债债券二级分类,B_info_ChinabondL2type(新增) |  | xla去前缀变体 |
| `cik` | CIK代码 |  | xla去前缀变体 |
| `city` | 城市 |  | xla去前缀变体 |
| `cityinvestmentbondgeo` | 城投行政级别 |  | xla去前缀变体 |
| `cityinvestmentbondgeowind` | 城投行政级别(Wind) |  | xla去前缀变体 |
| `ckgzjtxornot` | 是否企业的参控股公司为专精特新企业 |  | xla去前缀变体 |
| `ckgzjtxornot1` | 是否企业的参控股公司为专精特新企业(支持历史) | TRADEDATE | xla去前缀变体 |
| `clause` | 分红条款 |  | xla去前缀变体 |
| `clause_calloption_conditionalredeemenddate` | 条件赎回截止日期(新增) |  | xla去前缀变体 |
| `clause_calloption_conditionalredeemstartdate` | 条件赎回起始日期(新增) |  | xla去前缀变体 |
| `clause_calloption_indicativedaten` | 不强赎提示公告日 |  | xla去前缀变体 |
| `clause_calloption_indicativedatey` | 强赎提示公告日 |  | xla去前缀变体 |
| `clause_calloption_interestdisposal` | 利息处理(新增) |  | xla去前缀变体 |
| `clause_calloption_iswithtimeredemptionclause` | 是否有时点赎回条款(新增) |  | xla去前缀变体 |
| `clause_calloption_noticedate` | 赎回公告日 |  | xla去前缀变体 |
| `clause_calloption_recorddate` | 赎回登记日 |  | xla去前缀变体 |
| `clause_calloption_redeemclause` | 时点赎回条款全文(新增) |  | xla去前缀变体 |
| `clause_calloption_redeemitem` | 赎回条款(新增) |  | xla去前缀变体 |
| `clause_calloption_redeemmaxspan` | 赎回触发计算最大时间区间(新增) |  | xla去前缀变体 |
| `clause_calloption_redeemspan` | 赎回触发计算时间区间(新增) |  | xla去前缀变体 |
| `clause_calloption_redemptionmemo` | 赎回价格说明(新增) |  | xla去前缀变体 |
| `clause_calloption_redemptionprice` | 赎回价格(新增) |  | xla去前缀变体 |
| `clause_calloption_redemptiontimesperyear` | 每年可赎回次数(新增) |  | xla去前缀变体 |
| `clause_calloption_relativecalloptionperiod` | 相对赎回期(新增) |  | xla去前缀变体 |
| `clause_calloption_timeredemptiontimes` | 时点赎回数(新增) |  | xla去前缀变体 |
| `clause_calloption_triggerprice` | 赎回触发价 | TRADEDATE | xla去前缀变体 |
| `clause_calloption_triggerproportion` | 赎回触发比例(新增) |  | xla去前缀变体 |
| `clause_compensationinterest` | 补偿利率(公布) |  | xla去前缀变体 |
| `clause_conversion2_bondlot` | 未转股余额(新增) |  | xla去前缀变体 |
| `clause_conversion2_bondproportion` | 未转股比例(新增) |  | xla去前缀变体 |
| `clause_conversion2_conversionproportion` | 转换比例(新增) |  | xla去前缀变体 |
| `clause_conversion2_swapshareprice` | 转股价格(新增) |  | xla去前缀变体 |
| `clause_conversion2_tosharepriceadjustitem` | 转股条款(新增) |  | xla去前缀变体 |
| `clause_conversion_2_conversionproportion` | 转股价随派息调整(新增) |  | xla去前缀变体 |
| `clause_conversion_2_forceconvertdate` | 强制转股日(新增) |  | xla去前缀变体 |
| `clause_conversion_2_forceconvertprice` | 强制转股价格(新增) |  | xla去前缀变体 |
| `clause_conversion_2_isforced` | 是否强制转股(新增) |  | xla去前缀变体 |
| `clause_conversion_2_relativeswapsharemonth` | 相对转股期(新增) |  | xla去前缀变体 |
| `clause_conversion_2_swapshareenddate` | 自愿转股终止日期(新增) |  | xla去前缀变体 |
| `clause_conversion_2_swapsharestartdate` | 自愿转股起始日期(新增) |  | xla去前缀变体 |
| `clause_conversion_code` | 转股代码 |  | xla去前缀变体 |
| `clause_exannoundate` | 最新行权公告日 | DEALDATE | xla去前缀变体 |
| `clause_interest_compensationinterest` | 补偿利率(新增) |  | xla去前缀变体 |
| `clause_processmodeinterest` | 利息处理方式 |  | xla去前缀变体 |
| `clause_putoption_additionalpricememo` | 附加回售价格说明(新增) |  | xla去前缀变体 |
| `clause_putoption_conditionalputbackenddate` | 条件回售截止日期(新增) |  | xla去前缀变体 |
| `clause_putoption_conditionalputbackstartenddate` | 条件回售起始日期(新增) |  | xla去前缀变体 |
| `clause_putoption_interestdisposing` | 利息处理(新增) |  | xla去前缀变体 |
| `clause_putoption_noticedate` | 回售公告日 |  | xla去前缀变体 |
| `clause_putoption_putbackadditionalcondition` | 附加回售条件(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackclause` | 无条件回售条款(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackenddate` | 无条件回售结束日期(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackperiod` | 无条件回售期(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackperiodobs` | 相对回售期(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackprice` | 无条件回售价(新增) |  | xla去前缀变体 |
| `clause_putoption_putbackstartdate` | 无条件回售起始日期(新增) |  | xla去前缀变体 |
| `clause_putoption_putbacktimesperyear` | 每年回售次数(新增) |  | xla去前缀变体 |
| `clause_putoption_putbacktriggermaxspan` | 回售触发计算最大时间区间(新增) |  | xla去前缀变体 |
| `clause_putoption_putbacktriggerspan` | 回售触发计算时间区间(新增) |  | xla去前缀变体 |
| `clause_putoption_redeem_triggerproportion` | 回售触发比例(新增) |  | xla去前缀变体 |
| `clause_putoption_resellingprice` | 回售价格(新增) |  | xla去前缀变体 |
| `clause_putoption_resellingpriceexplaination` | 回售价格说明(新增) |  | xla去前缀变体 |
| `clause_putoption_sellbackitem` | 条件回售条款全文(新增) |  | xla去前缀变体 |
| `clause_putoption_timeputbackclause` | 时点回售条款全文(新增) |  | xla去前缀变体 |
| `clause_putoption_timeputbacktimes` | 时点回售数(新增) |  | xla去前缀变体 |
| `clause_putoption_triggerprice` | 回售触发价 | TRADEDATE | xla去前缀变体 |
| `clause_reset_isexitreset` | 是否有特别向下修正条款(新增) |  | xla去前缀变体 |
| `clause_reset_item` | 特别向下修正条款全文 |  | xla去前缀变体 |
| `clause_reset_referencepriceisanverage` | 是否为算术平均价(新增) |  | xla去前缀变体 |
| `clause_reset_resetmaxtimespan` | 重设触发计算最大时间区间(新增) |  | xla去前缀变体 |
| `clause_reset_resetperiodenddate` | 特别修正结束时间(新增) |  | xla去前缀变体 |
| `clause_reset_resetrange` | 特别修正幅度(新增) |  | xla去前缀变体 |
| `clause_reset_resetstartdate` | 特别修正起始时间(新增) |  | xla去前缀变体 |
| `clause_reset_resettimeslimit` | 修正次数限制(新增) |  | xla去前缀变体 |
| `clause_reset_resettimespan` | 重设触发计算时间区间(新增) |  | xla去前缀变体 |
| `clause_reset_resettriggerratio` | 触发比例(新增) |  | xla去前缀变体 |
| `clause_reset_stockpricelowestlimit` | 修正价格底线说明(新增) |  | xla去前缀变体 |
| `clause_reset_timepointclause` | 时点修正条款全文(新增) |  | xla去前缀变体 |
| `clauseabbr` | 特殊条款(缩写) |  | xla去前缀变体 |
| `clauseitem` | 特殊条款全文 |  | xla去前缀变体 |
| `cleanprice` | 收盘价(净价) | TRADEDATE | xla去前缀变体 |
| `cleanprice_cbr` | 估值净价(中债资信) | TRADEDATE | xla去前缀变体 |
| `clearing` | 清算机构 |  | xla去前缀变体 |
| `clo` | 法律顾问(新增) |  | xla去前缀变体 |
| `close` | 收盘价 |  | 探测法实测 |
| `close2` | 收盘价(外汇) | TRADEDATE、CloseTime | xla去前缀变体 |
| `close_auction_amount` | 收盘集合竞价成交额 | TRADEDATE | xla去前缀变体 |
| `close_auction_price` | 收盘集合竞价成交价 | TRADEDATE | xla去前缀变体 |
| `close_auction_volume` | 收盘集合竞价成交量 | TRADEDATE | xla去前缀变体 |
| `close_fixedincome` | 上证固收平台收盘价 | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `close_night` | 收盘价(夜盘)_期货历史同月 | TRADEDATE | xla去前缀变体 |
| `close_usd` | 收盘价(美元) | TRADEDATE | xla去前缀变体 |
| `cnscdate` | 纳入陆股通日期 | TRADEDATE | xla去前缀变体 |
| `cnvxty_cnbd` | 加权平均结算价凸性 | TRADEDATE | xla原码 |
| `cnvxty_csi` | 估价凸性(中证指数) |  | xla去前缀变体 |
| `cnvxty_csi1` | 估价凸性(中证指数) | DEALDATE、Credibility | xla去前缀变体 |
| `cnvxty_shc` | 估价凸性(上海清算所) |  | xla去前缀变体 |
| `codechangedate` | 证券代码变更日期 | TRADEDATE | xla去前缀变体 |
| `cogstosales` | 销售成本率 | REPORTDATE | xla去前缀变体 |
| `collateral` | 是否融资融券担保物 | TRADEDATE | xla去前缀变体 |
| `collateralcode` | 质押券代码 |  | xla原码 |
| `collateralname` | 质押券简称 |  | xla原码 |
| `collection_total` | 募资总额 |  | xla去前缀变体 |
| `collection_unused` | 募资未投入资金总额 |  | xla去前缀变体 |
| `commission_detailed` | 交易佣金(明细值) | REPORTDATE | xla去前缀变体 |
| `commission_total` | 交易佣金(合计值) | REPORTDATE | xla去前缀变体 |
| `compindex2` | 是否属于重要指数成份 | IndexBelong、TRADEDATE | xla去前缀变体 |
| `compindex3` | 是否属于指数成份 | WINDCODE3、TRADEDATE | xla去前缀变体 |
| `compprename` | 公司曾用名 | TRADEDATE | xla去前缀变体 |
| `concept` | 所属概念板块 |  | xla去前缀变体 |
| `conditionalcallprice` | 有条件赎回价 |  | xla去前缀变体 |
| `conditionalputprice` | 有条件回售价 |  | xla去前缀变体 |
| `connp_ttm` | 持续经营净利润(TTM) | REPORTDATE、CURTYPE | xla去前缀变体 |
| `connptoprofit_ttm` | 持续经营净利润/税后利润(TTM) | REPORTDATE | xla去前缀变体 |
| `cont_atm_code` | 连续平值期权代码 | TRADEDATE、Month、OptionType、UnderType、Strike、AdjustmentState | xla去前缀变体 |
| `contract_issuedate` | 标准合约上市日 |  | xla去前缀变体 |
| `contractmultiplier` | 合约乘数 |  | xla去前缀变体 |
| `controller_pct` | 实际控制人持股比例 | DEALDATE | xla去前缀变体 |
| `conversionpre_cnbd` | 转股溢价率(中债) | TRADEDATE | xla去前缀变体 |
| `conversionval_cnbd` | 转股价值(中债) | TRADEDATE | xla去前缀变体 |
| `convexity` | 凸性 |  | 探测法实测 |
| `convexity_cbr` | 凸性(中债资信) | TRADEDATE | xla去前缀变体 |
| `convexity_ifexe` | 行权凸性 | TRADEDATE | xla去前缀变体 |
| `convpb` | 转股市净率 |  | xla去前缀变体 |
| `convpe` | 转股市盈率 |  | xla去前缀变体 |
| `convpremium` | 转股溢价 |  | xla去前缀变体 |
| `convpremiumratio` | 转股溢价率 |  | xla去前缀变体 |
| `convprice` | 转股价 |  | xla去前缀变体 |
| `convratio` | 转股比例 |  | xla去前缀变体 |
| `convvalue` | 转换价值 |  | xla去前缀变体 |
| `corp_newlyissuedno` | 基金管理人新发产品数量 | StartDate、EndDate | xla去前缀变体 |
| `corporateindexbuzhoumountain` | 主体非市场化发行指数 | TRADEDATE | xla去前缀变体 |
| `corpscale` | 企业规模 | TRADEDATE | xla去前缀变体 |
| `cost_ttm` | 营业成本-非金融类(TTM) |  | xla去前缀变体 |
| `cost_ttm2` | 营业成本-非金融类(TTM) | REPORTDATE | xla去前缀变体 |
| `country` | 所属国家 |  | xla去前缀变体 |
| `coupon` | 息票品种 |  | xla去前缀变体 |
| `couponadj_max` | 票面利率调整上限 |  | xla去前缀变体 |
| `couponadj_min` | 票面利率调整下限 |  | xla去前缀变体 |
| `coupondatetxt` | 付息日说明 |  | xla去前缀变体 |
| `couponrate` | 票面利率 |  | 探测法实测 |
| `couponrate2` | 票面利率(当期) |  | xla去前缀变体 |
| `couponrate3` | 票面利率(指定日期) | TRADEDATE | xla去前缀变体 |
| `coupontxt` | 利率说明 |  | xla去前缀变体 |
| `credit_bondcreditstatus` | 债券信用状态 | TRADEDATE | xla去前缀变体 |
| `credit_formerline` | 历史授信额度 | TRADEDATE | xla去前缀变体 |
| `credit_line` | 最新授信额度 |  | xla去前缀变体 |
| `credit_linedate` | 最新授信日期 |  | xla去前缀变体 |
| `credit_lineunused` | 最新未使用授信额度 |  | xla去前缀变体 |
| `credit_lineused` | 最新已使用授信额度 |  | xla去前缀变体 |
| `credit_lineused2` | 历史已使用授信额度 | TRADEDATE | xla去前缀变体 |
| `creditrating` | 转债发行信用等级 |  | xla去前缀变体 |
| `creditratingagency` | 评级机构 |  | xla去前缀变体 |
| `creditspread_wind` | 信用利差(减Wind基准) | TRADEDATE | xla去前缀变体 |
| `crm_bookkeepingdate` | 簿记建档日,b_crm_bookkeepingdate(新增) |  | xla去前缀变体 |
| `crm_carrydate` | 凭证起始日,b_crm_carrydate(新增) |  | xla去前缀变体 |
| `crm_creditevent` | 信用事件,b_crm_creditevent(新增) |  | xla去前缀变体 |
| `crm_dateofrecord` | 凭证登记日,b_crm_dateofrecord(新增) |  | xla去前缀变体 |
| `crm_issuer` | 创设机构,b_crm_issuer(新增) |  | xla去前缀变体 |
| `crm_paymentterms` | 付费方式,b_crm_paymentterms(新增) |  | xla去前缀变体 |
| `crm_performguarantee` | 履约保障机制,b_crm_performguarantee(新增) |  | xla去前缀变体 |
| `crm_permissionnumber` | 创设批准文件编号,b_crm_permissionnumber(新增) |  | xla去前缀变体 |
| `crm_registeragency` | 登记机构,b_crm_registeragency(新增) |  | xla去前缀变体 |
| `crm_startingprice` | 创设价格,b_crm_startingprice(新增) |  | xla去前缀变体 |
| `crm_subject` | 标的实体,b_crm_subject(新增) |  | xla去前缀变体 |
| `crm_subjectcode` | 标的实体交易代码 |  | xla去前缀变体 |
| `crm_ubondoustandingamount` | 发行时标的债券余额,b_crm_ubondoustandingamount(新增) |  | xla去前缀变体 |
| `crtindpdirector` | 公司独立董事(现任)(新增) |  | xla去前缀变体 |
| `cs_cashpaidclaim` | 支付签发保险合同赔款的现金 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `cs_cashrecprem` | 收到签发保险合同保费取得的现金 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `cs_ntcashpaidcrc` | 支付分出再保险合同的现金净额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `cs_ntcashrecced` | 收到分入再保险合同的现金净额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `cs_ntincloanpled` | 保单质押贷款净增加额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `csrcjurisdiction` | 所属证监会辖区 | TRADEDATE | xla去前缀变体 |
| `cstype` | 所属中资股类型 |  | xla去前缀变体 |
| `current` | 流动比率 |  | 探测法实测 |
| `currentdebttodebt` | 流动负债／负债合计 | REPORTDATE | xla去前缀变体 |
| `currentdebttoequity` | 流动负债权益比率 | REPORTDATE | xla去前缀变体 |
| `cusipnumber` | Cusip代码 |  | xla去前缀变体 |
| `customizedfundornot` | 是否定制基金 |  | xla去前缀变体 |
| `d_vol_surface` | 品种隐含波动率曲面(按Delta) | TRADEDATE、Delta、Term、Construction、Exercisetype、Multipliertype | xla去前缀变体 |
| `dailycf` | 指定日现金流 |  | xla去前缀变体 |
| `dailycf_int` | 指定日利息现金流 | DEALDATE | xla去前缀变体 |
| `dailycf_prin` | 指定日本金现金流 | DEALDATE | xla去前缀变体 |
| `dailyclosefee` | 期权平今手续费 | DEALDATE | xla去前缀变体 |
| `day` | 距到期日时间(天)(新增) | TD | xla去前缀变体 |
| `dcm_accumamount` | 历史累计注册额度,B_DCM_Accumamount(新增) | BType | xla去前缀变体 |
| `dcm_expirationdata` | 未使用额度有效期,B_DCM_Expirationdata(新增) | BType | xla去前缀变体 |
| `dcm_firstissueenddate` | 首期发行截止日 |  | xla去前缀变体 |
| `dcm_meetingdata` | 未使用注册会议日期,B_DCM_Meetingdata(新增) | BType | xla去前缀变体 |
| `dcm_number` | 最新注册文件编号,B_DCM_Number(新增) | BType | xla去前缀变体 |
| `dcm_uesdamount` | 已使用注册额度,B_DCM_Uesdamount(新增) | BType | xla去前缀变体 |
| `dcm_underwriter` | 未使用额度主承销商,B_DCM_Underwriter(新增) | BType | xla去前缀变体 |
| `dcm_unuesdamount` | 未使用注册额度,B_DCM_Unuesdamount(新增) | BType | xla去前缀变体 |
| `ddate` | 交割日期 |  | xla去前缀变体 |
| `dealnum` | 成交笔数 |  | xla去前缀变体 |
| `dealnum_fixedincome` | 上证固收平台成交笔数 | TRADEDATE | xla去前缀变体 |
| `debt_mrq` | 负债合计(MRQ) |  | xla去前缀变体 |
| `debttoassets` | 资产负债率 |  | 探测法实测 |
| `debttoequity` | 产权比率(负债合计／归属母公司股东的权益) | REPORTDATE | xla去前缀变体 |
| `debttotangibleequity` | 有形净值债务率 | REPORTDATE | xla去前缀变体 |
| `deducteddebttoassets` | 剔除预收账款后的资产负债率 | REPORTDATE | xla去前缀变体 |
| `deductedprofit` | 扣除非经常性损益后的净利润 | REPORTDATE | xla去前缀变体 |
| `deductedprofit_ttm` | 扣除非经常性损益后的净利润(TTM) | TRADEDATE | xla去前缀变体 |
| `deductedprofit_ttm2` | 扣除非经常性损益后的净利润(TTM) | REPORTDATE | xla去前缀变体 |
| `deductedprofit_yoy` | 单季度.扣除非经常性损益后的净利润同比增长率 | REPORTDATE | xla去前缀变体 |
| `deductedprofittoprofit` | 扣除非经常损益后的净利润／净利润 | REPORTDATE | xla去前缀变体 |
| `defauloccurrencedate` | 违约发生日 | TRADEDATE | xla去前缀变体 |
| `defaultactualrepaymentdate` | 违约实际偿还日 | TRADEDATE | xla去前缀变体 |
| `defaultannouncedate` | 违约公告日 | TRADEDATE | xla去前缀变体 |
| `defaultbalance` | 违约日债券余额 | TRADEDATE | xla去前缀变体 |
| `defaulthistory` | 违约历程 |  | xla去前缀变体 |
| `defaultoverdueinterest` | 违约日逾期利息 | TRADEDATE | xla去前缀变体 |
| `defaultoverdueprincipal` | 违约日逾期本金 | TRADEDATE | xla去前缀变体 |
| `defaultoverduerepurchase` | 违约日逾期回售款 | TRADEDATE | xla去前缀变体 |
| `defaultreason` | 违约原因 | TRADEDATE | xla去前缀变体 |
| `defaultrepaymentannouncedate` | 违约偿还公告日 | TRADEDATE | xla去前缀变体 |
| `defaultrepaymentinterest` | 违约后偿还利息 | TRADEDATE | xla去前缀变体 |
| `defaultrepaymentmethod` | 违约后偿还方式 | TRADEDATE | xla去前缀变体 |
| `defaultrepaymentprincipal` | 违约后偿还本金 | TRADEDATE | xla去前缀变体 |
| `defaultrepaymentprocess` | 违约偿还历程 |  | xla去前缀变体 |
| `defaultrepaymentrepurchase` | 违约后偿还回售款 | TRADEDATE | xla去前缀变体 |
| `defaultsource` | 估值来源 |  | xla去前缀变体 |
| `defaultype` | 违约类型 | TRADEDATE | xla去前缀变体 |
| `deferraldays` | 假期顺延天数 | TRADEDATE | xla去前缀变体 |
| `defiguarantor` | 差额支付承诺人 |  | xla去前缀变体 |
| `delist_date` | 退市日期 |  | 探测法实测 |
| `delistreason` | 终止上市原因 |  | xla去前缀变体 |
| `deliveryfee` | 期货交割手续费 | TRADEDATE | xla去前缀变体 |
| `delta_atmcode` | Delta平值期权代码 | TRADEDATE、OptionalExpir、OptionType、Delta、AdjustmentState、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `delta_exch` | Delta(交易所) | TRADEDATE | xla去前缀变体 |
| `depositarybank` | 存托机构 | TRADEDATE | xla去前缀变体 |
| `diluterate` | 转股稀释率(新增) |  | xla去前缀变体 |
| `director` | 公司董事 |  | xla去前缀变体 |
| `dirty_cfets` | 估价全价(中国货币网) | TRADEDATE | xla去前缀变体 |
| `dirty_cnbd` | 估价全价 |  | xla去前缀变体 |
| `dirty_csi` | 估价全价(中证指数) |  | xla去前缀变体 |
| `dirty_csi1` | 估价全价(中证指数) | DEALDATE、Credibility | xla去前缀变体 |
| `dirty_shc` | 估价全价(上海清算所) |  | xla去前缀变体 |
| `dirtyprice` | 收盘价(全价) | TRADEDATE | xla去前缀变体 |
| `discloser` | 信息披露人 |  | xla去前缀变体 |
| `discloser1` | 董事会秘书 | TRADEDATE | xla去前缀变体 |
| `discount` | 贴水 |  | xla去前缀变体 |
| `dividendyield` | 股息率(股票获利率) |  | xla去前缀变体 |
| `dividendyield2` | 股息率(近12月) |  | 探测法实测 |
| `dlmonth` | 交割月份 |  | xla去前缀变体 |
| `dma` | DMA平均线差 |  | xla原码 |
| `dmi` | DMI趋向指标 |  | xla原码 |
| `dmi_2` | DMI趋向标准 | TRADEDATE | xla原码 |
| `doublelow` | 双低 | TRADEDATE | xla去前缀变体 |
| `down_mkt_capture` | 下行捕获率 | StartDate、EndDate、CalcTerm、Underlying_Index | xla去前缀变体 |
| `dp_yoy` | 扣除非经常性损益后的净利润(同比增长率) | REPORTDATE | xla去前缀变体 |
| `dpo` | DPO区间震荡线 |  | xla原码 |
| `dq_amount_cnbd` | 现券结算量(中债) | TRADEDATE | xla去前缀变体 |
| `dq_amtturnover` | 换手率(基准.流通市值) | TRADEDATE | xla去前缀变体 |
| `dq_change_close` | 涨跌(收盘价) | TRADEDATE | xla去前缀变体 |
| `dq_change_cnbd` | 涨跌(中债) | TRADEDATE | xla去前缀变体 |
| `dq_close_cnbd` | 指数值(中债) | TRADEDATE | xla去前缀变体 |
| `dq_close_night` | 收盘价(夜盘) | TRADEDATE | xla去前缀变体 |
| `dq_oiamount` | 持仓额 | TRADEDATE | xla去前缀变体 |
| `dq_pctchange_cnbd` | 涨跌幅(中债) | TRADEDATE | xla去前缀变体 |
| `dq_price_commodity` | 商品期货特殊时点价 | TRADEDATE、Point | xla去前缀变体 |
| `dq_price_premetals` | 贵金属现货特殊时点价 | TRADEDATE | xla去前缀变体 |
| `dq_quote_ask` | 最优报卖价 | TRADEDATE | xla去前缀变体 |
| `dq_quote_bid` | 最优报买价 | TRADEDATE | xla去前缀变体 |
| `dq_quote_mid` | 最优报中价 | TRADEDATE | xla去前缀变体 |
| `dq_settle` | 结算价 |  | xla去前缀变体 |
| `dq_stockmktcap1` | 正股总市值1 | TRADEDATE | xla去前缀变体 |
| `dq_stockmktcap2` | 正股总市值2 | TRADEDATE | xla去前缀变体 |
| `dsceval` | 上市公司信息披露考评 | Year | xla去前缀变体 |
| `dupont_assetstoequity` | 权益乘数(杜邦分析)(新增) | D | xla去前缀变体 |
| `dupont_intburden` | 利润总额／息税前利润(新增) | D | xla去前缀变体 |
| `dupont_np` | 归属母公司股东的净利润／净利润(新增) | D | xla去前缀变体 |
| `dupont_taxburden` | 净利润／利润总额(新增) | D | xla去前缀变体 |
| `duration` | 久期 |  | 探测法实测 |
| `eaname` | 证券扩位简称 |  | xla去前缀变体 |
| `earning` | 是否尚未盈利 |  | xla去前缀变体 |
| `ebbondpre_csi` | 可交换债纯债溢价率(中证指数) | TRADEDATE | xla去前缀变体 |
| `ebconversionpre_csi` | 可交换债转股溢价率(中证指数) | TRADEDATE | xla去前缀变体 |
| `ebit` | 息税前利润EBIT |  | 探测法实测 |
| `ebit2` | EBIT(正常化) |  | 探测法实测 |
| `ebit_ttm` | 息税前利润(TTM) |  | xla去前缀变体 |
| `ebit_ttm2` | 息税前利润(TTM反推法) | REPORTDATE | xla去前缀变体 |
| `ebitda` | 息税折旧摊销前利润EBITDA |  | 探测法实测 |
| `ebitda2` | 息税折旧摊销前利润(正向法)(新增) | DEALDATE、TP | xla去前缀变体 |
| `ebitda_ttm` | EBITDA(TTM反推法) | REPORTDATE | xla去前缀变体 |
| `ebitdaps` | 每股EBITDA | REPORTDATE | xla去前缀变体 |
| `ebitdatodebt` | 息税折旧摊销前利润／负债合计 | REPORTDATE | xla去前缀变体 |
| `ebitdatointerest` | EBITDA/利息费用 | REPORTDATE | xla去前缀变体 |
| `ebitdatointerestdebt` | EBITDA/带息债务 | REPORTDATE | xla去前缀变体 |
| `ebitdatosales` | EBITDA/营业总收入 | REPORTDATE | xla去前缀变体 |
| `ebitps` | 每股息税前利润 | REPORTDATE | xla去前缀变体 |
| `ebittoassets` | 息税前利润／总资产 | REPORTDATE | xla去前缀变体 |
| `ebittoassets2` | 息税前利润(TTM)/总资产 | REPORTDATE | xla去前缀变体 |
| `ebittoassets_ttm` | 息税前利润(TTM)/总资产 | REPORTDATE | xla去前缀变体 |
| `ebittogr` | 息税前利润／营业总收入 | REPORTDATE | xla去前缀变体 |
| `ebittointerest` | 已获利息倍数(EBIT／利息费用) | REPORTDATE | xla去前缀变体 |
| `eboptionval_csi` | 可交换债期权价值(中证指数) | TRADEDATE | xla去前缀变体 |
| `ebr` | 研发支出前利润 | REPORTDATE | xla去前缀变体 |
| `ebt_ttm` | 利润总额(TTM) |  | xla去前缀变体 |
| `ebt_ttm2` | 利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `ebttoor_ttm` | 利润总额/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `ebval_csi` | 可交换债估值(中证指数) | TRADEDATE | xla去前缀变体 |
| `ebvalyield_csi` | 可交换债估值收益率(中证指数) | TRADEDATE | xla去前缀变体 |
| `eft_invsttype` | ETF投资范围分类 | FundGroup | xla去前缀变体 |
| `elcd_number` | 交易所最新确认文件文号 |  | xla去前缀变体 |
| `email` | 公司电子邮件地址 |  | xla去前缀变体 |
| `embeddedopt_his` | 是否含权债(支持历史) | DEALDATE | xla去前缀变体 |
| `employee` | 员工总数 |  | xla去前缀变体 |
| `employee_admin` | 综合管理人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_admin_pct` | 综合管理人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_ba` | 本科人数 | TRADEDATE | xla去前缀变体 |
| `employee_ba_pct` | 本科人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_board` | 董事会人数 | TRADEDATE | xla去前缀变体 |
| `employee_coll` | 专科人数 | TRADEDATE | xla去前缀变体 |
| `employee_coll_pct` | 专科人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_excu` | 行政人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_excu_pct` | 行政人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_executivedirector` | 执行董事人数 | TRADEDATE | xla去前缀变体 |
| `employee_f` | 女性员工人数 | TRADEDATE | xla去前缀变体 |
| `employee_fin` | 财务人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_fin_pct` | 财务人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_highschool` | 高中及以下人数 | TRADEDATE | xla去前缀变体 |
| `employee_highschool_pct` | 高中及以下人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_hr` | 人事人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_hr_pct` | 人事人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_indpdirector` | 独立董事人数 | TRADEDATE | xla去前缀变体 |
| `employee_m` | 男性员工人数 | TRADEDATE | xla去前缀变体 |
| `employee_mgmt` | 高管人数 | TRADEDATE | xla去前缀变体 |
| `employee_ms` | 硕士人数 | TRADEDATE | xla去前缀变体 |
| `employee_ms_pct` | 硕士人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_othdegree` | 其他学历人数 | TRADEDATE | xla去前缀变体 |
| `employee_othdegree_pct` | 其他学历人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_othdept` | 其他人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_othdept_pct` | 其他专业人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_pc` | 母公司员工人数 | TRADEDATE | xla去前缀变体 |
| `employee_phd` | 博士人数 | TRADEDATE | xla去前缀变体 |
| `employee_phd_pct` | 博士人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_producer` | 生产人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_producer_pct` | 生产人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_pur` | 采购仓储人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_pur_pct` | 采购仓储人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_rc` | 风控稽核人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_rc_pct` | 风控稽核人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_sale` | 销售人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_sale_pct` | 销售人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_server` | 客服人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_server_pct` | 客服人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_tech` | 技术人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_tech_pct` | 技术人员人数占比 | TRADEDATE | xla去前缀变体 |
| `employee_techcore` | 核心技术人员人数 | TRADEDATE | xla去前缀变体 |
| `employee_totalmgmt` | 管理层人数 | TRADEDATE | xla去前缀变体 |
| `env` | ENV指标 |  | xla原码 |
| `eobspecialinstrutions` | 含权债期限特殊说明(新增) |  | xla去前缀变体 |
| `eps_adjust` | 每股收益EPS-最新股本摊薄 | REPORTDATE | xla去前缀变体 |
| `eps_basic` | 每股收益EPS(基本) |  | 探测法实测 |
| `eps_deducted_ttm` | 扣非后每股收益(TTM) | REPORTDATE | xla去前缀变体 |
| `eps_diluted` | 每股收益EPS(稀释) |  | 探测法实测 |
| `eps_diluted2` | 每股收益EPS-期末股本摊薄 | REPORTDATE | xla去前缀变体 |
| `eps_exbasic` | 每股收益EPS-扣除／基本 | REPORTDATE | xla去前缀变体 |
| `eps_exdiluted` | 每股收益EPS-扣除／稀释 | REPORTDATE | xla去前缀变体 |
| `eps_exdiluted2` | 每股收益EPS-扣除／期末股本摊薄 | REPORTDATE | xla去前缀变体 |
| `eps_ttm` | 每股收益EPS(TTM) |  | 探测法实测 |
| `equity_mrq` | 归属母公司股东的权益(MRQ) |  | xla去前缀变体 |
| `equity_mrq2` | 归属母公司股东权益(MRQ) | TRADEDATE | xla去前缀变体 |
| `equity_new` | 归属母公司股东的权益(最新公告) |  | xla去前缀变体 |
| `equity_to_asset` | 股东权益比 | REPORTDATE、TYPE | xla去前缀变体 |
| `equitytodebt` | 当日总市值／负债总计 | REPORTDATE | xla去前缀变体 |
| `equitytointerestdebt` | 归属母公司股东的权益／带息债务 | REPORTDATE | xla去前缀变体 |
| `equitytototalcapital` | 归属母公司股东的权益／全部投入资本 | REPORTDATE | xla去前缀变体 |
| `err_wi` | 盈利修正比例(可选类型) |  | xla去前缀变体 |
| `esgbondtype` | ESG(绿色)债券类型 |  | xla去前缀变体 |
| `esgl1type` | ESG(绿色)债券一级分类 |  | xla去前缀变体 |
| `esgl2type` | ESG(绿色)债券二级分类 |  | xla去前缀变体 |
| `estimated_netcollection` | 增发预计募集资金 |  | xla去前缀变体 |
| `estpb` | 预测PB | TRADEDATE、Year | xla去前缀变体 |
| `estpb_fy1` | 预测PB(FY1) | TRADEDATE | xla去前缀变体 |
| `estpb_fy2` | 预测PB(FY2) | TRADEDATE | xla去前缀变体 |
| `estpb_fy3` | 预测PB(FY3) | TRADEDATE | xla去前缀变体 |
| `estpe_fy1` | 预测PE(FY1) | TRADEDATE | xla去前缀变体 |
| `estpe_fy2` | 预测PE(FY2) | TRADEDATE | xla去前缀变体 |
| `estpe_fy3` | 预测PE(FY3) | TRADEDATE | xla去前缀变体 |
| `estpeg_ftm` | 预测PEG(未来12个月) | TRADEDATE | xla去前缀变体 |
| `estpeg_fy1` | 预测PEG(FY1) | TRADEDATE | xla去前缀变体 |
| `estpeg_fy2` | 预测PEG(FY2) | TRADEDATE | xla去前缀变体 |
| `estps` | 预测PS | TRADEDATE、Year | xla去前缀变体 |
| `etf_netasset` | ETF资产净值 | TRADEDATE | xla去前缀变体 |
| `ev` | 企业价值EV |  | 探测法实测 |
| `ev1` | 企业价值EV1 |  | 探测法实测 |
| `ev2` | 企业价值EV2 |  | 探测法实测 |
| `ev_exdate` | 现金股息除权日 | TRADEDATE | xla去前缀变体 |
| `ev_paydate` | 现金股息派息日 | TRADEDATE | xla去前缀变体 |
| `exch_city` | 交易所 |  | 探测法实测 |
| `exchange_cn` | 交易所中文名称,s_info_exchange_CN() |  | xla去前缀变体 |
| `excode` | 月合约代码(交易所) | TRADEDATE | xla去前缀变体 |
| `execmaturityembedded` | 含权债行权期限 |  | xla去前缀变体 |
| `executives` | 公司高管 |  | xla去前缀变体 |
| `exemptvat` | 是否免收增值税 |  | xla去前缀变体 |
| `exercisecouponrate_cnbd` | 估算的行权后票面利率 | DEALDATE | xla去前缀变体 |
| `exercisefee` | 期权行权履约手续费 | DEALDATE | xla去前缀变体 |
| `exinterestdebt_current` | 无息流动负债 | REPORTDATE | xla去前缀变体 |
| `exinterestdebt_noncurrent` | 无息非流动负债 | REPORTDATE | xla去前缀变体 |
| `expectedyield` | 预期收益率(文字) |  | xla去前缀变体 |
| `expense_ttm` | 营业支出-金融类(TTM) |  | xla去前缀变体 |
| `expense_ttm2` | 营业支出-金融类(TTM) | REPORTDATE | xla去前缀变体 |
| `expensetosales` | 销售期间费用率 | REPORTDATE | xla去前缀变体 |
| `expensetosales_ttm` | 销售期间费用率(TTM) |  | xla去前缀变体 |
| `expensetosales_ttm2` | 销售期间费用率(TTM) | REPORTDATE | xla去前缀变体 |
| `expiryamtratio` | 到期日期权成交额认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expirycallamount` | 到期日认购期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expirycalloi` | 到期日认购期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expirycallvolume` | 到期日认购期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryoiratio` | 到期日期权持仓量认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryoptionamount` | 到期日期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryoptionoi` | 到期日期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryoptionvolume` | 到期日期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryputamount` | 到期日认沽期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryputoi` | 到期日认沽期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryputvolume` | 到期日认沽期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expiryvolumeratio` | 到期日期权成交量认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `expma` | EXPMA指数平均数 |  | xla原码 |
| `exppropfdleundwt` | 主承销商自营资金获配说明 |  | xla去前缀变体 |
| `extensioncreditenhancementmeasure` | 展期增信措施 | TRADEDATE | xla去前缀变体 |
| `extensioninterestredemptionplan` | 展期利息兑付方案 | TRADEDATE | xla去前缀变体 |
| `extensionprincipalredemptionplan` | 展期本金兑付方案 | TRADEDATE | xla去前缀变体 |
| `extraordinary` | 非经常性损益 | REPORTDATE | xla去前缀变体 |
| `fairvaluechangesincome_forwards` | 远期投资公允价值变动收益 | REPORTDATE | xla去前缀变体 |
| `fairvaluechangesincome_futures` | 期货投资公允价值变动收益 | REPORTDATE | xla去前缀变体 |
| `fairvaluechangesincome_preciousmetal` | 贵金属投资公允价值变动收益 | REPORTDATE | xla去前缀变体 |
| `faturn` | 固定资产周转率 |  | 探测法实测 |
| `fax` | 公司传真 |  | xla去前缀变体 |
| `fcfe` | 股权自由现金流量FCFE | REPORTDATE | xla去前缀变体 |
| `fcfeps` | 每股股东自由现金流量 | REPORTDATE | xla去前缀变体 |
| `fcff` | 企业自由现金流量FCFF | REPORTDATE | xla去前缀变体 |
| `fcffps` | 每股企业自由现金流量 | REPORTDATE | xla去前缀变体 |
| `fcftocf` | 筹资活动产生的现金流量净额占比 | REPORTDATE | xla去前缀变体 |
| `featuredliststd` | 精选层准入标准 |  | xla去前缀变体 |
| `fellow_amount` | 增发数量 | RPTYEAR | xla去前缀变体 |
| `fellow_amt_fund` | 向基金配售数量(新增) |  | xla去前缀变体 |
| `fellow_amt_orgtradable` | 向原流通股东定向配售数量(新增) |  | xla去前缀变体 |
| `fellow_amt_otherpub` | 向其它公众投资者配售数量(新增) |  | xla去前缀变体 |
| `fellow_amt_targeted` | 定向配售数量(新增) |  | xla去前缀变体 |
| `fellow_amtbyplacing` | 网下机构投资者有效申购户数(新增) |  | xla去前缀变体 |
| `fellow_amttoincorp` | 网上向老股东优先配售比例(新增) |  | xla去前缀变体 |
| `fellow_amttoinst` | 网上向老股东优先配售数量(新增) |  | xla去前缀变体 |
| `fellow_amttojur` | 网下超额认购倍数(新增) |  | xla去前缀变体 |
| `fellow_anncedate` | 上网发行公告日(新增) |  | xla去前缀变体 |
| `fellow_approvaldate` | 增发获准日期 |  | xla去前缀变体 |
| `fellow_benchmarkprice` | 定向增发基准价格 |  | xla去前缀变体 |
| `fellow_capeffacc` | 老股东优先配售有效申购户数(新增) |  | xla去前缀变体 |
| `fellow_capeffamt` | 老股东优先配售有效申购股数(新增) |  | xla去前缀变体 |
| `fellow_capratio` | 公开发行认购有效申购户数(新增) |  | xla去前缀变体 |
| `fellow_cashamt` | 公开发行比例认购有效申购股数(新增) |  | xla去前缀变体 |
| `fellow_casheffacc` | 公开发行超额认购倍数(新增) |  | xla去前缀变体 |
| `fellow_cashratio` | 总超额认购倍数(新增) |  | xla去前缀变体 |
| `fellow_collection` | 增发募集资金 | RPTYEAR | xla去前缀变体 |
| `fellow_collection_acct` | 增发募集资金监管银行账户 | Year | xla去前缀变体 |
| `fellow_collection_bank` | 增发募集资金监管银行名称 | Year | xla去前缀变体 |
| `fellow_collection_t` | 区间增发募集资金合计 | StartDate、DATE | xla去前缀变体 |
| `fellow_deputyundr` | 增发上市推荐人(新增) |  | xla去前缀变体 |
| `fellow_dilutedpe` | 增发市盈率(摊薄)(新增) |  | xla去前缀变体 |
| `fellow_discntratio` | 折扣率(新增) |  | xla去前缀变体 |
| `fellow_distor` | 总有效申购户数(新增) |  | xla去前缀变体 |
| `fellow_expectedcollection` | 增发初始预计募集资金总额 | Year | xla去前缀变体 |
| `fellow_expectedcollection_new` | 增发最新预计募集资金总额 | Year | xla去前缀变体 |
| `fellow_expense` | 增发费用 | RPTYEAR | xla去前缀变体 |
| `fellow_firstfeedbackdate` | 增发首次回复日 |  | xla去前缀变体 |
| `fellow_firstinquirydate` | 增发首次问询日 |  | xla去前缀变体 |
| `fellow_iecapprovaldate` | 发审委通过公告日 | Year | xla去前缀变体 |
| `fellow_instlistdate` | 向机构投资者增发部分上市日期(新增) |  | xla去前缀变体 |
| `fellow_intercodnator` | 总有效申购股数(新增) |  | xla去前缀变体 |
| `fellow_issuedate` | 公开发行日(新增) |  | xla去前缀变体 |
| `fellow_issuedate_pp` | 定增发行日期 |  | xla去前缀变体 |
| `fellow_issuetype` | 增发发行方式(新增) |  | xla去前缀变体 |
| `fellow_latestfeedbackdate` | 增发最新回复日 |  | xla去前缀变体 |
| `fellow_latestinquirydate` | 增发最新问询日 |  | xla去前缀变体 |
| `fellow_leadundr` | 增发主承销商(新增) |  | xla去前缀变体 |
| `fellow_listeddate` | 增发上市日 | RPTYEAR | xla去前缀变体 |
| `fellow_n` | 区间定增次数 | StartDate、DATE | xla去前缀变体 |
| `fellow_netcollection` | 增发实际募集资金 | RPTYEAR | xla去前缀变体 |
| `fellow_netprice` | 净值价格(新增) |  | xla去前缀变体 |
| `fellow_nominator` | 增发分销商(新增) |  | xla去前缀变体 |
| `fellow_offeringdate` | 增发公告日(新增) |  | xla去前缀变体 |
| `fellow_otcamt` | 网下发行数量(新增) |  | xla去前缀变体 |
| `fellow_otcamt_pct` | 网下发售比例(新增) |  | xla去前缀变体 |
| `fellow_otcdate` | 向网下增发日期(新增) |  | xla去前缀变体 |
| `fellow_otcpreamt_org` | 网下向老股东优先配售数量(新增) |  | xla去前缀变体 |
| `fellow_oversubratio` | 其它公众投资者有效申购股数(新增) |  | xla去前缀变体 |
| `fellow_payenddate` | 向老股东配售缴款截止日(新增) |  | xla去前缀变体 |
| `fellow_paystartdate` | 向老股东配售缴款起始日(新增) |  | xla去前缀变体 |
| `fellow_preplandate` | 预案公告日(新增) |  | xla去前缀变体 |
| `fellow_price` | 增发价格 | RPTYEAR | xla去前缀变体 |
| `fellow_pricemax` | 增发预案价上限 |  | xla去前缀变体 |
| `fellow_pricemin` | 增发预案价下限 |  | xla去前缀变体 |
| `fellow_pricetobenchmarkprice` | 定向增发实际价格相对基准价格比率 |  | xla去前缀变体 |
| `fellow_pricetoreserveprice` | 定向增发实际价格相对增发底价比率 |  | xla去前缀变体 |
| `fellow_progress` | 增发进度(新增) |  | xla去前缀变体 |
| `fellow_pubamt` | 公开发行数量(新增) |  | xla去前缀变体 |
| `fellow_publicratio` | 公开发行中签率(新增) |  | xla去前缀变体 |
| `fellow_recorddate` | 向老股东配售股权登记日(新增) |  | xla去前缀变体 |
| `fellow_registerdate` | 股权登记日 | Year | xla去前缀变体 |
| `fellow_resultdate` | 发行结果公告日(新增) |  | xla去前缀变体 |
| `fellow_roadshowdate` | 网上路演日 |  | xla去前缀变体 |
| `fellow_shareholders` | 增发发行对象 |  | xla去前缀变体 |
| `fellow_simpleprogram` | 增发是否属于简易程序审核 | Year | xla去前缀变体 |
| `fellow_smtganncedate` | 股东大会公告日(新增) | D | xla去前缀变体 |
| `fellow_subaccbypub` | 其它公众投资者有效申购户数(新增) |  | xla去前缀变体 |
| `fellow_subamtbyplacing` | 网下机构投资者有效申购股数(新增) |  | xla去前缀变体 |
| `fellow_subbydistr` | 承销商认购余股(新增) |  | xla去前缀变体 |
| `fellow_submit_regist_date` | 提交注册日 |  | xla去前缀变体 |
| `fellow_sucregistdate` | 增发注册成功日 | Year | xla去前缀变体 |
| `fellow_totalratio` | 总中签率(新增) |  | xla去前缀变体 |
| `fellow_trnffamt` | 回拨数量(新增) |  | xla去前缀变体 |
| `fellow_undrtype` | 增发承销方式(新增) |  | xla去前缀变体 |
| `fellow_weightedpe` | 增发市盈率(加权)(新增) |  | xla去前缀变体 |
| `fellowon_matchfin` | 增发募集资金(配套融资) | Year | xla去前缀变体 |
| `ficode` | 金融机构分类编码 | Level | xla去前缀变体 |
| `fina_debtexeoffshore` | 债务压力(行权、境外) | StartDate、EndDate | xla去前缀变体 |
| `fina_debtexeonshore` | 债务压力(行权、境内) | StartDate、EndDate | xla去前缀变体 |
| `fina_debtmatoffshore` | 债务压力(到期、境外) | StartDate、EndDate | xla去前缀变体 |
| `fina_debtmatonshore` | 债务压力(到期、境内) | StartDate、EndDate | xla去前缀变体 |
| `fina_mat` | 指定期限内债券余额,B_Fina_mat(新增) | Term | xla去前缀变体 |
| `fina_perpb` | 主体永续债余额 | TRADEDATE | xla去前缀变体 |
| `fina_remainingnumber` | 存量债券数目 |  | xla去前缀变体 |
| `fina_subordinateddebt` | 主体次级债余额 | TRADEDATE | xla去前缀变体 |
| `fina_totalamount` | 总发债券余额,B_Fina_Totalamount(新增) | BType | xla去前缀变体 |
| `fina_totalamount2` | 区间发行债券总额 | StartDate、DATE | xla去前缀变体 |
| `fina_totalamount_meth` | 存量债券余额(按发行方式) | BondType、DEALDATE、Issue | xla去前缀变体 |
| `fina_totalnumber` | 区间发行债券数目 | StartDate、DATE | xla去前缀变体 |
| `finaexpense_ttm` | 财务费用(TTM) |  | xla去前缀变体 |
| `finaexpense_ttm2` | 财务费用(TTM) | REPORTDATE | xla去前缀变体 |
| `finaexpensetogr` | 财务费用／营业总收入 | REPORTDATE | xla去前缀变体 |
| `finaexpensetogr_ttm` | 财务费用／营业总收入(TTM) |  | xla去前缀变体 |
| `finaexpensetogr_ttm2` | 财务费用/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `final_totalamout_anytime` | 存量债券余额(支持历史) | DEALDATE | xla去前缀变体 |
| `financecashflow_ttm` | 筹资活动现金净流量(TTM) |  | xla去前缀变体 |
| `financecashflow_ttm2` | 筹资活动现金净流量(TTM) | REPORTDATE | xla去前缀变体 |
| `fintyothbi` | 发行人金融机构类型 |  | xla去前缀变体 |
| `firstdayofconstituents` | 最早成份日期 |  | xla去前缀变体 |
| `firstincentivedate` | 首次股权激励实施日期 |  | xla去前缀变体 |
| `firstissuebond` | 是否发行人首次发行债券 |  | xla去前缀变体 |
| `firstradeday_s` | 最早交易日期 |  | xla原码 |
| `fiscaldate` | 会计年结日 |  | xla去前缀变体 |
| `fix_assets` | 固定资产 |  | 探测法实测 |
| `float_a_shares` | 流通A股 |  | 探测法实测 |
| `floatingreference` | 浮息基准 |  | xla去前缀变体 |
| `fndate` | 第一通知日 | TRADEDATE | xla去前缀变体 |
| `forward_adjust_date` | 期权到期日展期 | TRADEDATE、EndDate、TermAdjust、ActiveAdjust | xla去前缀变体 |
| `founddate` | 成立日期 |  | xla去前缀变体 |
| `founddate1` | 成立日期 |  | xla去前缀变体 |
| `fpdocreditprofee` | 信用保护费首次支付日 |  | xla去前缀变体 |
| `free_float_shares` | 自由流通股本 |  | 探测法实测 |
| `free_turn` | 换手率(自由流通) |  | 探测法实测 |
| `frmindpdirector` | 公司独立董事(历任)(新增) |  | xla去前缀变体 |
| `ftdate` | 开始交易日 |  | xla去前缀变体 |
| `ftdate_new` | 开始交易日(支持历史) | TRADEDATE | xla去前缀变体 |
| `ftmargins` | 最初交易保证金 |  | xla去前缀变体 |
| `fuamtnewbrwn` | 借新还旧募资金额 |  | xla去前缀变体 |
| `fuamtprojcnstr` | 项目建设募资金额 |  | xla去前缀变体 |
| `fuamtrepibdb` | 偿还有息债务募资金额 |  | xla去前缀变体 |
| `fuamtspmwkcpt` | 补充流动资金募资金额 |  | xla去前缀变体 |
| `fullname` | 债券名称 |  | xla去前缀变体 |
| `fullofferacqpx` | 要约收购价格全价 | DEALDATE | xla去前缀变体 |
| `fullyieldindex` | 全收益指数代码 |  | xla去前缀变体 |
| `fundarrialdate` | 行权资金到帐日 |  | xla去前缀变体 |
| `fundinv_totalamout` | 基金投资收益-卖出/赎回基金成交总额 | REPORTDATE | xla去前缀变体 |
| `fundinv_totalcost` | 基金投资收益-卖出/赎回基金成本总额 | REPORTDATE | xla去前缀变体 |
| `fundinv_transcost` | 基金投资收益-交易费用 | REPORTDATE | xla去前缀变体 |
| `fundinv_vat` | 基金投资收益-买卖基金差价收入应缴纳增值税额 | REPORTDATE | xla去前缀变体 |
| `fundscale_latestdate` | 基金规模最新日期 |  | xla去前缀变体 |
| `funduse` | 募集资金用途 |  | xla去前缀变体 |
| `gamma_exch` | Gamma(交易所) | TRADEDATE | xla去前缀变体 |
| `gc2_ttm2` | 营业总成本2(TTM) | REPORTDATE | xla去前缀变体 |
| `gc_ttm` | 营业总成本(TTM) |  | xla去前缀变体 |
| `gc_ttm2` | 营业总成本(TTM) | REPORTDATE | xla去前缀变体 |
| `gctogr` | 营业总成本／营业总收入 | REPORTDATE | xla去前缀变体 |
| `gctogr_ttm` | 营业总成本／营业总收入(TTM) |  | xla去前缀变体 |
| `gctogr_ttm2` | 营业总成本/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `gdrname` | 同公司GDR简称 |  | xla去前缀变体 |
| `gdrwindcode` | 同公司GDRWind代码 |  | xla去前缀变体 |
| `gr_ttm` | 营业总收入(TTM) |  | xla去前缀变体 |
| `gr_ttm2` | 营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `greenbond` | 是否绿色债 |  | xla去前缀变体 |
| `greenbondnornot` | 是否绿债 |  | xla去前缀变体 |
| `grossmargin` | 毛利 | REPORTDATE | xla去前缀变体 |
| `grossmargin_ttm` | 毛利(TTM) |  | xla去前缀变体 |
| `grossmargin_ttm2` | 毛利(TTM) | REPORTDATE | xla去前缀变体 |
| `grossprofitmargin` | 销售毛利率 |  | 探测法实测 |
| `grossprofitmargin_ttm` | 销售毛利率(TTM) |  | xla去前缀变体 |
| `grossprofitmargin_ttm2` | 毛利率(TTM) |  | 探测法实测 |
| `growth_assets` | 资产总计 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_ebt` | 利润总额 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_equity` | 归属母公司股东的权益 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_gc` | 营业总成本 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_gr` | 营业总收入 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_investincome` | 价值变动净收益 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_netprofit` | 归属母公司股东的净利润 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_netprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_ocf` | 经营活动产生的现金流量净额 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_op` | 营业利润 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_operateincome` | 经营活动净收益 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_or` | 营业收入 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_profit` | 净利润 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_profittosales` | 销售利润率 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_roe` | 净资产收益率 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `growth_totalequity` | 股东权益 (N年, ％) | REPORTDATE | xla去前缀变体 |
| `grps` | 每股营业总收入 | REPORTDATE | xla去前缀变体 |
| `guaranteeornot` | 担保交收 |  | xla去前缀变体 |
| `guaranteesettlement` | 是否可担保交收 |  | xla去前缀变体 |
| `guarantor_type` | 担保人类型 |  | xla去前缀变体 |
| `gxjsornot` | 是否高新技术企业 |  | xla去前缀变体 |
| `handlingdate_pi` | 非公开发行股票受理日 |  | xla去前缀变体 |
| `handlingdate_rs` | 配股受理日 |  | xla去前缀变体 |
| `hedgefee` | 期权套保手续费 | DEALDATE | xla去前缀变体 |
| `hedgelong_margin` | 期货套保多头保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `hedgeshort_margin` | 期货套保空头保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `high` | 最高价 |  | 探测法实测 |
| `highyiled_broker` | 最高价收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `his_avgprice` | 成交均价_期货历史同月 | DATE | xla原码 |
| `his_change` | 涨跌_期货历史同月 | DATE | xla原码 |
| `his_change_settlement` | 涨跌(结算价)_期货历史同月 | DATE | xla原码 |
| `his_close` | 收盘价_期货历史同月 | DATE | xla原码 |
| `his_close_night` | 收盘价(夜盘)_期货历史同月 | TRADEDATE | xla原码 |
| `his_high` | 最高价_期货历史同月 | DATE | xla原码 |
| `his_low` | 最低价_期货历史同月 | DATE | xla原码 |
| `his_oi` | 持仓量_期货历史同月 | DATE | xla原码 |
| `his_oichange` | 持仓变化_期货历史同月 | DATE | xla原码 |
| `his_open` | 开盘价_期货历史同月 | DATE | xla原码 |
| `his_pctchange` | 涨跌幅_期货历史同月 | DATE | xla原码 |
| `his_pctchange_settlement` | 涨跌幅(结算价)_期货历史同月 | DATE | xla原码 |
| `his_presettle` | 前结算价_期货历史同月 | DATE | xla原码 |
| `his_settle` | 结算价_期货历史同月 | DATE | xla原码 |
| `his_swing` | 振幅_期货历史同月 | DATE | xla原码 |
| `his_turnover` | 成交额_期货历史同月 | TRADEDATE | xla原码 |
| `his_volume` | 成交量_期货历史同月 | DATE | xla原码 |
| `hkpcode` | 同公司港股并行Wind代码 |  | xla去前缀变体 |
| `hksc_date` | 纳入港股通日期 | TRADEDATE | xla去前缀变体 |
| `hotconcept` | 所属热门概念 | TRADEDATE | xla去前缀变体 |
| `hsharecode` | 同公司H股代码 |  | xla去前缀变体 |
| `ibdebtratio` | 有息负债率 | REPORTDATE | xla去前缀变体 |
| `ibiratingagency` | 发行时债项评级机构 |  | xla去前缀变体 |
| `icftocf` | 投资活动产生的现金流量净额占比 | REPORTDATE | xla去前缀变体 |
| `iiratingagency` | 发行时主体评级机构 |  | xla去前缀变体 |
| `impairment_ttm` | 资产减值损失(TTM) |  | xla去前缀变体 |
| `impairment_ttm2` | 资产减值损失(TTM) | REPORTDATE | xla去前缀变体 |
| `impairtogr` | 资产减值损失／营业总收入 | REPORTDATE | xla去前缀变体 |
| `impairtogr_ttm` | 资产减值损失／营业总收入(TTM) |  | xla去前缀变体 |
| `impairtogr_ttm2` | 资产减值损失/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `impairtoop` | 资产减值损失/营业利润 | REPORTDATE | xla去前缀变体 |
| `impliedvol` | 隐含波动率(新增) | DEALDATE、RF | xla去前缀变体 |
| `impliedvol_exch` | 期权隐含波动率(交易所) | TRADEDATE | xla去前缀变体 |
| `incashrepur` | 是否含现金要约条款 |  | xla去前缀变体 |
| `incentiveornot` | 是否有股权激励计划 |  | xla去前缀变体 |
| `incondicall` | 是否含有条件赎回条款 |  | xla去前缀变体 |
| `incouprate` | 是否含调整票面利率条款 |  | xla去前缀变体 |
| `indcaloption` | 是否含赎回条款 |  | xla去前缀变体 |
| `indefintepay` | 是否含利息递延权 |  | xla去前缀变体 |
| `indexcode_amac` | 所属AMAC行业指数代码 | TRADEDATE | xla去前缀变体 |
| `indexcode_citic` | 所属中信行业指数代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_cjsc` | 所属长江行业指数代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_cn` | 所属国证行业指数代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_sw` | 所属申万行业指数代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_us` | 所属Wind行业指数代码(美股) | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_wind` | 所属Wind行业指数代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `indexcode_windthematic` | 所属Wind主题行业指数代码 | TRADEDATE | xla去前缀变体 |
| `indexn_us` | 所属Wind行业指数名称(美股) | TRADEDATE、TYPE | xla去前缀变体 |
| `indexname_amac` | 所属AMAC行业指数名称 | TRADEDATE | xla去前缀变体 |
| `indexname_hs` | 所属恒生综合行业指数名称 | TRADEDATE | xla去前缀变体 |
| `indexweight` | 所属指数权重 | TRADEDATE、RelatedIndexType | xla去前缀变体 |
| `industry2` | 所属行业名称(支持历史) | TYPE、IndustryStandard、TRADEDATE | xla去前缀变体 |
| `industry_citic` | 中信行业 |  | 探测法实测 |
| `industry_citiccode` | 所属中信行业代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_citicorigincode` | 所属中信行业原始代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_cjsc` | 所属长江行业名称 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_cn` | 所属国证行业名称 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_cncode` | 所属国证行业代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_csi` | 所属中证行业名称 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_csicode` | 所属中证行业代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_csrc` | 证监会行业-中文 |  | xla去前缀变体 |
| `industry_csrc12` | 所属证监会行业(新) |  | xla去前缀变体 |
| `industry_csrc12_n` | 所属证监会行业名称 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_csrc2023` | 所属挂牌公司管理型行业名称(2023) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_csrccode` | 证监会行业-代码 |  | xla去前缀变体 |
| `industry_csrccode12` | 所属证监会行业代码 | TRADEDATE | xla去前缀变体 |
| `industry_csrccode2023` | 所属挂牌公司管理型行业代码(2023) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_fu` | 期货合约所属行业 |  | xla去前缀变体 |
| `industry_gics` | GICS行业 |  | 探测法实测 |
| `industry_gicscode` | GICS行业-代码 |  | xla去前缀变体 |
| `industry_gx` | 所属国信行业(新增) |  | xla去前缀变体 |
| `industry_hs` | 所属恒生行业 | Category | xla去前缀变体 |
| `industry_hscode` | 所属恒生行业代码 | TYPE | xla去前缀变体 |
| `industry_nc` | 所属国民经济行业分类 | TRADEDATE | xla去前缀变体 |
| `industry_nccode` | 所属国民经济行业代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_neeqconcept` | 所属新三板概念类板块 |  | xla去前缀变体 |
| `industry_neeqgics` | 所属挂牌公司投资型行业名称 | TYPE、TRADEDATE | xla去前缀变体 |
| `industry_neeqgicscode` | 所属挂牌公司投资型行业代码 | TYPE、TRADEDATE | xla去前缀变体 |
| `industry_neeqgicscode_inv` | 所属挂牌公司投资型行业代码 | TYPE、TRADEDATE | xla去前缀变体 |
| `industry_sic` | 所属SIC行业名称(美股) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_siccode` | 所属SIC行业代码(美股) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_sw` | 申万行业 |  | 探测法实测 |
| `industry_sw_2021` | 所属申万行业名称(2021) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_swcode` | 所属申万行业代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_swcode_2021` | 所属申万行业代码(2021) | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_sworigincode` | 所属申万行业原始代码 | TRADEDATE、TYPE | xla去前缀变体 |
| `industry_sworigincode_2021` | 所属申万行业原始代码(2021) | TRADEDATE、TYPE | xla去前缀变体 |
| `industrycode` | 所属行业代码(支持历史) | IndustryStandard、TYPE、TRADEDATE | xla去前缀变体 |
| `industryname` | 所属行业板块代码(支持历史) | IndustryStandard、TYPE、TRADEDATE | xla去前缀变体 |
| `inearlredemp` | 是否含提前购回权 |  | xla去前缀变体 |
| `inequitconve` | 是否含转股条款 |  | xla去前缀变体 |
| `infisoffer` | 是否含优先收购权 |  | xla去前缀变体 |
| `initargin` | 期货合约初始保证金 | TRADEDATE | xla去前缀变体 |
| `inooutstadex` | 是否含开放退出登记 |  | xla去前缀变体 |
| `inprivapla` | 是否含定向转让条款 |  | xla去前缀变体 |
| `inputoption` | 是否含回售条款 |  | xla去前缀变体 |
| `inshd_dlr_buy` | 自营商买进数量 | DEALDATE | xla去前缀变体 |
| `inshd_dlr_ex` | 自营买卖超 | DEALDATE | xla去前缀变体 |
| `inshd_dlr_exmv` | 自营买卖超市值 | DEALDATE | xla去前缀变体 |
| `inshd_dlr_sell` | 自营商卖出数量 | DEALDATE | xla去前缀变体 |
| `inshd_fund_buy` | 投信买进数量 | DEALDATE | xla去前缀变体 |
| `inshd_fund_ex` | 投信买卖超 | DEALDATE | xla去前缀变体 |
| `inshd_fund_exmv` | 投信买卖超市值 | DEALDATE | xla去前缀变体 |
| `inshd_fund_sell` | 投信卖出数量 | DEALDATE | xla去前缀变体 |
| `inshd_qfii_buy` | 外资买进数量 | DEALDATE | xla去前缀变体 |
| `inshd_qfii_ex` | 外资买卖超 | DEALDATE | xla去前缀变体 |
| `inshd_qfii_exmv` | 外资买卖超市值 | DEALDATE | xla去前缀变体 |
| `inshd_qfii_sell` | 外资卖出数量 | DEALDATE | xla去前缀变体 |
| `inshd_ttl_ex` | 合计买卖超 | DEALDATE | xla去前缀变体 |
| `inshd_ttl_exmv` | 合计买卖超市值 | DEALDATE | xla去前缀变体 |
| `inst_yybondrating` | 债项评级(YY) |  | xla去前缀变体 |
| `inst_yybondval` | 债券估值(YY) |  | xla去前缀变体 |
| `inst_yybondvalhis` | 债券估值历史(YY) | TRADEDATE | xla去前缀变体 |
| `inst_yyindustry` | 主体行业(YY) |  | xla去前缀变体 |
| `inst_yyissuerrating` | 主体评级(YY) |  | xla去前缀变体 |
| `inst_yyissuerrating_1` | 主体评级(YY) | TRADEDATE | xla去前缀变体 |
| `inst_yyissuerratinghis` | 主体评级历史(YY) | TRADEDATE | xla去前缀变体 |
| `inst_yyliquidity` | 债券流动性评级(YY) | TRADEDATE | xla去前缀变体 |
| `institution_purchasenum` | 机构席位买入次数 | StartDate、DATE | xla去前缀变体 |
| `institutiontype` | 金融机构类型 |  | xla去前缀变体 |
| `interestdebt` | 带息债务 | REPORTDATE | xla去前缀变体 |
| `interestdebttoev` | 带息债务／股权价值 |  | xla去前缀变体 |
| `interestexpense_ttm` | 利息支出(TTM) | REPORTDATE | xla去前缀变体 |
| `interestfloor` | 保底利率 |  | xla去前缀变体 |
| `interestfrequency` | 转债年付息次数 |  | xla去前缀变体 |
| `interestrate` | 边际利率 |  | xla去前缀变体 |
| `interesttype` | 转债利率类型 |  | xla去前缀变体 |
| `intpositionchg_impshareholder_secmarket` | 重要股东二级市场交易区间持仓市值变动 | StartDate、DATE | xla去前缀变体 |
| `intradayfullprice_cbr` | 日间估值全价(中债资信) | TRADEDATE | xla去前缀变体 |
| `intradayinterest_cbr` | 日间应计利息(中债资信) | TRADEDATE | xla去前缀变体 |
| `intrinctvalue` | 内在价值 |  | xla去前缀变体 |
| `inventories` | 存货 |  | 探测法实测 |
| `investcapital` | 全部投入资本 | REPORTDATE | xla去前缀变体 |
| `investcashflow_ttm` | 投资活动现金净流量(TTM) |  | xla去前缀变体 |
| `investcashflow_ttm2` | 投资活动现金净流量(TTM) | REPORTDATE | xla去前缀变体 |
| `investincome` | 价值变动净收益 | REPORTDATE | xla去前缀变体 |
| `investincome_ttm` | 价值变动净收益(TTM) |  | xla去前缀变体 |
| `investincome_ttm2` | 价值变动净收益(TTM) | REPORTDATE | xla去前缀变体 |
| `investincometoebt` | 价值变动净收益／利润总额 | REPORTDATE | xla去前缀变体 |
| `investincometoebt_ttm` | 价值变动净收益／利润总额(TTM) |  | xla去前缀变体 |
| `investincometoebt_ttm2` | 价值变动净收益/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `investmentfield` | 投向领域 |  | xla去前缀变体 |
| `investorad` | 适当性管理 |  | xla去前缀变体 |
| `invturn` | 存货周转率 |  | 探测法实测 |
| `invturndays` | 存货周转天数 | REPORTDATE | xla去前缀变体 |
| `iopv` | IOPV(新增) | DEALDATE | xla去前缀变体 |
| `ir_fcs` | 基金公司调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_irfd` | 机构调研首日 |  | xla去前缀变体 |
| `ir_irld` | 机构调研最新日 |  | xla去前缀变体 |
| `ir_nofci` | 基金公司调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noiami` | 保险资管调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noifoc` | 其他公司调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noii` | 机构调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noiifi` | 外资机构调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noiiii` | 投资机构调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noiisc` | 证券公司调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noinami` | 保险资管调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nomi` | 媒体(政府)调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nopi` | 个人调研家数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nos` | 被调研总次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosboc` | 其他公司调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_noscbsc` | 证券公司调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosfso` | 特定对象调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosofi` | 外资机构调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosoiam` | 保险资管调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosoii` | 投资机构调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_nosoinam` | 保险资管调研次数 | StartDate、EndDate | xla去前缀变体 |
| `ir_ocmr` | 调研最多的其他公司 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmrfc` | 调研最多的基金公司 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmrfi` | 调研最多的外资机构 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmriam` | 调研最多的保险资管 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmrii` | 调研最多的投资机构 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmrinam` | 调研最多的保险资管 | StartDate、EndDate | xla去前缀变体 |
| `ir_tmssc` | 调研最多的证券公司 | StartDate、EndDate | xla去前缀变体 |
| `is_amortinssvcco` | 摊回保险服务费用 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `is_apportcedprem` | 分出保费的分摊 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `is_cedreinsfingl` | 分出再保险财务损益 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `is_ebitda_ard` | EBITDA(公布值) | REPORTDATE | xla去前缀变体 |
| `is_inssvccosts` | 保险服务费用 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `is_inssvcincome` | 保险服务收入 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `is_sharepayments` | 股权激励支出 | REPORTDATE | xla去前缀变体 |
| `is_uwfinloss` | 承保财务损失 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE | xla去前缀变体 |
| `isassetout` | 资产是否出表 |  | xla去前缀变体 |
| `isscitechbond` | 是否科技创新债券 |  | xla去前缀变体 |
| `issueamount` | 发行总额 |  | 探测法实测 |
| `issuecurrencycode` | 发行币种 |  | xla去前缀变体 |
| `issueok` | 是否发行失败 |  | xla去前缀变体 |
| `issuer` | 创设机构,b_crm_issuer(新增) |  | xla去前缀变体 |
| `issuer2` | 发行人国际评级 | TRADEDATE | xla去前缀变体 |
| `issuer_abbr` | 债务主体中文简称 |  | xla去前缀变体 |
| `issuer_actual` | 实际发行人 |  | xla去前缀变体 |
| `issuer_actual_admin` | 所属行政区划(穿透信用主体) | DivisionType、DEALDATE | xla去前缀变体 |
| `issuer_actual_city` | 城市(穿透信用主体) |  | xla去前缀变体 |
| `issuer_actual_nature1` | 公司属性(穿透信用主体) | TRADEDATE | xla去前缀变体 |
| `issuer_actual_office` | 办公地址(穿透信用主体) |  | xla去前缀变体 |
| `issuer_actual_province` | 省份(穿透信用主体) |  | xla去前缀变体 |
| `issuer_actual_regaddress` | 注册地(穿透信用主体) |  | xla去前缀变体 |
| `issuer_actual_windindustry` | 所属Wind行业名称(穿透信用主体) | TYPE | xla去前缀变体 |
| `issuer_actual_windindustry2024` | 所属Wind行业名称(穿透信用主体)(2024) | TYPE | xla去前缀变体 |
| `issuer_banktype` | 发行人(银行)类型 |  | xla去前缀变体 |
| `issuer_cityinvestmentbondgeoyy` | 城投行政级别(YY) |  | xla去前缀变体 |
| `issuer_industry_ccxi` | 所属中诚信行业名称 | TRADEDATE、TYPE | xla去前缀变体 |
| `issuer_onshore` | 境内发债主体 |  | xla去前缀变体 |
| `issuerfirstdefaultdate` | 发行人首次违约日 |  | xla去前缀变体 |
| `issuerhisrating` | 发债主体历史信用等级(指定机构) | RATINGAGENCY、DEALDATE、RatedCompanyType | xla去前缀变体 |
| `issuerratingoutlook` | 发行时主体评级展望 |  | xla去前缀变体 |
| `issuerscore` | 发行人评分 | TRADEDATE | xla去前缀变体 |
| `issuershortened` | 发行人中文简称 |  | xla去前缀变体 |
| `issuerules` | 发行规则 |  | xla去前缀变体 |
| `issuerupdated` | 债务主体 |  | xla去前缀变体 |
| `issuestructure` | 发行结构 |  | xla去前缀变体 |
| `issurercreditratingcompany` | 发债主体评级机构 |  | xla去前缀变体 |
| `iv_1m1000` | 1个月100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1000_n` | 1个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1000_nr` | 1个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1025` | 1个月102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1025_n` | 1个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1025_nr` | 1个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1050` | 1个月105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1050_n` | 1个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1050_nr` | 1个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m10dc_n` | 1个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m10dc_nr` | 1个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m10dp_n` | 1个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m10dp_nr` | 1个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1100` | 1个月110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1100_n` | 1个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1100_nr` | 1个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1200` | 1个月120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1200_n` | 1个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1200_nr` | 1个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1300` | 1个月130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m1300_n` | 1个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m1300_nr` | 1个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m15dc_n` | 1个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m15dc_nr` | 1个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m15dp_n` | 1个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m15dp_nr` | 1个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m25dc_n` | 1个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m25dc_nr` | 1个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m25dp_n` | 1个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m25dp_nr` | 1个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m35dc_n` | 1个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m35dc_nr` | 1个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m35dp_n` | 1个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m35dp_nr` | 1个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m50d_n` | 1个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m50d_nr` | 1个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m600` | 1个月60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m600_n` | 1个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m600_nr` | 1个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m800` | 1个月80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m800_n` | 1个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m800_nr` | 1个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m900` | 1个月90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m900_n` | 1个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m900_nr` | 1个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m950` | 1个月95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m950_n` | 1个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m950_nr` | 1个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m975` | 1个月97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1m975_n` | 1个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1m975_nr` | 1个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1000` | 1年100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1000_n` | 1年100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1000_nr` | 1年100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1025` | 1年102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1025_n` | 1年102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1025_nr` | 1年102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1050` | 1年105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1050_n` | 1年105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1050_nr` | 1年105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y10dc_n` | 1年10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y10dc_nr` | 1年10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y10dp_n` | 1年10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y10dp_nr` | 1年10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1100` | 1年110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1100_n` | 1年110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1100_nr` | 1年110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1200` | 1年120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1200_n` | 1年120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1200_nr` | 1年120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1300` | 1年130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y1300_n` | 1年130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y1300_nr` | 1年130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y15dc_n` | 1年15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y15dc_nr` | 1年15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y15dp_n` | 1年15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y15dp_nr` | 1年15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y25dc_n` | 1年25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y25dc_nr` | 1年25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y25dp_n` | 1年25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y25dp_nr` | 1年25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y35dc_n` | 1年35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y35dc_nr` | 1年35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y35dp_n` | 1年35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y35dp_nr` | 1年35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y50d_n` | 1年50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y50d_nr` | 1年50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y600` | 1年60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y600_n` | 1年60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y600_nr` | 1年60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y800` | 1年80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y800_n` | 1年80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y800_nr` | 1年80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y900` | 1年90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y900_n` | 1年90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y900_nr` | 1年90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y950` | 1年95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y950_n` | 1年95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y950_nr` | 1年95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y975` | 1年97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_1y975_n` | 1年97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_1y975_nr` | 1年97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1000` | 2个月100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1000_n` | 2个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1000_nr` | 2个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1025` | 2个月102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1025_n` | 2个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1025_nr` | 2个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1050` | 2个月105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1050_n` | 2个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1050_nr` | 2个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m10dc_n` | 2个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m10dc_nr` | 2个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m10dp_n` | 2个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m10dp_nr` | 2个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1100` | 2个月110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1100_n` | 2个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1100_nr` | 2个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1200` | 2个月120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1200_n` | 2个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1200_nr` | 2个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1300` | 2个月130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m1300_n` | 2个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m1300_nr` | 2个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m15dc_n` | 2个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m15dc_nr` | 2个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m15dp_n` | 2个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m15dp_nr` | 2个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m25dc_n` | 2个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m25dc_nr` | 2个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m25dp_n` | 2个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m25dp_nr` | 2个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m35dc_n` | 2个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m35dc_nr` | 2个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m35dp_n` | 2个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m35dp_nr` | 2个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m50d_n` | 2个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m50d_nr` | 2个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m600` | 2个月60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m600_n` | 2个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m600_nr` | 2个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m800` | 2个月80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m800_n` | 2个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m800_nr` | 2个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m900` | 2个月90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m900_n` | 2个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m900_nr` | 2个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m950` | 2个月95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m950_n` | 2个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m950_nr` | 2个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m975` | 2个月97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_2m975_n` | 2个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_2m975_nr` | 2个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1000` | 3个月100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1000_n` | 3个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1000_nr` | 3个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1025` | 3个月102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1025_n` | 3个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1025_nr` | 3个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1050` | 3个月105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1050_n` | 3个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1050_nr` | 3个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m10dc_n` | 3个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m10dc_nr` | 3个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m10dp_n` | 3个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m10dp_nr` | 3个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1100` | 3个月110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1100_n` | 3个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1100_nr` | 3个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1200` | 3个月120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1200_n` | 3个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1200_nr` | 3个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1300` | 3个月130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m1300_n` | 3个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m1300_nr` | 3个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m15dc_n` | 3个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m15dc_nr` | 3个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m15dp_n` | 3个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m15dp_nr` | 3个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m25dc_n` | 3个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m25dc_nr` | 3个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m25dp_n` | 3个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m25dp_nr` | 3个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m35dc_n` | 3个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m35dc_nr` | 3个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m35dp_n` | 3个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m35dp_nr` | 3个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m50d_n` | 3个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m50d_nr` | 3个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m600` | 3个月60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m600_n` | 3个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m600_nr` | 3个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m800` | 3个月80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m800_n` | 3个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m800_nr` | 3个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m900` | 3个月90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m900_n` | 3个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m900_nr` | 3个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m950` | 3个月95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m950_n` | 3个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m950_nr` | 3个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m975` | 3个月97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_3m975_n` | 3个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_3m975_nr` | 3个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1000` | 6个月100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1000_n` | 6个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1000_nr` | 6个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1025` | 6个月102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1025_n` | 6个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1025_nr` | 6个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1050` | 6个月105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1050_n` | 6个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1050_nr` | 6个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m10dc_n` | 6个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m10dc_nr` | 6个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m10dp_n` | 6个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m10dp_nr` | 6个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1100` | 6个月110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1100_n` | 6个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1100_nr` | 6个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1200` | 6个月120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1200_n` | 6个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1200_nr` | 6个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1300` | 6个月130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m1300_n` | 6个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m1300_nr` | 6个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m15dc_n` | 6个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m15dc_nr` | 6个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m15dp_n` | 6个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m15dp_nr` | 6个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m25dc_n` | 6个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m25dc_nr` | 6个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m25dp_n` | 6个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m25dp_nr` | 6个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m35dc_n` | 6个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m35dc_nr` | 6个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m35dp_n` | 6个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m35dp_nr` | 6个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m50d_n` | 6个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m50d_nr` | 6个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m600` | 6个月60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m600_n` | 6个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m600_nr` | 6个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m800` | 6个月80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m800_n` | 6个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m800_nr` | 6个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m900` | 6个月90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m900_n` | 6个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m900_nr` | 6个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m950` | 6个月95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m950_n` | 6个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m950_nr` | 6个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m975` | 6个月97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_6m975_n` | 6个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_6m975_nr` | 6个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1000` | 9个月100%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1000_n` | 9个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1000_nr` | 9个月100%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1025` | 9个月102.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1025_n` | 9个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1025_nr` | 9个月102.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1050` | 9个月105%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1050_n` | 9个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1050_nr` | 9个月105%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m10dc_n` | 9个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m10dc_nr` | 9个月10dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m10dp_n` | 9个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m10dp_nr` | 9个月10dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1100` | 9个月110%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1100_n` | 9个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1100_nr` | 9个月110%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1200` | 9个月120%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1200_n` | 9个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1200_nr` | 9个月120%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1300` | 9个月130%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m1300_n` | 9个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m1300_nr` | 9个月130%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m15dc_n` | 9个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m15dc_nr` | 9个月15dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m15dp_n` | 9个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m15dp_nr` | 9个月15dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m25dc_n` | 9个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m25dc_nr` | 9个月25dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m25dp_n` | 9个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m25dp_nr` | 9个月25dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m35dc_n` | 9个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m35dc_nr` | 9个月35dc隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m35dp_n` | 9个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m35dp_nr` | 9个月35dp隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m50d_n` | 9个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m50d_nr` | 9个月50d隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m600` | 9个月60%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m600_n` | 9个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m600_nr` | 9个月60%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m800` | 9个月80%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m800_n` | 9个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m800_nr` | 9个月80%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m900` | 9个月90%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m900_n` | 9个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m900_nr` | 9个月90%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m950` | 9个月95%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m950_n` | 9个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m950_nr` | 9个月95%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m975` | 9个月97.5%价值状态隐含波动率 | TRADEDATE | xla去前缀变体 |
| `iv_9m975_n` | 9个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `iv_9m975_nr` | 9个月97.5%价值状态隐含波动率 | TRADEDATE、Model | xla去前缀变体 |
| `jensen` | Jensen(新增) | TD1、TD2 | xla去前缀变体 |
| `jenseny` | Jensen(年化)(新增) | TD1、TD2 | xla去前缀变体 |
| `kdj` | KDJ随机指标 |  | xla原码 |
| `largecommodity` | 所属大宗商品概念板块 | TRADEDATE | xla去前缀变体 |
| `lastdate_cfets` | 最新估值日期(中国货币网) |  | xla去前缀变体 |
| `lastdate_cnbd` | 最新中债估值日期 |  | xla去前缀变体 |
| `lastdate_csi` | 最新中证估值日期 |  | xla去前缀变体 |
| `lastdate_shc` | 最新清算所估值日期 |  | xla去前缀变体 |
| `lastradeday_s` | 最近交易日期 |  | xla原码 |
| `lastradeday_ssefi` | 上证固收平台最近交易日 | TRADEDATE | xla去前缀变体 |
| `lasttradingdate` | 最后交易日 |  | xla去前缀变体 |
| `lasttradingday` | 最后交易日 |  | xla去前缀变体 |
| `lastvaluationdate_cbr` | 最新估值日期(中债资信) |  | xla去前缀变体 |
| `latannproreamt` | 最新公布拟转售金额 |  | xla去前缀变体 |
| `latelyrd_bt` | 最新报告期 | TRADEDATE | xla去前缀变体 |
| `latelyrd_bts` | 最新报告期 | TRADEDATE | xla去前缀变体 |
| `latest_rptdate` | 最新报告期 | DATE、DataType | xla去前缀变体 |
| `latestconcept` | 所属最新概念 | TRADEDATE | xla去前缀变体 |
| `latestincentivedate` | 最新股权激励公布时间 | TRADEDATE | xla去前缀变体 |
| `latestincimplementdate` | 最新一次股权激励实施日期 | TRADEDATE | xla去前缀变体 |
| `latestissurercreditrating` | 发债主体最新信用评级 |  | xla去前缀变体 |
| `latestissurercreditrating2` | 主体评级 | TRADEDATE、RATINGAGENCY、RatedCompanyType | xla去前缀变体 |
| `latestissurercreditrating_actual` | 主体评级(主评机构(ABS穿透)) |  | xla去前缀变体 |
| `latestissurercreditratingdate` | 发债主体最新评级日期 |  | xla去前缀变体 |
| `latestissurercreditratingtype` | 发债主体信用评级类型 |  | xla去前缀变体 |
| `latestpar` | 债券最新面值 | TRADEDATE | xla去前缀变体 |
| `latestpar_cnbd` | 剩余本金(中债) | TRADEDATE、Credibility | xla去前缀变体 |
| `latestratingdate` | 发行人最新评级日期(指定机构) | RATINGAGENCY、RatedCompanyType | xla去前缀变体 |
| `latestratingofguarantor` | 担保人最新评级 |  | xla去前缀变体 |
| `latimpreamt` | 最新实施转售金额 |  | xla去前缀变体 |
| `launchdate` | 发布日期 |  | xla去前缀变体 |
| `lddate_new` | 最后交割日(支持历史) | TRADEDATE | xla去前缀变体 |
| `ldiluterate` | 对流通股稀释率(新增) |  | xla去前缀变体 |
| `legalrepresentative` | 法定代表人 | DEALDATE | xla去前缀变体 |
| `lei` | LEI编码 |  | xla去前缀变体 |
| `leverageratio` | 杠杆倍数 |  | xla去前缀变体 |
| `lic` | 经办律师 |  | xla去前缀变体 |
| `limit_cust` | 客户持仓限额 | TRADEDATE | xla去前缀变体 |
| `limit_futu` | 期货公司会员持仓限额 | TRADEDATE | xla去前缀变体 |
| `limit_indi` | 自然人客户持仓限额 | TRADEDATE | xla去前缀变体 |
| `limit_nonfu` | 非期货公司会员持仓限额 | TRADEDATE | xla去前缀变体 |
| `liqholder_num` | 流通股东户数 | TRADEDATE | xla去前缀变体 |
| `list` | 是否上市 |  | xla去前缀变体 |
| `list_floorsubscroffl` | 网下申购下限 |  | xla去前缀变体 |
| `list_floorsubscronl` | 网上申购下限 |  | xla去前缀变体 |
| `list_limitsubscroffl` | 网下申购上限 |  | xla去前缀变体 |
| `list_limitsubscronl` | 网上申购上限 |  | xla去前缀变体 |
| `list_stepsizesubscroffl` | 网下申购步长 |  | xla去前缀变体 |
| `list_stepsizesubscronl` | 网上申购步长 |  | xla去前缀变体 |
| `listdatadate` | 上市公告数据截止日期 |  | xla去前缀变体 |
| `listingornot1` | 是否上市公司 |  | xla去前缀变体 |
| `liststd` | 所属科创板上市标准 |  | xla去前缀变体 |
| `long_margin` | 期货多头保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `longcapitaltoinvestment` | 长期资产适合率 | REPORTDATE | xla去前缀变体 |
| `longdebtodebt` | 非流动负债／负债合计 | REPORTDATE | xla去前缀变体 |
| `longdebttodebt` | 长期负债占比 |  | 探测法实测 |
| `longdebttoequity` | 非流动负债权益比率 | REPORTDATE | xla去前缀变体 |
| `longdebttolongcaptial` | 长期资本负债率 | REPORTDATE | xla去前缀变体 |
| `longdebttoworkingcapital` | 长期债务与营运资金比率 | REPORTDATE | xla去前缀变体 |
| `lotsize` | 每手股数 | DEALDATE | xla去前缀变体 |
| `low` | 最低价 |  | 探测法实测 |
| `lower_limitprice` | 估值全价下限(中债) | DEALDATE | xla去前缀变体 |
| `lowestissurercreditrating` | 发行人最新最低评级 |  | xla去前缀变体 |
| `lowyiled_broker` | 最低价收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `lprice` | 挂牌基准价 |  | xla去前缀变体 |
| `ltdate_new` | 最后交易日(支持历史) | TRADEDATE | xla去前缀变体 |
| `ltdated` | 最后交易日说明 |  | xla去前缀变体 |
| `m_atmcode` | 平值期权代码(价值状态) | TRADEDATE、ExpirationDate、OptionType、Moneyness、AdjustmentState、Exercisetype、TermType、Multipliertype | xla去前缀变体 |
| `m_vol_sufpctl` | 品种波动率曲面分位数 | TRADEDATE、Moneyness、Term、Method、Exercisetype、Multipliertype、StartDate、DATE | xla去前缀变体 |
| `m_vol_surface` | 品种隐含波动率曲面(按价值状态) | TRADEDATE、Moneyness、Term、Construction、Exercisetype、Multipliertype | xla去前缀变体 |
| `ma` | MA简单移动平均 |  | xla原码 |
| `macd` | MACD指数平滑异同平均 |  | xla原码 |
| `mainmargin` | 期货合约维持保证金 | TRADEDATE | xla去前缀变体 |
| `maint_margin` | 期权维持保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `maintenance` | 资本项目规模维持率 | REPORTDATE | xla去前缀变体 |
| `maintermstructure_wind` | Wind主体期限结构曲线 | TRADEDATE、CT、Term | xla去前缀变体 |
| `majorindexcode` | 主指数代码 |  | xla去前缀变体 |
| `majorproductname` | 主营产品名称(新增) |  | xla去前缀变体 |
| `majorproducttype` | 主营产品类型(新增) |  | xla去前缀变体 |
| `makewholecall` | 是否全额可赎回 |  | xla去前缀变体 |
| `mamv` | 备考总市值(并购后) | TRADEDATE | xla去前缀变体 |
| `managementrisk` | 管理风险提示 |  | xla去前缀变体 |
| `manetprofit_fy0` | 备考净利润(FY0,并购后) | TRADEDATE | xla去前缀变体 |
| `manetprofit_fy1` | 备考净利润(FY1,并购后) | TRADEDATE | xla去前缀变体 |
| `manetprofit_fy2` | 备考净利润(FY2,并购后) | TRADEDATE | xla去前缀变体 |
| `manetprofit_fy3` | 备考净利润(FY3,并购后) | TRADEDATE | xla去前缀变体 |
| `mape_fy0` | 备考PE(FY0,并购后) | TRADEDATE | xla去前缀变体 |
| `mape_fy1` | 备考PE(FY1,并购后) | TRADEDATE | xla去前缀变体 |
| `mape_fy2` | 备考PE(FY2,并购后) | TRADEDATE | xla去前缀变体 |
| `mape_fy3` | 备考PE(FY3,并购后) | TRADEDATE | xla去前缀变体 |
| `marginornot` | 是否融资融券标的 | TRADEDATE | xla去前缀变体 |
| `marketmakedate` | 做市首日 |  | xla去前缀变体 |
| `marketrisk` | 市场风险提示 |  | xla去前缀变体 |
| `massredemptionprovision` | 巨额赎回条款 |  | xla去前缀变体 |
| `matotalshares` | 备考总股本(并购后) | TRADEDATE | xla去前缀变体 |
| `matu_cnbd` | 待偿年限(年) |  | xla去前缀变体 |
| `maturitdate` | 到期日期 |  | xla去前缀变体 |
| `maturitycallprice` | 到期赎回价 |  | xla去前缀变体 |
| `maturitydate` | 转债到期日期 |  | xla去前缀变体 |
| `maturityspreadcdb` | 到期利差(减国开) | TRADEDATE | xla去前缀变体 |
| `maturityspreadtb` | 到期利差(减国债) | TRADEDATE | xla去前缀变体 |
| `maxdown` | 跌停价 | TRADEDATE | xla去前缀变体 |
| `maxoq` | 期货合约最大下单量 | TRADEDATE、TYPE | xla去前缀变体 |
| `maxup` | 涨停价 | TRADEDATE | xla去前缀变体 |
| `maxupordown` | 涨跌停状态 |  | 探测法实测 |
| `mcnet_cnbd` | 市场净价(新增) | DATE | xla去前缀变体 |
| `mcyield_cnbd` | 市场收益率(新增) | DATE | xla去前缀变体 |
| `mdirty_cnbd` | 市场全价(新增) | DATE | xla去前缀变体 |
| `media` | 信息指定披露媒体 |  | xla去前缀变体 |
| `median` | N日收盘价中位数 |  | xla去前缀变体 |
| `methodology` | 加权方式 |  | xla去前缀变体 |
| `mfd_buyamt_a` | 主动买入额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_buyamt_at` | 主动买入额(全单) | TRADEDATE | xla去前缀变体 |
| `mfd_buyamt_d` | 流入额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_buyord` | 流入单数 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_buyvol_a` | 主动买入量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_buyvol_at` | 主动买入量(全单) | TRADEDATE | xla去前缀变体 |
| `mfd_buyvol_close_m` | 尾盘主力净流入量 | TRADEDATE | xla去前缀变体 |
| `mfd_buyvol_d` | 流入量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_buyvol_m` | 主力净流入量 | TRADEDATE | xla去前缀变体 |
| `mfd_buyvol_open_m` | 开盘主力净流入量 | TRADEDATE | xla去前缀变体 |
| `mfd_inflow_close_m` | 尾盘主力净流入额 | TRADEDATE | xla去前缀变体 |
| `mfd_inflow_m` | 主力净流入额 | TRADEDATE | xla去前缀变体 |
| `mfd_inflow_open_m` | 开盘主力净流入额 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowdays` | 区间主力净流入天数 | StartDate、EndDate | xla去前缀变体 |
| `mfd_inflowproportion_a` | 净主动买入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowproportion_close_a` | 尾盘净主动买入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowproportion_close_m` | 尾盘主力净流入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowproportion_m` | 主力净流入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowproportion_open_a` | 开盘净主动买入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowproportion_open_m` | 开盘主力净流入额占比 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowrate_close_a` | 尾盘净主动买入率(金额) | TRADEDATE | xla去前缀变体 |
| `mfd_inflowrate_close_m` | 尾盘主力净流入率(金额) | TRADEDATE | xla去前缀变体 |
| `mfd_inflowrate_m` | 主力净流入率(金额) | TRADEDATE | xla去前缀变体 |
| `mfd_inflowrate_open_a` | 开盘净主动买入率(金额) | TRADEDATE | xla去前缀变体 |
| `mfd_inflowrate_open_m` | 开盘主力净流入率(金额) | TRADEDATE | xla去前缀变体 |
| `mfd_inflowvolume_close_a` | 尾盘资金净主动买入量 | TRADEDATE | xla去前缀变体 |
| `mfd_inflowvolume_open_a` | 开盘资金净主动买入量 | TRADEDATE | xla去前缀变体 |
| `mfd_netbuyamt` | 净买入额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_netbuyamt_a` | 净主动买入额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_netbuyvol` | 净买入量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_netbuyvol_a` | 净主动买入量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sellamt_a` | 主动卖出额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sellamt_at` | 主动卖出额(全单) | TRADEDATE | xla去前缀变体 |
| `mfd_sellamt_d` | 流出额 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sellord` | 流出单数 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sellvol_a` | 主动卖出量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sellvol_at` | 主动卖出量(全单) | TRADEDATE | xla去前缀变体 |
| `mfd_sellvol_d` | 流出量 | TRADEDATE、TYPE | xla去前缀变体 |
| `mfd_sn_buyamt` | 沪深港股通买入金额 | TRADEDATE | xla去前缀变体 |
| `mfd_sn_inflow` | 沪深港股通净买入金额 | TRADEDATE | xla去前缀变体 |
| `mfd_sn_sellamt` | 沪深港股通卖出金额 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowproportion_close_a` | 尾盘净主动买入量占比 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowproportion_close_m` | 尾盘主力净流入量占比 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowproportion_m` | 主力净流入量占比 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowproportion_open_a` | 开盘净主动买入量占比 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowproportion_open_m` | 开盘主力净流入量占比 | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_a` | 净主动买入率(量) | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_close_a` | 尾盘净主动买入率(量) | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_close_m` | 尾盘主力净流入率(量) | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_m` | 主力净流入率(量) | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_open_a` | 开盘净主动买入率(量) | TRADEDATE | xla去前缀变体 |
| `mfd_volinflowrate_open_m` | 开盘主力净流入率(量) | TRADEDATE | xla去前缀变体 |
| `mfn_sn_inflowdays` | 持续净流入天数 | TRADEDATE | xla去前缀变体 |
| `mfn_sn_outflowdays` | 持续净卖出天数 | TRADEDATE | xla去前缀变体 |
| `mfp_sn_inflow` | 沪深港股通区间净买入额 | StartDate、EndDate | xla去前缀变体 |
| `mfp_sn_inflowamt` | 区间净买入金额 | StartDate、EndDate | xla去前缀变体 |
| `mfp_sn_inflowamt2` | 沪深港股通区间净买入量(调整) | StartDate、EndDate | xla去前缀变体 |
| `mfp_sn_inflowdays` | 区间净流入天数 | StartDate、EndDate | xla去前缀变体 |
| `mfp_sn_outflowdays` | 区间净流出天数 | StartDate、EndDate | xla去前缀变体 |
| `mfprice` | 发行价格 |  | 探测法实测 |
| `mfprice1` | 最小变动价位(支持历史) | TRADEDATE | xla去前缀变体 |
| `mgmt_sub_ratio` | 管理人认购比例 |  | xla去前缀变体 |
| `mgmt_sub_shares` | 管理人认购份额 |  | xla去前缀变体 |
| `mid_impliedvol` | 期权中价隐含波动率 | TRADEDATE | xla去前缀变体 |
| `mike` | MIKE麦克指标 |  | xla原码 |
| `minoq` | 期货合约最小开仓量下单量 | TRADEDATE、TYPE | xla去前缀变体 |
| `minorityinterest_ttm` | 少数股东损益(TTM) | REPORTDATE | xla去前缀变体 |
| `mkt` | 上市板 |  | xla去前缀变体 |
| `mkt_cap_ard` | 总市值 |  | 探测法实测 |
| `mkt_cap_ashare` | A股市值 |  | 探测法实测 |
| `mkt_freeshares` | 自由流通市值 |  | 探测法实测 |
| `mktcharacter` | 所属市场特征板块 |  | xla去前缀变体 |
| `mktpricetype` | 市价类型 |  | xla去前缀变体 |
| `mktpricetype_suph` | 市价类型(支持历史) | DEALDATE | xla去前缀变体 |
| `modidura_cnbd` | 修正久期 |  | 探测法实测 |
| `modidura_csi` | 估价修正久期(中证指数) |  | xla去前缀变体 |
| `modidura_csi1` | 估价修正久期(中证指数) | DEALDATE、Credibility | xla去前缀变体 |
| `moneyness` | 价值状态 | TRADEDATE | xla去前缀变体 |
| `mq_amount` | 月成交金额(新增) |  | xla去前缀变体 |
| `mq_pctchange` | 月涨跌幅(新增) |  | xla去前缀变体 |
| `mq_turn` | 月换手率(新增) |  | xla去前缀变体 |
| `mq_volume` | 月成交量(新增) |  | xla去前缀变体 |
| `mrg_bal_int_avg` | 区间融资融券余额均值 |  | xla原码 |
| `mrg_long_amt` | 融资余额 |  | 探测法实测 |
| `mrg_long_amt_int` | 区间融资买入额 |  | xla原码 |
| `mrg_long_bal_int_avg` | 区间融资余额均值 |  | xla原码 |
| `mrg_long_repay_int` | 区间融资偿还额 |  | xla原码 |
| `mrg_short_bal_int_avg` | 区间融券余额均值 |  | xla原码 |
| `mrg_short_vol_bal_int_avg` | 区间融券余量均值 |  | xla原码 |
| `mrg_short_vol_int` | 区间融券卖出量 |  | xla原码 |
| `mrg_short_vol_repay_int` | 区间融券偿还量 |  | xla原码 |
| `mtm` | MTM动力指标 |  | xla原码 |
| `multimktornot` | 是否跨市场交易 |  | xla去前缀变体 |
| `multiple` | 边际倍数 |  | xla去前缀变体 |
| `municipalbond` | 是否城投债 |  | xla去前缀变体 |
| `municipalbondwind` | 是否城投债(Wind) |  | xla去前缀变体 |
| `municipalbondyy` | 是否城投债(YY) |  | xla去前缀变体 |
| `munitype` | 地方债类型 |  | xla去前缀变体 |
| `mupc` | 最小价格变动单位 |  | xla去前缀变体 |
| `mv_ref` | 参考总市值 | TRADEDATE | xla去前缀变体 |
| `nafmiil1type` | NAFMII债券一级分类 |  | xla去前缀变体 |
| `nafmiil2type` | NAFMII债券二级分类 |  | xla去前缀变体 |
| `name_official` | 基金简称(官方) |  | xla去前缀变体 |
| `nature` | 公司属性 |  | xla去前缀变体 |
| `nature1` | 公司属性 | TRADEDATE | xla去前缀变体 |
| `ncatoassets` | 非流动资产／总资产 | REPORTDATE | xla去前缀变体 |
| `ncatoequity` | 资本固定化比率 | REPORTDATE | xla去前缀变体 |
| `neeq_green` | 是否绿色通道审核程序挂牌 |  | xla去前缀变体 |
| `neeq_level` | 所属分层 | TRADEDATE | xla去前缀变体 |
| `neeq_listanndate` | 挂牌公告日 |  | xla去前缀变体 |
| `neeq_listdate_innovationlevel` | 创新层挂牌日 |  | xla去前缀变体 |
| `neeq_listingdate` | 挂牌日 |  | xla去前缀变体 |
| `neeq_marketmakeanndate` | 转做市公告日 |  | xla去前缀变体 |
| `neeq_marketmakernum` | 做市商家数 | TRADEDATE | xla去前缀变体 |
| `neeq_park` | 挂牌园区 |  | xla去前缀变体 |
| `neeq_standard` | 所属创新层标准 |  | xla去前缀变体 |
| `neeq_standard2` | 所属挂牌标准(支持历史) | TRADEDATE | xla去前缀变体 |
| `neeq_suspensionday` | 转板精选层前停牌日 |  | xla去前缀变体 |
| `neeqsharewindcode` | 同公司新三板代码 |  | xla去前缀变体 |
| `net_cash_flows_oper_act` | 经营活动现金流净额 |  | 探测法实测 |
| `net_cfets` | 估价净价(中国货币网) | TRADEDATE | xla去前缀变体 |
| `net_cnbd` | 估价净价 |  | xla去前缀变体 |
| `net_csi` | 估价净价(中证指数) |  | xla去前缀变体 |
| `net_csi1` | 估价净价(中证指数) | DEALDATE、Credibility | xla去前缀变体 |
| `net_incr_cash_cash_equ_dm` | 现金及等价物净增加 |  | 探测法实测 |
| `net_profit_is` | 净利润(报表) |  | 探测法实测 |
| `net_shc` | 估价净价(上海清算所) |  | xla去前缀变体 |
| `netask_avg` | 报价卖出净价(算数平均) |  | xla去前缀变体 |
| `netask_bst` | 报价卖出净价(最优) |  | xla去前缀变体 |
| `netasset_total` | 基金规模(合计) | TRADEDATE | xla去前缀变体 |
| `netasset_total2` | 基金规模合计 | TRADEDATE | xla去前缀变体 |
| `netasset_total_cc` | 基金规模(合计,币种转换) | TRADEDATE | xla去前缀变体 |
| `netbid_avg` | 报价买入净价(算数平均) |  | xla去前缀变体 |
| `netbid_bst` | 报价买入净价(最优) |  | xla去前缀变体 |
| `netdebt` | 净债务 | REPORTDATE | xla去前缀变体 |
| `netdebttoev` | 净债务／股权价值 |  | xla去前缀变体 |
| `netofferacqpx` | 要约收购价格净价 | DEALDATE | xla去前缀变体 |
| `netprofit_min` | 扣非净利与归母净利较小值 | REPORTDATE | xla去前缀变体 |
| `netprofit_ttm` | 归属母公司股东的净利润(TTM) |  | xla去前缀变体 |
| `netprofit_ttm2` | 归属母公司股东的净利润(TTM) | REPORTDATE | xla去前缀变体 |
| `netprofitmargin` | 销售净利率 |  | 探测法实测 |
| `netprofitmargin_deducted` | 扣非后销售净利率 | REPORTDATE | xla去前缀变体 |
| `netprofitmargin_ttm` | 销售净利率(TTM) |  | xla去前缀变体 |
| `netprofitmargin_ttm2` | 销售净利率(TTM) | REPORTDATE | xla去前缀变体 |
| `netprofittoassets` | 总资产净利率-不含少数股东损益(TTM) | REPORTDATE | xla去前缀变体 |
| `netprofittoor_ttm` | 归属母公司股东的净利润/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `netturndays` | 净营业周期 | REPORTDATE | xla去前缀变体 |
| `networkingcapital` | 净营运资本 | REPORTDATE | xla去前缀变体 |
| `netyieldindex` | 净收益指数代码 |  | xla去前缀变体 |
| `nextexercisedate` | 下一行权日 | DEALDATE、TYPE | xla去前缀变体 |
| `non_currentassetsturn` | 非流动资产周转率 | REPORTDATE | xla去前缀变体 |
| `nonconnp_ttm` | 非持续经营净利润(TTM) | REPORTDATE、CURTYPE | xla去前缀变体 |
| `nonop_ttm` | 非营业利润(TTM) | REPORTDATE、CURTYPE | xla去前缀变体 |
| `nonoperateprofit_ttm` | 营业外收支净额(TTM) |  | xla去前缀变体 |
| `nonoperateprofit_ttm2` | 营业外收支净额(TTM) | REPORTDATE | xla去前缀变体 |
| `nonoperateprofittoebt` | 营业外收支净额／利润总额 | REPORTDATE | xla去前缀变体 |
| `nonoperateprofittoebt_ttm` | 营业外收支净额／利润总额(TTM) |  | xla去前缀变体 |
| `nonoperateprofittoebt_ttm2` | 营业外收支净额/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `nonoptoebt_ttm` | 非营业利润/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `noplat` | 息前税后经营利润(NOPLAT) | REPORTDATE | xla去前缀变体 |
| `np_belongto_parcomsh` | 归母净利润 |  | 探测法实测 |
| `npl_trust` | 不良资产比率 | Year | xla去前缀变体 |
| `nptocostexpense` | 成本费用利润率 | REPORTDATE | xla去前缀变体 |
| `nq_avgvolume` | N日平均成交量 | N、TRADEDATE、TRADType | xla去前缀变体 |
| `nq_originclose` | 推N日收盘价(债券) |  | xla去前缀变体 |
| `nq_relpctchange` | 相对大盘N日涨跌幅(新增) |  | xla去前缀变体 |
| `numberofconstituents` | 成份个数 |  | xla去前缀变体 |
| `numberofconstituents2` | 成份个数(支持历史) | TRADEDATE | xla去前缀变体 |
| `numspcproj` | 专项项目数量 |  | xla去前缀变体 |
| `nxcupn` | 下一付息日 |  | xla去前缀变体 |
| `nxcupn2` | 距下一付息日天数 |  | xla去前缀变体 |
| `nxoptiondate` | 下一行权日 |  | xla去前缀变体 |
| `obv` | OBV能量潮 |  | xla原码 |
| `ocficftocurrentdebt` | 非筹资性现金净流量与流动负债的比率 | REPORTDATE | xla去前缀变体 |
| `ocficftodebt` | 非筹资性现金净流量与负债总额的比率 | REPORTDATE | xla去前缀变体 |
| `ocfps` | 每股经营活动产生的现金流量净额 | REPORTDATE | xla去前缀变体 |
| `ocfps_ttm` | 每股经营活动产生的现金流量净额(TTM) |  | xla去前缀变体 |
| `ocftoassets` | 全部资产现金回收率 | REPORTDATE | xla去前缀变体 |
| `ocftocf` | 经营活动产生的现金流量净额占比 | REPORTDATE | xla去前缀变体 |
| `ocftodebt` | 经营现金流/负债 |  | 探测法实测 |
| `ocftodividend` | 现金股利保障倍数 | REPORTDATE | xla去前缀变体 |
| `ocftointerest` | 经营现金流/利息 |  | 探测法实测 |
| `ocftointerestdebt` | 经营活动产生的现金流量净额／带息债务 | REPORTDATE | xla去前缀变体 |
| `ocftoinveststockdividend` | 现金满足投资比率 | REPORTDATE | xla去前缀变体 |
| `ocftolongdebt` | 经营活动产生的现金流量净额/非流动负债 | REPORTDATE | xla去前缀变体 |
| `ocftonetdebt` | 经营活动产生的现金流量净额／净债务 | REPORTDATE | xla去前缀变体 |
| `ocftoop` | 现金营运指数 | REPORTDATE | xla去前缀变体 |
| `ocftooperateincome` | 经营活动产生的现金流量净额／经营活动净收益 | REPORTDATE | xla去前缀变体 |
| `ocftooperateincome_ttm` | 经营活动产生的现金流量净额／经营活动净收益(TTM) |  | xla去前缀变体 |
| `ocftooperateincome_ttm2` | 经营活动产生的现金流量净额/经营活动净收益(TTM) | REPORTDATE | xla去前缀变体 |
| `ocftoor` | 经营活动产生的现金流量净额／营业收入 | REPORTDATE | xla去前缀变体 |
| `ocftoor_ttm` | 经营活动产生的现金流量净额／营业收入(TTM) |  | xla去前缀变体 |
| `ocftoor_ttm2` | 经营活动产生的现金流量净额/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `ocftoquickdebt` | 现金到期债务比 | REPORTDATE | xla去前缀变体 |
| `ocftosales` | 经营性现金净流量/营业总收入 | REPORTDATE | xla去前缀变体 |
| `ocftosales_ttm2` | 经营活动产生的现金流量净额/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `ocftoshortdebt` | 经营活动产生的现金流量净额／流动负债 | REPORTDATE | xla去前缀变体 |
| `offeramt` | 要约金额 | DEALDATE | xla去前缀变体 |
| `offercncltndate` | 要约注销日 | DEALDATE | xla去前缀变体 |
| `offerddl` | 要约截止日期 | DEALDATE | xla去前缀变体 |
| `offertime` | 要约时间 | DEALDATE | xla去前缀变体 |
| `office` | 办公地址 |  | xla去前缀变体 |
| `officialstyle` | 指数风格 |  | xla去前缀变体 |
| `ofrclosingyield_broker` | 卖出收盘收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `ofryield_broker` | 卖出平均价收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `oi` | 持仓量_期货历史同月 | DATE | xla去前缀变体 |
| `oichange` | 持仓变化_期货历史同月 | DATE | xla去前缀变体 |
| `oiratio` | 持仓量认沽认购比率 | SettlementMonth、TRADEDATE | xla去前缀变体 |
| `op_active_undly` | 期权主力标的代码 | TRADEDATE | xla去前缀变体 |
| `op_cat` | 证券类型(期权用) | Level | xla去前缀变体 |
| `op_multipliertype` | 期权规模类型 |  | xla去前缀变体 |
| `op_termtype` | 期权期限类型 |  | xla去前缀变体 |
| `op_ttm` | 营业利润(TTM) |  | xla去前缀变体 |
| `op_ttm2` | 营业利润(TTM) | REPORTDATE | xla去前缀变体 |
| `open` | 开盘价 |  | 探测法实测 |
| `open_auction_amount` | 开盘集合竞价成交额 | TRADEDATE | xla去前缀变体 |
| `open_auction_amount_t` | 开盘集合竞价成交额(分时段) | TRADEDATE、SESSION_TYPE | xla去前缀变体 |
| `open_auction_price` | 开盘集合竞价成交价 | TRADEDATE | xla去前缀变体 |
| `open_auction_price_t` | 开盘集合竞价成交价(分时段) | TRADEDATE、SESSION_TYPE | xla去前缀变体 |
| `open_auction_volume` | 开盘集合竞价成交量 | TRADEDATE | xla去前缀变体 |
| `open_auction_volume_t` | 开盘集合竞价成交量(分时段) | TRADEDATE、SESSION_TYPE | xla去前缀变体 |
| `oper_cost` | 营业成本 |  | 探测法实测 |
| `oper_rev` | 营业收入 |  | 探测法实测 |
| `operatecaptialturn` | 营运资本周转率 | REPORTDATE | xla去前缀变体 |
| `operatecashflow_ttm` | 经营活动现金净流量(TTM) |  | xla去前缀变体 |
| `operatecashflow_ttm2` | 经营活动现金净流量(TTM) | REPORTDATE | xla去前缀变体 |
| `operatecashflowtoop_ttm` | 经营活动产生的现金流量净额/营业利润(TTM) | REPORTDATE | xla去前缀变体 |
| `operateexpense_ttm` | 销售费用(TTM) |  | xla去前缀变体 |
| `operateexpense_ttm2` | 销售费用(TTM) | REPORTDATE | xla去前缀变体 |
| `operateexpensetogr` | 营业费用／营业总收入 | REPORTDATE | xla去前缀变体 |
| `operateexpensetogr_ttm` | 营业费用／营业总收入(TTM) |  | xla去前缀变体 |
| `operateexpensetogr_ttm2` | 销售费用/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `operateincome` | 经营活动净收益 | REPORTDATE | xla去前缀变体 |
| `operateincome_ttm` | 经营活动净收益(TTM) |  | xla去前缀变体 |
| `operateincome_ttm2` | 经营活动净收益(TTM) | REPORTDATE | xla去前缀变体 |
| `operateincometoebt` | 经营活动净收益／利润总额 | REPORTDATE | xla去前缀变体 |
| `operateincometoebt_ttm` | 经营活动净收益／利润总额(TTM) |  | xla去前缀变体 |
| `operateincometoebt_ttm2` | 经营活动净收益/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `oplimit_client` | 期货公司客户期货开仓限额 | TRADEDATE | xla去前缀变体 |
| `oplimit_ftcom` | 期货公司会员期货开仓限额 | TRADEDATE | xla去前缀变体 |
| `oplimit_nonft` | 非期货公司会员期货开仓限额 | TRADEDATE | xla去前缀变体 |
| `oplimitcust` | 客户期权持仓限额 | TRADEDATE、Category、Limit | xla去前缀变体 |
| `oplimitfutu` | 期货公司会员期权持仓限额 | TRADEDATE、Category、Limit | xla去前缀变体 |
| `oplimitmark` | 做市商期权持仓限额 | TRADEDATE、Category、Limit | xla去前缀变体 |
| `oplimitnonfu` | 非期货公司会员期权持仓限额 | TRADEDATE、Category、Limit | xla去前缀变体 |
| `opriskfreerate` | 期权无风险利率 | TRADEDATE | xla去前缀变体 |
| `optionamount` | 品种成交额 | TRADEDATE | xla去前缀变体 |
| `optionoi` | 品种持仓量 | TRADEDATE | xla去前缀变体 |
| `optionspreadcdb` | 行权利差(减国开) | TRADEDATE | xla去前缀变体 |
| `optionspreadtb` | 行权利差(减国债) | TRADEDATE | xla去前缀变体 |
| `optionval_cnbd` | 期权价值(中债) | TRADEDATE | xla去前缀变体 |
| `optionvolume` | 品种成交量 | TRADEDATE | xla去前缀变体 |
| `optoebt` | 主营业务比率 | REPORTDATE | xla去前缀变体 |
| `optoebt_ttm2` | 营业利润/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `optogr` | 营业利润／营业总收入 | REPORTDATE | xla去前缀变体 |
| `optogr_ttm` | 营业利润／营业总收入(TTM) |  | xla去前缀变体 |
| `optogr_ttm2` | 营业利润/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `optoor_ttm` | 营业利润/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `or_ttm` | 营业收入(TTM) |  | 探测法实测 |
| `or_ttm2` | 营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `organizationcode` | 组织机构代码 |  | xla去前缀变体 |
| `orps` | 每股营业收入 | REPORTDATE | xla去前缀变体 |
| `orps_ttm` | 每股营业收入(TTM) |  | xla去前缀变体 |
| `otherrisks` | 其他风险提示 |  | xla去前缀变体 |
| `outstandingbalance` | 债券余额,B_info_OutstandingBalance(新增) | DATE | xla去前缀变体 |
| `pandabonds` | 是否熊猫债 |  | xla去前缀变体 |
| `par` | 转债面值 |  | xla去前缀变体 |
| `parallelcode` | 是否并行代码 |  | xla去前缀变体 |
| `parvalue` | 面值(新增) |  | xla去前缀变体 |
| `paydiscdate` | 付息公告日 |  | xla去前缀变体 |
| `paymentdate` | 年付息日 |  | xla原码 |
| `paymentorder` | 偿付顺序 |  | xla去前缀变体 |
| `pb` | 市净率PB |  | 探测法实测 |
| `pb_lf` | 市净率PB(LF) |  | 探测法实测 |
| `pb_lyr` | 市净率(PB, LYR) |  | xla去前缀变体 |
| `pb_mrq` | 市净率PB(MRQ) |  | 探测法实测 |
| `pcf_ncf` | 市现率(PCF,现金净流量) |  | xla去前缀变体 |
| `pcf_ncf_ttm` | 市现率PCF(净额,TTM) |  | 探测法实测 |
| `pcf_ocf` | 市现率(PCF,经营现金流) |  | xla去前缀变体 |
| `pcf_ocf_ttm` | 市现率PCF(经营,TTM) |  | 探测法实测 |
| `pct_chg` | 涨跌幅 |  | 探测法实测 |
| `pctchange_close` | 涨跌幅(收盘价) | TRADEDATE | xla去前缀变体 |
| `peg` | 历史PEG |  | xla去前缀变体 |
| `pelyr_ref` | 参考市盈率PE(LYR) | TRADEDATE | xla去前缀变体 |
| `performancedate` | 业绩说明会日期 | REPORTDATE | xla去前缀变体 |
| `performanceexp_bps_os` | 业绩快报.归属母公司普通股股东每股净资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_bps` | 业绩快报.每股净资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_bps_b` | 业绩快报.期初每股净资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_bps_growth` | 业绩快报.比年初增长率:归属于母公司股东的每股净资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_date` | 业绩快报披露日(新增) | D | xla去前缀变体 |
| `performanceexpress_ebt_yoy` | 业绩快报.同比增长率:利润总额 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_eps_ya` | 业绩快报.去年同期每股收益 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_eps_yoy` | 业绩快报.同比增长率:基本每股收益 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_eqy_growth` | 业绩快报.比年初增长率:归属母公司的股东权益 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_income_ya` | 业绩快报.去年同期营业收入 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_lastdate` | 业绩快报最新披露日期 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_lastrptdate` | 最新业绩快报报告期 |  | xla去前缀变体 |
| `performanceexpress_lrsd` | 截止指定日期最新业绩快报报告期 | TRADEDATE | xla去前缀变体 |
| `performanceexpress_netassets_b` | 业绩快报.期初净资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_netprofit_ya` | 业绩快报.去年同期净利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_np_yoy` | 业绩快报.同比增长率:归属母公司股东的净利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_npded_ya` | 业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_npded_yoy` | 业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_npdedtoshareholder` | 业绩快报.归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_op_yoy` | 业绩快报.同比增长率:营业利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_or_yoy` | 业绩快报.同比增长率:营业收入 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_perfexepsdiluted` | 业绩快报.每股收益EPS-摊薄(新增) | D | xla去前缀变体 |
| `performanceexpress_perfexincome` | 业绩快报.主营业务收入(新增) | D | xla去前缀变体 |
| `performanceexpress_perfexnetassets` | 业绩快报.净资产(新增) | D | xla去前缀变体 |
| `performanceexpress_perfexnetprofittoshareholder` | 业绩快报.归属母公司股东的净利润(新增) | D | xla去前缀变体 |
| `performanceexpress_perfexprofit` | 业绩快报.营业利润(新增) | D | xla去前缀变体 |
| `performanceexpress_perfexroediluted` | 业绩快报.净资产收益率ROE-摊薄(新增) | D | xla去前缀变体 |
| `performanceexpress_perfextotalassets` | 业绩快报.总资产(新增) | D | xla去前缀变体 |
| `performanceexpress_perfextotalprofit` | 业绩快报.利润总额(新增) | D | xla去前缀变体 |
| `performanceexpress_profit_ya` | 业绩快报.去年同期营业利润 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_roe_yoy` | 业绩快报.同比增减:加权平均净资产收益率 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_totassets_growth` | 业绩快报.比年初增长率:总资产 | REPORTDATE | xla去前缀变体 |
| `performanceexpress_totprofit_ya` | 业绩快报.去年同期利润总额 | REPORTDATE | xla去前缀变体 |
| `performancetime` | 业绩说明会时间 | REPORTDATE | xla去前缀变体 |
| `periodexpense_t_ttm` | 期间费用(TTM) | REPORTDATE | xla去前缀变体 |
| `periodexpense_ttm` | 期间费用(TTM) | REPORTDATE、CURTYPE | xla去前缀变体 |
| `periodmf_netinflow` | 区间净流入额 | StartDate、EndDate | xla去前缀变体 |
| `periodreturnranking_10y` | 近10年回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_1m` | 近1月回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_1w` | 近1周回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_1y` | 近1年回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_2y` | 近2年回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_3m` | 近3月回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_3y` | 近3年回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_5y` | 近5年回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_6m` | 近6月回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_y` | 单年度回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `periodreturnranking_ytd` | 今年以来回报排名 | TRADEDATE、FundGroup | xla去前缀变体 |
| `perpeintertax` | 利息是否免税(永续债) |  | xla去前缀变体 |
| `perpetualornot` | 是否永续债 |  | xla去前缀变体 |
| `phone` | 公司电话 |  | xla去前缀变体 |
| `pmir_redeemspread` | 贵金属投资收益-赎回差价收入 | REPORTDATE | xla去前缀变体 |
| `pmir_subscribespread` | 贵金属投资收益-申购差价收入 | REPORTDATE | xla去前缀变体 |
| `pmir_total` | 贵金属投资收益-合计 | REPORTDATE | xla去前缀变体 |
| `pmir_tradespread` | 贵金属投资收益-买卖贵金属差价收入 | REPORTDATE | xla去前缀变体 |
| `pmirredeemspread_total` | 贵金属赎回差价收入-合计 | REPORTDATE | xla去前缀变体 |
| `pmirredeemspread_totalredempamt` | 贵金属赎回差价收入-赎回贵金属份额对价总额 | REPORTDATE | xla去前缀变体 |
| `pmirredeemspread_totalredempamtpic` | 贵金属赎回差价收入-现金支付赎回款总额 | REPORTDATE | xla去前缀变体 |
| `pmirredeemspread_totalredempcpm` | 贵金属赎回差价收入-赎回贵金属成本总额 | REPORTDATE | xla去前缀变体 |
| `pmirredeemspread_transcost` | 贵金属赎回差价收入-交易费用 | REPORTDATE | xla去前缀变体 |
| `pmirtradespread_total` | 买卖贵金属差价收入-合计 | REPORTDATE | xla去前缀变体 |
| `pmirtradespread_totalamout` | 买卖贵金属差价收入-卖出贵金属成交总额 | REPORTDATE | xla去前缀变体 |
| `pmirtradespread_totcost` | 买卖贵金属差价收入-卖出贵金属成本总额 | REPORTDATE | xla去前缀变体 |
| `pmirtradespread_transcost` | 买卖贵金属差价收入-交易费用 | REPORTDATE | xla去前缀变体 |
| `pohqe` | 被剔除的最高价申报量占比 |  | xla去前缀变体 |
| `poqe` | 被剔除的申报量占比 |  | xla去前缀变体 |
| `pq_abnormaltrade_lp` | 区间龙虎榜净买入额 | StartDate、EndDate | xla去前缀变体 |
| `pq_abnormaltrade_sp` | 区间龙虎榜净卖出额 | StartDate、EndDate | xla去前缀变体 |
| `pq_abnormaltradenum` | 区间龙虎榜上榜次数 | StartDate、EndDate | xla去前缀变体 |
| `pq_amount` | 区间成交额 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_amount_aht` | 区间盘后成交额 | StartDate、EndDate | xla去前缀变体 |
| `pq_avgashrmv` | 区间日均A股市值(不含限售股) | StartDate、DATE | xla去前缀变体 |
| `pq_avgashrmv2` | 区间日均A股市值(含限售股) | StartDate、DATE | xla去前缀变体 |
| `pq_avgashrmv2_es` | 区间日均A股市值(不含限售股)(剔除停牌日) | StartDate、DATE | xla去前缀变体 |
| `pq_avgashrmv_es` | 区间日均A股市值(含限售股)(剔除停牌日) | StartDate、DATE | xla去前缀变体 |
| `pq_avgmv_es` | 区间日均总市值(剔除停牌日) | StartDate、DATE | xla去前缀变体 |
| `pq_avgmv_nonrestricted` | 区间日均流通市值 | StartDate、DATE、CURTYPE | xla去前缀变体 |
| `pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_avgprice2` | 区间成交均价(可复权) | StartDate、EndDate、AdjustType | xla去前缀变体 |
| `pq_avgturn2` | 区间日均换手率 | StartDate、EndDate | xla去前缀变体 |
| `pq_blocktrade_volume` | 区间大宗交易成交总量 | StartDate、EndDate | xla去前缀变体 |
| `pq_blocktradeamount` | 区间大宗交易成交总额 | StartDate、EndDate | xla去前缀变体 |
| `pq_blocktradeamounts` | 区间成交额(含大宗交易) | StartDate、EndDate | xla去前缀变体 |
| `pq_blocktradenum` | 区间大宗交易上榜次数 | StartDate、EndDate | xla去前缀变体 |
| `pq_blocktradevolume` | 区间成交量(含大宗交易) | StartDate、EndDate | xla去前缀变体 |
| `pq_change` | 区间涨跌 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_close` | 区间收盘价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_close_percentile` | 收盘价分位数 | TRADEDATE、StartDate、EndDate、AdjustType | xla去前缀变体 |
| `pq_ctnslimitdowndays` | 区间连续跌停天数 | StartDate、EndDate | xla去前缀变体 |
| `pq_ctnslimitupdays` | 区间连续涨停天数 | StartDate、EndDate | xla去前缀变体 |
| `pq_high` | 区间最高价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_high_date` | 区间最高价日 | StartDate、EndDate、PRICETYPE | xla去前缀变体 |
| `pq_highamount` | 区间最高成交额 | StartDate、EndDate | xla去前缀变体 |
| `pq_highamount_date` | 区间最高成交额日 | StartDate、EndDate | xla去前缀变体 |
| `pq_highestcreditrating` | 区间最高主体评级 | StartDate、DATE、RATINGAGENCY | xla去前缀变体 |
| `pq_highsettle_date` | 区间最高结算价日(支持复权) | StartDate、DATE | xla去前缀变体 |
| `pq_low` | 区间最低价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_low_date` | 区间最低价日 | StartDate、EndDate、PRICETYPE | xla去前缀变体 |
| `pq_lowestcreditrating` | 区间最低主体评级 | StartDate、DATE、RATINGAGENCY | xla去前缀变体 |
| `pq_lowsettle_date` | 区间最低结算价日(支持复权) | StartDate、DATE | xla去前缀变体 |
| `pq_maxuptype` | N天M板 | TRADEDATE | xla去前缀变体 |
| `pq_newh` | 创N日新高 | SDATE、DATE、AdjustType、PriceType | xla去前缀变体 |
| `pq_newl` | 创N日新低 | SDATE、DATE、AdjustType、PriceType | xla去前缀变体 |
| `pq_open` | 区间开盘价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_pctchange2` | 区间涨跌幅(包含上市首日涨跌幅) | StartDate、EndDate | xla去前缀变体 |
| `pq_pctchange_a` | 区间涨跌幅(年化) | StartDate、EndDate | xla去前缀变体 |
| `pq_pctchange_close` | 区间涨跌幅(收盘价) | SDATE、DATE | xla去前缀变体 |
| `pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_relpctchange` | 相对大盘区间涨跌幅(新增) | TD1、TD2 | xla去前缀变体 |
| `pq_relpctchange2` | 相对大盘区间涨跌幅(包含上市首日涨跌幅) | StartDate、EndDate | xla去前缀变体 |
| `pq_relpctchange_10d` | 近10日相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_1m` | 近1月相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_1y` | 近1年相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_3m` | 近3月相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_5d` | 近5日相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_6m` | 近6月相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_mtd` | 本月至今相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relpctchange_ytd` | 年迄今相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_relrelpctchange_mtd` | 季度至今相对指数涨跌幅 | TYPE | xla去前缀变体 |
| `pq_suspendenddate` | 长期停牌截止日 | TRADEDATE | xla去前缀变体 |
| `pq_suspendstartdate` | 长期停牌起始日 | TRADEDATE | xla去前缀变体 |
| `pq_topstockheldno` | 区间重仓股报告期重仓次数 | StartDate、EndDate、TopN | xla去前缀变体 |
| `pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_volume` | 区间成交量 | BEGINDATE、EndDate | xla去前缀变体 |
| `pq_volume_aht` | 区间盘后成交量 | StartDate、EndDate | xla去前缀变体 |
| `prdstrong` | 阶段强势指标 |  | xla原码 |
| `prdweak` | 阶段弱势指标 |  | xla原码 |
| `pre_close` | 前收盘价 |  | 探测法实测 |
| `preclose_ssefi` | 上证固收平台前收盘价 | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `precode` | 证券曾用Wind代码 | TRADEDATE | xla去前缀变体 |
| `premiumrate_ah` | AH股溢价率 | TRADEDATE | xla去前缀变体 |
| `prename` | 证券曾用名 |  | xla去前缀变体 |
| `prepaymentdate` | 含权债提前还款日期 |  | xla去前缀变体 |
| `prepaymethod` | 提前还本方式 |  | xla去前缀变体 |
| `prepayportion` | 提前还本比例 | Serial | xla去前缀变体 |
| `prevwtdavgpice_ssefi` | 上证固收平台前加权均价 | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `prewindcode` | Wind自定义代码 |  | xla原码 |
| `prf_valuedate` | 优先股起息日 |  | xla去前缀变体 |
| `prfshareissue_collection` | 区间优先股募集资金合计 | StartDate、DATE | xla去前缀变体 |
| `priceosc` | PRICEOSC价格振荡指标 |  | xla原码 |
| `profit_ttm` | 净利润(TTM) |  | xla去前缀变体 |
| `profit_ttm2` | 净利润(TTM) | REPORTDATE | xla去前缀变体 |
| `profitnotice_abstract` | 业绩预告摘要 | REPORTDATE | xla去前缀变体 |
| `profitnotice_basicearnmax` | 预告基本每股收益下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_basicearnmin` | 预告基本每股收益上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_changemax` | 预告净利润同比增长上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_changemin` | 预告净利润同比增长下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_date` | 业绩预告日期(新增) | D | xla去前缀变体 |
| `profitnotice_deductedearnmax` | 预告扣非后基本每股收益上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedearnmin` | 预告扣非后基本每股收益下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedprofitmax` | 预告扣非净利润上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedprofitmin` | 预告扣非净利润下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedprofityoymax` | 预告扣非净利润同比增长上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedprofityoymin` | 预告扣非净利润同比增长下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedsalesmax` | 预告扣除后营业收入上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_deductedsalesmin` | 预告扣除后营业收入下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_firstdate` | 业绩预告首次披露日期 | REPORTDATE | xla去前缀变体 |
| `profitnotice_incomemax` | 预告营业收入上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_incomemin` | 预告营业收入下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lasteps` | 去年同期每股收益(新增) | D | xla去前缀变体 |
| `profitnotice_lastoe` | 上年同期归属于母公司所有者权益 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lastrptdate` | 最新业绩预告报告期 |  | xla去前缀变体 |
| `profitnotice_lastyearbasicearn` | 上年同期基本每股收益 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lastyeardeductedearn` | 上年同期扣非后基本每股收益 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lastyeardeductedprofit` | 上年同期扣非净利润 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lastyeardeductedsales` | 上年同期扣除后营业收入 | REPORTDATE | xla去前缀变体 |
| `profitnotice_lastyearincome` | 上年同期营业收入 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netprofitmax` | 预告净利润上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netprofitmin` | 预告净利润下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netsalesmax` | 预告净营收上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netsalesmin` | 预告净营收下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netsalesyoymax` | 预告净营收同比增长上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_netsalesyoymin` | 预告净营收同比增长下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_oemax` | 预告归属于母公司所有者权益上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_oemin` | 预告归属于母公司所有者权益下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_reason` | 业绩预告变动原因 | REPORTDATE | xla去前缀变体 |
| `profitnotice_salesmax` | 预告总营收上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_salesmin` | 预告总营收下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_salesyoymax` | 预告总营收同比增长上限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_salesyoymin` | 预告总营收同比增长下限 | REPORTDATE | xla去前缀变体 |
| `profitnotice_style` | 业绩预告类型 | REPORTDATE | xla去前缀变体 |
| `profittogr` | 净利润／营业总收入 | REPORTDATE | xla去前缀变体 |
| `profittogr_ttm` | 净利润／营业总收入(TTM) |  | xla去前缀变体 |
| `profittogr_ttm2` | 净利润/营业总收入(TTM) | REPORTDATE | xla去前缀变体 |
| `prornot` | 是否PR债 |  | xla去前缀变体 |
| `province` | 主体地区 |  | xla去前缀变体 |
| `prt_absbycreditrating` | 按信用评级的资产支持证券投资市值 | REPORTDATE、CreditRatingType、CalcType | xla去前缀变体 |
| `prt_absbycreditratingtonav` | 按信用评级的资产支持证券投资占基金资产净值比 | REPORTDATE、CreditRatingType、CalcType | xla去前缀变体 |
| `prt_abstonav` | 资产支持证券市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_absvalue` | 资产支持证券市值 | REPORTDATE | xla去前缀变体 |
| `prt_avgnetasset` | 报告期基金日均资产净值 | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit` | 基金银行存款-合计 | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_dd` | 基金银行存款-活期存款 | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_ddabd` | 基金银行存款-活期存款(坏账准备) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_ddai` | 基金银行存款-活期存款(应计利息) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_ddp` | 基金银行存款-活期存款(本金) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_fbd` | 基金银行存款-其他存款 | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_fbdabd` | 基金银行存款-其他存款(坏账准备) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_fbdai` | 基金银行存款-其他存款(应计利息) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_fbdp` | 基金银行存款-其他存款(本金) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_ltd` | 基金银行存款-定期存款(存款期限3个月以上) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_omtd` | 基金银行存款-定期存款(存款期限1个月以内) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_td` | 基金银行存款-定期存款 | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_tdabd` | 基金银行存款-定期存款(坏账准备) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_tdai` | 基金银行存款-定期存款(应计利息) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_tdp` | 基金银行存款-定期存款(本金) | REPORTDATE | xla去前缀变体 |
| `prt_bankdeposit_tmtd` | 基金银行存款-定期存款(存款期限1-3个月) | REPORTDATE | xla去前缀变体 |
| `prt_bondbycreditrating` | 按信用评级的债券投资市值 | REPORTDATE、CreditRatingType、CalcType | xla去前缀变体 |
| `prt_bondbycreditratingtonav` | 按信用评级的债券投资占基金资产净值比 | REPORTDATE、CreditRatingType、CalcType | xla去前缀变体 |
| `prt_bondtoasset` | 债券市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_bondtonav` | 债券市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_bondtonavgrowth` | 债券市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_bondvalue` | 债券投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_bondvaluegrowth` | 债券市值增长率 |  | xla去前缀变体 |
| `prt_buystockcost` | 报告期买入股票总成本(新增) | REPORTDATE | xla去前缀变体 |
| `prt_cash` | 银行存款 | REPORTDATE | xla去前缀变体 |
| `prt_cashtoasset` | 银行存款占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_cashtonav` | 银行存款占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_cashtonavgrowth` | 银行存款市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_cashvaluegrowth` | 银行存款市值增长率 |  | xla去前缀变体 |
| `prt_cds` | 同业存单市值 | REPORTDATE | xla去前缀变体 |
| `prt_cdstonav` | 同业存单市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_centralbankbill` | 央行票据投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_centralbankbillgrowth` | 央行票据市值增长率 |  | xla去前缀变体 |
| `prt_centralbankbilltoasset` | 央行票据市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_centralbankbilltobond` | 央行票据市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_centralbankbilltonav` | 央行票据市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_centralbankbilltonavgrowth` | 央行票据市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_commercialpapertobond` | 短期融资券市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_convertiblebond` | 可转债投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_convertiblebondgrowth` | 可转债市值增长率 |  | xla去前缀变体 |
| `prt_convertiblebondtoasset` | 可转债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_convertiblebondtobond` | 可转债市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_convertiblebondtonav` | 可转债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_convertiblebondtonavgrowth` | 可转债市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_corporatebond` | 企债投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondgrowth` | 企业债市值增长率 |  | xla去前缀变体 |
| `prt_corporatebonds` | 企业债市值 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondsgrowth` | 企业债市值增长率 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondstoasset` | 企业债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondstobond` | 企业债市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondstonav` | 企业债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondstonavgrowth` | 企业债市值占基金资产净值比例增长 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondtoasset` | 企业债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondtobond` | 企业债市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondtonav` | 企业债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_corporatebondtonavgrowth` | 企业债市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_countryregioninvestment` | 国家/地区投资市值 | REPORTDATE、ZoneType | xla去前缀变体 |
| `prt_countryregioninvestmenttonav` | 国家/地区投资市值占基金资产净值比例 | REPORTDATE、ZoneType | xla去前缀变体 |
| `prt_cptoasset` | 短期融资券市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_cptonav` | 短期融资券市值占基金资产净值比 |  | xla去前缀变体 |
| `prt_cpvalue` | 短期融资券市值 | REPORTDATE | xla去前缀变体 |
| `prt_currency` | 报告期基金资产净值币种 | REPORTDATE | xla去前缀变体 |
| `prt_financialbond` | 金融债投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_financialbondgrowth` | 金融债市值增长率 |  | xla去前缀变体 |
| `prt_financialbondtoasset` | 金融债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_financialbondtobond` | 金融债市值占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_financialbondtonav` | 金融债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_financialbondtonavgrowth` | 金融债市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_foundleverage` | 基金杠杆率 | REPORTDATE | xla去前缀变体 |
| `prt_fundcotnachangeratio` | 所属基金公司资产净值合计变动率 |  | xla去前缀变体 |
| `prt_fundcototalnetassets` | 所属基金公司资产净值合计 |  | xla去前缀变体 |
| `prt_fundnoofsec` | 重仓证券持有基金数 | REPORTDATE | xla去前缀变体 |
| `prt_heavyweightreitsfundname` | 重仓REITs基金名称 | REPORTDATE、TopN | xla去前缀变体 |
| `prt_heavyweightreitsfundquantity` | 重仓REITs基金持仓数量 | REPORTDATE、TopN | xla去前缀变体 |
| `prt_heavyweightreitsfundtonav` | 重仓REITs基金市值占基金资产净值比 | REPORTDATE、TopN | xla去前缀变体 |
| `prt_heavyweightreitsfundvalue` | 重仓REITs基金持有市值 | REPORTDATE、TopN | xla去前缀变体 |
| `prt_hkstocktoasset` | 港股投资市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_hkstocktonav` | 港股投资市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_hkstockvalue` | 港股投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_industrytonavgrowth_citic` | 分行业市值占基金资产净值比增长(中信) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industrytonavgrowth_sw` | 分行业市值占基金资产净值比增长(申万) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industrytonavgrowth_sw2021` | 分行业市值占基金资产净值比增长(申万2021) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industrytonavgrowth_wind` | 分行业市值占基金资产净值比增长(Wind) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvalue_citic` | 分行业投资市值(中信) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvalue_sw` | 分行业投资市值(申万) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvalue_sw2021` | 分行业投资市值(申万2021) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvalue_wind` | 分行业投资市值(Wind) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluegrowth_citic` | 分行业市值增长率(中信) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluegrowth_sw` | 分行业市值增长率(申万) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluegrowth_sw2021` | 分行业市值增长率(申万2021) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluegrowth_wind` | 分行业市值增长率(Wind) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetonav_citic` | 分行业投资市值占基金资产净值比(中信) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetonav_sw` | 分行业投资市值占基金资产净值比(申万) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetonav_sw2021` | 分行业投资市值占基金资产净值比(申万2021) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetonav_wind` | 分行业投资市值占基金资产净值比(Wind) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetostockvalue_citic` | 分行业投资市值占股票投资市值比(中信) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetostockvalue_sw` | 分行业投资市值占股票投资市值比(申万) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetostockvalue_sw2021` | 分行业投资市值占股票投资市值比(申万2021) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_industryvaluetostockvalue_wind` | 分行业投资市值占股票投资市值比(Wind) | REPORTDATE、IndustryName | xla去前缀变体 |
| `prt_localgov` | 地方政府债市值 | REPORTDATE | xla去前缀变体 |
| `prt_localgovtoasset` | 地方政府债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_localgovtobond` | 地方政府债市值占债券投资净值比 | REPORTDATE | xla去前缀变体 |
| `prt_localgovtonav` | 地方政府债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_othervaluegrowth` | 其他资产市值增长率 |  | xla去前缀变体 |
| `prt_pcf_moddur` | PCF中债修正久期 | TRADEDATE | xla去前缀变体 |
| `prt_pfbtoasset` | 政策性金融债市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_pfbtobond` | 政策性金融债占债券投资市值比 | REPORTDATE | xla去前缀变体 |
| `prt_pfbtonav` | 政策性金融债市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_pfbvalue` | 政策性金融债市值 | REPORTDATE | xla去前缀变体 |
| `prt_qdii_countryregioninvestment` | 国家/地区投资市值(QDII) |  | xla去前缀变体 |
| `prt_qdii_countryregioninvestmenttonav` | 国家/地区投资市值占基金资产净值比例(QDII) |  | xla去前缀变体 |
| `prt_reverserepotonav` | 买入返售证券占基金资产净值比例 | REPORTDATE | xla去前缀变体 |
| `prt_seclendingvalue` | 转融通证券出借业务市值 | REPORTDATE | xla去前缀变体 |
| `prt_seclendingvaluetoasset` | 转融通证券出借业务市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_seclendingvaluetonav` | 转融通证券出借业务市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_sellstockincome` | 报告期卖出股票总收入(新增),f_prt_buystockcost | REPORTDATE | xla去前缀变体 |
| `prt_sharenum_stkhldgstyle` | 报告期不同持仓风格股票只数 | REPORTDATE、StyleType | xla去前缀变体 |
| `prt_sifutures` | 股指期货投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_stockholding` | 报告期末持有股票个数(中报、年报) | REPORTDATE | xla去前缀变体 |
| `prt_stockinvestmentactivity` | 股票投资活跃度(%) | REPORTDATE | xla去前缀变体 |
| `prt_stocktoasset` | 股票市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_stocktonav` | 股票市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_stocktonav_activeinvest` | 积极投资股票市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_stocktonav_passiveinvest` | 指数投资股票市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_stocktonavgrowth` | 股票市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_stockvalue` | 股票投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_stockvalue_activeinvest` | 积极投资股票市值 | REPORTDATE | xla去前缀变体 |
| `prt_stockvalue_holdingindustrymktvalue2` | 所属基金公司重仓行业市值 |  | xla去前缀变体 |
| `prt_stockvalue_industry2` | 分行业投资市值 |  | xla去前缀变体 |
| `prt_stockvalue_industrytoasset2` | 分行业市值占基金资产总值比 |  | xla去前缀变体 |
| `prt_stockvalue_industrytonav2` | 分行业市值占基金资产净值比 |  | xla去前缀变体 |
| `prt_stockvalue_industrytonavgrowth2` | 分行业市值占基金资产净值比增长 |  | xla去前缀变体 |
| `prt_stockvalue_industrytostock2` | 分行业市值占股票投资市值比 |  | xla去前缀变体 |
| `prt_stockvalue_industryvaluegrowth2` | 分行业市值增长率 |  | xla去前缀变体 |
| `prt_stockvalue_passiveinvest` | 指数投资股票市值 | REPORTDATE | xla去前缀变体 |
| `prt_totalasset` | 基金资产总值 | REPORTDATE | xla去前缀变体 |
| `prt_totalassetchange` | 基金资产总值变动 |  | xla去前缀变体 |
| `prt_totalassetchangeratio` | 基金资产总值变动率 |  | xla去前缀变体 |
| `prt_warranttoasset` | 权证市值占基金资产总值比 | REPORTDATE | xla去前缀变体 |
| `prt_warranttonav` | 权证市值占基金资产净值比 | REPORTDATE | xla去前缀变体 |
| `prt_warranttonavgrowth` | 权证市值占基金资产净值比例增长 |  | xla去前缀变体 |
| `prt_warrantvalue` | 权证投资市值 | REPORTDATE | xla去前缀变体 |
| `prt_warrantvaluegrowth` | 权证市值增长率 |  | xla去前缀变体 |
| `ps` | 市销率(PS) | DEALDATE、TYPE | xla去前缀变体 |
| `ps_lyr` | 市销率(PS, LYR) |  | xla去前缀变体 |
| `ps_ttm` | 市销率PS(TTM) |  | 探测法实测 |
| `ptmday` | 剩余存续期(新增) |  | xla去前缀变体 |
| `ptmtradeday` | 剩余存续期(交易日) | TRADEDATE | xla去前缀变体 |
| `ptmyear` | 剩余期限(年) |  | 探测法实测 |
| `punit` | 报价单位 |  | xla去前缀变体 |
| `putamount` | 认沽成交额 | TRADEDATE | xla去前缀变体 |
| `putcode` | 回售代码 |  | xla去前缀变体 |
| `putoi` | 认沽持仓量 | TRADEDATE | xla去前缀变体 |
| `putvolume` | 认沽成交量 | TRADEDATE | xla去前缀变体 |
| `pvt` | PVT量价趋势指标 |  | xla原码 |
| `pwmi` | 大盘同步指标 |  | xla原码 |
| `pzjtxornot` | 是否省级专精特新企业 | TRADEDATE | xla去前缀变体 |
| `qanal_accumulatednavreturn` | 季度累计基金份额净值增长率 |  | xla去前缀变体 |
| `qanal_avgnetincomeperunit` | 加权平均基金份额本期利润(新增) | REPORTDATE | xla去前缀变体 |
| `qanal_avgunitincome` | 加权平均基金份额本期净收益 | REPORTDATE | xla去前缀变体 |
| `qanal_benchdevreturn` | 季度超额收益率 |  | xla去前缀变体 |
| `qanal_benchreturn` | 季度业绩比较基准收益率 |  | xla去前缀变体 |
| `qanal_decutednetincome` | 本期利润扣减公允价值变动损益后的净额(新增) | REPORTDATE | xla去前缀变体 |
| `qanal_income` | 季度基金利润(新增) | REPORTDATE | xla去前缀变体 |
| `qanal_nav` | 季度末基金份额净值 | REPORTDATE | xla去前缀变体 |
| `qanal_navreturn` | 季度基金份额净值增长率 |  | xla去前缀变体 |
| `qanal_netasset` | 季度末基金资产净值 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_acr` | 单季度.平均合同租金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_actdist` | 单季度.实际分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_acu` | 单季度.平均产能利用率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_adjusteddecrease` | 单季度.调减项合计 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_adjustedincrease` | 单季度.调增项合计 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_adt` | 单季度.日均通行费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_advf` | 单季度.日均车流量 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ae` | 单季度.营业成本及费用-行政经费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ai` | 单季度.营业收入-综合管理服务收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ala` | 单季度.实际出租面积 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_amr` | 单季度.平均月租金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_aofa` | 单季度.调增减项-金融资产相关调整 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ast` | 单季度.污水平均处理量 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_bcat` | 单季度.调增减项-期初现金及交易所国债 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_bco` | 单季度.调增减项-期初现金余额 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_bcr` | 单季度.预算完成率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_btas` | 单季度.营业成本及费用-营业税金及附加 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cashflowbalance` | 单季度.经营活动现金流量余额 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cashrate` | 单季度.现金分派率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ce` | 单季度.营业成本及费用-资本性支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ceopp` | 单季度.调增减项-购买基础设施项目等资本性支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cop` | 单季度.调增减项-应付项目的变动 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cor` | 单季度.调增减项-应收项目的变动 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_corftp` | 单季度.调增减项-偿还借款本金支付的现金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_crap` | 单季度.调增减项-应收和应付项目的变动 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_crost` | 单季度.污水处理服务费回收率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cumactdist` | 单季度.实际分配金额(本年累计) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cumdistributedamounts` | 单季度.可供分配金额(本年累计) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_curra` | 单季度.流动比率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cwt` | 单季度.处理生活垃圾 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_cwti` | 单季度.营业收入-生活垃圾处置收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_daa` | 单季度.营业成本及费用-折旧及摊销 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_daorei` | 单季度.营业成本及费用-投资性房地产折旧及摊销 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_depreciationandamortization` | 单季度.折旧和摊销 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_distributedamounts` | 单季度.可供分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_doi` | 单季度.调增减项-存货的减少 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_domf` | 单季度.减免管理费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ebit` | 单季度税息折旧及摊销前利润 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ebitdap` | 单季度.息税折旧摊销前利润率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ebitdp` | 单季度.息税折旧前净利率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ebol` | 单季度.调增减项-期末负债余额 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ec` | 单季度.营业成本及费用-员工成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ela` | 单季度.期末出租面积 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_eor` | 单季度.期末出租率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_eta` | 单季度.期末租户家数 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_fc` | 单季度.营业成本及费用-财务费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_fissue` | 单季度.调增减项-基础设施基金发行份额募集的资金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_fl` | 单季度.全长 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_frrp` | 单季度.调增减项-未来合理相关支出预留 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_fs` | 单季度.建筑面积 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_gpm` | 单季度.毛利率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ic` | 单季度.营业成本及费用-利息支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_income` | 单季度.本期收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_interestcost` | 单季度.利息支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_kwt` | 单季度.处理厨余垃圾 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_la` | 单季度.可出租面积 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_lc` | 单季度.消耗LNG | REPORTDATE | xla去前缀变体 |
| `qanal_reits_lr` | 单季度.营业收入-渗滤液收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_lwti` | 单季度.营业收入-餐厨垃圾收运及处置 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_mbc` | 单季度.营业成本及费用-主营业务成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_mc` | 单季度.营业成本及费用-管理人报酬 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_me` | 单季度.营业成本及费用-维修维护费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_mf` | 单季度.营业成本及费用-管理费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_netprofit` | 单季度.本期净利润 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_npm` | 单季度.净利率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_npmincf` | 单季度.净利率(不扣除基金层面提取部分) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_oa` | 单季度.调增减项-其他调整项 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_oc` | 单季度.营业成本及费用-营运经费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_oeffrp` | 单季度.调增减项-未来合理期间内的运营费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_oge` | 单季度.上网电量 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_oi` | 单季度.营业收入-其他收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_omc` | 单季度.营业成本及费用-运营管理成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ooc` | 单季度.营业成本及费用-其他运营成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_operatingcost` | 单季度.营业成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_operatingrevenue` | 单季度.营业收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_or` | 单季度.出租率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ose` | 单季度.营业成本及费用-外包服务支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_otherc` | 单季度.营业成本及费用-其他成本/费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pc` | 单季度.营业成本及费用-物业成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pda` | 单季度.调增减项-前期可供分配金额 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pgi` | 单季度.营业收入-发电收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pi` | 单季度.营业收入-停车费收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pit` | 单季度.调增减项-支付的利息及所得税费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_plfc` | 单季度.调增减项-基础设施项目资产的公允价值变动损益 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pme` | 单季度.营业成本及费用-工程养护成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pol` | 单季度.调增减项-取得借款收到的本金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_pri` | 单季度.营业收入-物业收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_quira` | 单季度.速动比率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rc` | 单季度.调增减项-预留工程款 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rc2` | 单季度.营业成本-租赁成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rce` | 单季度.调增减项-预留资本性支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rcr` | 单季度.租金收缴率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rd` | 单季度.减免租金 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ri` | 单季度.营业收入-租金收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rm` | 单季度.营业成本及费用-原材料(燃气费) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_roe` | 单季度.调增减项-预留运营费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_roefny` | 单季度.调增减项-预留下一年度运营费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_rwi` | 单季度.营业收入-中水收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_sae` | 单季度.营业成本及费用-施救费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_seost` | 单季度.污水处理服务费 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_slti` | 单季度.营业收入-污泥收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_sme` | 单季度.营业成本及费用-系统维护成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_stc` | 单季度.营业成本及费用-污泥处理成本 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_sti` | 单季度.营业收入-污水处理收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_taxcost` | 单季度.所得税费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_ti` | 单季度.营业收入-通行费收入 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_tpce` | 单季度.调增减项-本期/本年资本性支出 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_tst` | 单季度.污水处理总量 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_uf` | 单季度.调增减项-不可预见费用 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_unitactdist` | 单季度.单位实际分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_unitcumactdist` | 单季度.单位实际分配金额(本年累计) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_unitcumdistributedamounts` | 单季度.单位可供分配金额(本年累计) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_unitdistributedamounts` | 单季度.单位可供分配金额(本期) | REPORTDATE | xla去前缀变体 |
| `qanal_reits_va` | 单季度.车辆总数 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_wqr` | 单季度.水质达标率 | REPORTDATE | xla去前缀变体 |
| `qanal_reits_wtc` | 单季度.营业成本及费用-污水处理成本 | REPORTDATE | xla去前缀变体 |
| `qanal_stdbenchdevreturn` | 季度超额收益率标准差 |  | xla去前缀变体 |
| `qanal_stdbenchreturn` | 季度业绩比较基准收益率标准差 |  | xla去前缀变体 |
| `qanal_stdnavreturn` | 季度基金份额净值增长率标准差 |  | xla去前缀变体 |
| `qanal_totalincome` | 单季度.基金利润(合计) | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_abstract` | 单季度.业绩预告摘要 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_changemax` | 单季度.预告净利润同比增长上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_changemin` | 单季度.预告净利润同比增长下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_date` | 单季度.业绩预告日期 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netprofitmax` | 单季度.预告净利润上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netprofitmin` | 单季度.预告净利润下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netsalesmax` | 单季度.预告净营收上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netsalesmin` | 单季度.预告净营收下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netsalesyoymax` | 单季度.预告净营收同比增长上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_netsalesyoymin` | 单季度.预告净营收同比增长下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_salesmax` | 单季度.预告总营收上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_salesmin` | 单季度.预告总营收下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_salesyoymax` | 单季度.预告总营收同比增长上限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_salesyoymin` | 单季度.预告总营收同比增长下限 | REPORTDATE | xla去前缀变体 |
| `qprofitnotice_style` | 单季度.业绩预告类型 | REPORTDATE | xla去前缀变体 |
| `qstm07_cs_cashpaidclaim` | 单季度.支付签发保险合同赔款的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_cs_cashrecprem` | 单季度.收到签发保险合同保费取得的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_cs_ntcashpaidcrc` | 单季度.支付分出再保险合同的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_cs_ntcashrecced` | 单季度.收到分入再保险合同的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_cs_ntincloanpled` | 单季度.保单质押贷款净增加额 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_amortinssvcco` | 单季度.摊回保险服务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_apportcedprem` | 单季度.分出保费的分摊 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_cedreinsfingl` | 单季度.分出再保险财务损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_inssvccosts` | 单季度.保险服务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_inssvcincome` | 单季度.保险服务收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstm07_is_uwfinloss` | 单季度.承保财务损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `qstmnote_insur_212505` | 核心偿付能力溢额 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212506` | 核心偿付能力充足率 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212507` | 综合偿付能力溢额 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212508` | 综合偿付能力充足率 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212509` | 保险业务收入 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212512` | 认可资产 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212513` | 认可负债 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212514` | 实际资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212515` | 核心一级资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212516` | 核心二级资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212517` | 附属一级资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212518` | 附属二级资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212519` | 最低资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212520` | 量化风险最低资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212521` | 寿险业务保险风险最低资本合计 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212522` | 非寿险业务保险风险最低资本合计 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212523` | 市场风险最低资本合计 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212524` | 信用风险最低资本合计 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212525` | 风险分散效应的资本要求增加 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212526` | 风险聚合效应的资本要求减少 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212527` | 控制风险最低资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212528` | 附加资本 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212529` | 最近一次风险综合评级类别 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212530` | 净现金流 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212531` | 净现金流:报告日后第1年 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212532` | 净现金流:报告日后第2年 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212533` | 净现金流:报告日后第3年 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212534` | 综合流动比率:3个月内 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212535` | 综合流动比率:1年内 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212536` | 综合流动比率:1年以上 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212537` | 综合流动比率:1-3年内 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212538` | 综合流动比率:3-5年内 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212539` | 综合流动比率:5年以上 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212540` | 流动性覆盖率:基本情景 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212541` | 流动性覆盖率:公司整体:压力情景1 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212542` | 流动性覆盖率:公司整体:压力情景2 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212543` | 流动性覆盖率:独立账户:压力情景1 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212544` | 流动性覆盖率:独立账户:压力情景2 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212546` | 保险风险最低资本合计 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212547` | 净现金流:报告日后第1年:未来1季度 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212548` | 净现金流:报告日后第1年:未来2季度 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212549` | 净现金流:报告日后第1年:未来3季度 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212550` | 净现金流:报告日后第1年:未来4季度 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212570` | 流动性覆盖率:公司整体:基本情景:未来3个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212571` | 流动性覆盖率:公司整体:基本情景:未来12个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212572` | 流动性覆盖率:公司整体:必测压力情景:未来3个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212573` | 流动性覆盖率:公司整体:必测压力情景:未来12个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212574` | 流动性覆盖率:不考虑资产变现:必测压力情景:未来3个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212575` | 流动性覆盖率:不考虑资产变现:必测压力情景:未来12个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212576` | 流动性覆盖率:公司整体:自测压力情景:未来3个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212577` | 流动性覆盖率:公司整体:自测压力情景:未来12个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212578` | 流动性覆盖率:不考虑资产变现:自测压力情景:未来3个月 | REPORTDATE | xla去前缀变体 |
| `qstmnote_insur_212579` | 流动性覆盖率:不考虑资产变现:自测压力情景:未来12个月 | REPORTDATE | xla去前缀变体 |
| `qtvolm` | 报价报价总笔数 |  | xla去前缀变体 |
| `quick` | 速动比率 |  | 探测法实测 |
| `r2` | 可决系数(新增) | TD1、TD2 | xla去前缀变体 |
| `ra_coposiware` | 虚实盘比(合约) | TRADEDATE | xla去前缀变体 |
| `ra_vaposiware` | 虚实盘比(品种) | TRADEDATE | xla去前缀变体 |
| `ratebond2` | 债券国际评级 | TRADEDATE | xla去前缀变体 |
| `rateofstdbndcsi` | 报价式回购折算率(中证指数) | TRADEDATE | xla去前缀变体 |
| `rating_3y` | 基金3年评级 | ORG、Y、M | xla去前缀变体 |
| `rating_5y` | 基金5年评级 | ORG、Y、M | xla去前缀变体 |
| `rating_avg` | 综合评级 |  | 探测法实测 |
| `rating_avgchn` | 综合评级(中文)(新增) | TD | xla去前缀变体 |
| `rating_avgeng` | 综合评级(英文)(新增) | TD | xla去前缀变体 |
| `rating_diag` | Wind基金诊断综合得分 | RatingPeriod、Year、Month | xla去前缀变体 |
| `rating_downgrade` | 一月内评级调低家数 |  | xla去前缀变体 |
| `rating_haitong3y` | 海通3年评级 | D、M | xla去前缀变体 |
| `rating_instnum` | 评级机构数 |  | 探测法实测 |
| `rating_latestmonth` | 最新评级月份 | RATINGAGENCY、RatingInterval | xla去前缀变体 |
| `rating_maintain` | 一月内评级维持家数 |  | xla去前缀变体 |
| `rating_marketavg` | 市场综合3年评级 |  | xla去前缀变体 |
| `rating_numofbearish` | 期货品种看空研报数量 | TRADEDATE | xla去前缀变体 |
| `rating_numofbullish` | 期货品种看多研报数量 | TRADEDATE | xla去前缀变体 |
| `rating_numofbuy` | 评级买入家数 |  | xla去前缀变体 |
| `rating_numofhold` | 评级中性家数 |  | xla去前缀变体 |
| `rating_numofneutral` | 期货品种中性研报数量 | TRADEDATE | xla去前缀变体 |
| `rating_numofoutperform` | 评级增持家数 |  | xla去前缀变体 |
| `rating_numofsell` | 评级卖出家数 |  | xla去前缀变体 |
| `rating_numofunderperform` | 评级减持家数 |  | xla去前缀变体 |
| `rating_shanghaioverall3y` | 上海证券3年评级（综合评级） | D、M | xla去前缀变体 |
| `rating_shanghaioverall5y` | 上海证券5年评级（综合评级） | D、M | xla去前缀变体 |
| `rating_shanghaisharpe3y` | 上海证券3年评级（夏普比率） | D、M | xla去前缀变体 |
| `rating_shanghaisharpe5y` | 上海证券5年评级（夏普比率） | D、M | xla去前缀变体 |
| `rating_shanghaistocking3y` | 上海证券3年评级（选证能力） | D、M | xla去前缀变体 |
| `rating_shanghaistocking5y` | 上海证券5年评级（选证能力） | D、M | xla去前缀变体 |
| `rating_shanghaitiming3y` | 上海证券3年评级（择时能力） | D、M | xla去前缀变体 |
| `rating_shanghaitiming5y` | 上海证券5年评级（择时能力） | D、M | xla去前缀变体 |
| `rating_upgrade` | 一月内评级调高家数 |  | xla去前缀变体 |
| `rating_wind1y` | Wind1年评级(新增) | D、M | xla去前缀变体 |
| `rating_wind2y` | Wind2年评级(新增) | D、M | xla去前缀变体 |
| `rating_wind3y` | Wind3年评级(新增) | D、M | xla去前缀变体 |
| `rating_wind5y` | Wind5年评级 | D、M | xla去前缀变体 |
| `rating_windavg` | Wind综合评级(新增) | D、M | xla去前缀变体 |
| `rating_yinhe1y` | 银河1年评级(新增) | D、M | xla去前缀变体 |
| `rating_yinhe2y` | 银河2年评级(新增) | D、M | xla去前缀变体 |
| `rating_zhaoshang3y` | 招商3年评级 | D、M | xla去前缀变体 |
| `ratingoutlooks` | 发行人最新评级展望 |  | xla去前缀变体 |
| `rc` | RC变化率指数 |  | xla去前缀变体 |
| `rcytm` | 票面调整收益率 |  | xla去前缀变体 |
| `rde_ttm` | 研发费用(TTM) | REPORTDATE | xla去前缀变体 |
| `redemption_price` | 提前兑付净价 | DEALDATE | xla去前缀变体 |
| `redemption_price_type` | 提前兑付净价类型 | DEALDATE | xla去前缀变体 |
| `redemptiondate` | 含权债赎回日期(新增) |  | xla去前缀变体 |
| `redemptionprice` | 含权债赎回价格(新增) |  | xla去前缀变体 |
| `redemptionrisk` | 赎回风险提示 |  | xla去前缀变体 |
| `reenddate` | 转售截止日 |  | xla去前缀变体 |
| `referencelevel_cbr` | 成交参考度(中债资信) | TRADEDATE | xla去前缀变体 |
| `refrmkd_preplandate` | 董事会预案公告日(新增) |  | xla去前缀变体 |
| `regcapitalcur` | 注册资本币种 |  | xla去前缀变体 |
| `registernumber` | 工商登记号(新增) |  | xla去前缀变体 |
| `registrationdate` | 债权债务登记日 |  | xla去前缀变体 |
| `reits_cbval` | 中债REITs估值 | TRADEDATE | xla去前缀变体 |
| `reits_cbvalyield` | 中债REITs估值收益率 | TRADEDATE | xla去前缀变体 |
| `reits_cmfee` | 客户维护费 | REPORTDATE | xla去前缀变体 |
| `reits_csabsvaluation` | 中证REITs-ABS估值 | TRADEDATE | xla去前缀变体 |
| `reits_csabsvaluationyield` | 中证REITs-ABS估值收益率 | TRADEDATE | xla去前缀变体 |
| `reits_csvaluation` | 中证REITs估值 | TRADEDATE | xla去前缀变体 |
| `reits_cumexpshare` | 累计扩募发售份额 | TRADEDATE | xla去前缀变体 |
| `reits_cumexpvalue` | 累计扩募发售金额 | TRADEDATE | xla去前缀变体 |
| `reits_distributableprofityield` | 派息率TTM | TRADEDATE | xla去前缀变体 |
| `reits_distributionratio` | 年化派息率 | TRADEDATE | xla去前缀变体 |
| `reits_dividendyield` | 股息率TTM | TRADEDATE | xla去前缀变体 |
| `reits_fixmanagfee` | 固定管理费 | REPORTDATE | xla去前缀变体 |
| `reits_flomanagfee` | 浮动管理费 | REPORTDATE | xla去前缀变体 |
| `reits_unitdistributableamount` | 近一年单位可供分配金额 | TRADEDATE | xla去前缀变体 |
| `rel_ipo_chg` | 上市后涨跌幅 |  | 探测法实测 |
| `relatedbond` | 公司发行债券一览 |  | xla去前缀变体 |
| `relatedcb_yearlyamount` | 年度可转债发行量 |  | xla去前缀变体 |
| `relationcode` | 跨市场代码 |  | xla去前缀变体 |
| `relpctchange` | 月相对大盘涨跌幅(新增) |  | xla去前缀变体 |
| `repaymentmethod` | 偿还方式 |  | xla去前缀变体 |
| `repurchasebegindate` | 回售登记起始日 |  | xla去前缀变体 |
| `repurchasedate` | 含权债回售日期(新增) |  | xla去前缀变体 |
| `repurchaseenddate` | 回售登记截止日 |  | xla去前缀变体 |
| `repurchaseprice` | 含权债回售价格(新增) |  | xla去前缀变体 |
| `resaleamount` | 最新回售金额 |  | xla去前缀变体 |
| `researchanddevelopmentexpenses` | 研发费用(新增) | REPORTDATE | xla去前缀变体 |
| `restartdate` | 转售开始日 |  | xla去前缀变体 |
| `retainedearnings` | 留存收益 | REPORTDATE | xla去前缀变体 |
| `retainedearningstoassets` | 留存收益／总资产 | REPORTDATE | xla去前缀变体 |
| `retainedps` | 每股留存收益 | REPORTDATE | xla去前缀变体 |
| `return` | 区间回报 |  | xla去前缀变体 |
| `return_10y` | 近10年回报 |  | xla去前缀变体 |
| `return_1m` | 近1月回报 |  | xla去前缀变体 |
| `return_1w` | 近1周回报 |  | xla去前缀变体 |
| `return_1y` | 近1年回报 |  | xla去前缀变体 |
| `return_20y` | 近20年回报 | Annualize、TRADEDATE | xla去前缀变体 |
| `return_2w` | 近2周回报 | Annualize、TRADEDATE | xla去前缀变体 |
| `return_2y` | 近2年回报 |  | xla去前缀变体 |
| `return_30y` | 近30年回报 | Annualize、TRADEDATE | xla去前缀变体 |
| `return_3m` | 近3月回报 |  | xla去前缀变体 |
| `return_3y` | 近3年回报 |  | xla去前缀变体 |
| `return_5y` | 近5年回报 |  | xla去前缀变体 |
| `return_6m` | 近6月回报 |  | xla去前缀变体 |
| `return_m` | 单月度回报 | TRADEDATE | xla去前缀变体 |
| `return_q` | 单季度回报 | TRADEDATE | xla去前缀变体 |
| `return_std` | 成立以来回报 |  | xla去前缀变体 |
| `return_y` | 单年度回报 | TRADEDATE | xla去前缀变体 |
| `return_ytd` | 今年以来回报 |  | xla去前缀变体 |
| `returntype` | 收益处理方式 |  | xla去前缀变体 |
| `revenuetoassets` | 营业收入／总资产 | REPORTDATE | xla去前缀变体 |
| `rho_exch` | Rho(交易所) | TRADEDATE | xla去前缀变体 |
| `rightsissue_actlnumtoemp` | 职工股实际配股数(新增) |  | xla去前缀变体 |
| `rightsissue_actlnumtojur` | 法人股实际配股数(新增) |  | xla去前缀变体 |
| `rightsissue_actlnumtostate` | 国有股实际配股数(新增) |  | xla去前缀变体 |
| `rightsissue_actlnumtotrd` | 已流通股实际配股数(新增) |  | xla去前缀变体 |
| `rightsissue_actlnumtotrsf` | 转配股实际配股数(新增) |  | xla去前缀变体 |
| `rightsissue_amount` | 实际配股数 | RPTYEAR | xla去前缀变体 |
| `rightsissue_anncedate` | 配股公告日(新增) |  | xla去前缀变体 |
| `rightsissue_approveddate` | 配股获准公告日(新增) |  | xla去前缀变体 |
| `rightsissue_baseshare` | 基准股本 | RPTYEAR | xla去前缀变体 |
| `rightsissue_collection` | 配股募集资金 | RPTYEAR | xla去前缀变体 |
| `rightsissue_collection_t` | 区间配股募集资金合计 | StartDate、DATE | xla去前缀变体 |
| `rightsissue_deputyundr` | 配股分销商(新增) |  | xla去前缀变体 |
| `rightsissue_exdividenddate` | 配股除权日 | RPTYEAR | xla去前缀变体 |
| `rightsissue_expense` | 配股费用 | RPTYEAR | xla去前缀变体 |
| `rightsissue_leadundr` | 配股主承销商(新增) |  | xla去前缀变体 |
| `rightsissue_listeddate` | 配股上市日 | RPTYEAR | xla去前缀变体 |
| `rightsissue_maxpricepreplan` | 配股预案价上限(新增) |  | xla去前缀变体 |
| `rightsissue_minpricepreplan` | 配股预案价下限(新增) |  | xla去前缀变体 |
| `rightsissue_netcollection` | 配股实际募集资金 | RPTYEAR | xla去前缀变体 |
| `rightsissue_payenddate` | 缴款终止日(新增) |  | xla去前缀变体 |
| `rightsissue_paystartdate` | 缴款起始日(新增) |  | xla去前缀变体 |
| `rightsissue_pershare` | 每股配股数 | RPTYEAR | xla去前缀变体 |
| `rightsissue_planamt` | 计划配股数(新增) |  | xla去前缀变体 |
| `rightsissue_preplandate` | 预案公告日(新增) |  | xla去前缀变体 |
| `rightsissue_price` | 配股价格 | RPTYEAR | xla去前缀变体 |
| `rightsissue_progress` | 配股进度(新增) |  | xla去前缀变体 |
| `rightsissue_recdateshareb` | B股股权登记日(新增) |  | xla去前缀变体 |
| `rightsissue_regdateshareb` | 股权登记日(B股最后交易日)(新增) |  | xla去前缀变体 |
| `rightsissue_registdate` | 配股提交注册日 | Year | xla去前缀变体 |
| `rightsissue_smtganncedate` | 股东大会公告日(新增) |  | xla去前缀变体 |
| `rightsissue_subbydistr` | 承销商认购余股(新增) |  | xla去前缀变体 |
| `rightsissue_sucregistdate` | 配股注册成功日 | Year | xla去前缀变体 |
| `rightsissue_theornumtoemp` | 职工股理论配股数(新增) |  | xla去前缀变体 |
| `rightsissue_theornumtojur` | 法人股理论配股数(新增) |  | xla去前缀变体 |
| `rightsissue_theornumtostate` | 国有股理论配股数(新增) |  | xla去前缀变体 |
| `rightsissue_theornumtotrd` | 已流通股理论配股数(新增) |  | xla去前缀变体 |
| `rightsissue_theornumtotrsf` | 转配股理论配股数(新增) |  | xla去前缀变体 |
| `rightsissue_type` | 配股方式(新增) |  | xla去前缀变体 |
| `rightsissue_undrtype` | 配股承销方式(新增) |  | xla去前缀变体 |
| `rightsissue_up5pctactlnum` | 持股5%以上大股东认购股数(新增) |  | xla去前缀变体 |
| `rightsissue_up5pctnum` | 持股5%以上大股东持股数(新增) |  | xla去前缀变体 |
| `rightsissue_up5pcttheornum` | 持股5%以上的大股东理论认购股数(新增) |  | xla去前缀变体 |
| `riskadmonition_date` | 戴帽摘帽时间(新增) |  | xla去前缀变体 |
| `riskstate` | 风险状态 |  | xla去前缀变体 |
| `riskwarning` | 是否属于风险警示板 | TRADEDATE | xla去前缀变体 |
| `riskwarningpre` | 可能被实施退市风险警示 | TRADEDATE | xla去前缀变体 |
| `ro` | 每份DR代表股数 |  | xla去前缀变体 |
| `roa` | 总资产报酬率ROA |  | 探测法实测 |
| `roa2` | 总资产净利率ROA2 |  | 探测法实测 |
| `roa2_ttm` | 总资产报酬率ROA(TTM) |  | xla去前缀变体 |
| `roa2_ttm2` | 总资产报酬率(TTM) | REPORTDATE | xla去前缀变体 |
| `roa2_yearly` | 年化总资产报酬率 | REPORTDATE | xla去前缀变体 |
| `roa_ttm` | 总资产净利率ROA(TTM) |  | xla去前缀变体 |
| `roa_ttm2` | ROA(TTM) |  | 探测法实测 |
| `roa_yearly` | 年化总资产净利率 | REPORTDATE | xla去前缀变体 |
| `roc` | ROC变动速率 |  | xla原码 |
| `roe` | 净资产收益率ROE |  | 探测法实测 |
| `roe_avg` | 净资产收益率ROE-增发条件 | REPORTDATE | xla去前缀变体 |
| `roe_basic` | 净资产收益率ROE(加权) | REPORTDATE | xla去前缀变体 |
| `roe_deducted` | 净资产收益率ROE-扣除非经常损益 | REPORTDATE | xla去前缀变体 |
| `roe_diluted` | ROE(摊薄) |  | 探测法实测 |
| `roe_exbasic` | 净资产收益率ROE(扣除／加权) | REPORTDATE | xla去前缀变体 |
| `roe_exdiluted` | 净资产收益率ROE(扣除／摊薄) | REPORTDATE | xla去前缀变体 |
| `roe_ttm` | 净资产收益率ROE(TTM) |  | xla去前缀变体 |
| `roe_ttm2` | ROE(TTM) |  | 探测法实测 |
| `roe_yearly` | 净资产收益率(ROE,Yearly) | REPORTDATE | xla去前缀变体 |
| `roic` | 投入资本回报率ROIC |  | 探测法实测 |
| `roic2_ttm` | 投入资本回报率ROIC(TTM) | REPORTDATE | xla去前缀变体 |
| `roic_ttm` | 投入资本回报率(TTM) | REPORTDATE | xla去前缀变体 |
| `roic_ttm2` | 投入资本回报率(TTM) | REPORTDATE | xla去前缀变体 |
| `rollsample` | 滚动序列样本券 | TRADEDATE | xla去前缀变体 |
| `rop` | 人力投入回报率（ROP) | REPORTDATE | xla去前缀变体 |
| `rps` | 相对强度指标 | TRADEDATE | xla去前缀变体 |
| `rsi` | RSI相对强弱指标 |  | xla原码 |
| `salescashin_ttm` | 销售商品提供劳务收到的现金(TTM) |  | xla去前缀变体 |
| `salescashin_ttm2` | 销售商品提供劳务收到的现金(TTM) | REPORTDATE | xla去前缀变体 |
| `salescashintoor` | 销售商品提供劳务收到的现金／营业收入 | REPORTDATE | xla去前缀变体 |
| `salescashintoor_ttm` | 销售商品提供劳务收到的现金／营业收入(TTM) |  | xla去前缀变体 |
| `salescashintoor_ttm2` | 销售商品提供劳务收到的现金/营业收入(TTM) | REPORTDATE | xla去前缀变体 |
| `sametermbond` | 同期债 |  | xla去前缀变体 |
| `sar` | SAR抛物转向 |  | xla原码 |
| `scalestyle` | 所属规模风格类型 | TRADEDATE | xla去前缀变体 |
| `sccode` | 标准合约代码 |  | xla去前缀变体 |
| `scitechbondornot` | 是否科创债 |  | xla去前缀变体 |
| `sconvexity_ifexe` | 行权利差凸性 | TRADEDATE | xla去前缀变体 |
| `sddate` | 开始交割日(支持历史) | TRADEDATE | xla去前缀变体 |
| `sduration` | 利差久期(新增) | TD | xla去前缀变体 |
| `sduration_ifexe` | 行权利差久期 | TRADEDATE | xla去前缀变体 |
| `sechighbondrate` | 债券次高信用评级 | DEALDATE | xla去前缀变体 |
| `sechighrating` | 发行人次高信用评级 | DEALDATE | xla去前缀变体 |
| `secondarycapital` | 是否二级资本债 |  | xla去前缀变体 |
| `sei` | 所属战略性新兴产业分类 | TRADEDATE、TYPE | xla去前缀变体 |
| `settle` | 结算价_期货历史同月 | DATE | xla去前缀变体 |
| `settlementmethod` | 结算方式 |  | xla去前缀变体 |
| `sharpe` | Sharpe(新增) | TD1、TD2 | xla去前缀变体 |
| `shclearl1type` | 上清所债券分类 |  | xla去前缀变体 |
| `short_margin` | 期货空头保证金(支持历史) | TRADEDATE | xla去前缀变体 |
| `shsc` | 是否沪港通买入标的 | TRADEDATE | xla去前缀变体 |
| `shsc2` | 是否深港通买入标的 | TRADEDATE | xla去前缀变体 |
| `si` | SI摆动指标 |  | xla原码 |
| `singleissuer` | 单一债务主体中文名称 |  | xla去前缀变体 |
| `slowkd` | SLOWKD慢速KD |  | xla原码 |
| `sobv` | SOBV能量潮 |  | xla原码 |
| `spacornot` | 是否SPAC上市 |  | xla去前缀变体 |
| `spedatguabal` | 指定日期担保余额 | Year、P1、Grarantee | xla去前缀变体 |
| `sponsrepresent` | 保荐代表人 |  | xla去前缀变体 |
| `sppboacfprcf` | 专项债投向领域一级分类 |  | xla去前缀变体 |
| `sppboacfsccf` | 专项债投向领域二级分类 |  | xla去前缀变体 |
| `sprcnxt_cnbd` | 加权平均结算价利差凸性 | TRADEDATE | xla原码 |
| `sprdinc_redm` | 股票投资收益-赎回差价收入 | REPORTDATE | xla去前缀变体 |
| `sprdinc_seclend` | 股票投资收益-证券出借差价收入 | REPORTDATE | xla去前缀变体 |
| `sprdinc_sub` | 股票投资收益-申购差价收入 | REPORTDATE | xla去前缀变体 |
| `sprdinc_trd` | 股票投资收益-买卖股票差价收入 | REPORTDATE | xla去前缀变体 |
| `sprdura_cnbd` | 加权平均结算价利差久期 | TRADEDATE | xla原码 |
| `spread` | 期现价差 | TRADEDATE | xla去前缀变体 |
| `spread2` | 行权后利差 |  | xla去前缀变体 |
| `spreadyield_cnbd` | 点差收益率 | TRADEDATE | xla原码 |
| `srmi` | SRMI MI修正指标 |  | xla原码 |
| `ssbpco` | 单季度.主营构成(按产品)-项目成本 | REPORTDATE、TopN | xla去前缀变体 |
| `ssbpgp` | 单季度.主营构成(按产品)-项目毛利 | REPORTDATE、TopN | xla去前缀变体 |
| `ssbrre` | 单季度.主营构成(按地区)-项目收入 | REPORTDATE、TopN | xla去前缀变体 |
| `st_efforecast` | 有效预报 | TRADEDATE | xla去前缀变体 |
| `st_stock` | 注册仓单数量 |  | xla去前缀变体 |
| `staff_sub_ratio` | 管理人员工认购比例 |  | xla去前缀变体 |
| `staff_sub_shares` | 管理人员工认购份额 |  | xla去前缀变体 |
| `startdate` | 存续起始日期 |  | xla去前缀变体 |
| `startdateoffer` | 要约起始日期 | DEALDATE | xla去前缀变体 |
| `std` | STD标准差 |  | xla原码 |
| `stdcof` | 标准差系数 |  | xla去前缀变体 |
| `stdebtratio` | 现金短债比 | REPORTDATE | xla去前缀变体 |
| `stkinv_spread` | 股票投资收益-买卖股票差价收入 | REPORTDATE | xla去前缀变体 |
| `stkinv_stkamount` | 股票投资收益-卖出股票成交总额 | REPORTDATE | xla去前缀变体 |
| `stkinv_stkcost` | 股票投资收益-卖出股票成本总额 | REPORTDATE | xla去前缀变体 |
| `stkinv_transcost` | 股票投资收益-交易费用 | REPORTDATE | xla去前缀变体 |
| `stm07_bs_crcassets` | 分出再保险合同资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_crcliab` | 分出再保险合同负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_allassets` | 资产总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_alldebt` | 负债合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_allequity` | 所有者权益合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_capitalreserve` | 资本公积金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_cash` | 货币资金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_debtequity` | 负债和所有者权益总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_equity` | 归属于母公司所有者权益合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_liquidasset` | 流动资产合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_liquiddebt` | 流动负债合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_nonliquid` | 非流动资产合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_notes` | 应收票据及应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_otherpayable` | 其他应付款(合计) | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_others` | 其他应收款(合计) | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_paidin` | 实收资本(或股本) | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_payable` | 应付票据及应付账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_realestate` | 投资性房地产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_recipts` | 预收款项 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_surplus` | 盈余公积金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_tax` | 应交税费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_bs_reits_undistrirprofit` | 未分配利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_cashpaidclaim` | 支付签发保险合同赔款的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_cashrecprem` | 收到签发保险合同保费取得的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_ntcashpaidcrc` | 支付分出再保险合同的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_ntcashrecced` | 收到分入再保险合同的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_ntincloanpled` | 保单质押贷款净增加额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_buycash` | 购买商品、接受劳务支付的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_cashadd` | 现金及现金等价物净增加额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_financecashin` | 筹资活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_financecashout` | 筹资活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_financenetcash` | 筹资活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_investcashin` | 投资活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_investcashout` | 投资活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_investnetcash` | 投资活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_opercashin` | 经营活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_opercashout` | 经营活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_opernetcash` | 经营活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_paidcash` | 支付其他与经营活动有关的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_salescash` | 销售商品、提供劳务收到的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_cs_reits_tax` | 支付的各项税费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_amortinssvcco` | 摊回保险服务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_apportcedprem` | 分出保费的分摊 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_cedreinsfingl` | 分出再保险财务损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_inssvccosts` | 保险服务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_inssvcincome` | 保险服务收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_cost` | 营业成本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_financefee` | 财务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_generalprofit` | 综合收益总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_income` | 营业收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_managefee` | 管理费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_netprofit` | 净利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_profit` | 营业利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_rdfee` | 研发费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_salesfee` | 销售费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_scost` | 营业总成本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_sincome` | 营业总收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_sumprofit` | 利润总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_reits_tax` | 税金及附加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm07_is_uwfinloss` | 承保财务损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_10` | 交易性金融资产 | REPORTDATE | xla去前缀变体 |
| `stm_bs_12` | 应收账款净额 | REPORTDATE | xla去前缀变体 |
| `stm_bs_17` | 存货 | REPORTDATE | xla去前缀变体 |
| `stm_bs_29` | 权益性投资 | REPORTDATE | xla去前缀变体 |
| `stm_bs_74` | 总资产 | REPORTDATE | xla去前缀变体 |
| `stm_bs_goldcontractinterest` | 应收黄金合约拆借孳息 | REPORTDATE | xla去前缀变体 |
| `stm_bs_reits_accountspayable` | 应付账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_accountsreceivable` | 应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_capitalreserves` | 资本公积 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_contractliabilities` | 合同负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_custodianfeepayable` | 应付托管费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_deferredincometaxassets` | 递延所得税资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_deferredincometaxliabilities` | 递延所得税负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_employeepaypayable` | 应付职工薪酬 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_goodwill` | 商誉 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_intangibleassets` | 无形资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_interest_receivable` | 应收利息 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_interestincome` | 利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_inventories` | 存货 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_investmentprofit` | 投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_investmentrealestate` | 投资性房地产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_liabilities_andownerequity` | 负债和所有者权益总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_longterm_equityinvestment` | 长期股权投资 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_longterm_loans` | 长期借款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_longtermdeferredexpenses` | 长期待摊费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_managementfeepayable` | 应付管理人报酬 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_moneyfunds` | 货币资金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_operatingrevenue` | 营业收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_otherassets` | 其他资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_otherliabilities` | 其他负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_paidincapital` | 实收基金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_settlementreserve` | 结算备付金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_taxpayable` | 应交税费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_totalassets` | 资产总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_totalliabilities` | 负债合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_totaloperatingrevenue` | 营业总收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_totalownersequity` | 所有者权益合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_tradablefinancialassets` | 交易性金融资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_reits_undistributedprofit` | 未分配利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_bs_repoin_exchmkt` | 买入返售金融资产(交易所市场) | REPORTDATE | xla去前缀变体 |
| `stm_bs_repoin_interbmkt` | 买入返售金融资产(银行间市场) | REPORTDATE | xla去前缀变体 |
| `stm_cs_reits_beginningcashequivalents` | 期初现金及现金等价物余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashfromborrowing` | 取得借款收到的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashfrominterest` | 取得利息收入收到的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashfromsr` | 销售商品、提供劳务收到的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashpaiddistribution` | 分配支付的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashpaidinterestpayment` | 偿付利息支付的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashpaidpgs` | 购买商品、接受劳务支付的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cashreceivedfromop` | 收到其他与经营活动有关的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cshpdrpbrw` | 偿还借款支付的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_cshrvdsubcon` | 认购/申购收到的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_endingcashequivalents` | 期末现金及现金等价物余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_netcashfrominvest` | 投资活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_netcashsbu` | 取得子公司及其他营业单位支付的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_netcffinancing` | 筹资活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_netcffromop` | 经营活动产生的现金流量净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_netincreasecashequivalents` | 现金及现金等价物净增加额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_ntcshpdacsinv` | 取得证券投资支付的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_ntcshrvddsinv` | 处置证券投资收到的现金净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_ntdecfinarsl` | 买入返售金融资产净减少额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_ntincfinarsl` | 买入返售金融资产净增加额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_othercashia` | 支付其他与投资活动有关的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_othercashoa` | 支付其他与经营活动有关的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_otherpaidcashtofa` | 支付其他与筹资活动有关的现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_subtotalcifromop` | 经营活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_subtotalcofromop` | 经营活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_taxchargespaid` | 支付的各项税费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_totalcff` | 筹资活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_totalcffinancing` | 筹资活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_totalcfia` | 投资活动现金流出小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_cs_reits_totalcifrominvest` | 投资活动现金流入小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_10` | 营业成本 | REPORTDATE | xla去前缀变体 |
| `stm_is_101` | 净投资业绩 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_102` | 承保财务损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_103` | 分出再保险财务损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_18` | 信息披露费 | REPORTDATE | xla去前缀变体 |
| `stm_is_19` | 审计费用 | REPORTDATE | xla去前缀变体 |
| `stm_is_26` | 税金及附加 | REPORTDATE | xla去前缀变体 |
| `stm_is_75` | 基金投资收益 | REPORTDATE | xla去前缀变体 |
| `stm_is_76` | 其他利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_77` | 汇兑收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_78` | 所得税费用 | REPORTDATE | xla去前缀变体 |
| `stm_is_79` | 净利润 | REPORTDATE | xla去前缀变体 |
| `stm_is_79_total` | 净利润(合计) | REPORTDATE | xla去前缀变体 |
| `stm_is_83` | 总营业收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_9` | 主营收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_dd` | 存款利息收入-活期存款利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_iid` | 存款利息收入-合计 | REPORTDATE | xla去前缀变体 |
| `stm_is_iiod` | 存款利息收入-其他 | REPORTDATE | xla去前缀变体 |
| `stm_is_od` | 存款利息收入-其他存款利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_reits_administrativecosts` | 管理费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_assetimpair` | 资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_credit_impairmentloss` | 信用减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_custodyfee` | 托管费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_financialcosts` | 财务费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_incometaxexpenses` | 所得税费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_interestcost` | 利息支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_managementfee` | 管理人报酬 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_netprofit` | 净利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_netprofit_fromgoingconcern` | 持续经营净利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_nonoperatingexpenses` | 营业外支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_nonoperatingrevenue` | 营业外收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_operatingcost` | 营业成本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_operatingprofit` | 营业利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_otherexpenses` | 其他费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_taxandsurcharges` | 税金及附加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_totalcomprehensiveincome` | 综合收益总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_totaloperatingcost` | 营业总成本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_reits_totalprofit` | 利润总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stm_is_securityborrowincome` | 证券出借利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_sr` | 存款利息收入-结算备付金利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_is_td` | 存款利息收入-定期存款利息收入 | REPORTDATE | xla去前缀变体 |
| `stm_issuingdate` | 定期报告披露日期 | REPORTDATE | xla去前缀变体 |
| `stm_issuingdate_fs` | 定期报告正报披露日期 | REPORTDATE | xla去前缀变体 |
| `stm_navchange_1` | 期初所有者权益(基金净值) | REPORTDATE | xla去前缀变体 |
| `stm_navchange_11` | 期末所有者权益(基金净值) | REPORTDATE | xla去前缀变体 |
| `stm_navchange_7_paidincapital` | 基金申购款(实收基金) | REPORTDATE | xla去前缀变体 |
| `stm_navchange_8_paidincapital` | 基金赎回款(实收基金) | REPORTDATE | xla去前缀变体 |
| `stm_ra` | 受限资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ar_1` | 应收账款-金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_ar_2` | 应收账款-比例 | REPORTDATE | xla去前缀变体 |
| `stmnote_arratio_cat` | 应收账款-比例(按性质) | REPORTDATE、Category | xla去前缀变体 |
| `stmnote_assetdetail_1` | 固定资产-原值 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_10` | 生产性生物资产-累计折旧 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_11` | 生产性生物资产-减值准备 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_12` | 生产性生物资产-净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_13` | 油气资产-原值 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_14` | 油气资产-累计折耗 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_15` | 油气资产-减值准备 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_16` | 油气资产-净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_17` | 无形资产-原值 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_18` | 无形资产-累计摊销 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_19` | 无形资产-减值准备 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_2` | 固定资产-累计折旧 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_20` | 无形资产-净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_3` | 固定资产-减值准备 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_4` | 固定资产-净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_5` | 投资性房地产-原值 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_6` | 投资性房地产-累计折旧 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_7` | 投资性房地产-减值准备 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_8` | 投资性房地产-净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetdetail_9` | 生产性生物资产-原值 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetmanage` | 受托管理资产总规模 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetmanage_inc_c` | 集合资产管理业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetmanage_inc_d` | 定向资产管理业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetmanage_inc_m` | 公募基金资产管理业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_assetmanage_inc_s` | 专项资产管理业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_1` | 向关联方销售产品及提供劳务金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_2` | 向关联方采购产品及接受劳务金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_3` | 向关联方提供资金发生额 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_4` | 向关联方提供资金余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_5` | 关联方向上市公司提供资金发生额 | REPORTDATE | xla去前缀变体 |
| `stmnote_associated_6` | 关联方向上市公司提供资金余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_aualaccmdiv` | 现金分红总额 | REPORTDATE | xla去前缀变体 |
| `stmnote_audit_agency` | 审计单位(新增) | D | xla去前缀变体 |
| `stmnote_audit_am` | 会计准则类型 | REPORTDATE | xla去前缀变体 |
| `stmnote_audit_category` | 审计意见类别(新增) | D | xla去前缀变体 |
| `stmnote_audit_cpa` | 签字注册会计师(新增) | D | xla去前缀变体 |
| `stmnote_audit_date` | 审计报告披露日期 | REPORTDATE | xla去前缀变体 |
| `stmnote_audit_expense` | 当期实付审计费用(新增) | D | xla去前缀变体 |
| `stmnote_audit_fee` | 审计费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_audit_interpretation` | 审计结果说明(新增) | D | xla去前缀变体 |
| `stmnote_audit_kam` | 关键审计事项 | REPORTDATE | xla去前缀变体 |
| `stmnote_audit_year` | 会计师事务所连续服务年限 | REPORTDATE | xla去前缀变体 |
| `stmnote_avofa` | 固定资产-净值 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_0001` | 逾期贷款_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0002` | 逾期贷款_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0003` | 逾期贷款_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0004` | 逾期贷款_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0005` | 逾期贷款合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0011` | 逾期信用贷款_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0012` | 逾期信用贷款_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0013` | 逾期信用贷款_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0014` | 逾期信用贷款_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0015` | 逾期信用贷款合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0021` | 逾期保证贷款_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0022` | 逾期保证贷款_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0023` | 逾期保证贷款_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0024` | 逾期保证贷款_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0025` | 逾期保证贷款合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0031` | 逾期抵押贷款_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0032` | 逾期抵押贷款_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0033` | 逾期抵押贷款_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0034` | 逾期抵押贷款_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0035` | 逾期抵押贷款合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0041` | 逾期票据贴现_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0042` | 逾期票据贴现_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0043` | 逾期票据贴现_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0044` | 逾期票据贴现_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0045` | 逾期票据贴现合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0051` | 逾期质押贷款_3个月以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0052` | 逾期质押贷款_3个月至1年 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0053` | 逾期质押贷款_1年以上3年以内 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0054` | 逾期质押贷款_3年以上 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_0055` | 逾期质押贷款合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_129` | 成本收入比(%) | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_131` | 资本净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_132` | 核心资本净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_133` | 加权风险资产净额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_144` | 净息差(%) | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_147` | 净利差(%) | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_147r` | 净利差(公布值) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_171` | 杠杆率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_172` | 流动性覆盖率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_1778` | 银行理财产品余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_24n` | 单一最大客户贷款占贷款总额比例 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_25n` | 最大十家客户贷款占贷款总额比例 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_26` | 不良贷款余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_30` | 非利息收入占比 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_31` | 正常-金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_37` | 次级-金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_40` | 可疑-金额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_46` | 短期贷款-平均余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_47` | 短期贷款-年平均利率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_48` | 中长期贷款-平均余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_49` | 中长期贷款-年平均利率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_50` | 企业存款-平均余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_51` | 企业存款-年平均利率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_52` | 储蓄存款-平均余额 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_53` | 储蓄存款-年平均利率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_5444` | 净息差(公布值) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_5453` | 库存现金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_55` | 拨贷比 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_57` | 生息资产平均余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_58` | 生息资产收益率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_59` | 计息负债平均余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_60` | 计息负债成本率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_611` | 存款余额_个人定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_612` | 存款余额_个人活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_613` | 存款余额_公司定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_614` | 存款余额_公司活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_615` | 存款余额_其它存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_616` | 存款余额_个人存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_617` | 存款余额_公司存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_618` | 存款余额_保证金存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_621` | 存款平均余额_个人定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_622` | 存款平均余额_个人活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_623` | 存款平均余额_公司定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_624` | 存款平均余额_公司活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_625` | 存款平均余额_其它存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_631` | 存款利息支出_个人定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_632` | 存款利息支出_个人活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_633` | 存款利息支出_公司定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_634` | 存款利息支出_公司活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_635` | 存款利息支出_其它存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_641` | 存款平均成本率_个人定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_642` | 存款平均成本率_个人活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_643` | 存款平均成本率_公司定期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_644` | 存款平均成本率_公司活期存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_645` | 存款平均成本率_其它存款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_646` | 存款平均成本率_存款总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_647` | 存款余额_存款总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_648` | 存款平均余额_存款总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_649` | 存款利息支出_存款总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_65` | 贷款余额(按行业) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_66` | 不良贷款余额(按行业) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_67` | 不良贷款率(按行业) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_680` | 贷款余额_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_681` | 贷款余额_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_682` | 贷款余额_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_683` | 贷款余额_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_684` | 贷款余额_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_685` | 贷款余额_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_686` | 贷款余额_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_687` | 贷款余额_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_688` | 贷款余额_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_689` | 贷款余额_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_690` | 不良贷款余额_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_691` | 不良贷款余额_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_692` | 不良贷款余额_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_693` | 不良贷款余额_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_694` | 不良贷款余额_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_695` | 不良贷款余额_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_696` | 不良贷款余额_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_697` | 不良贷款余额_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_698` | 不良贷款余额_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_699` | 不良贷款余额_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_700` | 贷款平均余额_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_701` | 不良贷款率_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_702` | 不良贷款率_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_703` | 不良贷款率_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_704` | 不良贷款率_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_705` | 不良贷款率_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_706` | 不良贷款率_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_707` | 不良贷款率_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_708` | 不良贷款率_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_709` | 不良贷款率_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_710` | 贷款利息收入_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_711` | 贷款平均余额_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_712` | 贷款平均余额_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_713` | 贷款平均余额_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_714` | 贷款平均余额_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_715` | 贷款平均余额_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_716` | 贷款平均余额_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_717` | 贷款平均余额_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_718` | 贷款平均余额_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_719` | 贷款平均余额_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_720` | 贷款平均收益率_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_721` | 贷款利息收入_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_722` | 贷款利息收入_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_723` | 贷款利息收入_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_724` | 贷款利息收入_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_725` | 贷款利息收入_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_726` | 贷款利息收入_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_727` | 贷款利息收入_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_728` | 贷款利息收入_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_729` | 贷款利息收入_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_730` | 不良贷款率_总计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_731` | 贷款平均收益率_企业贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_732` | 贷款平均收益率_个人贷款及垫款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_733` | 贷款平均收益率_票据贴现 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_734` | 贷款平均收益率_个人住房贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_735` | 贷款平均收益率_个人消费贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_736` | 贷款平均收益率_信用卡应收账款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_737` | 贷款平均收益率_经营性贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_738` | 贷款平均收益率_汽车贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_739` | 贷款平均收益率_其他个人贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_741` | 贷款余额_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_742` | 贷款余额_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_743` | 贷款余额_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_744` | 贷款余额_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_751` | 不良贷款余额_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_752` | 不良贷款余额_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_753` | 不良贷款余额_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_754` | 不良贷款余额_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_761` | 不良贷款率_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_762` | 不良贷款率_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_763` | 不良贷款率_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_764` | 不良贷款率_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_771` | 贷款平均余额_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_772` | 贷款平均余额_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_773` | 贷款平均余额_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_774` | 贷款平均余额_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_781` | 贷款利息收入_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_781210` | 银行信息科技投入 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_782` | 贷款利息收入_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_783` | 贷款利息收入_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_784` | 贷款利息收入_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_791` | 贷款平均收益率_信用贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_792` | 贷款平均收益率_保证贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_793` | 贷款平均收益率_抵押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_794` | 贷款平均收益率_质押贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_801` | 贷款余额_短期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_802` | 贷款余额_中长期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_811` | 不良贷款余额_短期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_812` | 不良贷款余额_中长期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_821` | 不良贷款率_短期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_822` | 不良贷款率_中长期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_841` | 贷款利息收入_短期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_842` | 贷款利息收入_中长期贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_850` | 贷款余额_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_851` | 不良贷款余额_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_852` | 不良贷款率_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_853` | 贷款平均余额_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_854` | 贷款利息收入_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_855` | 贷款平均收益率_中长期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_856` | 贷款余额_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_857` | 不良贷款余额_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_858` | 不良贷款率_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_859` | 贷款平均余额_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_860` | 贷款利息收入_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_861` | 贷款平均收益率_短期公司类贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_9501` | 正常-迁徙率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9502` | 关注-迁徙率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9503` | 次级-迁徙率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9504` | 可疑-迁徙率 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9506` | 正常-占贷款总额比 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9507` | 关注-占贷款总额比 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9508` | 次级-占贷款总额比 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9509` | 可疑-占贷款总额比 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_9510` | 损失-占贷款总额比 | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_alb` | 调整后表内外资产余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ar` | 贷款损失准备充足率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_asf` | 可用的稳定资金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_assetliqratio` | 短期资产流动性比率(本外币) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_aucd` | 托管资产(国内系统重要性指标) | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_aucg` | 托管资产(全球系统重要性指标) | REPORTDATE | xla去前缀变体 |
| `stmnote_bank_capadequacyratio` | 资本充足率(2013) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_capadequacyratio_ct1` | 核心一级资本充足率(2013) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_capadequacyratio_t1` | 一级资本充足率(2013) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_coretier1cap` | 核心一级资本净额(2013) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ibasst` | 同业资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ibasstpct` | 同业资产占比 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ibliabty` | 同业负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ibliabtypct` | 同业负债占比 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_impair` | 计提减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_ldr` | 贷款逾期率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_netequitycap` | 资本净额(2013) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_rl` | 已重组贷款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_bank_rsf` | 所需的稳定资金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_dpst_4406` | 美元存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4407` | 日元存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4408` | 欧元存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4409` | 港币存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4410` | 英镑存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4411` | 其他货币存款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_dpst_4412` | 银行存款合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_eduandunionfunds_add` | 工会经费和职工教育经费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eduandunionfunds_de` | 工会经费和职工教育经费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eduandunionfunds_eb` | 工会经费和职工教育经费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eduandunionfunds_sb` | 工会经费和职工教育经费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplinjuryins_add` | 工伤保险费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplinjuryins_de` | 工伤保险费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplinjuryins_eb` | 工伤保险费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplinjuryins_sb` | 工伤保险费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplpayable_add` | 应付职工薪酬合计:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplpayable_de` | 应付职工薪酬合计:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplpayable_eb` | 应付职工薪酬合计:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_emplpayable_sb` | 应付职工薪酬合计:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_10` | 企业合并产生的损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_11` | 非货币性资产交换损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_12` | 委托投资损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_13` | 资产减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_14` | 债务重组损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_15` | 企业重组费用 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_16` | 交易产生的损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_17` | 同一控制下企业合并产生的子公司当期净损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_18` | 预计负债产生的损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_19` | 其他营业外收支净额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_20` | 中国证监会认定的其他项目 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_21` | 非经常性损益项目小计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_22` | 所得税影响数 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_23` | 少数股东损益影响数 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_24` | 非经常性损益项目合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_28` | 持有(或处置)交易性金融资产和负债产生的公允价值变动损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_29` | 单独进行监制测试的应收款项减值准备转回 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_30` | 对外委托贷款取得的收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_31` | 公允价值法计量的投资性房地产价值变动损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_32` | 法规要求一次性损益调整影响 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_33` | 受托经营取得的托管费收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_6` | 非流动资产处置损益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_7` | 税收返还、减免 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_8` | 政府补助 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_eoitems_9` | 资金占用费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_faaviableforsale_0001` | 可供出售金融资产:产生的利得/(损失) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_faaviableforsale_0002` | 可供出售金融资产:产生的所得税影响 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_faaviableforsale_0003` | 可供出售金融资产:前期计入其他综合收益当期转入损益的金额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_faaviableforsale_0004` | 可供出售金融资产公允价值变动 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_fahb` | 固定资产-房屋及建筑物-原值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_fame` | 固定资产-机器设备-原值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_fao` | 固定资产-其他-原值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_fate` | 固定资产-运输工具-原值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_finexp_13` | 利息资本化金额 | DATE | xla原码 |
| `stmnote_franchiseright` | 特许经营权_账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_goodwillbv` | 商誉-账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_goodwilldetail` | 商誉-账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_goodwillimpairment` | 商誉-减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_guarantee_1` | 担保发生额合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_guarantee_2` | 担保余额合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_guarantee_3` | 关联担保余额合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_guarantee_4` | 对控股子公司担保发生额合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_guarantee_5` | 违规担保总额 | REPORTDATE | xla去前缀变体 |
| `stmnote_guarantee_6` | 担保总额占净资产比例 | REPORTDATE | xla去前缀变体 |
| `stmnote_housingfund_add` | 住房公积金:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_housingfund_de` | 住房公积金:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_housingfund_eb` | 住房公积金:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_housingfund_sb` | 住房公积金:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ieaibl_1` | 存放中央银行款项-平均利率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ieaibl_2` | 存拆放同业及其他金融机构-平均利率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ieaibl_3` | 金融投资-平均利率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ieaibl_4` | 同业和其他金融机构存放款项-平均利率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ieaibl_5` | 应付债券-平均利率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_1` | 长期股权投资减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_10` | 固定资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_11` | 无形资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_12` | 使用权资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_13` | 生产性生物资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_14` | 油气资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_15` | 资产减值损失-其他 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_17` | 投资性房地产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_18` | 买入返售金融资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_19` | 贷款减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_2` | 工程物资减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_20` | 融出资金减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_21` | 应收款项类投资减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_22` | 抵债资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_23` | 合同资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_3` | 在建工程减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_4` | 坏账损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_5` | 存货跌价损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_6` | 商誉减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_7` | 发放贷款和垫款减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_8` | 可供出售金融资产减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_9` | 持有至到期投资减值损失 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_impairmentloss_total` | 资产减值损失-合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_inaudit_agency` | 内控_审计单位 | REPORTDATE | xla去前缀变体 |
| `stmnote_inaudit_category` | 内控_审计意见类别 | REPORTDATE | xla去前缀变体 |
| `stmnote_inaudit_cost` | 内控_审计费用 | REPORTDATE、Zone | xla去前缀变体 |
| `stmnote_inaudit_cpa` | 内控_签字审计师 | REPORTDATE | xla去前缀变体 |
| `stmnote_inaudit_interpretation` | 内控_审计结果说明 | REPORTDATE | xla去前缀变体 |
| `stmnote_inaudit_issuingdate` | 内控报告披露日期 | REPORTDATE | xla去前缀变体 |
| `stmnote_incometax_0` | 当期所得税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_1` | 当期所得税:中国大陆 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_2` | 当期所得税:中国香港 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_3` | 当期所得税:其他境外 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_4` | 以前年度所得税调整 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_5` | 递延所得税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_incometax_6` | 所得税费用合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_increaseofsurplus` | 法定盈本期增加值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_initialsurplus` | 法定盈余期初值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_1` | 保单继续率(13个月) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_10` | 赔付率(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_11` | 费用率(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_12` | 偿付能力充足率(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_13` | 实际资本(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_13n` | 实际资本(产险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_14` | 最低资本(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_14n` | 最低资本(产险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_15` | 偿付能力充足率(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_16` | 内含价值(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_16n` | 内含价值(寿险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_17` | 新业务价值(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_17n` | 新业务价值(寿险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_18` | 有效业务价值(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_18n` | 有效业务价值(寿险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_19` | 实际资本(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_195834` | 综合投资收益率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_195835` | 综合成本率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_195836` | 综合费用率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_195837` | 综合赔付率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_195838` | 签单保费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_195839` | 车险签单保费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_19n` | 实际资本(寿险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_2` | 保单继续率(14个月) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_20` | 最低资本(寿险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_20n` | 最低资本(寿险) | REPORTDATE、TYPE、CURTYPE | xla去前缀变体 |
| `stmnote_insur_21` | 新业务价值率(寿险) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_3` | 保单继续率(25个月) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_30n` | 集团内含价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_4` | 保单继续率(26个月) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_5` | 净投资收益率 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_6` | 总投资收益率 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7` | 评估利率假设：风险贴现率 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7801` | 定期存款 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7802` | 债券投资 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7803` | 基金投资 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7804` | 股票投资 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7805` | 股权投资 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7806` | 基建投资 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7807` | 现金及现金等价物 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7808` | 其它资产 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7809` | 总投资资产 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7810` | 集团客户数 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7811` | 保险营销员人数 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7812` | 保险营销员每月人均首年保险业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_7813` | 保险营销员每月人均寿险新保单件数 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_8` | 退保率 | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_9` | 综合成本率(产险) | REPORTDATE | xla去前缀变体 |
| `stmnote_insur_mincap` | 最低资本(集团) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_rcap` | 实际资本(集团) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_insur_solratio` | 偿付能力充足率(集团) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_inv_1` | 存货明细-原材料 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_10` | 存货明细-合同履约成本 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_11` | 存货明细-其他存货 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_12` | 存货明细-在途物资 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_2` | 存货明细-在产品 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_3` | 存货明细-产成品 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_4` | 存货明细-低值易耗品 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_5` | 存货明细-包装物 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_6` | 存货明细-委托加工材料 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_7` | 存货明细-委托代销商品 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_9` | 存货明细-消耗性生物资产 | REPORTDATE | xla去前缀变体 |
| `stmnote_inv_goodsship` | 存货明细-发出商品 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0001` | 固定息证券投资利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0002` | 权益投资资产分红收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0003` | 投资性房地产租金收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0004` | 净投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0005` | 证券买卖收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0006` | 公允价值变动收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0007` | 计提投资资产减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0008` | 处置合营企业净收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0009` | 其他收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_investmentincome_0010` | 总投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_1` | 权益法核算的长期股权投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_10` | 投资收益-合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_11` | 投资收益-其他 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_12` | 持有可供出售金融资产等期间取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_13` | 成本法核算的长期股权投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_14` | 处置持有至到期投资取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_15` | 理财产品投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_16` | 应收款项类投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_17` | 金融工具持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_18` | 债权投资在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_19` | 其他债权投资在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_2` | 处置长期股权投资产生的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_20` | 其他权益工具投资在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_21` | 其他非流动金融资产在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_22` | 处置金融工具取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_23` | 处置债权投资取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_24` | 处置其他债权投资取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_25` | 处置其他权益工具投资取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_26` | 处置其他非流动金融资产取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_3` | 以公允价值计量且其变动计入当期损益的金融资产在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_4` | 处置以公允价值计量且变动计入当期损益的金融资产取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_5` | 持有至到期投资在持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_6` | 可供出售金融资产等取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_7` | 处置可供出售金融资产取得的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_8` | 丧失控制权后剩余股权按公允价值重新计量产生的利得 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invincome_9` | 处置子公司的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_invtot` | 存货合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_ird_1` | 名义金额-利率衍生工具(非套期工具) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ird_2` | 名义金额-权益衍生工具(非套期工具) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_landuserights_19` | 土地使用权_原值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_landuserights_20` | 土地使用权_累计摊销 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_landuserights_21` | 土地使用权_减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_landuserights_22` | 土地使用权_账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_legalsurplusreserve` | 法定盈余期末值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_loans_1` | 转融通融入资金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_ltborrow_4505` | 人民币长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4506` | 美元长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4507` | 日元长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4508` | 欧元长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4509` | 港币长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4510` | 英镑长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4511` | 其他货币长期借款(折算人民币) | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4512` | 长期借款小计 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4513` | 质押长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4514` | 抵押长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4515` | 保证长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4516` | 信用长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4517` | 委托长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_ltborrow_4518` | 其他长期借款 | REPORTDATE | xla去前缀变体 |
| `stmnote_maternityins_add` | 生育保险费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_maternityins_de` | 生育保险费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_maternityins_eb` | 生育保险费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_maternityins_sb` | 生育保险费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_medins_add` | 医疗保险费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_medins_de` | 医疗保险费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_medins_eb` | 医疗保险费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_medins_sb` | 医疗保险费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_mewprofitapr` | 可分配利润 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_mgmt_ben` | 管理层年度薪酬总额 | Year | xla去前缀变体 |
| `stmnote_mgmt_ben_bc` | 董事长薪酬 |  | xla去前缀变体 |
| `stmnote_mgmt_ben_ceo` | 总经理薪酬 |  | xla去前缀变体 |
| `stmnote_mgmt_ben_cfo` | 财务总监薪酬 |  | xla去前缀变体 |
| `stmnote_mgmt_ben_discloser` | 董事会秘书薪酬 |  | xla去前缀变体 |
| `stmnote_mgmt_ben_sar` | 证券事务代表薪酬 |  | xla去前缀变体 |
| `stmnote_mgmt_ben_top3b` | 金额前三的董事薪酬合计 | Year | xla去前缀变体 |
| `stmnote_mgmt_ben_top3m` | 金额前三的高管薪酬合计 | Year | xla去前缀变体 |
| `stmnote_netinv_1` | 存货明细-原材料(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_10` | 产成品明细-发出商品(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_11` | 存货明细-其他存货(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_12` | 存货明细-在途物资(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_2` | 存货明细-在产品(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_3` | 存货明细-产成品(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_4` | 存货明细-低值易耗品(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_5` | 存货明细-包装物(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_6` | 存货明细-委托加工材料(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_7` | 存货明细-委托代销商品(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_8` | 存货明细-已加工未结算(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_netinv_tlt` | 存货合计(净额) | REPORTDATE | xla去前缀变体 |
| `stmnote_nii_1` | 利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_10` | 发放贷款和垫款利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_11` | 货币资金及结算备付金利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_12` | 金融投资利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_13` | 其他按实际利率法计算的金融资产产生的利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_14` | 融出资金利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_15` | 融资融券利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_16` | 应收融资租赁款利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_17` | 债券投资利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_18` | 债权投资利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_19` | 其他债权投资利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_2` | 买入返售金融资产利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_20` | 其他利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_21` | 代理买卖证券款利息支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_22` | 租赁负债利息支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_23` | 应付短期融资款利息支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_24` | 应付债券利息支出 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_3` | 买入返售金融资产利息收入-约定购回利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_4` | 买入返售金融资产利息收入-股权质押回购利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_5` | 买入返售金融资产利息收入-股票质押回购利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_6` | 拆出资金利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_7` | 存放及拆放同业利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_8` | 存放中央银行利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nii_9` | 存款利息收入 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nonpatentedtechnology` | 非专利技术_账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_np_1` | 应付票据-商业承兑汇票 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_np_2` | 应付票据-银行承兑汇票 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_np_3` | 应付票据-其他 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_np_total` | 应付票据-合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_npls` | 租赁资产不良率 | Year | xla去前缀变体 |
| `stmnote_nr_1` | 应收票据-商业承兑汇票 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nr_2` | 应收票据-银行承兑汇票 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nr_3` | 应收票据-其他 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_nr_total` | 应收票据-合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7636` | 一年内到期的长期借款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7637` | 一年内到期的应付债券 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7639` | 短期融资债(其他流动负债) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7640` | 一年内到期的长期应付款 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7641` | 一年内到期的租赁负债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7642` | 其他流动负债(其他) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7643` | 合计(其他流动负债) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7644` | 合计(一年内到期的非流动负债) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7645` | 一年内到期的非流动负债(其他) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7646` | 研发费用(管理费用) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7647` | 差旅费(销售费用) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7648` | 业务招待费(销售费用) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7649` | 股份支付(销售费用) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7650` | 股份支付(管理费用) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_others_7651` | 研发费用-股份支付 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_patentright` | 专利权_账面价值 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_profitapr_1` | 期初未分配利润 | REPORTDATE | xla去前缀变体 |
| `stmnote_profitapr_10` | 提取一般风险准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_profitapr_2` | 本报告期实现净利润 | REPORTDATE | xla去前缀变体 |
| `stmnote_profitapr_3` | 期末可分配利润 | REPORTDATE | xla去前缀变体 |
| `stmnote_profitapr_4` | 支付普通股股利 | REPORTDATE | xla去前缀变体 |
| `stmnote_profitapr_5` | 提取法定盈余公积 | REPORTDATE | xla去前缀变体 |
| `stmnote_profitapr_6` | 提取任意公积金 | REPORTDATE | xla去前缀变体 |
| `stmnote_rdothers` | 研发费用-其他 | REPORTDATE | xla去前缀变体 |
| `stmnote_rdsalary` | 研发费用-工资薪酬 | REPORTDATE | xla去前缀变体 |
| `stmnote_rdtravel` | 研发费用-差旅费 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_salestop5` | 前五大客户销售收入总额 | REPORTDATE | xla去前缀变体 |
| `stmnote_salestop5_pct` | 前五大客户销售收入占比 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1` | 净资本 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_10` | 融资(含融券)的金额/净资本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_1500` | 手续费及佣金收入合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1501` | 手续费及佣金收入:证券经纪业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1502` | 手续费及佣金收入:受托客户资产管理业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1503` | 手续费及佣金收入:证券承销业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1504` | 手续费及佣金收入:财务顾问业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1505` | 手续费及佣金收入:保荐业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1506` | 手续费及佣金收入:投资咨询业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1507` | 手续费及佣金收入:期货经纪业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1510` | 利息收入合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1511` | 利息收入:融资融券业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1512` | 利息收入:金融企业往来业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1513` | 利息收入:金融资产回购业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1520` | 手续费及佣金净收入合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1521` | 手续费及佣金净收入:证券经纪业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1522` | 手续费及佣金净收入:受托客户资产管理业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1523` | 手续费及佣金净收入:证券承销业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1524` | 手续费及佣金净收入:财务顾问业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1525` | 手续费及佣金净收入:保荐业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1526` | 手续费及佣金净收入:投资咨询业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1527` | 手续费及佣金净收入:期货经纪业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1528` | 手续费及佣金净收入:基金管理业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1530` | 利息净收入合计 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1531` | 利息净收入:融资融券业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1532` | 利息净收入:金融企业往来业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1533` | 利息净收入:金融资产回购业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1540` | 证券投资业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1541` | 证券经纪业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1542` | 投资银行业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1543` | 资产管理业务收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1550` | 证券投资业务净收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1551` | 证券经纪业务净收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1552` | 投资银行业务净收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1553` | 资产管理业务净收入 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1554` | 手续费及佣金净收入:其他业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1555` | 手续费及佣金净收入:托管及其他受托业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_1853` | 权益乘数(剔除客户交易保证金) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_2` | 受托资金 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_3` | 净资本负债率 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_30` | 核心净资本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_31` | 附属净资本 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_32` | 各项风险资本准备之和 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_33` | 表内外资产总额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_34` | 资本杠杆率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_35` | 流动性覆盖率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_36` | 净稳定资金率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_4` | 净资本比率 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_5` | 净资本/各项风险准备之和 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_6` | 净资本/净资产 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_7` | 自营权益类证券及证券衍生品/净资本 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_8` | 自营固定收益类证券/净资本 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_9` | 净资产负债率 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_leaseseat` | 手续费及佣金收入:证券经纪业务:交易单元席位租赁 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_op_1` | 自营证券合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_op_2` | 自营股票 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_op_3` | 自营国债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_op_4` | 自营基金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_op_5` | 自营证可转债 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_sec_resellfin` | 手续费及佣金收入:证券经纪业务:代销金融产品业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_sec_security` | 手续费及佣金收入:证券经纪业务:代理买卖证券业务 | REPORTDATE | xla去前缀变体 |
| `stmnote_securitieslending_1` | 融出证券合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_securitieslending_2` | 融出证券:交易性金融资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_securitieslending_3` | 融出证券:可供出售金融资产 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_securitieslending_4` | 融出证券:转融通融入证券 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_securitieslending_5` | 融出证券:转融通融入证券余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_securitieslending_6` | 融出证券:减值准备 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax` | 债券/报表附注函数/所得税税率 | RPTYEAR | xla去前缀变体 |
| `stmnote_tax_building` | 房产税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_business` | 营业税金及附加合计 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_construction` | 城建税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_consumption` | 消费税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_edesupplementtary` | 教育费附加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_oth` | 其他营业税金及附加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_stamp` | 印花税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tax_urbanlanduse` | 土地使用税 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_1` | 交易性金融资产-股票/股权 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_10` | 交易性金融资产-债券/债务 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_11` | 交易性金融资产-信托 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_12` | 交易性金融资产-理财产品 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_13` | 交易性金融资产-永续债/优先股 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_14` | 交易性金融资产-资管产品 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_15` | 交易性金融资产-非上市股权 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_2` | 交易性金融资产-贵金属 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_3` | 交易性金融资产-基金(合计) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_4` | 交易性金融资产-基金(其他) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_5` | 交易性金融资产-私募基金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_6` | 交易性金融资产-公募基金 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_7` | 交易性金融资产-票据 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_8` | 交易性金融资产-其他 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfa_9` | 交易性金融资产-权益工具 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfainvest` | 交易性金融资产持有期间的投资收益 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_tfatotal` | 交易性金融资产(合计) | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_unemplins_add` | 失业保险费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_unemplins_de` | 失业保险费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_unemplins_eb` | 失业保险费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_unemplins_sb` | 失业保险费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_welfare_add` | 职工福利费:本期增加 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_welfare_de` | 职工福利费:本期减少 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_welfare_eb` | 职工福利费:期末余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stmnote_welfare_sb` | 职工福利费:期初余额 | REPORTDATE、TYPE | xla去前缀变体 |
| `stockclass` | 股票种类(新增) |  | xla去前缀变体 |
| `style_averagepositiontime` | 平均持仓时间 |  | xla去前缀变体 |
| `style_avgpositiontimeranking` | 平均持仓时间同类排名 |  | xla去前缀变体 |
| `style_commisaccount` | 佣金规模比 | REPORTDATE | xla去前缀变体 |
| `style_hy_averagepositiontime` | 平均持仓时间(半年) |  | xla去前缀变体 |
| `style_invconcentration` | 投资集中度 |  | xla去前缀变体 |
| `style_marketvalueattribute` | 市值属性 |  | xla去前缀变体 |
| `style_marketvaluestyleattribute` | 市值-风格属性 |  | xla去前缀变体 |
| `style_rpt_turn` | 基金报告期持仓换手率 |  | xla去前缀变体 |
| `style_styleattribute` | 风格属性 |  | xla去前缀变体 |
| `style_stylecoefficient` | 风格系数 |  | xla去前缀变体 |
| `style_topnproportiontoallindustries` | 前N大行业占全部行业比 |  | xla去前缀变体 |
| `style_topnproportiontoallshares` | 前N大股票占全部股票投资比 |  | xla去前缀变体 |
| `styleindexcode_citic` | 所属中信风格指数代码 | TRADEDATE | xla去前缀变体 |
| `styleindexname_citic` | 所属中信风格指数名称 | TRADEDATE | xla去前缀变体 |
| `subindexcode` | 副指数代码 |  | xla去前缀变体 |
| `sucdirector` | 公司董事(历任) | TRADEDATE | xla去前缀变体 |
| `sucexecutives` | 公司高管(历任) | TRADEDATE | xla去前缀变体 |
| `sucindpdirector` | 公司独立董事(历任) | TRADEDATE | xla去前缀变体 |
| `sucsupervisor` | 公司监事(历任) | TRADEDATE | xla去前缀变体 |
| `sunkcapital` | 沉淀资金 | TRADEDATE | xla去前缀变体 |
| `superiorcode` | 上级行业指数代码 | TYPE | xla去前缀变体 |
| `supervisor` | 公司监事 |  | xla去前缀变体 |
| `surpluscapitalps` | 每股资本公积 | REPORTDATE | xla去前缀变体 |
| `surplusreserveps` | 每股盈余公积 | REPORTDATE | xla去前缀变体 |
| `susp_days` | 连续停牌天数 |  | 探测法实测 |
| `swapwindcode` | 摘牌换股标的Wind代码 |  | xla去前缀变体 |
| `swiftcode` | SWIFT编码 |  | xla去前缀变体 |
| `swing` | 振幅 |  | 探测法实测 |
| `system_risk` | 系统风险 | StartDate、EndDate | xla去前缀变体 |
| `szse_distribcode` | 深交所分销代码 |  | xla去前缀变体 |
| `tangibleasset` | 有形资产 | REPORTDATE | xla去前缀变体 |
| `tangibleassetstoassets` | 有形资产／总资产 | REPORTDATE | xla去前缀变体 |
| `tangibleassettodebt` | 有形资产／负债合计 | REPORTDATE | xla去前缀变体 |
| `tangibleassettonetdebt` | 有形资产／净债务 | REPORTDATE | xla去前缀变体 |
| `tapi` | TAPI加权指数成交值 |  | xla原码 |
| `targetnp` | 股权激励目标净利润 |  | xla去前缀变体 |
| `targetprice_avg` | 目标价(均值) |  | 探测法实测 |
| `targetprice_max` | 目标价(MAX) | DATE、PERIOD | xla去前缀变体 |
| `targetprice_max1` | 目标价(MAX) | DATE | xla去前缀变体 |
| `targetprice_min` | 目标价(MIN) | DATE、PERIOD | xla去前缀变体 |
| `targetprice_min1` | 目标价(MIN) | DATE | xla去前缀变体 |
| `tax` | 债券/报表附注函数/所得税税率 | RPTYEAR | xla去前缀变体 |
| `tax_ttm` | 所得税(TTM) | REPORTDATE | xla去前缀变体 |
| `taxfree` | 是否免税 |  | xla去前缀变体 |
| `taxtoebt` | 所得税／利润总额 | REPORTDATE | xla去前缀变体 |
| `taxtoebt_ttm` | 税项/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `taxtoebt_ttm2` | 税项/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `taxtoor_ttm` | 营业利润/利润总额(TTM) | REPORTDATE | xla去前缀变体 |
| `tbf_basis` | 基差 | TRADEDATE | xla去前缀变体 |
| `tbf_basis01` | 基差 | FuturePriceType、DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_basis02` | 基差(CTD) | PRICETYPE、TradingVenue、TRADEDATE | xla去前缀变体 |
| `tbf_bonddeliverydate` | 交券日 | TRADEDATE | xla去前缀变体 |
| `tbf_ctd2` | CTD(支持历史) | TRADEDATE | xla去前缀变体 |
| `tbf_cvf` | 转换因子 |  | xla去前缀变体 |
| `tbf_cvf2` | 转换因子 |  | xla去前缀变体 |
| `tbf_cvf3` | 转换因子(主力合约) | TRADEDATE、ContractCode | xla去前缀变体 |
| `tbf_cvf4` | 转换因子 | DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_deliverprice` | 交割成本 | TRADEDATE | xla去前缀变体 |
| `tbf_deliverycost` | 交割成本 | DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_deliveryinterest` | 交割利息 | DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_fytm` | 远期收益率 | TRADEDATE | xla去前缀变体 |
| `tbf_fytm01` | 隐含利率 | FuturePriceType、DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_fytm02` | 隐含利率(CTD) | PRICETYPE、TradingVenue、TRADEDATE | xla去前缀变体 |
| `tbf_interest` | 交割利息 | TRADEDATE | xla去前缀变体 |
| `tbf_interestpayment` | 区间付息 | DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_invoiceprice` | 发票价格 | TRADEDATE | xla去前缀变体 |
| `tbf_invoiceprice01` | 发票价格 | FuturePriceType、DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_irr2` | IRR(支持历史) | TRADEDATE、PRICETYPE | xla去前缀变体 |
| `tbf_lastdeliverydate` | 最后交割日 | TRADEDATE | xla去前缀变体 |
| `tbf_netbasis` | 净基差 | TRADEDATE | xla去前缀变体 |
| `tbf_netbasis01` | 净基差 | FuturePriceType、DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_netbasis02` | 净基差(CTD) | PRICETYPE、TradingVenue、TRADEDATE | xla去前缀变体 |
| `tbf_payment` | 区间利息 | TRADEDATE | xla去前缀变体 |
| `tbf_paymentdate` | 缴款日 | TRADEDATE | xla去前缀变体 |
| `tbf_spotspread` | 期现利差(CTD)(减现货) | TYPE、VENUE、TRADEDATE | xla去前缀变体 |
| `tbf_spread` | 期现价差 | TRADEDATE | xla去前缀变体 |
| `tbf_spread01` | 期现价差 | FuturePriceType、DeliveryCode、TRADEDATE | xla去前缀变体 |
| `tbf_spread02` | 期现价差(CTD) | PRICETYPE、TradingVenue、TRADEDATE | xla去前缀变体 |
| `tbf_vbasis01` | 基差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_vbasis02` | 基差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbf_vctd02` | CTD(估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbf_vdeliverycost` | 交割成本(估) | DeliveryCode、PriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_vfytm01` | 隐含利率(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_vfytm02` | 隐含利率(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbf_virr01` | IRR(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_virr02` | IRR(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbf_vnetbasis01` | 净基差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_vnetbasis02` | 净基差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbf_vspread01` | 期现价差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE | xla去前缀变体 |
| `tbf_vspread02` | 期现价差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE | xla去前缀变体 |
| `tbondbalance` | 国债余额(做市后) | TRADEDATE | xla去前缀变体 |
| `techanal_stagehigh_num` | 成份创阶段新高数量 | TRADEDATE、NDAYS | xla去前缀变体 |
| `techanal_stagelow_num` | 成份创阶段新低数量 | TRADEDATE、NDAYS | xla去前缀变体 |
| `technicalrisk` | 技术风险提示 |  | xla去前缀变体 |
| `tender_exchange` | 招标场所 |  | xla去前缀变体 |
| `tender_payenddate` | 缴款截止日 |  | xla去前缀变体 |
| `tender_time` | 招标时间 |  | xla去前缀变体 |
| `tendrst_balance` | 主承销商余额包销金额 |  | xla去前缀变体 |
| `tendrst_balanceunderweiting` | 主承销商余额包销说明 |  | xla去前缀变体 |
| `tendrst_code` | 中债招标发行代码 |  | xla去前缀变体 |
| `tendrst_effectinvestors` | 有效投标(申购)家数 |  | xla去前缀变体 |
| `tendrst_tenderamount` | 投标(申购)总量 |  | xla去前缀变体 |
| `term` | 转债发行期限 |  | xla去前缀变体 |
| `term2` | 债券期限(文字) |  | xla去前缀变体 |
| `term3` | 债券期限(文字/加权) |  | xla去前缀变体 |
| `termifexercise` | 行权剩余期限(年) | TRADEDATE | xla去前缀变体 |
| `termnote` | 特殊剩余期限说明 |  | xla去前缀变体 |
| `termnote1` | 特殊剩余期限 | TRADEDATE | xla去前缀变体 |
| `termnote2` | 特殊剩余期限说明(最近行权日) | TRADEDATE | xla去前缀变体 |
| `termnote3` | 剩余期限(每个行权日) | Cycle、TRADEDATE | xla去前缀变体 |
| `termnote4` | 剩余期限(下一行权日) | Cycle、TRADEDATE | xla去前缀变体 |
| `thematicindustry_sib` | 所属科创板主题行业 | TRADEDATE、TYPE | xla去前缀变体 |
| `thematicindustry_wind` | 所属Wind主题行业名称 | TRADEDATE | xla去前缀变体 |
| `theoryvalue` | 理论价格 |  | xla去前缀变体 |
| `theta_exch` | Theta(交易所) | TRADEDATE | xla去前缀变体 |
| `thours` | 交易时间说明 |  | xla去前缀变体 |
| `thours2` | 交易时间说明 | TRADEDATE | xla去前缀变体 |
| `timevalue` | 时间价值 |  | xla去前缀变体 |
| `tlacbonds` | 是否TLAC债 |  | xla去前缀变体 |
| `tltoebitda` | 全部债务/EBITDA |  | xla去前缀变体 |
| `todaypositionfee` | 期货平今手续费 | TRADEDATE | xla去前缀变体 |
| `top10stock_pb` | 重仓持股平均市净率 | REPORTDATE | xla去前缀变体 |
| `top10stock_pe` | 重仓持股平均市盈率 | REPORTDATE | xla去前缀变体 |
| `topnindustry_stable_thirdparty` | 前N大行业是否稳定 | StartDate、DATE、PsitionThreshold | xla去前缀变体 |
| `topnindustrynames_thirdparty` | 前N大行业名称 | REPORTDATE | xla去前缀变体 |
| `tot_assets` | 资产总计 |  | 探测法实测 |
| `tot_cur_assets` | 流动资产合计 |  | 探测法实测 |
| `tot_cur_liab` | 流动负债合计 |  | 探测法实测 |
| `tot_equity` | 所有者权益合计 |  | 探测法实测 |
| `tot_liab` | 负债合计 |  | 探测法实测 |
| `tot_oper_cost` | 营业总成本 |  | 探测法实测 |
| `tot_oper_rev` | 营业总收入 |  | 探测法实测 |
| `total_shares` | 总股本 |  | 探测法实测 |
| `totalequity_mrq` | 股东权益(MRQ) |  | xla去前缀变体 |
| `totaltm` | 总存续期 |  | xla去前缀变体 |
| `towithdrawalamt` | 撤标总金额 |  | xla去前缀变体 |
| `trackedbyfunds` | 跟踪标的基金代码 | TRADEDATE | xla去前缀变体 |
| `trackedbyfundsnum` | 跟踪标的基金数量 | TRADEDATE | xla去前缀变体 |
| `tradecode` | 期权交易代码 | TRADEDATE | xla去前缀变体 |
| `tradefee` | 期权交易手续费 | DEALDATE | xla去前缀变体 |
| `tradeyiled_broker` | 成交收盘收益率(经纪商) | TRADEDATE | xla去前缀变体 |
| `tranche` | 各级发行总额 | Tranche | xla去前缀变体 |
| `trancheratio` | 各级占比 | Tranche | xla去前缀变体 |
| `transactionfee` | 期货交易手续费 | TRADEDATE | xla去前缀变体 |
| `transfertype` | 转让方式 | TRADEDATE | xla去前缀变体 |
| `treynor` | Treynor(新增) | TD1、TD2 | xla去前缀变体 |
| `trix` | TRIX三重指数平滑平均 |  | xla原码 |
| `trust_investfield` | 信托投资领域 |  | xla原码 |
| `trust_relatedfirm` | 预期收益率说明 |  | xla原码 |
| `trust_sourcetype` | 信托产品类别 |  | xla原码 |
| `trust_type` | 信托类别 |  | xla原码 |
| `tunit` | 交易单位 |  | xla去前缀变体 |
| `turn` | 换手率 |  | 探测法实测 |
| `turndays` | 营业周期 | REPORTDATE | xla去前缀变体 |
| `turnover_ttm` | 总资产周转率(TTM) | REPORTDATE | xla去前缀变体 |
| `udly_maturity` | 期权标的及到期日列表 | TRADEDATE | xla去前缀变体 |
| `underlyingcode` | 正股代码 |  | xla去前缀变体 |
| `underlyinghisvol_30d` | 标的30日历史波动率 | TRADEDATE | xla去前缀变体 |
| `underlyinghisvol_90d` | 标的90日历史波动率 | TRADEDATE | xla去前缀变体 |
| `underlyingmv` | 正股流通市值 | DEALDATE | xla去前缀变体 |
| `underlyingname` | 正股简称 |  | xla去前缀变体 |
| `underlyingpb` | 正股市净率 |  | xla去前缀变体 |
| `underlyingpe` | 正股市盈率 |  | xla去前缀变体 |
| `underlyingwindcode` | 基础证券Wind代码 |  | xla去前缀变体 |
| `undimpvolchg` | 期权波动率涨跌 | TRADEDATE | xla去前缀变体 |
| `undistributedps` | 每股未分配利润 | REPORTDATE | xla去前缀变体 |
| `undly_variety` | 标的品种代码 |  | xla去前缀变体 |
| `unit_change` | 基金份额变化 | BEGINDATE、EndDate | xla去前缀变体 |
| `unit_changedate` | 基金份额变动日期 |  | xla去前缀变体 |
| `unit_changerate` | 基金份额变化率 | BEGINDATE、EndDate | xla去前缀变体 |
| `unit_floortrading` | 场内流通份额 |  | xla去前缀变体 |
| `unit_floortradingchange` | 当期场内流通份额变化 | TRADEDATE | xla去前缀变体 |
| `unit_mergedsharesornot` | 份额是否为合并数据 |  | xla去前缀变体 |
| `unit_netpurchase` | 报告期申购赎回净额 | REPORTDATE | xla去前缀变体 |
| `unit_netpurchase_qty` | 单季申购赎回净额 | REPORTDATE | xla去前缀变体 |
| `unit_netpurchasetot` | 报告期申购赎回净额(合计) | REPORTDATE | xla去前缀变体 |
| `unit_netquarterlyratio` | 单季度净申购赎回率 |  | xla去前缀变体 |
| `unit_nontradable` | 未上市流通基金份数(封闭式) |  | xla去前缀变体 |
| `unit_purchase` | 报告期总申购份额 | REPORTDATE | xla去前缀变体 |
| `unit_purchase_qty` | 单季总申购份额 | REPORTDATE | xla去前缀变体 |
| `unit_purchasetot` | 报告期总申购份额(合计) | REPORTDATE | xla去前缀变体 |
| `unit_redemption` | 报告期总赎回份额 | REPORTDATE | xla去前缀变体 |
| `unit_redemption_qty` | 单季总赎回份额 | REPORTDATE | xla去前缀变体 |
| `unit_redemptiontot` | 报告期总赎回份额(合计) | REPORTDATE | xla去前缀变体 |
| `unit_reitsfloornontrading` | REITs未流通份额 | TRADEDATE | xla去前缀变体 |
| `unit_reitsfloortrading` | REITs场内流通份额 | TRADEDATE | xla去前缀变体 |
| `unit_total` | 基金份额 |  | xla去前缀变体 |
| `unit_tradable` | 已上市流通基金份数(封闭式) |  | xla去前缀变体 |
| `unofferamt` | 未要约金额 | DEALDATE | xla去前缀变体 |
| `unreleasedamount` | 最新未回售金额 |  | xla去前缀变体 |
| `up_mkt_capture` | 上行捕获率 | StartDate、EndDate、CalcTerm、Underlying_Index | xla去前缀变体 |
| `upper_limitprice` | 估值全价上限(中债) | DEALDATE | xla去前缀变体 |
| `us_amount` | 正股成交额 |  | xla去前缀变体 |
| `us_avgprice` | 正股均价 |  | xla去前缀变体 |
| `us_change` | 正股涨跌 |  | xla去前缀变体 |
| `us_close` | 正股收盘价 |  | xla去前缀变体 |
| `us_high` | 正股最高价 |  | xla去前缀变体 |
| `us_low` | 正股最低价 |  | xla去前缀变体 |
| `us_open` | 正股开盘价 |  | xla去前缀变体 |
| `us_pctchange` | 正股涨跌幅 |  | xla去前缀变体 |
| `us_preclose` | 正股前收盘价,w_dq_us_preclose, |  | xla去前缀变体 |
| `us_swing` | 正股振幅 |  | xla去前缀变体 |
| `us_turn` | 正股换手率 |  | xla去前缀变体 |
| `us_volume` | 正股成交量 |  | xla去前缀变体 |
| `useasprojcap` | 专项债用作项目资本金 |  | xla去前缀变体 |
| `ussharename` | 同公司美股简称 |  | xla去前缀变体 |
| `ussharewindcode` | 同公司美股Wind代码 |  | xla去前缀变体 |
| `valueatrisk_historical` | 历史VaR | StartDate、EndDate | xla去前缀变体 |
| `valueatrisk_param` | 参数VaR | StartDate、EndDate | xla去前缀变体 |
| `vega_exch` | Vega(交易所) | TRADEDATE | xla去前缀变体 |
| `vhf` | VHF纵横指标 |  | xla原码 |
| `vic` | 经办评估人员 |  | xla去前缀变体 |
| `vieornot` | 是否VIE结构 |  | xla去前缀变体 |
| `vma` | VMA量简单移动平均 |  | xla原码 |
| `vmacd` | VMACD量指数平滑异同平均 |  | xla原码 |
| `vobp_cnbd` | 加权平均结算价基点价值 | TRADEDATE | xla原码 |
| `vobp_shc` | 估价基点价值(上海清算所) |  | xla去前缀变体 |
| `volatilityratio` | 历史波动率 | TRADEDATE | xla去前缀变体 |
| `volume` | 成交量 |  | 探测法实测 |
| `volume_aht` | 盘后成交量 | TRADEDATE | xla去前缀变体 |
| `volume_btin` | 成交量(含大宗交易) | TRADEDATE | xla去前缀变体 |
| `volume_fixedincome` | 上证固收平台成交量 | TRADEDATE | xla去前缀变体 |
| `volumeratio` | 量比 |  | xla原码 |
| `vosc` | VOSC成交量震荡 |  | xla原码 |
| `vote` | 是否存在投票权差异 | TRADEDATE | xla去前缀变体 |
| `vstd` | VSTD成交量标准差 |  | xla原码 |
| `vwap` | 均价VWAP |  | 探测法实测 |
| `website` | 公司网站 |  | xla去前缀变体 |
| `weightedrt` | 加权剩余期限(年）(新增) |  | xla去前缀变体 |
| `weightedrt2` | 加权剩余期限(按本金) | TRADEDATE | xla去前缀变体 |
| `whethertoresell` | 是否转售 |  | xla去前缀变体 |
| `wicscode2024` | 所属Wind行业代码(2023) ,s_info_wicscode2023 | TRADEDATE、TYPE | xla去前缀变体 |
| `wicsname2024` | 所属Wind行业名称(2023) ,s_info_wicsname2023 | TRADEDATE、TYPE | xla去前缀变体 |
| `win_ratio` | 区间胜率 | StartDate、EndDate、CalcTerm、Underlying_Index | xla去前缀变体 |
| `win_ratiofixed` | 区间胜率(基于固定收益率计算) | StartDate、EndDate、CalcTerm、YIELD | xla去前缀变体 |
| `windcode` | Wind代码 |  | 探测法实测 |
| `windl1type` | Wind债券一级分类,B_info_WindL1type(新增) |  | xla去前缀变体 |
| `windl1type_1st` | Wind债券一级分类(2025) |  | xla去前缀变体 |
| `windl2type` | Wind债券二级分类,B_info_WindL2type(新增) |  | xla去前缀变体 |
| `windl2type_1st` | Wind债券二级分类(2025) |  | xla去前缀变体 |
| `windrating_report` | 期货品种观点Wind评分 | TRADEDATE | xla去前缀变体 |
| `windtype` | 指数分类(Wind) |  | xla去前缀变体 |
| `withdrawaldescription` | 撤标情况说明 |  | xla去前缀变体 |
| `workingcapital` | 营运资本 | REPORTDATE | xla去前缀变体 |
| `workingcapitaltoassets` | 营运资本／总资产 | REPORTDATE | xla去前缀变体 |
| `wpipreleasingdateup` | IPO申报预披露更新日 |  | xla去前缀变体 |
| `wq_amount` | 周成交金额(新增) |  | xla去前缀变体 |
| `wq_high` | 周最高价(新增) |  | xla去前缀变体 |
| `wq_low` | 周最低价(新增) |  | xla去前缀变体 |
| `wq_pctchange` | 周涨跌幅(新增) |  | xla去前缀变体 |
| `wq_turn` | 周换手率(新增) |  | xla去前缀变体 |
| `wq_volume` | 周成交量(新增) |  | xla去前缀变体 |
| `wr` | WR威廉指标 |  | xla原码 |
| `wrating_downgrade` | 一月内评级调低家数 | DATE、PERIOD | xla去前缀变体 |
| `wrating_instnum` | 评级机构家数 | DATE | xla去前缀变体 |
| `wrating_maintain` | 一月内评级维持家数 | DATE、PERIOD | xla去前缀变体 |
| `wrating_numofbuy` | 评级买入家数 | DATE | xla去前缀变体 |
| `wrating_numofhold` | 评级中性家数 | DATE | xla去前缀变体 |
| `wrating_numofoutperform` | 评级增持家数 | DATE | xla去前缀变体 |
| `wrating_numofsell` | 评级卖出家数 | DATE | xla去前缀变体 |
| `wrating_numofunderperform` | 评级减持家数 | DATE | xla去前缀变体 |
| `wrating_targetprice` | 一致预测目标价 | TRADEDATE | xla去前缀变体 |
| `wrating_upgrade` | 一月内评级调高家数 | DATE、PERIOD | xla去前缀变体 |
| `wvad` | WVAD威廉变异离散量 |  | xla原码 |
| `xq_accmcomments` | 累计讨论次数_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_accmfocus` | 累计关注人数_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_accmshares` | 累计交易分享数_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_commentsadded` | 一周新增讨论数_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_focusadded` | 一周新增关注_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_sharesadded` | 一周新增交易分享数_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_wow_comments` | 一周讨论增长率_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_wow_focus` | 一周关注增长率_雪球 | TRADEDATE | xla去前缀变体 |
| `xq_wow_shares` | 一周交易分享增长率_雪球 | TRADEDATE | xla去前缀变体 |
| `yccode` | 默认收益率曲线代码 |  | xla原码 |
| `yoy_assets` | 总资产同比 |  | 探测法实测 |
| `yoy_cash` | 货币资金增长率 | REPORTDATE | xla去前缀变体 |
| `yoy_equity` | 净资产同比 |  | 探测法实测 |
| `yoy_fixedassets` | 固定资产投资扩张率 | REPORTDATE | xla去前缀变体 |
| `yoy_or` | 营业收入同比 |  | 探测法实测 |
| `yoy_tr` | 营业总收入同比 |  | 探测法实测 |
| `yoyassets` | 总资产(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoybps` | 每股净资产 ％ | REPORTDATE | xla去前缀变体 |
| `yoycf` | 现金净流量(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoydebt` | 总负债(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoyebt` | 利润总额 ％ | REPORTDATE | xla去前缀变体 |
| `yoyeps_basic` | EPS同比 |  | 探测法实测 |
| `yoyeps_diluted` | 稀释每股收益 ％ | REPORTDATE | xla去前缀变体 |
| `yoyequity` | 净资产(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoyfcf` | 筹资活动产生的现金流量净额(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoyicf` | 投资活动产生的现金流量净额(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoynetprofit` | 归母净利润同比 |  | 探测法实测 |
| `yoynetprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益 ％ | REPORTDATE | xla去前缀变体 |
| `yoyocf` | 经营活动产生的现金流量净额 ％ | REPORTDATE | xla去前缀变体 |
| `yoyocfps` | 每股经营活动产生的现金流量净额 ％ | REPORTDATE | xla去前缀变体 |
| `yoyop` | 营业利润同比 |  | 探测法实测 |
| `yoyop2` | 营业利润(同比增长率) | REPORTDATE | xla去前缀变体 |
| `yoyprofit` | 净利润同比 |  | 探测法实测 |
| `yoyroe` | ROE同比(增减) |  | 探测法实测 |
| `yq_amount` | 年成交金额(新增) |  | xla去前缀变体 |
| `yq_pctchange` | 年涨跌幅(新增) |  | xla去前缀变体 |
| `yq_turn` | 年换手率(新增) |  | xla去前缀变体 |
| `yq_volume` | 年成交量(新增) |  | xla去前缀变体 |
| `ytc` | 赎回收益率 |  | xla去前缀变体 |
| `ytm_b` | 到期收益率 |  | 探测法实测 |
| `ytm_cbr` | 到期收益率(中债资信) | TRADEDATE | xla去前缀变体 |
| `ytm_ifexe` | 行权收益率 | TRADEDATE | xla去前缀变体 |
| `ytp` | 回售收益率 |  | xla去前缀变体 |
| `zipcode` | 邮编 |  | xla去前缀变体 |
| `zjtxitselfornot` | 是否企业本身为专精特新 |  | xla去前缀变体 |
| `zjtxitselfornot1` | 是否企业本身为专精特新(支持历史) | TRADEDATE | xla去前缀变体 |
| `zjtxornot` | 是否专精特新企业 |  | xla去前缀变体 |
| `zjtxornot1` | 是否专精特新企业(支持历史) | TRADEDATE | xla去前缀变体 |
