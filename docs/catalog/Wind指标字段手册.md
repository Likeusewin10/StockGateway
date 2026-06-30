# 万得 Wind 字段手册（全量）

> 共 **9689 个字段**,从 Wind 金融终端 Excel 插件 `WindFunc.xla`(函数向导)解析提取(OLE2 复合文档 → MS-OVBA 解压 VBA 源码 → 按 `'中文名,字段代码` + Function 签名抽取)。对标 EM(1.85万)/iFinD(2.29万),为 Wind 字段的全量级字典。

> 🔴 **命名口径(必读)**:本表字段代码是 **Excel 插件口径**(带品种/类别前缀,如 `s_dq_close`/`s_val_pe`/`s_fa_roe_ttm`)。**WindPy(`/wind/wsd`、`/wind/wss`)用的是另一套更短的命名**(如 `close`/`pe`/`roe_ttm`),二者指向同一底层指标但**不能混用**。经实测,多数 WindPy 名 ≈ 本表代码**去掉品种/类别前缀**(`s_dq_close`→`close`、`s_fa_roe_ttm`→`roe_ttm`),但**非 100% 规则**(如 `s_dq_mv` 的 WindPy 名不是 `mv`)。**直接用于 `/wind/wss` 前请以探测子集 `docs/catalog/wind/probed_fields.csv`(130 个已实测 WindPy 名)为准**,或用本表代码查中文名/找指标、再去 WindPy 验证短名。

> 「参数」列为该字段在 `options`/调用里可带的设置项(如报告期 `rptDate`/`year`、币种等)。来源:`DataBrowse/XLA/WindFunc.xla`;提取脚本 `scripts/catalog/extract_wind_xla.py`。


## 总览

| 分类 | 字段数 | 跳转 |
|---|---|---|
| 证券(股票/通用) | 4326 | [↓](#分类-证券股票-通用) |
| 基金 | 1798 | [↓](#分类-基金) |
| 债券 | 839 | [↓](#分类-债券) |
| 可转债 | 243 | [↓](#分类-可转债) |
| 港股 | 734 | [↓](#分类-港股) |
| 台股 | 665 | [↓](#分类-台股) |
| 通用/指数 | 534 | [↓](#分类-通用-指数) |
| 基金(专项) | 196 | [↓](#分类-基金专项) |
| 指数 | 90 | [↓](#分类-指数) |
| 期货 | 43 | [↓](#分类-期货) |
| 财务分析 | 42 | [↓](#分类-财务分析) |
| 历史行情 | 17 | [↓](#分类-历史行情) |
| 融资融券 | 8 | [↓](#分类-融资融券) |
| 单季财务 | 6 | [↓](#分类-单季财务) |
| 技术指标/其他 | 148 | [↓](#分类-技术指标-其他) |

**合计 9689 个字段,15 个分类。**


<a id="分类-证券股票-通用"></a>

## 证券(股票/通用)（4326 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `s_abnormaltrade_netbuy` | 龙虎榜净买入额 | TRADEDATE |
| `s_anal_basis` | 基差(商品期货) | TRADEDATE |
| `s_anal_basisannualyield` | 基差年化收益率(商品期货) |  |
| `s_anal_basispercent` | 基差率(商品期货) | TRADEDATE |
| `s_anal_volatilityratio` | 历史波动率 | TRADEDATE |
| `s_bs_crcassets` | 分出再保险合同资产 | YEARBASIS、REPORTDATE、TYPE |
| `s_bs_crcliab` | 分出再保险合同负债 | YEARBASIS、REPORTDATE、TYPE |
| `s_bs_fininv` | 金融投资 | YEARBASIS、REPORTDATE、TYPE |
| `s_bs_ra` | 受限资产 | YEARBASIS、REPORTDATE、TYPE |
| `s_bs_rf` | 受限资金 | YEARBASIS、REPORTDATE、TYPE |
| `s_cac_illegalityamount` | 区间违规处罚金额 | StartDate、DATE |
| `s_cac_illegalitynum` | 区间违规处罚次数 | StartDate、DATE |
| `s_cac_lawsuitamount` | 区间诉讼涉案金额 | StartDate、DATE |
| `s_cac_lawsuitnum` | 区间诉讼次数 | StartDate、DATE |
| `s_cac_repoamt` | 区间回购金额 | StartDate、DATE |
| `s_cac_repocshares` | 区间回购股份注销数量 | StartDate、DATE |
| `s_cac_reposhares` | 区间回购数量 | StartDate、DATE |
| `s_cal_date` | 日期计算函数，根据原始日期、数值和间隔来计算，Type_ 0，1，2分别对应计算出的当日，初和末 | ADate、N、PERIOD、TYPE |
| `s_cb_carrydate` | 转债起息日期 |  |
| `s_cb_code` | 转债代码 |  |
| `s_cb_code2` | 交债代码 |  |
| `s_cb_creditrating` | 转债发行信用等级 |  |
| `s_cb_interest` | 转债利率 | TRADEDATE |
| `s_cb_interestfrequency` | 转债年付息次数 |  |
| `s_cb_interesttype` | 转债利率类型 |  |
| `s_cb_issueamount` | 转债发行总额 |  |
| `s_cb_issueprice` | 转债发行价格 |  |
| `s_cb_list_annocedate` | 转债发行结果公告日 |  |
| `s_cb_list_announcedate` | 转债发行公告日期 |  |
| `s_cb_list_dateinstoff` | 转债网下向机构投资者发行日期 |  |
| `s_cb_list_dtonl` | 转债网上发行日期 |  |
| `s_cb_list_permitdate` | 转债发审委审批通过日期 |  |
| `s_cb_list_rationchkindate` | 转债老股东配售股权登记日 |  |
| `s_cb_list_rationdate` | 转债老股东配售日期 |  |
| `s_cb_list_rationpaymtdate` | 转债老股东配售缴款日 |  |
| `s_cb_maturitydate` | 转债到期日期 |  |
| `s_cb_name` | 转债简称 |  |
| `s_cb_par` | 转债面值 |  |
| `s_cb_tblist_permitdate` | 待发行可转债发审委审批通过日期 |  |
| `s_cb_term` | 转债发行期限 |  |
| `s_close_auction_amount` | 收盘集合竞价成交额 | TRADEDATE |
| `s_close_auction_price` | 收盘集合竞价成交价 | TRADEDATE |
| `s_close_auction_volume` | 收盘集合竞价成交量 | TRADEDATE |
| `s_collection_total` | 募资总额 |  |
| `s_collection_unused` | 募资未投入资金总额 |  |
| `s_contract_issuedate` | 标准合约上市日 |  |
| `s_controller_pct` | 实际控制人持股比例 | DEALDATE |
| `s_credit_formerline` | 历史授信额度 | TRADEDATE |
| `s_credit_line` | 最新授信额度 |  |
| `s_credit_linedate` | 最新授信日期 |  |
| `s_credit_lineunused` | 最新未使用授信额度 |  |
| `s_credit_lineused` | 最新已使用授信额度 |  |
| `s_credit_lineused2` | 历史已使用授信额度 | TRADEDATE |
| `s_cs_cashpaidclaim` | 支付签发保险合同赔款的现金 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_cs_cashrecprem` | 收到签发保险合同保费取得的现金 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_cs_ntcashpaidcrc` | 支付分出再保险合同的现金净额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_cs_ntcashrecced` | 收到分入再保险合同的现金净额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_cs_ntincloanpled` | 保单质押贷款净增加额 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_div_adjcash` | 除权每股现金分红 | StartDate、DATE |
| `s_div_adjfactor` | 阶段拆细系数 | StartDate、DATE |
| `s_div_aualaccmdiv` | 年度累计分红总额(新增) |  |
| `s_div_aualaccmdiv2` | 区间现金分红总额 | StartDate、DATE、CURTYPE |
| `s_div_aualaccmdiv_ard` | 年度累计分红总额(已宣告) |  |
| `s_div_aualaccmdiv_ex` | 年度累计分红总额(已宣告,剔除特别派息) | Year |
| `s_div_aualaccmdivcpy` | 公司区间现金分红总额 | StartDate、DATE |
| `s_div_aualaccmdivpershare` | 年度累计单位分红(新增) |  |
| `s_div_aualcashdividend` | 年度现金分红总额 |  |
| `s_div_capitalization` | 每股转增股本 | REPORTDATE |
| `s_div_capitalization2` | 每股转增股本(已宣告) | REPORTDATE |
| `s_div_cashaftertax` | 每股股利(税后) | REPORTDATE |
| `s_div_cashaftertax2` | 每股股利(税后)(已宣告) | REPORTDATE |
| `s_div_cashandstock` | 每股分红送转 | REPORTDATE |
| `s_div_cashbeforetax` | 每股股利(税前) | REPORTDATE |
| `s_div_cashbeforetax2` | 每股股利(税前)(已宣告) | REPORTDATE |
| `s_div_cashdivbb` | 年度累计分红总额(已宣告,含回购) | Year |
| `s_div_cashpaidaftertax` | 区间每股股利(税后) | StartDate、EndDate |
| `s_div_cashpaidbeforetax` | 区间每股股利(税前) | StartDate、EndDate |
| `s_div_cashpaidbeforetax1` | 区间每股股利(税前) | StartDate、DATE、TYPE、OptionParameters |
| `s_div_dividendratio` | 现金分红比例 |  |
| `s_div_divpct_3yaccubb` | 三年累计分红占比(含回购) | Year |
| `s_div_divpct_3yearaccu` | 三年累计分红占比(再融资条件)(新增) |  |
| `s_div_divpct_accu` | 上市以来分红率 | REPORTDATE |
| `s_div_exdate` | 除权除息日 | REPORTDATE |
| `s_div_firstyear` | 上市后首次分红年份 |  |
| `s_div_fstdiscdate` | 现金分红首次披露日 | REPORTDATE |
| `s_div_ifdiv` | 是否分红(新增) | D |
| `s_div_impdate` | 分红实施公告日(新增) | D |
| `s_div_lasttrddateshareb` | B股最后交易日(新增) | D |
| `s_div_object` | 分红对象(新增) | D |
| `s_div_paydate` | 派息日 | REPORTDATE |
| `s_div_payoutratio` | 年度现金分红比例 | Year |
| `s_div_payoutratio_ex` | 年度现金分红比例(已宣告,剔除特别派息) | Year |
| `s_div_predisclosuredate` | 预披露公告日 | REPORTDATE |
| `s_div_prelandate` | 预案公告日(新增) | D |
| `s_div_progress` | 分红方案进度 | REPORTDATE |
| `s_div_ratiocs` | 普通股股东年度现金分红比例 | Year |
| `s_div_ratiocsa` | 普通股股东年度现金分红比例(公告) | Year |
| `s_div_ratiocsd` | 普通股股东年度现金分红比例(已宣告) | Year |
| `s_div_ratiocsd_ex` | 普通股股东年度现金分红比例(已宣告,剔除特别派息) | Year |
| `s_div_recdateshareb` | B股股权登记日(新增) | D |
| `s_div_recorddate` | 股权登记日 | REPORTDATE |
| `s_div_shares` | 分红基准股本 | REPORTDATE |
| `s_div_smtgdate` | 股东大会公告日(新增) | D |
| `s_div_stock` | 每股红股 | REPORTDATE |
| `s_div_stock2` | 每股红股(已宣告) | REPORTDATE |
| `s_div_trddateshareb` | 红股上市交易日(新增) | D |
| `s_dq_adjfactor2` | 复权因子 |  |
| `s_dq_amount` | 成交额 |  |
| `s_dq_amount_aht` | 盘后成交额 | TRADEDATE |
| `s_dq_amount_btin` | 成交额(含大宗交易) | TRADEDATE |
| `s_dq_amount_fixedincome` | 上证固收平台成交金额 | TRADEDATE、PRICETYPE |
| `s_dq_amtturnover` | 换手率(基准.流通市值) | TRADEDATE |
| `s_dq_avgprice` | 成交均价 |  |
| `s_dq_avgprice_fixedincome` | 上证固收平台平均价 | TRADEDATE、PRICETYPE |
| `s_dq_callamount` | 认购成交额 | TRADEDATE |
| `s_dq_calloi` | 认购持仓量 | TRADEDATE |
| `s_dq_callvolume` | 认购成交量 | TRADEDATE |
| `s_dq_change` | 涨跌 |  |
| `s_dq_change_settlement` | 涨跌（结算价） |  |
| `s_dq_close` | 收盘价 |  |
| `s_dq_close2` | 定点复权 | TRADEDATE、TYPE、ADJDATE |
| `s_dq_close_fixedincome` | 上证固收平台收盘价 | TRADEDATE、PRICETYPE |
| `s_dq_close_lastradeday` | 最近交易日期 |  |
| `s_dq_close_night` | 收盘价(夜盘) | TRADEDATE |
| `s_dq_close_usd` | 收盘价(美元) | TRADEDATE |
| `s_dq_dealnum` | 成交笔数 |  |
| `s_dq_dealnum_fixedincome` | 上证固收平台成交笔数 | TRADEDATE |
| `s_dq_direction` | 交收方向(黄金现货) | TRADEDATE |
| `s_dq_freeturnover` | 换手率（基准.自由流通股本）(新增) |  |
| `s_dq_freeturnover_n` | 换手率(基准.自由流通股本) | TRADEDATE |
| `s_dq_high` | 最高价 |  |
| `s_dq_lastradeday_ssefi` | 上证固收平台最近交易日 | TRADEDATE |
| `s_dq_low` | 最低价 |  |
| `s_dq_maxdown` | 跌停价 | TRADEDATE |
| `s_dq_maxup` | 涨停价 | TRADEDATE |
| `s_dq_maxupordown` | 涨跌停状态 | TRADEDATE |
| `s_dq_oi` | 持仓量 |  |
| `s_dq_oiamount` | 持仓额 | TRADEDATE |
| `s_dq_oiamount_nomargin` | 持仓额(不计保证金) | TRADEDATE |
| `s_dq_oichange` | 持仓量变化 |  |
| `s_dq_open` | 开盘价 |  |
| `s_dq_optionamount` | 品种成交额 | TRADEDATE |
| `s_dq_optionoi` | 品种持仓量 | TRADEDATE |
| `s_dq_optionvolume` | 品种成交量 | TRADEDATE |
| `s_dq_pctchange` | 涨跌幅 |  |
| `s_dq_pctchange_close` | 涨跌幅(收盘价) | TRADEDATE |
| `s_dq_pctchange_settlement` | 涨跌幅（结算价） |  |
| `s_dq_preclose` | 前收盘价 |  |
| `s_dq_preclose_exch` | 交易所前收盘价 | TRADEDATE |
| `s_dq_premiumrate_ah` | AH股溢价率 | TRADEDATE |
| `s_dq_presettle` | 前结算价 |  |
| `s_dq_putamount` | 认沽成交额 | TRADEDATE |
| `s_dq_putoi` | 认沽持仓量 | TRADEDATE |
| `s_dq_putvolume` | 认沽成交量 | TRADEDATE |
| `s_dq_relipochange` | 相对发行价涨跌(新增) |  |
| `s_dq_relipopctchange` | 相对发行价涨跌幅(新增) |  |
| `s_dq_rps` | 相对强度指标 | TRADEDATE |
| `s_dq_settle` | 结算价 |  |
| `s_dq_suspenddays` | 连续停牌天数 | TRADEDATE |
| `s_dq_suspendreason` | 停牌原因(新增) |  |
| `s_dq_swing` | 振幅(新增) |  |
| `s_dq_tradestatus` | 交易状态(新增) |  |
| `s_dq_turn` | 换手率 |  |
| `s_dq_volume` | 成交量 |  |
| `s_dq_volume_aht` | 盘后成交量 | TRADEDATE |
| `s_dq_volume_btin` | 成交量(含大宗交易) | TRADEDATE |
| `s_dq_volume_fixedincome` | 上证固收平台成交量 | TRADEDATE |
| `s_employee_admin` | 综合管理人员人数 | TRADEDATE |
| `s_employee_admin_pct` | 综合管理人员人数占比 | TRADEDATE |
| `s_employee_ba` | 本科人数 | TRADEDATE |
| `s_employee_ba_pct` | 本科人数占比 | TRADEDATE |
| `s_employee_board` | 董事会人数 | TRADEDATE |
| `s_employee_coll` | 专科人数 | TRADEDATE |
| `s_employee_coll_pct` | 专科人数占比 | TRADEDATE |
| `s_employee_excu` | 行政人员人数 | TRADEDATE |
| `s_employee_excu_pct` | 行政人员人数占比 | TRADEDATE |
| `s_employee_executivedirector` | 执行董事人数 | TRADEDATE |
| `s_employee_f` | 女性员工人数 | TRADEDATE |
| `s_employee_fin` | 财务人员人数 | TRADEDATE |
| `s_employee_fin_pct` | 财务人员人数占比 | TRADEDATE |
| `s_employee_highschool` | 高中及以下人数 | TRADEDATE |
| `s_employee_highschool_pct` | 高中及以下人数占比 | TRADEDATE |
| `s_employee_hr` | 人事人员人数 | TRADEDATE |
| `s_employee_hr_pct` | 人事人员人数占比 | TRADEDATE |
| `s_employee_indpdirector` | 独立董事人数 | TRADEDATE |
| `s_employee_m` | 男性员工人数 | TRADEDATE |
| `s_employee_mgmt` | 高管人数 | TRADEDATE |
| `s_employee_ms` | 硕士人数 | TRADEDATE |
| `s_employee_ms_pct` | 硕士人数占比 | TRADEDATE |
| `s_employee_othdegree` | 其他学历人数 | TRADEDATE |
| `s_employee_othdegree_pct` | 其他学历人数占比 | TRADEDATE |
| `s_employee_othdept` | 其他人员人数 | TRADEDATE |
| `s_employee_othdept_pct` | 其他专业人员人数占比 | TRADEDATE |
| `s_employee_phd` | 博士人数 | TRADEDATE |
| `s_employee_phd_pct` | 博士人数占比 | TRADEDATE |
| `s_employee_producer` | 生产人员人数 | TRADEDATE |
| `s_employee_producer_pct` | 生产人员人数占比 | TRADEDATE |
| `s_employee_pur` | 采购仓储人员人数 | TRADEDATE |
| `s_employee_pur_pct` | 采购仓储人员人数占比 | TRADEDATE |
| `s_employee_rc` | 风控稽核人员人数 | TRADEDATE |
| `s_employee_rc_pct` | 风控稽核人员人数占比 | TRADEDATE |
| `s_employee_sale` | 销售人员人数 | TRADEDATE |
| `s_employee_sale_pct` | 销售人员人数占比 | TRADEDATE |
| `s_employee_server` | 客服人员人数 | TRADEDATE |
| `s_employee_server_pct` | 客服人员人数占比 | TRADEDATE |
| `s_employee_tech` | 技术人员人数 | TRADEDATE |
| `s_employee_tech_pct` | 技术人员人数占比 | TRADEDATE |
| `s_employee_techcore` | 核心技术人员人数 | TRADEDATE |
| `s_employee_totalmgmt` | 管理层人数 | TRADEDATE |
| `s_err_wi` | 盈利修正比例(可选类型) |  |
| `s_esg_cr_wind` | 确定性等级 | REPORTDATE |
| `s_esg_eem01001` | SCOPE 1 温室气体排放 | REPORTDATE |
| `s_esg_eem01002` | SCOPE 2 温室气体排放 | REPORTDATE |
| `s_esg_eem01004` | 总温室气体排放 | REPORTDATE |
| `s_esg_eem01008` | 温室气体减排量 | REPORTDATE |
| `s_esg_eem01011` | 是否就气候变化机会进行讨论 | REPORTDATE |
| `s_esg_eem01012` | 是否就气候变化风险进行讨论 | REPORTDATE |
| `s_esg_eem02001` | 氮氧化物排放 | REPORTDATE |
| `s_esg_eem02002` | 二氧化硫排放 | REPORTDATE |
| `s_esg_eem02003` | 悬浮粒子/颗粒物 | REPORTDATE |
| `s_esg_eem03001` | 有害废弃物量 | REPORTDATE |
| `s_esg_eem03002` | 无害废弃物量 | REPORTDATE |
| `s_esg_eem03003` | 废弃物总量 | REPORTDATE |
| `s_esg_eem03004` | 废弃物回收量 | REPORTDATE |
| `s_esg_em_wind` | 计算方法 | REPORTDATE |
| `s_esg_eot01003` | 是否重点排污单位 | REPORTDATE |
| `s_esg_eot02002` | 环保超标或其他违规次数 | REPORTDATE |
| `s_esg_ere01001` | 总能源消耗 | REPORTDATE |
| `s_esg_ere01002` | 耗电总量 | REPORTDATE |
| `s_esg_ere01003` | 节省用电量 | REPORTDATE |
| `s_esg_ere01004` | 煤碳使用量 | REPORTDATE |
| `s_esg_ere01005` | 天然气消耗 | REPORTDATE |
| `s_esg_ere01006` | 燃油消耗 | REPORTDATE |
| `s_esg_ere01007` | 节能量 | REPORTDATE |
| `s_esg_ere02001` | 纸消耗量 | REPORTDATE |
| `s_esg_ere02002` | 废纸回收量 | REPORTDATE |
| `s_esg_escore_wind` | 环境维度得分 | TRADEDATE |
| `s_esg_eventscore_wind` | ESG争议事件得分 | TRADEDATE |
| `s_esg_ewa01001` | 总用水量 | REPORTDATE |
| `s_esg_ewa01002` | 节省水量 | REPORTDATE |
| `s_esg_ewa01003` | 水循环与再利用的总量 | REPORTDATE |
| `s_esg_ewa01004` | 废水综合利用率 | REPORTDATE |
| `s_esg_ewa02002` | 废水/污水排放量 | REPORTDATE |
| `s_esg_ewa02003` | 废水处理量 | REPORTDATE |
| `s_esg_ewa02004` | 氨氮 | REPORTDATE |
| `s_esg_ewa02005` | 化学需氧量(COD) | REPORTDATE |
| `s_esg_gad01001` | 审计委员会会议次数 | REPORTDATE |
| `s_esg_gad01002` | 审计委员会会议出席率 | REPORTDATE |
| `s_esg_gad02002` | 是否出具标准无保留意见 | REPORTDATE |
| `s_esg_gbo01001` | 董事会规模 | REPORTDATE |
| `s_esg_gbo01002` | 董事会出席率 | REPORTDATE |
| `s_esg_gbo01003` | 董事会召开数 | REPORTDATE |
| `s_esg_gbo01004` | 参加少于75%会议的董事人数 | REPORTDATE |
| `s_esg_gbo01005` | 监事会召开数 | REPORTDATE |
| `s_esg_gbo01006` | 监事出席率 | REPORTDATE |
| `s_esg_gbo01007` | 是否设有监事委员会主席 | REPORTDATE |
| `s_esg_gbo01008` | 提名委员会会议数 | REPORTDATE |
| `s_esg_gbo01010` | 提名委员会会议出席率 | REPORTDATE |
| `s_esg_gbo01014` | 董事会成员受教育背景高于本科的比例 | REPORTDATE |
| `s_esg_gbo01015` | 女性董事占比 | REPORTDATE |
| `s_esg_gbo03001` | 独立董事董事会会议出席率 | REPORTDATE |
| `s_esg_gbo03002` | 独立董事占董事会总人数的比例 | REPORTDATE |
| `s_esg_gcb_wind` | 绿色信贷余额 | Year |
| `s_esg_gcbtd_wind` | 绿色信贷余额 | REPORTDATE |
| `s_esg_ghg12_wind` | 温室气体排放总量(范围1和范围2) | REPORTDATE |
| `s_esg_ghg1_wind` | 直接(范围1)温室气体排放 | REPORTDATE |
| `s_esg_ghg2_wind` | 能源间接(范围2)温室气体排放 | REPORTDATE |
| `s_esg_ghgr12_wind` | 每百万元营收温室气体排放量(范围1和范围2) | REPORTDATE |
| `s_esg_ghgr1_wind` | 每百万元营收直接(范围1)温室气体排放 | REPORTDATE |
| `s_esg_ghgr2_wind` | 每百万元营收间接温室气体排放(范围2) | REPORTDATE |
| `s_esg_gpa02001` | 是否有股权激励计划 | REPORTDATE |
| `s_esg_gpa03002` | 薪酬委员会会议出席率 | REPORTDATE |
| `s_esg_gpa03003` | 薪酬委员会会议数 | REPORTDATE |
| `s_esg_gscore_wind` | 治理维度得分 | TRADEDATE |
| `s_esg_mdc01002` | 公司是否有独立的公司社会责任报告 | REPORTDATE |
| `s_esg_mdc01003` | 第三方审查机构 | REPORTDATE |
| `s_esg_mdc01004` | 报告范围 | REPORTDATE |
| `s_esg_mdc01005` | 编制依据 | REPORTDATE |
| `s_esg_mdc01006` | 是否遵循/对照GRI标准 | REPORTDATE |
| `s_esg_mdc01007` | 是否遵循/对照联交所标准 | REPORTDATE |
| `s_esg_mgmtscore_wind` | ESG管理实践得分 | TRADEDATE |
| `s_esg_pplb_wind` | 普惠型小微企业贷款余额 | REPORTDATE |
| `s_esg_rating` | ESG评级 | TRADEDATE |
| `s_esg_rating_casvi` | 社会价值投资联盟ESG评级 | TRADEDATE |
| `s_esg_rating_ftserussell` | 富时罗素ESG评分 | TRADEDATE |
| `s_esg_rating_ssi` | 华证ESG评级 | TRADEDATE |
| `s_esg_rating_wind` | Wind ESG评级 | TRADEDATE |
| `s_esg_ratingdate_wind` | Wind ESG评级日期 | TRADEDATE |
| `s_esg_reptdate_wind` | ESG独立报告发布日期 | REPORTDATE |
| `s_esg_rpt_wind` | ESG独立报告名称 | REPORTDATE |
| `s_esg_sch01001` | 供应商数量 | REPORTDATE |
| `s_esg_sch01002` | 供应商本地化比例 | REPORTDATE |
| `s_esg_sch02001` | 本地化采购支出占比 | REPORTDATE |
| `s_esg_sch02002` | 接受ESG评估的供应商数量 | REPORTDATE |
| `s_esg_sco02001` | 志愿服务时长 | REPORTDATE |
| `s_esg_sco02002` | 注册志愿者人数 | REPORTDATE |
| `s_esg_score_wind` | Wind ESG综合得分 | TRADEDATE |
| `s_esg_sem01001` | 雇员总人数 | REPORTDATE |
| `s_esg_sem01002` | 员工流失率/离职率 | REPORTDATE |
| `s_esg_sem01003` | 兼职人员比例 | REPORTDATE |
| `s_esg_sem01004` | 劳动合同签订率 | REPORTDATE |
| `s_esg_sem01005` | 女性员工比例 | REPORTDATE |
| `s_esg_sem01006` | 少数裔员工比例 | REPORTDATE |
| `s_esg_sem02002` | 人均培训课时 | REPORTDATE |
| `s_esg_sem03001` | 工伤率 | REPORTDATE |
| `s_esg_sem03002` | 因工伤损失工作日数 | REPORTDATE |
| `s_esg_sem03003` | 职业病发生率 | REPORTDATE |
| `s_esg_sem03004` | 死亡事故数 | REPORTDATE |
| `s_esg_sem04001` | 医保覆盖率 | REPORTDATE |
| `s_esg_spc01001` | 客户投诉数量 | REPORTDATE |
| `s_esg_spc01002` | 客户满意度 | REPORTDATE |
| `s_esg_spc01003` | 是否有客户反馈系统 | REPORTDATE |
| `s_esg_spc02004` | 新增专利数 | REPORTDATE |
| `s_esg_sscore_wind` | 社会维度得分 | TRADEDATE |
| `s_est_avgbps` | 预测每股净资产(综合值) | RPTYEAR |
| `s_est_avgbps1` | 预测每股净资产(BPS)平均值 |  |
| `s_est_avgcps` | 预测每股现金流(综合值) | RPTYEAR |
| `s_est_avgcps1` | 预测每股现金流(CPS)平均值 |  |
| `s_est_avgdps` | 预测每股股利(综合值) | RPTYEAR |
| `s_est_avgdps1` | 预测每股股利(DPS)平均值 |  |
| `s_est_avgebit` | 预测息税前利润(综合值) | RPTYEAR |
| `s_est_avgebit1` | 预测息税前利润(EBIT)平均值 |  |
| `s_est_avgebitda` | 预测息税折旧摊销前利润(综合值) | RPTYEAR |
| `s_est_avgebitda1` | 预测息税折旧摊销前利润(EBITDA)平均值 |  |
| `s_est_avgebt` | 预测利润总额(综合值) | RPTYEAR |
| `s_est_avgebt1` | 预测利润总额平均值 |  |
| `s_est_avgoperatingprofit` | 预测营业利润(综合值) | RPTYEAR |
| `s_est_avgoperatingprofit1` | 预测营业利润平均值 |  |
| `s_est_avgroa` | 预测总资产收益率(综合值) | RPTYEAR |
| `s_est_avgroe` | 预测净资产收益率(综合值) | RPTYEAR |
| `s_est_cagr_np` | 未来3年净利润复合年增长率 |  |
| `s_est_cagr_sales` | 未来3年营业总收入复合年增长率 |  |
| `s_est_ebitda` | 机构预测EBITDA |  |
| `s_est_eps` | 预测每股收益(综合值) | RPTYEAR |
| `s_est_eps1` | 预测每股收益平均值 |  |
| `s_est_eps_inst` | 预测每股收益(明细值) | RPTYEAR |
| `s_est_eps_inst1` | 机构预测每股收益 |  |
| `s_est_estanalyst` | 预测研究员(新增) | RPTYEAR |
| `s_est_estnewtime_inst` | 机构最近预测时间(新增) | RPTYEAR |
| `s_est_event_date` | 大事日期(大事后预测) | DATE |
| `s_est_evtoebitda` | 机构预测EV/EBITDA |  |
| `s_est_frstratingtime_inst` | 机构首次评级时间(新增) |  |
| `s_est_highprice_inst` | 本次最低目标价 | EndDate |
| `s_est_highprice_inst1` | 本次最高目标价 | EndDate |
| `s_est_instnum` | 预测机构家数 | RPTYEAR |
| `s_est_lowprice_inst` | 本次最高目标价 | EndDate |
| `s_est_lowprice_inst1` | 本次最低目标价 | EndDate |
| `s_est_maxbps` | 预测每股净资产(最大值) | RPTYEAR |
| `s_est_maxbps1` | 预测每股净资产(BPS)最大值 |  |
| `s_est_maxcps` | 预测每股现金流(最大值) | RPTYEAR |
| `s_est_maxcps1` | 预测每股现金流(CPS)最大值 |  |
| `s_est_maxdps` | 预测每股股利(最大值) | RPTYEAR |
| `s_est_maxdps1` | 预测每股股利(DPS)最大值 |  |
| `s_est_maxebit` | 预测息税前利润(最大值) | RPTYEAR |
| `s_est_maxebit1` | 预测息税前利润(EBIT)最大值 |  |
| `s_est_maxebitda` | 预测息税折旧摊销前利润(最大值) | RPTYEAR |
| `s_est_maxebitda1` | 预测息税折旧摊销前利润(EBITDA)最大值 |  |
| `s_est_maxebt` | 预测利润总额(最大值) | RPTYEAR |
| `s_est_maxebt1` | 预测利润总额最大值 |  |
| `s_est_maxeps` | 预测每股收益(最大值) | RPTYEAR |
| `s_est_maxeps1` | 预测每股收益最大值 |  |
| `s_est_maxnetprofit` | 预测净利润(最大值) | RPTYEAR |
| `s_est_maxnetprofit1` | 预测净利润最大值 |  |
| `s_est_maxoperatingprofit` | 预测营业利润(最大值) | RPTYEAR |
| `s_est_maxoperatingprofit1` | 预测营业利润最大值 |  |
| `s_est_maxroa` | 预测总资产收益率(最大值) | RPTYEAR |
| `s_est_maxroe` | 预测净资产收益率(最大值) | RPTYEAR |
| `s_est_maxsales` | 预测主营业务收入(最大值) | RPTYEAR |
| `s_est_maxsales1` | 预测营业收入最大值 |  |
| `s_est_medianbps` | 预测每股净资产(中值) | RPTYEAR |
| `s_est_medianbps1` | 预测每股净资产(BPS)中值 |  |
| `s_est_mediancps` | 预测每股现金流(中值) | RPTYEAR |
| `s_est_mediancps1` | 预测每股现金流(CPS)中值 |  |
| `s_est_mediandps` | 预测每股股利(中值) | RPTYEAR |
| `s_est_mediandps1` | 预测每股股利(DPS)中值 |  |
| `s_est_medianebit` | 预测息税前利润(中值) | RPTYEAR |
| `s_est_medianebit1` | 预测息税前利润(EBIT)中值 |  |
| `s_est_medianebitda` | 预测息税折旧摊销前利润(中值) | RPTYEAR |
| `s_est_medianebitda1` | 预测息税折旧摊销前利润(EBITDA)中值 |  |
| `s_est_medianebt` | 预测利润总额(中值) | RPTYEAR |
| `s_est_medianebt1` | 预测利润总额中值 |  |
| `s_est_medianeps` | 预测每股收益(中值) | RPTYEAR |
| `s_est_medianeps1` | 预测每股收益中值 |  |
| `s_est_mediannetprofit` | 预测净利润(中值) | RPTYEAR |
| `s_est_mediannetprofit1` | 预测净利润中值 |  |
| `s_est_medianoperatingprofit` | 预测营业利润(中值) | RPTYEAR |
| `s_est_medianoperatingprofit1` | 预测营业利润中值 |  |
| `s_est_medianroa` | 预测总资产收益率(中值) | RPTYEAR |
| `s_est_medianroe` | 预测净资产收益率(中值) | RPTYEAR |
| `s_est_mediansales` | 预测主营业务收入(中值) | RPTYEAR |
| `s_est_mediansales1` | 预测营业收入中值 |  |
| `s_est_minbps` | 预测每股净资产(最小值) | RPTYEAR |
| `s_est_minbps1` | 预测每股净资产(BPS)最小值 |  |
| `s_est_mincps` | 预测每股现金流(最小值) | RPTYEAR |
| `s_est_mincps1` | 预测每股现金流(CPS)最小值 |  |
| `s_est_mindps` | 预测每股股利(最小值) | RPTYEAR |
| `s_est_mindps1` | 预测每股股利(DPS)最小值 |  |
| `s_est_minebit` | 预测息税前利润(最小值) | RPTYEAR |
| `s_est_minebit1` | 预测息税前利润(EBIT)最小值 |  |
| `s_est_minebitda` | 预测息税折旧摊销前利润(最小值) | RPTYEAR |
| `s_est_minebitda1` | 预测息税折旧摊销前利润(EBITDA)最小值 |  |
| `s_est_minebt` | 预测利润总额(最小值) | RPTYEAR |
| `s_est_minebt1` | 预测利润总额最小值 |  |
| `s_est_mineps` | 预测每股收益(最小值) | RPTYEAR |
| `s_est_mineps1` | 预测每股收益最小值 |  |
| `s_est_minnetprofit` | 预测净利润(最小值) | RPTYEAR |
| `s_est_minnetprofit1` | 预测净利润最小值 |  |
| `s_est_minoperatingprofit` | 预测营业利润(最小值) | RPTYEAR |
| `s_est_minoperatingprofit1` | 预测营业利润最小值 |  |
| `s_est_minroa` | 预测总资产收益率(最小值) | RPTYEAR |
| `s_est_minroe` | 预测净资产收益率(最小值) | RPTYEAR |
| `s_est_minsales` | 预测主营业务收入(最小值) | RPTYEAR |
| `s_est_minsales1` | 预测营业收入最小值 |  |
| `s_est_netprofit` | 预测净利润(综合值) | RPTYEAR |
| `s_est_netprofit1` | 预测净利润平均值 |  |
| `s_est_netprofit_downgrade` | 一月内净利润调低家数 | RPTYEAR |
| `s_est_netprofit_inst` | 预测净利润(明细值) | RPTYEAR |
| `s_est_netprofit_inst1` | 机构预测净利润 |  |
| `s_est_netprofit_maintain` | 一月内净利润维持家数 | RPTYEAR |
| `s_est_netprofit_upgrade` | 一月内净利润调高家数 | RPTYEAR |
| `s_est_newratingtime_inst` | 机构最近评级时间(新增) |  |
| `s_est_orgrating_inst` | 机构投资评级(原始)(新增) |  |
| `s_est_pctchange` | 预测涨跌幅(评级日,最低价) | TRADEDATE、TYPE |
| `s_est_prehighprice_inst` | 前次最低目标价 | EndDate |
| `s_est_prehighprice_inst1` | 前次最高目标价 | EndDate |
| `s_est_prelowprice_inst` | 前次最高目标价 | EndDate |
| `s_est_prelowprice_inst1` | 前次最低目标价 | EndDate |
| `s_est_ratinganalyst` | 评级研究员(新增) |  |
| `s_est_rptabstract_inst` | 内容 | EndDate |
| `s_est_rpttitle_inst` | 报告标题 | EndDate |
| `s_est_sales` | 预测主营业务收入(综合值) | RPTYEAR |
| `s_est_sales1` | 预测营业收入平均值 |  |
| `s_est_sales_downgrade` | 一月内主营业务收入调低家数 | RPTYEAR |
| `s_est_sales_inst` | 预测主营业务收入(明细值) | RPTYEAR |
| `s_est_sales_inst1` | 机构预测营业收入 |  |
| `s_est_sales_maintain` | 一月内主营业务收入维持家数 | RPTYEAR |
| `s_est_sales_upgrade` | 一月内主营业务收入调高家数 | RPTYEAR |
| `s_est_scorerating_inst` | 机构投资评级(标准化得分)(新增) |  |
| `s_est_stdbps` | 预测每股净资产(标准差) | RPTYEAR |
| `s_est_stdbps1` | 预测每股净资产(BPS)标准差 |  |
| `s_est_stdcps` | 预测每股现金流(标准差) | RPTYEAR |
| `s_est_stdcps1` | 预测每股现金流(CPS)标准差 |  |
| `s_est_stddps` | 预测每股股利(标准差) | RPTYEAR |
| `s_est_stddps1` | 预测每股股利(DPS)标准差 |  |
| `s_est_stdebit` | 预测息税前利润(标准差) | RPTYEAR |
| `s_est_stdebit1` | 预测息税前利润(EBIT)标准差 |  |
| `s_est_stdebitda` | 预测息税折旧摊销前利润(标准差) | RPTYEAR |
| `s_est_stdebitda1` | 预测息税折旧摊销前利润(EBITDA)标准差 |  |
| `s_est_stdebt` | 预测利润总额(标准差) | RPTYEAR |
| `s_est_stdebt1` | 预测利润总额标准差 |  |
| `s_est_stdeps` | 预测每股收益(标准差) | RPTYEAR |
| `s_est_stdeps1` | 预测每股收益标准差 |  |
| `s_est_stdnetprofit` | 预测净利润(标准差) | RPTYEAR |
| `s_est_stdnetprofit1` | 预测净利润标准差 |  |
| `s_est_stdoperatingprofit` | 预测营业利润(标准差) | RPTYEAR |
| `s_est_stdoperatingprofit1` | 预测营业利润标准差 |  |
| `s_est_stdrating_inst` | 机构投资评级(标准化评级)(新增) |  |
| `s_est_stdroa` | 预测总资产收益率(标准差) | RPTYEAR |
| `s_est_stdroe` | 预测净资产收益率(标准差) | RPTYEAR |
| `s_est_stdsales` | 预测主营业务收入(标准差) | RPTYEAR |
| `s_est_stdsales1` | 预测营业收入标准差 |  |
| `s_est_yoynetprofit` | 预测净利润增长率 | RPTYEAR |
| `s_est_yoysales` | 预测主营业务收入增长率 | RPTYEAR |
| `s_estimated_netcollection` | 增发预计募集资金 |  |
| `s_fa_abpturndays` | 应付账款及应付票据周转天数 | REPORTDATE |
| `s_fa_abrturndays` | 应收账款及应收票据周转天数 | REPORTDATE |
| `s_fa_admexptogr2` | 管理费用/营业总收入(不含研发费用) | REPORTDATE |
| `s_fa_adminexpense_ttm` | 管理费用(TTM) |  |
| `s_fa_adminexpense_ttm2` | 管理费用(TTM) | REPORTDATE |
| `s_fa_adminexpensetogr` | 管理费用／营业总收入 | REPORTDATE |
| `s_fa_adminexpensetogr_ttm` | 管理费用／营业总收入(TTM) |  |
| `s_fa_adminexpensetogr_ttm2` | 管理费用/营业总收入(TTM) | REPORTDATE |
| `s_fa_apnpturn` | 应付账款及应付票据周转率 | REPORTDATE |
| `s_fa_arnrturn` | 应收账款及应收票据周转率 | REPORTDATE |
| `s_fa_arturn` | 应收账款周转率 | REPORTDATE |
| `s_fa_arturn_reserve` | 应收账款周转率(含坏账准备) | REPORTDATE |
| `s_fa_arturn_ttm` | 应收账款周转率(TTM) | REPORTDATE |
| `s_fa_arturndays` | 应收账款周转天数 | REPORTDATE |
| `s_fa_asset_mrq` | 资产总计(MRQ) |  |
| `s_fa_assetstoequity` | 权益乘数 | REPORTDATE |
| `s_fa_assetsturn` | 总资产周转率 | REPORTDATE |
| `s_fa_bps` | 每股净资产BPS | REPORTDATE |
| `s_fa_bps2` | 每股净资产BPS | REPORTDATE、CURTYPE |
| `s_fa_bps_adjust` | 每股净资产BPS-最新股本摊薄 | REPORTDATE |
| `s_fa_bps_lyr` | 每股净资产BPS(最新年报,LYR) | TRADEDATE |
| `s_fa_bps_new` | 每股净资产BPS(最新公告) |  |
| `s_fa_cagr_netprofit` | 净利润复合年增长率 | Year |
| `s_fa_cagr_or` | 营业收入复合年增长率 | Year、N |
| `s_fa_cagr_ta` | 资产总计复合年增长率 | Year、N |
| `s_fa_cagr_totalprofit` | 利润总额复合年增长率 |  |
| `s_fa_cagr_tr` | 营业总收入复合年增长率 | Year |
| `s_fa_capitalizedtoda` | 资本支出／折旧和摊销 | REPORTDATE |
| `s_fa_cashflow_ttm` | 现金净流量(TTM) |  |
| `s_fa_cashflow_ttm2` | 现金净流量(TTM) | REPORTDATE |
| `s_fa_cashratio` | 保守速动比率 | REPORTDATE |
| `s_fa_cashtostdebt` | 货币资金/短期债务 | REPORTDATE、TYPE |
| `s_fa_cashturnratio` | 现金周转率 | REPORTDATE |
| `s_fa_catoassets` | 流动资产／总资产 | REPORTDATE |
| `s_fa_caturn` | 流动资产周转率 | REPORTDATE |
| `s_fa_caturn_ttm` | 流动资产周转率(TTM) | REPORTDATE |
| `s_fa_cfps` | 每股现金流量净额 | REPORTDATE |
| `s_fa_cfps2` | 每股现金流量净额 | REPORTDATE、CURTYPE |
| `s_fa_cfps_ttm` | 每股现金流量净额(TTM) |  |
| `s_fa_cfps_ttm2` | 每股现金流量净额(TTM) | TRADEDATE |
| `s_fa_cogstosales` | 销售成本率 | REPORTDATE |
| `s_fa_cost_ttm` | 营业成本-非金融类(TTM) |  |
| `s_fa_cost_ttm2` | 营业成本-非金融类(TTM) | REPORTDATE |
| `s_fa_crofll` | 长期债务资本化比率 | REPORTDATE |
| `s_fa_current` | 流动比率 | REPORTDATE |
| `s_fa_currentdebttodebt` | 流动负债／负债合计 | REPORTDATE |
| `s_fa_da` | 当期计提折旧与摊销 | REPORTDATE |
| `s_fa_debt_mrq` | 负债合计(MRQ) |  |
| `s_fa_debttoassets` | 资产负债率 | REPORTDATE |
| `s_fa_debttoequity` | 产权比率(负债合计／归属母公司股东的权益) | REPORTDATE |
| `s_fa_debttoeqy` | 净资产负债率 | REPORTDATE |
| `s_fa_deducteddebttoassets` | 剔除预收款项后的资产负债率 | REPORTDATE |
| `s_fa_deductedprofit` | 扣除非经常性损益后的净利润 | REPORTDATE |
| `s_fa_deductedprofit_1` | 扣除非经常性损益后归属母公司股东的净利润 | REPORTDATE、TYPE |
| `s_fa_deductedprofit_ttm` | 扣除非经常性损益后的净利润(TTM) | TRADEDATE |
| `s_fa_deductedprofit_ttm2` | 扣除非经常性损益后的净利润(TTM) | REPORTDATE |
| `s_fa_deductedprofittoprofit` | 扣除非经常损益后的净利润／净利润 | REPORTDATE |
| `s_fa_dp_yoy` | 扣除非经常性损益后的净利润(同比增长率) | REPORTDATE |
| `s_fa_dupont_assetstoequity` | 权益乘数(杜邦分析)(新增) | D |
| `s_fa_dupont_ebittosales` | 息税前利润／营业总收入(新增) | D |
| `s_fa_dupont_faturnover` | 总资产周转率(新增) | D |
| `s_fa_dupont_intburden` | 利润总额／息税前利润(新增) | D |
| `s_fa_dupont_np` | 归属母公司股东的净利润／净利润(新增) | D |
| `s_fa_dupont_nptosales` | 净利润／营业总收入(新增) | D |
| `s_fa_dupont_roe` | 净资产收益率ROE(新增) | D |
| `s_fa_dupont_taxburden` | 净利润／利润总额(新增) | D |
| `s_fa_ebit` | 息税前利润EBIT | REPORTDATE |
| `s_fa_ebit2` | 息税前利润(正向法)(新增) | DEALDATE、TP |
| `s_fa_ebit_ttm` | 息税前利润(TTM) |  |
| `s_fa_ebit_ttm2` | 息税前利润(TTM反推法) | REPORTDATE |
| `s_fa_ebitda` | 息税折旧摊销前利润EBITDA | REPORTDATE |
| `s_fa_ebitda2` | 息税折旧摊销前利润(正向法)(新增) | DEALDATE、TP |
| `s_fa_ebitda_ttm` | EBITDA(TTM反推法) | REPORTDATE |
| `s_fa_ebitdaps` | 每股EBITDA | REPORTDATE |
| `s_fa_ebitdatodebt` | 息税折旧摊销前利润／负债合计 | REPORTDATE |
| `s_fa_ebitdatointerestdebt` | EBITDA/带息债务 | REPORTDATE |
| `s_fa_ebitdatosales` | EBITDA/营业总收入 | REPORTDATE |
| `s_fa_ebitps` | 每股息税前利润 | REPORTDATE |
| `s_fa_ebitps2` | 每股息税前利润 | REPORTDATE、CURTYPE |
| `s_fa_ebittoassets2` | 息税前利润(TTM)/总资产 | REPORTDATE |
| `s_fa_ebittogr` | 息税前利润／营业总收入 | REPORTDATE |
| `s_fa_ebittointerest` | 已获利息倍数(EBIT／利息费用) | REPORTDATE |
| `s_fa_ebr` | 研发支出前利润 | REPORTDATE |
| `s_fa_ebt_ttm` | 利润总额(TTM) |  |
| `s_fa_ebt_ttm2` | 利润总额(TTM) | REPORTDATE |
| `s_fa_ebttoor_ttm` | 利润总额/营业收入(TTM) | REPORTDATE |
| `s_fa_eps_adjust` | 每股收益EPS-最新股本摊薄 | REPORTDATE |
| `s_fa_eps_adjust2` | 每股收益-最新股本摊薄 | REPORTDATE、CURTYPE |
| `s_fa_eps_basic` | 每股收益EPS-基本 | REPORTDATE |
| `s_fa_eps_basic2` | 每股收益EPS-基本 | REPORTDATE、CURTYPE |
| `s_fa_eps_deducted_ttm` | 扣非后每股收益(TTM) | REPORTDATE |
| `s_fa_eps_diluted` | 每股收益EPS-稀释 | REPORTDATE |
| `s_fa_eps_diluted2` | 每股收益EPS-期末股本摊薄 | REPORTDATE |
| `s_fa_eps_diluted3` | 每股收益-期末股本摊薄 | REPORTDATE、CURTYPE |
| `s_fa_eps_diluted4` | 每股收益EPS-稀释 | REPORTDATE、CURTYPE |
| `s_fa_eps_exbasic` | 每股收益EPS-扣除／基本 | REPORTDATE |
| `s_fa_eps_exdiluted` | 每股收益EPS-扣除／稀释 | REPORTDATE |
| `s_fa_eps_exdiluted2` | 每股收益EPS-扣除／期末股本摊薄 | REPORTDATE |
| `s_fa_eps_ttm` | 每股收益EPS(TTM) |  |
| `s_fa_eps_ttm2` | 每股收益EPS(TTM) | TRADEDATE |
| `s_fa_equity_mrq` | 归属母公司股东的权益(MRQ) |  |
| `s_fa_equity_mrq2` | 归属母公司股东权益(MRQ) | TRADEDATE |
| `s_fa_equity_new` | 归属母公司股东的权益(最新公告) |  |
| `s_fa_equity_new2` | 归属母公司股东的股东权益(LF) | TRADEDATE |
| `s_fa_equity_to_asset` | 股东权益比 | REPORTDATE、TYPE |
| `s_fa_equitytodebt` | 归属母公司股东的权益／负债合计 | REPORTDATE |
| `s_fa_equitytointerestdebt` | 归属母公司股东的权益／带息债务 | REPORTDATE |
| `s_fa_equitytototalcapital` | 归属母公司股东的权益／全部投入资本 | REPORTDATE |
| `s_fa_errorcorrectiondate` | 会计差错更正披露日期 | REPORTDATE |
| `s_fa_errorcorrectionornot` | 是否存在会计差错更正 | REPORTDATE |
| `s_fa_exinterestdebt_current` | 无息流动负债 | REPORTDATE |
| `s_fa_exinterestdebt_noncurrent` | 无息非流动负债 | REPORTDATE |
| `s_fa_expense_ttm` | 营业支出-金融类(TTM) |  |
| `s_fa_expense_ttm2` | 营业支出-金融类(TTM) | REPORTDATE |
| `s_fa_expensetosales` | 销售期间费用率 | REPORTDATE |
| `s_fa_expensetosales_ttm` | 销售期间费用率(TTM) |  |
| `s_fa_expensetosales_ttm2` | 销售期间费用率(TTM) | REPORTDATE |
| `s_fa_extraordinary` | 非经常性损益 | REPORTDATE |
| `s_fa_faturn` | 固定资产周转率 | REPORTDATE |
| `s_fa_fcfe` | 股权自由现金流量FCFE | REPORTDATE |
| `s_fa_fcfeps` | 每股股东自由现金流量 | REPORTDATE |
| `s_fa_fcfeps2` | 每股股东自由现金流量 | REPORTDATE、CURTYPE |
| `s_fa_fcff` | 企业自由现金流量FCFF | REPORTDATE |
| `s_fa_fcffps` | 每股企业自由现金流量 | REPORTDATE |
| `s_fa_fcffps2` | 每股企业自由现金流量 | REPORTDATE、CURTYPE |
| `s_fa_finaexpense_ttm` | 财务费用(TTM) |  |
| `s_fa_finaexpense_ttm2` | 财务费用(TTM) | REPORTDATE |
| `s_fa_finaexpensetogr` | 财务费用／营业总收入 | REPORTDATE |
| `s_fa_finaexpensetogr_ttm` | 财务费用／营业总收入(TTM) |  |
| `s_fa_finaexpensetogr_ttm2` | 财务费用/营业总收入(TTM) | REPORTDATE |
| `s_fa_financecashflow_ttm` | 筹资活动现金净流量(TTM) |  |
| `s_fa_financecashflow_ttm2` | 筹资活动现金净流量(TTM) | REPORTDATE |
| `s_fa_gc2_ttm2` | 营业总成本2(TTM) | REPORTDATE |
| `s_fa_gc_ttm` | 营业总成本(TTM) |  |
| `s_fa_gc_ttm2` | 营业总成本(TTM) | REPORTDATE |
| `s_fa_gctogr` | 营业总成本／营业总收入 | REPORTDATE |
| `s_fa_gctogr_ttm` | 营业总成本／营业总收入(TTM) |  |
| `s_fa_gctogr_ttm2` | 营业总成本/营业总收入(TTM) | REPORTDATE |
| `s_fa_gr_ttm` | 营业总收入(TTM) |  |
| `s_fa_gr_ttm2` | 营业总收入(TTM) | REPORTDATE |
| `s_fa_grossmargin` | 毛利 | REPORTDATE |
| `s_fa_grossmargin_ttm` | 毛利(TTM) |  |
| `s_fa_grossmargin_ttm2` | 毛利(TTM) | REPORTDATE |
| `s_fa_grossprofitmargin` | 销售毛利率 | REPORTDATE |
| `s_fa_grossprofitmargin_ttm` | 销售毛利率(TTM) |  |
| `s_fa_grossprofitmargin_ttm2` | 销售毛利率(TTM) | REPORTDATE |
| `s_fa_grps` | 每股营业总收入 | REPORTDATE |
| `s_fa_grps2` | 每股营业总收入 | REPORTDATE、CURTYPE |
| `s_fa_ibdebtratio` | 有息负债率 | REPORTDATE |
| `s_fa_impairment_ttm` | 资产减值损失(TTM) |  |
| `s_fa_impairment_ttm2` | 资产减值损失(TTM) | REPORTDATE |
| `s_fa_impairtogr` | 资产减值损失／营业总收入 | REPORTDATE |
| `s_fa_impairtogr_ttm` | 资产减值损失／营业总收入(TTM) |  |
| `s_fa_impairtogr_ttm2` | 资产减值损失/营业总收入(TTM) | REPORTDATE |
| `s_fa_interestdebt` | 带息债务 | REPORTDATE |
| `s_fa_interestdebttoev` | 带息债务／股权价值 |  |
| `s_fa_interestdebttototalcapital` | 带息债务／全部投入资本 | REPORTDATE |
| `s_fa_interestexpense_ttm` | 利息支出(TTM) | REPORTDATE |
| `s_fa_investcapital` | 全部投入资本 | REPORTDATE |
| `s_fa_investcashflow_ttm` | 投资活动现金净流量(TTM) |  |
| `s_fa_investcashflow_ttm2` | 投资活动现金净流量(TTM) | REPORTDATE |
| `s_fa_investincome` | 价值变动净收益 | REPORTDATE |
| `s_fa_investincome_ttm` | 价值变动净收益(TTM) |  |
| `s_fa_investincome_ttm2` | 价值变动净收益(TTM) | REPORTDATE |
| `s_fa_investincometoebt` | 价值变动净收益／利润总额 | REPORTDATE |
| `s_fa_investincometoebt_ttm` | 价值变动净收益／利润总额(TTM) |  |
| `s_fa_investincometoebt_ttm2` | 价值变动净收益/利润总额(TTM) | REPORTDATE |
| `s_fa_invturn` | 存货周转率 | REPORTDATE |
| `s_fa_invturndays` | 存货周转天数 | REPORTDATE |
| `s_fa_latelyrd_bt` | 最新报告期 | TRADEDATE |
| `s_fa_latelyrd_bts` | 最新报告期 | TRADEDATE |
| `s_fa_latelyyear2` | 最新年报年份 | TRADEDATE |
| `s_fa_longdebtodebt` | 非流动负债／负债合计 | REPORTDATE |
| `s_fa_longdebttoworkingcapital` | 长期债务与营运资金比率 | REPORTDATE |
| `s_fa_lyr_bt` | 最新年报 | TRADEDATE |
| `s_fa_minorityinterest_ttm` | 少数股东损益(TTM) | REPORTDATE |
| `s_fa_ncatoassets` | 非流动资产／总资产 | REPORTDATE |
| `s_fa_netdebt` | 净债务 | REPORTDATE |
| `s_fa_netdebtratio` | 净负债率 | REPORTDATE |
| `s_fa_netdebttoev` | 净债务／股权价值 |  |
| `s_fa_netprofit_min` | 扣非净利与归母净利较小值 | REPORTDATE |
| `s_fa_netprofit_ttm` | 归属母公司股东的净利润(TTM) |  |
| `s_fa_netprofit_ttm2` | 归属母公司股东的净利润(TTM) | REPORTDATE |
| `s_fa_netprofitcashcover` | 净利润现金含量 | REPORTDATE |
| `s_fa_netprofitmargin` | 销售净利率 | REPORTDATE |
| `s_fa_netprofitmargin_deducted` | 扣非后销售净利率 | REPORTDATE |
| `s_fa_netprofitmargin_ttm` | 销售净利率(TTM) |  |
| `s_fa_netprofitmargin_ttm2` | 销售净利率(TTM) | REPORTDATE |
| `s_fa_netprofittoassets` | 总资产净利率-不含少数股东损益(TTM) | REPORTDATE |
| `s_fa_netprofittoor_ttm` | 归属母公司股东的净利润/营业收入(TTM) | REPORTDATE |
| `s_fa_netturndays2` | 净营业周期(含应收应付票据) | REPORTDATE |
| `s_fa_networkingcapital` | 净营运资本 | REPORTDATE |
| `s_fa_noneinterestdebt` | 无息负债 | REPORTDATE、TYPE |
| `s_fa_nonoperateprofit_ttm` | 营业外收支净额(TTM) |  |
| `s_fa_nonoperateprofit_ttm2` | 营业外收支净额(TTM) | REPORTDATE |
| `s_fa_nonoperateprofittoebt` | 营业外收支净额／利润总额 | REPORTDATE |
| `s_fa_nonoperateprofittoebt_ttm` | 营业外收支净额／利润总额(TTM) |  |
| `s_fa_nonoperateprofittoebt_ttm2` | 营业外收支净额/利润总额(TTM) | REPORTDATE |
| `s_fa_ocfps` | 每股经营活动产生的现金流量净额 | REPORTDATE |
| `s_fa_ocfps2` | 每股经营活动产生的现金流量净额 | REPORTDATE、CURTYPE |
| `s_fa_ocfps_ttm` | 每股经营活动产生的现金流量净额(TTM) |  |
| `s_fa_ocfps_ttm2` | 每股经营活动产生的现金流量净额(TTM) | TRADEDATE |
| `s_fa_ocftodebt` | 经营活动产生的现金流量净额／负债合计 | REPORTDATE |
| `s_fa_ocftointerestdebt` | 经营活动产生的现金流量净额／带息债务 | REPORTDATE |
| `s_fa_ocftonetdebt` | 经营活动产生的现金流量净额／净债务 | REPORTDATE |
| `s_fa_ocftooperateincome` | 经营活动产生的现金流量净额／经营活动净收益 | REPORTDATE |
| `s_fa_ocftooperateincome_ttm` | 经营活动产生的现金流量净额／经营活动净收益(TTM) |  |
| `s_fa_ocftooperateincome_ttm2` | 经营活动产生的现金流量净额/经营活动净收益(TTM) | REPORTDATE |
| `s_fa_ocftoor` | 经营活动产生的现金流量净额／营业收入 | REPORTDATE |
| `s_fa_ocftoor_ttm` | 经营活动产生的现金流量净额／营业收入(TTM) |  |
| `s_fa_ocftoor_ttm2` | 经营活动产生的现金流量净额/营业收入(TTM) | REPORTDATE |
| `s_fa_ocftosales` | 经营性现金净流量/营业总收入 | REPORTDATE |
| `s_fa_ocftoshortdebt` | 经营活动产生的现金流量净额／流动负债 | REPORTDATE |
| `s_fa_op_ttm` | 营业利润(TTM) |  |
| `s_fa_op_ttm2` | 营业利润(TTM) | REPORTDATE |
| `s_fa_operatecashflow_ttm` | 经营活动现金净流量(TTM) |  |
| `s_fa_operatecashflow_ttm2` | 经营活动现金净流量(TTM) | REPORTDATE |
| `s_fa_operatecashflowtoop_ttm` | 经营活动产生的现金流量净额/营业利润(TTM) | REPORTDATE |
| `s_fa_operateexpense_ttm` | 销售费用(TTM) |  |
| `s_fa_operateexpense_ttm2` | 销售费用(TTM) | REPORTDATE |
| `s_fa_operateexpensetogr` | 营业费用／营业总收入 | REPORTDATE |
| `s_fa_operateexpensetogr_ttm` | 营业费用／营业总收入(TTM) |  |
| `s_fa_operateexpensetogr_ttm2` | 销售费用/营业总收入(TTM) | REPORTDATE |
| `s_fa_operateincome` | 经营活动净收益 | REPORTDATE |
| `s_fa_operateincome_ttm` | 经营活动净收益(TTM) |  |
| `s_fa_operateincome_ttm2` | 经营活动净收益(TTM) | REPORTDATE |
| `s_fa_operateincometoebt` | 经营活动净收益／利润总额 | REPORTDATE |
| `s_fa_operateincometoebt_ttm` | 经营活动净收益／利润总额(TTM) |  |
| `s_fa_operateincometoebt_ttm2` | 经营活动净收益/利润总额(TTM) | REPORTDATE |
| `s_fa_optogr` | 营业利润／营业总收入 | REPORTDATE |
| `s_fa_optogr_ttm` | 营业利润／营业总收入(TTM) |  |
| `s_fa_optogr_ttm2` | 营业利润/营业总收入(TTM) | REPORTDATE |
| `s_fa_optoor_ttm` | 营业利润/营业收入(TTM) | REPORTDATE |
| `s_fa_or_ttm` | 营业收入(TTM) |  |
| `s_fa_or_ttm2` | 营业收入(TTM) | REPORTDATE |
| `s_fa_orps` | 每股营业收入 | REPORTDATE |
| `s_fa_orps2` | 每股营业收入 | REPORTDATE、CURTYPE |
| `s_fa_orps_ttm` | 每股营业收入(TTM) |  |
| `s_fa_orps_ttm2` | 每股营业收入(TTM) | TRADEDATE |
| `s_fa_performancechan` | 业绩说明会召开渠道 | REPORTDATE |
| `s_fa_performancedate` | 业绩说明会日期 | REPORTDATE |
| `s_fa_performanceform` | 业绩说明会召开形式 | REPORTDATE |
| `s_fa_performancetime` | 业绩说明会时间 | REPORTDATE |
| `s_fa_periodexpense_t_ttm` | 期间费用(TTM) | REPORTDATE |
| `s_fa_profit_ttm` | 净利润(TTM) |  |
| `s_fa_profit_ttm2` | 净利润(TTM) | REPORTDATE |
| `s_fa_profitpp` | 人均创利 |  |
| `s_fa_profittogr` | 净利润／营业总收入 | REPORTDATE |
| `s_fa_profittogr_ttm` | 净利润／营业总收入(TTM) |  |
| `s_fa_profittogr_ttm2` | 净利润/营业总收入(TTM) | REPORTDATE |
| `s_fa_quick` | 速动比率 | REPORTDATE |
| `s_fa_rde_ttm` | 研发费用(TTM) | REPORTDATE |
| `s_fa_rdexp_yoy` | 研发费用同比增长 | REPORTDATE |
| `s_fa_researchanddevelopmentexpenses` | 研发费用(新增) | REPORTDATE |
| `s_fa_retainedearnings` | 留存收益 | REPORTDATE |
| `s_fa_retainedps` | 每股留存收益 | REPORTDATE |
| `s_fa_retainedps2` | 每股留存收益 | REPORTDATE、CURTYPE |
| `s_fa_revenuepp` | 人均创收 |  |
| `s_fa_roa` | 总资产净利润ROA | REPORTDATE |
| `s_fa_roa2` | 总资产报酬率ROA | REPORTDATE |
| `s_fa_roa2_ttm` | 总资产报酬率ROA(TTM) |  |
| `s_fa_roa2_ttm2` | 总资产报酬率(TTM) | REPORTDATE |
| `s_fa_roa2_yearly` | 年化总资产报酬率 | REPORTDATE |
| `s_fa_roa_ttm` | 总资产净利率ROA(TTM) |  |
| `s_fa_roa_yearly` | 年化总资产净利率 | REPORTDATE |
| `s_fa_roe` | 净资产收益率ROE | REPORTDATE |
| `s_fa_roe_avg` | 净资产收益率ROE-增发条件 | REPORTDATE |
| `s_fa_roe_basic` | 净资产收益率ROE(加权) | REPORTDATE |
| `s_fa_roe_deducted` | 净资产收益率ROE-扣除非经常损益 | REPORTDATE |
| `s_fa_roe_diluted` | 净资产收益率ROE(摊薄) | REPORTDATE |
| `s_fa_roe_exbasic` | 净资产收益率ROE(扣除／加权) | REPORTDATE |
| `s_fa_roe_exdiluted` | 净资产收益率ROE(扣除／摊薄) | REPORTDATE |
| `s_fa_roe_ttm` | 净资产收益率ROE(TTM) |  |
| `s_fa_roe_ttm2` | 净资产收益率(TTM) | REPORTDATE |
| `s_fa_roe_ttmavg` | 净资产收益率(TTM,平均) | REPORTDATE |
| `s_fa_roic` | 投入资本回报率ROIC | REPORTDATE |
| `s_fa_roic2_ttm` | 投入资本回报率ROIC(TTM) | REPORTDATE |
| `s_fa_roic_ttm` | 投入资本回报率(TTM) | REPORTDATE |
| `s_fa_roic_yearly` | 年化净资产收益率 | REPORTDATE |
| `s_fa_salary` | 员工薪酬 | Year |
| `s_fa_salarypp` | 人均薪酬 |  |
| `s_fa_salarypp_cost` | 费用化人均薪酬 | Year |
| `s_fa_salescashin_ttm` | 销售商品提供劳务收到的现金(TTM) |  |
| `s_fa_salescashin_ttm2` | 销售商品提供劳务收到的现金(TTM) | REPORTDATE |
| `s_fa_salescashintoor` | 销售商品提供劳务收到的现金／营业收入 | REPORTDATE |
| `s_fa_salescashintoor_ttm` | 销售商品提供劳务收到的现金／营业收入(TTM) |  |
| `s_fa_salescashintoor_ttm2` | 销售商品提供劳务收到的现金/营业收入(TTM) | REPORTDATE |
| `s_fa_stdebtratio` | 现金短债比 | REPORTDATE |
| `s_fa_surpluscapitalps` | 每股资本公积 | REPORTDATE |
| `s_fa_surplusreserveps` | 每股盈余公积 | REPORTDATE |
| `s_fa_tangibleasset` | 有形资产 | REPORTDATE |
| `s_fa_tangibleassetstoassets` | 有形资产／总资产 | REPORTDATE |
| `s_fa_tangibleassettodebt` | 有形资产／负债合计 | REPORTDATE |
| `s_fa_tangibleassettointerestdebt` | 有形资产／带息债务 | REPORTDATE |
| `s_fa_tangibleassettonetdebt` | 有形资产／净债务 | REPORTDATE |
| `s_fa_tax_ttm` | 所得税(TTM) | REPORTDATE |
| `s_fa_taxtoebt` | 所得税／利润总额 | REPORTDATE |
| `s_fa_taxtoebt_ttm` | 税项/利润总额(TTM) | REPORTDATE |
| `s_fa_taxtoor_ttm` | 营业利润/利润总额(TTM) | REPORTDATE |
| `s_fa_tltoebitda` | 全部债务/EBITDA |  |
| `s_fa_totalequity_mrq` | 股东权益(MRQ) |  |
| `s_fa_turndays` | 营业周期 | REPORTDATE |
| `s_fa_turnover_ttm` | 总资产周转率(TTM) | REPORTDATE |
| `s_fa_undistributedps` | 每股未分配利润 | REPORTDATE |
| `s_fa_workingcapital` | 营运资本 | REPORTDATE |
| `s_fa_yoy_assets` | 总资产(同比增长率) | REPORTDATE |
| `s_fa_yoy_equity` | 净资产(同比增长率) | REPORTDATE |
| `s_fa_yoy_or` | 营业收入同比增长率 | REPORTDATE |
| `s_fa_yoy_tr` | 营业总收入同比增长率 | REPORTDATE |
| `s_fa_yoyassets` | 总资产(同比增长率) | REPORTDATE |
| `s_fa_yoybps` | 每股净资产 ％ | REPORTDATE |
| `s_fa_yoycf` | 现金净流量(同比增长率) | REPORTDATE |
| `s_fa_yoydebt` | 总负债(同比增长率) | REPORTDATE |
| `s_fa_yoyebt` | 利润总额 ％ | REPORTDATE |
| `s_fa_yoyeps_basic` | 基本每股收益 ％ | REPORTDATE |
| `s_fa_yoyeps_diluted` | 稀释每股收益 ％ | REPORTDATE |
| `s_fa_yoyequity` | 净资产(同比增长率) | REPORTDATE |
| `s_fa_yoyfcf` | 筹资活动产生的现金流量净额(同比增长率) | REPORTDATE |
| `s_fa_yoyicf` | 投资活动产生的现金流量净额(同比增长率) | REPORTDATE |
| `s_fa_yoynetprofit` | 归属母公司股东的净利润 ％ | REPORTDATE |
| `s_fa_yoynetprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益 ％ | REPORTDATE |
| `s_fa_yoyocf` | 经营活动产生的现金流量净额 ％ | REPORTDATE |
| `s_fa_yoyocfps` | 每股经营活动产生的现金流量净额 ％ | REPORTDATE |
| `s_fa_yoyop` | 营业利润 ％ | REPORTDATE |
| `s_fa_yoyprofit` | 净利润(同比增长率) | REPORTDATE |
| `s_fa_yoyroe` | 净资产收益率(摊薄) ％ | REPORTDATE |
| `s_fellow_amount` | 增发数量 | RPTYEAR |
| `s_fellow_amt_fund` | 向基金配售数量(新增) |  |
| `s_fellow_amt_orgtradable` | 向原流通股东定向配售数量(新增) |  |
| `s_fellow_amt_otherpub` | 向其它公众投资者配售数量(新增) |  |
| `s_fellow_amt_targeted` | 定向配售数量(新增) |  |
| `s_fellow_amtbyplacing` | 网下机构投资者有效申购户数(新增) |  |
| `s_fellow_amttoincorp` | 网上向老股东优先配售比例(新增) |  |
| `s_fellow_amttoinst` | 网上向老股东优先配售数量(新增) |  |
| `s_fellow_amttojur` | 网下超额认购倍数(新增) |  |
| `s_fellow_anncedate` | 上网发行公告日(新增) |  |
| `s_fellow_approvaldate` | 增发获准日期 |  |
| `s_fellow_benchmarkprice` | 定向增发基准价格 |  |
| `s_fellow_capeffacc` | 老股东优先配售有效申购户数(新增) |  |
| `s_fellow_capeffamt` | 老股东优先配售有效申购股数(新增) |  |
| `s_fellow_capratio` | 公开发行认购有效申购户数(新增) |  |
| `s_fellow_cashamt` | 公开发行比例认购有效申购股数(新增) |  |
| `s_fellow_casheffacc` | 公开发行超额认购倍数(新增) |  |
| `s_fellow_cashratio` | 总超额认购倍数(新增) |  |
| `s_fellow_collection` | 增发募集资金 | RPTYEAR |
| `s_fellow_collection_acct` | 增发募集资金监管银行账户 | Year |
| `s_fellow_collection_bank` | 增发募集资金监管银行名称 | Year |
| `s_fellow_collection_t` | 区间增发募集资金合计 | StartDate、DATE |
| `s_fellow_deputyundr` | 增发上市推荐人(新增) |  |
| `s_fellow_dilutedpe` | 增发市盈率(摊薄)(新增) |  |
| `s_fellow_discntratio` | 折扣率(新增) |  |
| `s_fellow_distor` | 总有效申购户数(新增) |  |
| `s_fellow_exdividenddate` | 增发除权日 | RPTYEAR |
| `s_fellow_expectedcollection` | 增发初始预计募集资金总额 | Year |
| `s_fellow_expectedcollection_new` | 增发最新预计募集资金总额 | Year |
| `s_fellow_expense` | 增发费用 | RPTYEAR |
| `s_fellow_firstfeedbackdate` | 增发首次回复日 |  |
| `s_fellow_firstinquirydate` | 增发首次问询日 |  |
| `s_fellow_iecapprovaldate` | 发审委通过公告日 | Year |
| `s_fellow_instlistdate` | 向机构投资者增发部分上市日期(新增) |  |
| `s_fellow_intercodnator` | 总有效申购股数(新增) |  |
| `s_fellow_issuedate` | 公开发行日(新增) |  |
| `s_fellow_issuedate_pp` | 定增发行日期 |  |
| `s_fellow_issuetype` | 增发发行方式(新增) |  |
| `s_fellow_latestfeedbackdate` | 增发最新回复日 |  |
| `s_fellow_latestinquirydate` | 增发最新问询日 |  |
| `s_fellow_leadundr` | 增发主承销商(新增) |  |
| `s_fellow_listeddate` | 增发上市日 | RPTYEAR |
| `s_fellow_n` | 区间定增次数 | StartDate、DATE |
| `s_fellow_netcollection` | 增发实际募集资金 | RPTYEAR |
| `s_fellow_netprice` | 净值价格(新增) |  |
| `s_fellow_nominator` | 增发分销商(新增) |  |
| `s_fellow_offeringdate` | 增发公告日(新增) |  |
| `s_fellow_otcamt` | 网下发行数量(新增) |  |
| `s_fellow_otcamt_pct` | 网下发售比例(新增) |  |
| `s_fellow_otcdate` | 向网下增发日期(新增) |  |
| `s_fellow_otcpreamt_org` | 网下向老股东优先配售数量(新增) |  |
| `s_fellow_oversubratio` | 其它公众投资者有效申购股数(新增) |  |
| `s_fellow_payenddate` | 向老股东配售缴款截止日(新增) |  |
| `s_fellow_paystartdate` | 向老股东配售缴款起始日(新增) |  |
| `s_fellow_pe` | 增发市盈率 | RPTYEAR、TYPE |
| `s_fellow_preplandate` | 预案公告日(新增) |  |
| `s_fellow_price` | 增发价格 | RPTYEAR |
| `s_fellow_pricemax` | 增发预案价上限 |  |
| `s_fellow_pricemin` | 增发预案价下限 |  |
| `s_fellow_pricetobenchmarkprice` | 定向增发实际价格相对基准价格比率 |  |
| `s_fellow_pricetoreserveprice` | 定向增发实际价格相对增发底价比率 |  |
| `s_fellow_progress` | 增发进度(新增) |  |
| `s_fellow_pubamt` | 公开发行数量(新增) |  |
| `s_fellow_publicratio` | 公开发行中签率(新增) |  |
| `s_fellow_recorddate` | 向老股东配售股权登记日(新增) |  |
| `s_fellow_registerdate` | 股权登记日 | Year |
| `s_fellow_resultdate` | 发行结果公告日(新增) |  |
| `s_fellow_roadshowdate` | 网上路演日 |  |
| `s_fellow_shareholders` | 增发发行对象 |  |
| `s_fellow_simpleprogram` | 增发是否属于简易程序审核 | Year |
| `s_fellow_smtganncedate` | 股东大会公告日(新增) | D |
| `s_fellow_subaccbypub` | 其它公众投资者有效申购户数(新增) |  |
| `s_fellow_subamtbyplacing` | 网下机构投资者有效申购股数(新增) |  |
| `s_fellow_subbydistr` | 承销商认购余股(新增) |  |
| `s_fellow_submit_regist_date` | 提交注册日 |  |
| `s_fellow_sucregistdate` | 增发注册成功日 | Year |
| `s_fellow_totalratio` | 总中签率(新增) |  |
| `s_fellow_trnffamt` | 回拨数量(新增) |  |
| `s_fellow_undrtype` | 增发承销方式(新增) |  |
| `s_fellow_weightedpe` | 增发市盈率(加权)(新增) |  |
| `s_fellowon_matchfin` | 增发募集资金(配套融资) | Year |
| `s_fina_mat` | 存量债券余额(按期限) | TermType |
| `s_fina_remainingnumber` | 存量债券数目 | BondType |
| `s_fina_totalamount` | 存量债券余额 | BondType |
| `s_fina_totalamount2` | 区间发行债券总额 | StartDate、DATE、BondType |
| `s_fina_totalamout_anytime` | 存量债券余额(支持历史) | DEALDATE、BondType |
| `s_fina_totalnumber` | 区间发行债券数目 | StartDate、DATE、BondType |
| `s_findata_capexp` | 资本支出(拟增) | REPORTDATE |
| `s_findata_ebit` | 息税前利润(EBIT) | REPORTDATE |
| `s_findata_ebitda` | 息税折旧摊销前利润(EBITDA) | REPORTDATE |
| `s_findata_ebt_ttm` | 税前利润TTM |  |
| `s_findata_fcfe` | 股权自由现金流量(FCFE) | REPORTDATE |
| `s_findata_fcff` | 企业自由现金流量(FCFF) | REPORTDATE |
| `s_findata_mainprofit_ttm` | 主营业务利润TTM |  |
| `s_findata_netdebt` | 净债务 | REPORTDATE |
| `s_findata_netprofit_ttm` | 净利润TTM |  |
| `s_findata_normalnetprofit` | 扣除非经常损益后的净利润 | REPORTDATE |
| `s_findata_operatingprofit_ttm` | 营业利润TTM |  |
| `s_findata_sales_ttm` | 主营业务收入TTM |  |
| `s_findata_tangibleasset` | 有形资产净值 | REPORTDATE |
| `s_findata_workingcapital` | 营运资金 | REPORTDATE |
| `s_fund_esg_tax_wind` | Wind ESG投资基金类型 |  |
| `s_growth_assets` | 资产总计 (N年, ％) | REPORTDATE |
| `s_growth_ebt` | 利润总额 (N年, ％) | REPORTDATE |
| `s_growth_equity` | 归属母公司股东的权益 (N年, ％) | REPORTDATE |
| `s_growth_gc` | 营业总成本 (N年, ％) | REPORTDATE |
| `s_growth_gr` | 营业总收入 (N年, ％) | REPORTDATE |
| `s_growth_investincome` | 价值变动净收益 (N年, ％) | REPORTDATE |
| `s_growth_netprofit` | 归属母公司股东的净利润 (N年, ％) | REPORTDATE |
| `s_growth_netprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益 (N年, ％) | REPORTDATE |
| `s_growth_ocf` | 经营活动产生的现金流量净额 (N年, ％) | REPORTDATE |
| `s_growth_op` | 营业利润 (N年, ％) | REPORTDATE |
| `s_growth_operateincome` | 经营活动净收益 (N年, ％) | REPORTDATE |
| `s_growth_or` | 营业收入 (N年, ％) | REPORTDATE |
| `s_growth_profit` | 净利润 (N年, ％) | REPORTDATE |
| `s_growth_profittosales` | 销售利润率 (N年, ％) | REPORTDATE |
| `s_growth_roe` | 净资产收益率 (N年, ％) | REPORTDATE |
| `s_growth_totalequity` | 股东权益 (N年, ％) | REPORTDATE |
| `s_handlingdate_conb` | 可转债受理日 |  |
| `s_handlingdate_pi` | 非公开发行股票受理日 |  |
| `s_handlingdate_rs` | 配股受理日 |  |
| `s_hksc_date` | 纳入港股通日期 | TRADEDATE |
| `s_holder_avgnum` | 户均持股数量 | REPORTDATE |
| `s_holder_avgpct` | 户均持股比例 | REPORTDATE |
| `s_holder_avgpctchange` | 相对上一报告期户均持股比例差 | REPORTDATE |
| `s_holder_avgprofit` | 近三年归母净利润均值 | TRADEDATE |
| `s_holder_breaknetornot` | 是否破净 | TRADEDATE |
| `s_holder_breakornot` | 是否破发 | TRADEDATE |
| `s_holder_cashdivbb_3y` | 近三年累计分红总额(已宣告,含回购) | TRADEDATE |
| `s_holder_category` | 机构股东类型 | REPORTDATE、Sequence |
| `s_holder_controller` | 上市公司实际控制人名称(新增) | DEALDATE |
| `s_holder_controllerattr` | 实际控制人属性 | TRADEDATE |
| `s_holder_havgchange` | 户均持股数半年增长率(新增) | D |
| `s_holder_havgpctchange` | 户均持股比例半年增长率(新增) | D |
| `s_holder_institute` | 机构股东名称 | REPORTDATE、TopN |
| `s_holder_liqmrgnsrt` | 流通股东通过融资融券持股数 | DEALDATE、TopN |
| `s_holder_liqname` | 流通股东名称 |  |
| `s_holder_liqpct` | 流通股东持股比例 | DEALDATE、Sequence |
| `s_holder_liqquantity` | 流通股东持股数量 |  |
| `s_holder_liqsharecategory` | 流通股东持股股本性质 |  |
| `s_holder_minclose20` | 前20个交易日最低收盘价(后复权) | TRADEDATE |
| `s_holder_minpb20_lyr` | 前20个交易日最低市净率(最近会计年度) | TRADEDATE |
| `s_holder_minpb20_mrq` | 前20个交易日最低市净率(最近报告期) | TRADEDATE |
| `s_holder_name` | 大股东名称 |  |
| `s_holder_name_state` | 国有大股东名称 | TRADEDATE、Sequence |
| `s_holder_nature` | 大股东性质 | DEALDATE、TopN |
| `s_holder_num` | 股东户数 | REPORTDATE |
| `s_holder_num2` | 股东户数 | REPORTDATE、Captype |
| `s_holder_num_fund` | 持股基金数 | REPORTDATE |
| `s_holder_num_i` | 持股机构数 | REPORTDATE |
| `s_holder_num_insur` | 持股保险公司数 | REPORTDATE |
| `s_holder_num_qfii` | 持股QFII数 | REPORTDATE |
| `s_holder_num_ssfund` | 持股社保基金数 | REPORTDATE |
| `s_holder_pct` | 大股东持股比例 |  |
| `s_holder_pct_liq` | 流通股东持股比例(相对总股本) | TRADEDATE、Sequence |
| `s_holder_pctbybank` | 银行持股比例(新增) | D |
| `s_holder_pctbybywmp` | 券商理财产品持股比例(新增) | D |
| `s_holder_pctbycorppension` | 企业年金持股比例(新增) | D |
| `s_holder_pctbyfinancecorp` | 财务公司持股比例(新增) | D |
| `s_holder_pctbyfund` | 基金持股比例(新增) | D |
| `s_holder_pctbygeneralcorp` | 一般法人持股比例(新增) | D |
| `s_holder_pctbyinst` | 机构持股比例合计(新增) | D |
| `s_holder_pctbyinsur` | 保险公司持股比例(新增) | D |
| `s_holder_pctbylnfcorp` | 非金融类上市公司持股比例(新增) | D |
| `s_holder_pctbyqfii` | QFII持股比例(新增) | D |
| `s_holder_pctbysec` | 券商持股比例(新增) | D |
| `s_holder_pctbyssfund` | 社保基金持股比例(新增) | D |
| `s_holder_pctbytrustcorp` | 信托公司持股比例(新增) | D |
| `s_holder_price_esop` | 员工持股计划买入价格 | TRADEDATE |
| `s_holder_price_fellowon` | 定向增发价格 | TRADEDATE |
| `s_holder_price_majorshareholders` | 大股东增持价格 | TRADEDATE |
| `s_holder_price_mh` | 管理层增持价格 | TRADEDATE |
| `s_holder_price_stockbasedcompensation` | 股权激励行权价格 | TRADEDATE |
| `s_holder_qavgchange` | 户均持股数季度增长率(新增) | D |
| `s_holder_qavgpctchange` | 户均持股比例季度增长率(新增) | D |
| `s_holder_quantity` | 大股东持股数量 |  |
| `s_holder_quantity_restricted` | 大股东持有的限售股份数 | DEALDATE、Sequence |
| `s_holder_quantity_state` | 国有大股东持股数量 | TRADEDATE、Sequence |
| `s_holder_quantity_state_tot` | 国有大股东持股总数 | TRADEDATE |
| `s_holder_rptcontroller` | 公布实际控制人名称 | DEALDATE |
| `s_holder_sharecategory` | 大股东持股股本性质 |  |
| `s_holder_sumt10pct` | 前十大股东持股比例合计 | REPORTDATE |
| `s_holder_sumt10quantity` | 前十大股东持股数量合计 | REPORTDATE |
| `s_holder_sumt5pct` | 前五大股东持股比例合计 | REPORTDATE |
| `s_holder_sumt5quantity` | 前五大股东持股数量合计 | REPORTDATE |
| `s_holder_tlttop10liqpct` | 前十大流通股东持股比例合计 | DEALDATE |
| `s_holder_top10liqquantity` | 前十大流通股东持股数量合计 |  |
| `s_holder_top10pct` | 前十大股东持股比例合计 |  |
| `s_holder_top10q_qoq` | 前十大流通股东持股数量环比 | REPORTDATE |
| `s_holder_top10quantity` | 前十大股东持股数量合计 |  |
| `s_holder_top5pct` | 前五大股东持股比例合计 | REPORTDATE |
| `s_holder_top5quantity` | 前五大股东持股数量合计 | REPORTDATE |
| `s_holder_totalbybank` | 银行持股数量(新增) | D |
| `s_holder_totalbybysec` | 券商持股数量(新增) | D |
| `s_holder_totalbybywmp` | 券商理财产品持股数量(新增) | D |
| `s_holder_totalbycorppension` | 企业年金持股数量(新增) | D |
| `s_holder_totalbyfinancecorp` | 财务公司持股数量(新增) | D |
| `s_holder_totalbyfund` | 基金持股数量(新增) | D |
| `s_holder_totalbygeneralcorp` | 一般法人持股数量(新增) | D |
| `s_holder_totalbyinst` | 机构持股数量合计(新增) | D |
| `s_holder_totalbyinsur` | 保险公司持股数量(新增) | D |
| `s_holder_totalbylnfcorp` | 非金融类上市公司持股数量(新增) | D |
| `s_holder_totalbyqfii` | QFII持股数量(新增) | D |
| `s_holder_totalbyssfund` | 社保基金持股数量(新增) | D |
| `s_holder_totalbytrustcorp` | 信托公司持股数量(新增) | D |
| `s_holder_type` | 大股东类型 | DEALDATE、TopN |
| `s_info_abstract` | 公司一句话介绍 |  |
| `s_info_address` | 注册地址 |  |
| `s_info_admincode` | 所属行政区划代码 | AdminLevelType、TRADEDATE |
| `s_info_administrativedivision` | 所属行政区划 | Level、TRADEDATE |
| `s_info_asharewindcode` | 同公司A股Wind代码 |  |
| `s_info_atmcode` | 平值期权代码 | TRADEDATE、SettlementMonth |
| `s_info_atmiv_expiration` | 期权衍生剩余到期 | TRADEDATE |
| `s_info_atmiv_mapping` | 期权衍生对应关系 | TRADEDATE |
| `s_info_auditor` | 审计机构(新增) |  |
| `s_info_auditor2` | 审计机构(支持历史) | TRADEDATE |
| `s_info_backdoor` | 是否借壳上市 |  |
| `s_info_backdoordate` | 借壳上市日期 |  |
| `s_info_banktype` | 上市公司(银行)类型 |  |
| `s_info_boardchairmen` | 董事长 | TRADEDATE |
| `s_info_bps` | 是否长期破净 | TRADEDATE |
| `s_info_briefing` | 公司简介 |  |
| `s_info_bsharecode` | 同公司B股代码(新增) |  |
| `s_info_bsharename` | 同公司B股简称(新增) |  |
| `s_info_bsharewindcode` | 同公司B股Wind代码 |  |
| `s_info_business` | 经营范围 |  |
| `s_info_capital` | 注册资本 |  |
| `s_info_cbissueornot` | 是否发行过可转债 | TRADEDATE |
| `s_info_cbname` | 同公司可转债简称 | TRADEDATE |
| `s_info_cbwindcode` | 同公司可转债Wind代码 | TRADEDATE |
| `s_info_cdmonths` | 合约月份说明,fs_info_cdmonths |  |
| `s_info_cdrornot` | 是否CDR(沪伦通) |  |
| `s_info_ceabb` | 合约英文简称 |  |
| `s_info_cename` | 合约英文名称 |  |
| `s_info_ceo` | 总经理 | TRADEDATE |
| `s_info_cfo` | 财务总监 | TRADEDATE |
| `s_info_chain` | 所属产业链板块 |  |
| `s_info_chairman` | 法人代表 |  |
| `s_info_changelt` | 涨跌幅限制 |  |
| `s_info_changelt_new` | 涨跌幅限制(支持历史) | TRADEDATE |
| `s_info_city` | 城市 |  |
| `s_info_ckgzjtxornot` | 是否企业的参控股公司为专精特新企业 |  |
| `s_info_ckgzjtxornot1` | 是否企业的参控股公司为专精特新企业(支持历史) | TRADEDATE |
| `s_info_clo` | 法律顾问(新增) |  |
| `s_info_cnscdate` | 纳入陆股通日期 | TRADEDATE |
| `s_info_code` | 交易代码 |  |
| `s_info_code2` | 月合约代码 | TRADEDATE |
| `s_info_collateral` | 是否融资融券担保物 | TRADEDATE |
| `s_info_compindex` | 是否属于重要指数成分(新增) |  |
| `s_info_compindex2` | 是否属于重要指数成份 | IndexBelong、TRADEDATE |
| `s_info_compindex3` | 是否属于指数成份 | WINDCODE3、TRADEDATE |
| `s_info_compname` | 公司名称 |  |
| `s_info_compnameeng` | 公司英文名称 |  |
| `s_info_compprename` | 公司曾用名 | TRADEDATE |
| `s_info_concept` | 所属概念板块 | TRADEDATE |
| `s_info_contractmultiplier` | 合约乘数 |  |
| `s_info_corp_aumpermanager` | 基金经理人均管理资产规模 |  |
| `s_info_corp_bondtonav` | 基金管理人债券市值占资产净值比 | REPORTDATE |
| `s_info_corp_bondtototal` | 基金管理人债券市值占资产总值比 | REPORTDATE |
| `s_info_corp_bondvalue` | 基金管理人债券投资市值 | REPORTDATE |
| `s_info_corp_bondvaluegrowth` | 基金管理人债券市值增长率 | REPORTDATE |
| `s_info_corp_cashtonav` | 基金管理人银行存款占资产净值比 | REPORTDATE |
| `s_info_corp_cashtototal` | 基金管理人银行存款占资产总值比 | REPORTDATE |
| `s_info_corp_cashvalue` | 基金管理人银行存款 | REPORTDATE |
| `s_info_corp_cashvaluegrowth` | 基金管理人现金市值增长率 | REPORTDATE |
| `s_info_corp_fundcotnachange` | 基金管理人资产净值合计变动 | REPORTDATE |
| `s_info_corp_fundtonav` | 基金管理人基金市值占资产净值比 | REPORTDATE |
| `s_info_corp_fundtototal` | 基金管理人基金市值占资产总值比 | REPORTDATE |
| `s_info_corp_fundvalue` | 基金管理人基金投资市值 | REPORTDATE |
| `s_info_corp_fundvaluegrowth` | 基金管理人基金市值增长率 | REPORTDATE |
| `s_info_corp_heavilyheldbondtobond` | 基金管理人重仓债券市值占债券投资市值比 | REPORTDATE |
| `s_info_corp_heavilyheldbondtonav` | 基金管理人重仓债券市值占资产净值比 | REPORTDATE |
| `s_info_corp_heavilyheldstocktonav` | 基金管理人重仓股票市值占资产净值比 | REPORTDATE |
| `s_info_corp_heavilyheldstocktostock` | 基金管理人重仓股票市值占股票投资市值比 | REPORTDATE |
| `s_info_corp_individualratio` | 基金管理人个人投资者持有比例 | REPORTDATE |
| `s_info_corp_individualshares` | 基金管理人个人投资者持有份额 | REPORTDATE |
| `s_info_corp_instituteratio` | 基金管理人机构投资者持有比例 | REPORTDATE |
| `s_info_corp_instituteshares` | 基金管理人机构投资者持有份额 | REPORTDATE |
| `s_info_corp_netpurchase` | 基金管理人报告期申购赎回净额 | REPORTDATE |
| `s_info_corp_netpurchasetobegin` | 基金管理人报告期净申购占期初份额比 | REPORTDATE |
| `s_info_corp_newlyissuedaum` | 基金管理人新发产品规模 | StartDate、EndDate |
| `s_info_corp_newlyissuedno` | 基金管理人新发产品数量 | StartDate、EndDate |
| `s_info_corp_otherassettonav` | 基金管理人其他资产占资产净值比 | REPORTDATE |
| `s_info_corp_otherassettototal` | 基金管理人其他资产占资产总值比 | REPORTDATE |
| `s_info_corp_otherassetvalue` | 基金管理人其他资产市值 | REPORTDATE |
| `s_info_corp_otherassetvaluegrowth` | 基金管理人其他资产市值增长率 | REPORTDATE |
| `s_info_corp_productnopermanager` | 基金经理人均管理产品数 |  |
| `s_info_corp_purchase` | 基金管理人报告期总申购份额 | REPORTDATE |
| `s_info_corp_qtrnetpurchase` | 基金管理人单季度申购赎回净额 | REPORTDATE |
| `s_info_corp_qtrnetpurchasetobegin` | 基金管理人单季度净申购占期初份额比 | REPORTDATE |
| `s_info_corp_qtrpurchase` | 基金管理人单季度总申购份额 | REPORTDATE |
| `s_info_corp_qtrredemption` | 基金管理人单季度总赎回份额 | REPORTDATE |
| `s_info_corp_redemption` | 基金管理人报告期总赎回份额 | REPORTDATE |
| `s_info_corp_stocktonav` | 基金管理人股票市值占资产净值比 | REPORTDATE |
| `s_info_corp_stocktototal` | 基金管理人股票市值占资产总值比 | REPORTDATE |
| `s_info_corp_stockvalue` | 基金管理人股票投资市值 | REPORTDATE |
| `s_info_corp_stockvaluegrowth` | 基金管理人股票市值增长率 | REPORTDATE |
| `s_info_corp_topbondcode` | 基金管理人重仓债券代码 | REPORTDATE |
| `s_info_corp_topbondname` | 基金管理人重仓债券名称 | REPORTDATE |
| `s_info_corp_topbondquantity` | 基金管理人重仓债券数量 | REPORTDATE |
| `s_info_corp_topbondvalue` | 基金管理人重仓债券市值 | REPORTDATE |
| `s_info_corp_topbondwindcode` | 基金管理人重仓债券Wind代码 | REPORTDATE |
| `s_info_corp_topgicsindustryname_sw` | 基金管理人重仓行业名称(申万) | REPORTDATE、TopN |
| `s_info_corp_topgicsindustryname_sw2021` | 基金管理人重仓行业名称(申万2021) | REPORTDATE、TopN |
| `s_info_corp_topgicsindustryvalue_sw` | 基金管理人重仓行业投资市值(申万) | REPORTDATE、TopN |
| `s_info_corp_topgicsindustryvalue_sw2021` | 基金管理人重仓行业投资市值(申万2021) | REPORTDATE、TopN |
| `s_info_corp_topgicsindustryvaluetonav_sw` | 基金管理人重仓行业投资市值占资产净值比(申万) | REPORTDATE、TopN |
| `s_info_corp_topgicsindustryvaluetonav_sw2021` | 基金管理人重仓行业投资市值占资产净值比(申万2021) | REPORTDATE、TopN |
| `s_info_corp_topindustryname_citic` | 基金管理人重仓行业名称(中信) | REPORTDATE、TopN |
| `s_info_corp_topindustryvalue_citic` | 基金管理人重仓行业投资市值(中信) | REPORTDATE、TopN |
| `s_info_corp_topindustryvaluetonav_citic` | 基金管理人重仓行业投资市值占资产净值比(中信) | REPORTDATE、TopN |
| `s_info_corp_topnbondholdingchange` | 基金管理人重仓债券持仓变动 | REPORTDATE |
| `s_info_corp_topnbondtonav` | 基金管理人前N名重仓债券市值占资产净值比 | REPORTDATE |
| `s_info_corp_topnstockholdingchange` | 基金管理人重仓股票持仓变动 | REPORTDATE |
| `s_info_corp_topnstocktonav` | 基金管理人前N名重仓股票市值占资产净值比 | REPORTDATE |
| `s_info_corp_topstockcode` | 基金管理人重仓股票代码 | REPORTDATE |
| `s_info_corp_topstockname` | 基金管理人重仓股票名称 | REPORTDATE |
| `s_info_corp_topstockquantity` | 基金管理人重仓股票数量 | REPORTDATE |
| `s_info_corp_topstockvalue` | 基金管理人重仓股票市值 | REPORTDATE |
| `s_info_corp_topstockwindcode` | 基金管理人重仓股票Wind代码 | REPORTDATE |
| `s_info_corp_warranttonav` | 基金管理人权证市值占资产净值比 | REPORTDATE |
| `s_info_corp_warranttototal` | 基金管理人权证市值占资产总值比 | REPORTDATE |
| `s_info_corp_warrantvalue` | 基金管理人权证投资市值 | REPORTDATE |
| `s_info_corp_warrantvaluegrowth` | 基金管理人权证市值增长率 | REPORTDATE |
| `s_info_corpscale` | 企业规模 | TRADEDATE |
| `s_info_country` | 所属国家 |  |
| `s_info_cpv` | 资产评估机构(新增) |  |
| `s_info_crtindpdirector` | 公司独立董事(现任)(新增) |  |
| `s_info_csrcjurisdiction` | 所属证监会辖区 | TRADEDATE |
| `s_info_cstype` | 所属中资股类型 |  |
| `s_info_currency` | 交易币种 |  |
| `s_info_cusipnumber` | Cusip代码 |  |
| `s_info_ddate` | 交割日期 |  |
| `s_info_delistdate` | 摘牌日期(新增) |  |
| `s_info_delistreason` | 终止上市原因 |  |
| `s_info_deliveryfee` | 期货交割手续费 | TRADEDATE |
| `s_info_depositarybank` | 存托机构 | TRADEDATE |
| `s_info_director` | 公司董事 |  |
| `s_info_discloser` | 信息披露人 |  |
| `s_info_discloser1` | 董事会秘书 | TRADEDATE |
| `s_info_dlmonth` | 交割月份 |  |
| `s_info_dsceval` | 上市公司信息披露考评 | Year |
| `s_info_eaname` | 证券扩位简称 |  |
| `s_info_earning` | 是否尚未盈利 |  |
| `s_info_email` | 公司电子邮件地址 |  |
| `s_info_employee` | 员工总数 |  |
| `s_info_employee_pc` | 母公司员工人数 | TRADEDATE |
| `s_info_englishname` | 证券英文名称 |  |
| `s_info_exchange_cn` | 交易所中文名称,s_info_exchange_CN() |  |
| `s_info_exchmarket` | 上市地点(新增) |  |
| `s_info_executives` | 公司高管 |  |
| `s_info_exname` | 交易所简称 |  |
| `s_info_fax` | 公司传真 |  |
| `s_info_featuredliststd` | 精选层准入标准 |  |
| `s_info_ficode` | 金融机构分类编码 | Level |
| `s_info_firstincentivedate` | 首次股权激励实施日期 |  |
| `s_info_founddate` | 成立日期 |  |
| `s_info_founddate1` | 成立日期 |  |
| `s_info_frmindpdirector` | 公司独立董事(历任)(新增) |  |
| `s_info_ftdate` | 开始交易日 |  |
| `s_info_ftdate_new` | 开始交易日(支持历史) | TRADEDATE |
| `s_info_ftmargins` | 最初交易保证金 |  |
| `s_info_funduse` | 募集资金用途 |  |
| `s_info_gdrname` | 同公司GDR简称 |  |
| `s_info_gdrwindcode` | 同公司GDRWind代码 |  |
| `s_info_gxjsornot` | 是否高新技术企业 |  |
| `s_info_hkpcode` | 同公司港股并行Wind代码 |  |
| `s_info_hotconcept` | 所属热门概念 | TRADEDATE |
| `s_info_hsharecode` | 同公司H股代码 |  |
| `s_info_incentiveornot` | 是否有股权激励计划 |  |
| `s_info_indexcode_amac` | 所属AMAC行业指数代码 | TRADEDATE |
| `s_info_indexcode_citic` | 所属中信行业指数代码 | TRADEDATE、TYPE |
| `s_info_indexcode_cjsc` | 所属长江行业指数代码 | TRADEDATE、TYPE |
| `s_info_indexcode_cn` | 所属国证行业指数代码 | TRADEDATE、TYPE |
| `s_info_indexcode_sw` | 所属申万行业指数代码 | TRADEDATE、TYPE |
| `s_info_indexcode_wind` | 所属Wind行业指数代码 | TRADEDATE、TYPE |
| `s_info_indexcode_windthematic` | 所属Wind主题行业指数代码 | TRADEDATE |
| `s_info_indexname_amac` | 所属AMAC行业指数名称 | TRADEDATE |
| `s_info_indexweight` | 所属指数权重 | TRADEDATE、RelatedIndexType |
| `s_info_industry` | 所属行业，s_info_industry |  |
| `s_info_industry2` | 所属行业名称(支持历史) | TYPE、IndustryStandard、TRADEDATE |
| `s_info_industry_citic` | 所属中信行业名称 | TRADEDATE、TYPE |
| `s_info_industry_citiccode` | 所属中信行业代码 | TRADEDATE、TYPE |
| `s_info_industry_citicorigincode` | 所属中信行业原始代码 | TRADEDATE、TYPE |
| `s_info_industry_cjsc` | 所属长江行业名称 | TRADEDATE、TYPE |
| `s_info_industry_cn` | 所属国证行业名称 | TRADEDATE、TYPE |
| `s_info_industry_cncode` | 所属国证行业代码 | TRADEDATE、TYPE |
| `s_info_industry_csi` | 所属中证行业名称 | TRADEDATE、TYPE |
| `s_info_industry_csicode` | 所属中证行业代码 | TRADEDATE、TYPE |
| `s_info_industry_csrc` | 证监会行业-中文 |  |
| `s_info_industry_csrc12` | 所属证监会行业(新) |  |
| `s_info_industry_csrc12_n` | 所属证监会行业名称 | TRADEDATE、TYPE |
| `s_info_industry_csrc2023` | 所属挂牌公司管理型行业名称(2023) | TRADEDATE、TYPE |
| `s_info_industry_csrccode` | 证监会行业-代码 |  |
| `s_info_industry_csrccode12` | 所属证监会行业代码 | TRADEDATE |
| `s_info_industry_csrccode2023` | 所属挂牌公司管理型行业代码(2023) | TRADEDATE、TYPE |
| `s_info_industry_fu` | 期货合约所属行业 |  |
| `s_info_industry_gics` | GICS行业-中文 |  |
| `s_info_industry_gicscode` | GICS行业-代码 |  |
| `s_info_industry_gicseng` | GICS行业-英文 |  |
| `s_info_industry_gx` | 所属国信行业(新增) |  |
| `s_info_industry_nc` | 所属国民经济行业分类 | TRADEDATE |
| `s_info_industry_nccode` | 所属国民经济行业代码 | TRADEDATE、TYPE |
| `s_info_industry_neeqconcept` | 所属新三板概念类板块 |  |
| `s_info_industry_neeqgics` | 所属挂牌公司投资型行业名称 | TYPE、TRADEDATE |
| `s_info_industry_neeqgicscode` | 所属挂牌公司投资型行业代码 | TYPE、TRADEDATE |
| `s_info_industry_neeqgicscode_inv` | 所属挂牌公司投资型行业代码 | TYPE、TRADEDATE |
| `s_info_industry_sw` | 申万行业 |  |
| `s_info_industry_sw_2021` | 所属申万行业名称(2021) | TRADEDATE、TYPE |
| `s_info_industry_swcode` | 所属申万行业代码 | TRADEDATE、TYPE |
| `s_info_industry_swcode_2021` | 所属申万行业代码(2021) | TRADEDATE、TYPE |
| `s_info_industry_sworigincode` | 所属申万行业原始代码 | TRADEDATE、TYPE |
| `s_info_industry_sworigincode_2021` | 所属申万行业原始代码(2021) | TRADEDATE、TYPE |
| `s_info_industrycode` | 所属行业代码(支持历史) | IndustryStandard、TYPE、TRADEDATE |
| `s_info_industryname` | 所属行业板块代码(支持历史) | IndustryStandard、TYPE、TRADEDATE |
| `s_info_institutiontype` | 金融机构类型 |  |
| `s_info_isincode` | ISIN代码 |  |
| `s_info_largecommodity` | 所属大宗商品概念板块 | TRADEDATE |
| `s_info_latestconcept` | 所属最新概念 | TRADEDATE |
| `s_info_latestincentivedate` | 最新股权激励公布时间 | TRADEDATE |
| `s_info_latestincimplementdate` | 最新一次股权激励实施日期 | TRADEDATE |
| `s_info_lddate` | 最后交割日 |  |
| `s_info_lddate_new` | 最后交割日(支持历史) | TRADEDATE |
| `s_info_legalrepresentative` | 法定代表人 | DEALDATE |
| `s_info_lei` | LEI编码 |  |
| `s_info_lic` | 经办律师 |  |
| `s_info_list` | 是否上市 |  |
| `s_info_liststd` | 所属科创板上市标准 |  |
| `s_info_long_margin` | 期货多头保证金(支持历史) | TRADEDATE |
| `s_info_lprice` | 挂牌基准价 |  |
| `s_info_ltdate` | 最后交易日 |  |
| `s_info_ltdate_new` | 最后交易日(支持历史) | TRADEDATE |
| `s_info_ltdated` | 最后交易日说明 |  |
| `s_info_maint_margin` | 期权维持保证金(支持历史) | TRADEDATE |
| `s_info_majorproductname` | 主营产品名称(新增) |  |
| `s_info_majorproducttype` | 主营产品类型(新增) |  |
| `s_info_margin` | 交易保证金 |  |
| `s_info_margin_new` | 交易保证金(支持历史) | TRADEDATE |
| `s_info_marginornot` | 是否融资融券标的 | TRADEDATE |
| `s_info_market` | 交易所英文简称 |  |
| `s_info_marketmakedate` | 做市首日 |  |
| `s_info_media` | 信息指定披露媒体 |  |
| `s_info_mfprice` | 最小变动价位 |  |
| `s_info_mfprice1` | 最小变动价位(支持历史) | TRADEDATE |
| `s_info_mkt` | 上市板 |  |
| `s_info_mktcharacter` | 所属市场特征板块 |  |
| `s_info_mupc` | 最小价格变动单位 |  |
| `s_info_name` | 证券简称 |  |
| `s_info_name1` | 证券简称(支持历史) | TRADEDATE |
| `s_info_nature` | 公司属性 |  |
| `s_info_nature1` | 公司属性 | TRADEDATE |
| `s_info_neeqsharewindcode` | 同公司新三板代码 |  |
| `s_info_noplat` | 息前税后经营利润(NOPLAT) | REPORTDATE |
| `s_info_office` | 办公地址 |  |
| `s_info_organizationcode` | 组织机构代码 |  |
| `s_info_parallelcode` | 是否并行代码 |  |
| `s_info_phone` | 公司电话 |  |
| `s_info_prename` | 证券曾用名 |  |
| `s_info_prf_valuedate` | 优先股起息日 |  |
| `s_info_province` | 省份 |  |
| `s_info_punit` | 报价单位 |  |
| `s_info_pzjtxornot` | 是否省级专精特新企业 | TRADEDATE |
| `s_info_registernumber` | 工商登记号(新增) |  |
| `s_info_relatedbond` | 公司发行债券一览 |  |
| `s_info_relatedsecurity` | 公司发行证券一览 |  |
| `s_info_relatedshare` | 公司发行股票一览 |  |
| `s_info_relationcode` | 跨市场代码 |  |
| `s_info_riskadmonition_date` | 戴帽摘帽时间(新增) |  |
| `s_info_riskwarning` | 是否属于风险警示板 | TRADEDATE |
| `s_info_riskwarningpre` | 可能被实施退市风险警示 | TRADEDATE |
| `s_info_sar` | 证券事务代表 | TRADEDATE |
| `s_info_scalestyle` | 所属规模风格类型 | TRADEDATE |
| `s_info_sccode` | 标准合约代码 |  |
| `s_info_sedolcode` | SEDOL代码(新增) |  |
| `s_info_sei` | 所属战略性新兴产业分类 | TRADEDATE、TYPE |
| `s_info_short_margin` | 期货空头保证金(支持历史) | TRADEDATE |
| `s_info_shsc` | 是否沪港通买入标的 | TRADEDATE |
| `s_info_shsc2` | 是否深港通买入标的 | TRADEDATE |
| `s_info_st` | 特别处理类型 | TRADEDATE |
| `s_info_status` | 证券存续状态 |  |
| `s_info_stockclass` | 股票种类(新增) |  |
| `s_info_styleindexcode_citic` | 所属中信风格指数代码 | TRADEDATE |
| `s_info_styleindexname_citic` | 所属中信风格指数名称 | TRADEDATE |
| `s_info_sucdirector` | 公司董事(历任) | TRADEDATE |
| `s_info_sucexecutives` | 公司高管(历任) | TRADEDATE |
| `s_info_sucindpdirector` | 公司独立董事(历任) | TRADEDATE |
| `s_info_sucsupervisor` | 公司监事(历任) | TRADEDATE |
| `s_info_supervisor` | 公司监事 |  |
| `s_info_swapwindcode` | 摘牌换股标的Wind代码 |  |
| `s_info_swiftcode` | SWIFT编码 |  |
| `s_info_thematicindustry_sib` | 所属科创板主题行业 | TRADEDATE、TYPE |
| `s_info_thematicindustry_wind` | 所属Wind主题行业名称 | TRADEDATE |
| `s_info_thours` | 交易时间说明 |  |
| `s_info_thours2` | 交易时间说明 | TRADEDATE |
| `s_info_todaypositionfee` | 期货平今手续费 | TRADEDATE |
| `s_info_tradecode` | 期权交易代码 | TRADEDATE |
| `s_info_transactionfee` | 期货交易手续费 | TRADEDATE |
| `s_info_transfertype` | 转让方式 | TRADEDATE |
| `s_info_tunit` | 交易单位 |  |
| `s_info_type` | 证券类型 |  |
| `s_info_typeii` | 证券类型(细类) |  |
| `s_info_underlyingtype` | 标的类型 |  |
| `s_info_underlyingwindcode` | 基础证券Wind代码 |  |
| `s_info_ussharename` | 同公司美股简称 |  |
| `s_info_ussharewindcode` | 同公司美股Wind代码 |  |
| `s_info_vic` | 经办评估人员 |  |
| `s_info_vieornot` | 是否VIE结构 |  |
| `s_info_vote` | 是否存在投票权差异 | TRADEDATE |
| `s_info_website` | 公司网站 |  |
| `s_info_wicscode2023` | 所属Wind行业代码(2023) | TYPE、TRADEDATE |
| `s_info_wicscode2024` | 所属Wind行业代码(2023) ,s_info_wicscode2023 | TRADEDATE、TYPE |
| `s_info_wicsname2023` | 所属Wind行业名称(2023) | TYPE、TRADEDATE |
| `s_info_wicsname2024` | 所属Wind行业名称(2023) ,s_info_wicsname2023 | TRADEDATE、TYPE |
| `s_info_windcode` | Wind代码 |  |
| `s_info_zipcode` | 邮编 |  |
| `s_info_zjtxitselfornot` | 是否企业本身为专精特新 |  |
| `s_info_zjtxitselfornot1` | 是否企业本身为专精特新(支持历史) | TRADEDATE |
| `s_info_zjtxornot` | 是否专精特新企业 |  |
| `s_info_zjtxornot1` | 是否专精特新企业(支持历史) | TRADEDATE |
| `s_institution_purchasenum` | 机构席位买入次数 | StartDate、DATE |
| `s_intpositionchg_impshareholder_secmarket` | 重要股东二级市场交易区间持仓市值变动 | StartDate、DATE |
| `s_ipo_allotmentsubjects` | 配售对象名称(新增) | InstitutionType、TYPE |
| `s_ipo_allotway` | 网下投资者分类配售方式 |  |
| `s_ipo_amount` | 首发数量 |  |
| `s_ipo_amount_est` | 预计发行股数 |  |
| `s_ipo_amtbyplacing` | 上网发行数量(新增) |  |
| `s_ipo_amttofund` | 首发向基金配售数量(新增) |  |
| `s_ipo_amttoinscorp` | 向保险公司配售数量(新增) |  |
| `s_ipo_amttoinstinvestor` | 向战略投资者配售数量(新增) |  |
| `s_ipo_amttojur` | 向一般法人配售数量(新增) |  |
| `s_ipo_amttoother` | 其它发行数量(新增) |  |
| `s_ipo_anncedate` | 发行公告日(新增) |  |
| `s_ipo_anncelstdate` | 上市公告日(新增) |  |
| `s_ipo_applicationdeadline` | 网下投资者报备截止日 |  |
| `s_ipo_applicationdeadline_time` | 网下投资者报备截止时间 |  |
| `s_ipo_apprtoreg` | 是否核准制平移至注册制 |  |
| `s_ipo_assetdate` | 新股申购资产规模报备日 |  |
| `s_ipo_assetdate_lstmon` | 新股申购资产规模报备日(最近一个月末) |  |
| `s_ipo_audit_cpa` | 首发签字会计师 |  |
| `s_ipo_auditfee` | 首发审计费用 |  |
| `s_ipo_auditor` | 首发审计机构 |  |
| `s_ipo_avgprice` | 上市首日成交均价(新增) |  |
| `s_ipo_beyondactualcollec` | 首发超募资金(新增) |  |
| `s_ipo_bfund` | 网上冻结资金 |  |
| `s_ipo_capeffacc` | 市值配售有效申购户数(新增) |  |
| `s_ipo_capeffamt` | 市值配售有效申购股数(新增) |  |
| `s_ipo_cappaydate` | 网上申购缴款日 |  |
| `s_ipo_capplacingdate` | 市值配售日期(新增) |  |
| `s_ipo_capratio` | 市值配售发行中签率(新增) |  |
| `s_ipo_cashamt` | 现金申购发行数量(新增) |  |
| `s_ipo_casheffacc` | 现金申购有效申购户数(新增) |  |
| `s_ipo_cashratio` | 现金申购中签率(新增) |  |
| `s_ipo_cashsubisdate` | 现金申购发行日期(新增) |  |
| `s_ipo_close` | 上市首日收盘价 |  |
| `s_ipo_collection` | 首发募集资金 |  |
| `s_ipo_collection_acct` | 首发募集资金监管银行账户 |  |
| `s_ipo_collection_bal` | 募集资金专项账户余额 | TRADEDATE |
| `s_ipo_collection_bank` | 首发募集资金监管银行名称 |  |
| `s_ipo_collection_oldshares` | 股东售股金额 |  |
| `s_ipo_collection_total` | 募集资金总额(含股东售股) |  |
| `s_ipo_collection_unused` | 首发未投入资金金额 |  |
| `s_ipo_commissionrate` | 新股配售经纪佣金费率 |  |
| `s_ipo_comppe_deducted` | 可比上市公司PE均值(扣非后) |  |
| `s_ipo_deputyundr` | 副主承销商(新增) |  |
| `s_ipo_dilutedpe` | 首发市盈率(摊薄)(新增) |  |
| `s_ipo_distor` | 首发分销商(新增) |  |
| `s_ipo_draftsprospectusdate` | IPO申报稿首次报送时间 |  |
| `s_ipo_expectedcollection` | 首发预计募集资金(新增) |  |
| `s_ipo_expectednetcollection` | 首发预计募集资金净额 |  |
| `s_ipo_expense` | 首发发行费用 |  |
| `s_ipo_feedbackdate` | IPO首次反馈日期 |  |
| `s_ipo_firstinquirydate` | IPO首次问询日期 |  |
| `s_ipo_firstmrqdate` | 初始申报基准日 |  |
| `s_ipo_fndisdate` | 向基金配售部分上市日期(新增) |  |
| `s_ipo_giveup` | 网上放弃认购数量 |  |
| `s_ipo_handlingdate` | IPO受理日期 |  |
| `s_ipo_handlingdate_s` | IPO首次受理日期 |  |
| `s_ipo_high` | 上市首日最高价(新增) |  |
| `s_ipo_idc` | 首发信息披露费 |  |
| `s_ipo_iecresultdate` | IPO发审委审核通过公告日期 |  |
| `s_ipo_industrype` | 首发时所属行业市盈率 |  |
| `s_ipo_initialexpense` | 初始发行费用 |  |
| `s_ipo_inq_anncedate` | 初步询价公告日 |  |
| `s_ipo_inq_enddate` | 初步询价截止日 |  |
| `s_ipo_inq_startdate` | 初步询价起始日 |  |
| `s_ipo_inqresultdate` | 初步询价结果公告日 |  |
| `s_ipo_inquiriesnum` | IPO问询次数 |  |
| `s_ipo_inquiry` | 初步询价参与询价总家数(新增) |  |
| `s_ipo_inquiry_excl` | 剔除无效和最高报价后询价对象家数 |  |
| `s_ipo_inquiry_inst` | 初步询价参与询价机构家数(新增) |  |
| `s_ipo_inquirydate_new` | IPO问询日期(最新轮次) |  |
| `s_ipo_inquirymv_caldate` | 询价市值计算参考日 |  |
| `s_ipo_inquirymv_min` | 网下询价市值门槛 |  |
| `s_ipo_inquirymv_min_a` | 网下询价市值门槛(A类) |  |
| `s_ipo_inquirymv_min_themestrt` | 网下询价市值门槛(主题与战略) |  |
| `s_ipo_inscorpisdate` | 向保险公司配售上市日期(新增) |  |
| `s_ipo_instisdate` | 向战略投资者配售部分上市日期(新增) |  |
| `s_ipo_intercordtor` | 首发国际协调人(新增) |  |
| `s_ipo_invention` | 发明专利个数 |  |
| `s_ipo_investamount` | 近三年研发投入累计额 |  |
| `s_ipo_investorrefunddate` | 投资者退款日期 |  |
| `s_ipo_invsshares_a` | 网下高于有效报价上限的申购量 |  |
| `s_ipo_invssharespct_a` | 网下高于有效报价上限的申购量比例 |  |
| `s_ipo_issuedate` | 首发发行日期(新增) |  |
| `s_ipo_issuingsystem` | 发行制度 |  |
| `s_ipo_issuvolplanned` | 计划发行总数 |  |
| `s_ipo_jurisdate` | 向一般法人配售上市日期(新增) |  |
| `s_ipo_lawer` | 首发经办律师 |  |
| `s_ipo_lawfee` | 首发法律费用 |  |
| `s_ipo_lawfirm` | 首发经办律所 |  |
| `s_ipo_leadundr` | 首发主承销商(新增) |  |
| `s_ipo_leadundr_n` | 主办券商(持续督导) |  |
| `s_ipo_leadundr_n1` | 主办券商(持续督导) | TRADEDATE |
| `s_ipo_legaladvisor` | 首发保荐人律师 |  |
| `s_ipo_limitupdays` | 新股未开板涨停板天数 |  |
| `s_ipo_limitupopendate` | 开板日 |  |
| `s_ipo_limitupopendate_avgprice` | 新股开板日成交均价 |  |
| `s_ipo_limitupopendate_close` | 新股开板日收盘价 |  |
| `s_ipo_limitupopendate_pctchange` | 新股开板日涨跌幅 |  |
| `s_ipo_liqdiscount` | 限售股流动性折扣 | TRADEDATE、RestrictedPeriod |
| `s_ipo_listdays` | 上市天数(新增) |  |
| `s_ipo_listdayvolume` | 上市首日成交量(新增) |  |
| `s_ipo_listeddate` | 首发上市日期 |  |
| `s_ipo_lotteryrate_abc` | 网下投资者中签率 | InstitutionType |
| `s_ipo_lotwinningnumber` | 询价机构获配数量(新增) | InstitutionType、TYPE |
| `s_ipo_low` | 上市首日最低价(新增) |  |
| `s_ipo_lstnum` | 首日上市数量(新增) |  |
| `s_ipo_marketmaker` | 做市商名称 | TRADEDATE |
| `s_ipo_medianprice` | 网下申报价格中位数 | InstitutionType |
| `s_ipo_mrqdate` | 申报基准日 |  |
| `s_ipo_mvregdate` | 网上市值申购登记日 |  |
| `s_ipo_netcollection` | 首发实际募集资金 |  |
| `s_ipo_netcollection_est` | 预计募投项目投资总额 |  |
| `s_ipo_newshares` | 新股发行数量 |  |
| `s_ipo_newshares_initial` | 新股初始发行数量 |  |
| `s_ipo_ninstitutional_abc` | 网下投资者获配家数 | InstitutionType |
| `s_ipo_nominator` | 首发上市推荐人(新增) |  |
| `s_ipo_nooa` | 网上发行获配户数 |  |
| `s_ipo_npctchange` | 上市后N日涨跌幅(新增) |  |
| `s_ipo_nturn` | 上市后N日换手率(新增) |  |
| `s_ipo_numoffplacements` | 网下配售数量 |  |
| `s_ipo_offering` | 网下募集资金(新增) |  |
| `s_ipo_offsubpaydate` | 网下申购缴款日 |  |
| `s_ipo_oldshares` | 股东售股数量 |  |
| `s_ipo_oldsharesratio` | 老股转让比例 |  |
| `s_ipo_onsite` | IPO现场检查公告日期 |  |
| `s_ipo_op_amount` | 网下冻结资金 |  |
| `s_ipo_op_downlimit` | 网下申购下限 |  |
| `s_ipo_op_enddate` | 网下申购截止日期 |  |
| `s_ipo_op_minofchg` | 最低累进申购数量 |  |
| `s_ipo_op_numoffring` | 网下申购报价数量 |  |
| `s_ipo_op_numofinq` | 网下申购询价对象家数 |  |
| `s_ipo_op_numofpmt` | 网下申购配售对象家数 |  |
| `s_ipo_op_oversubratio` | 首发网下超额认购倍数 |  |
| `s_ipo_op_startdate` | 网下申购起始日期 |  |
| `s_ipo_op_uplimit` | 网下申购上限 |  |
| `s_ipo_op_volume` | 网下申购总量 |  |
| `s_ipo_op_volume_abc` | 网下投资者申购数量 | InstitutionType |
| `s_ipo_open` | 上市首日开盘价 |  |
| `s_ipo_or_startdate` | 网下报备起始日 |  |
| `s_ipo_otc_cash_pct` | 网下申购配售比例(新增) |  |
| `s_ipo_otherenddate` | 其它发行截止日期(新增) |  |
| `s_ipo_otherstartdate` | 其它发行起始日期(新增) |  |
| `s_ipo_overallot_amount` | 超额配售募资净额 |  |
| `s_ipo_overallot_prop_vol` | 拟超额配售数量 |  |
| `s_ipo_overallot_vol` | 超额配售数量 |  |
| `s_ipo_ovrsubratio` | 超额认购倍数(新增) |  |
| `s_ipo_par` | 发行时每股面值 |  |
| `s_ipo_parvalue` | 面值(新增) |  |
| `s_ipo_pb` | 发行市净率 |  |
| `s_ipo_pb_overallotbf` | 发行市净率(超额配售前) |  |
| `s_ipo_pctchange` | 上市首日涨跌幅(新增) |  |
| `s_ipo_pdate` | 网下定价日 |  |
| `s_ipo_pe` | 首发市盈率 | TYPE |
| `s_ipo_pebeforeoverallot` | 首发市盈率(超额配售前) |  |
| `s_ipo_placing_excl` | 剔除无效和最高报价后配售对象家数 |  |
| `s_ipo_placingdate` | 网下配售结果公告日 |  |
| `s_ipo_poc_offline` | 网下发行数量(回拨前) |  |
| `s_ipo_poc_online` | 网上发行数量(回拨前) |  |
| `s_ipo_pohqe` | 被剔除的最高价申报量占比 |  |
| `s_ipo_poqe` | 被剔除的申报量占比 |  |
| `s_ipo_preplacingdate` | 初步配售结果公告日 |  |
| `s_ipo_preprice` | 发行前均价 |  |
| `s_ipo_price` | 首发价格 |  |
| `s_ipo_price_max` | 发行价格上限 |  |
| `s_ipo_price_min` | 发行价格下限(底价) |  |
| `s_ipo_pshare_restrictpct` | 网下投资者分类配售限售比例 |  |
| `s_ipo_pshares_abc` | 网下投资者获配数量 | InstitutionType |
| `s_ipo_pshares_if` | 网下保险资金获配数量 |  |
| `s_ipo_pshares_mf` | 网下公募基金获配数量 |  |
| `s_ipo_pshares_sp` | 网下企业年金获配数量 |  |
| `s_ipo_pshares_ssf` | 网下社保基金获配数量 |  |
| `s_ipo_psharesmax_abc` | 网下投资者最高获配数量 | InstitutionType |
| `s_ipo_psharespct_abc` | 网下投资者配售数量占比 | InstitutionType |
| `s_ipo_puboffrdate` | 招股公告日(新增) |  |
| `s_ipo_purchasecode` | 网上申购代码 |  |
| `s_ipo_qnum_inquiry` | IPO问询函中问题数量 |  |
| `s_ipo_rdinvest` | 近三年研发投入占比 |  |
| `s_ipo_rdperson` | 研发人员占比 |  |
| `s_ipo_reallocationpct` | 回拨比例 |  |
| `s_ipo_refunddate` | 网上申购款解冻日 |  |
| `s_ipo_regist_date` | 注册成功日 |  |
| `s_ipo_restrictedvalue` | 限售股价值 | TRADEDATE、RestrictedPeriod |
| `s_ipo_resultdate` | 首发发行结果公告日(新增) |  |
| `s_ipo_revenue` | 近一年营收额 |  |
| `s_ipo_revenuegrowth` | 近三年营收复合增长率 |  |
| `s_ipo_rsdate_e` | 现场推介截止日期 |  |
| `s_ipo_rsdate_s` | 现场推介起始日期 |  |
| `s_ipo_samt_uplimit` | 网上申购资金上限 |  |
| `s_ipo_siallotment` | 战略配售获配股份数 |  |
| `s_ipo_siallotmentratio` | 战略配售获配股份占比 |  |
| `s_ipo_sponsor` | 首发保荐机构 |  |
| `s_ipo_sponsor_member` | 首发保荐机构项目组成员 |  |
| `s_ipo_sponsorrepresentative` | 首发保荐人代表 |  |
| `s_ipo_sprice_max` | 初步询价上限 |  |
| `s_ipo_sprice_min` | 初步询价下限 |  |
| `s_ipo_sratio` | 初步询价申购倍数(回拨前) |  |
| `s_ipo_sshares_t` | 初步询价申购总量 |  |
| `s_ipo_sshares_uplimit` | 网上申购数量上限 |  |
| `s_ipo_starposi` | 科创属性评价标准 |  |
| `s_ipo_subamtbyplacing` | 二级市场配售发行数量(新增) |  |
| `s_ipo_subbydistr` | 承销商认购余额(新增) |  |
| `s_ipo_submit_regist_date` | 提交注册日 |  |
| `s_ipo_subscription_excl` | 剔除无效和最高报价后申购总量 |  |
| `s_ipo_subscriptionprice` | 初步询价申购价格量(新增) | InstitutionType、TYPE |
| `s_ipo_subscriptionshares` | 初步询价申购数量(新增) | InstitutionType、TYPE |
| `s_ipo_termdate` | IPO终止审查日期 |  |
| `s_ipo_totcapafterissue` | 首发后总股本(上市日)(新增) |  |
| `s_ipo_totcapafterissue_est` | 预计发行后总股本 |  |
| `s_ipo_totcapbeforeissue` | 首发前总股本(新增) |  |
| `s_ipo_tradedays` | 上市交易天数 | TRADEDATE |
| `s_ipo_turn` | 上市首日换手率(新增) |  |
| `s_ipo_tutor` | 挂牌企业上市辅导券商 |  |
| `s_ipo_tutoring_enddate` | 挂牌企业上市辅导结束日期 |  |
| `s_ipo_tutoring_startdate` | 挂牌企业上市辅导开始日期 |  |
| `s_ipo_type` | 首发发行方式(新增) |  |
| `s_ipo_underwriterallotment` | 主承销商战略获配股份数 |  |
| `s_ipo_underwriterallotmentratio` | 主承销商战略获配股份占比 |  |
| `s_ipo_underwritingfees_shareholder` | 售股股东应摊承销与保荐费用 |  |
| `s_ipo_underwritingratio` | 包销比例 |  |
| `s_ipo_undrtype` | 首发承销方式(新增) |  |
| `s_ipo_usfees` | 首发承销保荐费用 |  |
| `s_ipo_volume` | 上市首日成交额(新增) |  |
| `s_ipo_vsprice_max` | 网下有效报价上限 |  |
| `s_ipo_vsprice_min` | 网下有效报价下限 |  |
| `s_ipo_vsratio` | 网下超额认购倍数(回拨前) |  |
| `s_ipo_vsshares` | 网下有效报价申购量 |  |
| `s_ipo_vsshares_s` | 网上发行有效申购数量 |  |
| `s_ipo_vssharespct` | 网下有效报价申购量比例 |  |
| `s_ipo_vssharespct_abc` | 网下投资者有效申购数量占比 | InstitutionType |
| `s_ipo_weightedpe` | 首发市盈率(加权)(新增) |  |
| `s_ipo_wgtavgprice` | 网下申报价格加权平均数 | InstitutionType |
| `s_ipo_wpipreleasingdateup` | IPO申报预披露更新日 |  |
| `s_ir_fcs` | 基金公司调研次数 | StartDate、EndDate |
| `s_ir_irfd` | 机构调研首日 |  |
| `s_ir_irld` | 机构调研最新日 |  |
| `s_ir_nofci` | 基金公司调研家数 | StartDate、EndDate |
| `s_ir_noiami` | 保险资管调研家数 | StartDate、EndDate |
| `s_ir_noifoc` | 其他公司调研家数 | StartDate、EndDate |
| `s_ir_noii` | 机构调研家数 | StartDate、EndDate |
| `s_ir_noiifi` | 外资机构调研家数 | StartDate、EndDate |
| `s_ir_noiiii` | 投资机构调研家数 | StartDate、EndDate |
| `s_ir_noiisc` | 证券公司调研家数 | StartDate、EndDate |
| `s_ir_noinami` | 保险资管调研家数 | StartDate、EndDate |
| `s_ir_nomi` | 媒体(政府)调研家数 | StartDate、EndDate |
| `s_ir_nopi` | 个人调研家数 | StartDate、EndDate |
| `s_ir_nos` | 被调研总次数 | StartDate、EndDate |
| `s_ir_nosboc` | 其他公司调研次数 | StartDate、EndDate |
| `s_ir_noscbsc` | 证券公司调研次数 | StartDate、EndDate |
| `s_ir_nosfso` | 特定对象调研次数 | StartDate、EndDate |
| `s_ir_nosofi` | 外资机构调研次数 | StartDate、EndDate |
| `s_ir_nosoiam` | 保险资管调研次数 | StartDate、EndDate |
| `s_ir_nosoii` | 投资机构调研次数 | StartDate、EndDate |
| `s_ir_nosoinam` | 保险资管调研次数 | StartDate、EndDate |
| `s_ir_ocmr` | 调研最多的其他公司 | StartDate、EndDate |
| `s_ir_tmrfc` | 调研最多的基金公司 | StartDate、EndDate |
| `s_ir_tmrfi` | 调研最多的外资机构 | StartDate、EndDate |
| `s_ir_tmriam` | 调研最多的保险资管 | StartDate、EndDate |
| `s_ir_tmrii` | 调研最多的投资机构 | StartDate、EndDate |
| `s_ir_tmrinam` | 调研最多的保险资管 | StartDate、EndDate |
| `s_ir_tmssc` | 调研最多的证券公司 | StartDate、EndDate |
| `s_is` | 26版财务指标 | ITEMSCODE、YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_amortinssvcco` | 摊回保险服务费用 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_apportcedprem` | 分出保费的分摊 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_cedreinsfingl` | 分出再保险财务损益 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_inssvccosts` | 保险服务费用 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_inssvcincome` | 保险服务收入 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_is_uwfinloss` | 承保财务损失 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `s_issuer_regcapitalcur` | 注册资本币种 |  |
| `s_liqholder_num` | 流通股东户数 | TRADEDATE |
| `s_margin_guaranteedstocksmarketvalue` | 融资融券担保股票市值 | TRADEDATE |
| `s_margin_marketvalueratio` | 担保证券市值占该证券总市值比重 | TRADEDATE |
| `s_margin_purchasewithborrowedmoney` | 融资买入额(新增) |  |
| `s_margin_purchasewithborrowedmoney_net` | 融资净买入额 | TRADEDATE |
| `s_margin_repaymentofborrowedsec` | 融券偿还量(新增) |  |
| `s_margin_repaymenttobroker` | 融资偿还额(新增) |  |
| `s_margin_salerepayamount` | 融券偿还额 | TRADEDATE |
| `s_margin_salesofborrowedsec` | 融券卖出量(新增) |  |
| `s_margin_saletradingamount` | 融券卖出额 | TRADEDATE |
| `s_margin_seclendingbalance` | 融券余额(新增) |  |
| `s_margin_seclendingbalancevolume` | 融券余量(新增) |  |
| `s_margin_shortamountint` | 区间融券卖出额 | StartDate、EndDate |
| `s_margin_shortamountrepayint` | 区间融券偿还额 | StartDate、EndDate |
| `s_margin_shortselleopbal` | 转融券期末余额 | TRADEDATE |
| `s_margin_sinstccolltrlratio` | 单一股票担保物比例 | TRADEDATE |
| `s_margin_tradingandseclendingbalance` | 融资融券余额(新增) |  |
| `s_margin_tradingbalance` | 融资余额(新增) |  |
| `s_mfd_buyamt` | 买入成交额 | StartDate、EndDate、TYPE |
| `s_mfd_buyamt_a` | 主动买入额 | TRADEDATE、TYPE |
| `s_mfd_buyamt_at` | 主动买入额(全单) | TRADEDATE |
| `s_mfd_buyamt_d` | 流入额 | TRADEDATE、TYPE |
| `s_mfd_buyord` | 流入单数 | TRADEDATE、TYPE |
| `s_mfd_buyvol` | 买入成交量 | StartDate、EndDate、TYPE |
| `s_mfd_buyvol_a` | 主动买入量 | TRADEDATE、TYPE |
| `s_mfd_buyvol_at` | 主动买入量(全单) | TRADEDATE |
| `s_mfd_buyvol_close_m` | 尾盘主力净流入量 | TRADEDATE |
| `s_mfd_buyvol_d` | 流入量 | TRADEDATE、TYPE |
| `s_mfd_buyvol_m` | 主力净流入量 | TRADEDATE |
| `s_mfd_buyvol_open_m` | 开盘主力净流入量 | TRADEDATE |
| `s_mfd_inflow` | (日)净流入资金 | DATE |
| `s_mfd_inflow_close` | (日)尾盘净流入资金 | DATE |
| `s_mfd_inflow_close_m` | 尾盘主力净流入额 | TRADEDATE |
| `s_mfd_inflow_m` | 主力净流入额 | TRADEDATE |
| `s_mfd_inflow_open` | (日)开盘净流入资金 | DATE |
| `s_mfd_inflow_open_m` | 开盘主力净流入额 | TRADEDATE |
| `s_mfd_inflowdays` | 区间主力净流入天数 | StartDate、EndDate |
| `s_mfd_inflowproportion` | (日)资金流向占比 |  |
| `s_mfd_inflowproportion_a` | 净主动买入额占比 | TRADEDATE |
| `s_mfd_inflowproportion_close_a` | 尾盘净主动买入额占比 | TRADEDATE |
| `s_mfd_inflowproportion_close_m` | 尾盘主力净流入额占比 | TRADEDATE |
| `s_mfd_inflowproportion_m` | 主力净流入额占比 | TRADEDATE |
| `s_mfd_inflowproportion_open_a` | 开盘净主动买入额占比 | TRADEDATE |
| `s_mfd_inflowproportion_open_m` | 开盘主力净流入额占比 | TRADEDATE |
| `s_mfd_inflowrate` | (日)金额流入率 | DATE |
| `s_mfd_inflowrate_close_a` | 尾盘净主动买入率(金额) | TRADEDATE |
| `s_mfd_inflowrate_close_m` | 尾盘主力净流入率(金额) | TRADEDATE |
| `s_mfd_inflowrate_m` | 主力净流入率(金额) | TRADEDATE |
| `s_mfd_inflowrate_open_a` | 开盘净主动买入率(金额) | TRADEDATE |
| `s_mfd_inflowrate_open_m` | 开盘主力净流入率(金额) | TRADEDATE |
| `s_mfd_inflowvolume` | (日)净流入量 | DATE |
| `s_mfd_inflowvolume_close_a` | 尾盘资金净主动买入量 | TRADEDATE |
| `s_mfd_inflowvolume_open_a` | 开盘资金净主动买入量 | TRADEDATE |
| `s_mfd_netbuyamt` | 净买入额 | TRADEDATE、TYPE |
| `s_mfd_netbuyamt_a` | 净主动买入额 | TRADEDATE、TYPE |
| `s_mfd_netbuyvol` | 净买入量 | TRADEDATE、TYPE |
| `s_mfd_netbuyvol_a` | 净主动买入量 | TRADEDATE、TYPE |
| `s_mfd_periodbuyamt_a_all` | 区间主动买入额 | StartDate、EndDate |
| `s_mfd_periodbuyvol_a_all` | 区间主动买入量 | StartDate、EndDate |
| `s_mfd_periodsellamt_a_all` | 区间主动卖出额 | StartDate、EndDate |
| `s_mfd_periodsellvol_a_all` | 区间主动卖出量 | StartDate、EndDate |
| `s_mfd_sellamt` | 卖出成交额 | StartDate、EndDate、TYPE |
| `s_mfd_sellamt_a` | 主动卖出额 | TRADEDATE、TYPE |
| `s_mfd_sellamt_at` | 主动卖出额(全单) | TRADEDATE |
| `s_mfd_sellamt_d` | 流出额 | TRADEDATE、TYPE |
| `s_mfd_sellord` | 流出单数 | TRADEDATE、TYPE |
| `s_mfd_sellvol` | 卖出成交量,s_mfd_ellvol | StartDate、EndDate、TYPE |
| `s_mfd_sellvol_a` | 主动卖出量 | TRADEDATE、TYPE |
| `s_mfd_sellvol_at` | 主动卖出量(全单) | TRADEDATE |
| `s_mfd_sellvol_d` | 流出量 | TRADEDATE、TYPE |
| `s_mfd_sn_buyamt` | 沪深港股通买入金额 | TRADEDATE |
| `s_mfd_sn_inflow` | 沪深港股通净买入金额 | TRADEDATE |
| `s_mfd_sn_sellamt` | 沪深港股通卖出金额 | TRADEDATE |
| `s_mfd_volinflowproportion_close_a` | 尾盘净主动买入量占比 | TRADEDATE |
| `s_mfd_volinflowproportion_close_m` | 尾盘主力净流入量占比 | TRADEDATE |
| `s_mfd_volinflowproportion_m` | 主力净流入量占比 | TRADEDATE |
| `s_mfd_volinflowproportion_open_a` | 开盘净主动买入量占比 | TRADEDATE |
| `s_mfd_volinflowproportion_open_m` | 开盘主力净流入量占比 | TRADEDATE |
| `s_mfd_volinflowrate_a` | 净主动买入率(量) | TRADEDATE |
| `s_mfd_volinflowrate_close_a` | 尾盘净主动买入率(量) | TRADEDATE |
| `s_mfd_volinflowrate_close_m` | 尾盘主力净流入率(量) | TRADEDATE |
| `s_mfd_volinflowrate_m` | 主力净流入率(量) | TRADEDATE |
| `s_mfd_volinflowrate_open_a` | 开盘净主动买入率(量) | TRADEDATE |
| `s_mfd_volinflowrate_open_m` | 开盘主力净流入率(量) | TRADEDATE |
| `s_mfn_sn_inflowdays` | 持续净流入天数 | TRADEDATE |
| `s_mfn_sn_outflowdays` | 持续净卖出天数 | TRADEDATE |
| `s_mfp_sn_inflow` | 沪深港股通区间净买入额 | StartDate、EndDate |
| `s_mfp_sn_inflowamt` | 区间净买入金额 | StartDate、EndDate |
| `s_mfp_sn_inflowamt2` | 沪深港股通区间净买入量(调整) | StartDate、EndDate |
| `s_mfp_sn_inflowdays` | 区间净流入天数 | StartDate、EndDate |
| `s_mfp_sn_outflowdays` | 区间净流出天数 | StartDate、EndDate |
| `s_mq_amount` | 月成交额(新增) |  |
| `s_mq_amount_btin` | 月成交额(含大宗交易) | TRADEDATE |
| `s_mq_avgamount` | 月日均成交额 |  |
| `s_mq_avgaoi` | 月日均持仓量 |  |
| `s_mq_avgprice` | 月均价(新增) |  |
| `s_mq_avgturn` | 月平均换手率(新增) |  |
| `s_mq_avgvolume` | 月日均成交量 |  |
| `s_mq_change` | 月涨跌(新增) |  |
| `s_mq_change_settlement` | 月涨跌（结算价） |  |
| `s_mq_close` | 月收盘价(新增) |  |
| `s_mq_freeavgturnover` | 月平均换手率（基准.自由流通股本）(新增) |  |
| `s_mq_freeturnover` | 月换手率（基准.自由流通股本）(新增) |  |
| `s_mq_high` | 月最高价(新增) |  |
| `s_mq_high_date` | 月最高价日(新增) |  |
| `s_mq_highclose` | 月最高收盘价(新增) |  |
| `s_mq_highclose_date` | 月最高收盘价日(新增) |  |
| `s_mq_highsettle` | 月最高结算价 |  |
| `s_mq_highswing_date` | 月最高结算价日 |  |
| `s_mq_low` | 月最低价(新增) |  |
| `s_mq_low_date` | 月最低价日(新增) |  |
| `s_mq_lowclose` | 月最低收盘价(新增) |  |
| `s_mq_lowclose_date` | 月最低收盘价日(新增) |  |
| `s_mq_lowsettle` | 月最低结算价 |  |
| `s_mq_lowswing_date` | 月最低结算价日 |  |
| `s_mq_oi` | 月持仓量 |  |
| `s_mq_oichange` | 月持仓变化 |  |
| `s_mq_open` | 月开盘价(新增) |  |
| `s_mq_pctchange` | 月涨跌幅(新增) |  |
| `s_mq_pctchange_settlement` | 月涨跌幅（结算价） |  |
| `s_mq_preclose` | 月前收盘价(新增) |  |
| `s_mq_presettle` | 月前结算价 |  |
| `s_mq_settle` | 月结算价 |  |
| `s_mq_swing` | 月振幅(新增) |  |
| `s_mq_turn` | 月换手率(新增) |  |
| `s_mq_volume` | 月成交量(新增) |  |
| `s_neeq_green` | 是否绿色通道审核程序挂牌 |  |
| `s_neeq_level` | 所属分层 | TRADEDATE |
| `s_neeq_listanndate` | 挂牌公告日 |  |
| `s_neeq_listdate_innovationlevel` | 创新层挂牌日 |  |
| `s_neeq_listingdate` | 挂牌日 |  |
| `s_neeq_marketmakeanndate` | 转做市公告日 |  |
| `s_neeq_marketmakernum` | 做市商家数 | TRADEDATE |
| `s_neeq_park` | 挂牌园区 |  |
| `s_neeq_standard` | 所属创新层标准 |  |
| `s_neeq_standard2` | 所属挂牌标准(支持历史) | TRADEDATE |
| `s_neeq_suspensionday` | 转板精选层前停牌日 |  |
| `s_npl_trust` | 不良资产比率 | Year |
| `s_nq_1stquartile` | N日收盘价1/4分位数 |  |
| `s_nq_3rdquartile` | N日收盘价3/4分位数 |  |
| `s_nq_amount` | N日成交额(新增) |  |
| `s_nq_avgchange` | N日日均涨跌幅(新增) |  |
| `s_nq_avgclose` | N日日均收盘价(算术平均) |  |
| `s_nq_avgprice` | N日成交均价 |  |
| `s_nq_avgprice2` | N日成交均价(算术平均) | N、TRADEDATE |
| `s_nq_avgturn` | N日日均换手率(新增) |  |
| `s_nq_close` | N日收盘价 | N、TRADEDATE、AdjustType |
| `s_nq_continuousdowns` | N日连续下跌 |  |
| `s_nq_continuousups` | N日连续上涨 |  |
| `s_nq_lowamount` | N日最低流通A市值(新增) |  |
| `s_nq_median` | N日收盘价中位数 |  |
| `s_nq_pctchange` | N日涨跌幅(新增) |  |
| `s_nq_relpctchange` | 相对大盘N日涨跌幅(新增) |  |
| `s_nq_swing` | N日振幅(新增) |  |
| `s_nq_tradeday` | 指定日相近交易日期 | TRADEDATE、N |
| `s_nq_turn` | N日换手率(新增) |  |
| `s_nq_volume` | N日成交量(新增) |  |
| `s_oi_lname` | 持买单量进榜会员名称 |  |
| `s_oi_loi` | 持买单量比上交易日增减 |  |
| `s_oi_loic` | 持买单量比上交易日增减 |  |
| `s_oi_lvname` | 持买单量(品种)会员名称 | TRADEDATE、TopN |
| `s_oi_lvoi` | 持买单量(品种) | TRADEDATE |
| `s_oi_nvoi` | 净持仓(品种) | TRADEDATE |
| `s_oi_sname` | 持卖单量进榜会员名称 |  |
| `s_oi_soi` | 持卖单量 |  |
| `s_oi_soic` | 持卖单量比上交易日增减 |  |
| `s_oi_svname` | 持卖单量(品种)会员名称 | TRADEDATE、TopN |
| `s_oi_svoi` | 持卖单量(品种) | TRADEDATE |
| `s_oi_vname` | 成交量进榜会员名称 |  |
| `s_oi_volume` | 成交量 |  |
| `s_oi_volumec` | 成交量比上交易日增减 |  |
| `s_open_auction_amount` | 开盘集合竞价成交额 | TRADEDATE |
| `s_open_auction_amount_t` | 开盘集合竞价成交额(分时段) | TRADEDATE、SESSION_TYPE |
| `s_open_auction_price` | 开盘集合竞价成交价 | TRADEDATE |
| `s_open_auction_price_t` | 开盘集合竞价成交价(分时段) | TRADEDATE、SESSION_TYPE |
| `s_open_auction_volume` | 开盘集合竞价成交量 | TRADEDATE |
| `s_open_auction_volume_t` | 开盘集合竞价成交量(分时段) | TRADEDATE、SESSION_TYPE |
| `s_performanceexp_bps_os` | 业绩快报.归属母公司普通股股东每股净资产 | REPORTDATE |
| `s_performanceexpress_bps` | 业绩快报.每股净资产 | REPORTDATE |
| `s_performanceexpress_bps_b` | 业绩快报.期初每股净资产 | REPORTDATE |
| `s_performanceexpress_bps_growth` | 业绩快报.比年初增长率:归属于母公司股东的每股净资产 | REPORTDATE |
| `s_performanceexpress_date` | 业绩快报披露日(新增) | D |
| `s_performanceexpress_ebt_yoy` | 业绩快报.同比增长率:利润总额 | REPORTDATE |
| `s_performanceexpress_eps_ya` | 业绩快报.去年同期每股收益 | REPORTDATE |
| `s_performanceexpress_eps_yoy` | 业绩快报.同比增长率:基本每股收益 | REPORTDATE |
| `s_performanceexpress_eqy_growth` | 业绩快报.比年初增长率:归属母公司的股东权益 | REPORTDATE |
| `s_performanceexpress_income_ya` | 业绩快报.去年同期营业收入 | REPORTDATE |
| `s_performanceexpress_lastdate` | 业绩快报最新披露日期 | REPORTDATE |
| `s_performanceexpress_lastrptdate` | 最新业绩快报报告期 |  |
| `s_performanceexpress_lrsd` | 截止指定日期最新业绩快报报告期 | TRADEDATE |
| `s_performanceexpress_netassets_b` | 业绩快报.期初净资产 | REPORTDATE |
| `s_performanceexpress_netprofit_ya` | 业绩快报.去年同期净利润 | REPORTDATE |
| `s_performanceexpress_np_yoy` | 业绩快报.同比增长率:归属母公司股东的净利润 | REPORTDATE |
| `s_performanceexpress_npded_ya` | 业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE |
| `s_performanceexpress_npded_yoy` | 业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE |
| `s_performanceexpress_npdedtoshareholder` | 业绩快报.归属于上市公司股东的扣除非经常性损益的净利润 | REPORTDATE |
| `s_performanceexpress_op_yoy` | 业绩快报.同比增长率:营业利润 | REPORTDATE |
| `s_performanceexpress_or_yoy` | 业绩快报.同比增长率:营业收入 | REPORTDATE |
| `s_performanceexpress_perfexepsdiluted` | 业绩快报.每股收益EPS-摊薄(新增) | D |
| `s_performanceexpress_perfexincome` | 业绩快报.主营业务收入(新增) | D |
| `s_performanceexpress_perfexnetassets` | 业绩快报.净资产(新增) | D |
| `s_performanceexpress_perfexnetprofittoshareholder` | 业绩快报.归属母公司股东的净利润(新增) | D |
| `s_performanceexpress_perfexprofit` | 业绩快报.营业利润(新增) | D |
| `s_performanceexpress_perfexroediluted` | 业绩快报.净资产收益率ROE-摊薄(新增) | D |
| `s_performanceexpress_perfextotalassets` | 业绩快报.总资产(新增) | D |
| `s_performanceexpress_perfextotalprofit` | 业绩快报.利润总额(新增) | D |
| `s_performanceexpress_profit_ya` | 业绩快报.去年同期营业利润 | REPORTDATE |
| `s_performanceexpress_roe_yoy` | 业绩快报.同比增减:加权平均净资产收益率 | REPORTDATE |
| `s_performanceexpress_totassets_growth` | 业绩快报.比年初增长率:总资产 | REPORTDATE |
| `s_performanceexpress_totprofit_ya` | 业绩快报.去年同期利润总额 | REPORTDATE |
| `s_periodmfd_inflow` | (区间)净流入资金 | StartDate、EndDate |
| `s_periodmfd_inflow_close` | (区间)尾盘净流入资金 | StartDate、EndDate |
| `s_periodmfd_inflow_open` | (区间)开盘净流入资金 | StartDate、EndDate |
| `s_periodmfd_inflowproportion` | (区间)资金流向占比 | StartDate、EndDate |
| `s_periodmfd_inflowrate` | (区间)金额流入率 | StartDate、EndDate |
| `s_periodmfd_inflowvolume` | (区间)净流入量 | StartDate、EndDate |
| `s_pq_abnormaltrade_lp` | 区间龙虎榜净买入额 | StartDate、EndDate |
| `s_pq_abnormaltrade_sp` | 区间龙虎榜净卖出额 | StartDate、EndDate |
| `s_pq_abnormaltradenum` | 区间龙虎榜上榜次数 | StartDate、EndDate |
| `s_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `s_pq_amount_aht` | 区间盘后成交额 | StartDate、EndDate |
| `s_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `s_pq_avgaoi` | 区间日均持仓量 | BEGINDATE、EndDate |
| `s_pq_avgashrmv` | 区间日均A股市值(不含限售股) | StartDate、DATE |
| `s_pq_avgashrmv2` | 区间日均A股市值(含限售股) | StartDate、DATE |
| `s_pq_avgashrmv2_es` | 区间日均A股市值(不含限售股)(剔除停牌日) | StartDate、DATE |
| `s_pq_avgashrmv_es` | 区间日均A股市值(含限售股)(剔除停牌日) | StartDate、DATE |
| `s_pq_avgclose` | 区间日均收盘价 | StartDate、EndDate、AdjustType |
| `s_pq_avgmv` | 区间日均总市值 | StartDate、DATE、CURTYPE |
| `s_pq_avgmv_es` | 区间日均总市值(剔除停牌日) | StartDate、DATE |
| `s_pq_avgmv_nonrestricted` | 区间日均流通市值 | StartDate、DATE、CURTYPE |
| `s_pq_avgpctchange` | 区间日均涨跌幅(新增) | TD1、TD2 |
| `s_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `s_pq_avgprice2` | 区间成交均价(可复权) | StartDate、EndDate、AdjustType |
| `s_pq_avgswing` | 区间日均振幅 | StartDate、EndDate |
| `s_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `s_pq_avgturn2` | 区间日均换手率 | StartDate、EndDate |
| `s_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `s_pq_blocktrade_volume` | 区间大宗交易成交总量 | StartDate、EndDate |
| `s_pq_blocktradeamount` | 区间大宗交易成交总额 | StartDate、EndDate |
| `s_pq_blocktradeamounts` | 区间成交额(含大宗交易) | StartDate、EndDate |
| `s_pq_blocktradenum` | 区间大宗交易上榜次数 | StartDate、EndDate |
| `s_pq_blocktradevolume` | 区间成交量(含大宗交易) | StartDate、EndDate |
| `s_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `s_pq_change_settlement` | 区间涨跌（结算价） | BEGINDATE、EndDate |
| `s_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `s_pq_close_percentile` | 收盘价分位数 | TRADEDATE、StartDate、EndDate、AdjustType |
| `s_pq_ctnslimitdowndays` | 区间连续跌停天数 | StartDate、EndDate |
| `s_pq_ctnslimitupdays` | 区间连续涨停天数 | StartDate、EndDate |
| `s_pq_downdays` | 区间下跌天数 | StartDate、EndDate |
| `s_pq_freeavgturnover` | 区间日均换手率（基准.自由流通股本）(新增) | TD1、TD2 |
| `s_pq_freeturnover` | 区间换手率（基准.自由流通股本）(新增) | TD1、TD2 |
| `s_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `s_pq_high_date` | 区间最高价日(新增) | TD1、TD2 |
| `s_pq_highamount` | 区间最高成交额 | StartDate、EndDate |
| `s_pq_highamount_date` | 区间最高成交额日 | StartDate、EndDate |
| `s_pq_highclose` | 区间最高收盘价(新增) | TD1、TD2 |
| `s_pq_highclose_date` | 区间最高收盘价日(新增) | TD1、TD2 |
| `s_pq_highsettle` | 区间最高结算价 | BEGINDATE、EndDate |
| `s_pq_highswing_date` | 区间最高结算价日 | BEGINDATE、EndDate |
| `s_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `s_pq_low_date` | 区间最低价日(新增) | TD1、TD2 |
| `s_pq_lowclose` | 区间最低收盘价(新增) | TD1、TD2 |
| `s_pq_lowclose_date` | 区间最低收盘价日(新增) | TD1、TD2 |
| `s_pq_lowsettle` | 区间最低结算价 | BEGINDATE、EndDate |
| `s_pq_lowswing_date` | 区间最低结算价日 | BEGINDATE、EndDate |
| `s_pq_maxuptype` | N天M板 | TRADEDATE |
| `s_pq_oi` | 区间持仓量 | BEGINDATE、EndDate |
| `s_pq_oichange` | 区间持仓变化 | BEGINDATE、EndDate |
| `s_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `s_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `s_pq_pctchange2` | 区间涨跌幅(包含上市首日涨跌幅) | StartDate、EndDate |
| `s_pq_pctchange_high` | 区间收盘最大涨幅 | StartDate、EndDate |
| `s_pq_pctchange_highest` | 区间自最低价的最大涨幅 | StartDate、EndDate |
| `s_pq_pctchange_low` | 区间收盘最大跌幅 | StartDate、EndDate |
| `s_pq_pctchange_lowest` | 区间自最高价的最大跌幅 | StartDate、EndDate |
| `s_pq_pctchange_settlement` | 区间涨跌幅（结算价） | BEGINDATE、EndDate |
| `s_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `s_pq_presettle` | 区间前结算价 | BEGINDATE、EndDate |
| `s_pq_relpctchange` | 区间相对涨跌幅 | BEGINDATE、EndDate |
| `s_pq_relpctchange2` | 相对大盘区间涨跌幅(包含上市首日涨跌幅) | StartDate、EndDate |
| `s_pq_settle` | 区间结算价 | BEGINDATE、EndDate |
| `s_pq_suspendenddate` | 长期停牌截止日 | TRADEDATE |
| `s_pq_suspendstartdate` | 长期停牌起始日 | TRADEDATE |
| `s_pq_swing` | 区间振幅(新增) | TD1、TD2 |
| `s_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `s_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `s_pq_updays` | 区间上涨天数 | StartDate、EndDate |
| `s_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `s_pq_volume_aht` | 区间盘后成交量 | StartDate、EndDate |
| `s_prfshareissue_collection` | 区间优先股募集资金合计 | StartDate、DATE |
| `s_profitnotice_abstract` | 业绩预告摘要 | REPORTDATE |
| `s_profitnotice_basicearnmax` | 预告基本每股收益下限 | REPORTDATE |
| `s_profitnotice_basicearnmin` | 预告基本每股收益上限 | REPORTDATE |
| `s_profitnotice_changemax` | 预告净利润同比增长上限 | REPORTDATE |
| `s_profitnotice_changemin` | 预告净利润同比增长下限 | REPORTDATE |
| `s_profitnotice_changeratio` | 预告净利润变动幅度 | REPORTDATE |
| `s_profitnotice_date` | 业绩预告日期(新增) | D |
| `s_profitnotice_deductedearnmax` | 预告扣非后基本每股收益上限 | REPORTDATE |
| `s_profitnotice_deductedearnmin` | 预告扣非后基本每股收益下限 | REPORTDATE |
| `s_profitnotice_deductedprofitmax` | 预告扣非净利润上限 | REPORTDATE |
| `s_profitnotice_deductedprofitmin` | 预告扣非净利润下限 | REPORTDATE |
| `s_profitnotice_deductedprofityoymax` | 预告扣非净利润同比增长上限 | REPORTDATE |
| `s_profitnotice_deductedprofityoymin` | 预告扣非净利润同比增长下限 | REPORTDATE |
| `s_profitnotice_deductedsalesmax` | 预告扣除后营业收入上限 | REPORTDATE |
| `s_profitnotice_deductedsalesmin` | 预告扣除后营业收入下限 | REPORTDATE |
| `s_profitnotice_firstdate` | 业绩预告首次披露日期 | REPORTDATE |
| `s_profitnotice_incomemax` | 预告营业收入上限 | REPORTDATE |
| `s_profitnotice_incomemin` | 预告营业收入下限 | REPORTDATE |
| `s_profitnotice_lasteps` | 去年同期每股收益(新增) | D |
| `s_profitnotice_lastoe` | 上年同期归属于母公司所有者权益 | REPORTDATE |
| `s_profitnotice_lastrptdate` | 最新业绩预告报告期 |  |
| `s_profitnotice_lastyearbasicearn` | 上年同期基本每股收益 | REPORTDATE |
| `s_profitnotice_lastyeardeductedearn` | 上年同期扣非后基本每股收益 | REPORTDATE |
| `s_profitnotice_lastyeardeductedprofit` | 上年同期扣非净利润 | REPORTDATE |
| `s_profitnotice_lastyeardeductedsales` | 上年同期扣除后营业收入 | REPORTDATE |
| `s_profitnotice_lastyearincome` | 上年同期营业收入 | REPORTDATE |
| `s_profitnotice_netprofitmax` | 预告净利润上限 | REPORTDATE |
| `s_profitnotice_netprofitmin` | 预告净利润下限 | REPORTDATE |
| `s_profitnotice_netsalesmax` | 预告净营收上限 | REPORTDATE |
| `s_profitnotice_netsalesmin` | 预告净营收下限 | REPORTDATE |
| `s_profitnotice_netsalesyoymax` | 预告净营收同比增长上限 | REPORTDATE |
| `s_profitnotice_netsalesyoymin` | 预告净营收同比增长下限 | REPORTDATE |
| `s_profitnotice_oemax` | 预告归属于母公司所有者权益上限 | REPORTDATE |
| `s_profitnotice_oemin` | 预告归属于母公司所有者权益下限 | REPORTDATE |
| `s_profitnotice_reason` | 业绩预告变动原因 | REPORTDATE |
| `s_profitnotice_salesmax` | 预告总营收上限 | REPORTDATE |
| `s_profitnotice_salesmin` | 预告总营收下限 | REPORTDATE |
| `s_profitnotice_salesyoymax` | 预告总营收同比增长上限 | REPORTDATE |
| `s_profitnotice_salesyoymin` | 预告总营收同比增长下限 | REPORTDATE |
| `s_profitnotice_style` | 业绩预告类型 | REPORTDATE |
| `s_qfa_adminexpensetogr` | 单季度.管理费用／营业总收入 | REPORTDATE |
| `s_qfa_adminexpensetogr2` | 单季度.管理费用/营业总收入(不含研发费用) | REPORTDATE |
| `s_qfa_cgrgr` | 单季度.营业总收入环比增长率 | REPORTDATE |
| `s_qfa_cgrnetprofit` | 单季度.归属母公司股东的净利润环比增长率 | REPORTDATE |
| `s_qfa_cgrop` | 单季度.营业利润环比增长率 | REPORTDATE |
| `s_qfa_cgrprofit` | 单季度.净利润环比增长率 | REPORTDATE |
| `s_qfa_cgrsales` | 单季度.营业收入环比增长率 | REPORTDATE |
| `s_qfa_deductedprofit` | 单季度.扣除非经常损益后的净利润 | REPORTDATE |
| `s_qfa_deductedprofit_cgr` | 单季度.扣除非经常性损益后的净利润环比增长率 | REPORTDATE |
| `s_qfa_deductedprofit_yoy` | 单季度.扣除非经常性损益后的净利润同比增长率 | REPORTDATE |
| `s_qfa_deductedprofitmargin` | 单季度.扣非销售净利率 | REPORTDATE |
| `s_qfa_deductedprofittoprofit` | 单季度.扣除非经常损益后的净利润／净利润 | REPORTDATE |
| `s_qfa_eps` | 单季度.每股收益EPS | REPORTDATE |
| `s_qfa_finaexpensetogr` | 单季度.财务费用／营业总收入 | REPORTDATE |
| `s_qfa_gctogr` | 单季度.营业总成本／营业总收入 | REPORTDATE |
| `s_qfa_grossmargin` | 单季度.毛利 | REPORTDATE、TYPE |
| `s_qfa_grossprofitmargin` | 单季度.销售毛利率 | REPORTDATE |
| `s_qfa_investincome` | 单季度.价值变动净收益 | REPORTDATE |
| `s_qfa_investincometoebt` | 单季度.价值变动净收益／利润总额 | REPORTDATE |
| `s_qfa_netprofitmargin` | 单季度.销售净利率 | REPORTDATE |
| `s_qfa_ocftooperateincome` | 单季度.经营活动产生的现金流量净额／经营活动净收益 | REPORTDATE |
| `s_qfa_ocftoor` | 单季度.经营活动产生的现金流量净额／营业收入 | REPORTDATE |
| `s_qfa_operateexpensetogr` | 单季度.营业费用／营业总收入 | REPORTDATE |
| `s_qfa_operateincome` | 单季度.经营活动净收益 | REPORTDATE |
| `s_qfa_operateincometoebt` | 单季度.经营活动净收益／利润总额 | REPORTDATE |
| `s_qfa_optogr` | 单季度.营业利润／营业总收入 | REPORTDATE |
| `s_qfa_profittogr` | 单季度.净利润／营业总收入 | REPORTDATE |
| `s_qfa_rdetogr` | 单季度.研发费用/营业总收入 | REPORTDATE |
| `s_qfa_roa` | 单季度.总资产净利率ROA | REPORTDATE |
| `s_qfa_roe` | 单季度.净资产收益率ROE | REPORTDATE |
| `s_qfa_roe_deducted` | 单季度.净资产收益率(扣除非经常损益) | REPORTDATE |
| `s_qfa_salescashintoor` | 单季度.销售商品提供劳务收到的现金／营业收入 | REPORTDATE |
| `s_qfa_yoyasset` | 单季度.总资产(同比增长率) | REPORTDATE |
| `s_qfa_yoycf` | 单季度.现金净流量(同比增长率) | REPORTDATE |
| `s_qfa_yoydebt` | 单季度.总负债(同比增长率) | REPORTDATE |
| `s_qfa_yoyeps` | 单季度.每股收益(同比增长率) | REPORTDATE |
| `s_qfa_yoyequity` | 单季度.净资产(同比增长率) | REPORTDATE |
| `s_qfa_yoygr` | 单季度.营业总收入同比增长率 | REPORTDATE |
| `s_qfa_yoynetprofit` | 单季度.归属母公司股东的净利润同比增长率 | REPORTDATE |
| `s_qfa_yoyocf` | 单季度.经营性现金净流量(同比增长率) | REPORTDATE |
| `s_qfa_yoyop` | 单季度.营业利润同比增长率 | REPORTDATE |
| `s_qfa_yoyprofit` | 单季度.净利润同比增长率 | REPORTDATE |
| `s_qfa_yoysales` | 单季度.营业收入同比增长率 | REPORTDATE |
| `s_qprofitnotice_abstract` | 单季度.业绩预告摘要 | REPORTDATE |
| `s_qprofitnotice_changemax` | 单季度.预告净利润同比增长上限 | REPORTDATE |
| `s_qprofitnotice_changemin` | 单季度.预告净利润同比增长下限 | REPORTDATE |
| `s_qprofitnotice_date` | 单季度.业绩预告日期 | REPORTDATE |
| `s_qprofitnotice_netprofitmax` | 单季度.预告净利润上限 | REPORTDATE |
| `s_qprofitnotice_netprofitmin` | 单季度.预告净利润下限 | REPORTDATE |
| `s_qprofitnotice_netsalesmax` | 单季度.预告净营收上限 | REPORTDATE |
| `s_qprofitnotice_netsalesmin` | 单季度.预告净营收下限 | REPORTDATE |
| `s_qprofitnotice_netsalesyoymax` | 单季度.预告净营收同比增长上限 | REPORTDATE |
| `s_qprofitnotice_netsalesyoymin` | 单季度.预告净营收同比增长下限 | REPORTDATE |
| `s_qprofitnotice_salesmax` | 单季度.预告总营收上限 | REPORTDATE |
| `s_qprofitnotice_salesmin` | 单季度.预告总营收下限 | REPORTDATE |
| `s_qprofitnotice_salesyoymax` | 单季度.预告总营收同比增长上限 | REPORTDATE |
| `s_qprofitnotice_salesyoymin` | 单季度.预告总营收同比增长下限 | REPORTDATE |
| `s_qprofitnotice_style` | 单季度.业绩预告类型 | REPORTDATE |
| `s_qq_amount` | 季成交额 |  |
| `s_qq_avgamount` | 季日均成交额 |  |
| `s_qq_avgaoi` | 季日均持仓量 |  |
| `s_qq_avgprice` | 季成交均价 |  |
| `s_qq_avgvolume` | 季日均成交量 |  |
| `s_qq_change` | 季涨跌 |  |
| `s_qq_change_settlement` | 季涨跌（结算价） |  |
| `s_qq_close` | 季收盘价 |  |
| `s_qq_high` | 季最高价 |  |
| `s_qq_high_date` | 季最高价日 |  |
| `s_qq_highclose` | 季最高收盘价 |  |
| `s_qq_highclose_date` | 季最高收盘价日 |  |
| `s_qq_highsettle` | 季最高结算价 |  |
| `s_qq_highswing_date` | 季最高结算价日 |  |
| `s_qq_low` | 季最低价 |  |
| `s_qq_low_date` | 季最低价日 |  |
| `s_qq_lowclose` | 季最低收盘价 |  |
| `s_qq_lowclose_date` | 季最低收盘价日 |  |
| `s_qq_lowsettle` | 季最低结算价 |  |
| `s_qq_lowswing_date` | 季最低结算价日 |  |
| `s_qq_oi` | 季持仓量 |  |
| `s_qq_oichange` | 季持仓变化 |  |
| `s_qq_open` | 季开盘价 |  |
| `s_qq_pctchange` | 季涨跌幅 |  |
| `s_qq_pctchange_settlement` | 季涨跌幅（结算价） |  |
| `s_qq_preclose` | 季前收盘价 |  |
| `s_qq_presettle` | 季前结算价 |  |
| `s_qq_settle` | 季结算价 |  |
| `s_qq_swing` | 季振幅 |  |
| `s_qq_volume` | 季成交量 |  |
| `s_qstm07_cs` | 07版财务报表现金流量表单季度 | ITEMSCODE、REPORTDATE |
| `s_qstm07_cs_10` | 单季度.收到的税费返还 | REPORTDATE |
| `s_qstm07_cs_100` | 单季度.经营性应收项目的减少 | REPORTDATE |
| `s_qstm07_cs_101` | 单季度.经营性应付项目的增加 | REPORTDATE |
| `s_qstm07_cs_105` | 单季度.间接法-经营活动产生的现金流量净额 | REPORTDATE |
| `s_qstm07_cs_106` | 单季度.债务转为资本 | REPORTDATE |
| `s_qstm07_cs_107` | 单季度.一年内到期的可转换公司债券 | REPORTDATE |
| `s_qstm07_cs_108` | 单季度.融资租入固定资产 | REPORTDATE |
| `s_qstm07_cs_109` | 单季度.现金的期末余额 | REPORTDATE |
| `s_qstm07_cs_11` | 单季度.收到的其他与经营活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_111` | 单季度.现金等价物的期末余额 | REPORTDATE |
| `s_qstm07_cs_116` | 单季度.间接法-现金及现金等价物净增加额 | REPORTDATE |
| `s_qstm07_cs_117` | 单季度.其他 | REPORTDATE |
| `s_qstm07_cs_118` | 单季度.子公司吸收少数股东投资收到的现金 | REPORTDATE |
| `s_qstm07_cs_119` | 单季度.子公司支付给少数股东的股利、利润 | REPORTDATE |
| `s_qstm07_cs_12` | 单季度.客户存款和同业存放款项净增加额 | REPORTDATE |
| `s_qstm07_cs_120` | 单季度.未确认的投资损失 | REPORTDATE |
| `s_qstm07_cs_121` | 单季度.支付保单红利的现金 | REPORTDATE |
| `s_qstm07_cs_13` | 单季度.向中央银行借款净增加额 | REPORTDATE |
| `s_qstm07_cs_131` | 单季度.信用减值损失 | REPORTDATE |
| `s_qstm07_cs_134` | 单季度.使用权资产折旧 | REPORTDATE |
| `s_qstm07_cs_14` | 单季度.向其他金融机构拆入资金净增加额 | REPORTDATE |
| `s_qstm07_cs_15` | 单季度.收取利息和手续费净增加额 | REPORTDATE |
| `s_qstm07_cs_16` | 单季度.收到的原保险合同保费取得的现金 | REPORTDATE |
| `s_qstm07_cs_17` | 单季度.收到的再保业务现金净额 | REPORTDATE |
| `s_qstm07_cs_18` | 单季度.处置交易性金融资产净增加额 | REPORTDATE |
| `s_qstm07_cs_20` | 单季度.拆入资金净增加额 | REPORTDATE |
| `s_qstm07_cs_21` | 单季度.回购业务资金净增加额 | REPORTDATE |
| `s_qstm07_cs_25` | 单季度.经营活动现金流入小计 | REPORTDATE |
| `s_qstm07_cs_26` | 单季度.购买商品、接受劳务支付的现金 | REPORTDATE |
| `s_qstm07_cs_27` | 单季度.支付给职工以及为职工支付的现金 | REPORTDATE |
| `s_qstm07_cs_28` | 单季度.支付的各项税费 | REPORTDATE |
| `s_qstm07_cs_29` | 单季度.支付的其他与经营活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_30` | 单季度.客户贷款及垫款净增加额 | REPORTDATE |
| `s_qstm07_cs_31` | 单季度.存放央行和同业款项净增加额 | REPORTDATE |
| `s_qstm07_cs_32` | 单季度.支付赔付款项的现金 | REPORTDATE |
| `s_qstm07_cs_33` | 单季度.支付手续费的现金 | REPORTDATE |
| `s_qstm07_cs_37` | 单季度.经营活动现金流出小计 | REPORTDATE |
| `s_qstm07_cs_39` | 单季度.经营活动产生的现金流量净额 | REPORTDATE |
| `s_qstm07_cs_40` | 单季度.收回投资所收到的现金 | REPORTDATE |
| `s_qstm07_cs_41` | 单季度.取得投资收益所收到的现金 | REPORTDATE |
| `s_qstm07_cs_42` | 单季度.处置固定资产、无形资产和其他长期资产收回的现金净额 | REPORTDATE |
| `s_qstm07_cs_43` | 单季度.处置子公司及其他营业单位收到的现金净额 | REPORTDATE |
| `s_qstm07_cs_44` | 单季度.收到的其他与投资活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_48` | 单季度.投资活动现金流入小计 | REPORTDATE |
| `s_qstm07_cs_49` | 单季度.购建固定资产、无形资产和其他长期资产支付的现金 | REPORTDATE |
| `s_qstm07_cs_50` | 单季度.投资支付的现金 | REPORTDATE |
| `s_qstm07_cs_51` | 单季度.取得子公司及其他营业单位支付的现金净额 | REPORTDATE |
| `s_qstm07_cs_52` | 单季度.支付的其他与投资活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_57` | 单季度.投资活动现金流出小计 | REPORTDATE |
| `s_qstm07_cs_59` | 单季度.投资活动产生的现金流量净额 | REPORTDATE |
| `s_qstm07_cs_60` | 单季度.吸收投资所收到的现金 | REPORTDATE |
| `s_qstm07_cs_61` | 单季度.取得借款收到的现金 | REPORTDATE |
| `s_qstm07_cs_62` | 单季度.收到的其他与筹资活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_63` | 单季度.发行债券收到的现金 | REPORTDATE |
| `s_qstm07_cs_64` | 单季度.保户储金净增加额 | REPORTDATE |
| `s_qstm07_cs_68` | 单季度.筹资活动现金流入小计 | REPORTDATE |
| `s_qstm07_cs_69` | 单季度.偿还债务所支付的现金 | REPORTDATE |
| `s_qstm07_cs_70` | 单季度.分配股利、利润和偿付利息所支付的现金 | REPORTDATE |
| `s_qstm07_cs_71` | 单季度.支付的其他与筹资活动有关的现金 | REPORTDATE |
| `s_qstm07_cs_75` | 单季度.筹资活动现金流出小计 | REPORTDATE |
| `s_qstm07_cs_77` | 单季度.筹资活动产生的现金流量净额 | REPORTDATE |
| `s_qstm07_cs_78` | 单季度.汇率变动对现金的影响 | REPORTDATE |
| `s_qstm07_cs_82` | 单季度.现金及现金等价物净增加额 | REPORTDATE |
| `s_qstm07_cs_84` | 单季度.期末现金及现金等价物余额 | REPORTDATE |
| `s_qstm07_cs_85` | 单季度.净利润 | REPORTDATE |
| `s_qstm07_cs_86` | 单季度.资产减值准备 | REPORTDATE |
| `s_qstm07_cs_87` | 单季度.固定资产折旧、油气资产折耗、生产性生物资产折旧 | REPORTDATE |
| `s_qstm07_cs_88` | 单季度.无形资产摊销 | REPORTDATE |
| `s_qstm07_cs_89` | 单季度.长期待摊费用摊销 | REPORTDATE |
| `s_qstm07_cs_9` | 单季度.销售商品、提供劳务收到的现金 | REPORTDATE |
| `s_qstm07_cs_90` | 单季度.待摊费用减少 | REPORTDATE |
| `s_qstm07_cs_91` | 单季度.预提费用增加 | REPORTDATE |
| `s_qstm07_cs_92` | 单季度.处置固定资产、无形资产和其他长期资产的损失 | REPORTDATE |
| `s_qstm07_cs_93` | 单季度.固定资产报废损失 | REPORTDATE |
| `s_qstm07_cs_94` | 单季度.公允价值变动损失 | REPORTDATE |
| `s_qstm07_cs_95` | 单季度.财务费用 | REPORTDATE |
| `s_qstm07_cs_96` | 单季度.投资损失 | REPORTDATE |
| `s_qstm07_cs_97` | 单季度.递延所得税资产减少 | REPORTDATE |
| `s_qstm07_cs_98` | 单季度.递延所得税负债增加 | REPORTDATE |
| `s_qstm07_cs_99` | 单季度.存货的减少 | REPORTDATE |
| `s_qstm07_cs_cashpaidclaim` | 单季度.支付签发保险合同赔款的现金 | REPORTDATE、TYPE |
| `s_qstm07_cs_cashrecprem` | 单季度.收到签发保险合同保费取得的现金 | REPORTDATE、TYPE |
| `s_qstm07_cs_ntcashpaidcrc` | 单季度.支付分出再保险合同的现金净额 | REPORTDATE、TYPE |
| `s_qstm07_cs_ntcashrecced` | 单季度.收到分入再保险合同的现金净额 | REPORTDATE、TYPE |
| `s_qstm07_cs_ntincloanpled` | 单季度.保单质押贷款净增加额 | REPORTDATE、TYPE |
| `s_qstm07_is` | 07版财务报表利润表单季度 | ITEMSCODE、REPORTDATE |
| `s_qstm07_is_10` | 单季度.营业成本 | REPORTDATE |
| `s_qstm07_is_100` | 单季度.终止经营净利润 | REPORTDATE、TYPE |
| `s_qstm07_is_101` | 单季度.信用减值损失 | REPORTDATE、TYPE |
| `s_qstm07_is_102` | 单季度.净敞口套期收益 | REPORTDATE、TYPE |
| `s_qstm07_is_103` | 单季度.研发费用 | REPORTDATE、TYPE |
| `s_qstm07_is_104` | 单季度.财务费用:利息费用 | REPORTDATE、TYPE |
| `s_qstm07_is_105` | 单季度.财务费用:利息收入 | REPORTDATE、TYPE |
| `s_qstm07_is_106` | 单季度.其他资产减值损失 | REPORTDATE |
| `s_qstm07_is_108` | 单季度.以摊余成本计量的金融资产终止确认收益 | REPORTDATE |
| `s_qstm07_is_109` | 单季度.营业总成本2 | REPORTDATE |
| `s_qstm07_is_11` | 单季度.营业税金及附加 | REPORTDATE |
| `s_qstm07_is_12` | 单季度.销售费用 | REPORTDATE |
| `s_qstm07_is_13` | 单季度.管理费用 | REPORTDATE |
| `s_qstm07_is_14` | 单季度.财务费用 | REPORTDATE |
| `s_qstm07_is_15` | 单季度.资产减值损失 | REPORTDATE |
| `s_qstm07_is_16` | 单季度.公允价值变动净收益 | REPORTDATE |
| `s_qstm07_is_17` | 单季度.投资净收益 | REPORTDATE |
| `s_qstm07_is_19` | 单季度.利息收入 | REPORTDATE |
| `s_qstm07_is_20` | 单季度.利息支出 | REPORTDATE |
| `s_qstm07_is_22` | 单季度.手续费及佣金收入 | REPORTDATE |
| `s_qstm07_is_23` | 单季度.手续费及佣金支出 | REPORTDATE |
| `s_qstm07_is_24` | 单季度.其他经营净收益 | REPORTDATE |
| `s_qstm07_is_25` | 单季度.汇兑净收益 | REPORTDATE |
| `s_qstm07_is_28` | 单季度.已赚保费 | REPORTDATE |
| `s_qstm07_is_33` | 单季度.赔付支出 | REPORTDATE |
| `s_qstm07_is_35` | 单季度.提取保险合同准备金净额 | REPORTDATE |
| `s_qstm07_is_38` | 单季度.分保费用 | REPORTDATE |
| `s_qstm07_is_39` | 单季度.退保金 | REPORTDATE |
| `s_qstm07_is_40` | 单季度.保单红利支出 | REPORTDATE |
| `s_qstm07_is_48` | 单季度.营业利润 | REPORTDATE |
| `s_qstm07_is_49` | 单季度.营业外收入 | REPORTDATE |
| `s_qstm07_is_50` | 单季度.营业外支出 | REPORTDATE |
| `s_qstm07_is_51` | 单季度.非流动资产处置净损失 | REPORTDATE |
| `s_qstm07_is_55` | 单季度.利润总额 | REPORTDATE |
| `s_qstm07_is_56` | 单季度.所得税 | REPORTDATE |
| `s_qstm07_is_60` | 单季度.净利润 | REPORTDATE |
| `s_qstm07_is_61` | 单季度.归属母公司股东的净利润 | REPORTDATE |
| `s_qstm07_is_62` | 单季度.少数股东损益 | REPORTDATE |
| `s_qstm07_is_82` | 单季度.对联营企业和合营企业的投资收益 | REPORTDATE |
| `s_qstm07_is_83` | 单季度.营业总收入 | REPORTDATE |
| `s_qstm07_is_84` | 单季度.营业总成本 | REPORTDATE |
| `s_qstm07_is_85` | 单季度.其他业务收入 | REPORTDATE |
| `s_qstm07_is_86` | 单季度.其他业务成本 | REPORTDATE |
| `s_qstm07_is_87` | 单季度.未确认的投资损失 | REPORTDATE |
| `s_qstm07_is_9` | 单季度.营业收入 | REPORTDATE |
| `s_qstm07_is_92` | 单季度.其他综合收益 | REPORTDATE |
| `s_qstm07_is_93` | 单季度.综合收益总额 | REPORTDATE |
| `s_qstm07_is_94` | 单季度.归属于母公司普通股东综合收益总额 | REPORTDATE |
| `s_qstm07_is_95` | 单季度.归属于少数股东的综合收益总额 | REPORTDATE |
| `s_qstm07_is_97` | 单季度.其他收益 | REPORTDATE、TYPE |
| `s_qstm07_is_98` | 单季度.资产处置收益 | REPORTDATE、TYPE |
| `s_qstm07_is_99` | 单季度.持续经营净利润 | REPORTDATE、TYPE |
| `s_qstm07_is_amortinssvcco` | 单季度.摊回保险服务费用 | REPORTDATE、TYPE |
| `s_qstm07_is_apportcedprem` | 单季度.分出保费的分摊 | REPORTDATE、TYPE |
| `s_qstm07_is_cedreinsfingl` | 单季度.分出再保险财务损益 | REPORTDATE、TYPE |
| `s_qstm07_is_inssvccosts` | 单季度.保险服务费用 | REPORTDATE、TYPE |
| `s_qstm07_is_inssvcincome` | 单季度.保险服务收入 | REPORTDATE、TYPE |
| `s_qstm07_is_uwfinloss` | 单季度.承保财务损失 | REPORTDATE、TYPE |
| `s_qstm_cs` | 股票/单季报表函数/现金流量表 | ITEMSCODE、REPORTDATE |
| `s_qstm_is` | 股票/单季报表函数/利润表 | ITEMSCODE、REPORTDATE |
| `s_qstmnote_insur_212505` | 核心偿付能力溢额 | REPORTDATE |
| `s_qstmnote_insur_212506` | 核心偿付能力充足率 | REPORTDATE |
| `s_qstmnote_insur_212507` | 综合偿付能力溢额 | REPORTDATE |
| `s_qstmnote_insur_212508` | 综合偿付能力充足率 | REPORTDATE |
| `s_qstmnote_insur_212509` | 保险业务收入 | REPORTDATE |
| `s_qstmnote_insur_212512` | 认可资产 | REPORTDATE |
| `s_qstmnote_insur_212513` | 认可负债 | REPORTDATE |
| `s_qstmnote_insur_212514` | 实际资本 | REPORTDATE |
| `s_qstmnote_insur_212515` | 核心一级资本 | REPORTDATE |
| `s_qstmnote_insur_212516` | 核心二级资本 | REPORTDATE |
| `s_qstmnote_insur_212517` | 附属一级资本 | REPORTDATE |
| `s_qstmnote_insur_212518` | 附属二级资本 | REPORTDATE |
| `s_qstmnote_insur_212519` | 最低资本 | REPORTDATE |
| `s_qstmnote_insur_212520` | 量化风险最低资本 | REPORTDATE |
| `s_qstmnote_insur_212521` | 寿险业务保险风险最低资本合计 | REPORTDATE |
| `s_qstmnote_insur_212522` | 非寿险业务保险风险最低资本合计 | REPORTDATE |
| `s_qstmnote_insur_212523` | 市场风险最低资本合计 | REPORTDATE |
| `s_qstmnote_insur_212524` | 信用风险最低资本合计 | REPORTDATE |
| `s_qstmnote_insur_212525` | 风险分散效应的资本要求增加 | REPORTDATE |
| `s_qstmnote_insur_212526` | 风险聚合效应的资本要求减少 | REPORTDATE |
| `s_qstmnote_insur_212527` | 控制风险最低资本 | REPORTDATE |
| `s_qstmnote_insur_212528` | 附加资本 | REPORTDATE |
| `s_qstmnote_insur_212529` | 最近一次风险综合评级类别 | REPORTDATE |
| `s_qstmnote_insur_212530` | 净现金流 | REPORTDATE |
| `s_qstmnote_insur_212531` | 净现金流:报告日后第1年 | REPORTDATE |
| `s_qstmnote_insur_212532` | 净现金流:报告日后第2年 | REPORTDATE |
| `s_qstmnote_insur_212533` | 净现金流:报告日后第3年 | REPORTDATE |
| `s_qstmnote_insur_212534` | 综合流动比率:3个月内 | REPORTDATE |
| `s_qstmnote_insur_212535` | 综合流动比率:1年内 | REPORTDATE |
| `s_qstmnote_insur_212536` | 综合流动比率:1年以上 | REPORTDATE |
| `s_qstmnote_insur_212537` | 综合流动比率:1-3年内 | REPORTDATE |
| `s_qstmnote_insur_212538` | 综合流动比率:3-5年内 | REPORTDATE |
| `s_qstmnote_insur_212539` | 综合流动比率:5年以上 | REPORTDATE |
| `s_qstmnote_insur_212540` | 流动性覆盖率:基本情景 | REPORTDATE |
| `s_qstmnote_insur_212541` | 流动性覆盖率:公司整体:压力情景1 | REPORTDATE |
| `s_qstmnote_insur_212542` | 流动性覆盖率:公司整体:压力情景2 | REPORTDATE |
| `s_qstmnote_insur_212543` | 流动性覆盖率:独立账户:压力情景1 | REPORTDATE |
| `s_qstmnote_insur_212544` | 流动性覆盖率:独立账户:压力情景2 | REPORTDATE |
| `s_qstmnote_insur_212546` | 保险风险最低资本合计 | REPORTDATE |
| `s_qstmnote_insur_212547` | 净现金流:报告日后第1年:未来1季度 | REPORTDATE |
| `s_qstmnote_insur_212548` | 净现金流:报告日后第1年:未来2季度 | REPORTDATE |
| `s_qstmnote_insur_212549` | 净现金流:报告日后第1年:未来3季度 | REPORTDATE |
| `s_qstmnote_insur_212550` | 净现金流:报告日后第1年:未来4季度 | REPORTDATE |
| `s_qstmnote_insur_212570` | 流动性覆盖率:公司整体:基本情景:未来3个月 | REPORTDATE |
| `s_qstmnote_insur_212571` | 流动性覆盖率:公司整体:基本情景:未来12个月 | REPORTDATE |
| `s_qstmnote_insur_212572` | 流动性覆盖率:公司整体:必测压力情景:未来3个月 | REPORTDATE |
| `s_qstmnote_insur_212573` | 流动性覆盖率:公司整体:必测压力情景:未来12个月 | REPORTDATE |
| `s_qstmnote_insur_212574` | 流动性覆盖率:不考虑资产变现:必测压力情景:未来3个月 | REPORTDATE |
| `s_qstmnote_insur_212575` | 流动性覆盖率:不考虑资产变现:必测压力情景:未来12个月 | REPORTDATE |
| `s_qstmnote_insur_212576` | 流动性覆盖率:公司整体:自测压力情景:未来3个月 | REPORTDATE |
| `s_qstmnote_insur_212577` | 流动性覆盖率:公司整体:自测压力情景:未来12个月 | REPORTDATE |
| `s_qstmnote_insur_212578` | 流动性覆盖率:不考虑资产变现:自测压力情景:未来3个月 | REPORTDATE |
| `s_qstmnote_insur_212579` | 流动性覆盖率:不考虑资产变现:自测压力情景:未来12个月 | REPORTDATE |
| `s_rate_agencyissuer` | 主体信用评级评级机构 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `s_rate_chngissuer` | 主体信用评级变动方向 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `s_rate_fwdissuer` | 主体信用评级展望 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `s_rate_lateissuerchng` | 主体最新信用评级变动方向 |  |
| `s_rate_latestissurercreditrating` | 主体最新信用评级 |  |
| `s_rate_latestissurercreditrating2` | 主体信用评级 | TRADEDATE、RATINGAGENCY、RatedCompanyType |
| `s_rate_latestissurercreditratingdate` | 主体最新信用评级日期 |  |
| `s_rate_latestissurercreditratingtype` | 主体最新信用评级评级类型 |  |
| `s_rate_lowestissurercreditrating` | 主体最新最低信用评级 |  |
| `s_rate_ratingoutlooks` | 主体最新信用评级展望 |  |
| `s_rating_avg` | 综合评级 |  |
| `s_rating_avgchn` | 综合评级(中文)(新增) | TD |
| `s_rating_avgeng` | 综合评级(英文)(新增) | TD |
| `s_rating_downgrade` | 一月内评级调低家数 |  |
| `s_rating_instnum` | 评级机构家数 |  |
| `s_rating_maintain` | 一月内评级维持家数 |  |
| `s_rating_numofbuy` | 评级买入家数 |  |
| `s_rating_numofhold` | 评级中性家数 |  |
| `s_rating_numofoutperform` | 评级增持家数 |  |
| `s_rating_numofsell` | 评级卖出家数 |  |
| `s_rating_numofunderperform` | 评级减持家数 |  |
| `s_rating_targetprice` | 目标价(综合值) | DATE、PERIOD |
| `s_rating_targetprice_max` | 目标价(MAX) | DATE、PERIOD |
| `s_rating_targetprice_max1` | 目标价(MAX) | DATE |
| `s_rating_targetprice_min` | 目标价(MIN) | DATE、PERIOD |
| `s_rating_targetprice_min1` | 目标价(MIN) | DATE |
| `s_rating_upgrade` | 一月内评级调高家数 |  |
| `s_ratio_arturn` | 应收帐款周转率 | REPORTDATE |
| `s_ratio_assettoequity` | 权益乘数 | REPORTDATE |
| `s_ratio_bps` | 每股净资产(BPS) | REPORTDATE、TYPE |
| `s_ratio_caturn` | 流动资产周转率 | REPORTDATE |
| `s_ratio_cfps` | 每股现金流量(CFPS) | REPORTDATE |
| `s_ratio_current` | 流动比率 | REPORTDATE |
| `s_ratio_debttoasset` | 资产负债率 | REPORTDATE |
| `s_ratio_debttoequity` | 产权比率 | REPORTDATE |
| `s_ratio_divpayout` | 股利支付率 | RPTYEAR |
| `s_ratio_eps` | 每股收益(EPS) | REPORTDATE、TYPE |
| `s_ratio_eps_qty` | 单季度.每股收益EPS(摊薄) | REPORTDATE |
| `s_ratio_eps_ttm` | 每股收益(EPS)TTM |  |
| `s_ratio_grossprofitmargin` | 销售毛利率(GPM) | REPORTDATE |
| `s_ratio_grossprofitmargin_qty` | 单季度.销售毛利率 | REPORTDATE |
| `s_ratio_invturn` | 存货周转率 | REPORTDATE |
| `s_ratio_netprofitmargin` | 销售净利率(NPM) | REPORTDATE |
| `s_ratio_netprofitmargin_qty` | 单季度.销售净利率 | REPORTDATE |
| `s_ratio_quick` | 速动比率 | REPORTDATE |
| `s_ratio_retention` | 收益留存率 | RPTYEAR |
| `s_ratio_roa` | 资产净利率(ROA) | REPORTDATE |
| `s_ratio_roa_qty` | 单季度.资产净利率(ROA) | REPORTDATE |
| `s_ratio_roe` | 权益净利率(ROE) | REPORTDATE、TYPE |
| `s_ratio_roe_qty` | 单季度.权益净利率(ROE) | REPORTDATE |
| `s_ratio_roic` | 投入资本回报率(ROIC) | REPORTDATE |
| `s_ratio_sgr` | 可持续增长率(拟增) | REPORTDATE |
| `s_ratio_sps` | 每股销售额(SPS) | REPORTDATE |
| `s_ratio_taturn` | 总资产周转率 | REPORTDATE |
| `s_refrmkd_apprvbycddate` | 商务部批准日期(新增) |  |
| `s_refrmkd_apprvbysasscdate` | 国资委批准日期(新增) |  |
| `s_refrmkd_apprvddate` | 获准公告日期(新增) |  |
| `s_refrmkd_conscashpaydate` | 对价支付现金支付日(新增) |  |
| `s_refrmkd_conssharelstdate` | 对价支付股票上市日(新增) |  |
| `s_refrmkd_drctvoteenddate` | 董事征集投票权截止日(新增) |  |
| `s_refrmkd_drctvotestartdate` | 董事征集投票权起始日(新增) |  |
| `s_refrmkd_impanncedate` | 股权分置实施股权公告日(新增) |  |
| `s_refrmkd_imprecdate` | 股权分置实施股权登记日(新增) |  |
| `s_refrmkd_imprsmpdate` | 实施阶段复牌日(新增) |  |
| `s_refrmkd_intnetenddate` | 网络投票截止日(新增) |  |
| `s_refrmkd_intnetstartdate` | 网络投票起始日(新增) |  |
| `s_refrmkd_preplandate` | 董事会预案公告日(新增) |  |
| `s_refrmkd_resumpdate` | 预案阶段复牌日(新增) |  |
| `s_refrmkd_smtganncedate` | 股东大会公告日(新增) |  |
| `s_refrmkd_smtgdate` | 股东大会召开日(新增) |  |
| `s_refrmkd_smtgrecdate` | 股东大会股权登记日(新增) |  |
| `s_refrmkd_spotmtgenddate` | 现场股东大会登记截止日(新增) |  |
| `s_refrmkd_spotmtgstartdate` | 现场股东大会登记起始日(新增) |  |
| `s_refrmkd_vttoimprsmpdate` | 表决到实施阶段复牌日(新增) |  |
| `s_refrmschm_abstract` | 对价方案摘要(新增) |  |
| `s_refrmschm_actualcash` | 流通股东每10股实际获得现金数(新增) |  |
| `s_refrmschm_actualnum` | 流通股东每10股实际获得股数(新增) |  |
| `s_refrmschm_callwarrant` | 流通股东每10股获得认购权证数(新增) |  |
| `s_refrmschm_constype` | 对价类型(新增) |  |
| `s_refrmschm_cvntcash` | 折算成送股的对价(WIND计算值)(新增) |  |
| `s_refrmschm_cvntnum` | 折算成送股的对价(上市公司公布值)(新增) |  |
| `s_refrmschm_detail` | 详细对价方案(新增) |  |
| `s_refrmschm_divcomm` | 未来分红承诺(新增) |  |
| `s_refrmschm_incentive` | 股权激励方案(新增) |  |
| `s_refrmschm_injcomm` | 资产注入承诺(新增) |  |
| `s_refrmschm_locktime` | 非流通股持股锁定承诺(新增) |  |
| `s_refrmschm_nominator` | 保荐机构(新增) |  |
| `s_refrmschm_paycash` | 每10股支付现金数(对价)(新增) |  |
| `s_refrmschm_paycashcorp` | 上市公司每10股派息(新增) |  |
| `s_refrmschm_paynum` | 每10股支付股数(对价)(新增) |  |
| `s_refrmschm_purcomm` | 增持承诺(新增) |  |
| `s_refrmschm_putwarrant` | 流通股东每10股获得认沽权证数(新增) |  |
| `s_refrmschm_rvrnum` | 非流通股东每10股缩股(新增) |  |
| `s_refrmschm_schedule` | 股改进度(新增) |  |
| `s_refrmschm_supplecomm` | 其他承诺(新增) |  |
| `s_refrmschm_trffnumcorp` | 上市公司每10股转增股数(新增) |  |
| `s_refrmschm_warrant` | 权证方案说明(新增) |  |
| `s_relatedcb_amount` | 未清偿可转债总量 |  |
| `s_relatedcb_code` | 未清偿可转债代码 |  |
| `s_relatedcb_name` | 未清偿可转债简称 |  |
| `s_relatedcb_yearlyamount` | 年度可转债发行量 |  |
| `s_report_date` | 报告期函数，年份参数、季度参数 | N、TYPE |
| `s_rightsissue_actlnumtoemp` | 职工股实际配股数(新增) |  |
| `s_rightsissue_actlnumtojur` | 法人股实际配股数(新增) |  |
| `s_rightsissue_actlnumtostate` | 国有股实际配股数(新增) |  |
| `s_rightsissue_actlnumtotrd` | 已流通股实际配股数(新增) |  |
| `s_rightsissue_actlnumtotrsf` | 转配股实际配股数(新增) |  |
| `s_rightsissue_amount` | 实际配股数 | RPTYEAR |
| `s_rightsissue_anncedate` | 配股公告日(新增) |  |
| `s_rightsissue_approveddate` | 配股获准公告日(新增) |  |
| `s_rightsissue_baseshare` | 基准股本 | RPTYEAR |
| `s_rightsissue_collection` | 配股募集资金 | RPTYEAR |
| `s_rightsissue_collection_t` | 区间配股募集资金合计 | StartDate、DATE |
| `s_rightsissue_deputyundr` | 配股分销商(新增) |  |
| `s_rightsissue_exdividenddate` | 配股除权日 | RPTYEAR |
| `s_rightsissue_expense` | 配股费用 | RPTYEAR |
| `s_rightsissue_leadundr` | 配股主承销商(新增) |  |
| `s_rightsissue_listeddate` | 配股上市日 | RPTYEAR |
| `s_rightsissue_maxpricepreplan` | 配股预案价上限(新增) |  |
| `s_rightsissue_minpricepreplan` | 配股预案价下限(新增) |  |
| `s_rightsissue_netcollection` | 配股实际募集资金 | RPTYEAR |
| `s_rightsissue_payenddate` | 缴款终止日(新增) |  |
| `s_rightsissue_paystartdate` | 缴款起始日(新增) |  |
| `s_rightsissue_pershare` | 每股配股数 | RPTYEAR |
| `s_rightsissue_planamt` | 计划配股数(新增) |  |
| `s_rightsissue_preplandate` | 预案公告日(新增) |  |
| `s_rightsissue_price` | 配股价格 | RPTYEAR |
| `s_rightsissue_progress` | 配股进度(新增) |  |
| `s_rightsissue_recdateshareb` | B股股权登记日(新增) |  |
| `s_rightsissue_regdateshareb` | 股权登记日(B股最后交易日)(新增) |  |
| `s_rightsissue_registdate` | 配股提交注册日 | Year |
| `s_rightsissue_smtganncedate` | 股东大会公告日(新增) |  |
| `s_rightsissue_subbydistr` | 承销商认购余股(新增) |  |
| `s_rightsissue_sucregistdate` | 配股注册成功日 | Year |
| `s_rightsissue_theornumtoemp` | 职工股理论配股数(新增) |  |
| `s_rightsissue_theornumtojur` | 法人股理论配股数(新增) |  |
| `s_rightsissue_theornumtostate` | 国有股理论配股数(新增) |  |
| `s_rightsissue_theornumtotrd` | 已流通股理论配股数(新增) |  |
| `s_rightsissue_theornumtotrsf` | 转配股理论配股数(新增) |  |
| `s_rightsissue_type` | 配股方式(新增) |  |
| `s_rightsissue_undrtype` | 配股承销方式(新增) |  |
| `s_rightsissue_up5pctactlnum` | 持股5%以上大股东认购股数(新增) |  |
| `s_rightsissue_up5pctnum` | 持股5%以上大股东持股数(新增) |  |
| `s_rightsissue_up5pcttheornum` | 持股5%以上的大股东理论认购股数(新增) |  |
| `s_risk_avgreturn` | 平均收益率 | DEALDATE、TYPE |
| `s_risk_avgreturnr100` | 年化收益率(最近100周)(新增) |  |
| `s_risk_avgreturnr24` | 年化收益率(最近24个月)(新增) |  |
| `s_risk_avgreturnr60` | 年化收益率(最近60个月)(新增) |  |
| `s_risk_avgreturny` | 平均收益率(年化)(新增) | TD1、TD2 |
| `s_risk_avgreturny2` | 平均收益率(年化) |  |
| `s_risk_beta` | Beta值 | DEALDATE、TYPE |
| `s_risk_beta_custom` | Beta值(自定义) | BEGINDATE、EndDate、PERIOD、CalcType、INDEX |
| `s_risk_betadf` | Beta(剔除财务杠杆)(新增) | TD1、TD2 |
| `s_risk_betar100` | BETA值(最近100周)(新增) |  |
| `s_risk_betar24` | BETA值(最近24个月)(新增) |  |
| `s_risk_betar60` | BETA值(最近60个月)(新增) |  |
| `s_risk_betaunincometaxrate` | Beta(剔除所得税率) | StartDate、EndDate |
| `s_risk_eshistorical` | 历史平均损失值ES | StartDate、EndDate |
| `s_risk_esparam` | 参数平均损失值ES | StartDate、EndDate |
| `s_risk_jensen` | Jensen(新增) | TD1、TD2 |
| `s_risk_jenseny` | Jensen(年化)(新增) | TD1、TD2 |
| `s_risk_liquidity` | 流动性指标 | StartDate、EndDate |
| `s_risk_maxdownside` | 最大回撤 | StartDate、EndDate |
| `s_risk_maxdownsidelistedfund` | 最大回撤(行情) | StartDate、EndDate |
| `s_risk_maxupside` | 最大上涨 | StartDate、EndDate |
| `s_risk_nonsysrisk` | 非系统风险 |  |
| `s_risk_premium` | 风险溢价 | TRADEDATE、No_Risk_Yield、Yield_Standard |
| `s_risk_premium2` | 风险溢价(倍) | TRADEDATE、No_Risk_Yield、Yield_Standard |
| `s_risk_sharpe` | Sharpe(新增) | TD1、TD2 |
| `s_risk_stdcof` | 标准差系数 |  |
| `s_risk_stdev` | 年化波动率 | DEALDATE、TYPE |
| `s_risk_stdevclose` | 收盘价标准差 | StartDate、EndDate、Cycle |
| `s_risk_stdevr100` | 年化波动率(最近100周)(新增) |  |
| `s_risk_stdevr24` | 年化波动率(最近24个月)(新增) |  |
| `s_risk_stdevr60` | 年化波动率(最近60个月)(新增) |  |
| `s_risk_stdevy` | 波动率(年化)(新增) | TD1、TD2 |
| `s_risk_treynor` | Treynor(新增) | TD1、TD2 |
| `s_rptcontroller_pct` | 公布实际控制人持股比例 | DEALDATE |
| `s_segment_industry_cost` | 主营构成(按行业)-项目成本 | REPORTDATE |
| `s_segment_industry_cost1` | 主营构成(按行业)-项目成本 | REPORTDATE、TopN |
| `s_segment_industry_gpmargin` | 主营构成(按行业)-项目毛利率 | REPORTDATE、TopN |
| `s_segment_industry_item` | 主营构成(按行业)-项目名称 | REPORTDATE |
| `s_segment_industry_profit` | 主营构成(按行业)-项目利润 | REPORTDATE |
| `s_segment_industry_profit1` | 主营构成(按行业)-项目毛利 | REPORTDATE、TopN |
| `s_segment_industry_sales` | 主营构成(按行业)-项目收入 | REPORTDATE |
| `s_segment_industry_sales1` | 主营构成(按行业)-项目收入 | REPORTDATE、TopN |
| `s_segment_product_cost` | 主营构成(按产品)-项目成本 | REPORTDATE |
| `s_segment_product_cost1` | 主营构成(按产品)-项目成本 | REPORTDATE、TopN |
| `s_segment_product_gpmargin` | 主营构成(按产品)-项目毛利率 | REPORTDATE、TopN |
| `s_segment_product_item` | 主营构成(按产品)-项目名称 | REPORTDATE |
| `s_segment_product_profit` | 主营构成(按产品)-项目利润 | REPORTDATE |
| `s_segment_product_profit1` | 主营构成(按产品)-项目毛利 | REPORTDATE、TopN |
| `s_segment_product_sales` | 主营构成(按产品)-项目收入 | REPORTDATE |
| `s_segment_product_sales1` | 主营构成(按产品)-项目收入 | REPORTDATE、TopN |
| `s_segment_region_cost` | 主营构成(按地区)-项目成本 | REPORTDATE |
| `s_segment_region_cost1` | 主营构成(按地区)-项目成本 | REPORTDATE、TopN |
| `s_segment_region_gpmargin` | 主营构成(按地区)-项目毛利率 | REPORTDATE、TopN |
| `s_segment_region_item` | 主营构成(按地区)-项目名称 | REPORTDATE |
| `s_segment_region_profit` | 主营构成(按地区)-项目利润 | REPORTDATE |
| `s_segment_region_profit1` | 主营构成(按地区)-项目毛利 | REPORTDATE、TopN |
| `s_segment_region_sales` | 主营构成(按地区)-项目收入 | REPORTDATE |
| `s_segment_region_sales1` | 主营构成(按地区)-项目收入 | REPORTDATE、TopN |
| `s_segment_sales` | 主营收入构成(新增) | REPORTDATE、TYPE |
| `s_segment_sm_cost` | 主营构成(按销售模式)-项目成本 | REPORTDATE、TopN |
| `s_segment_sm_gpmargin` | 主营构成(按销售模式)-项目毛利率 | REPORTDATE、TopN |
| `s_segment_sm_item` | 主营构成(按销售模式)-项目名称 | REPORTDATE、TopN |
| `s_segment_sm_profit` | 主营构成(按销售模式)-项目毛利 | REPORTDATE、TopN |
| `s_segment_sm_sales` | 主营构成(按销售模式)-项目收入 | REPORTDATE、TopN |
| `s_share_dr` | 已发行DR数量 | TRADEDATE |
| `s_share_freefloatshr_pct` | 自由流通股占总股本比例 | TRADEDATE |
| `s_share_freeshares` | 自由流通股本(新增) | D |
| `s_share_frozena_holder` | 大股东累计冻结数量 | TRADEDATE、Sequence |
| `s_share_frozena_pct_holder` | 大股东累计冻结数占持股数比例 | TRADEDATE、Sequence |
| `s_share_h` | 香港上市股 |  |
| `s_share_issuing` | 已发行数量 | TRADEDATE |
| `s_share_issuing_mkt` | 流通股本 | TRADEDATE |
| `s_share_liqa` | 流通A股 |  |
| `s_share_liqa_pct` | 流通A股占总股本比例 |  |
| `s_share_liqa_pledged` | 无限售股份质押数量 | TRADEDATE |
| `s_share_liqa_pledgedpct` | 无限售股份质押比例 | TRADEDATE |
| `s_share_liqb` | 流通B股 |  |
| `s_share_liqb_pct` | 流通B股占总股本比例 |  |
| `s_share_liqh_pct` | 流通H股占总股本比例 |  |
| `s_share_n` | 沪(深)股通持股数量 | TRADEDATE |
| `s_share_nontradable` | 股改前非流通股 |  |
| `s_share_nontradable_pct` | 非流通股合计占总股本比例 |  |
| `s_share_ntrd_domesinitor` | 境内发起人股(新增) | D |
| `s_share_ntrd_fundbal` | 基金持有获配股余额(新增) | D |
| `s_share_ntrd_genjuris` | 一般法人股(新增) | D |
| `s_share_ntrd_insderemp` | 内部职工股(新增) | D |
| `s_share_ntrd_ipoinip` | 自然人发起人股(新增) | D |
| `s_share_ntrd_ipojuris` | 募集法人股(新增) | D |
| `s_share_ntrd_nonlstfrgn` | 非上市外资股(新增) | D |
| `s_share_ntrd_prfshare` | 优先股(新增) | D |
| `s_share_ntrd_snormnger` | 高管股(新增) | D |
| `s_share_ntrd_state` | 国家股(新增) | D |
| `s_share_ntrd_state_pct` | 国有股比例(新增) | D |
| `s_share_ntrd_statjur` | 国有法人股(新增) | D |
| `s_share_ntrd_strtinvestor` | 战略投资者持股(新增) | D |
| `s_share_ntrd_subdomesjur` | 境内法人股合计(新增) | D |
| `s_share_ntrd_trfnshare` | 转配股(新增) | D |
| `s_share_otca` | 三板A股 |  |
| `s_share_otca_pct` | 三板A股占总股本比例(新增) | D |
| `s_share_otcb` | 三板B股 |  |
| `s_share_otcb_pct` | 三板B股占总股本比例(新增) | D |
| `s_share_otcrestricted` | 限售三板股 | TRADEDATE |
| `s_share_otcrestricted_backbone` | 限售股份(核心员工) | TRADEDATE |
| `s_share_otcrestricted_controller` | 限售股份(控股股东或实际控制人) | TRADEDATE |
| `s_share_otcrestricted_others` | 限售股份(其他) | TRADEDATE |
| `s_share_otctradable` | 流通三板股 | DATE |
| `s_share_otctradable_backbone` | 流通股(核心员工) | TRADEDATE |
| `s_share_otctradable_controller` | 流通股(控股股东或实际控制人) | TRADEDATE |
| `s_share_otctradable_others` | 流通股(其他) | TRADEDATE |
| `s_share_oversea` | 境外流通股 |  |
| `s_share_oversea_pct` | 海外上市股占总股本比例(新增) | D |
| `s_share_pct_n` | 沪(深)股通持股占比 | TRADEDATE |
| `s_share_pct_ntofreefloat` | 沪(深)股通持股占自由流通股比例 | TRADEDATE |
| `s_share_pct_shnliqa` | 沪(深)股通持股占流通A股比例 | TRADEDATE |
| `s_share_pledged_repurchase` | 质押待购回余量 | TRADEDATE |
| `s_share_pledgeda` | 质押股份数量合计 | TRADEDATE |
| `s_share_pledgeda_holder` | 大股东累计质押数量 | TRADEDATE、Sequence |
| `s_share_pledgeda_largestholder` | 大股东累计质押数量 | TRADEDATE |
| `s_share_pledgeda_pct` | 质押比例 | TRADEDATE |
| `s_share_pledgeda_pct_holder` | 大股东累计质押数占持股数比例 | TRADEDATE、Sequence |
| `s_share_pledgeda_pct_largestholder` | 大股东累计质押数占持股数比例 | TRADEDATE |
| `s_share_restricted_m` | 限售股份(高管持股) | TRADEDATE |
| `s_share_restricted_pct` | 股改限售股份占总股本比例 |  |
| `s_share_restricteda` | 限售A股 |  |
| `s_share_restricteda_detailed` | 限售A股(明细) | DEALDATE、TYPE |
| `s_share_restricteda_pct` | 限售A股占总股本比例(新增) | D |
| `s_share_restricteda_pledged` | 有限售股份质押数量 | TRADEDATE |
| `s_share_restricteda_pledgedpct` | 有限售股份质押比例 | TRADEDATE |
| `s_share_restrictedb` | 限售B股 |  |
| `s_share_restrictedb_pct` | 限售B股占总股本比例(新增) | D |
| `s_share_rsp` | 有限售股份质押待购回余量 | TRADEDATE |
| `s_share_rtd_bance` | 未流通数量 | TRADEDATE |
| `s_share_rtd_datatype` | 解禁数据类型 | TRADEDATE |
| `s_share_rtd_datatype_fwd` | 指定日之后最近一次解禁数据类型 | TRADEDATE |
| `s_share_rtd_domesjur` | 限售股份(境内法人持股)(新增) | D |
| `s_share_rtd_domesnp` | 限售股份(境内自然人持股)(新增) | D |
| `s_share_rtd_frgnjur` | 限售股份(境外法人持股)(新增) | D |
| `s_share_rtd_frgnnp` | 限售股份(境外自然人持股)(新增) | D |
| `s_share_rtd_inst` | 限售股份(机构配售股份)(新增) | D |
| `s_share_rtd_state` | 限售股份(国家持股)(新增) | D |
| `s_share_rtd_statejur` | 限售股份(国有法人持股)(新增) | D |
| `s_share_rtd_subfrgn` | 限售股份(外资持股合计)(新增) | D |
| `s_share_rtd_subotherdomes` | 限售股份(其他内资持股合计)(新增) | D |
| `s_share_rtd_unlockingdate` | 限售解禁日期 | TRADEDATE |
| `s_share_rtd_unlockingdate_fwd` | 指定日之后最近一次解禁日期 | TRADEDATE |
| `s_share_total` | 总股本 |  |
| `s_share_totala` | A股合计 |  |
| `s_share_totala_pct` | A股合计占总股本比例(新增) | D |
| `s_share_totalb` | B股合计 |  |
| `s_share_totalb_pct` | B股合计占总股本比例(新增) | D |
| `s_share_totalotc` | 三板合计 |  |
| `s_share_totalotc_pct` | 三板合计占总股本比例(新增) | D |
| `s_share_totalrestricted` | 限售股合计 |  |
| `s_share_totaltradable` | 流通股合计 |  |
| `s_share_totshares_pre` | 上市前总股本 |  |
| `s_share_tradable_current` | 本期解禁数量 | TRADEDATE |
| `s_share_tradable_current_fwd` | 指定日之后最近一次解禁数量 | TRADEDATE |
| `s_share_tradable_pct` | 流通股合计占总股本比例 |  |
| `s_share_tradable_sharetype` | 解禁股份性质 | TRADEDATE |
| `s_share_tradable_sharetype_fwd` | 指定日之后最近一次解禁股份性质 | TRADEDATE |
| `s_share_usp` | 无限售股份质押待购回余量 | TRADEDATE |
| `s_shareholder_rptcontrolling` | 公布控股股东名称 | TRADEDATE |
| `s_st_stock` | 注册仓单数量 |  |
| `s_stm07_bs` | 07版财务报表资产负债表 | ITEMSCODE、REPORTDATE |
| `s_stm07_bs_10` | 交易性金融资产 | REPORTDATE |
| `s_stm07_bs_100` | 非流动负债差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_101` | 非流动负债差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_102` | 非流动负债差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_103` | 非流动负债合计 | REPORTDATE |
| `s_stm07_bs_104` | 同业和其它金融机构存放款项 | REPORTDATE |
| `s_stm07_bs_105` | 向中央银行借款 | REPORTDATE |
| `s_stm07_bs_106` | 拆入资金 | REPORTDATE |
| `s_stm07_bs_107` | 衍生金融负债 | REPORTDATE |
| `s_stm07_bs_108` | 卖出回购金融资产款 | REPORTDATE |
| `s_stm07_bs_109` | 吸收存款 | REPORTDATE |
| `s_stm07_bs_11` | 应收票据 | REPORTDATE |
| `s_stm07_bs_110` | 代理业务负债 | REPORTDATE |
| `s_stm07_bs_111` | 其他负债 | REPORTDATE |
| `s_stm07_bs_112` | 预收保费 | REPORTDATE |
| `s_stm07_bs_113` | 应付手续费及佣金 | REPORTDATE |
| `s_stm07_bs_114` | 应付分保账款 | REPORTDATE |
| `s_stm07_bs_115` | 存入保证金 | REPORTDATE |
| `s_stm07_bs_116` | 保户储金及投资款 | REPORTDATE |
| `s_stm07_bs_117` | 未到期责任准备金 | REPORTDATE |
| `s_stm07_bs_118` | 未决赔款准备金 | REPORTDATE |
| `s_stm07_bs_119` | 寿险责任准备金 | REPORTDATE |
| `s_stm07_bs_12` | 应收账款 | REPORTDATE |
| `s_stm07_bs_120` | 长期健康险责任准备金 | REPORTDATE |
| `s_stm07_bs_121` | 独立账户负债 | REPORTDATE |
| `s_stm07_bs_122` | 质押借款 | REPORTDATE |
| `s_stm07_bs_123` | 代理买卖证券款 | REPORTDATE |
| `s_stm07_bs_124` | 代理承销证券款 | REPORTDATE |
| `s_stm07_bs_125` | 负债差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_126` | 负债差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_127` | 负债差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_128` | 负债合计 | REPORTDATE |
| `s_stm07_bs_129` | 实收资本(或股本) | REPORTDATE |
| `s_stm07_bs_13` | 其他应收款 | REPORTDATE |
| `s_stm07_bs_130` | 资本公积金 | REPORTDATE |
| `s_stm07_bs_131` | 盈余公积金 | REPORTDATE |
| `s_stm07_bs_132` | 未分配利润 | REPORTDATE |
| `s_stm07_bs_133` | 减：库存股 | REPORTDATE |
| `s_stm07_bs_134` | 一般风险准备 | REPORTDATE |
| `s_stm07_bs_135` | 外币报表折算差额 | REPORTDATE |
| `s_stm07_bs_136` | 少数股东权益 | REPORTDATE |
| `s_stm07_bs_137` | 股东权益差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_138` | 股东权益差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_139` | 其他股东权益差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_14` | 预付账款 | REPORTDATE |
| `s_stm07_bs_140` | 归属母公司股东的权益 | REPORTDATE |
| `s_stm07_bs_141` | 所有者权益合计 | REPORTDATE |
| `s_stm07_bs_142` | 负债及股东权益差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_143` | 负债及股东权益差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_144` | 负债及股东权益差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_145` | 负债及股东权益总计 | REPORTDATE |
| `s_stm07_bs_146` | 定期存款 | REPORTDATE |
| `s_stm07_bs_147` | 应付短期债券 | REPORTDATE |
| `s_stm07_bs_148` | 递延收益-非流动负债 | REPORTDATE |
| `s_stm07_bs_149` | 应付赔付款 | REPORTDATE |
| `s_stm07_bs_15` | 应收股利 | REPORTDATE |
| `s_stm07_bs_150` | 应付保单红利 | REPORTDATE |
| `s_stm07_bs_151` | 未确认的投资损失 | REPORTDATE |
| `s_stm07_bs_152` | 应收分保合同准备金 | REPORTDATE |
| `s_stm07_bs_153` | 吸收存款及同业存放 | REPORTDATE |
| `s_stm07_bs_154` | 保险合同准备金 | REPORTDATE |
| `s_stm07_bs_155` | 应收款项类投资 | REPORTDATE |
| `s_stm07_bs_158` | 专项储备 | REPORTDATE |
| `s_stm07_bs_16` | 应收利息 | REPORTDATE |
| `s_stm07_bs_163` | 其他综合收益 | REPORTDATE、TYPE |
| `s_stm07_bs_164` | 其他权益工具 | REPORTDATE、TYPE |
| `s_stm07_bs_165` | 其他权益工具:优先股 | REPORTDATE、TYPE |
| `s_stm07_bs_169` | 应付款项 | REPORTDATE、TYPE |
| `s_stm07_bs_17` | 存货 | REPORTDATE |
| `s_stm07_bs_170` | 以摊余成本计量的金融资产 | REPORTDATE、TYPE |
| `s_stm07_bs_171` | 以公允价值且其变动计入其他综合收益的金融资产 | REPORTDATE、TYPE |
| `s_stm07_bs_172` | 合同资产 | REPORTDATE、TYPE |
| `s_stm07_bs_173` | 合同负债 | REPORTDATE、TYPE |
| `s_stm07_bs_174` | 应收票据及应收账款 | REPORTDATE、TYPE |
| `s_stm07_bs_175` | 应付票据及应付账款 | REPORTDATE、TYPE |
| `s_stm07_bs_176` | 其他应收款(合计) | REPORTDATE、TYPE |
| `s_stm07_bs_177` | 固定资产(合计) | REPORTDATE、TYPE |
| `s_stm07_bs_178` | 在建工程(合计) | REPORTDATE、TYPE |
| `s_stm07_bs_179` | 其他应付款(合计) | REPORTDATE、TYPE |
| `s_stm07_bs_18` | 消耗性生物资产 | REPORTDATE |
| `s_stm07_bs_180` | 长期应付款(合计) | REPORTDATE、TYPE |
| `s_stm07_bs_181` | 债权投资 | REPORTDATE、TYPE |
| `s_stm07_bs_182` | 其他债权投资 | REPORTDATE、TYPE |
| `s_stm07_bs_183` | 其他权益工具投资 | REPORTDATE、TYPE |
| `s_stm07_bs_184` | 其他非流动金融资产 | REPORTDATE、TYPE |
| `s_stm07_bs_185` | 其他权益工具:永续债 | REPORTDATE、TYPE |
| `s_stm07_bs_187` | 应收款项融资 | REPORTDATE |
| `s_stm07_bs_188` | 使用权资产 | REPORTDATE |
| `s_stm07_bs_189` | 租赁负债 | REPORTDATE |
| `s_stm07_bs_19` | 待摊费用 | REPORTDATE |
| `s_stm07_bs_193` | 应收货币保证金 | REPORTDATE、TYPE |
| `s_stm07_bs_194` | 应收质押保证金 | REPORTDATE、TYPE |
| `s_stm07_bs_195` | 应收结算担保金 | REPORTDATE、TYPE |
| `s_stm07_bs_196` | 期货会员资格投资 | REPORTDATE、TYPE |
| `s_stm07_bs_197` | 应付货币保证金 | REPORTDATE、TYPE |
| `s_stm07_bs_198` | 应付质押保证金 | REPORTDATE、TYPE |
| `s_stm07_bs_199` | 期货风险准备金 | REPORTDATE、TYPE |
| `s_stm07_bs_20` | 一年内到期的非流动资产 | REPORTDATE |
| `s_stm07_bs_200` | 应付期货投资者保障基金 | REPORTDATE、TYPE |
| `s_stm07_bs_204` | 数据资源(开发支出) | REPORTDATE、TYPE |
| `s_stm07_bs_205` | 数据资源(存货) | REPORTDATE、TYPE |
| `s_stm07_bs_206` | 数据资源(无形资产) | REPORTDATE、TYPE |
| `s_stm07_bs_21` | 其他流动资产 | REPORTDATE |
| `s_stm07_bs_22` | 流动资产差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_23` | 流动资产差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_24` | 流动资产差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_25` | 流动资产合计 | REPORTDATE |
| `s_stm07_bs_26` | 可供出售金融资产 | REPORTDATE |
| `s_stm07_bs_27` | 持有至到期投资 | REPORTDATE |
| `s_stm07_bs_28` | 投资性房地产 | REPORTDATE |
| `s_stm07_bs_29` | 长期股权投资 | REPORTDATE |
| `s_stm07_bs_30` | 长期应收款 | REPORTDATE |
| `s_stm07_bs_31` | 固定资产 | REPORTDATE |
| `s_stm07_bs_32` | 工程物资 | REPORTDATE |
| `s_stm07_bs_33` | 在建工程 | REPORTDATE |
| `s_stm07_bs_34` | 固定资产清理 | REPORTDATE |
| `s_stm07_bs_35` | 生产性生物资产 | REPORTDATE |
| `s_stm07_bs_36` | 油气资产 | REPORTDATE |
| `s_stm07_bs_37` | 无形资产 | REPORTDATE |
| `s_stm07_bs_38` | 开发支出 | REPORTDATE |
| `s_stm07_bs_39` | 商誉 | REPORTDATE |
| `s_stm07_bs_40` | 长期待摊费用 | REPORTDATE |
| `s_stm07_bs_41` | 递延所得税资产 | REPORTDATE |
| `s_stm07_bs_42` | 其他非流动资产 | REPORTDATE |
| `s_stm07_bs_43` | 非流动资产差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_44` | 非流动资产差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_45` | 非流动资产差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_46` | 非流动资产合计 | REPORTDATE |
| `s_stm07_bs_47` | 现金及存放中央银行款项 | REPORTDATE |
| `s_stm07_bs_48` | 存放同业和其它金融机构款项 | REPORTDATE |
| `s_stm07_bs_49` | 贵金属 | REPORTDATE |
| `s_stm07_bs_50` | 拆出资金 | REPORTDATE |
| `s_stm07_bs_51` | 衍生金融资产 | REPORTDATE |
| `s_stm07_bs_52` | 买入返售金融资产 | REPORTDATE |
| `s_stm07_bs_53` | 发放贷款及垫款 | REPORTDATE |
| `s_stm07_bs_54` | 代理业务资产 | REPORTDATE |
| `s_stm07_bs_55` | 应收保费 | REPORTDATE |
| `s_stm07_bs_56` | 应收代位追偿款 | REPORTDATE |
| `s_stm07_bs_57` | 应收分保账款 | REPORTDATE |
| `s_stm07_bs_58` | 应收分保未到期责任准备金 | REPORTDATE |
| `s_stm07_bs_59` | 应收分保未决赔款准备金 | REPORTDATE |
| `s_stm07_bs_60` | 应收分保寿险责任准备金 | REPORTDATE |
| `s_stm07_bs_61` | 应收分保长期健康险责任准备金 | REPORTDATE |
| `s_stm07_bs_62` | 存出保证金 | REPORTDATE |
| `s_stm07_bs_63` | 保户质押贷款 | REPORTDATE |
| `s_stm07_bs_64` | 存出资本保证金 | REPORTDATE |
| `s_stm07_bs_65` | 独立账户资产 | REPORTDATE |
| `s_stm07_bs_66` | 客户资金存款 | REPORTDATE |
| `s_stm07_bs_67` | 结算备付金 | REPORTDATE |
| `s_stm07_bs_68` | 客户备付金 | REPORTDATE |
| `s_stm07_bs_69` | 交易席位费 | REPORTDATE |
| `s_stm07_bs_70` | 其他资产 | REPORTDATE |
| `s_stm07_bs_71` | 资产差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_72` | 资产差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_73` | 资产差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_74` | 资产总计 | REPORTDATE |
| `s_stm07_bs_75` | 短期借款 | REPORTDATE |
| `s_stm07_bs_76` | 交易性金融负债 | REPORTDATE |
| `s_stm07_bs_77` | 应付票据 | REPORTDATE |
| `s_stm07_bs_78` | 应付账款 | REPORTDATE |
| `s_stm07_bs_79` | 预收账款 | REPORTDATE |
| `s_stm07_bs_80` | 应付职工薪酬 | REPORTDATE |
| `s_stm07_bs_81` | 应交税费 | REPORTDATE |
| `s_stm07_bs_82` | 应付利息 | REPORTDATE |
| `s_stm07_bs_83` | 应付股利 | REPORTDATE |
| `s_stm07_bs_84` | 其他应付款 | REPORTDATE |
| `s_stm07_bs_85` | 预提费用 | REPORTDATE |
| `s_stm07_bs_86` | 预计负债 | REPORTDATE |
| `s_stm07_bs_87` | 递延收益-流动负债 | REPORTDATE |
| `s_stm07_bs_88` | 一年内到期的非流动负债 | REPORTDATE |
| `s_stm07_bs_89` | 其他流动负债 | REPORTDATE |
| `s_stm07_bs_9` | 货币资金 | REPORTDATE |
| `s_stm07_bs_90` | 流动负债差额(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_91` | 流动负债差额(合计平衡项目) | REPORTDATE |
| `s_stm07_bs_92` | 流动负债差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_bs_93` | 流动负债合计 | REPORTDATE |
| `s_stm07_bs_94` | 长期借款 | REPORTDATE |
| `s_stm07_bs_95` | 应付债券 | REPORTDATE |
| `s_stm07_bs_96` | 长期应付款 | REPORTDATE |
| `s_stm07_bs_97` | 专项应付款 | REPORTDATE |
| `s_stm07_bs_98` | 递延所得税负债 | REPORTDATE |
| `s_stm07_bs_99` | 其他非流动负债 | REPORTDATE |
| `s_stm07_bs_crcassets` | 分出再保险合同资产 | REPORTDATE、TYPE |
| `s_stm07_bs_crcliab` | 分出再保险合同负债 | REPORTDATE、TYPE |
| `s_stm07_bs_fininv` | 金融投资 | REPORTDATE、TYPE |
| `s_stm07_cs` | 07版财务报表现金流量表 | ITEMSCODE、REPORTDATE |
| `s_stm07_cs_10` | 收到的税费返还 | REPORTDATE |
| `s_stm07_cs_100` | 经营性应收项目的减少 | REPORTDATE |
| `s_stm07_cs_101` | 经营性应付项目的增加 | REPORTDATE |
| `s_stm07_cs_102` | 间接法-经营活动现金流量净额差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_103` | 间接法-经营活动现金流量净额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_104` | 间接法-经营活动现金流量净额差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_105` | 间接法-经营活动产生的现金流量净额 | REPORTDATE |
| `s_stm07_cs_106` | 债务转为资本 | REPORTDATE |
| `s_stm07_cs_107` | 一年内到期的可转换公司债券 | REPORTDATE |
| `s_stm07_cs_108` | 融资租入固定资产 | REPORTDATE |
| `s_stm07_cs_109` | 现金的期末余额 | REPORTDATE |
| `s_stm07_cs_11` | 收到的其他与经营活动有关的现金 | REPORTDATE |
| `s_stm07_cs_110` | 现金的期初余额 | REPORTDATE |
| `s_stm07_cs_111` | 现金等价物的期末余额 | REPORTDATE |
| `s_stm07_cs_112` | 现金等价物的期初余额 | REPORTDATE |
| `s_stm07_cs_113` | 间接法-现金净增加额差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_114` | 间接法-现金净增加额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_115` | 间接法-现金净增加额差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_116` | 间接法-现金及现金等价物净增加额 | REPORTDATE |
| `s_stm07_cs_117` | 其他 | REPORTDATE |
| `s_stm07_cs_118` | 子公司吸收少数股东投资收到的现金 | REPORTDATE |
| `s_stm07_cs_119` | 子公司支付给少数股东的股利、利润 | REPORTDATE |
| `s_stm07_cs_12` | 客户存款和同业存放款项净增加额 | REPORTDATE |
| `s_stm07_cs_120` | 未确认的投资损失 | REPORTDATE |
| `s_stm07_cs_121` | 支付保单红利的现金 | REPORTDATE |
| `s_stm07_cs_129` | 拆入/拆出资金净减少额 | REPORTDATE、TYPE |
| `s_stm07_cs_13` | 向中央银行借款净增加额 | REPORTDATE |
| `s_stm07_cs_131` | 信用减值损失 | REPORTDATE |
| `s_stm07_cs_132` | 其他资产减值损失 | REPORTDATE、TYPE |
| `s_stm07_cs_134` | 使用权资产折旧 | REPORTDATE |
| `s_stm07_cs_14` | 向其他金融机构拆入资金净增加额 | REPORTDATE |
| `s_stm07_cs_15` | 收取利息和手续费净增加额 | REPORTDATE |
| `s_stm07_cs_16` | 收到的原保险合同保费取得的现金 | REPORTDATE |
| `s_stm07_cs_17` | 收到的再保业务现金净额 | REPORTDATE |
| `s_stm07_cs_18` | 处置交易性金融资产净增加额 | REPORTDATE |
| `s_stm07_cs_20` | 拆入资金净增加额 | REPORTDATE |
| `s_stm07_cs_21` | 回购业务资金净增加额 | REPORTDATE |
| `s_stm07_cs_22` | 经营活动现金流入差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_23` | 经营活动现金流入差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_24` | 经营活动现金流入差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_25` | 经营活动现金流入小计 | REPORTDATE |
| `s_stm07_cs_26` | 购买商品、接受劳务支付的现金 | REPORTDATE |
| `s_stm07_cs_27` | 支付给职工以及为职工支付的现金 | REPORTDATE |
| `s_stm07_cs_28` | 支付的各项税费 | REPORTDATE |
| `s_stm07_cs_29` | 支付的其他与经营活动有关的现金 | REPORTDATE |
| `s_stm07_cs_30` | 客户贷款及垫款净增加额 | REPORTDATE |
| `s_stm07_cs_31` | 存放央行和同业款项净增加额 | REPORTDATE |
| `s_stm07_cs_32` | 支付赔付款项的现金 | REPORTDATE |
| `s_stm07_cs_33` | 支付手续费的现金 | REPORTDATE |
| `s_stm07_cs_34` | 经营活动现金流出差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_35` | 经营活动现金流出差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_36` | 经营活动现金流出差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_37` | 经营活动现金流出小计 | REPORTDATE |
| `s_stm07_cs_38` | 经营活动产生的现金流量净额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_39` | 经营活动产生的现金流量净额 | REPORTDATE |
| `s_stm07_cs_40` | 收回投资收到的现金 | REPORTDATE |
| `s_stm07_cs_41` | 取得投资收益收到的现金 | REPORTDATE |
| `s_stm07_cs_42` | 处置固定资产、无形资产和其他长期资产收回的现金净额 | REPORTDATE |
| `s_stm07_cs_43` | 处置子公司及其他营业单位收到的现金净额 | REPORTDATE |
| `s_stm07_cs_44` | 收到的其他与投资活动有关的现金 | REPORTDATE |
| `s_stm07_cs_45` | 投资活动现金流入差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_46` | 投资活动现金流入差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_47` | 投资活动现金流入差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_48` | 投资活动现金流入小计 | REPORTDATE |
| `s_stm07_cs_49` | 购建固定资产、无形资产和其他长期资产支付的现金 | REPORTDATE |
| `s_stm07_cs_50` | 投资支付的现金 | REPORTDATE |
| `s_stm07_cs_51` | 取得子公司及其他营业单位支付的现金净额 | REPORTDATE |
| `s_stm07_cs_52` | 支付的其他与投资活动有关的现金 | REPORTDATE |
| `s_stm07_cs_54` | 投资活动现金流出差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_55` | 投资活动现金流出差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_56` | 投资活动现金流出差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_57` | 投资活动现金流出小计 | REPORTDATE |
| `s_stm07_cs_58` | 投资活动产生的现金流量净额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_59` | 投资活动产生的现金流量净额 | REPORTDATE |
| `s_stm07_cs_60` | 吸收投资所收到的现金 | REPORTDATE |
| `s_stm07_cs_61` | 取得借款收到的现金 | REPORTDATE |
| `s_stm07_cs_62` | 收到的其他与筹资活动有关的现金 | REPORTDATE |
| `s_stm07_cs_63` | 发行债券收到的现金 | REPORTDATE |
| `s_stm07_cs_64` | 保户储金净增加额 | REPORTDATE |
| `s_stm07_cs_65` | 筹资活动现金流入差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_66` | 筹资活动现金流入差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_67` | 筹资活动现金流入差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_68` | 筹资活动现金流入小计 | REPORTDATE |
| `s_stm07_cs_69` | 偿还债务所支付的现金 | REPORTDATE |
| `s_stm07_cs_70` | 分配股利、利润和偿付利息所支付的现金 | REPORTDATE |
| `s_stm07_cs_71` | 支付的其他与筹资活动有关的现金 | REPORTDATE |
| `s_stm07_cs_72` | 筹资活动现金流出差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_73` | 筹资活动现金流出差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_74` | 筹资活动现金流出差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_75` | 筹资活动现金流出小计 | REPORTDATE |
| `s_stm07_cs_76` | 筹资活动产生的现金流量净额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_77` | 筹资活动产生的现金流量净额 | REPORTDATE |
| `s_stm07_cs_78` | 汇率变动对现金的影响 | REPORTDATE |
| `s_stm07_cs_79` | 现金净增加额差额(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_80` | 现金及现金等价物净增加额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_cs_81` | 现金净增加额差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_cs_82` | 现金及现金等价物净增加额 | REPORTDATE |
| `s_stm07_cs_83` | 期初现金及现金等价物余额 | REPORTDATE |
| `s_stm07_cs_84` | 期末现金及现金等价物余额 | REPORTDATE |
| `s_stm07_cs_85` | 净利润 | REPORTDATE |
| `s_stm07_cs_86` | 资产减值准备 | REPORTDATE |
| `s_stm07_cs_87` | 固定资产折旧、油气资产折耗、生产性生物资产折旧 | REPORTDATE |
| `s_stm07_cs_88` | 无形资产摊销 | REPORTDATE |
| `s_stm07_cs_89` | 长期待摊费用摊销 | REPORTDATE |
| `s_stm07_cs_9` | 销售商品、提供劳务收到的现金 | REPORTDATE |
| `s_stm07_cs_90` | 待摊费用减少 | REPORTDATE |
| `s_stm07_cs_91` | 预提费用增加 | REPORTDATE |
| `s_stm07_cs_92` | 处置固定资产、无形资产和其他长期资产的损失 | REPORTDATE |
| `s_stm07_cs_93` | 固定资产报废损失 | REPORTDATE |
| `s_stm07_cs_94` | 公允价值变动损失 | REPORTDATE |
| `s_stm07_cs_95` | 财务费用 | REPORTDATE |
| `s_stm07_cs_96` | 投资损失 | REPORTDATE |
| `s_stm07_cs_97` | 递延所得税资产减少 | REPORTDATE |
| `s_stm07_cs_98` | 递延所得税负债增加 | REPORTDATE |
| `s_stm07_cs_99` | 存货的减少 | REPORTDATE |
| `s_stm07_cs_cashpaidclaim` | 支付签发保险合同赔款的现金 | REPORTDATE、TYPE |
| `s_stm07_cs_cashrecprem` | 收到签发保险合同保费取得的现金 | REPORTDATE、TYPE |
| `s_stm07_cs_ntcashpaidcrc` | 支付分出再保险合同的现金净额 | REPORTDATE、TYPE |
| `s_stm07_cs_ntcashrecced` | 收到分入再保险合同的现金净额 | REPORTDATE、TYPE |
| `s_stm07_cs_ntincloanpled` | 保单质押贷款净增加额 | REPORTDATE、TYPE |
| `s_stm07_is` | 07版财务报表利润表 | ITEMSCODE、REPORTDATE |
| `s_stm07_is_10` | 营业成本 | REPORTDATE |
| `s_stm07_is_100` | 终止经营净利润 | REPORTDATE |
| `s_stm07_is_101` | 信用减值损失 | REPORTDATE、TYPE |
| `s_stm07_is_102` | 净敞口套期收益 | REPORTDATE、TYPE |
| `s_stm07_is_103` | 研发费用 | REPORTDATE、TYPE |
| `s_stm07_is_104` | 财务费用:利息费用 | REPORTDATE、TYPE |
| `s_stm07_is_105` | 财务费用:利息收入 | REPORTDATE、TYPE |
| `s_stm07_is_106` | 其他资产减值损失 | REPORTDATE、TYPE |
| `s_stm07_is_108` | 以摊余成本计量的金融资产终止确认收益 | REPORTDATE |
| `s_stm07_is_109` | 营业总成本2 | REPORTDATE |
| `s_stm07_is_11` | 营业税金及附加 | REPORTDATE |
| `s_stm07_is_12` | 销售费用 | REPORTDATE |
| `s_stm07_is_13` | 管理费用 | REPORTDATE |
| `s_stm07_is_14` | 财务费用 | REPORTDATE |
| `s_stm07_is_15` | 资产减值损失 | REPORTDATE |
| `s_stm07_is_16` | 公允价值变动净收益 | REPORTDATE |
| `s_stm07_is_17` | 投资净收益 | REPORTDATE |
| `s_stm07_is_19` | 利息收入 | REPORTDATE |
| `s_stm07_is_20` | 利息支出 | REPORTDATE |
| `s_stm07_is_22` | 手续费及佣金收入 | REPORTDATE |
| `s_stm07_is_23` | 手续费及佣金支出 | REPORTDATE |
| `s_stm07_is_24` | 其他经营净收益 | REPORTDATE |
| `s_stm07_is_25` | 汇兑净收益 | REPORTDATE |
| `s_stm07_is_27` | 营业支出 | REPORTDATE |
| `s_stm07_is_28` | 已赚保费 | REPORTDATE |
| `s_stm07_is_33` | 赔付支出 | REPORTDATE |
| `s_stm07_is_35` | 提取保险合同准备金净额 | REPORTDATE |
| `s_stm07_is_38` | 分保费用 | REPORTDATE |
| `s_stm07_is_39` | 退保金 | REPORTDATE |
| `s_stm07_is_40` | 保单红利支出 | REPORTDATE |
| `s_stm07_is_45` | 营业利润差额(特殊报表科目) | REPORTDATE |
| `s_stm07_is_46` | 营业利润差额(合计平衡项目) | REPORTDATE |
| `s_stm07_is_47` | 营业利润差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_is_48` | 营业利润 | REPORTDATE |
| `s_stm07_is_49` | 营业外收入 | REPORTDATE |
| `s_stm07_is_50` | 营业外支出 | REPORTDATE |
| `s_stm07_is_51` | 非流动资产处置净损失 | REPORTDATE |
| `s_stm07_is_52` | 利润总额差额(特殊报表科目) | REPORTDATE |
| `s_stm07_is_53` | 利润总额差额(合计平衡项目) | REPORTDATE |
| `s_stm07_is_54` | 利润总额差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_is_55` | 利润总额 | REPORTDATE |
| `s_stm07_is_56` | 所得税 | REPORTDATE |
| `s_stm07_is_57` | 净利润差额(特殊报表科目) | REPORTDATE |
| `s_stm07_is_58` | 净利润差额(合计平衡项目) | REPORTDATE |
| `s_stm07_is_59` | 净利润差额说明(特殊报表科目) | REPORTDATE |
| `s_stm07_is_60` | 净利润 | REPORTDATE |
| `s_stm07_is_61` | 归属母公司股东的净利润 | REPORTDATE |
| `s_stm07_is_62` | 少数股东损益 | REPORTDATE |
| `s_stm07_is_82` | 对联营企业和合营企业的投资收益 | REPORTDATE |
| `s_stm07_is_83` | 营业总收入 | REPORTDATE |
| `s_stm07_is_84` | 营业总成本 | REPORTDATE |
| `s_stm07_is_85` | 其他业务收入 | REPORTDATE |
| `s_stm07_is_86` | 其他业务成本 | REPORTDATE |
| `s_stm07_is_87` | 未确认的投资损失 | REPORTDATE |
| `s_stm07_is_9` | 营业收入 | REPORTDATE |
| `s_stm07_is_92` | 其他综合收益 | REPORTDATE |
| `s_stm07_is_93` | 综合收益总额 | REPORTDATE |
| `s_stm07_is_94` | 归属于母公司普通股东综合收益总额 | REPORTDATE |
| `s_stm07_is_95` | 归属于少数股东的综合收益总额 | REPORTDATE |
| `s_stm07_is_97` | 其他收益 | REPORTDATE |
| `s_stm07_is_98` | 资产处置收益 | REPORTDATE |
| `s_stm07_is_99` | 持续经营净利润 | REPORTDATE |
| `s_stm07_is_amortinssvcco` | 摊回保险服务费用 | REPORTDATE、TYPE |
| `s_stm07_is_apportcedprem` | 分出保费的分摊 | REPORTDATE、TYPE |
| `s_stm07_is_cedreinsfingl` | 分出再保险财务损益 | REPORTDATE、TYPE |
| `s_stm07_is_inssvccosts` | 保险服务费用 | REPORTDATE、TYPE |
| `s_stm07_is_inssvcincome` | 保险服务收入 | REPORTDATE、TYPE |
| `s_stm07_is_uwfinloss` | 承保财务损失 | REPORTDATE、TYPE |
| `s_stm_bs` | 股票/原始报表函数/资产负债表 | ITEMSCODE、REPORTDATE |
| `s_stm_cs` | 股票/原始报表函数/现金流量表 | ITEMSCODE、REPORTDATE |
| `s_stm_is` | 股票/原始报表函数/利润表 | ITEMSCODE、REPORTDATE |
| `s_stm_is_53` | 扣除非经常性损益后的净利润 | REPORTDATE |
| `s_stm_issuingdate` | 定期报告披露日期 | REPORTDATE |
| `s_stm_issuingdate2` | 定期报告预计披露日期 | REPORTDATE |
| `s_stm_issuingdate_emrq` | 最近定期报告预计披露日期 |  |
| `s_stm_issuingdate_fs` | 定期报告正报披露日期 | REPORTDATE |
| `s_stm_issuingdate_mrq` | 最近定期报告披露日期 |  |
| `s_stm_ra` | 受限资产 | REPORTDATE、TYPE |
| `s_stm_rf` | 受限资金 | REPORTDATE |
| `s_stmnote_ar` | 股票/报表附注函数/应收帐款明细 | ITEMSCODE、REPORTDATE |
| `s_stmnote_ar_1` | 应收账款-金额 | REPORTDATE |
| `s_stmnote_ar_2` | 应收账款-比例 | REPORTDATE |
| `s_stmnote_ar_3` | 应收账款-坏账准备 | REPORTDATE |
| `s_stmnote_ar_debtor` | 应收账款-主要欠款人 | REPORTDATE、Sequence |
| `s_stmnote_ar_debtor_sum` | 应收账款-主要欠款人欠款金额合计 | REPORTDATE |
| `s_stmnote_ar_debtorname` | 应收账款-主要欠款人名称 | REPORTDATE、TopN |
| `s_stmnote_ar_total` | 应收账款余额 | REPORTDATE、TYPE |
| `s_stmnote_aramount_cat` | 应收账款-金额(按性质) | REPORTDATE、Category |
| `s_stmnote_ardebtorbad` | 应收账款-主要欠款人坏账准备 | REPORTDATE、TopN |
| `s_stmnote_ardebtorrs` | 应收账款-主要欠款人拖欠原因 | REPORTDATE、TopN |
| `s_stmnote_ardebtorrt` | 应收账款-主要欠款人比例 | REPORTDATE、TopN |
| `s_stmnote_ardebtortime` | 应收账款-主要欠款人拖欠时间 | REPORTDATE、TopN |
| `s_stmnote_arratio_cat` | 应收账款-比例(按性质) | REPORTDATE、Category |
| `s_stmnote_assetdetail` | 股票/报表附注函数/资产原值与净值 | ITEMSCODE、REPORTDATE |
| `s_stmnote_assetdetail_1` | 固定资产-原值 | REPORTDATE |
| `s_stmnote_assetdetail_10` | 生产性生物资产-累计折旧 | REPORTDATE |
| `s_stmnote_assetdetail_11` | 生产性生物资产-减值准备 | REPORTDATE |
| `s_stmnote_assetdetail_12` | 生产性生物资产-净额 | REPORTDATE |
| `s_stmnote_assetdetail_13` | 油气资产-原值 | REPORTDATE |
| `s_stmnote_assetdetail_14` | 油气资产-累计折耗 | REPORTDATE |
| `s_stmnote_assetdetail_15` | 油气资产-减值准备 | REPORTDATE |
| `s_stmnote_assetdetail_16` | 油气资产-净额 | REPORTDATE |
| `s_stmnote_assetdetail_17` | 无形资产-原值 | REPORTDATE |
| `s_stmnote_assetdetail_18` | 无形资产-累计摊销 | REPORTDATE |
| `s_stmnote_assetdetail_19` | 无形资产-减值准备 | REPORTDATE |
| `s_stmnote_assetdetail_2` | 固定资产-累计折旧 | REPORTDATE |
| `s_stmnote_assetdetail_20` | 无形资产-净额 | REPORTDATE |
| `s_stmnote_assetdetail_3` | 固定资产-减值准备 | REPORTDATE |
| `s_stmnote_assetdetail_4` | 固定资产-净额 | REPORTDATE |
| `s_stmnote_assetdetail_5` | 投资性房地产-原值 | REPORTDATE |
| `s_stmnote_assetdetail_6` | 投资性房地产-累计折旧 | REPORTDATE |
| `s_stmnote_assetdetail_7` | 投资性房地产-减值准备 | REPORTDATE |
| `s_stmnote_assetdetail_8` | 投资性房地产-净额 | REPORTDATE |
| `s_stmnote_assetdetail_9` | 生产性生物资产-原值 | REPORTDATE |
| `s_stmnote_assetmanage` | 受托管理资产总规模 | REPORTDATE |
| `s_stmnote_assetmanage_inc_c` | 集合资产管理业务收入 | REPORTDATE |
| `s_stmnote_assetmanage_inc_d` | 定向资产管理业务收入 | REPORTDATE |
| `s_stmnote_assetmanage_inc_m` | 公募基金资产管理业务收入 | REPORTDATE |
| `s_stmnote_assetmanage_inc_s` | 专项资产管理业务收入 | REPORTDATE |
| `s_stmnote_associated` | 关联交易(新增) | ITEMSCODE、REPORTDATE、UnitVal |
| `s_stmnote_associated_1` | 向关联方销售产品及提供劳务金额 | REPORTDATE |
| `s_stmnote_associated_2` | 向关联方采购产品及接受劳务金额 | REPORTDATE |
| `s_stmnote_associated_3` | 向关联方提供资金发生额 | REPORTDATE |
| `s_stmnote_associated_4` | 向关联方提供资金余额 | REPORTDATE |
| `s_stmnote_associated_5` | 关联方向上市公司提供资金发生额 | REPORTDATE |
| `s_stmnote_associated_6` | 关联方向上市公司提供资金余额 | REPORTDATE |
| `s_stmnote_aualaccmdiv` | 现金分红总额 | REPORTDATE |
| `s_stmnote_audit_agency` | 审计单位(新增) | D |
| `s_stmnote_audit_am` | 会计准则类型 | REPORTDATE |
| `s_stmnote_audit_category` | 审计意见类别(新增) | D |
| `s_stmnote_audit_cpa` | 签字注册会计师(新增) | D |
| `s_stmnote_audit_date` | 审计报告披露日期 | REPORTDATE |
| `s_stmnote_audit_expense` | 当期实付审计费用(新增) | D |
| `s_stmnote_audit_fee` | 审计费用 | REPORTDATE、TYPE |
| `s_stmnote_audit_interpretation` | 审计结果说明(新增) | D |
| `s_stmnote_audit_kam` | 关键审计事项 | REPORTDATE |
| `s_stmnote_audit_year` | 会计师事务所连续服务年限 | REPORTDATE |
| `s_stmnote_avofa` | 固定资产-净值 | REPORTDATE |
| `s_stmnote_bank` | 股票/报表附注函数/银行专用指标函数 | ITEMSCODE、REPORTDATE |
| `s_stmnote_bank_0001` | 逾期贷款_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0002` | 逾期贷款_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0003` | 逾期贷款_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0004` | 逾期贷款_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0005` | 逾期贷款合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_0011` | 逾期信用贷款_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0012` | 逾期信用贷款_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0013` | 逾期信用贷款_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0014` | 逾期信用贷款_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0015` | 逾期信用贷款合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_0021` | 逾期保证贷款_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0022` | 逾期保证贷款_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0023` | 逾期保证贷款_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0024` | 逾期保证贷款_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0025` | 逾期保证贷款合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_0031` | 逾期抵押贷款_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0032` | 逾期抵押贷款_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0033` | 逾期抵押贷款_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0034` | 逾期抵押贷款_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0035` | 逾期抵押贷款合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_0041` | 逾期票据贴现_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0042` | 逾期票据贴现_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0043` | 逾期票据贴现_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0044` | 逾期票据贴现_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0045` | 逾期票据贴现合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_0051` | 逾期质押贷款_3个月以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0052` | 逾期质押贷款_3个月至1年 | REPORTDATE、TYPE |
| `s_stmnote_bank_0053` | 逾期质押贷款_1年以上3年以内 | REPORTDATE、TYPE |
| `s_stmnote_bank_0054` | 逾期质押贷款_3年以上 | REPORTDATE、TYPE |
| `s_stmnote_bank_0055` | 逾期质押贷款合计 | REPORTDATE、TYPE |
| `s_stmnote_bank_1` | 贷款总额 | REPORTDATE |
| `s_stmnote_bank_10` | 短期资产流动性比例(外币) | REPORTDATE |
| `s_stmnote_bank_10n` | 短期资产流动性比率(外币) | REPORTDATE、TYPE |
| `s_stmnote_bank_11` | 拆入资金比例 | REPORTDATE |
| `s_stmnote_bank_11n` | 拆入资金比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_12` | 拆出资金比例 | REPORTDATE |
| `s_stmnote_bank_129` | 成本收入比(%) | REPORTDATE |
| `s_stmnote_bank_129n` | 成本收入比 | REPORTDATE、TYPE |
| `s_stmnote_bank_12n` | 拆出资金比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_13` | 中长期贷款比例(人民币) | REPORTDATE |
| `s_stmnote_bank_131` | 资本净额 | REPORTDATE |
| `s_stmnote_bank_131n` | 资本净额 | REPORTDATE、TYPE |
| `s_stmnote_bank_132` | 核心资本净额 | REPORTDATE |
| `s_stmnote_bank_132n` | 核心资本净额 | REPORTDATE、TYPE |
| `s_stmnote_bank_133` | 加权风险资产净额 | REPORTDATE |
| `s_stmnote_bank_133n` | 加权风险资产净额 | REPORTDATE、TYPE |
| `s_stmnote_bank_13n` | 中长期贷款比率(人民币) | REPORTDATE、TYPE |
| `s_stmnote_bank_14` | 中长期贷款比例(外币) | REPORTDATE |
| `s_stmnote_bank_144` | 净息差(%) | REPORTDATE |
| `s_stmnote_bank_144n` | 净息差 | REPORTDATE、TYPE |
| `s_stmnote_bank_147` | 净利差(%) | REPORTDATE |
| `s_stmnote_bank_147n` | 净利差 | REPORTDATE、TYPE |
| `s_stmnote_bank_147r` | 净利差(公布值) | REPORTDATE、TYPE |
| `s_stmnote_bank_14n` | 中长期贷款比率(外币) | REPORTDATE、TYPE |
| `s_stmnote_bank_15` | 国际商业借款比例 | REPORTDATE |
| `s_stmnote_bank_15n` | 国际商业借款比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_16` | 利息回收率 | REPORTDATE |
| `s_stmnote_bank_16n` | 利息回收率 | REPORTDATE、TYPE |
| `s_stmnote_bank_17` | 单一最大客户贷款比例 | REPORTDATE |
| `s_stmnote_bank_171` | 杠杆率 | REPORTDATE、TYPE |
| `s_stmnote_bank_172` | 流动性覆盖率 | REPORTDATE、TYPE |
| `s_stmnote_bank_1778` | 银行理财产品余额 | REPORTDATE |
| `s_stmnote_bank_17n` | 单一最大客户贷款比例 | REPORTDATE、TYPE |
| `s_stmnote_bank_18` | 最大十家客户贷款比例 | REPORTDATE |
| `s_stmnote_bank_18n` | 最大十家客户贷款比例 | REPORTDATE、TYPE |
| `s_stmnote_bank_19` | 备付金比例(人民币) | REPORTDATE |
| `s_stmnote_bank_19n` | 备付金比率(人民币) | REPORTDATE、TYPE |
| `s_stmnote_bank_1n` | 贷款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_2` | 存款总额 | REPORTDATE |
| `s_stmnote_bank_20` | 备付金比例(外币) | REPORTDATE |
| `s_stmnote_bank_20n` | 备付金比率(外币) | REPORTDATE、TYPE |
| `s_stmnote_bank_21` | 境外资金运用比例 | REPORTDATE |
| `s_stmnote_bank_21n` | 境外资金运用比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_22` | 贷款呆帐准备金 | REPORTDATE |
| `s_stmnote_bank_22n` | 贷款减值准备 | REPORTDATE、TYPE |
| `s_stmnote_bank_23` | 不良贷款拨备覆盖率 | REPORTDATE |
| `s_stmnote_bank_23n` | 不良贷款拨备覆盖率 | REPORTDATE、TYPE |
| `s_stmnote_bank_24n` | 单一最大客户贷款占贷款总额比例 | REPORTDATE |
| `s_stmnote_bank_25n` | 最大十家客户贷款占贷款总额比例 | REPORTDATE |
| `s_stmnote_bank_26` | 不良贷款余额 | REPORTDATE、TYPE |
| `s_stmnote_bank_2n` | 存款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_3` | 资本充足率 | REPORTDATE |
| `s_stmnote_bank_30` | 非利息收入占比 | REPORTDATE、TYPE |
| `s_stmnote_bank_31` | 正常-金额 | REPORTDATE |
| `s_stmnote_bank_34` | 市场风险资本 | REPORTDATE、TYPE |
| `s_stmnote_bank_35` | 生息资产 | REPORTDATE、TYPE |
| `s_stmnote_bank_37` | 次级-金额 | REPORTDATE |
| `s_stmnote_bank_38` | 计息负债 | REPORTDATE、TYPE |
| `s_stmnote_bank_3n` | 资本充足率 | REPORTDATE、TYPE |
| `s_stmnote_bank_4` | 核心资本充足率 | REPORTDATE |
| `s_stmnote_bank_40` | 可疑-金额 | REPORTDATE |
| `s_stmnote_bank_41` | 非利息收入 | REPORTDATE、TYPE |
| `s_stmnote_bank_42` | 非生息资产 | REPORTDATE、TYPE |
| `s_stmnote_bank_43` | 非计息负债 | REPORTDATE、TYPE |
| `s_stmnote_bank_46` | 短期贷款-平均余额 | REPORTDATE |
| `s_stmnote_bank_47` | 短期贷款-年平均利率 | REPORTDATE |
| `s_stmnote_bank_48` | 中长期贷款-平均余额 | REPORTDATE |
| `s_stmnote_bank_49` | 中长期贷款-年平均利率 | REPORTDATE |
| `s_stmnote_bank_4n` | 核心资本充足率 | REPORTDATE、TYPE |
| `s_stmnote_bank_5` | 不良贷款比例 | REPORTDATE |
| `s_stmnote_bank_50` | 企业存款-平均余额 | REPORTDATE |
| `s_stmnote_bank_51` | 企业存款-年平均利率 | REPORTDATE |
| `s_stmnote_bank_52` | 储蓄存款-平均余额 | REPORTDATE |
| `s_stmnote_bank_53` | 储蓄存款-年平均利率 | REPORTDATE |
| `s_stmnote_bank_5444` | 净息差(公布值) | REPORTDATE、TYPE |
| `s_stmnote_bank_5453` | 库存现金 | REPORTDATE、TYPE |
| `s_stmnote_bank_55` | 拨贷比 | REPORTDATE、TYPE |
| `s_stmnote_bank_57` | 生息资产平均余额 | REPORTDATE、TYPE |
| `s_stmnote_bank_58` | 生息资产收益率 | REPORTDATE、TYPE |
| `s_stmnote_bank_59` | 计息负债平均余额 | REPORTDATE、TYPE |
| `s_stmnote_bank_5n` | 不良贷款比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_6` | 存贷款比例 | REPORTDATE |
| `s_stmnote_bank_60` | 计息负债成本率 | REPORTDATE、TYPE |
| `s_stmnote_bank_611` | 存款余额_个人定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_612` | 存款余额_个人活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_613` | 存款余额_公司定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_614` | 存款余额_公司活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_615` | 存款余额_其它存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_616` | 存款余额_个人存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_617` | 存款余额_公司存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_618` | 存款余额_保证金存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_621` | 存款平均余额_个人定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_622` | 存款平均余额_个人活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_623` | 存款平均余额_公司定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_624` | 存款平均余额_公司活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_625` | 存款平均余额_其它存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_631` | 存款利息支出_个人定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_632` | 存款利息支出_个人活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_633` | 存款利息支出_公司定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_634` | 存款利息支出_公司活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_635` | 存款利息支出_其它存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_641` | 存款平均成本率_个人定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_642` | 存款平均成本率_个人活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_643` | 存款平均成本率_公司定期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_644` | 存款平均成本率_公司活期存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_645` | 存款平均成本率_其它存款 | REPORTDATE、TYPE |
| `s_stmnote_bank_646` | 存款平均成本率_存款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_647` | 存款余额_存款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_648` | 存款平均余额_存款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_649` | 存款利息支出_存款总额 | REPORTDATE、TYPE |
| `s_stmnote_bank_65` | 贷款余额(按行业) | REPORTDATE、TYPE |
| `s_stmnote_bank_66` | 不良贷款余额(按行业) | REPORTDATE、TYPE |
| `s_stmnote_bank_67` | 不良贷款率(按行业) | REPORTDATE、TYPE |
| `s_stmnote_bank_680` | 贷款余额_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_681` | 贷款余额_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_682` | 贷款余额_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_683` | 贷款余额_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_684` | 贷款余额_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_685` | 贷款余额_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_686` | 贷款余额_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_687` | 贷款余额_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_688` | 贷款余额_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_689` | 贷款余额_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_690` | 不良贷款余额_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_691` | 不良贷款余额_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_692` | 不良贷款余额_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_693` | 不良贷款余额_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_694` | 不良贷款余额_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_695` | 不良贷款余额_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_696` | 不良贷款余额_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_697` | 不良贷款余额_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_698` | 不良贷款余额_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_699` | 不良贷款余额_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_6n` | 存贷款比率 | REPORTDATE、TYPE |
| `s_stmnote_bank_7` | 存贷款比例(人民币) | REPORTDATE |
| `s_stmnote_bank_700` | 贷款平均余额_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_701` | 不良贷款率_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_702` | 不良贷款率_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_703` | 不良贷款率_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_704` | 不良贷款率_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_705` | 不良贷款率_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_706` | 不良贷款率_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_707` | 不良贷款率_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_708` | 不良贷款率_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_709` | 不良贷款率_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_710` | 贷款利息收入_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_711` | 贷款平均余额_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_712` | 贷款平均余额_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_713` | 贷款平均余额_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_714` | 贷款平均余额_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_715` | 贷款平均余额_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_716` | 贷款平均余额_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_717` | 贷款平均余额_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_718` | 贷款平均余额_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_719` | 贷款平均余额_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_720` | 贷款平均收益率_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_721` | 贷款利息收入_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_722` | 贷款利息收入_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_723` | 贷款利息收入_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_724` | 贷款利息收入_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_725` | 贷款利息收入_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_726` | 贷款利息收入_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_727` | 贷款利息收入_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_728` | 贷款利息收入_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_729` | 贷款利息收入_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_730` | 不良贷款率_总计 | REPORTDATE、TYPE |
| `s_stmnote_bank_731` | 贷款平均收益率_企业贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_732` | 贷款平均收益率_个人贷款及垫款 | REPORTDATE、TYPE |
| `s_stmnote_bank_733` | 贷款平均收益率_票据贴现 | REPORTDATE、TYPE |
| `s_stmnote_bank_734` | 贷款平均收益率_个人住房贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_735` | 贷款平均收益率_个人消费贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_736` | 贷款平均收益率_信用卡应收账款 | REPORTDATE、TYPE |
| `s_stmnote_bank_737` | 贷款平均收益率_经营性贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_738` | 贷款平均收益率_汽车贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_739` | 贷款平均收益率_其他个人贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_741` | 贷款余额_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_742` | 贷款余额_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_743` | 贷款余额_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_744` | 贷款余额_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_751` | 不良贷款余额_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_752` | 不良贷款余额_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_753` | 不良贷款余额_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_754` | 不良贷款余额_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_761` | 不良贷款率_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_762` | 不良贷款率_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_763` | 不良贷款率_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_764` | 不良贷款率_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_771` | 贷款平均余额_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_772` | 贷款平均余额_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_773` | 贷款平均余额_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_774` | 贷款平均余额_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_781` | 贷款利息收入_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_781210` | 银行信息科技投入 | REPORTDATE |
| `s_stmnote_bank_782` | 贷款利息收入_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_783` | 贷款利息收入_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_784` | 贷款利息收入_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_791` | 贷款平均收益率_信用贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_792` | 贷款平均收益率_保证贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_793` | 贷款平均收益率_抵押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_794` | 贷款平均收益率_质押贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_7n` | 存贷款比率(人民币) | REPORTDATE、TYPE |
| `s_stmnote_bank_8` | 存贷款比例(外币) | REPORTDATE |
| `s_stmnote_bank_801` | 贷款余额_短期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_802` | 贷款余额_中长期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_811` | 不良贷款余额_短期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_812` | 不良贷款余额_中长期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_821` | 不良贷款率_短期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_822` | 不良贷款率_中长期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_841` | 贷款利息收入_短期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_842` | 贷款利息收入_中长期贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_850` | 贷款余额_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_851` | 不良贷款余额_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_852` | 不良贷款率_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_853` | 贷款平均余额_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_854` | 贷款利息收入_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_855` | 贷款平均收益率_中长期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_856` | 贷款余额_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_857` | 不良贷款余额_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_858` | 不良贷款率_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_859` | 贷款平均余额_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_860` | 贷款利息收入_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_861` | 贷款平均收益率_短期公司类贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_8n` | 存贷款比率(外币) | REPORTDATE、TYPE |
| `s_stmnote_bank_9` | 短期资产流动性比例(人民币) | REPORTDATE |
| `s_stmnote_bank_9501` | 正常-迁徙率 | REPORTDATE |
| `s_stmnote_bank_9502` | 关注-迁徙率 | REPORTDATE |
| `s_stmnote_bank_9503` | 次级-迁徙率 | REPORTDATE |
| `s_stmnote_bank_9504` | 可疑-迁徙率 | REPORTDATE |
| `s_stmnote_bank_9506` | 正常-占贷款总额比 | REPORTDATE |
| `s_stmnote_bank_9507` | 关注-占贷款总额比 | REPORTDATE |
| `s_stmnote_bank_9508` | 次级-占贷款总额比 | REPORTDATE |
| `s_stmnote_bank_9509` | 可疑-占贷款总额比 | REPORTDATE |
| `s_stmnote_bank_9510` | 损失-占贷款总额比 | REPORTDATE |
| `s_stmnote_bank_9n` | 短期资产流动性比率(人民币) | REPORTDATE、TYPE |
| `s_stmnote_bank_alb` | 调整后表内外资产余额 | REPORTDATE、TYPE |
| `s_stmnote_bank_ar` | 贷款损失准备充足率 | REPORTDATE、TYPE |
| `s_stmnote_bank_asf` | 可用的稳定资金 | REPORTDATE、TYPE |
| `s_stmnote_bank_assetliqratio` | 短期资产流动性比率(本外币) | REPORTDATE、TYPE |
| `s_stmnote_bank_aucd` | 托管资产(国内系统重要性指标) | REPORTDATE |
| `s_stmnote_bank_aucg` | 托管资产(全球系统重要性指标) | REPORTDATE |
| `s_stmnote_bank_avgrate` | 股票/报表附注函数/银行专用指标函数/平均存贷款利率指标 | ITEMSCODE、REPORTDATE |
| `s_stmnote_bank_capadequacyratio` | 资本充足率(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_capadequacyratio_ct1` | 核心一级资本充足率(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_capadequacyratio_t1` | 一级资本充足率(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_coretier1cap` | 核心一级资本净额(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_fiveclass` | 股票/报表附注函数/银行专用指标函数/银行贷款的五级分类指标 | ITEMSCODE、REPORTDATE |
| `s_stmnote_bank_ibasst` | 同业资产 | REPORTDATE、TYPE |
| `s_stmnote_bank_ibasstpct` | 同业资产占比 | REPORTDATE、TYPE |
| `s_stmnote_bank_ibliabty` | 同业负债 | REPORTDATE、TYPE |
| `s_stmnote_bank_ibliabtypct` | 同业负债占比 | REPORTDATE、TYPE |
| `s_stmnote_bank_impair` | 计提减值准备 | REPORTDATE、TYPE |
| `s_stmnote_bank_ldr` | 贷款逾期率 | REPORTDATE、TYPE |
| `s_stmnote_bank_netequitycap` | 资本净额(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_rl` | 已重组贷款 | REPORTDATE、TYPE |
| `s_stmnote_bank_rsf` | 所需的稳定资金 | REPORTDATE、TYPE |
| `s_stmnote_bank_rweightedassets` | 加权风险资产净额(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_rweightedassets_cr` | 信用风险加权资产(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_rweightedassets_mr` | 市场风险加权资产(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_rweightedassets_or` | 操作风险加权资产(2013) | REPORTDATE、TYPE |
| `s_stmnote_bank_tier1cap` | 一级资本净额(2013) | REPORTDATE、TYPE |
| `s_stmnote_bankdeposit` | 货币资金-银行存款 | REPORTDATE、TYPE |
| `s_stmnote_basicpen_add` | 基本养老保险:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_basicpen_de` | 基本养老保险:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_basicpen_eb` | 基本养老保险:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_basicpen_sb` | 基本养老保险:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_ben_add` | 工资、奖金、津贴和补贴:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_ben_de` | 工资、奖金、津贴和补贴:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_ben_eb` | 工资、奖金、津贴和补贴:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_ben_sb` | 工资、奖金、津贴和补贴:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_borrow_4512` | 借款合计 | REPORTDATE |
| `s_stmnote_cash_deposits_1` | 存放中央银行法定准备金 | REPORTDATE、TYPE |
| `s_stmnote_cash_deposits_2` | 存放中央银行超额存款准备金 | REPORTDATE、TYPE |
| `s_stmnote_cashinvault` | 货币资金-库存现金 | REPORTDATE、TYPE |
| `s_stmnote_cfm1` | 发生额-结构性存款自有资金 | REPORTDATE |
| `s_stmnote_cfm2` | 发生额-结构性存款募集资金 | REPORTDATE |
| `s_stmnote_cfvg_1` | 交易性金融资产 | REPORTDATE、TYPE |
| `s_stmnote_cfvg_2` | 交易性金融负债 | REPORTDATE、TYPE |
| `s_stmnote_cfvg_3` | 衍生金融工具 | REPORTDATE、TYPE |
| `s_stmnote_cfvg_4` | 投资性房地产 | REPORTDATE、TYPE |
| `s_stmnote_cfvg_sum` | 公允价值变动收益-合计 | REPORTDATE、TYPE |
| `s_stmnote_cil_1` | 应收账款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_10` | 融出资金减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_11` | 应收款项减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_12` | 应收款项融资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_13` | 坏账减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_14` | 合同资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_15` | 一年内到期的非流动资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_16` | 发放贷款和垫款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_2` | 应收票据减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_3` | 债权投资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_4` | 其他债权投资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_5` | 其他应收款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_6` | 长期应收款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_cil_9` | 买入返售金融资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_ciltotal` | 信用减值损失-合计 | REPORTDATE、TYPE |
| `s_stmnote_cip_1` | 在建工程合计账面余额 | REPORTDATE、TYPE |
| `s_stmnote_cip_2` | 在建工程合计减值准备 | REPORTDATE、TYPE |
| `s_stmnote_cip_3` | 在建工程合计账面价值 | REPORTDATE、TYPE |
| `s_stmnote_cpc_add` | 企业年金缴费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_cpc_de` | 企业年金缴费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_cpc_eb` | 企业年金缴费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_cpc_sb` | 企业年金缴费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_customertop5` | 前五大客户名称 | REPORTDATE、Sequence |
| `s_stmnote_dataresources` | 数据资源_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_dpst_4405` | 人民币存款 | REPORTDATE |
| `s_stmnote_dpst_4406` | 美元存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4407` | 日元存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4408` | 欧元存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4409` | 港币存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4410` | 英镑存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4411` | 其他货币存款(折算人民币) | REPORTDATE |
| `s_stmnote_dpst_4412` | 银行存款合计 | REPORTDATE |
| `s_stmnote_eduandunionfunds_add` | 工会经费和职工教育经费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_eduandunionfunds_de` | 工会经费和职工教育经费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_eduandunionfunds_eb` | 工会经费和职工教育经费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_eduandunionfunds_sb` | 工会经费和职工教育经费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_emplinjuryins_add` | 工伤保险费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_emplinjuryins_de` | 工伤保险费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_emplinjuryins_eb` | 工伤保险费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_emplinjuryins_sb` | 工伤保险费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_emplpayable_add` | 应付职工薪酬合计:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_emplpayable_de` | 应付职工薪酬合计:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_emplpayable_eb` | 应付职工薪酬合计:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_emplpayable_sb` | 应付职工薪酬合计:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_10` | 企业合并产生的损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_11` | 非货币性资产交换损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_12` | 委托投资损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_13` | 资产减值准备 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_14` | 债务重组损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_15` | 企业重组费用 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_16` | 交易产生的损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_17` | 同一控制下企业合并产生的子公司当期净损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_18` | 预计负债产生的损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_19` | 其他营业外收支净额 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_20` | 中国证监会认定的其他项目 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_21` | 非经常性损益项目小计 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_22` | 所得税影响数 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_23` | 少数股东损益影响数 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_24` | 非经常性损益项目合计 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_28` | 持有(或处置)交易性金融资产和负债产生的公允价值变动损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_29` | 单独进行监制测试的应收款项减值准备转回 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_30` | 对外委托贷款取得的收益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_31` | 公允价值法计量的投资性房地产价值变动损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_32` | 法规要求一次性损益调整影响 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_33` | 受托经营取得的托管费收入 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_6` | 非流动资产处置损益 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_7` | 税收返还、减免 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_8` | 政府补助 | REPORTDATE、TYPE |
| `s_stmnote_eoitems_9` | 资金占用费 | REPORTDATE、TYPE |
| `s_stmnote_faaviableforsale_0001` | 可供出售金融资产:产生的利得/(损失) | REPORTDATE、TYPE |
| `s_stmnote_faaviableforsale_0002` | 可供出售金融资产:产生的所得税影响 | REPORTDATE、TYPE |
| `s_stmnote_faaviableforsale_0003` | 可供出售金融资产:前期计入其他综合收益当期转入损益的金额 | REPORTDATE、TYPE |
| `s_stmnote_faaviableforsale_0004` | 可供出售金融资产公允价值变动 | REPORTDATE、TYPE |
| `s_stmnote_fahb` | 固定资产-房屋及建筑物-原值 | REPORTDATE、TYPE |
| `s_stmnote_fame` | 固定资产-机器设备-原值 | REPORTDATE、TYPE |
| `s_stmnote_fao` | 固定资产-其他-原值 | REPORTDATE、TYPE |
| `s_stmnote_fate` | 固定资产-运输工具-原值 | REPORTDATE、TYPE |
| `s_stmnote_finexp` | 股票/报表附注函数/财务费用明细 | ITEMSCODE、REPORTDATE |
| `s_stmnote_franchiseright` | 特许经营权_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_goodwillbv` | 商誉-账面价值 | REPORTDATE、TYPE |
| `s_stmnote_goodwilldetail` | 商誉-账面价值 | REPORTDATE、TYPE |
| `s_stmnote_goodwillimpairment` | 商誉-减值准备 | REPORTDATE、TYPE |
| `s_stmnote_guarantee` | 股票/报表附注函数/报告期担保数据 | ITEMSCODE、REPORTDATE |
| `s_stmnote_guarantee_1` | 担保发生额合计 | REPORTDATE |
| `s_stmnote_guarantee_2` | 担保余额合计 | REPORTDATE |
| `s_stmnote_guarantee_3` | 关联担保余额合计 | REPORTDATE |
| `s_stmnote_guarantee_4` | 对控股子公司担保发生额合计 | REPORTDATE |
| `s_stmnote_guarantee_5` | 违规担保总额 | REPORTDATE |
| `s_stmnote_guarantee_6` | 担保总额占净资产比例 | REPORTDATE |
| `s_stmnote_housingfund_add` | 住房公积金:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_housingfund_de` | 住房公积金:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_housingfund_eb` | 住房公积金:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_housingfund_sb` | 住房公积金:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_ieaibl_1` | 存放中央银行款项-平均利率 | REPORTDATE、TYPE |
| `s_stmnote_ieaibl_2` | 存拆放同业及其他金融机构-平均利率 | REPORTDATE、TYPE |
| `s_stmnote_ieaibl_3` | 金融投资-平均利率 | REPORTDATE、TYPE |
| `s_stmnote_ieaibl_4` | 同业和其他金融机构存放款项-平均利率 | REPORTDATE、TYPE |
| `s_stmnote_ieaibl_5` | 应付债券-平均利率 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_1` | 长期股权投资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_10` | 固定资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_11` | 无形资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_12` | 使用权资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_13` | 生产性生物资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_14` | 油气资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_15` | 资产减值损失-其他 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_17` | 投资性房地产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_18` | 买入返售金融资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_19` | 贷款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_2` | 工程物资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_20` | 融出资金减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_21` | 应收款项类投资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_22` | 抵债资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_23` | 合同资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_3` | 在建工程减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_4` | 坏账损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_5` | 存货跌价损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_6` | 商誉减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_7` | 发放贷款和垫款减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_8` | 可供出售金融资产减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_9` | 持有至到期投资减值损失 | REPORTDATE、TYPE |
| `s_stmnote_impairmentloss_total` | 资产减值损失-合计 | REPORTDATE、TYPE |
| `s_stmnote_inaudit_agency` | 内控_审计单位 | REPORTDATE |
| `s_stmnote_inaudit_category` | 内控_审计意见类别 | REPORTDATE |
| `s_stmnote_inaudit_cost` | 内控_审计费用 | REPORTDATE、Zone |
| `s_stmnote_inaudit_cpa` | 内控_签字审计师 | REPORTDATE |
| `s_stmnote_inaudit_interpretation` | 内控_审计结果说明 | REPORTDATE |
| `s_stmnote_inaudit_issuingdate` | 内控报告披露日期 | REPORTDATE |
| `s_stmnote_incometax_0` | 当期所得税 | REPORTDATE、TYPE |
| `s_stmnote_incometax_1` | 当期所得税:中国大陆 | REPORTDATE、TYPE |
| `s_stmnote_incometax_2` | 当期所得税:中国香港 | REPORTDATE、TYPE |
| `s_stmnote_incometax_3` | 当期所得税:其他境外 | REPORTDATE、TYPE |
| `s_stmnote_incometax_4` | 以前年度所得税调整 | REPORTDATE、TYPE |
| `s_stmnote_incometax_5` | 递延所得税 | REPORTDATE、TYPE |
| `s_stmnote_incometax_6` | 所得税费用合计 | REPORTDATE、TYPE |
| `s_stmnote_increaseofsurplus` | 法定盈本期增加值 | REPORTDATE、TYPE |
| `s_stmnote_initialsurplus` | 法定盈余期初值 | REPORTDATE、TYPE |
| `s_stmnote_insur_1` | 保单继续率(13个月) | REPORTDATE |
| `s_stmnote_insur_10` | 赔付率(产险) | REPORTDATE |
| `s_stmnote_insur_11` | 费用率(产险) | REPORTDATE |
| `s_stmnote_insur_12` | 偿付能力充足率(产险) | REPORTDATE |
| `s_stmnote_insur_13` | 实际资本(产险) | REPORTDATE |
| `s_stmnote_insur_13n` | 实际资本(产险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_14` | 最低资本(产险) | REPORTDATE |
| `s_stmnote_insur_14n` | 最低资本(产险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_15` | 偿付能力充足率(寿险) | REPORTDATE |
| `s_stmnote_insur_16` | 内含价值(寿险) | REPORTDATE |
| `s_stmnote_insur_16n` | 内含价值(寿险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_17` | 新业务价值(寿险) | REPORTDATE |
| `s_stmnote_insur_17n` | 新业务价值(寿险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_18` | 有效业务价值(寿险) | REPORTDATE |
| `s_stmnote_insur_18n` | 有效业务价值(寿险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_19` | 实际资本(寿险) | REPORTDATE |
| `s_stmnote_insur_195834` | 综合投资收益率 | REPORTDATE、TYPE |
| `s_stmnote_insur_195835` | 综合成本率 | REPORTDATE、TYPE |
| `s_stmnote_insur_195836` | 综合费用率 | REPORTDATE、TYPE |
| `s_stmnote_insur_195837` | 综合赔付率 | REPORTDATE、TYPE |
| `s_stmnote_insur_195838` | 签单保费 | REPORTDATE、TYPE |
| `s_stmnote_insur_195839` | 车险签单保费 | REPORTDATE、TYPE |
| `s_stmnote_insur_19n` | 实际资本(寿险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_2` | 保单继续率(14个月) | REPORTDATE |
| `s_stmnote_insur_20` | 最低资本(寿险) | REPORTDATE |
| `s_stmnote_insur_20n` | 最低资本(寿险) | REPORTDATE、TYPE、CURTYPE |
| `s_stmnote_insur_21` | 新业务价值率(寿险) | REPORTDATE、TYPE |
| `s_stmnote_insur_3` | 保单继续率(25个月) | REPORTDATE |
| `s_stmnote_insur_30n` | 集团内含价值 | REPORTDATE、TYPE |
| `s_stmnote_insur_4` | 保单继续率(26个月) | REPORTDATE |
| `s_stmnote_insur_5` | 净投资收益率 | REPORTDATE |
| `s_stmnote_insur_6` | 总投资收益率 | REPORTDATE |
| `s_stmnote_insur_7` | 评估利率假设：风险贴现率 | REPORTDATE |
| `s_stmnote_insur_7801` | 定期存款 | REPORTDATE |
| `s_stmnote_insur_7802` | 债券投资 | REPORTDATE |
| `s_stmnote_insur_7803` | 基金投资 | REPORTDATE |
| `s_stmnote_insur_7804` | 股票投资 | REPORTDATE |
| `s_stmnote_insur_7805` | 股权投资 | REPORTDATE |
| `s_stmnote_insur_7806` | 基建投资 | REPORTDATE |
| `s_stmnote_insur_7807` | 现金及现金等价物 | REPORTDATE |
| `s_stmnote_insur_7808` | 其它资产 | REPORTDATE |
| `s_stmnote_insur_7809` | 总投资资产 | REPORTDATE |
| `s_stmnote_insur_7810` | 集团客户数 | REPORTDATE |
| `s_stmnote_insur_7811` | 保险营销员人数 | REPORTDATE |
| `s_stmnote_insur_7812` | 保险营销员每月人均首年保险业务收入 | REPORTDATE |
| `s_stmnote_insur_7813` | 保险营销员每月人均寿险新保单件数 | REPORTDATE |
| `s_stmnote_insur_8` | 退保率 | REPORTDATE |
| `s_stmnote_insur_9` | 综合成本率(产险) | REPORTDATE |
| `s_stmnote_insur_mincap` | 最低资本(集团) | REPORTDATE、TYPE |
| `s_stmnote_insur_rcap` | 实际资本(集团) | REPORTDATE、TYPE |
| `s_stmnote_insur_solratio` | 偿付能力充足率(集团) | REPORTDATE、TYPE |
| `s_stmnote_inv` | 股票/报表附注函数/存货项目明细 | ITEMSCODE、REPORTDATE |
| `s_stmnote_inv_1` | 存货明细-原材料 | REPORTDATE |
| `s_stmnote_inv_10` | 存货明细-合同履约成本 | REPORTDATE |
| `s_stmnote_inv_11` | 存货明细-其他存货 | REPORTDATE |
| `s_stmnote_inv_12` | 存货明细-在途物资 | REPORTDATE |
| `s_stmnote_inv_2` | 存货明细-在产品 | REPORTDATE |
| `s_stmnote_inv_3` | 存货明细-产成品 | REPORTDATE |
| `s_stmnote_inv_4` | 存货明细-低值易耗品 | REPORTDATE |
| `s_stmnote_inv_5` | 存货明细-包装物 | REPORTDATE |
| `s_stmnote_inv_6` | 存货明细-委托加工材料 | REPORTDATE |
| `s_stmnote_inv_7` | 存货明细-委托代销商品 | REPORTDATE |
| `s_stmnote_inv_9` | 存货明细-消耗性生物资产 | REPORTDATE |
| `s_stmnote_inv_goodsship` | 存货明细-发出商品 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0001` | 固定息证券投资利息收入 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0002` | 权益投资资产分红收入 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0003` | 投资性房地产租金收入 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0004` | 净投资收益 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0005` | 证券买卖收益 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0006` | 公允价值变动收益 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0007` | 计提投资资产减值准备 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0008` | 处置合营企业净收益 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0009` | 其他收益 | REPORTDATE、TYPE |
| `s_stmnote_investmentincome_0010` | 总投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_1` | 权益法核算的长期股权投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_10` | 投资收益-合计 | REPORTDATE、TYPE |
| `s_stmnote_invincome_11` | 投资收益-其他 | REPORTDATE、TYPE |
| `s_stmnote_invincome_12` | 持有可供出售金融资产等期间取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_13` | 成本法核算的长期股权投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_14` | 处置持有至到期投资取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_15` | 理财产品投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_16` | 应收款项类投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_17` | 金融工具持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_18` | 债权投资在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_19` | 其他债权投资在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_2` | 处置长期股权投资产生的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_20` | 其他权益工具投资在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_21` | 其他非流动金融资产在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_22` | 处置金融工具取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_23` | 处置债权投资取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_24` | 处置其他债权投资取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_25` | 处置其他权益工具投资取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_26` | 处置其他非流动金融资产取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_3` | 以公允价值计量且其变动计入当期损益的金融资产在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_4` | 处置以公允价值计量且变动计入当期损益的金融资产取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_5` | 持有至到期投资在持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_6` | 可供出售金融资产等取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_7` | 处置可供出售金融资产取得的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invincome_8` | 丧失控制权后剩余股权按公允价值重新计量产生的利得 | REPORTDATE、TYPE |
| `s_stmnote_invincome_9` | 处置子公司的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_invtot` | 存货合计 | REPORTDATE |
| `s_stmnote_ird_1` | 名义金额-利率衍生工具(非套期工具) | REPORTDATE、TYPE |
| `s_stmnote_ird_2` | 名义金额-权益衍生工具(非套期工具) | REPORTDATE、TYPE |
| `s_stmnote_landuserights_19` | 土地使用权_原值 | REPORTDATE、TYPE |
| `s_stmnote_landuserights_20` | 土地使用权_累计摊销 | REPORTDATE、TYPE |
| `s_stmnote_landuserights_21` | 土地使用权_减值准备 | REPORTDATE、TYPE |
| `s_stmnote_landuserights_22` | 土地使用权_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_legalsurplusreserve` | 法定盈余期末值 | REPORTDATE、TYPE |
| `s_stmnote_loans_1` | 转融通融入资金 | REPORTDATE、TYPE |
| `s_stmnote_ltborrow_4505` | 人民币长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4506` | 美元长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4507` | 日元长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4508` | 欧元长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4509` | 港币长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4510` | 英镑长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4511` | 其他货币长期借款(折算人民币) | REPORTDATE |
| `s_stmnote_ltborrow_4512` | 长期借款小计 | REPORTDATE |
| `s_stmnote_ltborrow_4513` | 质押长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4514` | 抵押长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4515` | 保证长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4516` | 信用长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4517` | 委托长期借款 | REPORTDATE |
| `s_stmnote_ltborrow_4518` | 其他长期借款 | REPORTDATE |
| `s_stmnote_maternityins_add` | 生育保险费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_maternityins_de` | 生育保险费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_maternityins_eb` | 生育保险费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_maternityins_sb` | 生育保险费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_medins_add` | 医疗保险费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_medins_de` | 医疗保险费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_medins_eb` | 医疗保险费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_medins_sb` | 医疗保险费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_mewprofitapr` | 可分配利润 | REPORTDATE、TYPE |
| `s_stmnote_mgmt_ben` | 管理层年度薪酬总额 | Year |
| `s_stmnote_mgmt_ben_bc` | 董事长薪酬 |  |
| `s_stmnote_mgmt_ben_ceo` | 总经理薪酬 |  |
| `s_stmnote_mgmt_ben_cfo` | 财务总监薪酬 |  |
| `s_stmnote_mgmt_ben_discloser` | 董事会秘书薪酬 |  |
| `s_stmnote_mgmt_ben_sar` | 证券事务代表薪酬 |  |
| `s_stmnote_mgmt_ben_top3b` | 金额前三的董事薪酬合计 | Year |
| `s_stmnote_mgmt_ben_top3m` | 金额前三的高管薪酬合计 | Year |
| `s_stmnote_netinv_1` | 存货明细-原材料(净额) | REPORTDATE |
| `s_stmnote_netinv_10` | 产成品明细-发出商品(净额) | REPORTDATE |
| `s_stmnote_netinv_11` | 存货明细-其他存货(净额) | REPORTDATE |
| `s_stmnote_netinv_12` | 存货明细-在途物资(净额) | REPORTDATE |
| `s_stmnote_netinv_2` | 存货明细-在产品(净额) | REPORTDATE |
| `s_stmnote_netinv_3` | 存货明细-产成品(净额) | REPORTDATE |
| `s_stmnote_netinv_4` | 存货明细-低值易耗品(净额) | REPORTDATE |
| `s_stmnote_netinv_5` | 存货明细-包装物(净额) | REPORTDATE |
| `s_stmnote_netinv_6` | 存货明细-委托加工材料(净额) | REPORTDATE |
| `s_stmnote_netinv_7` | 存货明细-委托代销商品(净额) | REPORTDATE |
| `s_stmnote_netinv_8` | 存货明细-已加工未结算(净额) | REPORTDATE |
| `s_stmnote_netinv_tlt` | 存货合计(净额) | REPORTDATE |
| `s_stmnote_nii_1` | 利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_10` | 发放贷款和垫款利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_11` | 货币资金及结算备付金利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_12` | 金融投资利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_13` | 其他按实际利率法计算的金融资产产生的利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_14` | 融出资金利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_15` | 融资融券利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_16` | 应收融资租赁款利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_17` | 债券投资利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_18` | 债权投资利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_19` | 其他债权投资利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_2` | 买入返售金融资产利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_20` | 其他利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_21` | 代理买卖证券款利息支出 | REPORTDATE、TYPE |
| `s_stmnote_nii_22` | 租赁负债利息支出 | REPORTDATE、TYPE |
| `s_stmnote_nii_23` | 应付短期融资款利息支出 | REPORTDATE、TYPE |
| `s_stmnote_nii_24` | 应付债券利息支出 | REPORTDATE、TYPE |
| `s_stmnote_nii_3` | 买入返售金融资产利息收入-约定购回利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_4` | 买入返售金融资产利息收入-股权质押回购利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_5` | 买入返售金融资产利息收入-股票质押回购利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_6` | 拆出资金利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_7` | 存放及拆放同业利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_8` | 存放中央银行利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nii_9` | 存款利息收入 | REPORTDATE、TYPE |
| `s_stmnote_nonpatentedtechnology` | 非专利技术_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_np_1` | 应付票据-商业承兑汇票 | REPORTDATE、TYPE |
| `s_stmnote_np_2` | 应付票据-银行承兑汇票 | REPORTDATE、TYPE |
| `s_stmnote_np_3` | 应付票据-其他 | REPORTDATE、TYPE |
| `s_stmnote_np_total` | 应付票据-合计 | REPORTDATE、TYPE |
| `s_stmnote_npls` | 租赁资产不良率 | Year |
| `s_stmnote_nr_1` | 应收票据-商业承兑汇票 | REPORTDATE、TYPE |
| `s_stmnote_nr_2` | 应收票据-银行承兑汇票 | REPORTDATE、TYPE |
| `s_stmnote_nr_3` | 应收票据-其他 | REPORTDATE、TYPE |
| `s_stmnote_nr_total` | 应收票据-合计 | REPORTDATE、TYPE |
| `s_stmnote_olrinsur` | 境外人身再保险业务:分保费收入 | REPORTDATE、TYPE |
| `s_stmnote_olrinsuryoy` | 境外人身再保险业务:分保费收入(同比增长率) | REPORTDATE、TYPE |
| `s_stmnote_or` | 其他应收款-金额 | REPORTDATE |
| `s_stmnote_or_debtor` | 其他应收款-主要欠款人欠款金额 | REPORTDATE、TopN |
| `s_stmnote_or_debtorname` | 其他应收款-主要欠款人名称 | REPORTDATE、TopN |
| `s_stmnote_ordebtorbad` | 其他应收款-主要欠款人坏账准备 | REPORTDATE、TopN |
| `s_stmnote_ordebtorpro` | 其他应收款-主要欠款人比例 | REPORTDATE、TopN |
| `s_stmnote_ordebtorrs` | 其他应收款-主要欠款人拖欠原因 | REPORTDATE、TopN |
| `s_stmnote_ordebtortime` | 其他应收款-主要欠款人拖欠时间 | REPORTDATE、TopN |
| `s_stmnote_osrinsur` | 境外储蓄型再保险业务:分保费收入 | REPORTDATE、TYPE |
| `s_stmnote_osrinsuryoy` | 境外储蓄型再保险业务:分保费收入(同比增长率) | REPORTDATE、TYPE |
| `s_stmnote_othernetinv_9` | 其他存货明细-消耗性生物资产(净额) | REPORTDATE |
| `s_stmnote_otherobsin` | 其他境外业务:分保费收入 | REPORTDATE、TYPE |
| `s_stmnote_otherobsinyoy` | 其他境外业务:分保费收入(同比增长率) | REPORTDATE、TYPE |
| `s_stmnote_others_4504` | 政府补助_营业外收入 | REPORTDATE、TYPE |
| `s_stmnote_others_7626` | 工资薪酬(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7627` | 工资薪酬(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7628` | 折旧摊销(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7629` | 折旧摊销(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7630` | 租赁费(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7631` | 租赁费(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7632` | 仓储运输费(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7633` | 广告宣传推广费(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7634` | 业务招待费(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7635` | 差旅费(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7636` | 一年内到期的长期借款 | REPORTDATE、TYPE |
| `s_stmnote_others_7637` | 一年内到期的应付债券 | REPORTDATE、TYPE |
| `s_stmnote_others_7638` | 挂牌费(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7639` | 短期融资债(其他流动负债) | REPORTDATE、TYPE |
| `s_stmnote_others_7640` | 一年内到期的长期应付款 | REPORTDATE、TYPE |
| `s_stmnote_others_7641` | 一年内到期的租赁负债 | REPORTDATE、TYPE |
| `s_stmnote_others_7642` | 其他流动负债(其他) | REPORTDATE、TYPE |
| `s_stmnote_others_7643` | 合计(其他流动负债) | REPORTDATE、TYPE |
| `s_stmnote_others_7644` | 合计(一年内到期的非流动负债) | REPORTDATE、TYPE |
| `s_stmnote_others_7645` | 一年内到期的非流动负债(其他) | REPORTDATE、TYPE |
| `s_stmnote_others_7646` | 研发费用(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7647` | 差旅费(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7648` | 业务招待费(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7649` | 股份支付(销售费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7650` | 股份支付(管理费用) | REPORTDATE、TYPE |
| `s_stmnote_others_7651` | 研发费用-股份支付 | REPORTDATE、TYPE |
| `s_stmnote_patentright` | 专利权_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_profitapr` | 利润分配明细(新增) | ITEMSCODE、D |
| `s_stmnote_profitapr_1` | 期初未分配利润 | REPORTDATE |
| `s_stmnote_profitapr_10` | 提取一般风险准备 | REPORTDATE、TYPE |
| `s_stmnote_profitapr_2` | 本报告期实现净利润 | REPORTDATE |
| `s_stmnote_profitapr_3` | 期末可分配利润 | REPORTDATE |
| `s_stmnote_profitapr_4` | 支付普通股股利 | REPORTDATE |
| `s_stmnote_profitapr_5` | 提取法定盈余公积 | REPORTDATE |
| `s_stmnote_profitapr_6` | 提取任意公积金 | REPORTDATE |
| `s_stmnote_profitapr_8` | 转增股本 | REPORTDATE |
| `s_stmnote_profitapr_9` | 期末未分配利润 | REPORTDATE |
| `s_stmnote_purchase__pct_top5` | 大供应商采购金额占比 | REPORTDATE、Sequence |
| `s_stmnote_purchase_top5` | 大供应商采购金额 | REPORTDATE、Sequence |
| `s_stmnote_purchasetop5` | 前五大供应商采购金额总额 | REPORTDATE |
| `s_stmnote_purchasetop5_pct` | 前五大供应商采购金额占比 | REPORTDATE |
| `s_stmnote_rdda` | 研发费用-折旧摊销 | REPORTDATE |
| `s_stmnote_rde` | 研发支出 | REPORTDATE、TYPE |
| `s_stmnote_rdeca` | 资本化研发支出 | REPORTDATE |
| `s_stmnote_rdeco` | 费用化研发支出 | REPORTDATE |
| `s_stmnote_rded` | 研发支出-折旧摊销 | REPORTDATE |
| `s_stmnote_rdedi` | 研发支出-直接投入 | REPORTDATE |
| `s_stmnote_rdemfp` | 研发支出-材料、燃料和动力费 | REPORTDATE |
| `s_stmnote_rdemployee` | 研发人员数量 | REPORTDATE |
| `s_stmnote_rdemployee_pct` | 研发人员数量占比 | REPORTDATE |
| `s_stmnote_rdeo` | 研发支出-其他 | REPORTDATE |
| `s_stmnote_rdes` | 研发支出-工资薪酬 | REPORTDATE |
| `s_stmnote_rdexp` | 研发支出合计 | REPORTDATE |
| `s_stmnote_rdexp_capital` | 本期资本化研发支出 | REPORTDATE |
| `s_stmnote_rdexp_cost` | 本期费用化研发支出 | REPORTDATE |
| `s_stmnote_rdexp_costtosales` | 研发费用占营业收入比例 | REPORTDATE、TYPE |
| `s_stmnote_rdexp_pct` | 研发投入资本化的比重 | REPORTDATE、TYPE |
| `s_stmnote_rdexptosales` | 研发支出总额占营业收入比例 | REPORTDATE |
| `s_stmnote_rdinv` | 研发费用-直接投入 | REPORTDATE |
| `s_stmnote_rdlease` | 研发费用-租赁费 | REPORTDATE |
| `s_stmnote_rdothers` | 研发费用-其他 | REPORTDATE |
| `s_stmnote_rdsalary` | 研发费用-工资薪酬 | REPORTDATE |
| `s_stmnote_rdtravel` | 研发费用-差旅费 | REPORTDATE、TYPE |
| `s_stmnote_reserve` | 股票/报表附注函数/资产减值准备明细 | ITEMSCODE、REPORTDATE |
| `s_stmnote_sales_pct_top5` | 大客户销售收入占比 | REPORTDATE、Sequence |
| `s_stmnote_sales_top5` | 大客户销售收入 | REPORTDATE、Sequence |
| `s_stmnote_salestop5` | 前五大客户销售收入总额 | REPORTDATE |
| `s_stmnote_salestop5_pct` | 前五大客户销售收入占比 | REPORTDATE |
| `s_stmnote_sec_1` | 净资本 | REPORTDATE |
| `s_stmnote_sec_10` | 融资(含融券)的金额/净资本 | REPORTDATE、TYPE |
| `s_stmnote_sec_1500` | 手续费及佣金收入合计 | REPORTDATE |
| `s_stmnote_sec_1501` | 手续费及佣金收入:证券经纪业务 | REPORTDATE |
| `s_stmnote_sec_1502` | 手续费及佣金收入:受托客户资产管理业务 | REPORTDATE |
| `s_stmnote_sec_1503` | 手续费及佣金收入:证券承销业务 | REPORTDATE |
| `s_stmnote_sec_1504` | 手续费及佣金收入:财务顾问业务 | REPORTDATE |
| `s_stmnote_sec_1505` | 手续费及佣金收入:保荐业务 | REPORTDATE |
| `s_stmnote_sec_1506` | 手续费及佣金收入:投资咨询业务 | REPORTDATE |
| `s_stmnote_sec_1507` | 手续费及佣金收入:期货经纪业务 | REPORTDATE |
| `s_stmnote_sec_1510` | 利息收入合计 | REPORTDATE |
| `s_stmnote_sec_1511` | 利息收入:融资融券业务 | REPORTDATE |
| `s_stmnote_sec_1512` | 利息收入:金融企业往来业务收入 | REPORTDATE |
| `s_stmnote_sec_1513` | 利息收入:金融资产回购业务收入 | REPORTDATE |
| `s_stmnote_sec_1520` | 手续费及佣金净收入合计 | REPORTDATE |
| `s_stmnote_sec_1521` | 手续费及佣金净收入:证券经纪业务 | REPORTDATE |
| `s_stmnote_sec_1522` | 手续费及佣金净收入:受托客户资产管理业务 | REPORTDATE |
| `s_stmnote_sec_1523` | 手续费及佣金净收入:证券承销业务 | REPORTDATE |
| `s_stmnote_sec_1524` | 手续费及佣金净收入:财务顾问业务 | REPORTDATE |
| `s_stmnote_sec_1525` | 手续费及佣金净收入:保荐业务 | REPORTDATE |
| `s_stmnote_sec_1526` | 手续费及佣金净收入:投资咨询业务 | REPORTDATE |
| `s_stmnote_sec_1527` | 手续费及佣金净收入:期货经纪业务 | REPORTDATE |
| `s_stmnote_sec_1528` | 手续费及佣金净收入:基金管理业务 | REPORTDATE |
| `s_stmnote_sec_1530` | 利息净收入合计 | REPORTDATE |
| `s_stmnote_sec_1531` | 利息净收入:融资融券业务 | REPORTDATE |
| `s_stmnote_sec_1532` | 利息净收入:金融企业往来业务收入 | REPORTDATE |
| `s_stmnote_sec_1533` | 利息净收入:金融资产回购业务收入 | REPORTDATE |
| `s_stmnote_sec_1540` | 证券投资业务收入 | REPORTDATE |
| `s_stmnote_sec_1541` | 证券经纪业务收入 | REPORTDATE |
| `s_stmnote_sec_1542` | 投资银行业务收入 | REPORTDATE |
| `s_stmnote_sec_1543` | 资产管理业务收入 | REPORTDATE |
| `s_stmnote_sec_1550` | 证券投资业务净收入 | REPORTDATE |
| `s_stmnote_sec_1551` | 证券经纪业务净收入 | REPORTDATE |
| `s_stmnote_sec_1552` | 投资银行业务净收入 | REPORTDATE |
| `s_stmnote_sec_1553` | 资产管理业务净收入 | REPORTDATE |
| `s_stmnote_sec_1554` | 手续费及佣金净收入:其他业务 | REPORTDATE |
| `s_stmnote_sec_1555` | 手续费及佣金净收入:托管及其他受托业务 | REPORTDATE |
| `s_stmnote_sec_1853` | 权益乘数(剔除客户交易保证金) | REPORTDATE、TYPE |
| `s_stmnote_sec_2` | 受托资金 | REPORTDATE |
| `s_stmnote_sec_3` | 净资本负债率 | REPORTDATE |
| `s_stmnote_sec_30` | 核心净资本 | REPORTDATE、TYPE |
| `s_stmnote_sec_31` | 附属净资本 | REPORTDATE、TYPE |
| `s_stmnote_sec_32` | 各项风险资本准备之和 | REPORTDATE、TYPE |
| `s_stmnote_sec_33` | 表内外资产总额 | REPORTDATE、TYPE |
| `s_stmnote_sec_34` | 资本杠杆率 | REPORTDATE、TYPE |
| `s_stmnote_sec_35` | 流动性覆盖率 | REPORTDATE、TYPE |
| `s_stmnote_sec_36` | 净稳定资金率 | REPORTDATE、TYPE |
| `s_stmnote_sec_4` | 净资本比率 | REPORTDATE |
| `s_stmnote_sec_5` | 净资本/各项风险准备之和 | REPORTDATE |
| `s_stmnote_sec_6` | 净资本/净资产 | REPORTDATE |
| `s_stmnote_sec_7` | 自营权益类证券及证券衍生品/净资本 | REPORTDATE |
| `s_stmnote_sec_8` | 自营固定收益类证券/净资本 | REPORTDATE |
| `s_stmnote_sec_9` | 净资产负债率 | REPORTDATE、TYPE |
| `s_stmnote_sec_leaseseat` | 手续费及佣金收入:证券经纪业务:交易单元席位租赁 | REPORTDATE |
| `s_stmnote_sec_op_1` | 自营证券合计 | REPORTDATE、TYPE |
| `s_stmnote_sec_op_2` | 自营股票 | REPORTDATE、TYPE |
| `s_stmnote_sec_op_3` | 自营国债 | REPORTDATE、TYPE |
| `s_stmnote_sec_op_4` | 自营基金 | REPORTDATE、TYPE |
| `s_stmnote_sec_op_5` | 自营证可转债 | REPORTDATE、TYPE |
| `s_stmnote_sec_resellfin` | 手续费及佣金收入:证券经纪业务:代销金融产品业务 | REPORTDATE |
| `s_stmnote_sec_security` | 手续费及佣金收入:证券经纪业务:代理买卖证券业务 | REPORTDATE |
| `s_stmnote_securitieslending_1` | 融出证券合计 | REPORTDATE、TYPE |
| `s_stmnote_securitieslending_2` | 融出证券:交易性金融资产 | REPORTDATE、TYPE |
| `s_stmnote_securitieslending_3` | 融出证券:可供出售金融资产 | REPORTDATE、TYPE |
| `s_stmnote_securitieslending_4` | 融出证券:转融通融入证券 | REPORTDATE、TYPE |
| `s_stmnote_securitieslending_5` | 融出证券:转融通融入证券余额 | REPORTDATE、TYPE |
| `s_stmnote_securitieslending_6` | 融出证券:减值准备 | REPORTDATE、TYPE |
| `s_stmnote_seg_1501` | 海外业务收入 | REPORTDATE |
| `s_stmnote_seg_1501_pct` | 境外业务收入占比 | REPORTDATE |
| `s_stmnote_seg_1502` | 境外业务成本 | REPORTDATE |
| `s_stmnote_seg_1503` | 境外业务毛利率 | REPORTDATE |
| `s_stmnote_seg_1701` | 主营业务收入 | REPORTDATE、TYPE |
| `s_stmnote_seg_1702` | 主营业务成本 | REPORTDATE、TYPE |
| `s_stmnote_seg_1703` | 其他业务收入 | REPORTDATE、TYPE |
| `s_stmnote_seg_1704` | 其他业务成本 | REPORTDATE、TYPE |
| `s_stmnote_seg_1705` | 营业收入扣除后金额 | REPORTDATE、TYPE |
| `s_stmnote_socialsecurity_add` | 社会保险费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_socialsecurity_de` | 社会保险费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_socialsecurity_eb` | 社会保险费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_socialsecurity_sb` | 社会保险费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_software` | 软件_账面价值 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0001` | 买入返售金融资产:证券 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0002` | 买入返售金融资产:票据 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0003` | 买入返售金融资产:贷款 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0004` | 买入返售金融资产:信托及其他受益权 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0005` | 买入返售金融资产:长期应收款 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0006` | 买入返售金融资产:其他担保物 | REPORTDATE、TYPE |
| `s_stmnote_spuar_0007` | 买入返售金融资产:减值准备 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10001` | 买入返售金融资产:股票质押式回购 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10002` | 买入返售金融资产:约定购回式证券 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10003` | 买入返售金融资产:债券买断式回购 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10004` | 买入返售金融资产:债券质押式回购 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10005` | 买入返售金融资产:其他 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10006` | 买入返售金融资产合计 | REPORTDATE、TYPE |
| `s_stmnote_spuar_10007` | 买入返售金融资产:债券回购 | REPORTDATE、TYPE |
| `s_stmnote_stborrow_4505` | 人民币短期借款 | REPORTDATE |
| `s_stmnote_stborrow_4506` | 美元短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4507` | 日元短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4508` | 欧元短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4509` | 港币短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4510` | 英镑短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4511` | 其他货币短期借款(折算人民币) | REPORTDATE |
| `s_stmnote_stborrow_4512` | 短期借款小计 | REPORTDATE |
| `s_stmnote_stborrow_4513` | 质押短期借款 | REPORTDATE |
| `s_stmnote_stborrow_4514` | 抵押短期借款 | REPORTDATE |
| `s_stmnote_stborrow_4515` | 保证短期借款 | REPORTDATE |
| `s_stmnote_stborrow_4516` | 信用短期借款 | REPORTDATE |
| `s_stmnote_stborrow_4517` | 其他短期借款 | REPORTDATE |
| `s_stmnote_stempl_add` | 短期薪酬:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_stempl_de` | 短期薪酬:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_stempl_ed` | 短期薪酬:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_stempl_sb` | 短期薪酬:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_stoem_add` | 其他短期薪酬:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_stoem_de` | 其他短期薪酬:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_stoem_eb` | 其他短期薪酬:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_stoem_sb` | 其他短期薪酬:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_suppliertop5` | 前五大供应商名称 | REPORTDATE、Sequence |
| `s_stmnote_tax` | 股票/报表附注函数/所得税税率 | RPTYEAR |
| `s_stmnote_tax_building` | 房产税 | REPORTDATE、TYPE |
| `s_stmnote_tax_business` | 营业税金及附加合计 | REPORTDATE、TYPE |
| `s_stmnote_tax_construction` | 城建税 | REPORTDATE、TYPE |
| `s_stmnote_tax_consumption` | 消费税 | REPORTDATE、TYPE |
| `s_stmnote_tax_edesupplementtary` | 教育费附加 | REPORTDATE、TYPE |
| `s_stmnote_tax_oth` | 其他营业税金及附加 | REPORTDATE、TYPE |
| `s_stmnote_tax_stamp` | 印花税 | REPORTDATE、TYPE |
| `s_stmnote_tax_urbanlanduse` | 土地使用税 | REPORTDATE、TYPE |
| `s_stmnote_tfa_1` | 交易性金融资产-股票/股权 | REPORTDATE、TYPE |
| `s_stmnote_tfa_10` | 交易性金融资产-债券/债务 | REPORTDATE、TYPE |
| `s_stmnote_tfa_11` | 交易性金融资产-信托 | REPORTDATE、TYPE |
| `s_stmnote_tfa_12` | 交易性金融资产-理财产品 | REPORTDATE、TYPE |
| `s_stmnote_tfa_13` | 交易性金融资产-永续债/优先股 | REPORTDATE、TYPE |
| `s_stmnote_tfa_14` | 交易性金融资产-资管产品 | REPORTDATE、TYPE |
| `s_stmnote_tfa_15` | 交易性金融资产-非上市股权 | REPORTDATE、TYPE |
| `s_stmnote_tfa_2` | 交易性金融资产-贵金属 | REPORTDATE、TYPE |
| `s_stmnote_tfa_3` | 交易性金融资产-基金(合计) | REPORTDATE、TYPE |
| `s_stmnote_tfa_4` | 交易性金融资产-基金(其他) | REPORTDATE、TYPE |
| `s_stmnote_tfa_5` | 交易性金融资产-私募基金 | REPORTDATE、TYPE |
| `s_stmnote_tfa_6` | 交易性金融资产-公募基金 | REPORTDATE、TYPE |
| `s_stmnote_tfa_7` | 交易性金融资产-票据 | REPORTDATE、TYPE |
| `s_stmnote_tfa_8` | 交易性金融资产-其他 | REPORTDATE、TYPE |
| `s_stmnote_tfa_9` | 交易性金融资产-权益工具 | REPORTDATE、TYPE |
| `s_stmnote_tfainvest` | 交易性金融资产持有期间的投资收益 | REPORTDATE、TYPE |
| `s_stmnote_tfatotal` | 交易性金融资产(合计) | REPORTDATE、TYPE |
| `s_stmnote_txp` | 应交税费 | ITEMSCODE |
| `s_stmnote_txpe` | 应交税费-环境保护税 | REPORTDATE、TYPE |
| `s_stmnote_unemplins_add` | 失业保险费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_unemplins_de` | 失业保险费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_unemplins_eb` | 失业保险费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_unemplins_sb` | 失业保险费:期初余额 | REPORTDATE、TYPE |
| `s_stmnote_vat` | 应交增值税(新增) | ITEMSCODE、D、C |
| `s_stmnote_welfare_add` | 职工福利费:本期增加 | REPORTDATE、TYPE |
| `s_stmnote_welfare_de` | 职工福利费:本期减少 | REPORTDATE、TYPE |
| `s_stmnote_welfare_eb` | 职工福利费:期末余额 | REPORTDATE、TYPE |
| `s_stmnote_welfare_sb` | 职工福利费:期初余额 | REPORTDATE、TYPE |
| `s_techanal_downavgline` | 向下有效突破均线 |  |
| `s_techanal_drpdays` | 连跌天数 |  |
| `s_techanal_incdays` | 连涨天数 |  |
| `s_techanal_limitdowndays` | 区间跌停天数 | StartDate、EndDate |
| `s_techanal_limitupdays` | 区间涨停天数 | StartDate、EndDate |
| `s_techanal_rcnthigh` | 近期创历史新高 |  |
| `s_techanal_rcnthigh_amount` | 近期创历史新高成交额 | TRADEDATE |
| `s_techanal_rcnthigh_days` | 近期创历史新高次数 | TRADEDATE |
| `s_techanal_rcnthigh_vol` | 近期创历史新高成交量 | TRADEDATE |
| `s_techanal_rcntlow` | 近期创历史新低 |  |
| `s_techanal_rcntlow_days` | 近期创历史新低次数 | TRADEDATE |
| `s_techanal_stagehigh` | 近期创阶段新高 |  |
| `s_techanal_stagelow` | 近期创阶段新低 |  |
| `s_techanal_svravgline` | 均线多空头排列看涨看跌 |  |
| `s_techanal_upavgline` | 向上有效突破均线 |  |
| `s_techind_adtm` | ADTM动态买卖气指标 |  |
| `s_techind_arbp` | ARBR人气意愿指标 |  |
| `s_techind_atr` | ATR真实波幅 |  |
| `s_techind_b3612` | B3612三减六日乖离 |  |
| `s_techind_bbi` | BBI多空指数 |  |
| `s_techind_bbiboll` | BBIBOLL多空布林线 |  |
| `s_techind_bias` | BIAS乖离率 |  |
| `s_techind_boll` | BOLL布林线 |  |
| `s_techind_bottom` | 筑底指标 |  |
| `s_techind_cci` | CCI顺势指标 |  |
| `s_techind_cdp` | CDP逆势操作 |  |
| `s_techind_cr` | CR能量指标 |  |
| `s_techind_dbcd` | DBCD异同离差乖离率 |  |
| `s_techind_ddi` | DDI方向标准离差指数 |  |
| `s_techind_dma` | DMA平均线差 |  |
| `s_techind_dmi` | DMI趋向指标 |  |
| `s_techind_dpo` | DPO区间震荡线 |  |
| `s_techind_env` | ENV指标 |  |
| `s_techind_expma` | EXPMA指数平均数 |  |
| `s_techind_kdj` | KDJ随机指标 |  |
| `s_techind_lwr` | LWR威廉指标 |  |
| `s_techind_ma` | MA简单移动平均 |  |
| `s_techind_macd` | MACD指数平滑异同平均 |  |
| `s_techind_mass` | MASS梅丝线 |  |
| `s_techind_mfi` | MFI资金流向指标 |  |
| `s_techind_mi` | MI动量指标 |  |
| `s_techind_micd` | MICD异同离差动力指数 |  |
| `s_techind_mike` | MIKE麦克指标 |  |
| `s_techind_mtm` | MTM动力指标 |  |
| `s_techind_obv` | OBV能量潮 |  |
| `s_techind_poc` | ROC变动速率 |  |
| `s_techind_prdstrong` | 阶段强势指标 |  |
| `s_techind_prdweak` | 阶段弱势指标 |  |
| `s_techind_priceosc` | PRICEOSC价格振荡指标 |  |
| `s_techind_psy` | PSY心理指标 |  |
| `s_techind_pvt` | PVT量价趋势指标 |  |
| `s_techind_pwmi` | 大盘同步指标 |  |
| `s_techind_rc` | RC变化率指数 |  |
| `s_techind_rccd` | RCCD异同离差变化率指数 |  |
| `s_techind_rsi` | RSI相对强弱指标 |  |
| `s_techind_sar` | SAR抛物转向 |  |
| `s_techind_si` | SI摆动指标 |  |
| `s_techind_slowkd` | SLOWKD慢速KD |  |
| `s_techind_sobv` | SOBV能量潮 |  |
| `s_techind_srdm` | SRDM动向速度比率 |  |
| `s_techind_srmi_mi` | SRMI MI修正指标 |  |
| `s_techind_std` | STD标准差 |  |
| `s_techind_tapi` | TAPI加权指数成交值 |  |
| `s_techind_trd_vol_ratio` | 量比 |  |
| `s_techind_trix` | TRIX三重指数平滑平均 |  |
| `s_techind_vhf` | VHF纵横指标 |  |
| `s_techind_vma` | VMA量简单移动平均 |  |
| `s_techind_vmacd` | VMACD量指数平滑异同平均 |  |
| `s_techind_volati` | CVLT佳庆离散指标 |  |
| `s_techind_vosc_vol_osci` | VOSC成交量震荡 |  |
| `s_techind_vr` | VR成交量比率 |  |
| `s_techind_vroc` | VROC量变动速率 |  |
| `s_techind_vrsi` | VRSI量相对强弱 |  |
| `s_techind_vstd` | VSTD成交量标准差 |  |
| `s_techind_wad` | WAD威廉聚散指标 |  |
| `s_techind_wr` | WR威廉指标 |  |
| `s_techind_wvad` | WVAD威廉变异离散量 |  |
| `s_trade_date` | 交易日函数 S_trade_date,根据输入的日期前推后者后退几日找交易日 |  |
| `s_trade_date_current` | 前一交易日 S_trade_Date_Current, |  |
| `s_val_ashrmarketvalue` | 流通A股市值 |  |
| `s_val_ashrmarketvalue2` | A股市值(含限售股) |  |
| `s_val_bshrmarketvalue` | 流通B股市值(人民币) |  |
| `s_val_bshrmarketvalue2` | 流通B股市值(交易币种) |  |
| `s_val_bshrmarketvalue3` | B股市值(含限售股,折人民币) |  |
| `s_val_bshrmarketvalue4` | B股市值(含限售股,交易币种) |  |
| `s_val_dividendyield` | 股息率(股票获利率) |  |
| `s_val_dividendyield2` | 股息率(近12月) |  |
| `s_val_dividendyield3` | 股息率TTM | TRADEDATE |
| `s_val_dividendyield4` | 股息率TTM(剔除特别派息) | TRADEDATE |
| `s_val_estpb` | 预测PB | TRADEDATE、Year |
| `s_val_estpb_fy1` | 预测PB(FY1) | TRADEDATE |
| `s_val_estpb_fy2` | 预测PB(FY2) | TRADEDATE |
| `s_val_estpb_fy3` | 预测PB(FY3) | TRADEDATE |
| `s_val_estpe` | 预测市盈率(PE) |  |
| `s_val_estpe_ftm` | 预测市盈率(PE,未来12个月) |  |
| `s_val_estpe_fy1` | 预测PE(FY1) | TRADEDATE |
| `s_val_estpe_fy2` | 预测PE(FY2) | TRADEDATE |
| `s_val_estpe_fy3` | 预测PE(FY3) | TRADEDATE |
| `s_val_estpe_new` | 预测市盈率(PE,最新预测) | RPTYEAR |
| `s_val_estpeg` | 预测PEG |  |
| `s_val_estpeg_ftm` | 预测PEG(未来12个月) | TRADEDATE |
| `s_val_estpeg_fy1` | 预测PEG(FY1) | TRADEDATE |
| `s_val_estpeg_fy2` | 预测PEG(FY2) | TRADEDATE |
| `s_val_estps` | 预测PS | TRADEDATE、Year |
| `s_val_ev` | 股权价值 |  |
| `s_val_ev1` | 企业价值(含货币资金)(EV1) |  |
| `s_val_ev2` | 企业价值(剔除货币资金)(EV2) |  |
| `s_val_evebitda` | 企业倍数(TTM) | TRADEDATE |
| `s_val_evebitda2` | 企业倍数2(TTM) | TRADEDATE |
| `s_val_evtoebitda` | 企业倍数(EV2/EBITDA) |  |
| `s_val_evtoebitda2` | 企业倍数2(EV2/EBITDA) | TRADEDATE |
| `s_val_mamv` | 备考总市值(并购后) | TRADEDATE |
| `s_val_manetprofit_fy0` | 备考净利润(FY0,并购后) | TRADEDATE |
| `s_val_manetprofit_fy1` | 备考净利润(FY1,并购后) | TRADEDATE |
| `s_val_manetprofit_fy2` | 备考净利润(FY2,并购后) | TRADEDATE |
| `s_val_manetprofit_fy3` | 备考净利润(FY3,并购后) | TRADEDATE |
| `s_val_mape_fy0` | 备考PE(FY0,并购后) | TRADEDATE |
| `s_val_mape_fy1` | 备考PE(FY1,并购后) | TRADEDATE |
| `s_val_mape_fy2` | 备考PE(FY2,并购后) | TRADEDATE |
| `s_val_mape_fy3` | 备考PE(FY3,并购后) | TRADEDATE |
| `s_val_matotalshares` | 备考总股本(并购后) | TRADEDATE |
| `s_val_mv` | 总市值 |  |
| `s_val_mv2` | 总市值(证监会算法) |  |
| `s_val_mv3` | 总市值3 |  |
| `s_val_mv_ard` | 当日总市值(新增) | DEALDATE |
| `s_val_mv_ref` | 参考总市值 | TRADEDATE |
| `s_val_pb` | 市净率(PB) | DEALDATE、TYPE |
| `s_val_pb_avg` | 区间平均PB(LF) | StartDate、EndDate |
| `s_val_pb_high` | 区间最高PB(LF) | StartDate、EndDate |
| `s_val_pb_lf` | 市净率(LF)(新增) | DEALDATE |
| `s_val_pb_low` | 区间最低PB(LF) | StartDate、EndDate |
| `s_val_pb_mrq_ard` | 市净率PB(MRQ) | TRADEDATE |
| `s_val_pb_new` | 市净率(PB,最新) |  |
| `s_val_pcf` | 市现率(PCF) | DEALDATE、TYPE |
| `s_val_pcf_ncf` | 市现率(PCF,现金净流量) |  |
| `s_val_pcf_ncfttm` | 市现率PCF(现金净流量,TTM) |  |
| `s_val_pcf_nflyr_ard` | 市现率PCF(现金净流量LYR) | TRADEDATE |
| `s_val_pcf_ocf` | 市现率(PCF,经营现金流) |  |
| `s_val_pcf_ocflyr_ard` | 市现率PCF(经营现金流LYR) | TRADEDATE |
| `s_val_pcf_ocfttm` | 市现率PCF(经营现金流,TTM) |  |
| `s_val_pcf_ocfttm_ard` | 市现率PCF(经营现金流TTM) | TRADEDATE |
| `s_val_pe` | 市盈率(PE) | DEALDATE、TYPE |
| `s_val_pe_deducted_lyr` | 市盈率PE(lyr,扣除非经常性损益) | DEALDATE |
| `s_val_pe_deducted_ttm` | 市盈率PE(TTM,扣除非经常性损益) | TRADEDATE |
| `s_val_pe_lyr_ard` | 市盈率PE(LYR) | TRADEDATE |
| `s_val_pe_lyr_nongaap` | Non-gaap归母市盈率(LYR) | TRADEDATE |
| `s_val_pe_ttm` | 市盈率(PE,TTM) |  |
| `s_val_peg` | 历史PEG |  |
| `s_val_pelyr_ref` | 参考市盈率PE(LYR) | TRADEDATE |
| `s_val_pep` | 市盈率百分位 | StartDate、EndDate |
| `s_val_pep2` | 市盈率百分位 | TRADEDATE、StartDate、EndDate |
| `s_val_pettm_avg` | 区间平均PE(TTM) | StartDate、EndDate |
| `s_val_pettm_high` | 区间最高PE(TTM) | StartDate、EndDate |
| `s_val_pettm_low` | 区间最低PE(TTM) | StartDate、EndDate |
| `s_val_pettm_median1` | 区间中位数PE(TTM) | StartDate、EndDate |
| `s_val_ps` | 市销率(PS) | DEALDATE、TYPE |
| `s_val_ps_lyr_ard` | 市销率PS(LYR) | TRADEDATE |
| `s_val_ps_ttm` | 市销率(PS,TTM) |  |
| `s_val_pslyr_avg` | 区间平均PS(LYR) | StartDate、EndDate |
| `s_val_pslyr_high` | 区间最高PS(LYR) | StartDate、EndDate |
| `s_val_pslyr_low` | 区间最低PS(LYR) | StartDate、EndDate |
| `s_val_psttm_avg` | 区间平均PS(TTM) | StartDate、EndDate |
| `s_val_psttm_high` | 区间最高PS(TTM) | StartDate、EndDate |
| `s_val_psttm_low` | 区间最低PS(TTM) | StartDate、EndDate |
| `s_val_targetnp` | 股权激励目标净利润 |  |
| `s_valueatrisk_historical` | 历史VaR | StartDate、EndDate |
| `s_valueatrisk_param` | 参数VaR | StartDate、EndDate |
| `s_west_avgbps` | 预测每股净资产平均值 | Year、DATE、PERIOD |
| `s_west_avgbps1` | 预测每股净资产(BPS)平均值 |  |
| `s_west_avgbps_fy1` | 一致预测每股净资产(FY1) | TRADEDATE |
| `s_west_avgbps_fy2` | 一致预测每股净资产(FY2) | TRADEDATE |
| `s_west_avgbps_fy3` | 一致预测每股净资产(FY3) | TRADEDATE |
| `s_west_avgcps` | 预测每股现金流平均值 | Year、DATE、PERIOD |
| `s_west_avgcps1` | 预测每股现金流(CPS)平均值 |  |
| `s_west_avgcps_ftm` | 一致预测每股现金流(未来12个月) | TRADEDATE |
| `s_west_avgcps_fy1` | 一致预测每股现金流(FY1) | TRADEDATE |
| `s_west_avgcps_fy2` | 一致预测每股现金流(FY2) | TRADEDATE |
| `s_west_avgcps_fy3` | 一致预测每股现金流(FY3) | TRADEDATE |
| `s_west_avgdps` | 预测每股股利平均值 | Year、DATE、PERIOD |
| `s_west_avgdps1` | 预测每股股利(DPS)平均值 |  |
| `s_west_avgdps_fy1` | 一致预测每股股利(FY1) | TRADEDATE |
| `s_west_avgdps_fy2` | 一致预测每股股利(FY2) | TRADEDATE |
| `s_west_avgdps_fy3` | 一致预测每股股利(FY3) | TRADEDATE |
| `s_west_avgdps_yoy2` | 一致预测每股股利同比(FY2比FY1) | TRADEDATE |
| `s_west_avgebit` | 预测息税前利润平均值 | Year、DATE、PERIOD |
| `s_west_avgebit1` | 预测息税前利润(EBIT)平均值 |  |
| `s_west_avgebit_cagr` | 一致预测息税前利润年复合增长率 | TRADEDATE |
| `s_west_avgebit_ftm` | 一致预测息税前利润(未来12个月) | TRADEDATE |
| `s_west_avgebit_fy1` | 一致预测息税前利润(FY1) | TRADEDATE |
| `s_west_avgebit_fy2` | 一致预测息税前利润(FY2) | TRADEDATE |
| `s_west_avgebit_fy3` | 一致预测息税前利润(FY3) | TRADEDATE |
| `s_west_avgebit_yoy` | 一致预测息税前利润同比 | TRADEDATE |
| `s_west_avgebitda` | 预测息税折旧摊销前利润平均值 | Year、DATE、PERIOD |
| `s_west_avgebitda1` | 预测息税折旧摊销前利润(EBITDA)平均值 |  |
| `s_west_avgebitda_cagr` | 一致预测息税折旧摊销前利润2年复合增长率 | TRADEDATE |
| `s_west_avgebitda_ftm` | 一致预测息税折旧摊销前利润(未来12个月) | TRADEDATE |
| `s_west_avgebitda_fy1` | 一致预测息税折旧摊销前利润(FY1) | TRADEDATE |
| `s_west_avgebitda_fy2` | 一致预测息税折旧摊销前利润(FY2) | TRADEDATE |
| `s_west_avgebitda_fy3` | 一致预测息税折旧摊销前利润(FY3) | TRADEDATE |
| `s_west_avgebitda_yoy` | 一致预测息税折旧摊销前利润同比 | TRADEDATE |
| `s_west_avgebt` | 预测利润总额平均值 | Year、DATE、PERIOD |
| `s_west_avgebt1` | 预测利润总额平均值 |  |
| `s_west_avgebt_cagr` | 一致预测利润总额2年复合增长率 | TRADEDATE |
| `s_west_avgebt_ftm` | 一致预测利润总额(未来12个月) | TRADEDATE |
| `s_west_avgebt_fy1` | 一致预测利润总额(FY1) | TRADEDATE |
| `s_west_avgebt_fy2` | 一致预测利润总额(FY2) | TRADEDATE |
| `s_west_avgebt_fy3` | 一致预测利润总额(FY3) | TRADEDATE |
| `s_west_avgebt_surprise` | 预测利润总额Surprise |  |
| `s_west_avgebt_surprise_pct` | 预测利润总额Surprise百分比 |  |
| `s_west_avgebt_yoy` | 一致预测利润总额同比 | TRADEDATE |
| `s_west_avggm` | 预测销售毛利率(GM)平均值(可选类型) |  |
| `s_west_avgnp_yoy` | 一致预测净利润同比(FY2比FY1) | TRADEDATE |
| `s_west_avgoc` | 预测营业成本平均值 | Year、TRADEDATE |
| `s_west_avgoc1` | 预测营业成本平均值 | Year、TRADEDATE |
| `s_west_avgoc_cagr` | 一致预测营业成本2年复合增长率 | TRADEDATE |
| `s_west_avgoc_ftm` | 一致预测营业成本(未来12个月) | TRADEDATE |
| `s_west_avgoc_fy1` | 一致预测营业成本(FY1) | TRADEDATE |
| `s_west_avgoc_fy2` | 一致预测营业成本(FY2) | TRADEDATE |
| `s_west_avgoc_fy3` | 一致预测营业成本(FY3) | TRADEDATE |
| `s_west_avgoc_surprise` | 预测营业成本Surprise |  |
| `s_west_avgoc_surprise_pct` | 预测营业成本Surprise百分比 |  |
| `s_west_avgoc_yoy` | 一致预测营业成本同比 | TRADEDATE |
| `s_west_avgoperatingprofit` | 预测营业利润平均值 | Year、DATE、PERIOD |
| `s_west_avgoperatingprofit1` | 预测营业利润平均值 |  |
| `s_west_avgoperatingprofit_cagr` | 一致预测营业利润2年复合增长率 | TRADEDATE |
| `s_west_avgoperatingprofit_ftm` | 一致预测营业利润(未来12个月) | TRADEDATE |
| `s_west_avgoperatingprofit_fy1` | 一致预测营业利润(FY1) | TRADEDATE |
| `s_west_avgoperatingprofit_fy2` | 一致预测营业利润(FY2) | TRADEDATE |
| `s_west_avgoperatingprofit_fy3` | 一致预测营业利润(FY3) | TRADEDATE |
| `s_west_avgoperatingprofit_surprise` | 预测营业利润Surprise |  |
| `s_west_avgoperatingprofit_surprise_pct` | 预测营业利润Surprise百分比 |  |
| `s_west_avgoperatingprofit_yoy` | 一致预测营业利润同比 | TRADEDATE |
| `s_west_avgopm` | 预测营业利润率(OPM)平均值(可选类型) |  |
| `s_west_avgroa` | 预测总资产收益率平均值 | Year、DATE、PERIOD |
| `s_west_avgroe` | 预测净资产收益率平均值 | Year、DATE、PERIOD |
| `s_west_avgroe_fy1` | 一致预测ROE(FY1) | TRADEDATE |
| `s_west_avgroe_fy2` | 一致预测ROE(FY2) | TRADEDATE |
| `s_west_avgroe_fy3` | 一致预测ROE(FY3) | TRADEDATE |
| `s_west_avgroe_yoy` | 一致预测ROE同比 | TRADEDATE |
| `s_west_avgshares` | 预测基准股本综合值 | TRADEDATE、Year |
| `s_west_bps_surprise` | 预测每股净资产Surprise |  |
| `s_west_bps_surprise_pct` | 预测每股净资产Surprise百分比 |  |
| `s_west_eps` | 预测每股收益平均值 | Year、DATE、PERIOD |
| `s_west_eps1` | 预测每股收益平均值 |  |
| `s_west_eps_ftm` | 一致预测每股收益(未来12个月) | TRADEDATE |
| `s_west_eps_fy1` | 一致预测每股收益(FY1) | TRADEDATE |
| `s_west_eps_fy2` | 一致预测每股收益(FY2) | TRADEDATE |
| `s_west_eps_fy3` | 一致预测每股收益(FY3) | TRADEDATE |
| `s_west_eps_surprise` | 预测每股收益Surprise |  |
| `s_west_eps_surprise_pct` | 预测每股收益Surprise百分比 |  |
| `s_west_instnum` | 每股收益预测机构家数 | Year、DATE、PERIOD |
| `s_west_instnum_bps` | 每股净资产预测机构家数 |  |
| `s_west_instnum_cps` | 每股现金流预测机构家数 |  |
| `s_west_instnum_dps` | 每股股利预测机构家数 |  |
| `s_west_instnum_ebit` | 息税前利润预测机构家数 |  |
| `s_west_instnum_ebitda` | 息税折旧摊销前利润预测机构家数 |  |
| `s_west_instnum_ebt` | 利润总额预测机构家数 |  |
| `s_west_instnum_gm` | 销售毛利率预测机构家数(可选类型) |  |
| `s_west_instnum_np` | 净利润预测机构家数 |  |
| `s_west_instnum_op` | 营业利润预测机构家数 |  |
| `s_west_instnum_opm` | 营业利润率(OPM)预测机构家数(可选类型) |  |
| `s_west_instnum_roa` | 总资产收益率预测机构家数 |  |
| `s_west_instnum_roe` | 净资产收益率预测机构家数 |  |
| `s_west_instnum_sales` | 营业收入预测机构家数 |  |
| `s_west_maxbps` | 预测每股净资产最大值 | Year、DATE、PERIOD |
| `s_west_maxbps1` | 预测每股净资产(BPS)最大值 |  |
| `s_west_maxcps` | 预测每股现金流最大值 | Year、DATE、PERIOD |
| `s_west_maxcps1` | 预测每股现金流(CPS)最大值 |  |
| `s_west_maxdps` | 预测每股股利最大值 | Year、DATE、PERIOD |
| `s_west_maxdps1` | 预测每股股利(DPS)最大值 |  |
| `s_west_maxebit` | 预测息税前利润最大值 | Year、DATE、PERIOD |
| `s_west_maxebit1` | 预测息税前利润(EBIT)最大值 |  |
| `s_west_maxebitda` | 预测息税折旧摊销前利润最大值 | Year、DATE、PERIOD |
| `s_west_maxebitda1` | 预测息税折旧摊销前利润(EBITDA)最大值 |  |
| `s_west_maxebt` | 预测利润总额最大值 | Year、DATE、PERIOD |
| `s_west_maxebt1` | 预测利润总额最大值 |  |
| `s_west_maxeps` | 预测每股收益最大值 | Year、DATE、PERIOD |
| `s_west_maxeps1` | 预测每股收益最大值 |  |
| `s_west_maxgm` | 预测销售毛利率(GM)最大值(可选类型) |  |
| `s_west_maxnetprofit` | 预测净利润最大值 | Year、DATE、PERIOD |
| `s_west_maxnetprofit1` | 预测净利润最大值 |  |
| `s_west_maxoc` | 预测营业成本最大值 | TRADEDATE、Year |
| `s_west_maxoc1` | 预测营业成本最大值 | TRADEDATE、Year |
| `s_west_maxoperatingprofit` | 预测营业利润最大值 | Year、DATE、PERIOD |
| `s_west_maxoperatingprofit1` | 预测营业利润最大值 |  |
| `s_west_maxopm` | 预测营业利润率(OPM)最大值(可选类型) |  |
| `s_west_maxroa` | 预测总资产收益率最大值 | Year、DATE、PERIOD |
| `s_west_maxroe` | 预测净资产收益率最大值 | Year、DATE、PERIOD |
| `s_west_maxsales` | 预测主营业务收入最大值 | Year、DATE、PERIOD |
| `s_west_maxsales1` | 预测营业收入最大值 |  |
| `s_west_mediagm` | 预测销售毛利率(GM)中值(可选类型) |  |
| `s_west_medianbps` | 预测每股净资产中值 | Year、DATE、PERIOD |
| `s_west_medianbps1` | 预测每股净资产(BPS)中值 |  |
| `s_west_mediancps` | 预测每股现金流中值 | Year、DATE、PERIOD |
| `s_west_mediancps1` | 预测每股现金流(CPS)中值 |  |
| `s_west_mediandps` | 预测每股股利中值 | Year、DATE、PERIOD |
| `s_west_mediandps1` | 预测每股股利(DPS)中值 |  |
| `s_west_medianebit` | 预测息税前利润中值 | Year、DATE、PERIOD |
| `s_west_medianebit1` | 预测息税前利润(EBIT)中值 |  |
| `s_west_medianebitda` | 预测息税折旧摊销前利润中值 | Year、DATE、Perild |
| `s_west_medianebitda1` | 预测息税折旧摊销前利润(EBITDA)中值 |  |
| `s_west_medianebt` | 预测利润总额中值 | Year、DATE、PERIOD |
| `s_west_medianebt1` | 预测利润总额中值 |  |
| `s_west_medianeps` | 预测每股收益中值 | Year、DATE、PERIOD |
| `s_west_medianeps1` | 预测每股收益中值 |  |
| `s_west_mediannetprofit` | 预测净利润中值 | Year、DATE、PERIOD |
| `s_west_mediannetprofit1` | 预测净利润中值 |  |
| `s_west_medianoperatingprofit` | 预测营业利润中值 | Year、DATE、PERIOD |
| `s_west_medianoperatingprofit1` | 预测营业利润中值 |  |
| `s_west_medianroa` | 预测总资产收益率中值 | Year、DATE、PERIOD |
| `s_west_medianroe` | 预测净资产收益率中值 | Year、DATE、PERIOD |
| `s_west_mediansales` | 预测主营业务收入中值 | Year、DATE、PERIOD |
| `s_west_mediansales1` | 预测营业收入中值 |  |
| `s_west_mediaoc` | 预测营业成本中值 | TRADEDATE、Year |
| `s_west_mediaoc1` | 预测营业成本中值 | TRADEDATE、Year |
| `s_west_mediaopm` | 预测营业利润率(OPM)中值(可选类型) |  |
| `s_west_minbps` | 预测每股净资产最小值 | Year、DATE、PERIOD |
| `s_west_minbps1` | 预测每股净资产(BPS)最小值 |  |
| `s_west_mincps` | 预测每股现金流最小值 | Year、DATE、PERIOD |
| `s_west_mincps1` | 预测每股现金流(CPS)最小值 |  |
| `s_west_mindps` | 预测每股股利最小值 | Year、DATE、PERIOD |
| `s_west_mindps1` | 预测每股股利(DPS)最小值 |  |
| `s_west_minebit` | 预测息税前利润最小值 | Year、DATE、PERIOD |
| `s_west_minebit1` | 预测息税前利润(EBIT)最小值 |  |
| `s_west_minebitda` | 预测息税折旧摊销前利润最小值 | Year、DATE、PERIOD |
| `s_west_minebitda1` | 预测息税折旧摊销前利润(EBITDA)最小值 |  |
| `s_west_minebt` | 预测利润总额最小值 | Year、DATE、PERIOD |
| `s_west_minebt1` | 预测利润总额最小值 |  |
| `s_west_mineps` | 预测每股收益最小值 | Year、DATE、PERIOD |
| `s_west_mineps1` | 预测每股收益最小值 |  |
| `s_west_mingm` | 预测销售毛利率(GM)最小值(可选类型) |  |
| `s_west_minnetprofit` | 预测净利润最小值 | Year、DATE、PERIOD |
| `s_west_minnetprofit1` | 预测净利润最小值 |  |
| `s_west_minoc` | 预测营业成本最小值 | TRADEDATE、Year |
| `s_west_minoc1` | 预测营业成本最小值 | TRADEDATE、Year |
| `s_west_minoperatingprofit` | 预测营业利润最小值 | Year、DATE、PERIOD |
| `s_west_minoperatingprofit1` | 预测营业利润最小值 |  |
| `s_west_minopm` | 预测营业利润率(OPM)最小值(可选类型) |  |
| `s_west_minroa` | 预测总资产收益率最小值 | Year、DATE、PERIOD |
| `s_west_minroe` | 预测净资产收益率最小值 | Year、DATE、PERIOD |
| `s_west_minsales` | 预测主营业务收入最小值 | Year、DATE、PERIOD |
| `s_west_minsales1` | 预测营业收入最小值 |  |
| `s_west_netprofit` | 预测净利润平均值 | Year、DATE、PERIOD |
| `s_west_netprofit1` | 预测净利润平均值 |  |
| `s_west_netprofit_cagr` | 一致预测净利润2年复合增长率 | TRADEDATE |
| `s_west_netprofit_downgrade` | 一月内净利润调低家数 | Year、DATE、PERIOD |
| `s_west_netprofit_ftm` | 一致预测净利润(未来12个月) | TRADEDATE |
| `s_west_netprofit_fy1` | 一致预测净利润(FY1) | TRADEDATE |
| `s_west_netprofit_fy2` | 一致预测净利润(FY2) | TRADEDATE |
| `s_west_netprofit_fy3` | 一致预测净利润(FY3) | TRADEDATE |
| `s_west_netprofit_maintain` | 一月内净利润维持家数 | Year、DATE、PERIOD |
| `s_west_netprofit_surprise` | 预测净利润Surprise |  |
| `s_west_netprofit_surprise_pct` | 预测净利润Surprise百分比 |  |
| `s_west_netprofit_upgrade` | 一月内净利润调高家数 | Year、DATE、PERIOD |
| `s_west_netprofit_yoy` | 一致预测净利润同比 | TRADEDATE |
| `s_west_nproc_13w` | 一致预测净利润13周变化率 | TRADEDATE、Year |
| `s_west_nproc_1w` | 一致预测净利润1周变化率 | Year、TRADEDATE |
| `s_west_nproc_26w` | 一致预测净利润26周变化率 | TRADEDATE、Year |
| `s_west_nproc_4w` | 一致预测净利润4周变化率 | Year、TRADEDATE |
| `s_west_pe` | 预测PE(可选类型) | Year、DATE |
| `s_west_peg` | 预测PEG(可选类型) | Year、DATE |
| `s_west_sales` | 预测主营业务收入平均值 | Year、DATE、PERIOD |
| `s_west_sales1` | 预测营业收入平均值 |  |
| `s_west_sales_cagr` | 一致预测营业收入2年复合增长率 | TRADEDATE |
| `s_west_sales_downgrade` | 一月内主营业务收入调低家数 | Year、DATE、PERIOD |
| `s_west_sales_ftm` | 一致预测营业收入(未来12个月) | TRADEDATE |
| `s_west_sales_fy1` | 一致预测营业收入(FY1) | TRADEDATE |
| `s_west_sales_fy2` | 一致预测营业收入(FY2) | TRADEDATE |
| `s_west_sales_fy3` | 一致预测营业收入(FY3) | TRADEDATE |
| `s_west_sales_maintain` | 一月内主营业务收入维持家数 | Year、DATE、PERIOD |
| `s_west_sales_surprise` | 预测营业收入Surprise |  |
| `s_west_sales_surprise_pct` | 预测营业收入Surprise百分比 |  |
| `s_west_sales_upgrade` | 一月内主营业务收入调高家数 | Year、DATE、PERIOD |
| `s_west_sales_yoy` | 一致预测营业收入同比 | TRADEDATE |
| `s_west_stdbps` | 预测每股净资产标准差 | Year、DATE、PERIOD |
| `s_west_stdbps1` | 预测每股净资产(BPS)标准差 |  |
| `s_west_stdcps` | 预测每股现金流标准差 | Year、DATE、PERIOD |
| `s_west_stdcps1` | 预测每股现金流(CPS)标准差 |  |
| `s_west_stddps` | 预测每股股利标准差 | Year、DATE、PERIOD |
| `s_west_stddps1` | 预测每股股利(DPS)标准差 |  |
| `s_west_stdebit` | 预测息税前利润标准差 | Year、DATE、PERIOD |
| `s_west_stdebit1` | 预测息税前利润(EBIT)标准差 |  |
| `s_west_stdebitda` | 预测息税折旧摊销前利润标准差 | Year、DATE、PERIOD |
| `s_west_stdebitda1` | 预测息税折旧摊销前利润(EBITDA)标准差 |  |
| `s_west_stdebt` | 预测利润总额标准差 | Year、DATE、PERIOD |
| `s_west_stdebt1` | 预测利润总额标准差 |  |
| `s_west_stdeps` | 预测每股收益标准差 | Year、DATE、PERIOD |
| `s_west_stdeps1` | 预测每股收益标准差 |  |
| `s_west_stdgm` | 预测销售毛利率(GM)标准差值(可选类型) |  |
| `s_west_stdnetprofit` | 预测净利润标准差 | Year、DATE、PERIOD |
| `s_west_stdnetprofit1` | 预测净利润标准差 |  |
| `s_west_stdoperatingprofit` | 预测营业利润标准差 | Year、DATE、PERIOD |
| `s_west_stdoperatingprofit1` | 预测营业利润标准差 |  |
| `s_west_stdopm` | 预测营业利润率(OPM)标准差值(可选类型) |  |
| `s_west_stdroa` | 预测总资产收益率标准差 | Year、DATE、PERIOD |
| `s_west_stdroe` | 预测净资产收益率标准差 | Year、DATE、PERIOD |
| `s_west_stdsales` | 预测主营业务收入标准差 | Year、DATE、PERIOD |
| `s_west_stdsales1` | 预测营业收入标准差 |  |
| `s_west_stoc` | 预测营业成本标准差 | TRADEDATE、Year |
| `s_west_stoc1` | 预测营业成本标准差 | TRADEDATE、Year |
| `s_west_yoynetprofit` | 预测净利润增长率 | Year、DATE、PERIOD |
| `s_west_yoysales` | 预测主营业务收入增长率 | Year、DATE、PERIOD |
| `s_wq_amount` | 周成交额(新增) |  |
| `s_wq_avgamount` | 周日均成交额 |  |
| `s_wq_avgaoi` | 周日均持仓量 |  |
| `s_wq_avgprice` | 周均价(新增) |  |
| `s_wq_avgturn` | 周平均换手率(新增) |  |
| `s_wq_avgvolume` | 周日均成交量 |  |
| `s_wq_change` | 周涨跌(新增) |  |
| `s_wq_change_settlement` | 周涨跌（结算价） |  |
| `s_wq_close` | 周收盘价(新增) |  |
| `s_wq_freeavgturnover` | 周平均换手率（基准.自由流通股本）(新增) |  |
| `s_wq_freeturnover` | 周换手率（基准.自由流通股本）(新增) |  |
| `s_wq_high` | 周最高价(新增) |  |
| `s_wq_high_date` | 周最高价日(新增) |  |
| `s_wq_highclose` | 周最高收盘价(新增) |  |
| `s_wq_highclose_date` | 周最高收盘价日(新增) |  |
| `s_wq_highsettle` | 周最高结算价 |  |
| `s_wq_highswing_date` | 周最高结算价日 |  |
| `s_wq_low` | 周最低价(新增) |  |
| `s_wq_low_date` | 周最低价日(新增) |  |
| `s_wq_lowclose` | 周最低收盘价(新增) |  |
| `s_wq_lowclose_date` | 周最低收盘价日(新增) |  |
| `s_wq_lowsettle` | 周最低结算价 |  |
| `s_wq_lowswing_date` | 周最低结算价日 |  |
| `s_wq_oi` | 周持仓量 |  |
| `s_wq_oichange` | 周持仓变化 |  |
| `s_wq_open` | 周开盘价(新增) |  |
| `s_wq_pctchange` | 周涨跌幅(新增) |  |
| `s_wq_pctchange_settlement` | 周涨跌幅（结算价） |  |
| `s_wq_preclose` | 周前收盘价(新增) |  |
| `s_wq_presettle` | 周前结算价 |  |
| `s_wq_settle` | 周结算价 |  |
| `s_wq_swing` | 周振幅(新增) |  |
| `s_wq_turn` | 周换手率(新增) |  |
| `s_wq_volume` | 周成交量(新增) |  |
| `s_wrating_avg` | 综合评级(数值) | DATE、PERIOD |
| `s_wrating_avgchn` | 综合评级(中文) | DATE、PERIOD |
| `s_wrating_avgeng` | 综合评级(英文) | DATE、PERIOD |
| `s_wrating_downgrade` | 一月内评级调低家数 | DATE、PERIOD |
| `s_wrating_instnum` | 评级机构家数 | DATE |
| `s_wrating_maintain` | 一月内评级维持家数 | DATE、PERIOD |
| `s_wrating_numofbuy` | 评级买入家数 | DATE |
| `s_wrating_numofhold` | 评级中性家数 | DATE |
| `s_wrating_numofoutperform` | 评级增持家数 | DATE |
| `s_wrating_numofsell` | 评级卖出家数 | DATE |
| `s_wrating_numofunderperform` | 评级减持家数 | DATE |
| `s_wrating_targetprice` | 一致预测目标价 | TRADEDATE |
| `s_wrating_upgrade` | 一月内评级调高家数 | DATE、PERIOD |
| `s_xq_accmcomments` | 累计讨论次数_雪球 | TRADEDATE |
| `s_xq_accmfocus` | 累计关注人数_雪球 | TRADEDATE |
| `s_xq_accmshares` | 累计交易分享数_雪球 | TRADEDATE |
| `s_xq_commentsadded` | 一周新增讨论数_雪球 | TRADEDATE |
| `s_xq_focusadded` | 一周新增关注_雪球 | TRADEDATE |
| `s_xq_sharesadded` | 一周新增交易分享数_雪球 | TRADEDATE |
| `s_xq_wow_comments` | 一周讨论增长率_雪球 | TRADEDATE |
| `s_xq_wow_focus` | 一周关注增长率_雪球 | TRADEDATE |
| `s_xq_wow_shares` | 一周交易分享增长率_雪球 | TRADEDATE |
| `s_yoy_asset` | 总资产同比增长率 | REPORTDATE |
| `s_yoy_debt` | 总负债同比增长率 | REPORTDATE |
| `s_yoy_ebt` | 利润总额同比增长率 | REPORTDATE |
| `s_yoy_ebt_qty` | 单季度.税前利润同比增长率 | REPORTDATE |
| `s_yoy_equity` | 净资产同比增长率 | REPORTDATE |
| `s_yoy_mainprofit` | 主营利润同比增长率 | REPORTDATE |
| `s_yoy_mainprofit_qty` | 单季度.主营业务利润同比增长率 | REPORTDATE |
| `s_yoy_netprofit` | 净利润同比增长率 | REPORTDATE |
| `s_yoy_netprofit_qty` | 单季度.净利润同比增长率 | REPORTDATE |
| `s_yoy_operatingprofit` | 营业利润同比增长率 | REPORTDATE |
| `s_yoy_sales` | 主营收入同比增长率 | REPORTDATE |
| `s_yoy_sales_qty` | 单季度.主营业务收入同比增长率 | REPORTDATE |
| `s_yq_amount` | 年成交额(新增) |  |
| `s_yq_avgamount` | 年日均成交额 |  |
| `s_yq_avgaoi` | 年日均持仓量 |  |
| `s_yq_avgprice` | 年均价(新增) |  |
| `s_yq_avgturn` | 年平均换手率(新增) |  |
| `s_yq_avgvolume` | 年日均成交量 |  |
| `s_yq_change` | 年涨跌(新增) |  |
| `s_yq_change_settlement` | 年涨跌（结算价） |  |
| `s_yq_close` | 年收盘价(新增) |  |
| `s_yq_freeavgturnover` | 年平均换手率（基准.自由流通股本）(新增) |  |
| `s_yq_freeturnover` | 年换手率（基准.自由流通股本）(新增) |  |
| `s_yq_high` | 年最高价(新增) |  |
| `s_yq_high_date` | 年最高价日(新增) |  |
| `s_yq_highclose` | 年最高收盘价(新增) |  |
| `s_yq_highclose_date` | 年最高收盘价日(新增) |  |
| `s_yq_highsettle` | 年最高结算价 |  |
| `s_yq_highswing_date` | 年最高结算价日 |  |
| `s_yq_low` | 年最低价(新增) |  |
| `s_yq_low_date` | 年最低价日(新增) |  |
| `s_yq_lowclose` | 年最低收盘价(新增) |  |
| `s_yq_lowclose_date` | 年最低收盘价日(新增) |  |
| `s_yq_lowsettle` | 年最低结算价 |  |
| `s_yq_lowswing_date` | 年最低结算价日 |  |
| `s_yq_oi` | 年持仓量 |  |
| `s_yq_oichange` | 年持仓变化 |  |
| `s_yq_open` | 年开盘价(新增) |  |
| `s_yq_pctchange` | 年涨跌幅(新增) |  |
| `s_yq_pctchange_settlement` | 年涨跌幅（结算价） |  |
| `s_yq_preclose` | 年前收盘价(新增) |  |
| `s_yq_presettle` | 年前结算价 |  |
| `s_yq_settle` | 年结算价 |  |
| `s_yq_swing` | 年振幅(新增) |  |
| `s_yq_turn` | 年换手率(新增) |  |
| `s_yq_volume` | 年成交量(新增) |  |
| `s_ytd_pctchange` | 年初至今涨跌幅 | TRADEDATE |

<a id="分类-基金"></a>

## 基金（1798 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `f_absinv_interest` | 资产支持证券投资收益-利息收入 | REPORTDATE |
| `f_absinv_redemptionspread` | 资产支持证券投资收益-赎回差价收入 | REPORTDATE |
| `f_absinv_subscriptionspread` | 资产支持证券投资收益-申购差价收入 | REPORTDATE |
| `f_absinv_tradespread` | 资产支持证券投资收益-买卖资产支持证券差价收入 | REPORTDATE |
| `f_absolute_avgincome` | 平均收益 | BEGINDATE、EndDate |
| `f_absolute_avgloss` | 平均损失 | BEGINDATE、EndDate |
| `f_absolute_avgmonthlyreturn` | 平均月度回报 | StartDate、EndDate |
| `f_absolute_condownsmonth` | 连跌月数 | BEGINDATE、EndDate |
| `f_absolute_conupsmonth` | 连涨月数 | BEGINDATE、EndDate |
| `f_absolute_highestmonthlyreturn` | 最高单月回报 | BEGINDATE、EndDate |
| `f_absolute_highestquatreturn` | 最高季度回报 | StartDate、EndDate |
| `f_absolute_highestreturnofconmonth` | 最高连续N月回报 | BEGINDATE、EndDate |
| `f_absolute_longestcondownmonth` | 最长连续下跌月数 | BEGINDATE、EndDate |
| `f_absolute_longestconupmonth` | 最长连续上涨月数 | BEGINDATE、EndDate |
| `f_absolute_lowestmonthlyreturn` | 最低单月回报 | BEGINDATE、EndDate |
| `f_absolute_lowestquatreturn` | 最低季度回报 | StartDate、EndDate |
| `f_absolute_lowestreturnofconmonth` | 最差连续N月回报 | BEGINDATE、EndDate |
| `f_absolute_maxfallofdownmonth` | 最长连续下跌整月跌幅 | BEGINDATE、EndDate |
| `f_absolute_maxincreaseofupmonth` | 最长连续上涨整月涨幅 | BEGINDATE、EndDate |
| `f_absolute_monthlycompositereturn` | 月度复合回报 | BEGINDATE、EndDate |
| `f_absolute_profitmonthper` | 上涨月份占比 | BEGINDATE、EndDate |
| `f_absolute_profitper` | 区间盈利百分比 | StartDate、EndDate、CalcTerm |
| `f_absolute_siml_avglowestmonthlyreturn` | 最低单月回报同类平均 | StartDate、EndDate |
| `f_absolute_updownmonthratio` | 上涨/下跌月数比 | BEGINDATE、EndDate |
| `f_allstock_pb` | 全部持股平均市净率 | REPORTDATE |
| `f_allstock_pe` | 全部持股平均市盈率 | REPORTDATE |
| `f_anal_avgnavreturn` | 基金加权平均净值利润率(新增) | REPORTDATE |
| `f_anal_avgnetincomeperunit` | 报告期加权平均份额利润(新增) | REPORTDATE |
| `f_anal_disratiodevi` | 折溢价比率偏离系数 |  |
| `f_anal_distributable` | 期末可供分配基金收益 | REPORTDATE |
| `f_anal_distributableperunit` | 期末可供分配基金份额收益 | REPORTDATE |
| `f_anal_downdiscount_pctchange` | 下折母基金需跌 | TRADEDATE |
| `f_anal_downdiscount_threshold` | 下折阈值 |  |
| `f_anal_impliedyield` | 隐含收益率 | TRADEDATE |
| `f_anal_income` | 报告期利润(新增) | REPORTDATE |
| `f_anal_nav` | 期末基金份额净值 | REPORTDATE |
| `f_anal_navlever` | 净值杠杆 |  |
| `f_anal_netasset` | 期末基金资产净值 | REPORTDATE |
| `f_anal_netincome` | 报告期基金净收益 | REPORTDATE |
| `f_anal_nextaayield` | 下期约定年收益率 |  |
| `f_anal_nextdiscountdate` | 下一定期折算日 |  |
| `f_anal_pricelever` | 价格杠杆 |  |
| `f_anal_reits_actdist` | 实际分配金额(本期) | REPORTDATE |
| `f_anal_reits_cashdist` | 现金分派率 | Year |
| `f_anal_reits_cashflowbalance` | 经营活动现金流量余额 | REPORTDATE |
| `f_anal_reits_depreciationandamortization` | 折旧和摊销 | REPORTDATE |
| `f_anal_reits_distributedamounts` | 可供分配金额(本期) | REPORTDATE |
| `f_anal_reits_ebit` | 税息折旧及摊销前利润 | REPORTDATE |
| `f_anal_reits_fairvalue` | 期末基金份额公允价值参考净值 | Year |
| `f_anal_reits_income` | 本期收入 | REPORTDATE |
| `f_anal_reits_interestcost` | 利息支出 | REPORTDATE |
| `f_anal_reits_irr` | 内部收益率 | Year |
| `f_anal_reits_netprofit` | 本期净利润 | REPORTDATE |
| `f_anal_reits_operatingcost` | 营业成本 | REPORTDATE |
| `f_anal_reits_operatingrevenue` | 营业收入 | REPORTDATE |
| `f_anal_reits_taxcost` | 所得税费用 | REPORTDATE |
| `f_anal_reits_unitactdist` | 单位实际分配金额(本期) | REPORTDATE |
| `f_anal_reits_unitdistributedamounts` | 单位可供分配金额(本期) | REPORTDATE |
| `f_anal_smfbfactualcost` | 实际资金成本 |  |
| `f_anal_smfbnamedcost` | 名义资金成本 |  |
| `f_anal_smfearning` | 分级基金收益分配方式 |  |
| `f_anal_tdiscountratio` | 整体折溢价率 |  |
| `f_anal_updiscount_pctchange` | 上折母基金需涨 | TRADEDATE |
| `f_anal_updiscount_threshold` | 上折阈值 |  |
| `f_bndinv_accrintamount` | 买卖债券差价收入-应计利息总额 | REPORTDATE |
| `f_bndinv_bndamount` | 买卖债券差价收入-卖出债券(债转股及债券到期兑付)成交总额 | REPORTDATE |
| `f_bndinv_bndcost` | 买卖债券差价收入-卖出债券(债转股及债券到期兑付)成本总额 | REPORTDATE |
| `f_bndinv_interest` | 债券投资收益-利息收入 | REPORTDATE |
| `f_bndinv_redeemspread` | 债券投资收益-赎回差价收入 | REPORTDATE |
| `f_bndinv_spread` | 买卖债券差价收入-买卖债券差价收入 | REPORTDATE |
| `f_bndinv_subscribespread` | 债券投资收益-申购差价收入 | REPORTDATE |
| `f_bndinv_tradespread` | 债券投资收益-买卖债券差价收入 | REPORTDATE |
| `f_bndinv_transcost` | 买卖债券差价收入-交易费用 | REPORTDATE |
| `f_chapter5_digital_industries` | 是否数字产业化主题基金 | REPORTDATE |
| `f_chapter5_finance_digital` | 是否数字金融领域基金 | REPORTDATE |
| `f_chapter5_finance_green` | 是否绿色金融领域基金 | REPORTDATE |
| `f_chapter5_finance_inclusive` | 是否普惠金融领域基金 | REPORTDATE |
| `f_chapter5_finance_pension` | 是否养老金融领域基金 | REPORTDATE |
| `f_chapter5_finance_tech` | 是否科技金融领域基金 | REPORTDATE |
| `f_chapter5_industries_digital` | 是否产业数字化主题基金 | REPORTDATE |
| `f_chapter5_products_agriculture` | 是否三农领域主题基金 | REPORTDATE |
| `f_chapter5_products_consumer` | 是否民生消费主题基金 | REPORTDATE |
| `f_chapter5_products_enterprise` | 是否民营企业主题基金 | REPORTDATE |
| `f_chapter5_products_esg` | 是否ESG主题基金 | REPORTDATE |
| `f_chapter5_products_sme` | 是否中小微企业主题基金 | REPORTDATE |
| `f_commission_detailed` | 交易佣金(明细值) | REPORTDATE |
| `f_commission_total` | 交易佣金(合计值) | REPORTDATE |
| `f_customizedfundornot` | 是否定制基金 |  |
| `f_div_accumulatedpayout` | 累计分红总额 |  |
| `f_div_accumulatedperunit` | 单位累计分红 |  |
| `f_div_accumulatedtimes` | 累计分红次数 |  |
| `f_div_clause` | 分红条款 |  |
| `f_div_exdivdate` | 最新分红日期 | DEALDATE |
| `f_div_payout` | 年度分红总额 | RPTYEAR |
| `f_div_periodpayout` | 区间分红总额 |  |
| `f_div_periodperunit` | 单位区间分红 |  |
| `f_div_periodtimes` | 区间分红次数 |  |
| `f_div_perunit` | 单位年度分红 | RPTYEAR |
| `f_div_profitdistall` | 年度利润分配合计 | Year |
| `f_div_profitdistcash` | 年度现金形式发放总额 | Year |
| `f_div_profitdistre` | 年度再投资形式发放总额 | Year |
| `f_div_times` | 年度分红次数 | RPTYEAR |
| `f_down_mkt_capture` | 下行捕获率 | StartDate、EndDate、CalcTerm、Underlying_Index |
| `f_dq_amount` | 成交额 |  |
| `f_dq_avgprice` | 成交均价 |  |
| `f_dq_change` | 涨跌 |  |
| `f_dq_close` | 收盘价 |  |
| `f_dq_discount` | 贴水 |  |
| `f_dq_discountratio` | 贴水率 |  |
| `f_dq_dquantity` | 交收量(黄金现货) | TRADEDATE |
| `f_dq_high` | 最高价 |  |
| `f_dq_low` | 最低价 |  |
| `f_dq_open` | 开盘价 |  |
| `f_dq_pctchange` | 涨跌幅 |  |
| `f_dq_preclose` | 前收盘价 |  |
| `f_dq_status` | 申购赎回状态(新增) | D |
| `f_dq_swing` | 振幅(新增) |  |
| `f_dq_turn` | 换手率 |  |
| `f_dq_volume` | 成交量 |  |
| `f_eft_invsttype` | ETF投资范围分类 | FundGroup |
| `f_esg_cfootprint_wind` | 基金碳足迹 | REPORTDATE |
| `f_esg_cfrating_wind` | 基金碳足迹评级 | REPORTDATE |
| `f_esg_escore_wind` | 基金环境维度得分 | REPORTDATE |
| `f_esg_eventscore_wind` | 基金ESG争议事件得分 | REPORTDATE |
| `f_esg_gscore_wind` | 基金治理维度得分 | REPORTDATE |
| `f_esg_mgmtscore_wind` | 基金ESG管理实践得分 | REPORTDATE |
| `f_esg_rating_wind` | 基金Wind ESG评级 | REPORTDATE |
| `f_esg_score_wind` | 基金Wind ESG综合得分 | REPORTDATE |
| `f_esg_sscore_wind` | 基金社会维度得分 | REPORTDATE |
| `f_esg_tcemission_wind` | 基金碳排放总量 | REPORTDATE |
| `f_etf_netasset` | ETF资产净值 | TRADEDATE |
| `f_fairvaluechangesincome_forwards` | 远期投资公允价值变动收益 | REPORTDATE |
| `f_fairvaluechangesincome_futures` | 期货投资公允价值变动收益 | REPORTDATE |
| `f_fairvaluechangesincome_preciousmetal` | 贵金属投资公允价值变动收益 | REPORTDATE |
| `f_fund_leveragemultiple` | 基金的杠杆倍数 |  |
| `f_fundinv_totalamout` | 基金投资收益-卖出/赎回基金成交总额 | REPORTDATE |
| `f_fundinv_totalcost` | 基金投资收益-卖出/赎回基金成本总额 | REPORTDATE |
| `f_fundinv_transcost` | 基金投资收益-交易费用 | REPORTDATE |
| `f_fundinv_vat` | 基金投资收益-买卖基金差价收入应缴纳增值税额 | REPORTDATE |
| `f_fundscale_latestdate` | 基金规模最新日期 |  |
| `f_highestaccumnav_date` | 区间最高累计单位净值日 | StartDate、EndDate |
| `f_highestadjnav_date` | 区间最高复权单位净值日 | StartDate、EndDate |
| `f_highestnav_date` | 区间最高单位净值日 | StartDate、EndDate |
| `f_holder_avgholding` | 平均每户持有基金份额 | REPORTDATE |
| `f_holder_begbalindinv` | 单一投资者报告期初持有份额 | REPORTDATE、Year、InvestorType、Number |
| `f_holder_corp_holding` | 基金管理公司持有份额 | REPORTDATE |
| `f_holder_corp_holdingpct` | 基金管理公司持有比例 | REPORTDATE |
| `f_holder_director_holding` | 董事合计持有份额(新增) | REPORTDATE |
| `f_holder_director_holdingpct` | 董事合计持有比例(新增) | REPORTDATE |
| `f_holder_fcmpshngs` | 基金管理人从业人员持有份额总量的数量区间 | REPORTDATE、PERSONNEL_TYPE |
| `f_holder_feeder_holding` | ETF联接基金持有份额 | REPORTDATE |
| `f_holder_feeder_holdingpct` | ETF联接基金持有比例 | REPORTDATE |
| `f_holder_fundmanager_holding` | 基金经理持有份额(新增) | REPORTDATE |
| `f_holder_fundmanager_holdingpct` | 基金经理持有比例(新增) | REPORTDATE |
| `f_holder_holding` | 第N名持有人持有份额(封闭式) | REPORTDATE |
| `f_holder_holdinglisting` | 第N名持有人持有份额(上市公告) | TopN |
| `f_holder_holdingmmf` | 第N名持有人持有份额(货币) | REPORTDATE |
| `f_holder_insthld2` | 机构投资者持有份额(上市交易公告书) |  |
| `f_holder_insthldpct2` | 机构投资者持有比例(上市交易公告书) |  |
| `f_holder_institution_holding` | 机构投资者持有份额 | REPORTDATE |
| `f_holder_institution_holding2` | 机构投资者持有份额(排除ETF联接) | REPORTDATE |
| `f_holder_institution_holdingpct` | 机构投资者持有比例 | REPORTDATE |
| `f_holder_institution_holdingpct2` | 机构投资者持有比例(排除ETF联接) | REPORTDATE |
| `f_holder_institution_totalholding` | 机构投资者持有份额(合计) | REPORTDATE |
| `f_holder_institution_totalholding2` | 机构投资者持有份额(合计,排除ETF联接) | REPORTDATE |
| `f_holder_institution_totalholdingpct` | 机构投资者持有比例(合计) | REPORTDATE |
| `f_holder_institution_totalholdingpct2` | 机构投资者持有比例(合计,排除ETF联接) | REPORTDATE |
| `f_holder_mergedholdingornot` | 持有份额是否为合并数据 | REPORTDATE |
| `f_holder_mergednumberornot` | 持有人户数是否为合并数据 | REPORTDATE |
| `f_holder_mngemp_holding` | 管理人员工持有份额(新增) | REPORTDATE |
| `f_holder_mngemp_holdingpct` | 管理人员工持有比例(新增) | REPORTDATE |
| `f_holder_mngemp_totalholding` | 管理人员工持有份额(合计) | REPORTDATE |
| `f_holder_mngemp_totalholdingpct` | 管理人员工持有比例(合计) | REPORTDATE |
| `f_holder_name` | 第N名持有人名称(封闭式) | REPORTDATE |
| `f_holder_namelisting` | 第N名持有人名称(上市公告) | TopN |
| `f_holder_namemmf` | 第N名持有人类别(货币) | REPORTDATE |
| `f_holder_number` | 基金份额持有人户数 | REPORTDATE |
| `f_holder_pct` | 第N名持有人持有比例(封闭式) | REPORTDATE |
| `f_holder_pctlisting` | 第N名持有人持有比例(上市公告) | TopN |
| `f_holder_pctmmf` | 第N名持有人持有比例(货币) | REPORTDATE |
| `f_holder_pershld2` | 个人投资者持有份额(上市交易公告书) |  |
| `f_holder_pershldpct2` | 个人投资者持有比例(上市交易公告书) |  |
| `f_holder_personal_holding` | 个人投资者持有份额 | REPORTDATE |
| `f_holder_personal_holdingpct` | 个人投资者持有比例 | REPORTDATE |
| `f_holder_personal_totalholding` | 个人投资者持有份额(合计) | REPORTDATE |
| `f_holder_personal_totalholdingpct` | 个人投资者持有比例(合计) | REPORTDATE |
| `f_holder_redmrptper` | 单一投资者报告期内赎回持有份额 | REPORTDATE、Year、InvestorType、Number |
| `f_holder_single_holding` | 单一投资者报告期末持有份额 | REPORTDATE |
| `f_holder_single_holdingpct` | 单一投资者报告期末持有比例 | REPORTDATE |
| `f_holder_single_totalholding` | 单一投资者报告期末持有份额合计 | REPORTDATETYPE、Year |
| `f_holder_single_totalholdingpct` | 单一投资者报告期末持有比例合计 | REPORTDATETYPE、Year |
| `f_holder_subrptper` | 单一投资者报告期内申购持有份额 | REPORTDATE、Year、InvestorType、Number |
| `f_holder_top10_holding` | 前十大持有人持有比例合计(封闭式) | REPORTDATE |
| `f_holder_top10_holdingmmf` | 前十大持有人持有份额合计(货币) | REPORTDATE |
| `f_holder_top10_pct` | 前十大持有人持有份额合计(封闭式) | REPORTDATE |
| `f_holder_top10_pctmmf` | 前十大持有人持有比例合计(货币) | REPORTDATE |
| `f_holder_totalnumber` | 基金份额持有人户数(合计) | REPORTDATE |
| `f_hq_turn` | 半年换手率 |  |
| `f_info_aayeildinfo` | 约定年收益率表达式 |  |
| `f_info_abnormalnavfluctuation` | 净值异常涨跌幅说明 |  |
| `f_info_actualannualyield` | 实际年化收益率 |  |
| `f_info_actualduration` | 实际运作期限 |  |
| `f_info_actualmaturitydate` | 实际到期日 |  |
| `f_info_actualscale` | 实际发行规模 |  |
| `f_info_agreedannuyield` | 约定年收益率 |  |
| `f_info_amaccode` | 基金业协会编码 |  |
| `f_info_applim` | 基金认购限额说明 | TRADEDATE |
| `f_info_approveddate` | 基金获批注册日期 |  |
| `f_info_attorney` | 基金经办律师 |  |
| `f_info_auditor` | 基金经办会计师 |  |
| `f_info_averageworkingyears` | 基金经理平均年限 |  |
| `f_info_avgfundscale` | 同类基金平均规模 |  |
| `f_info_backendcode` | 基金后端代码 |  |
| `f_info_benchindexcode` | 基准指数代码 |  |
| `f_info_benchmark` | 业绩比较基准 |  |
| `f_info_businessmode` | 业务模式 |  |
| `f_info_bwmp_recordcode` | 理财产品登记编码 |  |
| `f_info_capverifins` | 基金验资机构 |  |
| `f_info_changeofbenchmark` | 业绩比较基准变更说明 |  |
| `f_info_closedayillus` | 封闭期说明 |  |
| `f_info_cndpretermination` | 提前终止条件 |  |
| `f_info_cndpurchredemption` | 申购赎回条件 |  |
| `f_info_code` | 交易代码 |  |
| `f_info_companyindex_weight_alpha` | Alpha(基金公司指数) | StartDate、EndDate |
| `f_info_companyindex_weight_beta` | Beta(基金公司指数) | StartDate、EndDate |
| `f_info_companyindex_weight_maxdownside` | 基金公司指数最大回撤 | StartDate、EndDate |
| `f_info_companyindex_weight_return` | 基金公司指数区间回报 | StartDate、EndDate |
| `f_info_companyindex_weight_sharpe` | Sharpe(基金公司指数) | StartDate、EndDate |
| `f_info_companyindex_weight_stdev` | 基金公司指数收益标准差 | StartDate、EndDate |
| `f_info_companyindex_weight_stdevyearly` | 基金公司指数年化波动率 | StartDate、EndDate |
| `f_info_companyindex_weight_treynor` | Treynor(基金公司指数) | StartDate、EndDate |
| `f_info_concepttype` | 所属基金概念类别 |  |
| `f_info_corp_averageworkingyears` | 基金经理平均年限 |  |
| `f_info_corp_averageworkingyears_hist` | 基金经理平均年限(支持历史) | TRADEDATE |
| `f_info_corp_fivestarfundsprop` | 五星基金占比 |  |
| `f_info_corp_fourstarfundsprop` | 四星基金占比 |  |
| `f_info_corp_fundmanagementcompany` | 基金管理人简称 |  |
| `f_info_corp_fundmanagermaturity` | 基金经理成熟度 |  |
| `f_info_corp_fundmanagersno` | 基金经理数 |  |
| `f_info_corp_fundno` | 旗下基金数 |  |
| `f_info_corp_maxworkingyears` | 基金经理最大年限 |  |
| `f_info_corp_teamstability` | 团队稳定性 |  |
| `f_info_corpaddress` | 基金管理人注册地址 |  |
| `f_info_corpadmindivision` | 基金管理人注册地所属行政区划 | DIVISION_TYPE、TRADEDATE |
| `f_info_corpchairman` | 基金管理人法人代表 |  |
| `f_info_corpcity` | 基金管理人注册城市 |  |
| `f_info_corpemail` | 基金管理人电子邮箱 |  |
| `f_info_corpestablishmentdate` | 基金管理人成立日期 |  |
| `f_info_corpfax` | 基金管理人传真 |  |
| `f_info_corpmanager` | 基金管理人总经理 |  |
| `f_info_corpname` | 基金管理人中文名称 |  |
| `f_info_corpnameeng` | 基金管理人英文名称 |  |
| `f_info_corpoffice` | 基金管理人办公地址 |  |
| `f_info_corpphone` | 基金管理人电话 |  |
| `f_info_corpregisteredcapital` | 基金管理人注册资本 |  |
| `f_info_corpwebsite` | 基金管理人主页 |  |
| `f_info_corpzip` | 基金管理人邮编 |  |
| `f_info_counselor` | 律师事务所 |  |
| `f_info_csrctype` | 证监会基金分类 |  |
| `f_info_ctrcode` | 信托产品中信登编码 |  |
| `f_info_custenddate` | 托管结束日期(新增) |  |
| `f_info_custodianbank` | 基金托管人 |  |
| `f_info_custodianfeechangedate` | 托管费率变更日期 |  |
| `f_info_custodianfeeratio` | 托管费率 |  |
| `f_info_custodianfeeratio2` | 托管费率(支持历史) | TRADEDATE |
| `f_info_custstartdate` | 开始托管日期(新增) |  |
| `f_info_date_resumption` | 基金恢复运作日 | TRADEDATE |
| `f_info_date_suspension` | 基金暂停运作日 | TRADEDATE |
| `f_info_daystoconversion` | 剩余折算天数(新增) | DEALDATE |
| `f_info_discountmethod` | 定期折算条款 |  |
| `f_info_discountperiod` | 定期折算周期 |  |
| `f_info_distributionarea` | 销售地区 |  |
| `f_info_domesticagent` | 互认基金境内代理人 |  |
| `f_info_downdiscount` | 向下触点折算条款 |  |
| `f_info_earlyterminationornot` | 是否可提前终止 |  |
| `f_info_effsubscrholederno` | 有效认购户数 |  |
| `f_info_etf_feedercode` | ETF关联联接基金代码 |  |
| `f_info_etfdealshareonmarket` | 上市交易份额 |  |
| `f_info_etffeeder` | 是否ETF联接基金 |  |
| `f_info_etflisteddate` | 上市日期 |  |
| `f_info_etfornot` | 是否ETF基金 |  |
| `f_info_etfpr_cashbalance` | ETF申购赎回现金差额 | TRADEDATE |
| `f_info_etfpr_cashratio` | ETF申购赎回现金替代比例上限(%) | TRADEDATE |
| `f_info_etfpr_estcash` | ETF申购赎回预估现金部分 | TRADEDATE |
| `f_info_etfpr_maxnetpurchase` | ETF申购赎回清单当天净申购上限 | TRADEDATE |
| `f_info_etfpr_maxnetpurchasepersecurityaccount` | ETF申购赎回清单单个证券账户净申购上限 | TRADEDATE |
| `f_info_etfpr_maxnetredemption` | ETF申购赎回清单当天净赎回上限 | TRADEDATE |
| `f_info_etfpr_maxnetredemptionpersecurityaccount` | ETF申购赎回清单单个证券账户净赎回上限 | TRADEDATE |
| `f_info_etfpr_maxpurchase` | ETF申购赎回净申购上限 | TRADEDATE |
| `f_info_etfpr_maxpurchasepersecurityaccount` | ETF申购赎回清单单个证券账户累计可申购上限 | TRADEDATE |
| `f_info_etfpr_maxredemptionpersecurityaccount` | ETF申购赎回清单单个证券账户累计可赎回上限 | TRADEDATE |
| `f_info_etfpr_minnav` | ETF申购赎回最小申购赎回单位 | TRADEDATE |
| `f_info_etfpr_minnav_unit` | ETF申购赎回最小申购赎回单位资产净值 | TRADEDATE |
| `f_info_etfpr_minredemption` | ETF申购赎回净赎回上限 | TRADEDATE |
| `f_info_etfredcommrate` | ETF赎回佣金费率 | TRADEDATE |
| `f_info_etfrtgs` | 是否实时逐笔全额结算(RTGS) |  |
| `f_info_etfsubcommrate` | ETF申购佣金费率 | TRADEDATE |
| `f_info_etfwindcode` | 关联ETFWind代码 |  |
| `f_info_exceptionstatus` | 产品异常状态 |  |
| `f_info_exchangecode` | 理财产品交易所代码 |  |
| `f_info_exchangeshortname` | 基金场内简称 |  |
| `f_info_exchmarket` | 基金上市地点(新增) |  |
| `f_info_existingyear` | 成立年限 |  |
| `f_info_expectedendingday` | 预计封闭期结束日 |  |
| `f_info_expectedopenday` | 预计下期开放日 |  |
| `f_info_expectedrateofreturn` | 预计年收益率 |  |
| `f_info_expectedyield` | 预期收益率(文字) |  |
| `f_info_feediscountornot` | 是否费率优惠 |  |
| `f_info_firstinveststrategy` | 投资策略分类(一级)(私募) |  |
| `f_info_firstinvesttype` | 投资类型(一级分类)(新增) |  |
| `f_info_firstmarketfundcode` | 一级市场基金代码 |  |
| `f_info_floatingmgntfeedescrip` | 浮动管理费率说明 |  |
| `f_info_floatingmgntfeeornot` | 是否收取浮动管理费 |  |
| `f_info_floatingratenote` | 浮动收益说明 |  |
| `f_info_foffundornot` | 是否FOF基金 |  |
| `f_info_foreigncustodian` | 境外托管人 |  |
| `f_info_foreigninvestmentadvisor` | 境外投资顾问 |  |
| `f_info_frontendcode` | 基金前端代码 |  |
| `f_info_fullname` | 基金全称 |  |
| `f_info_fullnameen` | 基金全称(英文) |  |
| `f_info_fundarrivaldays` | 资金到账天数 |  |
| `f_info_fundmaincodeofficial` | 基金主代码(官方) |  |
| `f_info_fundmanager` | 基金经理 |  |
| `f_info_fundmanager_rank` | 基金经理(现任,按名次) | TopN |
| `f_info_fundmanageroftradedate` | 基金经理 | TRADEDATE |
| `f_info_fundscale` | 基金规模 |  |
| `f_info_fundscale_cc` | 基金规模(币种转换) | TRADEDATE |
| `f_info_fundsharetranslationdate` | 基金份额折算日 |  |
| `f_info_fundsharetranslationratio` | 基金份额折算比例 |  |
| `f_info_fundtransition` | 基金转型说明 |  |
| `f_info_generalbeneficialamount` | 一般受益权金额 |  |
| `f_info_grlmrkr` | 一般做市商 | TRADEDATE |
| `f_info_guaranteedcycle` | 保本周期 |  |
| `f_info_guaranteedcycle_enddate` | 保本周期终止日期 |  |
| `f_info_guaranteedcycle_startdate` | 保本周期起始日期 |  |
| `f_info_guaranteedfeerate` | 保本费率 |  |
| `f_info_guaranteedornot` | 是否保本 |  |
| `f_info_guaranteedtriggerratio` | 保本触发收益率 |  |
| `f_info_guaranteedtriggertxt` | 保本触发机制说明 |  |
| `f_info_highestsubscriptionfee` | 最高认购费率 | Charges、TRADEDATE |
| `f_info_hkscinvestmentproportion` | 港股通股票投资比例说明 |  |
| `f_info_inceptionfundmanager` | 基金经理(成立) |  |
| `f_info_indexusagefeeratio` | 指数使用费率 |  |
| `f_info_initial` | 是否初始基金 |  |
| `f_info_initialcode` | 基金初始代码 |  |
| `f_info_initiallever` | 初始杠杆 |  |
| `f_info_interestpaymethod` | 付息方式说明 |  |
| `f_info_invadvisermgntfee` | 投资顾问固定管理费率 |  |
| `f_info_investconception` | 投资理念 |  |
| `f_info_investingregiondescription` | 主要投资区域说明 |  |
| `f_info_investmentadvisor` | 投资顾问 |  |
| `f_info_investmentproportion` | 投资品种比例限制 | InvestmentVariety |
| `f_info_investmentregion` | 投资区域 |  |
| `f_info_investobject` | 投资目标 |  |
| `f_info_investscope` | 投资范围 |  |
| `f_info_investstrategy` | 基金投资策略 | REPORTDATE |
| `f_info_investstrategy2` | 基金投资策略 |  |
| `f_info_investstyle` | 投资风格 |  |
| `f_info_investtype` | 投资类型 |  |
| `f_info_investtype2` | 投资类型 | FundGroup |
| `f_info_investtype_anytime` | 投资类型(支持历史) | FundGroup、TRADEDATE |
| `f_info_investtypeeng` | 投资类型(英文) | FundGroup |
| `f_info_invrstr` | 基金投资限制 |  |
| `f_info_issuecurrencycode` | 发行币种 |  |
| `f_info_issuedcontractamount` | 发行信托合同总数 |  |
| `f_info_issuercode` | 发行机构自编代码 |  |
| `f_info_issuershortname` | 发行机构自编简称 |  |
| `f_info_issuertype` | 发行人类型 |  |
| `f_info_issuingplace` | 发行地 |  |
| `f_info_lastopenday` | 定开基金上一开放日 |  |
| `f_info_lcrisklevel` | 银行理财风险等级(银行) |  |
| `f_info_lcrisklevelwind` | 银行理财风险等级(Wind) |  |
| `f_info_lipperfundtype` | 理柏基金类型 |  |
| `f_info_listdatadate` | 上市公告数据截止日期 |  |
| `f_info_listeddate` | 封闭式基金上市日 |  |
| `f_info_lofdealshareonmarket` | 上市交易份额 |  |
| `f_info_loflisteddate` | 上市日期 |  |
| `f_info_lofornot` | 是否LOF基金 |  |
| `f_info_longestfundmanager_hist` | 任职期限最长的在任基金经理(支持历史) | TRADEDATE、TopN |
| `f_info_lowerbenchmark` | 业绩比较基准下限 |  |
| `f_info_mainrisk` | 主要风险点 |  |
| `f_info_managementfeechangedate` | 管理费率变更日期 |  |
| `f_info_managementfeeratio` | 管理费率 |  |
| `f_info_managementfeeratio2` | 管理费率(支持历史) | TRADEDATE |
| `f_info_managementrisk` | 管理风险提示 |  |
| `f_info_manager_age` | 年龄 |  |
| `f_info_manager_age_2` | 年龄 |  |
| `f_info_manager_arithmeticannualizedyield` | 算术平均年化收益率 |  |
| `f_info_manager_arithmeticannualizedyield_2` | 算术平均年化收益率 |  |
| `f_info_manager_arithmeticavgannualyieldoverbench` | 超越基准算术平均年化收益率 |  |
| `f_info_manager_arithmeticavgannualyieldoverbench_2` | 超越基准算术平均年化收益率 |  |
| `f_info_manager_awardrecord` | 任职基金获奖记录 |  |
| `f_info_manager_awardrecordnum` | 履任以来获奖总次数 |  |
| `f_info_manager_awardrecordnum_2` | 履任以来获奖总次数 |  |
| `f_info_manager_background` | 投资经理背景 | TopN |
| `f_info_manager_bestperformance` | 现任基金最佳回报 | TopN |
| `f_info_manager_birthyear` | 出生年份 |  |
| `f_info_manager_birthyear_2` | 出生年份 |  |
| `f_info_manager_education` | 学历 |  |
| `f_info_manager_education_2` | 学历 |  |
| `f_info_manager_enddate` | 离职日期 |  |
| `f_info_manager_fundcodes` | 任职基金代码 | TopN |
| `f_info_manager_fundcodes_2` | 任职基金代码 |  |
| `f_info_manager_fundno` | 任职基金数 |  |
| `f_info_manager_fundno_2` | 任职基金数 |  |
| `f_info_manager_gender` | 性别 |  |
| `f_info_manager_gender_2` | 性别 |  |
| `f_info_manager_geometricannualizedyield` | 几何平均年化收益率 |  |
| `f_info_manager_geometricannualizedyield_2` | 几何平均年化收益率 |  |
| `f_info_manager_geometricavgannualyieldoverbench` | 超越基准几何平均年化收益率 |  |
| `f_info_manager_geometricavgannualyieldoverbench_2` | 超越基准几何平均年化收益率 |  |
| `f_info_manager_longestfundmanager` | 任职期限最长的现任基金经理 |  |
| `f_info_manager_managerworkingyears` | 基金经理年限 |  |
| `f_info_manager_managerworkingyears_2` | 基金经理年限 |  |
| `f_info_manager_maxdrawdown` | 任期最大回撤 |  |
| `f_info_manager_maxreturn` | 任期最大回报 |  |
| `f_info_manager_nationality` | 国籍 |  |
| `f_info_manager_nationality_2` | 国籍 |  |
| `f_info_manager_onthepostdays` | 任职天数 |  |
| `f_info_manager_pamp` | 基金经理(兼任私募) | REPORTDATE、TopN |
| `f_info_manager_pampna` | 兼任私募产品规模 | REPORTDATE、TopN |
| `f_info_manager_pampno` | 兼任私募产品数 | REPORTDATE、TopN |
| `f_info_manager_previousfundno` | 历任基金数 |  |
| `f_info_manager_previousfundno_2` | 历任基金数 |  |
| `f_info_manager_proxyformanager` | 代管基金经理说明 |  |
| `f_info_manager_resignationreason` | 离任原因 |  |
| `f_info_manager_resume` | 简历 |  |
| `f_info_manager_resume_2` | 简历 |  |
| `f_info_manager_startdate` | 任职日期 |  |
| `f_info_manager_startdateofmanagercareer` | 证券从业日期 | TopN |
| `f_info_manager_totalgeometricreturn` | 任职基金几何总回报 |  |
| `f_info_manager_totalnetasset` | 任职基金总规模 | TopN |
| `f_info_manager_totalnetasset2` | 任职基金总规模(支持历史) | TopN、TRADEDATE |
| `f_info_manager_totalnetasset2_2` | 任职基金总规模(支持历史) | TRADEDATE |
| `f_info_manager_totalnetasset_2` | 任职基金总规模 |  |
| `f_info_manager_totalreturnoverbenchmark` | 超越基准总回报 |  |
| `f_info_manager_totalreturnoverbenchmark_2` | 超越基准总回报 |  |
| `f_info_managerindex_alpha` | Alpha(基金经理指数) | StartDate、EndDate |
| `f_info_managerindex_alpha_2` | Alpha(基金经理指数,算术平均) | StartDate、EndDate |
| `f_info_managerindex_beta` | Beta(基金经理指数) | StartDate、EndDate |
| `f_info_managerindex_beta_2` | Beta(基金经理指数,算术平均) | StartDate、EndDate |
| `f_info_managerindex_maxdownside` | 基金经理指数最大回撤(算术平均) | StartDate、EndDate、TopN、IndexBelong |
| `f_info_managerindex_maxdownside_2` | 基金经理指数最大回撤(算术平均) | StartDate、EndDate |
| `f_info_managerindex_return` | 基金经理指数区间回报 | StartDate、EndDate |
| `f_info_managerindex_return_2` | 基金经理指数区间回报(算术平均) | StartDate、EndDate |
| `f_info_managerindex_sharpe` | Sharpe(基金经理指数) | StartDate、EndDate |
| `f_info_managerindex_sharpe_2` | Sharpe(基金经理指数,算术平均) | StartDate、EndDate |
| `f_info_managerindex_stdev` | 基金经理指数收益标准差 | StartDate、EndDate |
| `f_info_managerindex_stdev_2` | 基金经理指数收益标准差(算术平均) | StartDate、EndDate |
| `f_info_managerindex_stdevyearly` | 基金经理指数年化波动率 | StartDate、EndDate |
| `f_info_managerindex_stdevyearly_2` | 基金经理指数年化波动率(算术平均) | StartDate、EndDate |
| `f_info_managerindex_treynor` | Treynor(基金经理指数) | StartDate、EndDate |
| `f_info_managerindex_treynor_2` | Treynor(基金经理指数,算术平均) | StartDate、EndDate |
| `f_info_managerindex_weight_alpha` | Alpha(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_alpha_2` | Alpha(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_beta` | Beta(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_beta_2` | Beta(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_maxdownside` | 基金经理指数最大回撤(规模加权) | StartDate、EndDate、TopN |
| `f_info_managerindex_weight_maxdownside_2` | 基金经理指数最大回撤(规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_return` | 基金经理指数区间回报(规模加权) | StartDate、EndDate、TopN |
| `f_info_managerindex_weight_return_2` | 基金经理指数区间回报(规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_sharpe` | Sharpe(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_sharpe_2` | Sharpe(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_stdev` | 基金经理指数收益标准差(规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_stdevyearly` | 基金经理指数年化波动率(规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_treynor` | Treynor(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerindex_weight_treynor_2` | Treynor(基金经理指数,规模加权) | StartDate、EndDate |
| `f_info_managerintergrity` | 管理人是否存在诚信信息 |  |
| `f_info_managernoticeinfo` | 管理人是否存在提示信息 |  |
| `f_info_managersbuyamount` | 管理人参与金额 |  |
| `f_info_managescaleinterval` | 协会备案管理人在管规模 | ManagementType |
| `f_info_marketanalysis` | 市场分析 | REPORTDATE |
| `f_info_marketoutlook` | 市场展望 |  |
| `f_info_marketrisk` | 市场风险提示 |  |
| `f_info_massredemptionprovision` | 巨额赎回条款 |  |
| `f_info_maturitydate` | 基金到期日 |  |
| `f_info_maturitydate_2` | 基金到期日 |  |
| `f_info_maxfduntoffex` | 网下投资方认购份额上限 |  |
| `f_info_maxsubscripamount` | 委托金额上限 |  |
| `f_info_maxworkingyears` | 基金经理最大年限 |  |
| `f_info_mgntfeeexplain` | 管理费说明 |  |
| `f_info_mgrcomp` | 基金管理人 |  |
| `f_info_minaddbuyamount` | 追加认购最低金额 |  |
| `f_info_minaipdiscounts` | 最低定投折扣 |  |
| `f_info_minbuyamount` | 最低参与金额 |  |
| `f_info_minfduntoffex` | 网下投资方认购份额下限 |  |
| `f_info_minholdingperiod` | 基金最短持有期 |  |
| `f_info_minpurchasediscounts` | 最低申购折扣 |  |
| `f_info_minsublotsz` | 网下投资方认购份额最小变动单位 |  |
| `f_info_morningstarfundtype` | 晨星基金类型 |  |
| `f_info_name` | 基金简称 |  |
| `f_info_name_official` | 基金简称(官方) |  |
| `f_info_networkcashbuyenddate` | 网上现金认购截止日 |  |
| `f_info_networkcashbuysharedownlimit` | 网上现金认购份额下限 |  |
| `f_info_networkcashbuyshareuplimit` | 网上现金认购份额上限 |  |
| `f_info_networkcashbuystartdate` | 网上现金认购起始日 |  |
| `f_info_numofopendays` | 定开基金已开放次数 |  |
| `f_info_offnetworkbuyenddate` | 网下现金认购截止日 |  |
| `f_info_offnetworkbuystartdate` | 网下现金认购起始日 |  |
| `f_info_offnetworkcashbuysharedownlimit` | 网下现金认购份额下限 |  |
| `f_info_offnetworkstockbuyenddate` | 网下股票认购截止日 |  |
| `f_info_offnetworkstockbuysharedownlimit` | 网下股票认购份额下限 |  |
| `f_info_offnetworkstockbuystartdate` | 网下股票认购起始日 |  |
| `f_info_onlinecashofferingsymbol` | 网上现金发售代码 |  |
| `f_info_opendayillus` | 开放日说明 |  |
| `f_info_opendays` | 定开基金开放日(支持历史) | N |
| `f_info_operateperiod_cls` | 封闭运作期 |  |
| `f_info_operationmode` | 产品运作方式 |  |
| `f_info_operationtype` | 运作模式 |  |
| `f_info_otherrisks` | 其他风险提示 |  |
| `f_info_pairconversion` | 是否配对转换 |  |
| `f_info_parvalue` | 面值(新增) |  |
| `f_info_pchconfirmdate` | 申购确认日 |  |
| `f_info_pchmstatus` | 申购状态 | TRADEDATE |
| `f_info_pchquerydate` | 申购确认查询天数 |  |
| `f_info_pequotationcode` | 机构间私募产品报价系统编码 |  |
| `f_info_performancefeemethod` | 业绩报酬提取方法 |  |
| `f_info_performancefeeornot` | 是否提取业绩报酬 |  |
| `f_info_periodtype` | 期限类型 |  |
| `f_info_plantype` | 计划类型 |  |
| `f_info_pledgableornot` | 是否可质押 |  |
| `f_info_postbondtype` | 基金债券券种配置事后分类 |  |
| `f_info_postinvestregiontype` | 基金股票投资区域事后分类 |  |
| `f_info_postinvesttype` | 基金投资类型事后分类 | FundGroup |
| `f_info_poststockindustrytype` | 基金股票行业事后分类 |  |
| `f_info_prctkperfdunt` | 网下投资方认购价格最小变动单位 |  |
| `f_info_predfundmanager` | 基金经理(历任)(新增) |  |
| `f_info_primarydealers` | 一级交易商 |  |
| `f_info_primymrkr` | 主做市商 | TRADEDATE |
| `f_info_prioritybeneficialamount` | 优先受益权金额 |  |
| `f_info_prioritytogeneral` | 受托资金比(优先/一般) |  |
| `f_info_prodtype_wind` | Wind产品类型 |  |
| `f_info_prodtypeoc_wind` | Wind封闭式开放式基金分类 |  |
| `f_info_ptm` | 剩余存续期 |  |
| `f_info_ptmday` | 剩余存续期(新增) |  |
| `f_info_ptmyear` | 基金存续期(新增) |  |
| `f_info_purchaseandredemptionabbreviation` | 申购赎回简称 |  |
| `f_info_purchasedate` | 开放式基金申购起始日 |  |
| `f_info_purchasefee` | 申购费率 |  |
| `f_info_purchasefee2` | 申购费率(支持历史) | Charges_Type、TRADEDATE |
| `f_info_purchasefeeratio` | 最高申购费率 |  |
| `f_info_qsimilarproductsimilarranking` | 规模同类排名（券商集合理财） |  |
| `f_info_raisingmode` | 募集方式 |  |
| `f_info_recognitiondate` | 互认基金批复日期 |  |
| `f_info_recognitionrep` | 境内代理人 |  |
| `f_info_redemptionfee` | 赎回费率 |  |
| `f_info_redemptionfee2` | 赎回费率(支持历史) | Charges_Type、TRADEDATE |
| `f_info_redemptionfeeratio` | 最高赎回费率 |  |
| `f_info_redemptionrisk` | 赎回风险提示 |  |
| `f_info_redmarrialdate` | 赎回划款日 |  |
| `f_info_redmconfirmdate` | 赎回确认日 |  |
| `f_info_redmquerydate` | 赎回确认查询天数 |  |
| `f_info_redmstartdate` | 赎回起始日(新增) |  |
| `f_info_redmstatus` | 赎回状态 | TRADEDATE |
| `f_info_regulopenfundornot` | 是否定期开放基金 |  |
| `f_info_reits_amcity` | 资产运营管理机构所在城市 |  |
| `f_info_reits_amprov` | 资产运营管理机构所在省份 |  |
| `f_info_reitsabscode` | 持有资产支持证券代码 | TopN |
| `f_info_reitsabsname` | 持有资产支持证券名称 | TopN |
| `f_info_reitsasname` | 资产名称 | TopN |
| `f_info_reitsassetcity` | 项目资产所在城市 |  |
| `f_info_reitsassetprov` | 项目资产所在省份 |  |
| `f_info_reitsbkblddt` | REITs基金份额询价日期 |  |
| `f_info_reitscomname` | 项目公司名称 | TopN |
| `f_info_reitsdisc` | 初始折现率 |  |
| `f_info_reitsdistramountf` | 可供分配金额(预测) | REPORTDATE |
| `f_info_reitsdprf` | 派息率(预测) | REPORTDATE |
| `f_info_reitsebitdaf` | 税息折旧及摊销前利润(预测) | REPORTDATE |
| `f_info_reitsevalue` | 资产估值 |  |
| `f_info_reitsfmam` | 网下基金公司或其资管机构配售金额 |  |
| `f_info_reitsfmar` | 网下基金公司或其资管计划配售份额占比 |  |
| `f_info_reitsfmas` | 网下基金公司或其资管计划配售数量 |  |
| `f_info_reitsfmm` | 网下基金公司或其资管子公司配售金额 |  |
| `f_info_reitsfmr` | 网下基金公司或其资管子公司配售份额占比 |  |
| `f_info_reitsfms` | 网下基金公司或其资管子公司配售数量 |  |
| `f_info_reitsinfo` | 项目介绍 |  |
| `f_info_reitsirr` | 初始内部收益率 |  |
| `f_info_reitsism` | 网下保险资金投资账户配售金额 |  |
| `f_info_reitsisr` | 网下保险资金投资账户配售份额占比 |  |
| `f_info_reitsiss` | 网下保险资金投资账户配售数量 |  |
| `f_info_reitsissuesize` | 发行规模 |  |
| `f_info_reitslimitedshare` | 限售份额 | DATE |
| `f_info_reitslimitedshareft` | 场内限售份额 | TRADEDATE |
| `f_info_reitslisteddate` | REITs上市日期 |  |
| `f_info_reitslocation` | 资产所在地 | TopN |
| `f_info_reitsoca` | REITs运营管理统筹机构 |  |
| `f_info_reitsoffendate` | 网下发售截止日 |  |
| `f_info_reitsoffshare` | 网下配售份额 |  |
| `f_info_reitsoffsharera` | 网下配售份额占比 |  |
| `f_info_reitsoffstdate` | 网下发售起始日 |  |
| `f_info_reitsoia` | REITs运营管理实施机构 |  |
| `f_info_reitsoiratio` | 网下投资方认购比例 |  |
| `f_info_reitsoishare` | 网下认购份额 |  |
| `f_info_reitsoprisk` | 项目运营风险 |  |
| `f_info_reitsorcom` | 原始权益人企业性质 | TopN |
| `f_info_reitsoriginal` | 原始权益人 | TopN |
| `f_info_reitsoriginalequityratio` | 原始权益人或其同一控制下关联方配售份额占总份额比例 |  |
| `f_info_reitsoriginalequityshare` | 原始权益人或其同一控制下关联方配售份额 |  |
| `f_info_reitsothersiratio` | 其他战略投资者配售份额占总份额比例 |  |
| `f_info_reitsothersishare` | 其他战略投资者配售份额 |  |
| `f_info_reitspbendate` | 公众发售截止日 |  |
| `f_info_reitspbshare` | 公众配售份额 |  |
| `f_info_reitspbsharera` | 公众配售份额占比 |  |
| `f_info_reitspbstdate` | 公众发售起始日 |  |
| `f_info_reitspfm` | 网下私募基金配售金额 |  |
| `f_info_reitspfr` | 网下私募基金配售份额占比 |  |
| `f_info_reitspfs` | 网下私募基金配售数量 |  |
| `f_info_reitspim` | 网下机构自营投资账户配售金额 |  |
| `f_info_reitspir` | 网下机构自营投资账户配售份额占比 |  |
| `f_info_reitspiratio` | 公众投资方认购比例 |  |
| `f_info_reitspis` | 网下机构自营投资账户配售数量 |  |
| `f_info_reitspishare` | 公众认购份额 |  |
| `f_info_reitspricemax` | 询价区间上限 |  |
| `f_info_reitspricemin` | 询价区间下限 |  |
| `f_info_reitspropmgmt` | REITs运营管理机构 |  |
| `f_info_reitsqfm` | 网下QFII投资账户配售金额 |  |
| `f_info_reitsqfr` | 网下QFII投资账户配售份额占比 |  |
| `f_info_reitsqfs` | 网下QFII投资账户配售数量 |  |
| `f_info_reitsrproperty` | 项目属性 |  |
| `f_info_reitsscm` | 网下证券公司集合资产管理计划配售金额 |  |
| `f_info_reitsscr` | 网下证券公司集合资产管理计划配售份额占比 |  |
| `f_info_reitsscs` | 网下证券公司集合资产管理计划配售数量 |  |
| `f_info_reitsscsm` | 网下证券公司单一资产管理计划配售金额 |  |
| `f_info_reitsscsr` | 网下证券公司单一资产管理计划配售份额占比 |  |
| `f_info_reitsscss` | 网下证券公司单一资产管理计划配售数量 |  |
| `f_info_reitssiendate` | 战略发售截止日 |  |
| `f_info_reitssiratio` | 战略投资方认购比例 |  |
| `f_info_reitssishare` | 战略配售份额 |  |
| `f_info_reitssisharera` | 战略配售份额占比 |  |
| `f_info_reitssisharesub` | 战略投资方认购份额 |  |
| `f_info_reitssistdate` | 战略发售起始日 |  |
| `f_info_reitsspmanager` | 专项计划管理人 | TRADEDATE |
| `f_info_reitstrm` | 网下集合信托计划配售金额 |  |
| `f_info_reitstrr` | 网下集合信托计划配售份额占比 |  |
| `f_info_reitstrs` | 网下集合信托计划配售数量 |  |
| `f_info_reitstype` | 资产类型 |  |
| `f_info_reitsvaag` | 资产评估机构 |  |
| `f_info_reitsvalin` | 初始估值 |  |
| `f_info_relatedcode` | 关联基金代码 |  |
| `f_info_returnenddate` | 收益终止日 |  |
| `f_info_returnstartdate` | 收益起始日 |  |
| `f_info_risklevel` | 基金风险等级 |  |
| `f_info_risklevelfiling` | 基金风险等级(公告口径) | TRADEDATE |
| `f_info_riskreturn_characters` | 风险收益特征 | TRADEDATE |
| `f_info_salefeeratio` | 销售服务费率 |  |
| `f_info_salefeeratio2` | 销售服务费率(支持历史) | TRADEDATE |
| `f_info_salesfeechangedate` | 销售服务费率变更日期 |  |
| `f_info_scaleranking` | 规模同类排名 |  |
| `f_info_secondinveststrategy` | 投资策略分类(二级)(私募) |  |
| `f_info_securitiesbroker` | 证券经纪人 |  |
| `f_info_settlementmode` | 交易结算模式 |  |
| `f_info_setupdate` | 基金成立日 |  |
| `f_info_sidepocketfundornot` | 是否使用侧袋机制 |  |
| `f_info_similarfundno` | 同类基金数量 |  |
| `f_info_smfacode` | 分级基金优先级代码 |  |
| `f_info_smfbcode` | 分级基金普通级代码 |  |
| `f_info_smfcode` | 分级基金母基金代码 |  |
| `f_info_smftype` | 分级基金类别 |  |
| `f_info_smftype2` | 基金分级类型 |  |
| `f_info_spenotice` | 基金特别提示信息 |  |
| `f_info_splitratio` | 拆分比率 |  |
| `f_info_startdateofclosure` | 定开基金封闭起始日 | TRADEDATE |
| `f_info_structuredfundornot` | 是否分级基金(新增) |  |
| `f_info_structuredornot` | 是否结构化产品 |  |
| `f_info_subenddate` | 销售截止日期 |  |
| `f_info_sublim` | 基金申购限额说明 | TRADEDATE |
| `f_info_subscriptionfee` | 认购费率 |  |
| `f_info_subscriptionfee2` | 认购费率(支持历史) | Charges_Type、TRADEDATE |
| `f_info_substartdate` | 销售起始日期 |  |
| `f_info_t0ornot` | 是否T+0交易 |  |
| `f_info_targetscale` | 目标规模 |  |
| `f_info_technicalrisk` | 技术风险提示 |  |
| `f_info_terfops` | 基金运作综合费率(年化) | TRADEDATE |
| `f_info_themetype` | 所属主题基金类别 |  |
| `f_info_themetype_concept` | 所属主题基金类别(Wind概念) |  |
| `f_info_themetype_index` | 所属主题基金类别(Wind股票指数) |  |
| `f_info_themetype_industry` | 所属主题基金类别(Wind行业) |  |
| `f_info_thirdpartyfundtype` | 第三方基金分类 | ORG |
| `f_info_trackdeviation_threshold` | 日均跟踪偏离度阀值(业绩基准) |  |
| `f_info_trackerror_threshold` | 年化跟踪误差阀值(业绩基准) |  |
| `f_info_trackindexcode` | 跟踪指数代码 |  |
| `f_info_trackindexname` | 跟踪指数名称 |  |
| `f_info_trustee` | 受托人 |  |
| `f_info_trusteemgntfee` | 受托人固定管理费率 |  |
| `f_info_trusttype` | 信托类别 |  |
| `f_info_type` | 基金类型 |  |
| `f_info_underlyingtarget` | 收益挂钩标的 |  |
| `f_info_updiscount` | 向上触点折算条款 |  |
| `f_info_upperbenchmark` | 业绩比较基准上限 |  |
| `f_info_valadsfeef` | 基金增值服务费率(支持历史) | TRADEDATE |
| `f_info_valuationmethod` | 基金估值方法 |  |
| `f_info_warrantor` | 保证人 |  |
| `f_info_warrantorintroduction` | 保证人简介 |  |
| `f_info_windcode` | Wind代码 |  |
| `f_info_wmissuer` | 银行理财发行人 |  |
| `f_info_yieldtype` | 收益类型 |  |
| `f_info_yinhefundtype` | 银河基金类型 |  |
| `f_ipo_anncelstdate` | 上市公告日 |  |
| `f_issue_announcedate` | 发行公告日 |  |
| `f_issue_cef_inipurchase` | 封闭式基金认购数量(新增) |  |
| `f_issue_cef_listdate` | 封闭式基金上市日期(新增) |  |
| `f_issue_cef_npctchange` | 基金上市后N日涨跌幅(新增) |  |
| `f_issue_cef_nturn` | 基金上市后N日换手率(新增) |  |
| `f_issue_cef_oversub` | 封闭式基金超额认购倍数(新增) |  |
| `f_issue_cef_pctchange` | 基金上市首日涨跌幅(新增) |  |
| `f_issue_cef_succratio` | 封闭式基金中签率(新增) |  |
| `f_issue_cef_turn` | 基金上市首日换手率(新增) |  |
| `f_issue_channel` | 产品发行渠道 |  |
| `f_issue_coordinator` | 基金发行协调人(新增) |  |
| `f_issue_date` | 发行日期(新增) |  |
| `f_issue_deputy` | 基金销售代理人(新增) |  |
| `f_issue_financeconsultant` | 财务顾问 | TopN |
| `f_issue_initiator` | 基金发起人(新增) |  |
| `f_issue_leadunderwriter` | 基金主承销商(新增) |  |
| `f_issue_nominator` | 基金上市推荐人(新增) |  |
| `f_issue_object` | 发行对象(新增) |  |
| `f_issue_oef_clsperiod` | 发行封闭期(新增) |  |
| `f_issue_oef_cndnetpurchase` | 成立条件-净认购份额 |  |
| `f_issue_oef_cndpurchasers` | 成立条件-认购户数(新增) |  |
| `f_issue_oef_confirmdate` | 认购比例确认公告日 |  |
| `f_issue_oef_confirmratio` | 认购份额确认比例 |  |
| `f_issue_oef_days` | 认购天数 |  |
| `f_issue_oef_dnddateinst` | 机构投资者设立认购终止日(新增) |  |
| `f_issue_oef_enddateind` | 个人投资者认购终止日(新增) |  |
| `f_issue_oef_maxamtind` | 个人投资者认购金额上限(新增) |  |
| `f_issue_oef_maxamtinst` | 封闭期机构投资者认购上限(新增) |  |
| `f_issue_oef_maxcollection` | 募集份额上限 |  |
| `f_issue_oef_minamtind` | 个人投资者认购金额下限(新增) |  |
| `f_issue_oef_minamtinst` | 封闭期机构投资者认购下限(新增) |  |
| `f_issue_oef_mthdind` | 个人投资者认购方式(新增) |  |
| `f_issue_oef_mthdinst` | 封闭期机构投资者认购方式(新增) |  |
| `f_issue_oef_numpurchasers` | 开放式基金认购户数(新增) |  |
| `f_issue_oef_startdateind` | 个人投资者认购起始日(新增) |  |
| `f_issue_oef_startdateinst` | 机构投资者设立认购起始日(新增) |  |
| `f_issue_price` | 上市基金发行价格(新增) |  |
| `f_issue_rasing_isenddeferred` | 是否延长募集期 |  |
| `f_issue_rasing_isendearly` | 是否提前结束募集 |  |
| `f_issue_rasing_isstartdeferred` | 是否延期募集 |  |
| `f_issue_rasing_isstartearly` | 是否提前开始募集 |  |
| `f_issue_registrar` | 基金注册与过户登记人(新增) |  |
| `f_issue_totalsize` | 发行总规模 |  |
| `f_issue_totalunit` | 发行总份额(新增) |  |
| `f_issue_type` | 发行方式(新增) |  |
| `f_issue_unit` | 发行份额 |  |
| `f_latest_rptdate` | 最新报告期 | DATE、DataType |
| `f_lowestaccumnav_date` | 区间最低累计单位净值日 | StartDate、EndDate |
| `f_lowestadjnav_date` | 区间最低复权单位净值日 | StartDate、EndDate |
| `f_lowestnav_date` | 区间最低单位净值日 | StartDate、EndDate |
| `f_mf_netinflow` | 净流入额 | TRADEDATE |
| `f_mgmt_sub_ratio` | 管理人认购比例 |  |
| `f_mgmt_sub_shares` | 管理人认购份额 |  |
| `f_mmf_annualizedyield` | 7日年化收益率 |  |
| `f_mmf_avgannualizedyield` | 区间7日年化收益率均值 | BEGINDATE、EndDate |
| `f_mmf_avgdeviation` | 报告期内每个工作日偏离度的绝对值的简单平均值 | REPORTDATE |
| `f_mmf_avgptm` | 报告期末投资组合平均剩余期限 | REPORTDATE |
| `f_mmf_avgptm_max` | 报告期内投资组合平均剩余期限最高值 | REPORTDATE |
| `f_mmf_avgptm_min` | 报告期内投资组合平均剩余期限最低值 | REPORTDATE |
| `f_mmf_avgunityield` | 区间万份基金单位收益均值 | BEGINDATE、EndDate |
| `f_mmf_bond` | 债券投资金额 | REPORTDATE |
| `f_mmf_bondtoasset` | 债券投资占基金资产总值的比例 | REPORTDATE |
| `f_mmf_carryover` | 份额结转方式 |  |
| `f_mmf_carryoverdate` | 份额结转日期类型 |  |
| `f_mmf_deposit` | 银行存款和清算备付金 | REPORTDATE |
| `f_mmf_deposittoasset` | 银行存款和清算备付金合计占基金资产总值的比例 | REPORTDATE |
| `f_mmf_differentptmtonav` | 各期限资产占基金资产净值比例 | REPORTDATE |
| `f_mmf_frequencyofdeviation` | 报告期内偏离度的绝对值在0.25%(含)-0.5%间的次数 | REPORTDATE |
| `f_mmf_maxdeviation` | 报告期内偏离度的最高值 | REPORTDATE |
| `f_mmf_mindeviation` | 报告期内偏离度的最低值 | REPORTDATE |
| `f_mmf_other` | 其他资产 | REPORTDATE |
| `f_mmf_othertoasset` | 其他资产占基金资产总值的比例 | REPORTDATE |
| `f_mmf_repurchase1` | 报告期内债券回购融资余额 | REPORTDATE |
| `f_mmf_repurchase1tonav` | 报告期内债券回购融资余额占基金资产净值比例 | REPORTDATE |
| `f_mmf_repurchase2` | 报告期末债券回购融资余额 | REPORTDATE |
| `f_mmf_repurchase2tonav` | 报告期末债券回购融资余额占基金资产净值比例 | REPORTDATE |
| `f_mmf_reverserepo` | 买入返售证券金额 | REPORTDATE |
| `f_mmf_reverserepotoasset` | 买入返售证券占基金资产总值的比例 | REPORTDATE |
| `f_mmf_totalunityield` | 区间万份基金单位收益总值 |  |
| `f_mmf_unityield` | 万份基金单位收益 |  |
| `f_mmf_varannualizedyield` | 区间7日年化收益率方差 | BEGINDATE、EndDate |
| `f_mmf_varunityield` | 区间万份基金单位收益方差 | BEGINDATE、EndDate |
| `f_mq_amount` | 月成交额(新增) |  |
| `f_mq_avgprice` | 月均价(新增) |  |
| `f_mq_avgturn` | 月平均换手率(新增) |  |
| `f_mq_change` | 月涨跌(新增) |  |
| `f_mq_close` | 月收盘价(新增) |  |
| `f_mq_discount` | 月均贴水(新增) |  |
| `f_mq_discountratio` | 月均贴水率(新增) |  |
| `f_mq_high` | 月最高价(新增) |  |
| `f_mq_highclose` | 月最高收盘价(新增) |  |
| `f_mq_highclose_date` | 月最高收盘价日(新增) |  |
| `f_mq_highdate` | 月最高价日(新增) |  |
| `f_mq_low` | 月最低价(新增) |  |
| `f_mq_lowclose` | 月最低收盘价(新增) |  |
| `f_mq_lowclose_date` | 月最低收盘价日(新增) |  |
| `f_mq_lowdate` | 月最低价日(新增) |  |
| `f_mq_open` | 月开盘价(新增) |  |
| `f_mq_pctchange` | 月涨跌幅(新增) |  |
| `f_mq_preclose` | 月前收盘价(新增) |  |
| `f_mq_relpctchange` | 月相对大盘涨跌幅(新增) |  |
| `f_mq_swing` | 月振幅(新增) |  |
| `f_mq_turn` | 月换手率(新增) |  |
| `f_mq_volume` | 月成交量(新增) |  |
| `f_nav_accumulated` | 累计单位净值 |  |
| `f_nav_accumulated_transform` | 累计单位净值(支持转型基金) | TRADEDATE |
| `f_nav_accumulated_transformnf` | 累计单位净值(支持转型基金,不前推) | TRADEDATE |
| `f_nav_accumulatedchange` | 累计单位净值增长(新增) | TD1、TD2 |
| `f_nav_accumulatedreturn` | 累计单位净值增长率 | BEGINDATE、EndDate |
| `f_nav_adjfactor` | 基金净值复权因子 | TRADEDATE |
| `f_nav_adjusted` | 复权单位净值 |  |
| `f_nav_adjusted_b` | 复权单位净值(前复权) | TRADEDATE |
| `f_nav_adjusted_transform` | 复权单位净值(支持转型基金) | TRADEDATE |
| `f_nav_adjusted_transformnf` | 复权单位净值(支持转型基金,不前推) | TRADEDATE |
| `f_nav_adjustedchange` | 复权单位净值增长(新增) | TD1、TD2 |
| `f_nav_adjustedrelpctchange` | 复权单位净值相对大盘增长率(新增) | TD1、TD2 |
| `f_nav_adjustedreturn` | 复权单位净值增长率 | BEGINDATE、EndDate |
| `f_nav_adjustedreturn1` | 当期复权单位净值增长率 | TRADEDATE |
| `f_nav_adjustedreturn_org` | 自成立日起复权单位净值增长率(新增) | TD |
| `f_nav_benchdevreturn` | 报告期净值增长率减基准增长率(新增) | D |
| `f_nav_benchreturn` | 报告期业绩比较基准增长率(新增) | D |
| `f_nav_benchstddev` | 报告期业绩比较基准增长率标准差(新增) | D |
| `f_nav_cashdivreturn` | 现金分红净值增长率 |  |
| `f_nav_date` | 基金净值日期 |  |
| `f_nav_date2` | 基金净值日期 | DEALDATE |
| `f_nav_exrightdate` | 最新净值除权日 | DEALDATE |
| `f_nav_firstdate` | 净值披露首日 |  |
| `f_nav_highestaccumulatednav` | 区间最高累计单位净值 | StartDate、EndDate |
| `f_nav_highestadjustednav` | 区间最高复权单位净值 | StartDate、EndDate |
| `f_nav_highestnav` | 区间最高单位净值 | StartDate、EndDate |
| `f_nav_iopv` | IOPV(新增) | DEALDATE |
| `f_nav_iopv_discountratio` | IOPV溢折率 | TRADEDATE |
| `f_nav_lcqperiodreturnranking` | 同类基金区间收益排名（券商集合理财） |  |
| `f_nav_lcqperiodreturnrankingper` | 同类基金区间收益排名(百分比)(券商集合理财) | StartDate、EndDate |
| `f_nav_lowestaccumulatednav` | 区间最低累计单位净值 | StartDate、EndDate |
| `f_nav_lowestadjustednav` | 区间最低复权单位净值 | StartDate、EndDate |
| `f_nav_lowestnav` | 区间最低单位净值 | StartDate、EndDate |
| `f_nav_navoverbenchreturn` | 区间净值超越基准收益率 |  |
| `f_nav_navoverbenchreturn_freq` | 区间净值超越基准收益频率 | Year |
| `f_nav_navoverbenchreturn_freq2` | 区间净值超越基准收益频率(百分比) | StartDate、EndDate |
| `f_nav_periodicannualizedreturn` | 任职年化回报 |  |
| `f_nav_periodicannualizedreturn_hist` | 任职年化回报(支持历史) | TRADEDATE、TopN |
| `f_nav_periodreturnranking` | 同类基金区间收益排名 |  |
| `f_nav_periodreturnranking_10y` | 近10年回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_1m` | 近1月回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_1w` | 近1周回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_1y` | 近1年回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_2y` | 近2年回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_3m` | 近3月回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_3y` | 近3年回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_5y` | 近5年回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_6m` | 近6月回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_y` | 单年度回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnranking_ytd` | 今年以来回报排名 | TRADEDATE、FundGroup |
| `f_nav_periodreturnrankingper` | 同类基金区间收益排名（百分比） |  |
| `f_nav_publishtype` | 基金净值公布类型 |  |
| `f_nav_ranking_p` | 同类基金区间收益排名P值 | StartDate、EndDate |
| `f_nav_return` | 报告期净值增长率(新增) | D |
| `f_nav_sellprice` | 投连险卖出价 | DATE |
| `f_nav_similarperiodavgreturn` | 同类基金区间平均收益率 |  |
| `f_nav_stddevnavbench` | 报告期净值增长率标准差减基准标准差(新增) | D |
| `f_nav_stddevreturn` | 报告期净值增长率标准差(新增) | D |
| `f_nav_unit` | 单位净值 |  |
| `f_nav_unit_transform` | 单位净值(支持转型基金) | TRADEDATE |
| `f_nav_updatecompleteness` | 基金净值完整度 | StartDate、EndDate、CalcTerm |
| `f_nav_updatefrequency` | 基金净值更新频率 |  |
| `f_nav_winlossratio` | 基金盈利概率 | StartDate、EndDate、CalcTerm |
| `f_nav_xtqperiodreturnranking` | 同类基金区间收益排名（阳光私募） |  |
| `f_nav_xtqperiodreturnranking2` | 同类基金区间收益排名(阳光私募,投资策略) | StartDate、EndDate、FundGroup |
| `f_nav_xtqperiodreturnrankingper` | 同类基金区间收益排名(百分比)(阳光私募) | StartDate、EndDate |
| `f_netasset_total` | 基金规模(合计) | TRADEDATE |
| `f_netasset_total2` | 基金规模合计 | TRADEDATE |
| `f_netasset_total_cc` | 基金规模(合计,币种转换) | TRADEDATE |
| `f_nq_navchange` | 基金N日净值增长率(新增) | Acount、DEALDATE |
| `f_pchredm_largepchmaxamt` | 单日大额申购限额 | TRADEDATE |
| `f_pchredm_maxredmfee` | 赎回费率上限(新增) |  |
| `f_pchredm_pchmaxfee` | 申购费率上限(新增) |  |
| `f_pchredm_pchminamt` | 申购金额下限(新增) |  |
| `f_pchredm_pchminamt_floor` | 申购金额下限(场内) |  |
| `f_pchredm_pchstartdate` | 申购起始日(新增) |  |
| `f_pchredm_redmminamt` | 单笔赎回份额下限(新增) |  |
| `f_periodmf_netinflow` | 区间净流入额 | StartDate、EndDate |
| `f_pmir_redeemspread` | 贵金属投资收益-赎回差价收入 | REPORTDATE |
| `f_pmir_subscribespread` | 贵金属投资收益-申购差价收入 | REPORTDATE |
| `f_pmir_total` | 贵金属投资收益-合计 | REPORTDATE |
| `f_pmir_tradespread` | 贵金属投资收益-买卖贵金属差价收入 | REPORTDATE |
| `f_pmirredeemspread_total` | 贵金属赎回差价收入-合计 | REPORTDATE |
| `f_pmirredeemspread_totalredempamt` | 贵金属赎回差价收入-赎回贵金属份额对价总额 | REPORTDATE |
| `f_pmirredeemspread_totalredempamtpic` | 贵金属赎回差价收入-现金支付赎回款总额 | REPORTDATE |
| `f_pmirredeemspread_totalredempcpm` | 贵金属赎回差价收入-赎回贵金属成本总额 | REPORTDATE |
| `f_pmirredeemspread_transcost` | 贵金属赎回差价收入-交易费用 | REPORTDATE |
| `f_pmirtradespread_total` | 买卖贵金属差价收入-合计 | REPORTDATE |
| `f_pmirtradespread_totalamout` | 买卖贵金属差价收入-卖出贵金属成交总额 | REPORTDATE |
| `f_pmirtradespread_totcost` | 买卖贵金属差价收入-卖出贵金属成本总额 | REPORTDATE |
| `f_pmirtradespread_transcost` | 买卖贵金属差价收入-交易费用 | REPORTDATE |
| `f_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `f_pq_avgamount` | 区间日均成交额,F_PQ_AvgAmount  ''''''''''未修改 | BEGINDATE、EndDate |
| `f_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `f_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `f_pq_avgvolume` | 区间日均成交量,F_PQ_AvgVolume  '''''''''未修改 | BEGINDATE、EndDate |
| `f_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `f_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `f_pq_discount` | 区间均贴水(新增) | TD1、TD2 |
| `f_pq_discountratio` | 区间均贴水率(新增) | TD1、TD2 |
| `f_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `f_pq_highclose` | 区间最高收盘价(新增) | TD1、TD2 |
| `f_pq_highclose_date` | 区间最高收盘价日(新增) | TD1、TD2 |
| `f_pq_highdate` | 区间最高价日(新增) | TD1、TD2 |
| `f_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `f_pq_lowclose` | 区间最低收盘价(新增) | TD1、TD2 |
| `f_pq_lowclose_date` | 区间最低收盘价日(新增) | TD1、TD2 |
| `f_pq_lowdate` | 区间最低价日(新增) | TD1、TD2 |
| `f_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `f_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `f_pq_pctchange2` | 区间涨跌幅(包含上市首日涨跌幅) | StartDate、EndDate |
| `f_pq_pctchange_a` | 区间涨跌幅(年化) | StartDate、EndDate |
| `f_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `f_pq_relpctchange` | 相对大盘区间涨跌幅(新增) | TD1、TD2 |
| `f_pq_swing` | 区间振幅(新增) | TD1、TD2 |
| `f_pq_topstockheldno` | 区间重仓股报告期重仓次数 | StartDate、EndDate、TopN |
| `f_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `f_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `f_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `f_prt_absbycreditrating` | 按信用评级的资产支持证券投资市值 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_absbycreditratingtonav` | 按信用评级的资产支持证券投资占基金资产净值比 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_abstonav` | 资产支持证券市值占基金资产净值比 | REPORTDATE |
| `f_prt_absvalue` | 资产支持证券市值 | REPORTDATE |
| `f_prt_avgnetasset` | 报告期基金日均资产净值 | REPORTDATE |
| `f_prt_bankdeposit` | 基金银行存款-合计 | REPORTDATE |
| `f_prt_bankdeposit_dd` | 基金银行存款-活期存款 | REPORTDATE |
| `f_prt_bankdeposit_ddabd` | 基金银行存款-活期存款(坏账准备) | REPORTDATE |
| `f_prt_bankdeposit_ddai` | 基金银行存款-活期存款(应计利息) | REPORTDATE |
| `f_prt_bankdeposit_ddp` | 基金银行存款-活期存款(本金) | REPORTDATE |
| `f_prt_bankdeposit_fbd` | 基金银行存款-其他存款 | REPORTDATE |
| `f_prt_bankdeposit_fbdabd` | 基金银行存款-其他存款(坏账准备) | REPORTDATE |
| `f_prt_bankdeposit_fbdai` | 基金银行存款-其他存款(应计利息) | REPORTDATE |
| `f_prt_bankdeposit_fbdp` | 基金银行存款-其他存款(本金) | REPORTDATE |
| `f_prt_bankdeposit_ltd` | 基金银行存款-定期存款(存款期限3个月以上) | REPORTDATE |
| `f_prt_bankdeposit_omtd` | 基金银行存款-定期存款(存款期限1个月以内) | REPORTDATE |
| `f_prt_bankdeposit_td` | 基金银行存款-定期存款 | REPORTDATE |
| `f_prt_bankdeposit_tdabd` | 基金银行存款-定期存款(坏账准备) | REPORTDATE |
| `f_prt_bankdeposit_tdai` | 基金银行存款-定期存款(应计利息) | REPORTDATE |
| `f_prt_bankdeposit_tdp` | 基金银行存款-定期存款(本金) | REPORTDATE |
| `f_prt_bankdeposit_tmtd` | 基金银行存款-定期存款(存款期限1-3个月) | REPORTDATE |
| `f_prt_bondbycreditrating` | 按信用评级的债券投资市值 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_bondbycreditratingtonav` | 按信用评级的债券投资占基金资产净值比 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_bondtoasset` | 债券市值占基金资产总值比 | REPORTDATE |
| `f_prt_bondtonav` | 债券市值占基金资产净值比 | REPORTDATE |
| `f_prt_bondtonavgrowth` | 债券市值占基金资产净值比例增长 |  |
| `f_prt_bondvalue` | 债券投资市值 | REPORTDATE |
| `f_prt_bondvaluegrowth` | 债券市值增长率 |  |
| `f_prt_buystockcost` | 报告期买入股票总成本(新增) | REPORTDATE |
| `f_prt_cash` | 银行存款 | REPORTDATE |
| `f_prt_cashtoasset` | 银行存款占基金资产总值比 | REPORTDATE |
| `f_prt_cashtonav` | 银行存款占基金资产净值比 | REPORTDATE |
| `f_prt_cashtonavgrowth` | 银行存款市值占基金资产净值比例增长 |  |
| `f_prt_cashvaluegrowth` | 银行存款市值增长率 |  |
| `f_prt_cds` | 同业存单市值 | REPORTDATE |
| `f_prt_cdstonav` | 同业存单市值占基金资产净值比 | REPORTDATE |
| `f_prt_centralbankbill` | 央行票据投资市值 | REPORTDATE |
| `f_prt_centralbankbillgrowth` | 央行票据市值增长率 |  |
| `f_prt_centralbankbilltoasset` | 央行票据市值占基金资产总值比 | REPORTDATE |
| `f_prt_centralbankbilltobond` | 央行票据市值占债券投资市值比 | REPORTDATE |
| `f_prt_centralbankbilltonav` | 央行票据市值占基金资产净值比 | REPORTDATE |
| `f_prt_centralbankbilltonavgrowth` | 央行票据市值占基金资产净值比例增长 |  |
| `f_prt_commercialpapertobond` | 短期融资券市值占债券投资市值比 | REPORTDATE |
| `f_prt_convertiblebond` | 可转债投资市值 | REPORTDATE |
| `f_prt_convertiblebondgrowth` | 可转债市值增长率 |  |
| `f_prt_convertiblebondtoasset` | 可转债市值占基金资产总值比 | REPORTDATE |
| `f_prt_convertiblebondtobond` | 可转债市值占债券投资市值比 | REPORTDATE |
| `f_prt_convertiblebondtonav` | 可转债市值占基金资产净值比 | REPORTDATE |
| `f_prt_convertiblebondtonavgrowth` | 可转债市值占基金资产净值比例增长 |  |
| `f_prt_corporatebond` | 企债投资市值 | REPORTDATE |
| `f_prt_corporatebondgrowth` | 企业债市值增长率 |  |
| `f_prt_corporatebonds` | 企业债市值 | REPORTDATE |
| `f_prt_corporatebondsgrowth` | 企业债市值增长率 | REPORTDATE |
| `f_prt_corporatebondstoasset` | 企业债市值占基金资产总值比 | REPORTDATE |
| `f_prt_corporatebondstobond` | 企业债市值占债券投资市值比 | REPORTDATE |
| `f_prt_corporatebondstonav` | 企业债市值占基金资产净值比 | REPORTDATE |
| `f_prt_corporatebondstonavgrowth` | 企业债市值占基金资产净值比例增长 | REPORTDATE |
| `f_prt_corporatebondtoasset` | 企业债市值占基金资产总值比 | REPORTDATE |
| `f_prt_corporatebondtobond` | 企业债市值占债券投资市值比 | REPORTDATE |
| `f_prt_corporatebondtonav` | 企业债市值占基金资产净值比 | REPORTDATE |
| `f_prt_corporatebondtonavgrowth` | 企业债市值占基金资产净值比例增长 |  |
| `f_prt_countryregioninvestment` | 国家/地区投资市值 | REPORTDATE、ZoneType |
| `f_prt_countryregioninvestmenttonav` | 国家/地区投资市值占基金资产净值比例 | REPORTDATE、ZoneType |
| `f_prt_cptoasset` | 短期融资券市值占基金资产总值比 | REPORTDATE |
| `f_prt_cptonav` | 短期融资券市值占基金资产净值比 |  |
| `f_prt_cpvalue` | 短期融资券市值 | REPORTDATE |
| `f_prt_currency` | 报告期基金资产净值币种 | REPORTDATE |
| `f_prt_financialbond` | 金融债投资市值 | REPORTDATE |
| `f_prt_financialbondgrowth` | 金融债市值增长率 |  |
| `f_prt_financialbondtoasset` | 金融债市值占基金资产总值比 | REPORTDATE |
| `f_prt_financialbondtobond` | 金融债市值占债券投资市值比 | REPORTDATE |
| `f_prt_financialbondtonav` | 金融债市值占基金资产净值比 | REPORTDATE |
| `f_prt_financialbondtonavgrowth` | 金融债市值占基金资产净值比例增长 |  |
| `f_prt_foundleverage` | 基金杠杆率 | REPORTDATE |
| `f_prt_fundcotnachangeratio` | 所属基金公司资产净值合计变动率 |  |
| `f_prt_fundcototalnetassets` | 所属基金公司资产净值合计 |  |
| `f_prt_fundcototalnetassetsranking` | 所属基金公司资产净值合计排名 |  |
| `f_prt_fundnoofbonds` | 重仓债券持有基金数 |  |
| `f_prt_fundnooffunds` | 重仓基金持有基金数 | REPORTDATE |
| `f_prt_fundnoofsec` | 重仓证券持有基金数 | REPORTDATE |
| `f_prt_fundnoofstocks` | 重仓股票持有基金数 |  |
| `f_prt_fundnoofwarrant` | 重仓权证持有基金数 |  |
| `f_prt_fundtoasset` | 基金市值占基金资产总值比 |  |
| `f_prt_fundtonav` | 基金市值占基金资产净值比 |  |
| `f_prt_fundtonavgrowth` | 基金市值占基金资产净值比例增长 |  |
| `f_prt_fundvalue` | 基金投资市值 |  |
| `f_prt_fundvaluegrowth` | 基金市值增长率 |  |
| `f_prt_futcdheld` | 持有期货代码 | REPORTDATE、TopN |
| `f_prt_futnmheld` | 持有期货名称 | REPORTDATE、TopN |
| `f_prt_gbfutures` | 国债期货投资市值 | REPORTDATE |
| `f_prt_gicsindustryvalue` | 分行业投资市值(GICS) | REPORTDATE、IndustryName |
| `f_prt_gicsindustryvaluetonav` | 分行业投资市值占基金资产净值比例(GICS) | REPORTDATE、IndustryName |
| `f_prt_governmentbond` | 国债投资市值 | REPORTDATE |
| `f_prt_governmentbondgrowth` | 国债市值增长率 |  |
| `f_prt_governmentbondtoasset` | 国债市值占基金资产总值比 | REPORTDATE |
| `f_prt_governmentbondtobond` | 国债市值占债券投资市值比 | REPORTDATE |
| `f_prt_governmentbondtonav` | 国债市值占基金资产净值比 | REPORTDATE |
| `f_prt_governmentbondtonavgrowth` | 国债市值占基金资产净值比例增长 |  |
| `f_prt_heavilyheldabstoasset` | 重仓资产支持证券市值占基金资产总值比 | REPORTDATE |
| `f_prt_heavilyheldabstonav` | 重仓资产支持证券市值占基金资产净值比 | REPORTDATE |
| `f_prt_heavilyheldbondsperchange` | 重仓债券涨跌幅 |  |
| `f_prt_heavilyheldbondtoasset` | 重仓债券市值占基金资产总值比 | REPORTDATE |
| `f_prt_heavilyheldbondtobond` | 重仓债券市值占债券投资市值比 | REPORTDATE |
| `f_prt_heavilyheldbondtonav` | 重仓债券市值占基金资产净值比 | REPORTDATE |
| `f_prt_heavilyheldfundperchange` | 重仓基金涨跌幅 | REPORTDATE、SEQ、StartDate、EndDate |
| `f_prt_heavilyheldfundtoasset` | 重仓基金市值占基金资产总值比 | REPORTDATE |
| `f_prt_heavilyheldfundtofund` | 重仓基金市值占基金投资市值比 | REPORTDATE |
| `f_prt_heavilyheldfundtonav` | 重仓基金市值占基金资产净值比 | REPORTDATE |
| `f_prt_heavilyheldsecperchange` | 重仓证券涨跌幅 | REPORTDATE、SEQ、StartDate、EndDate |
| `f_prt_heavilyheldsectoasset` | 重仓证券市值占基金资产总值比 | REPORTDATE |
| `f_prt_heavilyheldsectonav` | 重仓证券市值占基金资产净值比 | REPORTDATE |
| `f_prt_heavilyheldsectosec` | 重仓证券市值占证券投资市值比 | REPORTDATE |
| `f_prt_heavilyheldstocksperchange` | 重仓股涨跌幅 |  |
| `f_prt_heavilyheldstocktoasset` | 重仓股市值占基金资产总值比 | REPORTDATE |
| `f_prt_heavilyheldstocktonav` | 重仓股市值占基金资产净值比 | REPORTDATE |
| `f_prt_heavilyheldstocktostock` | 重仓股市值占股票投资市值比 | REPORTDATE |
| `f_prt_heavilyheldwarrantperchange` | 重仓权证涨跌幅 |  |
| `f_prt_heavilyheldwarranttoasset` | 重仓权证持仓市值占基金资产总值比例 |  |
| `f_prt_heavilyheldwarranttonav` | 重仓权证持仓市值占基金资产净值比例 |  |
| `f_prt_heavilyheldwarranttowarrant` | 重仓权证持仓市值占权证投资市值比例 |  |
| `f_prt_heavyweightreitsfundname` | 重仓REITs基金名称 | REPORTDATE、TopN |
| `f_prt_heavyweightreitsfundquantity` | 重仓REITs基金持仓数量 | REPORTDATE、TopN |
| `f_prt_heavyweightreitsfundtonav` | 重仓REITs基金市值占基金资产净值比 | REPORTDATE、TopN |
| `f_prt_heavyweightreitsfundvalue` | 重仓REITs基金持有市值 | REPORTDATE、TopN |
| `f_prt_hkstocktoasset` | 港股投资市值占基金资产总值比 | REPORTDATE |
| `f_prt_hkstocktonav` | 港股投资市值占基金资产净值比 | REPORTDATE |
| `f_prt_hkstockvalue` | 港股投资市值 | REPORTDATE |
| `f_prt_industrytonavgrowth_citic` | 分行业市值占基金资产净值比增长(中信) | REPORTDATE、IndustryName |
| `f_prt_industrytonavgrowth_sw` | 分行业市值占基金资产净值比增长(申万) | REPORTDATE、IndustryName |
| `f_prt_industrytonavgrowth_sw2021` | 分行业市值占基金资产净值比增长(申万2021) | REPORTDATE、IndustryName |
| `f_prt_industrytonavgrowth_wind` | 分行业市值占基金资产净值比增长(Wind) | REPORTDATE、IndustryName |
| `f_prt_industryvalue_citic` | 分行业投资市值(中信) | REPORTDATE、IndustryName |
| `f_prt_industryvalue_sw` | 分行业投资市值(申万) | REPORTDATE、IndustryName |
| `f_prt_industryvalue_sw2021` | 分行业投资市值(申万2021) | REPORTDATE、IndustryName |
| `f_prt_industryvalue_wind` | 分行业投资市值(Wind) | REPORTDATE、IndustryName |
| `f_prt_industryvaluegrowth_citic` | 分行业市值增长率(中信) | REPORTDATE、IndustryName |
| `f_prt_industryvaluegrowth_sw` | 分行业市值增长率(申万) | REPORTDATE、IndustryName |
| `f_prt_industryvaluegrowth_sw2021` | 分行业市值增长率(申万2021) | REPORTDATE、IndustryName |
| `f_prt_industryvaluegrowth_wind` | 分行业市值增长率(Wind) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetonav_citic` | 分行业投资市值占基金资产净值比(中信) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetonav_sw` | 分行业投资市值占基金资产净值比(申万) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetonav_sw2021` | 分行业投资市值占基金资产净值比(申万2021) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetonav_wind` | 分行业投资市值占基金资产净值比(Wind) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetostockvalue_citic` | 分行业投资市值占股票投资市值比(中信) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetostockvalue_sw` | 分行业投资市值占股票投资市值比(申万) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetostockvalue_sw2021` | 分行业投资市值占股票投资市值比(申万2021) | REPORTDATE、IndustryName |
| `f_prt_industryvaluetostockvalue_wind` | 分行业投资市值占股票投资市值比(Wind) | REPORTDATE、IndustryName |
| `f_prt_localgov` | 地方政府债市值 | REPORTDATE |
| `f_prt_localgovtoasset` | 地方政府债市值占基金资产总值比 | REPORTDATE |
| `f_prt_localgovtobond` | 地方政府债市值占债券投资净值比 | REPORTDATE |
| `f_prt_localgovtonav` | 地方政府债市值占基金资产净值比 | REPORTDATE |
| `f_prt_mergednavornot` | 资产净值是否为合并数据 |  |
| `f_prt_mergednavornot1` | 资产净值是否为合并数据 | REPORTDATE |
| `f_prt_mktvalfutheld` | 持有期货市值 | REPORTDATE、TopN |
| `f_prt_mmitonav` | 货币市场工具市值占基金资产净值比 | REPORTDATE |
| `f_prt_mmivalue` | 货币市场工具市值 | REPORTDATE |
| `f_prt_mtntoasset` | 中期票据占基金资产总值比 | REPORTDATE |
| `f_prt_mtntobond` | 中期票据市值占债券市值比 | REPORTDATE |
| `f_prt_mtntonav` | 中期票据市值占基金资产净值比 |  |
| `f_prt_mtnvalue` | 中期票据市值 | REPORTDATE |
| `f_prt_munibondgrowth` | 地方政府债市值增长率 | REPORTDATE |
| `f_prt_munibondtonavgrowth` | 地方政府债市值占基金资产净值比例增长 | REPORTDATE |
| `f_prt_navtoasset` | 基金净值占基金资产总值比 | REPORTDATE |
| `f_prt_ncdbycreditrating` | 按信用评级的同业存单投资市值 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_ncdbycreditratingtonav` | 按信用评级的同业存单投资占基金资产净值比 | REPORTDATE、CreditRatingType、CalcType |
| `f_prt_ncdtobond` | 同业存单市值占债券投资市值比 | REPORTDATE |
| `f_prt_netasset` | 基金资产净值 | REPORTDATE |
| `f_prt_netassetchange` | 基金资产净值变动 |  |
| `f_prt_netassetchangeratio` | 基金资产净值变动率 |  |
| `f_prt_nonmoneynetassets` | 所属基金公司资产净值合计(非货币) | REPORTDATE |
| `f_prt_other` | 其他资产 | REPORTDATE |
| `f_prt_otherbond` | 其他债券市值 | REPORTDATE |
| `f_prt_otherbondtonav` | 其他债券市值占基金资产净值比 | REPORTDATE |
| `f_prt_othertoasset` | 其他资产占基金资产总值比 | REPORTDATE |
| `f_prt_othertonav` | 其他资产占基金资产净值比 | REPORTDATE |
| `f_prt_othertonavgrowth` | 其他资产市值占基金资产净值比例增长 |  |
| `f_prt_othervaluegrowth` | 其他资产市值增长率 |  |
| `f_prt_pcf_moddur` | PCF中债修正久期 | TRADEDATE |
| `f_prt_pfbtoasset` | 政策性金融债市值占基金资产总值比 | REPORTDATE |
| `f_prt_pfbtobond` | 政策性金融债占债券投资市值比 | REPORTDATE |
| `f_prt_pfbtonav` | 政策性金融债市值占基金资产净值比 | REPORTDATE |
| `f_prt_pfbvalue` | 政策性金融债市值 | REPORTDATE |
| `f_prt_qdii_countryregioninvestment` | 国家/地区投资市值(QDII) |  |
| `f_prt_qdii_countryregioninvestmenttonav` | 国家/地区投资市值占基金资产净值比例(QDII) |  |
| `f_prt_qdii_gicsindustryvalue` | 分行业投资市值(QDII) |  |
| `f_prt_qdii_gicsindustryvaluetonav` | 分行业投资市值占基金资产净值比例(QDII) |  |
| `f_prt_qdii_topgicsindustryvalue` | 重仓行业投资市值(QDII) |  |
| `f_prt_qdii_topgicsindustryvaluetonav` | 重仓行业投资市值占基金资产净值比例(QDII) |  |
| `f_prt_qdii_topholdingcountry` | 重仓证券所属国家(QDII) |  |
| `f_prt_qdii_topholdinglistingplace` | 重仓证券上市地点(QDII) |  |
| `f_prt_qdii_topindustryname` | 重仓行业名称(QDII) |  |
| `f_prt_qdii_topposition` | 重仓持仓数量(QDII) | REPORTDATE |
| `f_prt_qdii_toppositionvalue` | 重仓持仓市值(QDII) |  |
| `f_prt_qdii_toppositionvaluechanging` | 重仓持仓市值变化(QDII) |  |
| `f_prt_qdii_toppositionvaluetonav` | 重仓持仓市值占基金资产净值比例(QDII) |  |
| `f_prt_qdii_topsecuritiesname` | 重仓证券名称(QDII) |  |
| `f_prt_qdii_topsecuritiessymbol` | 重仓证券代码(QDII) |  |
| `f_prt_qdii_topsecuritiestype` | 重仓证券类型(QDII) |  |
| `f_prt_qdii_topsecuritieswindcode` | 重仓证券Wind代码(QDII) | REPORTDATE |
| `f_prt_qtyfutheld` | 持有期货数量 | REPORTDATE、TopN |
| `f_prt_reverserepo` | 买入返售金融资产 | REPORTDATE |
| `f_prt_reverserepotonav` | 买入返售证券占基金资产净值比例 | REPORTDATE |
| `f_prt_seclendingvalue` | 转融通证券出借业务市值 | REPORTDATE |
| `f_prt_seclendingvaluetoasset` | 转融通证券出借业务市值占基金资产总值比 | REPORTDATE |
| `f_prt_seclendingvaluetonav` | 转融通证券出借业务市值占基金资产净值比 | REPORTDATE |
| `f_prt_sellstockincome` | 报告期卖出股票总收入(新增),f_prt_buystockcost | REPORTDATE |
| `f_prt_sharenum_stkhldgstyle` | 报告期不同持仓风格股票只数 | REPORTDATE、StyleType |
| `f_prt_sifutures` | 股指期货投资市值 | REPORTDATE |
| `f_prt_stockholding` | 报告期末持有股票个数(中报、年报) | REPORTDATE |
| `f_prt_stockinvestmentactivity` | 股票投资活跃度(%) | REPORTDATE |
| `f_prt_stocktoasset` | 股票市值占基金资产总值比 | REPORTDATE |
| `f_prt_stocktonav` | 股票市值占基金资产净值比 | REPORTDATE |
| `f_prt_stocktonav_activeinvest` | 积极投资股票市值占基金资产净值比 | REPORTDATE |
| `f_prt_stocktonav_passiveinvest` | 指数投资股票市值占基金资产净值比 | REPORTDATE |
| `f_prt_stocktonavgrowth` | 股票市值占基金资产净值比例增长 |  |
| `f_prt_stockvalue` | 股票投资市值 | REPORTDATE |
| `f_prt_stockvalue_activeinvest` | 积极投资股票市值 | REPORTDATE |
| `f_prt_stockvalue_holdingindustrymktvalue` | 所属基金公司重仓行业市值 |  |
| `f_prt_stockvalue_holdingindustrymktvalue2` | 所属基金公司重仓行业市值 |  |
| `f_prt_stockvalue_industry` | 股票投资市值(分行业) | REPORTDATE、TYPE |
| `f_prt_stockvalue_industry2` | 分行业投资市值 |  |
| `f_prt_stockvalue_industrytoasset` | 分行业市值占基金资产总值比 | REPORTDATE |
| `f_prt_stockvalue_industrytoasset2` | 分行业市值占基金资产总值比 |  |
| `f_prt_stockvalue_industrytonav` | 分行业市值占基金资产净值比 | REPORTDATE |
| `f_prt_stockvalue_industrytonav2` | 分行业市值占基金资产净值比 |  |
| `f_prt_stockvalue_industrytonavgrowth` | 分行业市值占基金资产净值比增长 |  |
| `f_prt_stockvalue_industrytonavgrowth2` | 分行业市值占基金资产净值比增长 |  |
| `f_prt_stockvalue_industrytostock` | 分行业市值占股票投资市值比 | REPORTDATE |
| `f_prt_stockvalue_industrytostock2` | 分行业市值占股票投资市值比 |  |
| `f_prt_stockvalue_industryvaluegrowth` | 分行业市值增长率 |  |
| `f_prt_stockvalue_industryvaluegrowth2` | 分行业市值增长率 |  |
| `f_prt_stockvalue_passiveinvest` | 指数投资股票市值 | REPORTDATE |
| `f_prt_stockvalue_topindexpercentchange` | 重仓行业指数涨跌幅 |  |
| `f_prt_stockvalue_topindustryname` | 重仓行业名称 |  |
| `f_prt_stockvalue_topindustryname2` | 重仓行业名称 |  |
| `f_prt_stockvalue_topindustrysymbol` | 重仓行业代码 |  |
| `f_prt_stockvalue_topindustrysymbol2` | 重仓行业代码 |  |
| `f_prt_stockvalue_topindustrytoasset` | 重仓行业市值占基金资产总值比 |  |
| `f_prt_stockvalue_topindustrytoasset2` | 重仓行业市值占基金资产总值比 |  |
| `f_prt_stockvalue_topindustrytonav` | 重仓行业市值占基金资产净值比 |  |
| `f_prt_stockvalue_topindustrytonav2` | 重仓行业市值占基金资产净值比 |  |
| `f_prt_stockvalue_topindustrytostock` | 重仓行业市值占股票投资市值比 |  |
| `f_prt_stockvalue_topindustrytostock2` | 重仓行业市值占股票投资市值比 |  |
| `f_prt_stockvalue_topindustryvalue` | 重仓行业市值 |  |
| `f_prt_stockvalue_topindustryvalue2` | 重仓行业市值 |  |
| `f_prt_stockvaluegrowth` | 股票市值增长率 |  |
| `f_prt_stockvolume` | 基金成交股票金额(合计) | REPORTDATE |
| `f_prt_stockvolumebybroker` | 股票成交金额(分券商明细) | REPORTDATE |
| `f_prt_tamr` | 资产支持证券市值占债券投资市值比 | REPORTDATE |
| `f_prt_top10name_sw2021` | 前十大重仓股行业名称(申万2021) | REPORTDATE、TopN |
| `f_prt_top10ratio_sw2021` | 前十大重仓股行业占基金净值比(申万2021) | REPORTDATE、TopN |
| `f_prt_top5tobond` | 前5名重仓债券市值合计占债券投资市值比(新增) | D |
| `f_prt_top5tonav` | 前5名重仓债券市值合计占基金资产净值比 | D |
| `f_prt_topabsholdingchanging` | 重仓资产支持证券持仓变动 | REPORTDATE |
| `f_prt_topabsname` | 重仓资产支持证券名称 | REPORTDATE |
| `f_prt_topabsquantity` | 重仓资产支持证券持仓数量 | REPORTDATE |
| `f_prt_topabssymbol` | 重仓资产支持证券代码 | REPORTDATE |
| `f_prt_topabsvalue` | 重仓资产支持证券持有市值 | REPORTDATE |
| `f_prt_topabswindcode` | 重仓资产支持证券Wind代码 | REPORTDATE |
| `f_prt_topbondcode` | 重仓债券代码 | REPORTDATE |
| `f_prt_topbondholdingchanging` | 重仓债券持仓变动 | REPORTDATE |
| `f_prt_topbondname` | 重仓债券名称 | REPORTDATE |
| `f_prt_topbondquantity` | 重仓债券持仓数量 | REPORTDATE |
| `f_prt_topbondsymbol` | 重仓债券代码 |  |
| `f_prt_topbondvalue` | 重仓债券市值 | REPORTDATE |
| `f_prt_topbondwindcode` | 重仓债券Wind代码 | REPORTDATE |
| `f_prt_topfundcode` | 重仓基金代码 | REPORTDATE |
| `f_prt_topfundholdingchanging` | 重仓基金持仓变动 | REPORTDATE |
| `f_prt_topfundname` | 重仓基金名称 | REPORTDATE |
| `f_prt_topfundquantity` | 重仓基金持仓数量 | REPORTDATE |
| `f_prt_topfundtofund` | 前N名重仓基金市值合计占基金投资市值比 | REPORTDATE |
| `f_prt_topfundvalue` | 重仓基金持有市值 | REPORTDATE |
| `f_prt_topfundwindcode` | 重仓基金Wind代码 | REPORTDATE |
| `f_prt_topgicsindustryname` | 重仓行业名称(GICS) | REPORTDATE、TopN |
| `f_prt_topgicsindustryvalue` | 重仓行业投资市值(GICS) | REPORTDATE、TopN |
| `f_prt_topgicsindustryvaluetonav` | 重仓行业投资市值占基金资产净值比例(GICS) | REPORTDATE、TopN |
| `f_prt_topindustryname_citic` | 重仓行业名称(中信) | REPORTDATE、TopN |
| `f_prt_topindustryname_sw` | 重仓行业名称(申万) | REPORTDATE、TopN |
| `f_prt_topindustryname_sw2021` | 重仓行业名称(申万2021) | REPORTDATE、TopN |
| `f_prt_topindustryname_wind` | 重仓行业名称(Wind) | REPORTDATE、TopN |
| `f_prt_topindustryvalue_citic` | 重仓行业投资市值(中信) | REPORTDATE、TopN |
| `f_prt_topindustryvalue_sw` | 重仓行业投资市值(申万) | REPORTDATE、TopN |
| `f_prt_topindustryvalue_sw2021` | 重仓行业投资市值(申万2021) | REPORTDATE、TopN |
| `f_prt_topindustryvalue_wind` | 重仓行业投资市值(Wind) | REPORTDATE、TopN |
| `f_prt_topindustryvaluetonav_citic` | 重仓行业投资市值占基金资产净值比(中信) | REPORTDATE、TopN |
| `f_prt_topindustryvaluetonav_sw` | 重仓行业投资市值占基金资产净值比(申万) | REPORTDATE、TopN |
| `f_prt_topindustryvaluetonav_sw2021` | 重仓行业投资市值占基金资产净值比(申万2021) | REPORTDATE、TopN |
| `f_prt_topindustryvaluetonav_wind` | 重仓行业投资市值占基金资产净值比(Wind) | REPORTDATE、TopN |
| `f_prt_topnfundtonav` | 前N名重仓基金市值合计占基金资产净值比 | REPORTDATE |
| `f_prt_topnsectonav` | 前N名重仓证券市值合计占基金资产净值比 | REPORTDATE |
| `f_prt_topnstocktonav` | 前N名重仓股票市值合计占基金资产净值比 | REPORTDATE |
| `f_prt_topnstocktostock` | 前N名重仓股票市值合计占股票投资市值比 | REPORTDATE |
| `f_prt_topoptionamount` | 持有期权数量 | REPORTDATE、TopN |
| `f_prt_topoptioncode` | 持有期权代码 | REPORTDATE、TopN |
| `f_prt_topoptionname` | 持有期权名称 | REPORTDATE、TopN |
| `f_prt_topoptionvalue` | 持有期权市值 | REPORTDATE、TopN |
| `f_prt_topporportiontocirculating` | 重仓权证持有量占流通量比例 |  |
| `f_prt_topproportiontofloating` | 重仓股持仓占流通股比例 |  |
| `f_prt_topsectortostock_sw2021` | 重仓行业市值占股票投资市值比(申万2021) | REPORTDATE、TopN |
| `f_prt_topsectosec` | 前N名重仓证券市值合计占证券投资市值比 | REPORTDATE |
| `f_prt_topsecuritiecode` | 重仓证券代码 | REPORTDATE |
| `f_prt_topsecuritieholdingchanging` | 重仓证券持仓变动 | REPORTDATE |
| `f_prt_topsecuritiename` | 重仓证券名称 | REPORTDATE |
| `f_prt_topsecuritiequantity` | 重仓证券持仓数量 | REPORTDATE |
| `f_prt_topsecuritietype` | 重仓证券类型 | REPORTDATE |
| `f_prt_topsecuritievalue` | 重仓证券持仓市值 | REPORTDATE |
| `f_prt_topsecuritiewindcode` | 重仓证券Wind代码 | REPORTDATE |
| `f_prt_topspotamount` | 持有现货数量 | REPORTDATE、TopN |
| `f_prt_topspotcode` | 持有现货代码 | REPORTDATE、TopN |
| `f_prt_topspotname` | 持有现货名称 | REPORTDATE、TopN |
| `f_prt_topspotvalue` | 持有现货市值 | REPORTDATE、TopN |
| `f_prt_topstockcode` | 重仓股股票代码 | REPORTDATE |
| `f_prt_topstockdate` | 最早重仓时间 | REPORTDATE、TopN |
| `f_prt_topstockheldno` | 重仓股报告期重仓次数 | REPORTDATE |
| `f_prt_topstockholdingchanging` | 重仓股持仓变动 |  |
| `f_prt_topstockname` | 重仓股股票名称 | REPORTDATE |
| `f_prt_topstockquantity` | 重仓股持股数量 | REPORTDATE |
| `f_prt_topstockvalue` | 重仓股持股市值 | REPORTDATE |
| `f_prt_topstockwindcode` | 重仓股股票Wind代码 | REPORTDATE |
| `f_prt_topwarrantholdingchanging` | 重仓权证持仓变动 | REPORTDATE |
| `f_prt_topwarrantname` | 重仓权证名称 |  |
| `f_prt_topwarrantquantity` | 重仓权证持仓数量 | REPORTDATE |
| `f_prt_topwarrantsymbol` | 重仓权证代码 |  |
| `f_prt_topwarrantvalue` | 重仓权证持仓市值 |  |
| `f_prt_topwarrantwindcode` | 重仓权证Wind代码 | REPORTDATE |
| `f_prt_totalasset` | 基金资产总值 | REPORTDATE |
| `f_prt_totalassetchange` | 基金资产总值变动 |  |
| `f_prt_totalassetchangeratio` | 基金资产总值变动率 |  |
| `f_prt_warranttoasset` | 权证市值占基金资产总值比 | REPORTDATE |
| `f_prt_warranttonav` | 权证市值占基金资产净值比 | REPORTDATE |
| `f_prt_warranttonavgrowth` | 权证市值占基金资产净值比例增长 |  |
| `f_prt_warrantvalue` | 权证投资市值 | REPORTDATE |
| `f_prt_warrantvaluegrowth` | 权证市值增长率 |  |
| `f_qanal_accumulatednavreturn` | 季度累计基金份额净值增长率 |  |
| `f_qanal_avgnetincomeperunit` | 加权平均基金份额本期利润(新增) | REPORTDATE |
| `f_qanal_avgunitincome` | 加权平均基金份额本期净收益 | REPORTDATE |
| `f_qanal_benchdevreturn` | 季度超额收益率 |  |
| `f_qanal_benchreturn` | 季度业绩比较基准收益率 |  |
| `f_qanal_decutednetincome` | 本期利润扣减公允价值变动损益后的净额(新增) | REPORTDATE |
| `f_qanal_income` | 季度基金利润(新增) | REPORTDATE |
| `f_qanal_nav` | 季度末基金份额净值 | REPORTDATE |
| `f_qanal_navreturn` | 季度基金份额净值增长率 |  |
| `f_qanal_netasset` | 季度末基金资产净值 | REPORTDATE |
| `f_qanal_reits_acr` | 单季度.平均合同租金 | REPORTDATE |
| `f_qanal_reits_actdist` | 单季度.实际分配金额(本期) | REPORTDATE |
| `f_qanal_reits_acu` | 单季度.平均产能利用率 | REPORTDATE |
| `f_qanal_reits_adjusteddecrease` | 单季度.调减项合计 | REPORTDATE |
| `f_qanal_reits_adjustedincrease` | 单季度.调增项合计 | REPORTDATE |
| `f_qanal_reits_adt` | 单季度.日均通行费 | REPORTDATE |
| `f_qanal_reits_advf` | 单季度.日均车流量 | REPORTDATE |
| `f_qanal_reits_ae` | 单季度.营业成本及费用-行政经费 | REPORTDATE |
| `f_qanal_reits_ai` | 单季度.营业收入-综合管理服务收入 | REPORTDATE |
| `f_qanal_reits_ala` | 单季度.实际出租面积 | REPORTDATE |
| `f_qanal_reits_amr` | 单季度.平均月租金 | REPORTDATE |
| `f_qanal_reits_aofa` | 单季度.调增减项-金融资产相关调整 | REPORTDATE |
| `f_qanal_reits_ast` | 单季度.污水平均处理量 | REPORTDATE |
| `f_qanal_reits_bcat` | 单季度.调增减项-期初现金及交易所国债 | REPORTDATE |
| `f_qanal_reits_bco` | 单季度.调增减项-期初现金余额 | REPORTDATE |
| `f_qanal_reits_bcr` | 单季度.预算完成率 | REPORTDATE |
| `f_qanal_reits_btas` | 单季度.营业成本及费用-营业税金及附加 | REPORTDATE |
| `f_qanal_reits_cashflowbalance` | 单季度.经营活动现金流量余额 | REPORTDATE |
| `f_qanal_reits_cashrate` | 单季度.现金分派率 | REPORTDATE |
| `f_qanal_reits_ce` | 单季度.营业成本及费用-资本性支出 | REPORTDATE |
| `f_qanal_reits_ceopp` | 单季度.调增减项-购买基础设施项目等资本性支出 | REPORTDATE |
| `f_qanal_reits_cop` | 单季度.调增减项-应付项目的变动 | REPORTDATE |
| `f_qanal_reits_cor` | 单季度.调增减项-应收项目的变动 | REPORTDATE |
| `f_qanal_reits_corftp` | 单季度.调增减项-偿还借款本金支付的现金 | REPORTDATE |
| `f_qanal_reits_crap` | 单季度.调增减项-应收和应付项目的变动 | REPORTDATE |
| `f_qanal_reits_crost` | 单季度.污水处理服务费回收率 | REPORTDATE |
| `f_qanal_reits_cumactdist` | 单季度.实际分配金额(本年累计) | REPORTDATE |
| `f_qanal_reits_cumdistributedamounts` | 单季度.可供分配金额(本年累计) | REPORTDATE |
| `f_qanal_reits_curra` | 单季度.流动比率 | REPORTDATE |
| `f_qanal_reits_cwt` | 单季度.处理生活垃圾 | REPORTDATE |
| `f_qanal_reits_cwti` | 单季度.营业收入-生活垃圾处置收入 | REPORTDATE |
| `f_qanal_reits_daa` | 单季度.营业成本及费用-折旧及摊销 | REPORTDATE |
| `f_qanal_reits_daorei` | 单季度.营业成本及费用-投资性房地产折旧及摊销 | REPORTDATE |
| `f_qanal_reits_depreciationandamortization` | 单季度.折旧和摊销 | REPORTDATE |
| `f_qanal_reits_distributedamounts` | 单季度.可供分配金额(本期) | REPORTDATE |
| `f_qanal_reits_doi` | 单季度.调增减项-存货的减少 | REPORTDATE |
| `f_qanal_reits_domf` | 单季度.减免管理费 | REPORTDATE |
| `f_qanal_reits_ebit` | 单季度税息折旧及摊销前利润 | REPORTDATE |
| `f_qanal_reits_ebitdap` | 单季度.息税折旧摊销前利润率 | REPORTDATE |
| `f_qanal_reits_ebitdp` | 单季度.息税折旧前净利率 | REPORTDATE |
| `f_qanal_reits_ebol` | 单季度.调增减项-期末负债余额 | REPORTDATE |
| `f_qanal_reits_ec` | 单季度.营业成本及费用-员工成本 | REPORTDATE |
| `f_qanal_reits_ela` | 单季度.期末出租面积 | REPORTDATE |
| `f_qanal_reits_eor` | 单季度.期末出租率 | REPORTDATE |
| `f_qanal_reits_eta` | 单季度.期末租户家数 | REPORTDATE |
| `f_qanal_reits_fc` | 单季度.营业成本及费用-财务费用 | REPORTDATE |
| `f_qanal_reits_fissue` | 单季度.调增减项-基础设施基金发行份额募集的资金 | REPORTDATE |
| `f_qanal_reits_fl` | 单季度.全长 | REPORTDATE |
| `f_qanal_reits_frrp` | 单季度.调增减项-未来合理相关支出预留 | REPORTDATE |
| `f_qanal_reits_fs` | 单季度.建筑面积 | REPORTDATE |
| `f_qanal_reits_gpm` | 单季度.毛利率 | REPORTDATE |
| `f_qanal_reits_ic` | 单季度.营业成本及费用-利息支出 | REPORTDATE |
| `f_qanal_reits_income` | 单季度.本期收入 | REPORTDATE |
| `f_qanal_reits_interestcost` | 单季度.利息支出 | REPORTDATE |
| `f_qanal_reits_kwt` | 单季度.处理厨余垃圾 | REPORTDATE |
| `f_qanal_reits_la` | 单季度.可出租面积 | REPORTDATE |
| `f_qanal_reits_lc` | 单季度.消耗LNG | REPORTDATE |
| `f_qanal_reits_lr` | 单季度.营业收入-渗滤液收入 | REPORTDATE |
| `f_qanal_reits_lwti` | 单季度.营业收入-餐厨垃圾收运及处置 | REPORTDATE |
| `f_qanal_reits_mbc` | 单季度.营业成本及费用-主营业务成本 | REPORTDATE |
| `f_qanal_reits_mc` | 单季度.营业成本及费用-管理人报酬 | REPORTDATE |
| `f_qanal_reits_me` | 单季度.营业成本及费用-维修维护费 | REPORTDATE |
| `f_qanal_reits_mf` | 单季度.营业成本及费用-管理费用 | REPORTDATE |
| `f_qanal_reits_netprofit` | 单季度.本期净利润 | REPORTDATE |
| `f_qanal_reits_npm` | 单季度.净利率 | REPORTDATE |
| `f_qanal_reits_npmincf` | 单季度.净利率(不扣除基金层面提取部分) | REPORTDATE |
| `f_qanal_reits_oa` | 单季度.调增减项-其他调整项 | REPORTDATE |
| `f_qanal_reits_oc` | 单季度.营业成本及费用-营运经费 | REPORTDATE |
| `f_qanal_reits_oeffrp` | 单季度.调增减项-未来合理期间内的运营费用 | REPORTDATE |
| `f_qanal_reits_oge` | 单季度.上网电量 | REPORTDATE |
| `f_qanal_reits_oi` | 单季度.营业收入-其他收入 | REPORTDATE |
| `f_qanal_reits_omc` | 单季度.营业成本及费用-运营管理成本 | REPORTDATE |
| `f_qanal_reits_ooc` | 单季度.营业成本及费用-其他运营成本 | REPORTDATE |
| `f_qanal_reits_operatingcost` | 单季度.营业成本 | REPORTDATE |
| `f_qanal_reits_operatingrevenue` | 单季度.营业收入 | REPORTDATE |
| `f_qanal_reits_or` | 单季度.出租率 | REPORTDATE |
| `f_qanal_reits_ose` | 单季度.营业成本及费用-外包服务支出 | REPORTDATE |
| `f_qanal_reits_otherc` | 单季度.营业成本及费用-其他成本/费用 | REPORTDATE |
| `f_qanal_reits_pc` | 单季度.营业成本及费用-物业成本 | REPORTDATE |
| `f_qanal_reits_pda` | 单季度.调增减项-前期可供分配金额 | REPORTDATE |
| `f_qanal_reits_pgi` | 单季度.营业收入-发电收入 | REPORTDATE |
| `f_qanal_reits_pi` | 单季度.营业收入-停车费收入 | REPORTDATE |
| `f_qanal_reits_pit` | 单季度.调增减项-支付的利息及所得税费用 | REPORTDATE |
| `f_qanal_reits_plfc` | 单季度.调增减项-基础设施项目资产的公允价值变动损益 | REPORTDATE |
| `f_qanal_reits_pme` | 单季度.营业成本及费用-工程养护成本 | REPORTDATE |
| `f_qanal_reits_pol` | 单季度.调增减项-取得借款收到的本金 | REPORTDATE |
| `f_qanal_reits_pri` | 单季度.营业收入-物业收入 | REPORTDATE |
| `f_qanal_reits_quira` | 单季度.速动比率 | REPORTDATE |
| `f_qanal_reits_rc` | 单季度.调增减项-预留工程款 | REPORTDATE |
| `f_qanal_reits_rc2` | 单季度.营业成本-租赁成本 | REPORTDATE |
| `f_qanal_reits_rce` | 单季度.调增减项-预留资本性支出 | REPORTDATE |
| `f_qanal_reits_rcr` | 单季度.租金收缴率 | REPORTDATE |
| `f_qanal_reits_rd` | 单季度.减免租金 | REPORTDATE |
| `f_qanal_reits_ri` | 单季度.营业收入-租金收入 | REPORTDATE |
| `f_qanal_reits_rm` | 单季度.营业成本及费用-原材料(燃气费) | REPORTDATE |
| `f_qanal_reits_roe` | 单季度.调增减项-预留运营费用 | REPORTDATE |
| `f_qanal_reits_roefny` | 单季度.调增减项-预留下一年度运营费用 | REPORTDATE |
| `f_qanal_reits_rwi` | 单季度.营业收入-中水收入 | REPORTDATE |
| `f_qanal_reits_sae` | 单季度.营业成本及费用-施救费 | REPORTDATE |
| `f_qanal_reits_seost` | 单季度.污水处理服务费 | REPORTDATE |
| `f_qanal_reits_slti` | 单季度.营业收入-污泥收入 | REPORTDATE |
| `f_qanal_reits_sme` | 单季度.营业成本及费用-系统维护成本 | REPORTDATE |
| `f_qanal_reits_stc` | 单季度.营业成本及费用-污泥处理成本 | REPORTDATE |
| `f_qanal_reits_sti` | 单季度.营业收入-污水处理收入 | REPORTDATE |
| `f_qanal_reits_taxcost` | 单季度.所得税费用 | REPORTDATE |
| `f_qanal_reits_ti` | 单季度.营业收入-通行费收入 | REPORTDATE |
| `f_qanal_reits_tpce` | 单季度.调增减项-本期/本年资本性支出 | REPORTDATE |
| `f_qanal_reits_tst` | 单季度.污水处理总量 | REPORTDATE |
| `f_qanal_reits_uf` | 单季度.调增减项-不可预见费用 | REPORTDATE |
| `f_qanal_reits_unitactdist` | 单季度.单位实际分配金额(本期) | REPORTDATE |
| `f_qanal_reits_unitcumactdist` | 单季度.单位实际分配金额(本年累计) | REPORTDATE |
| `f_qanal_reits_unitcumdistributedamounts` | 单季度.单位可供分配金额(本年累计) | REPORTDATE |
| `f_qanal_reits_unitdistributedamounts` | 单季度.单位可供分配金额(本期) | REPORTDATE |
| `f_qanal_reits_va` | 单季度.车辆总数 | REPORTDATE |
| `f_qanal_reits_wqr` | 单季度.水质达标率 | REPORTDATE |
| `f_qanal_reits_wtc` | 单季度.营业成本及费用-污水处理成本 | REPORTDATE |
| `f_qanal_stdbenchdevreturn` | 季度超额收益率标准差 |  |
| `f_qanal_stdbenchreturn` | 季度业绩比较基准收益率标准差 |  |
| `f_qanal_stdnavreturn` | 季度基金份额净值增长率标准差 |  |
| `f_qanal_totalincome` | 单季度.基金利润(合计) | REPORTDATE |
| `f_quot_benchreturn` | 业绩比较基准增长率(新增) | TD1、TD2 |
| `f_rating_1y` | 基金1年评级 | ORG、Y、M |
| `f_rating_2y` | 基金2年评级 | ORG、Y、M |
| `f_rating_3y` | 基金3年评级 | ORG、Y、M |
| `f_rating_5y` | 基金5年评级 | ORG、Y、M |
| `f_rating_diag` | Wind基金诊断综合得分 | RatingPeriod、Year、Month |
| `f_rating_haitong3y` | 海通3年评级 | D、M |
| `f_rating_latestmonth` | 最新评级月份 | RATINGAGENCY、RatingInterval |
| `f_rating_lip1ycon` | 理柏1年评级(稳定回报)(新增) | D、M |
| `f_rating_lip1yexp` | 理柏1年评级(费用)(新增) | D、M |
| `f_rating_lip1ypre` | 理柏1年评级(保本能力)(新增) | D、M |
| `f_rating_lip1ytotalret` | 理柏1年评级(总回报)(新增) | D、M |
| `f_rating_lip2ycon` | 理柏2年评级(稳定回报)(新增) | D、M |
| `f_rating_lip2yexp` | 理柏2年评级(费用)(新增) | D、M |
| `f_rating_lip2yrre` | 理柏2年评级(保本能力)(新增) | D、M |
| `f_rating_lip2ytotalret` | 理柏2年评级(总回报)(新增) | D、M |
| `f_rating_lip3yconsret` | 理柏3年评级(稳定回报)(新增) | D、M |
| `f_rating_lip3yexp` | 理柏3年评级(费用)(新增) | D、M |
| `f_rating_lip3ypre` | 理柏3年评级(保本能力)(新增) | D、M |
| `f_rating_lip3ytotalret` | 理柏3年评级(总回报)(新增) | D、M |
| `f_rating_marketavg` | 市场综合3年评级 |  |
| `f_rating_mstar1y` | 晨星1年评级(新增) | D、M |
| `f_rating_mstar2y` | 晨星2年评级(新增) | D、M |
| `f_rating_mstar3y` | 晨星3年评级(新增) | D、M |
| `f_rating_mstar5y` | 晨星5年评级 | D、M |
| `f_rating_shanghaioverall3y` | 上海证券3年评级（综合评级） | D、M |
| `f_rating_shanghaioverall5y` | 上海证券5年评级（综合评级） | D、M |
| `f_rating_shanghaisharpe3y` | 上海证券3年评级（夏普比率） | D、M |
| `f_rating_shanghaisharpe5y` | 上海证券5年评级（夏普比率） | D、M |
| `f_rating_shanghaistocking3y` | 上海证券3年评级（选证能力） | D、M |
| `f_rating_shanghaistocking5y` | 上海证券5年评级（选证能力） | D、M |
| `f_rating_shanghaitiming3y` | 上海证券3年评级（择时能力） | D、M |
| `f_rating_shanghaitiming5y` | 上海证券5年评级（择时能力） | D、M |
| `f_rating_wind1y` | Wind1年评级(新增) | D、M |
| `f_rating_wind2y` | Wind2年评级(新增) | D、M |
| `f_rating_wind3y` | Wind3年评级(新增) | D、M |
| `f_rating_wind5y` | Wind5年评级 | D、M |
| `f_rating_windavg` | Wind综合评级(新增) | D、M |
| `f_rating_yinhe1y` | 银河1年评级(新增) | D、M |
| `f_rating_yinhe2y` | 银河2年评级(新增) | D、M |
| `f_rating_yinhe3y` | 银河3年评级(新增) | D、M |
| `f_rating_zhaoshang3y` | 招商3年评级 | D、M |
| `f_reits_cbval` | 中债REITs估值 | TRADEDATE |
| `f_reits_cbvalyield` | 中债REITs估值收益率 | TRADEDATE |
| `f_reits_cmfee` | 客户维护费 | REPORTDATE |
| `f_reits_csabsvaluation` | 中证REITs-ABS估值 | TRADEDATE |
| `f_reits_csabsvaluationyield` | 中证REITs-ABS估值收益率 | TRADEDATE |
| `f_reits_csvaluation` | 中证REITs估值 | TRADEDATE |
| `f_reits_cumexpshare` | 累计扩募发售份额 | TRADEDATE |
| `f_reits_cumexpvalue` | 累计扩募发售金额 | TRADEDATE |
| `f_reits_distributableprofityield` | 派息率TTM | TRADEDATE |
| `f_reits_distributionratio` | 年化派息率 | TRADEDATE |
| `f_reits_dividendyield` | 股息率TTM | TRADEDATE |
| `f_reits_explistd` | 限售份额预计上市流通日期 | TRADEDATE、TopN |
| `f_reits_fixmanagfee` | 固定管理费 | REPORTDATE |
| `f_reits_flomanagfee` | 浮动管理费 | REPORTDATE |
| `f_reits_limliqdisc` | 限售份额流动性折扣 | TRADEDATE、TopN |
| `f_reits_limoption` | 限售份额期权价值 | TRADEDATE、TopN |
| `f_reits_limval` | 限售份额估值 | TRADEDATE、TopN |
| `f_reits_limvol` | 预期限售份额估值波动率 | TRADEDATE、TopN |
| `f_reits_restlimd` | 限售份额剩余限售期 | TRADEDATE、TopN |
| `f_reits_unitdistributableamount` | 近一年单位可供分配金额 | TRADEDATE |
| `f_return` | 区间回报 |  |
| `f_return_10y` | 近10年回报 |  |
| `f_return_1m` | 近1月回报 |  |
| `f_return_1w` | 近1周回报 |  |
| `f_return_1y` | 近1年回报 |  |
| `f_return_20y` | 近20年回报 | Annualize、TRADEDATE |
| `f_return_2w` | 近2周回报 | Annualize、TRADEDATE |
| `f_return_2y` | 近2年回报 |  |
| `f_return_30y` | 近30年回报 | Annualize、TRADEDATE |
| `f_return_3m` | 近3月回报 |  |
| `f_return_3y` | 近3年回报 |  |
| `f_return_5y` | 近5年回报 |  |
| `f_return_6m` | 近6月回报 |  |
| `f_return_m` | 单月度回报 | TRADEDATE |
| `f_return_q` | 单季度回报 | TRADEDATE |
| `f_return_std` | 成立以来回报 |  |
| `f_return_y` | 单年度回报 | TRADEDATE |
| `f_return_ytd` | 今年以来回报 |  |
| `f_risk_alpha` | Alpha(新增) | TD1、TD2 |
| `f_risk_alpha_bm` | Alpha(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod |
| `f_risk_annualintervalyield` | 区间收益率(年化) | StartDate、EndDate |
| `f_risk_annualintervalyield_calc` | 7日年化收益率(计算) | TRADEDATE |
| `f_risk_annualintervalyield_inclph` | 7日年化收益率(含节假日) | TRADEDATE |
| `f_risk_annualintervalyield_tradedate` | 区间收益率(工作日年化) | StartDate、EndDate |
| `f_risk_annualpha` | Alpha(年化) | StartDate、EndDate、CT、CM、UI |
| `f_risk_annualpha_bm` | Alpha(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod |
| `f_risk_annualvolranking` | 年化波动率同类排名 | BEGINDATE、EndDate |
| `f_risk_annuinforatio` | 信息比率(年化) | StartDate、EndDate、CT、CM、NRY、UI |
| `f_risk_annujensen` | Jensen(年化) | StartDate、EndDate、CM、NRY、UI、CT |
| `f_risk_annujensen_bm` | Jensen(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield |
| `f_risk_annusharpe` | Sharpe(年化) | StartDate、EndDate、CT、CM、NRY |
| `f_risk_annusortino` | 索丁诺比率(年化) | StartDate、EndDate、CT、CM、NRY |
| `f_risk_annustdev` | 收益标准差(年化) | StartDate、EndDate、CT、CM |
| `f_risk_annutrackerror` | 跟踪误差(年化) | StartDate、EndDate、CT、CM、UI |
| `f_risk_annutrackerror_index` | 跟踪误差(跟踪指数,年化) | StartDate、EndDate |
| `f_risk_annutreynor` | Treynor(年化) | StartDate、EndDate、CT、CM、NRY、UI |
| `f_risk_annutreynor_bm` | Treynor(年化,业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield |
| `f_risk_avgreturn` | 平均收益率(新增) | TD1、TD2 |
| `f_risk_avgriskreturn` | 平均风险收益率 |  |
| `f_risk_avgtrackdeviation_benchmark` | 区间跟踪偏离度均值(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod |
| `f_risk_avgtrackdeviation_trackindex` | 区间跟踪偏离度均值(跟踪指数) | StartDate、EndDate、CalcTerm、CalcMethod |
| `f_risk_beta` | Beta(新增) | TD1、TD2 |
| `f_risk_beta_bm` | Beta(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod |
| `f_risk_correcoefficient` | 相关系数 | StartDate、EndDate、CT、CM、WINDCODE2 |
| `f_risk_correcoefficient_trackindex` | 相关系数(跟踪指数) | StartDate、EndDate |
| `f_risk_cvar` | 条件VaR | StartDate、EndDate |
| `f_risk_downside` | 回撤(相对前期高点) | TRADEDATE |
| `f_risk_downsiderisk` | 下行风险 |  |
| `f_risk_downsideriskranking` | 下行风险同类排名 | BEGINDATE、EndDate |
| `f_risk_downsidestdev` | 下行标准差(新增) | StartDate、EndDate、CT、CM、TY |
| `f_risk_drawdown` | 区间回撤(相对前期高点) | StartDate、EndDate |
| `f_risk_duration` | 基金组合久期 | REPORTDATE |
| `f_risk_durationupdate` | 基金组合久期(基于利率风险计算) | REPORTDATE |
| `f_risk_gemavgriskreturn` | 几何平均风险收益率 |  |
| `f_risk_gemreturn` | 几何平均收益率(新增) | TD1、TD2 |
| `f_risk_hvar` | 历史VaR | StartDate、EndDate |
| `f_risk_inforatio` | 信息比率(新增) | TD1、TD2 |
| `f_risk_inforatio_trackindex` | 信息比率(跟踪指数) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield |
| `f_risk_inforatioranking` | 信息比率同类排名(新增) | StartDate、EndDate |
| `f_risk_interestsensitivity` | 市场利率敏感性 | REPORTDATE |
| `f_risk_jensen` | Jensen(新增) | TD1、TD2 |
| `f_risk_jensen_bm` | Jensen(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield |
| `f_risk_maxdownside` | 最大回撤 | StartDate、EndDate |
| `f_risk_maxdownside_date` | 最大回撤区间日期 | StartDate、EndDate |
| `f_risk_maxdownside_recoverdays` | 最大回撤恢复天数 | StartDate、EndDate |
| `f_risk_maxupside` | 最大上涨 | StartDate、EndDate |
| `f_risk_navoverbenchannualreturn` | 区间净值超越基准年化收益率 |  |
| `f_risk_nonsysrisk` | 非系统风险(新增) | TD1、TD2 |
| `f_risk_r2` | 可决系数(新增) | TD1、TD2 |
| `f_risk_returnyearly` | 年化收益率(新增) | TD1、TD2 |
| `f_risk_returnyearly_tradedate` | 年化收益率(工作日) | StartDate |
| `f_risk_sharpe` | Sharpe(新增) | TD1、TD2 |
| `f_risk_siml_avgalpha` | Alpha同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgannualpha` | Alpha(年化)同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgannusharpe` | Sharpe(年化)同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgannusortino` | Sortino(年化)同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgbeta` | Beta同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgdownsiderisk` | 下行风险同类平均 | StartDate、EndDate |
| `f_risk_siml_avgmaxdownside` | 最大回撤同类平均 | StartDate、EndDate |
| `f_risk_siml_avgsharpe` | Sharpe同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgsortino` | Sortino同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_siml_avgstdevyearly` | 年化波动率同类平均 | StartDate、EndDate、CalcTerm |
| `f_risk_sortino` | 索丁诺比率 | BEGINDATE、EndDate |
| `f_risk_stdev` | 收益标准差(新增) | TD1、TD2 |
| `f_risk_stdevyearly` | 年化波动率(新增) | TD1、TD2 |
| `f_risk_stock` | 选股能力(新增) | TD1、TD2 |
| `f_risk_stockranking` | 选股能力同类排名(新增) | StartDate、EndDate |
| `f_risk_time` | 选时能力(新增) | TD1、TD2 |
| `f_risk_timeranking` | 选时能力同类排名(新增) | StartDate、EndDate |
| `f_risk_trackdeviation_trackindex` | 日跟踪偏离度(跟踪指数) | TRADEDATE |
| `f_risk_trackerror` | 跟踪误差(新增) | TD1、TD2 |
| `f_risk_trackerror_trackindex` | 跟踪误差(跟踪指数) | StartDate、EndDate |
| `f_risk_trackerrorranking` | 跟踪误差排名 | BEGINDATE、EndDate |
| `f_risk_treynor` | Treynor(新增) | TD1、TD2 |
| `f_risk_treynor_bm` | Treynor(业绩基准) | StartDate、EndDate、CalcTerm、CalcMethod、No_Risk_Yield |
| `f_risk_upsidestdev` | 上行标准差(新增) | StartDate、EndDate、CT、CM、TY |
| `f_sprdinc_redm` | 股票投资收益-赎回差价收入 | REPORTDATE |
| `f_sprdinc_seclend` | 股票投资收益-证券出借差价收入 | REPORTDATE |
| `f_sprdinc_sub` | 股票投资收益-申购差价收入 | REPORTDATE |
| `f_sprdinc_trd` | 股票投资收益-买卖股票差价收入 | REPORTDATE |
| `f_staff_sub_ratio` | 管理人员工认购比例 |  |
| `f_staff_sub_shares` | 管理人员工认购份额 |  |
| `f_stkinv_spread` | 股票投资收益-买卖股票差价收入 | REPORTDATE |
| `f_stkinv_stkamount` | 股票投资收益-卖出股票成交总额 | REPORTDATE |
| `f_stkinv_stkcost` | 股票投资收益-卖出股票成本总额 | REPORTDATE |
| `f_stkinv_transcost` | 股票投资收益-交易费用 | REPORTDATE |
| `f_stm07_bs_reits_allassets` | 资产总计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_alldebt` | 负债合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_allequity` | 所有者权益合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_capitalreserve` | 资本公积金 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_cash` | 货币资金 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_debtequity` | 负债和所有者权益总计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_equity` | 归属于母公司所有者权益合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_liquidasset` | 流动资产合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_liquiddebt` | 流动负债合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_nonliquid` | 非流动资产合计 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_notes` | 应收票据及应收账款 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_otherpayable` | 其他应付款(合计) | REPORTDATE、TYPE |
| `f_stm07_bs_reits_others` | 其他应收款(合计) | REPORTDATE、TYPE |
| `f_stm07_bs_reits_paidin` | 实收资本(或股本) | REPORTDATE、TYPE |
| `f_stm07_bs_reits_payable` | 应付票据及应付账款 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_realestate` | 投资性房地产 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_recipts` | 预收款项 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_surplus` | 盈余公积金 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_tax` | 应交税费 | REPORTDATE、TYPE |
| `f_stm07_bs_reits_undistrirprofit` | 未分配利润 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_buycash` | 购买商品、接受劳务支付的现金 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_cashadd` | 现金及现金等价物净增加额 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_financecashin` | 筹资活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_financecashout` | 筹资活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_financenetcash` | 筹资活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_investcashin` | 投资活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_investcashout` | 投资活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_investnetcash` | 投资活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_opercashin` | 经营活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_opercashout` | 经营活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_opernetcash` | 经营活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_paidcash` | 支付其他与经营活动有关的现金 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_salescash` | 销售商品、提供劳务收到的现金 | REPORTDATE、TYPE |
| `f_stm07_cs_reits_tax` | 支付的各项税费 | REPORTDATE、TYPE |
| `f_stm07_is_reits_cost` | 营业成本 | REPORTDATE、TYPE |
| `f_stm07_is_reits_financefee` | 财务费用 | REPORTDATE、TYPE |
| `f_stm07_is_reits_generalprofit` | 综合收益总额 | REPORTDATE、TYPE |
| `f_stm07_is_reits_income` | 营业收入 | REPORTDATE、TYPE |
| `f_stm07_is_reits_managefee` | 管理费用 | REPORTDATE、TYPE |
| `f_stm07_is_reits_netprofit` | 净利润 | REPORTDATE、TYPE |
| `f_stm07_is_reits_profit` | 营业利润 | REPORTDATE、TYPE |
| `f_stm07_is_reits_rdfee` | 研发费用 | REPORTDATE、TYPE |
| `f_stm07_is_reits_salesfee` | 销售费用 | REPORTDATE、TYPE |
| `f_stm07_is_reits_scost` | 营业总成本 | REPORTDATE、TYPE |
| `f_stm07_is_reits_sincome` | 营业总收入 | REPORTDATE、TYPE |
| `f_stm07_is_reits_sumprofit` | 利润总额 | REPORTDATE、TYPE |
| `f_stm07_is_reits_tax` | 税金及附加 | REPORTDATE、TYPE |
| `f_stm_bs` | 基金/报表函数/资产负债表 | ITEMSCODE、REPORTDATE |
| `f_stm_bs_goldcontractinterest` | 应收黄金合约拆借孳息 | REPORTDATE |
| `f_stm_bs_reits_accountspayable` | 应付账款 | REPORTDATE、TYPE |
| `f_stm_bs_reits_accountsreceivable` | 应收账款 | REPORTDATE、TYPE |
| `f_stm_bs_reits_capitalreserves` | 资本公积 | REPORTDATE、TYPE |
| `f_stm_bs_reits_contractliabilities` | 合同负债 | REPORTDATE、TYPE |
| `f_stm_bs_reits_custodianfeepayable` | 应付托管费 | REPORTDATE、TYPE |
| `f_stm_bs_reits_deferredincometaxassets` | 递延所得税资产 | REPORTDATE、TYPE |
| `f_stm_bs_reits_deferredincometaxliabilities` | 递延所得税负债 | REPORTDATE、TYPE |
| `f_stm_bs_reits_employeepaypayable` | 应付职工薪酬 | REPORTDATE、TYPE |
| `f_stm_bs_reits_goodwill` | 商誉 | REPORTDATE、TYPE |
| `f_stm_bs_reits_intangibleassets` | 无形资产 | REPORTDATE、TYPE |
| `f_stm_bs_reits_interest_receivable` | 应收利息 | REPORTDATE、TYPE |
| `f_stm_bs_reits_interestincome` | 利息收入 | REPORTDATE、TYPE |
| `f_stm_bs_reits_inventories` | 存货 | REPORTDATE、TYPE |
| `f_stm_bs_reits_investmentprofit` | 投资收益 | REPORTDATE、TYPE |
| `f_stm_bs_reits_investmentrealestate` | 投资性房地产 | REPORTDATE、TYPE |
| `f_stm_bs_reits_liabilities_andownerequity` | 负债和所有者权益总计 | REPORTDATE、TYPE |
| `f_stm_bs_reits_longterm_equityinvestment` | 长期股权投资 | REPORTDATE、TYPE |
| `f_stm_bs_reits_longterm_loans` | 长期借款 | REPORTDATE、TYPE |
| `f_stm_bs_reits_longtermdeferredexpenses` | 长期待摊费用 | REPORTDATE、TYPE |
| `f_stm_bs_reits_managementfeepayable` | 应付管理人报酬 | REPORTDATE、TYPE |
| `f_stm_bs_reits_moneyfunds` | 货币资金 | REPORTDATE、TYPE |
| `f_stm_bs_reits_operatingrevenue` | 营业收入 | REPORTDATE、TYPE |
| `f_stm_bs_reits_otherassets` | 其他资产 | REPORTDATE、TYPE |
| `f_stm_bs_reits_otherliabilities` | 其他负债 | REPORTDATE、TYPE |
| `f_stm_bs_reits_paidincapital` | 实收基金 | REPORTDATE、TYPE |
| `f_stm_bs_reits_settlementreserve` | 结算备付金 | REPORTDATE、TYPE |
| `f_stm_bs_reits_taxpayable` | 应交税费 | REPORTDATE、TYPE |
| `f_stm_bs_reits_totalassets` | 资产总计 | REPORTDATE、TYPE |
| `f_stm_bs_reits_totalliabilities` | 负债合计 | REPORTDATE、TYPE |
| `f_stm_bs_reits_totaloperatingrevenue` | 营业总收入 | REPORTDATE、TYPE |
| `f_stm_bs_reits_totalownersequity` | 所有者权益合计 | REPORTDATE、TYPE |
| `f_stm_bs_reits_tradablefinancialassets` | 交易性金融资产 | REPORTDATE、TYPE |
| `f_stm_bs_reits_undistributedprofit` | 未分配利润 | REPORTDATE、TYPE |
| `f_stm_bs_repoin_exchmkt` | 买入返售金融资产(交易所市场) | REPORTDATE |
| `f_stm_bs_repoin_interbmkt` | 买入返售金融资产(银行间市场) | REPORTDATE |
| `f_stm_cs_reits_beginningcashequivalents` | 期初现金及现金等价物余额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashfromborrowing` | 取得借款收到的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashfrominterest` | 取得利息收入收到的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashfromsr` | 销售商品、提供劳务收到的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashpaiddistribution` | 分配支付的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashpaidinterestpayment` | 偿付利息支付的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashpaidpgs` | 购买商品、接受劳务支付的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cashreceivedfromop` | 收到其他与经营活动有关的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cshpdrpbrw` | 偿还借款支付的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_cshrvdsubcon` | 认购/申购收到的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_endingcashequivalents` | 期末现金及现金等价物余额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_netcashfrominvest` | 投资活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_netcashsbu` | 取得子公司及其他营业单位支付的现金净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_netcffinancing` | 筹资活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_netcffromop` | 经营活动产生的现金流量净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_netincreasecashequivalents` | 现金及现金等价物净增加额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_ntcshpdacsinv` | 取得证券投资支付的现金净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_ntcshrvddsinv` | 处置证券投资收到的现金净额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_ntdecfinarsl` | 买入返售金融资产净减少额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_ntincfinarsl` | 买入返售金融资产净增加额 | REPORTDATE、TYPE |
| `f_stm_cs_reits_othercashia` | 支付其他与投资活动有关的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_othercashoa` | 支付其他与经营活动有关的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_otherpaidcashtofa` | 支付其他与筹资活动有关的现金 | REPORTDATE、TYPE |
| `f_stm_cs_reits_subtotalcifromop` | 经营活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm_cs_reits_subtotalcofromop` | 经营活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm_cs_reits_taxchargespaid` | 支付的各项税费 | REPORTDATE、TYPE |
| `f_stm_cs_reits_totalcff` | 筹资活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm_cs_reits_totalcffinancing` | 筹资活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm_cs_reits_totalcfia` | 投资活动现金流出小计 | REPORTDATE、TYPE |
| `f_stm_cs_reits_totalcifrominvest` | 投资活动现金流入小计 | REPORTDATE、TYPE |
| `f_stm_ds` | 基金/财务报表/基金收益分配表 | ITEMSCODE、REPORTDATE |
| `f_stm_is` | 基金/财务报表/经营业绩表 | ITEMSCODE、REPORTDATE |
| `f_stm_is_18` | 信息披露费 | REPORTDATE |
| `f_stm_is_19` | 审计费用 | REPORTDATE |
| `f_stm_is_26` | 税金及附加 | REPORTDATE |
| `f_stm_is_75` | 基金投资收益 | REPORTDATE |
| `f_stm_is_76` | 其他利息收入 | REPORTDATE |
| `f_stm_is_77` | 汇兑收入 | REPORTDATE |
| `f_stm_is_78` | 所得税费用 | REPORTDATE |
| `f_stm_is_79` | 净利润 | REPORTDATE |
| `f_stm_is_79_total` | 净利润(合计) | REPORTDATE |
| `f_stm_is_dd` | 存款利息收入-活期存款利息收入 | REPORTDATE |
| `f_stm_is_iid` | 存款利息收入-合计 | REPORTDATE |
| `f_stm_is_iiod` | 存款利息收入-其他 | REPORTDATE |
| `f_stm_is_od` | 存款利息收入-其他存款利息收入 | REPORTDATE |
| `f_stm_is_reits_administrativecosts` | 管理费用 | REPORTDATE、TYPE |
| `f_stm_is_reits_assetimpair` | 资产减值损失 | REPORTDATE、TYPE |
| `f_stm_is_reits_credit_impairmentloss` | 信用减值损失 | REPORTDATE、TYPE |
| `f_stm_is_reits_custodyfee` | 托管费 | REPORTDATE、TYPE |
| `f_stm_is_reits_financialcosts` | 财务费用 | REPORTDATE、TYPE |
| `f_stm_is_reits_incometaxexpenses` | 所得税费用 | REPORTDATE、TYPE |
| `f_stm_is_reits_interestcost` | 利息支出 | REPORTDATE、TYPE |
| `f_stm_is_reits_managementfee` | 管理人报酬 | REPORTDATE、TYPE |
| `f_stm_is_reits_netprofit` | 净利润 | REPORTDATE、TYPE |
| `f_stm_is_reits_netprofit_fromgoingconcern` | 持续经营净利润 | REPORTDATE、TYPE |
| `f_stm_is_reits_nonoperatingexpenses` | 营业外支出 | REPORTDATE、TYPE |
| `f_stm_is_reits_nonoperatingrevenue` | 营业外收入 | REPORTDATE、TYPE |
| `f_stm_is_reits_operatingcost` | 营业成本 | REPORTDATE、TYPE |
| `f_stm_is_reits_operatingprofit` | 营业利润 | REPORTDATE、TYPE |
| `f_stm_is_reits_otherexpenses` | 其他费用 | REPORTDATE、TYPE |
| `f_stm_is_reits_taxandsurcharges` | 税金及附加 | REPORTDATE、TYPE |
| `f_stm_is_reits_totalcomprehensiveincome` | 综合收益总额 | REPORTDATE、TYPE |
| `f_stm_is_reits_totaloperatingcost` | 营业总成本 | REPORTDATE、TYPE |
| `f_stm_is_reits_totalprofit` | 利润总额 | REPORTDATE、TYPE |
| `f_stm_is_securityborrowincome` | 证券出借利息收入 | REPORTDATE |
| `f_stm_is_sr` | 存款利息收入-结算备付金利息收入 | REPORTDATE |
| `f_stm_is_td` | 存款利息收入-定期存款利息收入 | REPORTDATE |
| `f_stm_issuingdate` | 定期报告披露日期 | REPORTDATE |
| `f_stm_issuingdate_qty` | 季度报告披露日期 |  |
| `f_stm_navchange` | 基金/财务报表/基金净值变动表 | ITEMSCODE、REPORTDATE |
| `f_stm_navchange_1` | 期初所有者权益(基金净值) | REPORTDATE |
| `f_stm_navchange_11` | 期末所有者权益(基金净值) | REPORTDATE |
| `f_stm_navchange_7_paidincapital` | 基金申购款(实收基金) | REPORTDATE |
| `f_stm_navchange_8_paidincapital` | 基金赎回款(实收基金) | REPORTDATE |
| `f_style_averagepositiontime` | 平均持仓时间 |  |
| `f_style_avgpositiontimeranking` | 平均持仓时间同类排名 |  |
| `f_style_commisaccount` | 佣金规模比 | REPORTDATE |
| `f_style_hy_averagepositiontime` | 平均持仓时间(半年) |  |
| `f_style_invconcentration` | 投资集中度 |  |
| `f_style_marketvalueattribute` | 市值属性 |  |
| `f_style_marketvaluestyleattribute` | 市值-风格属性 |  |
| `f_style_rpt_turn` | 基金报告期持仓换手率 |  |
| `f_style_styleattribute` | 风格属性 |  |
| `f_style_stylecoefficient` | 风格系数 |  |
| `f_style_topnproportiontoallindustries` | 前N大行业占全部行业比 |  |
| `f_style_topnproportiontoallshares` | 前N大股票占全部股票投资比 |  |
| `f_system_risk` | 系统风险 | StartDate、EndDate |
| `f_top10stock_pb` | 重仓持股平均市净率 | REPORTDATE |
| `f_top10stock_pe` | 重仓持股平均市盈率 | REPORTDATE |
| `f_topnindustry_stable_thirdparty` | 前N大行业是否稳定 | StartDate、DATE、PsitionThreshold |
| `f_topnindustrynames_thirdparty` | 前N大行业名称 | REPORTDATE |
| `f_unit_change` | 基金份额变化 | BEGINDATE、EndDate |
| `f_unit_changedate` | 基金份额变动日期 |  |
| `f_unit_changerate` | 基金份额变化率 | BEGINDATE、EndDate |
| `f_unit_floortrading` | 场内流通份额 |  |
| `f_unit_floortradingchange` | 当期场内流通份额变化 | TRADEDATE |
| `f_unit_mergedsharesornot` | 份额是否为合并数据 |  |
| `f_unit_netpurchase` | 报告期申购赎回净额 | REPORTDATE |
| `f_unit_netpurchase_qty` | 单季申购赎回净额 | REPORTDATE |
| `f_unit_netpurchasetot` | 报告期申购赎回净额(合计) | REPORTDATE |
| `f_unit_netquarterlyratio` | 单季度净申购赎回率 |  |
| `f_unit_nontradable` | 未上市流通基金份数(封闭式) |  |
| `f_unit_purchase` | 报告期总申购份额 | REPORTDATE |
| `f_unit_purchase_qty` | 单季总申购份额 | REPORTDATE |
| `f_unit_purchasetot` | 报告期总申购份额(合计) | REPORTDATE |
| `f_unit_redemption` | 报告期总赎回份额 | REPORTDATE |
| `f_unit_redemption_qty` | 单季总赎回份额 | REPORTDATE |
| `f_unit_redemptiontot` | 报告期总赎回份额(合计) | REPORTDATE |
| `f_unit_reitsfloornontrading` | REITs未流通份额 | TRADEDATE |
| `f_unit_reitsfloortrading` | REITs场内流通份额 | TRADEDATE |
| `f_unit_total` | 基金份额 |  |
| `f_unit_tradable` | 已上市流通基金份数(封闭式) |  |
| `f_up_mkt_capture` | 上行捕获率 | StartDate、EndDate、CalcTerm、Underlying_Index |
| `f_val_mv_ard` | 总市值 | TRADEDATE |
| `f_val_mvc` | 流通市值 | TRADEDATE |
| `f_west_return` | 估算涨跌幅 | TRADEDATE |
| `f_west_return_error` | 估算涨跌幅误差 | TRADEDATE |
| `f_win_ratio` | 区间胜率 | StartDate、EndDate、CalcTerm、Underlying_Index |
| `f_win_ratiofixed` | 区间胜率(基于固定收益率计算) | StartDate、EndDate、CalcTerm、YIELD |
| `f_wq_amount` | 周成交额(新增) |  |
| `f_wq_avgprice` | 周均价(新增) |  |
| `f_wq_avgturn` | 周平均换手率(新增) |  |
| `f_wq_change` | 周涨跌(新增) |  |
| `f_wq_close` | 周收盘价(新增) |  |
| `f_wq_discount` | 周均贴水(新增) |  |
| `f_wq_discountratio` | 周均贴水率(新增) |  |
| `f_wq_high` | 周最高价(新增) |  |
| `f_wq_highclose` | 周最高收盘价(新增) |  |
| `f_wq_highclose_date` | 周最高收盘价日(新增) |  |
| `f_wq_highdate` | 周最高价日(新增) |  |
| `f_wq_low` | 周最低价(新增) |  |
| `f_wq_lowclose` | 周最低收盘价(新增) |  |
| `f_wq_lowclose_date` | 周最低收盘价日(新增) |  |
| `f_wq_lowdate` | 周最低价日(新增) |  |
| `f_wq_open` | 周开盘价(新增) |  |
| `f_wq_pctchange` | 周涨跌幅(新增) |  |
| `f_wq_preclose` | 周前收盘价(新增) |  |
| `f_wq_swing` | 周振幅(新增) |  |
| `f_wq_turn` | 周换手率(新增) |  |
| `f_wq_volume` | 周成交量(新增) |  |
| `f_yq_amount` | 年成交额(新增) |  |
| `f_yq_avgprice` | 年均价(新增) |  |
| `f_yq_avgturn` | 年平均换手率(新增) |  |
| `f_yq_change` | 年涨跌(新增) |  |
| `f_yq_close` | 年收盘价(新增) |  |
| `f_yq_discount` | 年均贴水(新增) |  |
| `f_yq_discountratio` | 年均贴水率(新增) |  |
| `f_yq_high` | 年最高价(新增) |  |
| `f_yq_highclose` | 年最高收盘价(新增) |  |
| `f_yq_highclose_date` | 年最高收盘价日(新增) |  |
| `f_yq_highdate` | 年最高价日(新增) |  |
| `f_yq_low` | 年最低价(新增) |  |
| `f_yq_lowclose` | 年最低收盘价(新增) |  |
| `f_yq_lowclose_date` | 年最低收盘价日(新增) |  |
| `f_yq_lowdate` | 年最低价日(新增) |  |
| `f_yq_open` | 年开盘价(新增) |  |
| `f_yq_pctchange` | 年涨跌幅(新增) |  |
| `f_yq_preclose` | 年前收盘价(新增) |  |
| `f_yq_relpctchange` | 年相对大盘涨跌幅(新增) |  |
| `f_yq_swing` | 年振幅(新增) |  |
| `f_yq_turn` | 年换手率(新增) |  |
| `f_yq_volume` | 年成交量(新增) |  |

<a id="分类-债券"></a>

## 债券（839 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `b_abs_12mavgdefaultrate` | 年化违约率(12月平均) | DEALDATE |
| `b_abs_12mavgprepayrate` | 年化早偿率(12月平均) | DEALDATE |
| `b_abs_actualrecoveryrate` | 不良ABS实际回收比率 | DEALDATE |
| `b_abs_agency_custodian` | 资金保管机构 |  |
| `b_abs_agency_trustee1` | 受托机构 |  |
| `b_abs_annualdefaultrate` | 年化违约率(单月年化) | DEALDATE |
| `b_abs_annualprepayrate` | 年化早偿率 | DEALDATE |
| `b_abs_assetserviceagency` | 资产服务机构 |  |
| `b_abs_borrower` | 基础债务人 |  |
| `b_abs_capyieldpertermofsub` | 次级每期收益率上限 |  |
| `b_abs_cdr_cbr` | ABS累计违约率(中债资信) | TRADEDATE |
| `b_abs_clrprchs` | 清仓回购条款 |  |
| `b_abs_codebtors` | 共同债务人 |  |
| `b_abs_collectionenddate` | 资产池归集时间 |  |
| `b_abs_compassetsrecovrate` | 不良ABS处置完毕资产回收率 | DEALDATE |
| `b_abs_coreindustry` | 基础债务人行业 |  |
| `b_abs_coreproperty` | 基础债务人性质 |  |
| `b_abs_coreprovince` | 基础债务人地区 |  |
| `b_abs_creditnormal` | 承销团成员 |  |
| `b_abs_creditsupport` | 信用支持 | DEALDATE |
| `b_abs_cumdefaultrate` | 累计违约率 | DEALDATE |
| `b_abs_cumulativedefaultrate` | 累计违约率 |  |
| `b_abs_currentloan` | 当前贷款笔数 |  |
| `b_abs_currentloans` | 当前贷款余额 |  |
| `b_abs_currentwarm` | 当前加权平均贷款剩余期限 |  |
| `b_abs_currentwtgavgrate` | 当前加权平均贷款利率 |  |
| `b_abs_cutoffdate` | 初始起算日 |  |
| `b_abs_dealbalance` | 项目发行规模 |  |
| `b_abs_dealout` | 项目存量规模 | DEALDATE |
| `b_abs_dealoutststandingamount` | 项目余额 | DEALDATE |
| `b_abs_defiguarantor` | 差额支付承诺人 |  |
| `b_abs_delinquencyrate` | 严重拖欠率 |  |
| `b_abs_delinquencyrate2` | 严重拖欠率 | DEALDATE |
| `b_abs_endborrower` | 期末剩余资产池借款人户数 | DEALDATE |
| `b_abs_enddateofassetclearing` | 清算结束日 |  |
| `b_abs_endnplbal` | 不良ABS期末本息余额 | DEALDATE |
| `b_abs_endpoolbalance` | 期末剩余资产池余额 | DEALDATE |
| `b_abs_endpoolnumber` | 期末剩余资产池笔数 | DEALDATE |
| `b_abs_endweightedaveragelife` | 期末资产池剩余期限 | DEALDATE |
| `b_abs_endweightedaveragerate` | 期末资产池加权平均利率 | DEALDATE |
| `b_abs_expectedmaturitywithprepay` | 早偿预期到期日 |  |
| `b_abs_expectrecoveramount` | 预计可回收金额 |  |
| `b_abs_expectrecoveryrate` | 不良ABS预期回收比率 | DEALDATE |
| `b_abs_expreconasset` | 不良ABS预期回收比率(占入池资产总额比) | DEALDATE |
| `b_abs_fiexdcapitalcostrate` | 固定资金成本 |  |
| `b_abs_finaladjdur` | 证券最终修正久期 |  |
| `b_abs_finalyiled` | 证券最终收益率 |  |
| `b_abs_firstpaymentdate` | 首次支付日 |  |
| `b_abs_fullnamepro` | 项目名称 |  |
| `b_abs_guarassetpool` | 担保人(对资产池) |  |
| `b_abs_industry` | 主体行业 |  |
| `b_abs_industry1` | 主体性质 |  |
| `b_abs_initialpoolbalance` | 初始资产池金额统计 | AMTTYPE |
| `b_abs_initialpoollife` | 初始资产池期限统计 | AMTTYPE |
| `b_abs_initialpoolnumber` | 初始资产池数量统计 | AMTTYPE |
| `b_abs_initialpoolrate` | 初始资产池利率统计 | AMTTYPE |
| `b_abs_issueprop` | 发行分层占比 | DEALDATE |
| `b_abs_legalmaturity` | 法定到期日 |  |
| `b_abs_liquiditysup` | 流动性支持承诺人(对资产池) |  |
| `b_abs_liquiguarantor` | 流动性支持承诺人 |  |
| `b_abs_namepro` | 项目简称 |  |
| `b_abs_nplcurpirecamt` | 不良ABS本期间本息回收金额 | DEALDATE |
| `b_abs_payback` | 还本方式 |  |
| `b_abs_paymentdate` | 支付日 |  |
| `b_abs_penetrateactrualdebtor` | 穿透信用主体 |  |
| `b_abs_penetrateactrualdebtor_abbr` | 穿透信用主体中文简称 |  |
| `b_abs_periodprepayrate` | 期间早偿率 | DEALDATE |
| `b_abs_prepayrate_cbr` | ABS早偿率预测(中债资信) | TRADEDATE、FN |
| `b_abs_principalbasis_cbr` | ABS本金因子(中债资信) | TRADEDATE |
| `b_abs_prinfinaldate` | 本金最终兑付日 |  |
| `b_abs_projectarrange` | 项目安排人 |  |
| `b_abs_projectcode` | 项目代码 |  |
| `b_abs_province` | 主体地区 |  |
| `b_abs_recommendcpr` | 早偿率 |  |
| `b_abs_recoverycash` | 不良AB期间合计本息回收金额 | DEALDATE |
| `b_abs_recoveryrate_cbr` | ABS回收率预测(中债资信) | TRADEDATE、FN |
| `b_abs_rectopool` | 不良ABS实际回收比率(占入池资产总额比) | DEALDATE |
| `b_abs_reinvestenddate` | 循环期截止日 |  |
| `b_abs_revstartdt` | 循环期起始日 |  |
| `b_abs_samepoolsize` | 同资产池发行规模 |  |
| `b_abs_selfsustainingproportion` | 自持比例 |  |
| `b_abs_shortfallpay` | 差额支付承诺人(对资产池) |  |
| `b_abs_spv` | 计划管理人 |  |
| `b_abs_startdateofassetclearing` | 清算起始日 |  |
| `b_abs_trustee` | 专项计划托管人 |  |
| `b_abs_underlyingtype` | ABS基础资产分类 | ABSType |
| `b_abs_wal_cbr` | ABS预计加权平均期限(中债资信) | TRADEDATE |
| `b_abs_weightedaveragematuritywithprepay` | 加权平均期限 | Cycle |
| `b_actissuer_area` | 国家或地区(穿透信用主体) |  |
| `b_agency_bondtrustee` | 受托管理人 |  |
| `b_agency_bookkeeper` | 账簿管理人 |  |
| `b_agency_booksupporter` | 集中簿记建档系统技术支持机构 |  |
| `b_agency_certification` | 绿色债券认证机构 |  |
| `b_agency_coordinator` | 联席全球协调人(海外) |  |
| `b_agency_fundbank` | 募集资金专项账户开户行 |  |
| `b_agency_guarantor_abbr` | 担保人中文简称 |  |
| `b_agency_guarantorbriefing` | 担保人公司简介,b_agency_guarantorbriefing(新增) |  |
| `b_agency_guarantornature` | 担保人公司属性,b_agency_guarantornature(新增) |  |
| `b_agency_jointleadunder` | 联席主承销商 |  |
| `b_agency_leadunderwritersn` | 主承销商(简称) |  |
| `b_agency_management` | 存续期管理机构 |  |
| `b_agency_manaleadunder` | 牵头主承销商 |  |
| `b_agency_reguarantor` | 再担保人 |  |
| `b_agency_sblc` | 备用信用证提供方 |  |
| `b_agency_underwriter` | 牵头经办人 |  |
| `b_anal_accrint_cnbd` | 应计利息 |  |
| `b_anal_accrint_csi` | 应计利息(中证指数) |  |
| `b_anal_accrint_shc` | 应计利息(上海清算所) |  |
| `b_anal_accrueddays` | 已计息天数 |  |
| `b_anal_accruedinterest` | 应计利息 |  |
| `b_anal_baseduration` | 基准久期 |  |
| `b_anal_basevalue_ifexe` | 行权基点价值 | TRADEDATE |
| `b_anal_bconvexity_ifexe` | 行权基准凸性 | TRADEDATE |
| `b_anal_bduration` | 基准久期(新增) | TD |
| `b_anal_bduration_ifexe` | 行权基准久期 | TRADEDATE |
| `b_anal_bondcleanprice_cnbd` | 债底净价(中债) | TRADEDATE |
| `b_anal_bondcnvxty_cnbd` | 债底凸性(中债) | TRADEDATE |
| `b_anal_bonddirtyprice_cnbd` | 债底全价(中债) | TRADEDATE |
| `b_anal_bondmodidura_cnbd` | 债底修正久期(中债) | TRADEDATE |
| `b_anal_bondpre_cnbd` | 纯债溢价率(中债) | TRADEDATE |
| `b_anal_bondyield_cnbd` | 债底收益率(中债) | TRADEDATE |
| `b_anal_cnvxty_cnbd` | 估价凸性 |  |
| `b_anal_cnvxty_csi` | 估价凸性(中证指数) |  |
| `b_anal_cnvxty_csi1` | 估价凸性(中证指数) | DEALDATE、Credibility |
| `b_anal_cnvxty_shc` | 估价凸性(上海清算所) |  |
| `b_anal_conversionpre_cnbd` | 转股溢价率(中债) | TRADEDATE |
| `b_anal_conversionval_cnbd` | 转股价值(中债) | TRADEDATE |
| `b_anal_convexity` | 凸性 |  |
| `b_anal_convexity_ifexe` | 行权凸性 | TRADEDATE |
| `b_anal_dailycf` | 指定日现金流 |  |
| `b_anal_day` | 距到期日时间(天)(新增) | TD |
| `b_anal_defaultsource` | 估值来源 |  |
| `b_anal_dirty_cfets` | 估价全价(中国货币网) | TRADEDATE |
| `b_anal_dirty_cnbd` | 估价全价 |  |
| `b_anal_dirty_csi` | 估价全价(中证指数) |  |
| `b_anal_dirty_csi1` | 估价全价(中证指数) | DEALDATE、Credibility |
| `b_anal_dirty_shc` | 估价全价(上海清算所) |  |
| `b_anal_duration` | 久期 |  |
| `b_anal_duration2` | 收盘价久期(行/到) | DEALDATE、TYPE |
| `b_anal_durationifexercise` | 行权久期 | TRADEDATE |
| `b_anal_ebbondpre_csi` | 可交换债纯债溢价率(中证指数) | TRADEDATE |
| `b_anal_ebconversionpre_csi` | 可交换债转股溢价率(中证指数) | TRADEDATE |
| `b_anal_eboptionval_csi` | 可交换债期权价值(中证指数) | TRADEDATE |
| `b_anal_ebval_csi` | 可交换债估值(中证指数) | TRADEDATE |
| `b_anal_ebvalyield_csi` | 可交换债估值收益率(中证指数) | TRADEDATE |
| `b_anal_exercisecouponrate_cnbd` | 估算的行权后票面利率 | DEALDATE |
| `b_anal_idxcnxt_cnbd` | 估价利率凸性 |  |
| `b_anal_idxdura_cnbd` | 估价利率久期 |  |
| `b_anal_lastdate_cfets` | 最新估值日期(中国货币网) |  |
| `b_anal_lastdate_cnbd` | 最新中债估值日期 |  |
| `b_anal_lastdate_csi` | 最新中证估值日期 |  |
| `b_anal_lastdate_shc` | 最新清算所估值日期 |  |
| `b_anal_latestpar_cnbd` | 剩余本金(中债) | TRADEDATE、Credibility |
| `b_anal_matu_cnbd` | 待偿年限(年) |  |
| `b_anal_maturityspreadcdb` | 到期利差(减国开) | TRADEDATE |
| `b_anal_maturityspreadtb` | 到期利差(减国债) | TRADEDATE |
| `b_anal_mcnet_cnbd` | 市场净价(新增) | DATE |
| `b_anal_mcyield_cnbd` | 市场收益率(新增) | DATE |
| `b_anal_mdirty_cnbd` | 市场全价(新增) | DATE |
| `b_anal_modidura_cnbd` | 估价修正久期 |  |
| `b_anal_modidura_csi` | 估价修正久期(中证指数) |  |
| `b_anal_modidura_csi1` | 估价修正久期(中证指数) | DEALDATE、Credibility |
| `b_anal_modidura_shc` | 估价修正久期(上海清算所) |  |
| `b_anal_modiduration_ifexe` | 行权修正久期 | TRADEDATE |
| `b_anal_modifiedduration` | 修正久期 |  |
| `b_anal_modifiedduration2` | 收盘价修正久期(行/到) | DEALDATE、TYPE |
| `b_anal_net_cfets` | 估价净价(中国货币网) | TRADEDATE |
| `b_anal_net_cnbd` | 估价净价 |  |
| `b_anal_net_csi` | 估价净价(中证指数) |  |
| `b_anal_net_csi1` | 估价净价(中证指数) | DEALDATE、Credibility |
| `b_anal_net_shc` | 估价净价(上海清算所) |  |
| `b_anal_nextexercisedate` | 下一行权日 | DEALDATE、TYPE |
| `b_anal_nxcupn` | 下一付息日 |  |
| `b_anal_nxcupn2` | 距下一付息日天数 |  |
| `b_anal_nxoptiondate` | 下一行权日 |  |
| `b_anal_optionspreadcdb` | 行权利差(减国开) | TRADEDATE |
| `b_anal_optionspreadtb` | 行权利差(减国债) | TRADEDATE |
| `b_anal_optionval_cnbd` | 期权价值(中债) | TRADEDATE |
| `b_anal_precupn` | 上一付息日 | DEALDATE |
| `b_anal_ptm` | 剩余存续期 | DEALDATE、TYPE |
| `b_anal_ptmyear` | 距到期日时间(年)(新增) | TD |
| `b_anal_rcytm` | 票面调整收益率 |  |
| `b_anal_sconvexity_ifexe` | 行权利差凸性 | TRADEDATE |
| `b_anal_sduration` | 利差久期(新增) | TD |
| `b_anal_sduration_ifexe` | 行权利差久期 | TRADEDATE |
| `b_anal_sprcnxt_cnbd` | 估价利差凸性 |  |
| `b_anal_sprdura_cnbd` | 估价利差久期 |  |
| `b_anal_spreadduration` | 利差久期 |  |
| `b_anal_termifexercise` | 行权剩余期限(年) | TRADEDATE |
| `b_anal_vobp_cnbd` | 估价基点价值 |  |
| `b_anal_vobp_shc` | 估价基点价值(上海清算所) |  |
| `b_anal_yield_cfets` | 估价收益率(中国货币网) | TRADEDATE |
| `b_anal_yield_cnbd` | 估价收益率(%) |  |
| `b_anal_yield_csi` | 估价收益率(中证指数) |  |
| `b_anal_yield_csi1` | 估价收益率(中证指数) | DEALDATE、Credibility |
| `b_anal_yield_shc` | 估价收益率(上海清算所) |  |
| `b_anal_ytc` | 赎回收益率 |  |
| `b_anal_ytm` | 到期收益率 |  |
| `b_anal_ytm_ifexe` | 行权收益率 | TRADEDATE |
| `b_anal_ytp` | 回售收益率 |  |
| `b_assetmanagementshold_products` | 持有券商资管家数 | REPORTDATE |
| `b_base_currency` | 基准货币名称 |  |
| `b_buy_rate_cash` | 钞买价 | TRADEDATE、ForeignExchange |
| `b_buy_rate_transfer` | 汇买价 | TRADEDATE、ForeignExchange |
| `b_calc_accrint` | 指定日应计利息 |  |
| `b_calc_accrued` | 应计利息 |  |
| `b_calc_adjyield` | 价格算票面调整收益率 | TRADEDATE、ExtraCoupon、BondPrice |
| `b_calc_askprice` | 计算卖出价格 |  |
| `b_calc_chinabond` | 收益率曲线(中债)3.0 | TRADEDATE、Term |
| `b_calc_clean` | 全价算净价 |  |
| `b_calc_conv` | 凸性 |  |
| `b_calc_curve` | 收益率曲线 |  |
| `b_calc_curve_chinabond` | 收益率曲线(中债) |  |
| `b_calc_curve_csi` | 收益率曲线(中证) |  |
| `b_calc_curve_shc` | 收益率曲线(上清所) |  |
| `b_calc_dirty` | 净价算全价 |  |
| `b_calc_duration` | 麦考利久期 |  |
| `b_calc_floataddbp` | 计算浮息债隐含加息基点 |  |
| `b_calc_floatbench` | 计算浮息债隐含基准利率 |  |
| `b_calc_floatpv` | 计算浮息债全价 | TRADEDATE、Rate、Implied |
| `b_calc_hpy` | 持有期收益率 |  |
| `b_calc_hpygain` | 计算持有资本利得(BC2) | BUYDATE、BUYPRICE、SELLDATE、SELLPRICE |
| `b_calc_hpyinc` | 计算持有本息收益(BC2) | BUYDATE、SELLDATE |
| `b_calc_mduration` | 修正久期 |  |
| `b_calc_outrepoprice` | 买断式回购到期结算价 |  |
| `b_calc_outreporate` | 计算买断式回购利率 |  |
| `b_calc_price` | 收益率(Wind)算价格 |  |
| `b_calc_price2` | 收益率(本币)算价格 |  |
| `b_calc_pv` | 收益率算价格(BC1) | TRADEDATE、IncomeRate、IncomeRateType、PRICETYPE |
| `b_calc_pv_vat` | 增值税税后价格 | TRADEDATE、BondPrice、PRICETYPE、FXCLOSINGTIME |
| `b_calc_pvbp` | 基点价值 |  |
| `b_calc_repoactrate` | 计算回购交易利率 |  |
| `b_calc_repodays` | 回购资金占用天数 |  |
| `b_calc_repomodrate` | 计算回购修正利率 |  |
| `b_calc_repoprice` | 质押式回购利率算到期结算价 |  |
| `b_calc_reporate` | 计算质押式回购利率 |  |
| `b_calc_yield` | 价格算到期收益率(Wind) |  |
| `b_calc_yield2` | 价格算到期收益率(本币) |  |
| `b_calc_ytm` | 价格算收益率(BC1) | TRADEDATE、BondPrice、PRICETYPE、IncomeRateType |
| `b_calc_ytm_vat` | 增值税税后收益率 | TRADEDATE、YIELD、YIELDTYPE、FXCLOSINGTIME |
| `b_capital_ccontinent_security` | 是否COCO债 |  |
| `b_cashofferperiod` | 是否在现金要约期 | DEALDATE |
| `b_clause_conversion_code` | 转股代码 |  |
| `b_cleanprice_cbr` | 估值净价(中债资信) | TRADEDATE |
| `b_convexity_cbr` | 凸性(中债资信) | TRADEDATE |
| `b_credit_bondcreditstatus` | 债券信用状态 | TRADEDATE |
| `b_credit_linedate` | 最新授信日期 |  |
| `b_credit_lineused2` | 历史已使用授信额度 | TRADEDATE |
| `b_creditspread_wind` | 信用利差(减Wind基准) | TRADEDATE |
| `b_crm_bookkeepingdate` | 簿记建档日,b_crm_bookkeepingdate(新增) |  |
| `b_crm_carrydate` | 凭证起始日,b_crm_carrydate(新增) |  |
| `b_crm_creditevent` | 信用事件,b_crm_creditevent(新增) |  |
| `b_crm_dateofrecord` | 凭证登记日,b_crm_dateofrecord(新增) |  |
| `b_crm_issuer` | 创设机构,b_crm_issuer(新增) |  |
| `b_crm_issuerbriefing` | 创设机构公司简介,b_crm_issuerbriefing(新增) |  |
| `b_crm_issuercode` | 创设机构交易代码 |  |
| `b_crm_issuernature` | 创设机构公司属性,b_crm_issuernature(新增) |  |
| `b_crm_paymentterms` | 付费方式,b_crm_paymentterms(新增) |  |
| `b_crm_performguarantee` | 履约保障机制,b_crm_performguarantee(新增) |  |
| `b_crm_permissionnumber` | 创设批准文件编号,b_crm_permissionnumber(新增) |  |
| `b_crm_registeragency` | 登记机构,b_crm_registeragency(新增) |  |
| `b_crm_startingprice` | 创设价格,b_crm_startingprice(新增) |  |
| `b_crm_subject` | 标的实体,b_crm_subject(新增) |  |
| `b_crm_subjectcode` | 标的实体交易代码 |  |
| `b_crm_ubondoustandingamount` | 发行时标的债券余额,b_crm_ubondoustandingamount(新增) |  |
| `b_currency_pair` | 货币对名称 |  |
| `b_cvn_rateofstdbndcsi` | 报价式回购折算率(中证指数) | TRADEDATE |
| `b_dailycf_int` | 指定日利息现金流 | DEALDATE |
| `b_dailycf_prin` | 指定日本金现金流 | DEALDATE |
| `b_dcm_accumamount` | 历史累计注册额度,B_DCM_Accumamount(新增) | BType |
| `b_dcm_expirationdata` | 未使用额度有效期,B_DCM_Expirationdata(新增) | BType |
| `b_dcm_firstissueenddate` | 首期发行截止日 |  |
| `b_dcm_meetingdata` | 未使用注册会议日期,B_DCM_Meetingdata(新增) | BType |
| `b_dcm_number` | 最新注册文件编号,B_DCM_Number(新增) | BType |
| `b_dcm_uesdamount` | 已使用注册额度,B_DCM_Uesdamount(新增) | BType |
| `b_dcm_underwriter` | 未使用额度主承销商,B_DCM_Underwriter(新增) | BType |
| `b_dcm_unuesdamount` | 未使用注册额度,B_DCM_Unuesdamount(新增) | BType |
| `b_dq_adjclose` | 收盘价(可复权) | TRADEDATE、PRICETYPE、AdjustType |
| `b_dq_adjfactor` | 复权因子 | TRADEDATE、PRICETYPE |
| `b_dq_adjhigh` | 最高价(可复权) | TRADEDATE、PRICETYPE、AdjustType |
| `b_dq_adjlow` | 最低价(可复权) | TRADEDATE、PRICETYPE、AdjustType |
| `b_dq_adjopen` | 开盘价(可复权) | TRADEDATE、PRICETYPE、AdjustType |
| `b_dq_adjpreclose` | 前收盘价(可复权) | TRADEDATE、PRICETYPE、AdjustType |
| `b_dq_amount` | 成交额 |  |
| `b_dq_askrt_avg` | 报价卖出收益率(算数平均) |  |
| `b_dq_askrt_bst` | 报价卖出收益率(最优) |  |
| `b_dq_avgprice` | 成交均价 |  |
| `b_dq_avgyiled_broker` | 均价收益率(经纪商) | TRADEDATE |
| `b_dq_biaskrt_bst` | 双边卖出收益率(最优) |  |
| `b_dq_biaskrt_wt` | 双边卖出收益率(加权平均) |  |
| `b_dq_bibidrt_bst` | 双边买入收益率(最优) |  |
| `b_dq_bibidrt_wt` | 双边买入收益率(加权平均) |  |
| `b_dq_bidclosingyield_broker` | 买入收盘收益率(经纪商) | TRADEDATE |
| `b_dq_bidrt_avg` | 报价买入收益率(算数平均) |  |
| `b_dq_bidrt_bst` | 报价买入收益率(最优) |  |
| `b_dq_bidyield_broker` | 买入平均价收益率(经纪商) | TRADEDATE |
| `b_dq_binetask_bst` | 双边卖出净价(最优) |  |
| `b_dq_binetask_wt` | 双边卖出净价(加权平均) |  |
| `b_dq_binetbid_bst` | 双边买入净价(最优) |  |
| `b_dq_binetbid_wt` | 双边买入净价(加权平均) |  |
| `b_dq_biqtvolm` | 双边报价笔数 |  |
| `b_dq_change` | 涨跌 |  |
| `b_dq_cleanprice` | 收盘价(净价) | TRADEDATE |
| `b_dq_close` | 收盘价 |  |
| `b_dq_dirtyprice` | 收盘价(全价) | TRADEDATE |
| `b_dq_high` | 最高价 |  |
| `b_dq_highyiled_broker` | 最高价收益率(经纪商) | TRADEDATE |
| `b_dq_low` | 最低价 |  |
| `b_dq_lowyiled_broker` | 最低价收益率(经纪商) | TRADEDATE |
| `b_dq_netask_avg` | 报价卖出净价(算数平均) |  |
| `b_dq_netask_bst` | 报价卖出净价(最优) |  |
| `b_dq_netbid_avg` | 报价买入净价(算数平均) |  |
| `b_dq_netbid_bst` | 报价买入净价(最优) |  |
| `b_dq_ofrclosingyield_broker` | 卖出收盘收益率(经纪商) | TRADEDATE |
| `b_dq_ofryield_broker` | 卖出平均价收益率(经纪商) | TRADEDATE |
| `b_dq_open` | 开盘价 |  |
| `b_dq_originclose` | 收盘价 |  |
| `b_dq_pctchange` | 涨跌幅 |  |
| `b_dq_preclose` | 前收盘价 |  |
| `b_dq_preclose_ssefi` | 上证固收平台前收盘价 | TRADEDATE、PRICETYPE |
| `b_dq_prevwtdavgpice_ssefi` | 上证固收平台前加权均价 | TRADEDATE、PRICETYPE |
| `b_dq_qtvolm` | 报价报价总笔数 |  |
| `b_dq_rollsample` | 滚动序列样本券 | TRADEDATE |
| `b_dq_tradeyiled_broker` | 成交收盘收益率(经纪商) | TRADEDATE |
| `b_dq_volume` | 成交量 |  |
| `b_dq_volume_z` | 成交量 | TRADEDATE |
| `b_elcd_number` | 交易所最新确认文件文号 |  |
| `b_esg_approval` | ESG债券认证标准 |  |
| `b_esg_benefit_evaluation` | ESG债券效益评估 |  |
| `b_esg_conclusion` | ESG债券认证结论 |  |
| `b_esg_escore_wind` | 环境维度得分 | TRADEDATE |
| `b_esg_eventscore_wind` | ESG争议事件得分 | TRADEDATE |
| `b_esg_gscore_wind` | 治理维度得分 | TRADEDATE |
| `b_esg_mgmtscore_wind` | ESG管理实践得分 | TRADEDATE |
| `b_esg_proportion` | ESG债券募集金额认定比例 |  |
| `b_esg_rating_wind` | Wind ESG评级 | TRADEDATE |
| `b_esg_score_wind` | Wind ESG综合得分 | TRADEDATE |
| `b_esg_sscore_wind` | 社会维度得分 | TRADEDATE |
| `b_fina_debtexeoffshore` | 债务压力(行权、境外) | StartDate、EndDate |
| `b_fina_debtexeonshore` | 债务压力(行权、境内) | StartDate、EndDate |
| `b_fina_debtmatoffshore` | 债务压力(到期、境外) | StartDate、EndDate |
| `b_fina_debtmatonshore` | 债务压力(到期、境内) | StartDate、EndDate |
| `b_fina_mat` | 指定期限内债券余额,B_Fina_mat(新增) | Term |
| `b_fina_perpb` | 主体永续债余额 | TRADEDATE |
| `b_fina_remainingnumber` | 存量债券数目 |  |
| `b_fina_subordinateddebt` | 主体次级债余额 | TRADEDATE |
| `b_fina_totalamount` | 总发债券余额,B_Fina_Totalamount(新增) | BType |
| `b_fina_totalamount2` | 区间发行债券总额 | StartDate、DATE |
| `b_fina_totalamount_meth` | 存量债券余额(按发行方式) | BondType、DEALDATE、Issue |
| `b_fina_totalnumber` | 区间发行债券数目 | StartDate、DATE |
| `b_final_totalamout_anytime` | 存量债券余额(支持历史) | DEALDATE |
| `b_fundhold_names` | 持有基金名称 | REPORTDATE |
| `b_fundhold_ratio` | 基金持债市值占发行量比 | REPORTDATE |
| `b_fundhold_value` | 基金持债市值 | REPORTDATE |
| `b_fx_source` | 外汇牌价来源 |  |
| `b_guarantor_type` | 担保人类型 |  |
| `b_holder_amount` | 发行人债券机构持仓金额 | REPORTDATE、TYPE |
| `b_holder_code` | 发行人债券机构持仓产品代码 | REPORTDATE、TYPE |
| `b_holder_detail` | 发行人债券机构持仓明细 | REPORTDATE、TYPE |
| `b_info_acceleratedornot` | 是否可加速到期 |  |
| `b_info_accounttreatment` | 会计处理 |  |
| `b_info_actualbenchmark` | 计息基准 |  |
| `b_info_actualmaturitydate` | 实际到期日 |  |
| `b_info_additionalto` | 增发债对应原债券 |  |
| `b_info_ado_actualissueamt` | 增发债实际发行额 | Batch |
| `b_info_ado_amountplan` | 增发债计划发行额 | Batch |
| `b_info_ado_anndate` | 增发债公告日 | Batch |
| `b_info_ado_bidcoverratio` | 增发债全场倍数 | Batch |
| `b_info_ado_biddernum` | 增发债投标家数 | Batch |
| `b_info_ado_bidmax` | 增发债投标上限 | Batch |
| `b_info_ado_bidmin` | 增发债投标下限 | Batch |
| `b_info_ado_bidspread` | 增发债中标利差 | Batch |
| `b_info_ado_bidstep` | 增发债投标步长 | Batch |
| `b_info_ado_continuousbidpos` | 增发债是否要求标位连续 | Batch |
| `b_info_ado_distend` | 增发债分销截止日 | Batch |
| `b_info_ado_diststart` | 增发债分销起始日 | Batch |
| `b_info_ado_fee` | 增发债手续费 | Batch |
| `b_info_ado_issuanceamtmax` | 增发债发行金额上限 | Batch |
| `b_info_ado_issueend` | 增发债发行截止日 | Batch |
| `b_info_ado_issuestart` | 增发债发行起始日 | Batch |
| `b_info_ado_listdate` | 增发债上市日 | Batch |
| `b_info_ado_marginalrate` | 增发债边际利率 | Batch |
| `b_info_ado_marginalratio` | 增发债边际倍数 | Batch |
| `b_info_ado_maxbidprice` | 增发债最高投标价位 | Batch |
| `b_info_ado_maxbidqty` | 增发债标位最高投标量 | Batch |
| `b_info_ado_minbidprice` | 增发债最低投标价位 | Batch |
| `b_info_ado_minbidqty` | 增发债标位最低投标量 | Batch |
| `b_info_ado_minbidunit` | 增发债最小投标单位 | Batch |
| `b_info_ado_payend` | 增发债缴款截止日 | Batch |
| `b_info_ado_paystart` | 增发债缴款起始日 | Batch |
| `b_info_ado_refyield` | 增发债参考收益率 | Batch |
| `b_info_ado_tendermethod` | 增发债招标方式 | Batch |
| `b_info_ado_tendertarget` | 增发债招标标的 | Batch |
| `b_info_ado_tendertime` | 增发债招标时间 | Batch |
| `b_info_ado_tendervenue` | 增发债招标场所 | Batch |
| `b_info_ado_totalbidamt` | 增发债投标总量 | Batch |
| `b_info_ado_totalvalidbidamt` | 增发债有效投标总量 | Batch |
| `b_info_ado_transferdate` | 增发债债券过户日 | Batch |
| `b_info_ado_underwritingmethod` | 增发债承销方式 | Batch |
| `b_info_ado_validbiddernum` | 增发债有效投标家数 | Batch |
| `b_info_ado_winprice` | 增发债中标价格 | Batch |
| `b_info_allreturndate` | 理论回售日 |  |
| `b_info_amtpropfdleundwt` | 主承销商自营资金获配金额 |  |
| `b_info_anchorbond` | 主债券代码 |  |
| `b_info_audaccdate` | 债券审核受理日期 |  |
| `b_info_balanceafterrepayment` | 违约偿还后债券余额 | TRADEDATE |
| `b_info_baserate` | 基准利率 |  |
| `b_info_baserate2` | 基准利率(发行时) |  |
| `b_info_baserate3` | 基准利率(指定日期) | TRADEDATE |
| `b_info_bclc` | 公司债对应上市公司代码(新增) |  |
| `b_info_bissuingdate` | 发行人首次发债日 |  |
| `b_info_bondconsector` | 是否所属债券概念板块 | SectorID |
| `b_info_bondindexbuzhoumountain` | 债券非市场化发行指数 | TRADEDATE |
| `b_info_callrecdate` | 赎回登记日 |  |
| `b_info_carrydate` | 起息日期 |  |
| `b_info_carryenddate` | 计息截止日 |  |
| `b_info_chinabondl1type` | 中债债券一级分类,B_info_ChinabondL1type(新增) |  |
| `b_info_chinabondl2type` | 中债债券二级分类,B_info_ChinabondL2type(新增) |  |
| `b_info_clauseabbr` | 特殊条款(缩写) |  |
| `b_info_clauseitem` | 特殊条款全文 |  |
| `b_info_clausetxt` | 特殊条款文字说明 |  |
| `b_info_clearing` | 清算机构 |  |
| `b_info_code` | 债券代码 |  |
| `b_info_concept` | 所属概念板块 |  |
| `b_info_corporateindexbuzhoumountain` | 主体非市场化发行指数 | TRADEDATE |
| `b_info_coupon` | 息票品种 |  |
| `b_info_couponadj_max` | 票面利率调整上限 |  |
| `b_info_couponadj_min` | 票面利率调整下限 |  |
| `b_info_coupondatetxt` | 付息日说明 |  |
| `b_info_couponrate` | 票面利率(发行时) |  |
| `b_info_couponrate2` | 票面利率(当期) |  |
| `b_info_couponrate3` | 票面利率(指定日期) | TRADEDATE |
| `b_info_coupontxt` | 利率说明 |  |
| `b_info_creditrating` | 信用级别 |  |
| `b_info_creditratingagency` | 评级机构 |  |
| `b_info_defauloccurrencedate` | 违约发生日 | TRADEDATE |
| `b_info_defaultactualrepaymentdate` | 违约实际偿还日 | TRADEDATE |
| `b_info_defaultannouncedate` | 违约公告日 | TRADEDATE |
| `b_info_defaultbalance` | 违约日债券余额 | TRADEDATE |
| `b_info_defaulthistory` | 违约历程 |  |
| `b_info_defaultoverdueinterest` | 违约日逾期利息 | TRADEDATE |
| `b_info_defaultoverdueprincipal` | 违约日逾期本金 | TRADEDATE |
| `b_info_defaultoverduerepurchase` | 违约日逾期回售款 | TRADEDATE |
| `b_info_defaultreason` | 违约原因 | TRADEDATE |
| `b_info_defaultrepaymentannouncedate` | 违约偿还公告日 | TRADEDATE |
| `b_info_defaultrepaymentinterest` | 违约后偿还利息 | TRADEDATE |
| `b_info_defaultrepaymentmethod` | 违约后偿还方式 | TRADEDATE |
| `b_info_defaultrepaymentprincipal` | 违约后偿还本金 | TRADEDATE |
| `b_info_defaultrepaymentprocess` | 违约偿还历程 |  |
| `b_info_defaultrepaymentrepurchase` | 违约后偿还回售款 | TRADEDATE |
| `b_info_defaultype` | 违约类型 | TRADEDATE |
| `b_info_deferraldays` | 假期顺延天数 | TRADEDATE |
| `b_info_defiguarantor` | 差额补偿人 |  |
| `b_info_embeddedopt_his` | 是否含权债(支持历史) | DEALDATE |
| `b_info_eobspecialinstrutions` | 含权债期限特殊说明(新增) |  |
| `b_info_esgbondtype` | ESG(绿色)债券类型 |  |
| `b_info_esgl1type` | ESG(绿色)债券一级分类 |  |
| `b_info_esgl2type` | ESG(绿色)债券二级分类 |  |
| `b_info_execmaturityembedded` | 含权债行权期限 |  |
| `b_info_exemptvat` | 是否免收增值税 |  |
| `b_info_exppropfdleundwt` | 主承销商自营资金获配说明 |  |
| `b_info_extensioncreditenhancementmeasure` | 展期增信措施 | TRADEDATE |
| `b_info_extensioninterestredemptionplan` | 展期利息兑付方案 | TRADEDATE |
| `b_info_extensionprincipalredemptionplan` | 展期本金兑付方案 | TRADEDATE |
| `b_info_fintyothbi` | 发行人金融机构类型 |  |
| `b_info_firstissuebond` | 是否发行人首次发行债券 |  |
| `b_info_floatingreference` | 浮息基准 |  |
| `b_info_fpdocreditprofee` | 信用保护费首次支付日 |  |
| `b_info_fuamtnewbrwn` | 借新还旧募资金额 |  |
| `b_info_fuamtprojcnstr` | 项目建设募资金额 |  |
| `b_info_fuamtrepibdb` | 偿还有息债务募资金额 |  |
| `b_info_fuamtspmwkcpt` | 补充流动资金募资金额 |  |
| `b_info_fullname` | 债券名称 |  |
| `b_info_fullofferacqpx` | 要约收购价格全价 | DEALDATE |
| `b_info_fundarrialdate` | 行权资金到帐日 |  |
| `b_info_greenbond` | 是否绿色债 |  |
| `b_info_greenbondnornot` | 是否绿债 |  |
| `b_info_guaranteeornot` | 担保交收 |  |
| `b_info_guaranteesettlement` | 是否可担保交收 |  |
| `b_info_ibiratingagency` | 发行时债项评级机构 |  |
| `b_info_icqigbe` | 保险(可投有担保)是否可投,B_info_ICQIGBE(新增) |  |
| `b_info_icqigbetype` | 保险可投有担保禁投原因,B_info_ICQIGBEType(新增) |  |
| `b_info_icqingbe` | 保险(可投无担保)是否可投,B_info_ICQINGBE(新增) |  |
| `b_info_icqingbetype` | 保险可投无担保禁投原因,B_info_ICQINGBEType(新增) |  |
| `b_info_iiratingagency` | 发行时主体评级机构 |  |
| `b_info_incashrepur` | 是否含现金要约条款 |  |
| `b_info_incondicall` | 是否含有条件赎回条款 |  |
| `b_info_incouprate` | 是否含调整票面利率条款 |  |
| `b_info_indcaloption` | 是否含赎回条款 |  |
| `b_info_indefintepay` | 是否含利息递延权 |  |
| `b_info_inearlredemp` | 是否含提前购回权 |  |
| `b_info_inequitconve` | 是否含转股条款 |  |
| `b_info_infisoffer` | 是否含优先收购权 |  |
| `b_info_inooutstadex` | 是否含开放退出登记 |  |
| `b_info_inprivapla` | 是否含定向转让条款 |  |
| `b_info_inputoption` | 是否含回售条款 |  |
| `b_info_interestfloor` | 保底利率 |  |
| `b_info_interestfrequency` | 年付息次数 |  |
| `b_info_interestrate` | 边际利率 |  |
| `b_info_interesttype` | 利率类型 |  |
| `b_info_investmentfield` | 投向领域 |  |
| `b_info_investorad` | 适当性管理 |  |
| `b_info_isassetout` | 资产是否出表 |  |
| `b_info_isscitechbond` | 是否科技创新债券 |  |
| `b_info_issueamount` | 发行总额 |  |
| `b_info_issuenumber` | 发行期号 |  |
| `b_info_issueok` | 是否发行失败 |  |
| `b_info_issueprice` | 发行价格 |  |
| `b_info_issuer` | 发行人名称 |  |
| `b_info_issuer_abbr` | 债务主体中文简称 |  |
| `b_info_issuerfirstdefaultdate` | 发行人首次违约日 |  |
| `b_info_issuerhisrating` | 发债主体历史信用等级(指定机构) | RATINGAGENCY、DEALDATE、RatedCompanyType |
| `b_info_issuerratingoutlook` | 发行时主体评级展望 |  |
| `b_info_issuerules` | 发行规则 |  |
| `b_info_issuerupdated` | 债务主体 |  |
| `b_info_issuestructure` | 发行结构 |  |
| `b_info_issueyear` | 发行年度 |  |
| `b_info_issurercreditratingcompany` | 发债主体评级机构 |  |
| `b_info_latannproreamt` | 最新公布拟转售金额 |  |
| `b_info_latestissurercreditrating` | 发债主体最新信用评级 |  |
| `b_info_latestissurercreditrating2` | 主体评级 | TRADEDATE、RATINGAGENCY、RatedCompanyType |
| `b_info_latestissurercreditrating_actual` | 主体评级(主评机构(ABS穿透)) |  |
| `b_info_latestissurercreditratingdate` | 发债主体最新评级日期 |  |
| `b_info_latestissurercreditratingtype` | 发债主体信用评级类型 |  |
| `b_info_latestpar` | 债券最新面值 | TRADEDATE |
| `b_info_latestratingdate` | 发行人最新评级日期(指定机构) | RATINGAGENCY、RatedCompanyType |
| `b_info_latestratingofguarantor` | 担保人最新评级 |  |
| `b_info_latimpreamt` | 最新实施转售金额 |  |
| `b_info_listeddate` | 上市日期 |  |
| `b_info_lowestissurercreditrating` | 发行人最新最低评级 |  |
| `b_info_makewholecall` | 是否全额可赎回 |  |
| `b_info_maturitdate` | 到期日期 |  |
| `b_info_maturitydate` | 到期日期 |  |
| `b_info_mktpricetype` | 市价类型 |  |
| `b_info_mktpricetype_suph` | 市价类型(支持历史) | DEALDATE |
| `b_info_mmfe` | 货基投资合规性,B_info_MMFE(新增) |  |
| `b_info_mmfetype` | 货基禁投原因,B_info_MMFEType(新增) |  |
| `b_info_multimktornot` | 是否跨市场交易 |  |
| `b_info_multiple` | 边际倍数 |  |
| `b_info_municipalbond` | 是否城投债 |  |
| `b_info_municipalbondwind` | 是否城投债(Wind) |  |
| `b_info_municipalbondyy` | 是否城投债(YY) |  |
| `b_info_munitype` | 地方债类型 |  |
| `b_info_nafmiil1type` | NAFMII债券一级分类 |  |
| `b_info_nafmiil2type` | NAFMII债券二级分类 |  |
| `b_info_name` | 债券简称 |  |
| `b_info_netofferacqpx` | 要约收购价格净价 | DEALDATE |
| `b_info_numspcproj` | 专项项目数量 |  |
| `b_info_offeramt` | 要约金额 | DEALDATE |
| `b_info_offercncltndate` | 要约注销日 | DEALDATE |
| `b_info_offerddl` | 要约截止日期 | DEALDATE |
| `b_info_offertime` | 要约时间 | DEALDATE |
| `b_info_outstandingbalance` | 债券余额,B_info_OutstandingBalance(新增) | DATE |
| `b_info_pandabonds` | 是否熊猫债 |  |
| `b_info_paydiscdate` | 付息公告日 |  |
| `b_info_paymentorder` | 偿付顺序 |  |
| `b_info_perpeintertax` | 利息是否免税(永续债) |  |
| `b_info_perpetualornot` | 是否永续债 |  |
| `b_info_pq_highestcreditrating` | 区间最高主体评级 | StartDate、DATE、RATINGAGENCY |
| `b_info_pq_lowestcreditrating` | 区间最低主体评级 | StartDate、DATE、RATINGAGENCY |
| `b_info_prepaymentdate` | 含权债提前还款日期 |  |
| `b_info_prepaymethod` | 提前还本方式 |  |
| `b_info_prepayportion` | 提前还本比例 | Serial |
| `b_info_prornot` | 是否PR债 |  |
| `b_info_putcode` | 回售代码 |  |
| `b_info_ratingoutlooks` | 发行人最新评级展望 |  |
| `b_info_redemptiondate` | 含权债赎回日期(新增) |  |
| `b_info_redemptionprice` | 含权债赎回价格(新增) |  |
| `b_info_reenddate` | 转售截止日 |  |
| `b_info_regamount` | 发行注册额度 |  |
| `b_info_regdate` | 发行注册日期 |  |
| `b_info_registrationdate` | 债权债务登记日 |  |
| `b_info_regnumber` | 发行注册文件号 |  |
| `b_info_repaymentmethod` | 偿还方式 |  |
| `b_info_repo_briefing` | 品种简介 |  |
| `b_info_repurchasebegindate` | 回售登记起始日 |  |
| `b_info_repurchasedate` | 含权债回售日期(新增) |  |
| `b_info_repurchaseenddate` | 回售登记截止日 |  |
| `b_info_repurchaseprice` | 含权债回售价格(新增) |  |
| `b_info_resaleamount` | 最新回售金额 |  |
| `b_info_restartdate` | 转售开始日 |  |
| `b_info_riskstate` | 风险状态 |  |
| `b_info_sametermbond` | 同期债 |  |
| `b_info_scitechbondornot` | 是否科创债 |  |
| `b_info_sechighbondrate` | 债券次高信用评级 | DEALDATE |
| `b_info_sechighrating` | 发行人次高信用评级 | DEALDATE |
| `b_info_secondarycapital` | 是否二级资本债 |  |
| `b_info_shclearl1type` | 上清所债券分类 |  |
| `b_info_singleissuer` | 单一债务主体中文名称 |  |
| `b_info_spedatguabal` | 指定日期担保余额 | Year、P1、Grarantee |
| `b_info_sponsrepresent` | 保荐代表人 |  |
| `b_info_sppboacfprcf` | 专项债投向领域一级分类 |  |
| `b_info_sppboacfsccf` | 专项债投向领域二级分类 |  |
| `b_info_spread` | 利差 |  |
| `b_info_spread2` | 行权后利差 |  |
| `b_info_startdateoffer` | 要约起始日期 | DEALDATE |
| `b_info_taxfree` | 是否免税 |  |
| `b_info_tbondbalance` | 国债余额(做市后) | TRADEDATE |
| `b_info_term` | 期限 |  |
| `b_info_term2` | 债券期限(文字) |  |
| `b_info_term3` | 债券期限(文字/加权) |  |
| `b_info_termnote` | 特殊剩余期限说明 |  |
| `b_info_termnote1` | 特殊剩余期限 | TRADEDATE |
| `b_info_termnote2` | 特殊剩余期限说明(最近行权日) | TRADEDATE |
| `b_info_termnote3` | 剩余期限(每个行权日) | Cycle、TRADEDATE |
| `b_info_termnote4` | 剩余期限(下一行权日) | Cycle、TRADEDATE |
| `b_info_tlacbonds` | 是否TLAC债 |  |
| `b_info_towithdrawalamt` | 撤标总金额 |  |
| `b_info_tranche` | 各级发行总额 | Tranche |
| `b_info_trancheratio` | 各级占比 | Tranche |
| `b_info_type` | 债券类型 |  |
| `b_info_unofferamt` | 未要约金额 | DEALDATE |
| `b_info_unreleasedamount` | 最新未回售金额 |  |
| `b_info_useasprojcap` | 专项债用作项目资本金 |  |
| `b_info_weightedrt` | 加权剩余期限(年）(新增) |  |
| `b_info_weightedrt2` | 加权剩余期限(按本金) | TRADEDATE |
| `b_info_whethertoresell` | 是否转售 |  |
| `b_info_windl1type` | Wind债券一级分类,B_info_WindL1type(新增) |  |
| `b_info_windl1type_1st` | Wind债券一级分类(2025) |  |
| `b_info_windl2type` | Wind债券二级分类,B_info_WindL2type(新增) |  |
| `b_info_windl2type_1st` | Wind债券二级分类(2025) |  |
| `b_info_withdrawaldescription` | 撤标情况说明 |  |
| `b_inst_yybondrating` | 债项评级(YY) |  |
| `b_inst_yybondratinghis` | 债项评级历史(YY) | TRADEDATE |
| `b_inst_yybondval` | 债券估值(YY) |  |
| `b_inst_yybondvalhis` | 债券估值历史(YY) | TRADEDATE |
| `b_inst_yyindustry` | 主体行业(YY) |  |
| `b_inst_yyissuerrating` | 主体评级(YY) |  |
| `b_inst_yyissuerrating_1` | 主体评级(YY) | TRADEDATE |
| `b_inst_yyissuerratinghis` | 主体评级历史(YY) | TRADEDATE |
| `b_inst_yyliquidity` | 债券流动性评级(YY) | TRADEDATE |
| `b_intradayfullprice_cbr` | 日间估值全价(中债资信) | TRADEDATE |
| `b_intradayinterest_cbr` | 日间应计利息(中债资信) | TRADEDATE |
| `b_issue_amountmax` | 发行金额上限 |  |
| `b_issue_dcmvaluation` | NAFMII发行指导利率 |  |
| `b_issue_firstpricedate` | 首个定价日 |  |
| `b_issue_officialdocdate` | 证监会/发改委批文日 |  |
| `b_issue_terms` | 发行条款 |  |
| `b_issuer_actual` | 实际发行人 |  |
| `b_issuer_actual_admin` | 所属行政区划(穿透信用主体) | DivisionType、DEALDATE |
| `b_issuer_actual_city` | 城市(穿透信用主体) |  |
| `b_issuer_actual_nature1` | 公司属性(穿透信用主体) | TRADEDATE |
| `b_issuer_actual_office` | 办公地址(穿透信用主体) |  |
| `b_issuer_actual_province` | 省份(穿透信用主体) |  |
| `b_issuer_actual_regaddress` | 注册地(穿透信用主体) |  |
| `b_issuer_actual_windindustry` | 所属Wind行业名称(穿透信用主体) | TYPE |
| `b_issuer_actual_windindustry2024` | 所属Wind行业名称(穿透信用主体)(2024) | TYPE |
| `b_issuer_banktype` | 发行人(银行)类型 |  |
| `b_issuer_cityinvestmentbondgeo` | 城投行政级别 |  |
| `b_issuer_cityinvestmentbondgeowind` | 城投行政级别(Wind) |  |
| `b_issuer_cityinvestmentbondgeoyy` | 城投行政级别(YY) |  |
| `b_issuer_industry_ccxi` | 所属中诚信行业名称 | TRADEDATE、TYPE |
| `b_issuer_issuershortened` | 发行人中文简称 |  |
| `b_issuer_listingornot1` | 是否上市公司 |  |
| `b_issuer_onshore` | 境内发债主体 |  |
| `b_issuer_shareholderbriefing` | 发行人股东公司简介,b_issuer_shareholderbriefing(新增) | DATE、HS |
| `b_issuer_shareholdernature` | 发行人股东公司属性,b_issuer_shareholdernature(新增) | DATE、HS |
| `b_lastvaluationdate_cbr` | 最新估值日期(中债资信) |  |
| `b_lower_limitprice` | 估值全价下限(中债) | DEALDATE |
| `b_maintermstructure_wind` | Wind主体期限结构曲线 | TRADEDATE、CT、Term |
| `b_mid_rate` | 中间价 | TRADEDATE、ForeignExchange |
| `b_modifiedduration_cbr` | 修正久期(中债资信) | TRADEDATE |
| `b_mq_amount` | 月成交金额(新增) |  |
| `b_mq_avg` | 月均价(新增) |  |
| `b_mq_change` | 月涨跌(新增) |  |
| `b_mq_close` | 月收盘价(新增) |  |
| `b_mq_high` | 月最高价(新增) |  |
| `b_mq_low` | 月最低价(新增) |  |
| `b_mq_open` | 月开盘价(新增) |  |
| `b_mq_pctchange` | 月涨跌幅(新增) |  |
| `b_mq_preclose` | 月前收盘价(新增) |  |
| `b_mq_repo_amount` | 月成交额(新增) |  |
| `b_mq_repo_avgprice` | 月加权平均价(新增) |  |
| `b_mq_repo_close` | 月收盘价(新增) |  |
| `b_mq_repo_high` | 月最高价(新增) |  |
| `b_mq_repo_low` | 月最低价(新增) |  |
| `b_mq_repo_open` | 月开盘价(新增) |  |
| `b_mq_repo_preavgprice` | 月前加权平均价(新增) |  |
| `b_mq_theory` | 月理论价(中国债券信息网)(新增) |  |
| `b_mq_volume` | 月成交量(新增) |  |
| `b_nq_avgvolume` | N日平均成交量 | N、TRADEDATE、TRADType |
| `b_nq_close` | 推N日收盘价(当日结算价) |  |
| `b_nq_originclose` | 推N日收盘价(债券) |  |
| `b_pq_adjclose` | 区间收盘价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjhigh` | 区间最高价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjhighclose` | 区间最高收盘价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjlow` | 区间最低价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjlowclose` | 区间最低收盘价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjopen` | 区间开盘价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_adjpreclose` | 区间前收盘价(可复权) | StartDate、EndDate、PRICETYPE、AdjustType |
| `b_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `b_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `b_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `b_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `b_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `b_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `b_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `b_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `b_pq_high_date` | 区间最高价日 | StartDate、EndDate、PRICETYPE |
| `b_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `b_pq_low_date` | 区间最低价日 | StartDate、EndDate、PRICETYPE |
| `b_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `b_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `b_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `b_pq_theory` | 区间理论价 | BEGINDATE、EndDate |
| `b_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `b_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `b_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `b_qstm_cs` | 债券/单季报表函数/现金流量表 | ITEMSCODE、REPORTDATE |
| `b_qstm_is` | 债券/单季报表函数/利润表 | ITEMSCODE、REPORTDATE |
| `b_qualified_investor` | 合格投资者类型 |  |
| `b_quote_currency` | 计价货币名称 |  |
| `b_rate_agencybond` | 债项评级机构 | TRADEDATE、RATINGAGENCY |
| `b_rate_agencyguarantor` | 担保人评级评级机构 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_agencyissuer` | 主体评级评级机构 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_beginguarantor` | 发行时担保人评级 |  |
| `b_rate_bondscore` | 债券评分 | TRADEDATE |
| `b_rate_changesofrating` | 最新债项评级变动方向 |  |
| `b_rate_chngbond` | 债项评级变动方向 | TRADEDATE、RATINGAGENCY |
| `b_rate_chngguarantor` | 担保人评级变动方向 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_chngissuer` | 主体评级变动方向 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_default_csi` | 隐含违约率(中证指数) | TRADEDATE |
| `b_rate_fwdguarantor` | 担保人评级展望 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_fwdissuer` | 主体评级展望 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_rate_historicalmir_cnbd` | 市场历史隐含评级(中债) |  |
| `b_rate_issuer` | 发债主体历史信用等级 |  |
| `b_rate_issuer2` | 发行人国际评级 | TRADEDATE |
| `b_rate_issuerscore` | 发行人评分 | TRADEDATE |
| `b_rate_issurercreditratingcompany` | 发债主体评级机构(新增) |  |
| `b_rate_lateguarantorchng` | 担保人最新评级变动方向 |  |
| `b_rate_lateguarantordate` | 担保人最新评级日期 |  |
| `b_rate_lateguarantorfwd` | 担保人最新评级展望 |  |
| `b_rate_lateissuerchng` | 发行人最新评级变动方向 |  |
| `b_rate_latest1` | 最新债项评级日期(指定机构) | RATINGAGENCY |
| `b_rate_latestcredit_mainagency` | 债项评级(主评机构) |  |
| `b_rate_latestmir_cnbd` | 市场隐含评级(中债) | TRADEDATE |
| `b_rate_latestmir_csi` | 隐含评级(中证指数) | TRADEDATE |
| `b_rate_ratebond` | 债项评级 | TRADEDATE、RATINGAGENCY |
| `b_rate_ratebond2` | 债券国际评级 | TRADEDATE |
| `b_rate_rateguarantor` | 担保人评级 | TRADEDATE、RatedCompanyType、RATINGAGENCY |
| `b_redemption_price` | 提前兑付净价 | DEALDATE |
| `b_redemption_price_type` | 提前兑付净价类型 | DEALDATE |
| `b_referencelevel_cbr` | 成交参考度(中债资信) | TRADEDATE |
| `b_sell_rate_cash` | 钞卖价 | TRADEDATE、ForeignExchange |
| `b_sell_rate_transfer` | 汇卖价 | TRADEDATE、ForeignExchange |
| `b_stm_bs` | 债券/原始报表函数/资产负债表 | ITEMSCODE、REPORTDATE |
| `b_stm_cs` | 债券/原始报表函数/现金流量表 | ITEMSCODE、REPORTDATE |
| `b_stm_is` | 债券/原始报表函数/利润表 | ITEMSCODE、REPORTDATE |
| `b_stmnote_ar` | 债券/报表附注函数/应收帐款明细 | ITEMSCODE、REPORTDATE |
| `b_stmnote_bank` | 债券/报表附注函数/银行专用指标函数 | ITEMSCODE、REPORTDATE |
| `b_stmnote_finexp` | 债券/报表附注函数/财务费用明细 | ITEMSCODE、REPORTDATE |
| `b_stmnote_guarantee` | 债券/报表附注函数/报告期担保数据 | ITEMSCODE、REPORTDATE |
| `b_stmnote_inv` | 债券/报表附注函数/存货项目明细 | ITEMSCODE、REPORTDATE |
| `b_stmnote_reserve` | 债券/报表附注函数/资产减值准备明细 | ITEMSCODE、REPORTDATE |
| `b_stmnote_tax` | 债券/报表附注函数/所得税税率 | RPTYEAR |
| `b_szse_distribcode` | 深交所分销代码 |  |
| `b_tbf_basis` | 基差 | TRADEDATE |
| `b_tbf_basis01` | 基差 | FuturePriceType、DeliveryCode、TRADEDATE |
| `b_tbf_basis02` | 基差(CTD) | PRICETYPE、TradingVenue、TRADEDATE |
| `b_tbf_bonddeliverydate` | 交券日 | TRADEDATE |
| `b_tbf_ctd2` | CTD(支持历史) | TRADEDATE |
| `b_tbf_cvf` | 转换因子 |  |
| `b_tbf_cvf2` | 转换因子 |  |
| `b_tbf_cvf3` | 转换因子(主力合约) | TRADEDATE、ContractCode |
| `b_tbf_cvf4` | 转换因子 | DeliveryCode、TRADEDATE |
| `b_tbf_deliverprice` | 交割成本 | TRADEDATE |
| `b_tbf_deliverycost` | 交割成本 | DeliveryCode、TRADEDATE |
| `b_tbf_deliveryinterest` | 交割利息 | DeliveryCode、TRADEDATE |
| `b_tbf_fytm` | 远期收益率 | TRADEDATE |
| `b_tbf_fytm01` | 隐含利率 | FuturePriceType、DeliveryCode、TRADEDATE |
| `b_tbf_fytm02` | 隐含利率(CTD) | PRICETYPE、TradingVenue、TRADEDATE |
| `b_tbf_interest` | 交割利息 | TRADEDATE |
| `b_tbf_interestpayment` | 区间付息 | DeliveryCode、TRADEDATE |
| `b_tbf_invoiceprice` | 发票价格 | TRADEDATE |
| `b_tbf_invoiceprice01` | 发票价格 | FuturePriceType、DeliveryCode、TRADEDATE |
| `b_tbf_irr2` | IRR(支持历史) | TRADEDATE、PRICETYPE |
| `b_tbf_lastdeliverydate` | 最后交割日 | TRADEDATE |
| `b_tbf_netbasis` | 净基差 | TRADEDATE |
| `b_tbf_netbasis01` | 净基差 | FuturePriceType、DeliveryCode、TRADEDATE |
| `b_tbf_netbasis02` | 净基差(CTD) | PRICETYPE、TradingVenue、TRADEDATE |
| `b_tbf_payment` | 区间利息 | TRADEDATE |
| `b_tbf_paymentdate` | 缴款日 | TRADEDATE |
| `b_tbf_spotspread` | 期现利差(CTD)(减现货) | TYPE、VENUE、TRADEDATE |
| `b_tbf_spread` | 期现价差 | TRADEDATE |
| `b_tbf_spread01` | 期现价差 | FuturePriceType、DeliveryCode、TRADEDATE |
| `b_tbf_spread02` | 期现价差(CTD) | PRICETYPE、TradingVenue、TRADEDATE |
| `b_tbf_vbasis01` | 基差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE |
| `b_tbf_vbasis02` | 基差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tbf_vctd02` | CTD(估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tbf_vdeliverycost` | 交割成本(估) | DeliveryCode、PriceType5、TRADEDATE |
| `b_tbf_vfytm01` | 隐含利率(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE |
| `b_tbf_vfytm02` | 隐含利率(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tbf_virr01` | IRR(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE |
| `b_tbf_virr02` | IRR(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tbf_vnetbasis01` | 净基差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE |
| `b_tbf_vnetbasis02` | 净基差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tbf_vspread01` | 期现价差(估) | FuturePriceType、DeliveryCode、BondPriceType5、TRADEDATE |
| `b_tbf_vspread02` | 期现价差(CTD估) | FuturePriceType、TradingVenue、BondSourceType2、TRADEDATE |
| `b_tender_exchange` | 招标场所 |  |
| `b_tender_payenddate` | 缴款截止日 |  |
| `b_tender_time` | 招标时间 |  |
| `b_tendrst_balance` | 主承销商余额包销金额 |  |
| `b_tendrst_balanceunderweiting` | 主承销商余额包销说明 |  |
| `b_tendrst_code` | 中债招标发行代码 |  |
| `b_tendrst_effectinvestors` | 有效投标(申购)家数 |  |
| `b_tendrst_tenderamount` | 投标(申购)总量 |  |
| `b_upper_limitprice` | 估值全价上限(中债) | DEALDATE |
| `b_wq_amount` | 周成交金额(新增) |  |
| `b_wq_avg` | 均价(新增) |  |
| `b_wq_change` | 周涨跌(新增) |  |
| `b_wq_close` | 周收盘价(新增) |  |
| `b_wq_high` | 周最高价(新增) |  |
| `b_wq_low` | 周最低价(新增) |  |
| `b_wq_open` | 周开盘价(新增) |  |
| `b_wq_pctchange` | 周涨跌幅(新增) |  |
| `b_wq_preclose` | 周前收盘价(新增) |  |
| `b_wq_repo_amount` | 周成交额(新增) |  |
| `b_wq_repo_avgprice` | 周加权平均价(新增) |  |
| `b_wq_repo_close` | 周收盘价(新增) |  |
| `b_wq_repo_high` | 周最高价(新增) |  |
| `b_wq_repo_low` | 周最低价(新增) |  |
| `b_wq_repo_preavgprice` | 周前加权平均价(新增) |  |
| `b_wq_theory` | 周理论价(中国债券信息网)(新增) |  |
| `b_wq_volume` | 周成交量(新增) |  |
| `b_yq_amount` | 年成交金额(新增) |  |
| `b_yq_avg` | 年均价(新增) |  |
| `b_yq_change` | 年涨跌(新增) |  |
| `b_yq_close` | 年收盘价(新增) |  |
| `b_yq_high` | 年最高价(新增) |  |
| `b_yq_low` | 年最低价(新增) |  |
| `b_yq_open` | 年开盘价(新增) |  |
| `b_yq_pctchange` | 年涨跌幅(新增) |  |
| `b_yq_preclose` | 年前收盘价(新增) |  |
| `b_yq_repo_amount` | 年成交额(新增) |  |
| `b_yq_repo_avgprice` | 年加权平均价(新增) |  |
| `b_yq_repo_preavgprice` | 年前加权平均价(新增) |  |
| `b_yq_theory` | 年理论价(中国债券信息网)(新增) |  |
| `b_yq_volume` | 年成交量(新增) |  |
| `b_ytm_cbr` | 到期收益率(中债资信) | TRADEDATE |

<a id="分类-可转债"></a>

## 可转债（243 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `cb_anal_accrueddays` | 已计息天数 |  |
| `cb_anal_accruedinterest` | 应计利息 |  |
| `cb_anal_announcedateofcsrc` | 证监会核准公告日 |  |
| `cb_anal_caclldatehint` | 预计赎回触发提示日 | TRADEDATE |
| `cb_anal_cacllnxtdate` | 下一赎回条件起始日 | TRADEDATE |
| `cb_anal_caclltrigdate` | 赎回触发日期 | TRADEDATE |
| `cb_anal_caclltrigprog` | 赎回触发进度 | TRADEDATE |
| `cb_anal_caclltrigratio` | 赎回进度比例 | TRADEDATE |
| `cb_anal_caclltrigsit` | 赎回触发情况 | TRADEDATE |
| `cb_anal_convpb` | 转股市净率 |  |
| `cb_anal_convpe` | 转股市盈率 |  |
| `cb_anal_convpremium` | 转股溢价 |  |
| `cb_anal_convpremiumratio` | 转股溢价率 |  |
| `cb_anal_convprice` | 转股价 |  |
| `cb_anal_convratio` | 转股比例 |  |
| `cb_anal_convvalue` | 转换价值 |  |
| `cb_anal_diluterate` | 转股稀释率(新增) |  |
| `cb_anal_doublelow` | 双低 | TRADEDATE |
| `cb_anal_impliedvol` | 隐含波动率(新增) | DEALDATE、RF |
| `cb_anal_lasttradingday` | 最后交易日 |  |
| `cb_anal_ldiluterate` | 对流通股稀释率(新增) |  |
| `cb_anal_noresetpubdate` | 转股价不修正公告日 | TRADEDATE |
| `cb_anal_nxcupn` | 下一付息日 |  |
| `cb_anal_ptm` | 剩余期限 |  |
| `cb_anal_putdecperiod` | 回售申报期 | TRADEDATE |
| `cb_anal_putnxtdate` | 下一回售条件起始日 | TRADEDATE |
| `cb_anal_puttrigdate` | 回售触发日期 | TRADEDATE |
| `cb_anal_puttrigprog` | 回售触发进度 | TRADEDATE |
| `cb_anal_puttrigratio` | 回售进度比例 | TRADEDATE |
| `cb_anal_puttrigsit` | 回售触发情况 | TRADEDATE |
| `cb_anal_resetdate` | 转股价修正日 | TRADEDATE |
| `cb_anal_resetdatehint` | 预计下修触发提示日 | TRADEDATE |
| `cb_anal_resetnxtdate` | 下一转股价修正起始日 | TRADEDATE |
| `cb_anal_resetpubdate` | 转股价修正公告日 | TRADEDATE |
| `cb_anal_resettrigdate` | 下修触发日期 | TRADEDATE |
| `cb_anal_resettrigprog` | 下修触发进度 | TRADEDATE |
| `cb_anal_resettrigratio` | 下修进度比例 | TRADEDATE |
| `cb_anal_resettrigsit` | 下修触发情况 | TRADEDATE |
| `cb_anal_straightbondpremium` | 纯债溢价 |  |
| `cb_anal_straightbondpremiumratio` | 纯债溢价率 |  |
| `cb_anal_straightbondvalue` | 纯债价值 |  |
| `cb_anal_underlyingmv` | 正股流通市值 | DEALDATE |
| `cb_anal_underlyingpb` | 正股市净率 |  |
| `cb_anal_underlyingpe` | 正股市盈率 |  |
| `cb_anal_ytm` | 到期收益率 |  |
| `cb_clause_calloption` | 相对赎回期 | ITEMSCODE |
| `cb_clause_calloption_conditionalredeemenddate` | 条件赎回截止日期(新增) |  |
| `cb_clause_calloption_conditionalredeemstartdate` | 条件赎回起始日期(新增) |  |
| `cb_clause_calloption_indicativedaten` | 不强赎提示公告日 |  |
| `cb_clause_calloption_indicativedatey` | 强赎提示公告日 |  |
| `cb_clause_calloption_interestdisposal` | 利息处理(新增) |  |
| `cb_clause_calloption_iswithtimeredemptionclause` | 是否有时点赎回条款(新增) |  |
| `cb_clause_calloption_noticedate` | 赎回公告日 |  |
| `cb_clause_calloption_recorddate` | 赎回登记日 |  |
| `cb_clause_calloption_redeemclause` | 时点赎回条款全文(新增) |  |
| `cb_clause_calloption_redeemitem` | 赎回条款(新增) |  |
| `cb_clause_calloption_redeemmaxspan` | 赎回触发计算最大时间区间(新增) |  |
| `cb_clause_calloption_redeemspan` | 赎回触发计算时间区间(新增) |  |
| `cb_clause_calloption_redemptionmemo` | 赎回价格说明(新增) |  |
| `cb_clause_calloption_redemptionprice` | 赎回价格(新增) |  |
| `cb_clause_calloption_redemptiontimesperyear` | 每年可赎回次数(新增) |  |
| `cb_clause_calloption_relativecalloptionperiod` | 相对赎回期(新增) |  |
| `cb_clause_calloption_timeredemptiontimes` | 时点赎回数(新增) |  |
| `cb_clause_calloption_triggerprice` | 赎回触发价 | TRADEDATE |
| `cb_clause_calloption_triggerproportion` | 赎回触发比例(新增) |  |
| `cb_clause_compensationinterest` | 补偿利率(公布) |  |
| `cb_clause_conversion` | 转股条款 | ITEMSCODE |
| `cb_clause_conversion2_bondlot` | 未转股余额(新增) |  |
| `cb_clause_conversion2_bondproportion` | 未转股比例(新增) |  |
| `cb_clause_conversion2_conversionproportion` | 转换比例(新增) |  |
| `cb_clause_conversion2_swapshareprice` | 转股价格(新增) |  |
| `cb_clause_conversion2_tosharepriceadjustitem` | 转股条款(新增) |  |
| `cb_clause_conversion_2` | 转股条款2 | ITEMSCODE、DEALDATE |
| `cb_clause_conversion_2_conversionproportion` | 转股价随派息调整(新增) |  |
| `cb_clause_conversion_2_forceconvertdate` | 强制转股日(新增) |  |
| `cb_clause_conversion_2_forceconvertprice` | 强制转股价格(新增) |  |
| `cb_clause_conversion_2_isforced` | 是否强制转股(新增) |  |
| `cb_clause_conversion_2_relativeswapsharemonth` | 相对转股期(新增) |  |
| `cb_clause_conversion_2_swapshareenddate` | 自愿转股终止日期(新增) |  |
| `cb_clause_conversion_2_swapsharestartdate` | 自愿转股起始日期(新增) |  |
| `cb_clause_exannoundate` | 最新行权公告日 | DEALDATE |
| `cb_clause_interest` | 利率类型 | ITEMSCODE |
| `cb_clause_interest_compensationinterest` | 补偿利率(新增) |  |
| `cb_clause_processmodeinterest` | 利息处理方式 |  |
| `cb_clause_putoption` | 相对回售期 | ITEMSCODE |
| `cb_clause_putoption_additionalpricememo` | 附加回售价格说明(新增) |  |
| `cb_clause_putoption_conditionalputbackenddate` | 条件回售截止日期(新增) |  |
| `cb_clause_putoption_conditionalputbackstartenddate` | 条件回售起始日期(新增) |  |
| `cb_clause_putoption_interestdisposing` | 利息处理(新增) |  |
| `cb_clause_putoption_noticedate` | 回售公告日 |  |
| `cb_clause_putoption_putbackadditionalcondition` | 附加回售条件(新增) |  |
| `cb_clause_putoption_putbackclause` | 无条件回售条款(新增) |  |
| `cb_clause_putoption_putbackenddate` | 无条件回售结束日期(新增) |  |
| `cb_clause_putoption_putbackperiod` | 无条件回售期(新增) |  |
| `cb_clause_putoption_putbackperiodobs` | 相对回售期(新增) |  |
| `cb_clause_putoption_putbackprice` | 无条件回售价(新增) |  |
| `cb_clause_putoption_putbackstartdate` | 无条件回售起始日期(新增) |  |
| `cb_clause_putoption_putbacktimesperyear` | 每年回售次数(新增) |  |
| `cb_clause_putoption_putbacktriggermaxspan` | 回售触发计算最大时间区间(新增) |  |
| `cb_clause_putoption_putbacktriggerspan` | 回售触发计算时间区间(新增) |  |
| `cb_clause_putoption_redeem_triggerproportion` | 回售触发比例(新增) |  |
| `cb_clause_putoption_resellingprice` | 回售价格(新增) |  |
| `cb_clause_putoption_resellingpriceexplaination` | 回售价格说明(新增) |  |
| `cb_clause_putoption_sellbackitem` | 条件回售条款全文(新增) |  |
| `cb_clause_putoption_timeputbackclause` | 时点回售条款全文(新增) |  |
| `cb_clause_putoption_timeputbacktimes` | 时点回售数(新增) |  |
| `cb_clause_putoption_triggerprice` | 回售触发价 | TRADEDATE |
| `cb_clause_reset` | 特别修正起始时间 | ITEMSCODE |
| `cb_clause_reset_isexitreset` | 是否有特别向下修正条款(新增) |  |
| `cb_clause_reset_item` | 特别向下修正条款全文 |  |
| `cb_clause_reset_referencepriceisanverage` | 是否为算术平均价(新增) |  |
| `cb_clause_reset_resetmaxtimespan` | 重设触发计算最大时间区间(新增) |  |
| `cb_clause_reset_resetperiodenddate` | 特别修正结束时间(新增) |  |
| `cb_clause_reset_resetrange` | 特别修正幅度(新增) |  |
| `cb_clause_reset_resetstartdate` | 特别修正起始时间(新增) |  |
| `cb_clause_reset_resettimeslimit` | 修正次数限制(新增) |  |
| `cb_clause_reset_resettimespan` | 重设触发计算时间区间(新增) |  |
| `cb_clause_reset_resettriggerratio` | 触发比例(新增) |  |
| `cb_clause_reset_stockpricelowestlimit` | 修正价格底线说明(新增) |  |
| `cb_clause_reset_timepointclause` | 时点修正条款全文(新增) |  |
| `cb_dq_amount` | 成交额 |  |
| `cb_dq_avgprice` | 成交均价 |  |
| `cb_dq_change` | 涨跌 |  |
| `cb_dq_close` | 收盘价 |  |
| `cb_dq_high` | 最高价 |  |
| `cb_dq_low` | 最低价 |  |
| `cb_dq_open` | 开盘价 |  |
| `cb_dq_pctchange` | 涨跌幅 |  |
| `cb_dq_preclose` | 前收盘价 |  |
| `cb_dq_stockamnt` | 正股成交额(新增) |  |
| `cb_dq_stockmktcap1` | 正股总市值1 | TRADEDATE |
| `cb_dq_stockmktcap2` | 正股总市值2 | TRADEDATE |
| `cb_dq_swing` | 振幅 | DEALDATE、PRICETYPE |
| `cb_dq_turn` | 换手率 |  |
| `cb_dq_volume` | 成交量 |  |
| `cb_holder_name` | 持有人名称 |  |
| `cb_holder_pct` | 持有人持有比例 |  |
| `cb_holder_quantity` | 持有人持有数量 |  |
| `cb_info_carrydate` | 起息日期 |  |
| `cb_info_code` | 转债代码 |  |
| `cb_info_conditionalcallprice` | 有条件赎回价 |  |
| `cb_info_conditionalputprice` | 有条件回售价 |  |
| `cb_info_convs_ed` | 停止转股日 |  |
| `cb_info_creditrating` | 信用级别 |  |
| `cb_info_creditratingagency` | 评级机构 |  |
| `cb_info_guarantor` | 担保人 |  |
| `cb_info_industry_csrc` | 证监会行业-中文 |  |
| `cb_info_industry_csrccode` | 证监会行业-代码 |  |
| `cb_info_industry_gics` | GICS行业-中文 |  |
| `cb_info_industry_gicscode` | GICS行业-代码 |  |
| `cb_info_industry_gicseng` | GICS行业-英文 |  |
| `cb_info_interestfrequency` | 年付息次数(新增) |  |
| `cb_info_interesttype` | 利率类型(新增) |  |
| `cb_info_issueamount` | 发行总额 |  |
| `cb_info_issueprice` | 发行价格 |  |
| `cb_info_issuer` | 发行人名称 |  |
| `cb_info_listeddate` | 上市日期 |  |
| `cb_info_maturitycallprice` | 到期赎回价 |  |
| `cb_info_maturitydate` | 到期日期 |  |
| `cb_info_name` | 转债简称 |  |
| `cb_info_outstandingbalance` | 债券余额(新增) |  |
| `cb_info_term` | 期限 |  |
| `cb_info_underlyingcode` | 正股代码 |  |
| `cb_info_underlyingname` | 正股简称 |  |
| `cb_list_floorsubscroffl` | 网下申购下限 |  |
| `cb_list_floorsubscronl` | 网上申购下限 |  |
| `cb_list_issuevolonl` | 网上发行数量(不含优先配售) |  |
| `cb_list_limitsubscroffl` | 网下申购上限 |  |
| `cb_list_limitsubscronl` | 网上申购上限 |  |
| `cb_list_rationvol` | 向老股东配售数量 |  |
| `cb_list_stepsizesubscroffl` | 网下申购步长 |  |
| `cb_list_stepsizesubscronl` | 网上申购步长 |  |
| `cb_list_volinstoff` | 网下向机构投资者发行数量(不含优先配售) |  |
| `cb_mq_stockamnt` | 正股月成交额(新增) |  |
| `cb_mq_stockaveturnover` | 正股月平均换手率(新增) |  |
| `cb_mq_stockavg` | 正股月均价(新增) |  |
| `cb_mq_stockchg` | 正股月涨跌(新增) |  |
| `cb_mq_stockclose` | 正股月收盘价(新增) |  |
| `cb_mq_stockhigh` | 正股月最高价(新增) |  |
| `cb_mq_stockhighclose` | 正股月最高收盘价(新增) |  |
| `cb_mq_stocklow` | 正股月最低价(新增) |  |
| `cb_mq_stocklowclose` | 正股月最低收盘价(新增) |  |
| `cb_mq_stockopen` | 正股月开盘价(新增) |  |
| `cb_mq_stockpctchg` | 正股月涨跌幅(新增) |  |
| `cb_mq_stockpreclose` | 正股月前收盘价(新增) |  |
| `cb_mq_stockswing` | 正股月振幅(新增) |  |
| `cb_mq_stockturnover` | 正股月换手率(新增) |  |
| `cb_mq_stockvol` | 正股月成交量(新增) |  |
| `cb_mq_swing` | 月振幅 | DEALDATE、PRICETYPE |
| `cb_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `cb_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `cb_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `cb_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `cb_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `cb_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `cb_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `cb_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `cb_pq_highclose` | 区间最高收盘价 | StartDate、EndDate |
| `cb_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `cb_pq_lowclose` | 区间最低收盘价 | StartDate、EndDate |
| `cb_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `cb_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `cb_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `cb_pq_stockavg` | 正股区间均价(新增) | TD1、TD2 |
| `cb_pq_stockchg` | 正股区间涨跌(新增) | TD1、TD2 |
| `cb_pq_stockpctchg` | 正股区间涨跌幅(新增) | TD1、TD2 |
| `cb_pq_swing` | 区间振幅 | StartDate、EndDate、PRICETYPE |
| `cb_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `cb_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `cb_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `cb_warrant_issuetype` | 发行方式(新增) |  |
| `cb_wq_stockamnt` | 正股周成交额(新增) |  |
| `cb_wq_stockaveturnover` | 正股周平均换手率(新增) |  |
| `cb_wq_stockavg` | 正股周均价(新增) |  |
| `cb_wq_stockchg` | 正股周涨跌(新增) |  |
| `cb_wq_stockclose` | 正股周收盘价(新增) |  |
| `cb_wq_stockhigh` | 正股周最高价(新增) |  |
| `cb_wq_stockhighclose` | 正股周最高收盘价(新增) |  |
| `cb_wq_stocklow` | 正股周最低价(新增) |  |
| `cb_wq_stocklowclose` | 正股周最低收盘价(新增) |  |
| `cb_wq_stockopen` | 正股周开盘价(新增) |  |
| `cb_wq_stockpctchg` | 正股周涨跌幅(新增) |  |
| `cb_wq_stockpreclose` | 正股周前收盘价(新增) |  |
| `cb_wq_stockswing` | 正股周振幅(新增) |  |
| `cb_wq_stockturnover` | 正股周换手率(新增) |  |
| `cb_wq_stockvol` | 正股周成交量(新增) |  |
| `cb_wq_swing` | 周振幅 | DEALDATE、PRICETYPE |
| `cb_yq_stockamnt` | 正股年成交额(新增) |  |
| `cb_yq_stockaveturnover` | 正股年平均换手率(新增) |  |
| `cb_yq_stockavg` | 正股年均价(新增) |  |
| `cb_yq_stockchg` | 正股年涨跌(新增) |  |
| `cb_yq_stockclose` | 正股年收盘价(新增) |  |
| `cb_yq_stockhigh` | 正股年最高价(新增) |  |
| `cb_yq_stockhighclose` | 正股年最高收盘价(新增) |  |
| `cb_yq_stocklow` | 正股年最低价(新增) |  |
| `cb_yq_stocklowclose` | 正股年最低收盘价(新增) |  |
| `cb_yq_stockopen` | 正股年开盘价(新增) |  |
| `cb_yq_stockpctchg` | 正股年涨跌幅(新增) |  |
| `cb_yq_stockpreclose` | 正股年前收盘价(新增) |  |
| `cb_yq_stockswing` | 正股年振幅(新增) |  |
| `cb_yq_stockturnover` | 正股年换手率(新增) |  |
| `cb_yq_stockvol` | 正股年成交量(新增) |  |
| `cb_yq_swing` | 年振幅 | DEALDATE、PRICETYPE |

<a id="分类-港股"></a>

## 港股（734 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `hks_ard_bs_perp_min` | 永续债_归属于少数股东 | REPORTDATE |
| `hks_ard_bs_perp_par` | 永续债_归属于母公司股东 | REPORTDATE |
| `hks_ard_bs_perpetual` | 永续债_合计 | REPORTDATE |
| `hks_ard_is_investmentproperty` | 投资物业公允价值变动(公布值) | REPORTDATE、TYPE |
| `hks_ard_is_sales` | 总营业收入(公布值) | REPORTDATE、TYPE |
| `hks_bs_ap` | 预收款项 | YEARBASIS、REPORTDATE、TYPE |
| `hks_bs_cl` | 合同负债 | YEARBASIS、REPORTDATE、TYPE |
| `hks_bs_perp_min` | 永续债_归属于少数股东 | YEARBASIS、REPORTDATE、TYPE |
| `hks_bs_perp_par` | 永续债_归属于母公司股东 | YEARBASIS、REPORTDATE、TYPE |
| `hks_bs_perpetual` | 永续债_合计 | YEARBASIS、REPORTDATE、TYPE |
| `hks_bs_rf` | 受限资金 | YEARBASIS、REPORTDATE、TYPE |
| `hks_cal_bs_1017` | 非流动负债合计 | Year |
| `hks_cal_bs_128` | 负债合计 | Year |
| `hks_cal_bs_136` | 少数股东权益 | Year |
| `hks_cal_bs_140` | 归属母公司股东权益 | Year |
| `hks_cal_bs_145` | 股东权益合计 | Year |
| `hks_cal_bs_25` | 流动资产合计 | Year |
| `hks_cal_bs_46` | 非流动资产合计 | Year |
| `hks_cal_bs_74` | 资产总计 | Year |
| `hks_cal_bs_93` | 流动负债合计 | Year |
| `hks_cal_cs_39` | 经营活动产生的现金流量净额 | Year |
| `hks_cal_cs_59` | 投资活动产生的现金流量净额 | Year |
| `hks_cal_cs_77` | 筹资活动产生的现金流量净额 | Year |
| `hks_cal_cs_78` | 汇率变动影响 | Year |
| `hks_cal_cs_82` | 现金及现金等价物净增加额 | Year |
| `hks_cal_cs_83` | 现金及现金等价物期初余额 | Year |
| `hks_cal_cs_84` | 现金及现金等价物期末余额 | Year |
| `hks_cal_is_10` | 营业成本 | Year |
| `hks_cal_is_1016` | 除税前利润 | Year |
| `hks_cal_is_1032` | 总营业支出 | Year |
| `hks_cal_is_1041` | 营业利润 | Year |
| `hks_cal_is_15` | 管理费用 | Year |
| `hks_cal_is_47` | 销售费用 | Year |
| `hks_cal_is_56` | 所得税 | Year |
| `hks_cal_is_60` | 除税后利润(净利润) | Year |
| `hks_cal_is_61` | 归属母公司股东的净利润 | Year |
| `hks_cal_is_62` | 少数股东损益 | Year |
| `hks_cal_is_83` | 营业总收入 | Year |
| `hks_cal_is_9` | 营业收入 | Year |
| `hks_cal_is_92` | 营业开支 | Year |
| `hks_cs` | 26版财务指标 | ITEMSCODE、YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `hks_div_accmdivrpt` | 现金分红总额 | REPORTDATE |
| `hks_div_aualaccmdiv` | 年度累计分红总额 |  |
| `hks_div_aualaccmdiv_i` | 年度累计分红总额 | Year |
| `hks_div_cashbftax` | 每股股利(税前) | REPORTDATE |
| `hks_div_cashbftax_ex` | 每股股利(税前,剔除特别派息) | REPORTDATE |
| `hks_div_ccyoptend` | 股东行使现金分红货币选择权截止日 | REPORTDATE |
| `hks_div_ccyoptstart` | 股东行使现金分红货币选择权起始日 | REPORTDATE |
| `hks_div_freq` | 年度现金分红次数 |  |
| `hks_div_freqard` | 年度现金分红次数(已宣告) | Year |
| `hks_div_payoutratio` | 年度现金分红比例 |  |
| `hks_dq_amount` | 成交额 |  |
| `hks_dq_avgprice` | 均价 |  |
| `hks_dq_change` | 涨跌 |  |
| `hks_dq_close` | 收盘价 |  |
| `hks_dq_high` | 最高价 |  |
| `hks_dq_low` | 最低价 |  |
| `hks_dq_mv` | 流通市值 |  |
| `hks_dq_open` | 开盘价 |  |
| `hks_dq_pctchange` | 涨跌幅 |  |
| `hks_dq_preclose` | 前收盘价 |  |
| `hks_dq_turn` | 换手率 |  |
| `hks_dq_volume` | 成交量 |  |
| `hks_esg_invention` | 有效专利总数 | TRADEDATE |
| `hks_est_cagr_np` | 未来3年净利润复合年增长率 | TRADEDATE |
| `hks_ev_cashdvd` | 现金股息每股派息 | DEALDATE |
| `hks_ev_exdate` | 现金股息除权日 | TRADEDATE |
| `hks_ev_paydate` | 现金股息派息日 | TRADEDATE |
| `hks_fa_adminexpense_ttm` | 管理费用(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_adminexpensetogr` | 管理费用/营业总收入 | REPORTDATE |
| `hks_fa_adminexpensetogr_ttm` | 管理费用/营业总收入(TTM) | REPORTDATE |
| `hks_fa_apturn` | 应付账款周转率 | REPORTDATE |
| `hks_fa_apturndays` | 应付账款周转天数 | REPORTDATE |
| `hks_fa_arturn` | 应收账款周转率 | REPORTDATE |
| `hks_fa_arturndays` | 应收账款周转天数 | REPORTDATE |
| `hks_fa_assetstoequity` | 权益乘数 | REPORTDATE |
| `hks_fa_assetsturn` | 总资产周转率 | REPORTDATE |
| `hks_fa_assetsturn_day` | 总资产周转天数 | REPORTDATE |
| `hks_fa_bps` | 每股净资产(BPS) | REPORTDATE |
| `hks_fa_bps_new` | 每股净资产BPS(最新公告) |  |
| `hks_fa_cagr_netprofit` | 净利润复合年增长率 | Year、N |
| `hks_fa_cagr_netprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益(N年,增长率)_GSD | REPORTDATE |
| `hks_fa_cagr_totalprofit` | 利润总额复合年增长率_GSD |  |
| `hks_fa_cagr_tr` | 营业总收入复合年增长率 | Year、N |
| `hks_fa_capitalizedtoda` | 资本支出/折旧和摊销 | REPORTDATE |
| `hks_fa_cashflow_ttm` | 现金及现金等价物净增加额(TTM) |  |
| `hks_fa_cashflow_ttm2` | 现金净流量(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_cashratio` | 保守速动比率 | REPORTDATE |
| `hks_fa_cashtoliqdebt` | 货币资金／流动负债 | REPORTDATE |
| `hks_fa_catoassets` | 流动资产／总资产 | REPORTDATE |
| `hks_fa_caturn` | 流动资产周转率 | REPORTDATE |
| `hks_fa_ce` | 资本性支出(公布值) | REPORTDATE、TYPE |
| `hks_fa_cfps` | 每股现金流量净额 | REPORTDATE |
| `hks_fa_cfps_ttm` | 每股现金流量净额(TTM) |  |
| `hks_fa_cfps_ttm2` | 每股现金流量净额(TTM) | TRADEDATE、CURTYPE |
| `hks_fa_cogstosales` | 销售成本率 | REPORTDATE |
| `hks_fa_connp_ttm` | 持续经营净利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_connptoprofit_ttm` | 持续经营净利润/税后利润(TTM) | REPORTDATE |
| `hks_fa_cost_ttm` | 营业成本-非金融类(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_current` | 流动比率 | REPORTDATE |
| `hks_fa_currentdebttodebt` | 流动负债／负债合计 | REPORTDATE |
| `hks_fa_da2` | 当期计提折旧与摊销 | REPORTDATE、CURTYPE |
| `hks_fa_debttoassets` | 资产负债率 | REPORTDATE |
| `hks_fa_debttoequity` | 产权比率 | REPORTDATE |
| `hks_fa_deductedprofit` | 扣除非经常损益后净利润 | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_deductedprofit_ttm` | 扣除非经常性损益后的净利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_deductedprofittoprofit` | 扣除非经常损益后的净利润/净利润 | REPORTDATE |
| `hks_fa_dps` | 每股派息 |  |
| `hks_fa_dps_ard` | 每股派息(公布值) | REPORTDATE |
| `hks_fa_dupont_assetstoequity` | 权益乘数(杜邦分析) | REPORTDATE |
| `hks_fa_dupont_ebittosales` | 息税前利润/营业总收入 | REPORTDATE |
| `hks_fa_dupont_intburden` | 利润总额/息税前利润 | REPORTDATE |
| `hks_fa_dupont_np` | 归属母公司股东的净利润/净利润 | REPORTDATE |
| `hks_fa_dupont_nptosales` | 净利润/营业总收入 | REPORTDATE |
| `hks_fa_dupont_roe` | 平均净资产收益率 | REPORTDATE |
| `hks_fa_dupont_taxburden` | 净利润/利润总额 | REPORTDATE |
| `hks_fa_ebit` | EBIT(反推法) | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_ebit2` | 息税前利润(正向法) | REPORTDATE、TYPE |
| `hks_fa_ebit3` | 息税前利润(正向法) | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_ebit_ttm` | 息税前利润(TTM反推法) | REPORTDATE、CURTYPE |
| `hks_fa_ebitda` | EBITDA(反推法) | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_ebitda2` | 息税折旧摊销前利润(正向法) | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_ebitda_ttm` | EBITDA(TTM反推法) | REPORTDATE、CURTYPE |
| `hks_fa_ebitdatodebt` | 息税折旧摊销前利润/负债合计 | REPORTDATE |
| `hks_fa_ebitdatosales` | EBITDA/营业总收入 | REPORTDATE |
| `hks_fa_ebitps2` | 每股息税前利润 | REPORTDATE、CURTYPE |
| `hks_fa_ebittoassets_ttm` | 息税前利润(TTM)/总资产 | REPORTDATE |
| `hks_fa_ebittointerest` | 已获利息倍数(EBIT/利息费用) | REPORTDATE |
| `hks_fa_ebt_ttm2` | 利润总额(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_ebttoor_ttm` | 利润总额/营业收入(TTM) | REPORTDATE |
| `hks_fa_eps_adjust2` | 每股收益-最新股本摊薄 | REPORTDATE、CURTYPE |
| `hks_fa_eps_basic` | 每股收益EPS-基本 | REPORTDATE |
| `hks_fa_eps_diluted` | 每股收益EPS-稀释 | REPORTDATE |
| `hks_fa_eps_diluted3` | 每股收益-期末股本摊薄 | REPORTDATE、CURTYPE |
| `hks_fa_eps_ttm` | 每股收益EPS(TTM) |  |
| `hks_fa_eps_ttm2` | 每股收益(TTM) | TRADEDATE、CURTYPE |
| `hks_fa_equity_mrq2` | 归属母公司股东权益(MRQ) | TRADEDATE、CURTYPE |
| `hks_fa_equitytodebt` | 归属母公司股东的权益／负债合计 | REPORTDATE |
| `hks_fa_equitytointerestdebt` | 归属母公司股东的权益/带息债务 | REPORTDATE |
| `hks_fa_equitytototalcapital` | 归属母公司股东的权益／投入资本 | REPORTDATE |
| `hks_fa_exinterestdebt_current` | 无息流动负债 | REPORTDATE |
| `hks_fa_exinterestdebt_noncurrent2` | 无息非流动负债 | REPORTDATE、CURTYPE |
| `hks_fa_expense_ttm` | 营业支出-金融类(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_expensetosales_ttm` | 销售期间费用率(TTM) | REPORTDATE |
| `hks_fa_faturn` | 固定资产周转率 | REPORTDATE |
| `hks_fa_fcfe2` | 股权自由现金流量FCFE | REPORTDATE、CURTYPE |
| `hks_fa_fcfeps2` | 每股股东自由现金流量 | REPORTDATE、CURTYPE |
| `hks_fa_fcff2` | 企业自由现金流量 | REPORTDATE、CURTYPE |
| `hks_fa_fcffps2` | 每股企业自由现金流量 | REPORTDATE、CURTYPE |
| `hks_fa_finaexpense_ttm` | 财务费用(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_finaexpensetogr` | 财务费用/营业总收入 | REPORTDATE |
| `hks_fa_finaexpensetogr_ttm` | 财务费用/营业总收入(TTM) | REPORTDATE |
| `hks_fa_financecashflow_ttm` | 筹资活动现金净流量(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_gc_ttm` | 营业总成本(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_gctogr` | 营业总成本/营业总收入 | REPORTDATE |
| `hks_fa_gctogr_ttm` | 营业总成本/营业总收入(TTM) | REPORTDATE |
| `hks_fa_gr_ttm` | 营业总收入(TTM) |  |
| `hks_fa_gr_ttm2` | 营业总收入(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_grossmargin2` | 毛利 | REPORTDATE、CURTYPE |
| `hks_fa_grossmargin_ttm` | 毛利(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_grossprofitmargin` | 销售毛利率 | REPORTDATE |
| `hks_fa_grossprofitmargin_ttm` | 销售毛利率(TTM) |  |
| `hks_fa_grossprofitmargin_ttm2` | 销售毛利率(TTM) | REPORTDATE |
| `hks_fa_grps2` | 每股营业总收入 | REPORTDATE、CURTYPE |
| `hks_fa_interestdebt2` | 带息债务 | REPORTDATE、CURTYPE |
| `hks_fa_interestdebttototalcapital` | 带息债务/全部投入资本 | REPORTDATE |
| `hks_fa_interestexpense_ttm` | 利息支出(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_investcapital2` | 全部投入资本 | REPORTDATE、CURTYPE |
| `hks_fa_investcashflow_ttm` | 投资活动现金净流量(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_investincome_ttm` | 价值变动净收益(TTM) | CURTYPE |
| `hks_fa_investincome_ttm2` | 价值变动净收益(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_investincometoebt` | 价值变动净收益/利润总额 | REPORTDATE |
| `hks_fa_investincometoebt_ttm` | 价值变动净收益/利润总额(TTM) | REPORTDATE |
| `hks_fa_invturn` | 存货周转率 | REPORTDATE |
| `hks_fa_invturndays` | 存货周转天数 | REPORTDATE |
| `hks_fa_longdebtodebt` | 非流动负债／负债合计 | REPORTDATE |
| `hks_fa_longdebttoworkingcapital` | 长期债务与营运资金比率 | REPORTDATE |
| `hks_fa_minorityinterest_ttm` | 少数股东损益(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_ncatoassets` | 非流动资产／总资产 | REPORTDATE |
| `hks_fa_netdebt2` | 净债务 | REPORTDATE、CURTYPE |
| `hks_fa_netdebtratio` | 净负债率 | REPORTDATE |
| `hks_fa_netdebtratio_ard` | 净负债率(公告值) | REPORTDATE |
| `hks_fa_netprofit_ttm` | 归属母公司股东的净利润(TTM) |  |
| `hks_fa_netprofit_ttm2` | 归属母公司股东的净利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_netprofitmargin` | 销售净利率 | REPORTDATE |
| `hks_fa_netprofitmargin_ttm` | 销售净利率(TTM) |  |
| `hks_fa_netprofitmargin_ttm2` | 销售净利率(TTM) | REPORTDATE |
| `hks_fa_netprofittoassets` | 总资产净利率-不含少数股东损益(TTM) | REPORTDATE |
| `hks_fa_netprofittoor_ttm` | 归属母公司股东的净利润/营业收入(TTM) | REPORTDATE |
| `hks_fa_networkingcapital2` | 净营运资本 | REPORTDATE、CURTYPE |
| `hks_fa_nogaapeps` | 每股收益EPS-基本(Non-GAAP) | REPORTDATE、TYPE |
| `hks_fa_nogaapparent` | 归属母公司股东的净利润(Non-GAAP) | REPORTDATE、TYPE |
| `hks_fa_nogaapprofit` | 净利润(Non-GAAP) | REPORTDATE、TYPE、CURTYPE |
| `hks_fa_nonconnp_ttm` | 非持续经营净利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_nonop_ttm` | 非营业利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_nonoperateprofittoebt` | 营业外收支净额/利润总额 | REPORTDATE |
| `hks_fa_nonoperateprofittoebt_ttm` | 营业外收支净额/利润总额(TTM) | REPORTDATE |
| `hks_fa_nonoptoebt_ttm` | 非营业利润/利润总额(TTM) | REPORTDATE |
| `hks_fa_nptocostexpense` | 成本费用利润率_GSD | REPORTDATE |
| `hks_fa_ocfps` | 每股经营现金净流量 | REPORTDATE |
| `hks_fa_ocfps_ttm` | 每股经营现金净流量(TTM) |  |
| `hks_fa_ocfps_ttm2` | 每股经营活动产生的现金流量净额(TTM) | TRADEDATE、CURTYPE |
| `hks_fa_ocftodebt` | 经营活动产生的现金流量净额／负债合计 | REPORTDATE |
| `hks_fa_ocftointerestdebt` | 经营活动产生的现金流量净额/带息债务 | REPORTDATE |
| `hks_fa_ocftoliqdebt` | 经营活动产生的现金流量净额／流动负债 | REPORTDATE |
| `hks_fa_ocftonetdebt` | 经营活动产生的现金流量净额/净债务 | REPORTDATE |
| `hks_fa_ocftooperateincome` | 经营活动产生的现金流量净额/经营活动净收益 | REPORTDATE |
| `hks_fa_ocftooperateincome_ttm` | 经营活动产生的现金流量净额/经营活动净收益(TTM) | REPORTDATE |
| `hks_fa_ocftosales` | 经营活动产生的现金流量净额／营业收入 | REPORTDATE |
| `hks_fa_ocftosales_ttm` | 经营活动产生的现金流量净额／营业收入(TTM) |  |
| `hks_fa_ocftosales_ttm2` | 经营活动产生的现金流量净额/营业收入(TTM) | REPORTDATE |
| `hks_fa_op_ttm` | 营业利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_operatecashflow_ttm` | 经营活动产生的现金流量净额(TTM) |  |
| `hks_fa_operatecashflow_ttm2` | 经营活动现金净流量(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_operatecashflowtoop_ttm` | 经营活动产生的现金流量净额/营业利润(TTM) | REPORTDATE |
| `hks_fa_operateexpense_ttm` | 销售费用(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_operateexpensetogr` | 销售费用/营业总收入 | REPORTDATE |
| `hks_fa_operateexpensetogr_ttm` | 销售费用/营业总收入(TTM) | REPORTDATE |
| `hks_fa_operateincome_ttm` | 经营活动净收益(TTM) | CURTYPE |
| `hks_fa_operateincome_ttm2` | 经营活动净收益(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_operateincometoebt` | 经营活动净收益/利润总额 | REPORTDATE |
| `hks_fa_operateincometoebt_ttm` | 经营活动净收益/利润总额(TTM) | REPORTDATE |
| `hks_fa_optodebt` | 营业利润／负债合计 | REPORTDATE |
| `hks_fa_optoebt` | 营业利润／利润总额 | REPORTDATE |
| `hks_fa_optoebt_ttm` | 营业利润／利润总额(TTM) |  |
| `hks_fa_optoebt_ttm2` | 营业利润/利润总额(TTM) | REPORTDATE |
| `hks_fa_optogr` | 营业利润/营业总收入 | REPORTDATE |
| `hks_fa_optogr_ttm` | 营业利润/营业总收入(TTM) | REPORTDATE |
| `hks_fa_optoliqdebt` | 营业利润／流动负债 | REPORTDATE |
| `hks_fa_optoor_ttm` | 营业利润/营业收入(TTM) | REPORTDATE |
| `hks_fa_or_ttm` | 营业收入(TTM) |  |
| `hks_fa_or_ttm2` | 营业收入(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_orps` | 每股营业收入 | REPORTDATE |
| `hks_fa_orps_ttm` | 每股营业收入(TTM) | TRADEDATE、CURTYPE |
| `hks_fa_periodexpense_ttm` | 期间费用(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_profit_ttm2` | 净利润(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_profitpp` | 人均创利 |  |
| `hks_fa_profittogr_ttm` | 净利润/营业总收入(TTM) | REPORTDATE |
| `hks_fa_quick` | 速动比率 | REPORTDATE |
| `hks_fa_retainedearnings2` | 留存收益 | REPORTDATE、CURTYPE |
| `hks_fa_retainedps2` | 每股留存收益 | REPORTDATE、CURTYPE |
| `hks_fa_revenuepp` | 人均创收 |  |
| `hks_fa_roa` | 总资产净利率(ROA) | REPORTDATE |
| `hks_fa_roa2` | 总资产报酬率ROA | REPORTDATE |
| `hks_fa_roa2_ttm` | 总资产报酬率(TTM) | REPORTDATE |
| `hks_fa_roa2_yearly` | 总资产报酬率(年化) | REPORTDATE |
| `hks_fa_roa_ttm` | 总资产净利率(ROA,TTM) |  |
| `hks_fa_roa_ttm2` | 总资产净利率(TTM) | REPORTDATE |
| `hks_fa_roa_yearly` | 总资产净利率(ROA,Yearly) | REPORTDATE |
| `hks_fa_roe` | 净资产收益率(ROE) | REPORTDATE |
| `hks_fa_roe_deducted` | 净资产收益率(扣除) | REPORTDATE |
| `hks_fa_roe_diluted` | 净资产收益率ROE(摊薄) | REPORTDATE |
| `hks_fa_roe_exdiluted` | 净资产收益率ROE(扣除/摊薄) | REPORTDATE |
| `hks_fa_roe_ttm` | 净资产收益率(ROE,TTM) |  |
| `hks_fa_roe_ttm2` | 净资产收益率(TTM) | REPORTDATE |
| `hks_fa_roe_yearly` | 净资产收益率(ROE,Yearly) | REPORTDATE |
| `hks_fa_roic` | 投入资本回报率(ROIC) | REPORTDATE |
| `hks_fa_roic1` | 投入资本回报率ROIC | REPORTDATE |
| `hks_fa_roic2_ttm` | 投入资本回报率ROIC(TTM) | REPORTDATE |
| `hks_fa_roic3_ttm` | 投入资本回报率(TTM,息前税后) | REPORTDATE |
| `hks_fa_roic_ttm` | 投入资本回报率(ROIC,TTM) |  |
| `hks_fa_roic_ttm2` | 投入资本回报率(TTM) | REPORTDATE |
| `hks_fa_roic_yearly` | 投入资本回报率(ROIC,Yearly) | REPORTDATE |
| `hks_fa_salarypp` | 人均薪酬 |  |
| `hks_fa_stdebtratio` | 现金短债比(公告值) | REPORTDATE |
| `hks_fa_tangibleasset2` | 有形资产 | REPORTDATE、CURTYPE |
| `hks_fa_tangibleassetstoassets` | 有形资产/总资产 | REPORTDATE |
| `hks_fa_tangibleassettodebt` | 有形资产/负债合计 | REPORTDATE |
| `hks_fa_tangibleassettointerestdebt` | 有形资产/带息债务 | REPORTDATE |
| `hks_fa_tangibleassettonetdebt` | 有形资产/净债务 | REPORTDATE |
| `hks_fa_tax_ttm` | 所得税(TTM) | REPORTDATE、CURTYPE |
| `hks_fa_taxtoebt` | 税项／利润总额 | REPORTDATE |
| `hks_fa_taxtoebt_ttm` | 税项／利润总额(TTM) |  |
| `hks_fa_taxtoebt_ttm2` | 税项/利润总额(TTM) | REPORTDATE |
| `hks_fa_turndays` | 营业周期 | REPORTDATE |
| `hks_fa_workingcapital2` | 营运资本 | REPORTDATE、CURTYPE |
| `hks_fa_yoy_or` | 营业收入(同比增长率) | REPORTDATE |
| `hks_fa_yoy_tr` | 营业总收入(同比增长率) | REPORTDATE |
| `hks_fa_yoyassets` | 资产总计(相对年初增长率) | REPORTDATE |
| `hks_fa_yoybps` | 每股净资产(相对年初增长率) | REPORTDATE |
| `hks_fa_yoyebt` | 利润总额(同比增长率) | REPORTDATE |
| `hks_fa_yoyeps_basic` | 基本每股收益(同比增长率) | REPORTDATE |
| `hks_fa_yoyeps_diluted` | 稀释每股收益(同比增长率) | REPORTDATE |
| `hks_fa_yoyequity` | 归属母公司股东的权益(相对年初增长率) | REPORTDATE |
| `hks_fa_yoynetprofit` | 归属母公司股东的净利润(同比增长率) | REPORTDATE |
| `hks_fa_yoynetprofit_deducted` | 归属母公司股东的净利润-扣除非经常损益(同比增长率) | REPORTDATE |
| `hks_fa_yoyocf` | 经营活动产生的现金流量净额(同比增长率) | REPORTDATE |
| `hks_fa_yoyocfps` | 每股经营活动产生的现金流量净额(同比增长率) | REPORTDATE |
| `hks_fa_yoyop2` | 营业利润(同比增长率) | REPORTDATE |
| `hks_fa_yoyroe` | 净资产收益率(摊薄)(同比增长率) | REPORTDATE |
| `hks_fellow_collection_t` | 区间再融资募集资金合计 | StartDate、EndDate |
| `hks_growth_asset_1y` | 资产总计(近1年增长率) |  |
| `hks_growth_asset_3y` | 资产总计(近3年增长率) |  |
| `hks_growth_assets` | 资产总计(N年,增长率) | REPORTDATE、N |
| `hks_growth_bps_1y` | 每股净资产(近1年增长率) |  |
| `hks_growth_bps_3y` | 每股净资产(近3年增长率) |  |
| `hks_growth_debt_1y` | 负债合计(近1年增长率) |  |
| `hks_growth_debt_3y` | 负债合计(近3年增长率) |  |
| `hks_growth_ebt` | 利润总额(N年,增长率) | REPORTDATE、N |
| `hks_growth_ebt_1y` | 税前利润(近1年增长率) |  |
| `hks_growth_ebt_3y` | 税前利润(近3年增长率) |  |
| `hks_growth_eps_1y` | 基本每股收益(近1年增长率) |  |
| `hks_growth_eps_3y` | 基本每股收益(近3年增长率) |  |
| `hks_growth_equity` | 归属母公司股东的权益(N年,增长率) | REPORTDATE、N |
| `hks_growth_equity_1y` | 归属母公司股东的权益(近1年增长率) |  |
| `hks_growth_equity_3y` | 归属母公司股东的权益(近3年增长率) |  |
| `hks_growth_gc` | 营业总成本(N年,增长率) | REPORTDATE、N |
| `hks_growth_gp_1y` | 毛利(近1年增长率) |  |
| `hks_growth_gp_3y` | 毛利(近3年增长率) |  |
| `hks_growth_gr` | 营业总收入(N年,增长率) | REPORTDATE、N |
| `hks_growth_investincome` | 价值变动净收益(N年,增长率) | REPORTDATE、N |
| `hks_growth_netprofit` | 归属母公司股东的净利润(N年,增长率) | REPORTDATE、N |
| `hks_growth_np_1y` | 归属母公司股东的净利润(近1年增长率) |  |
| `hks_growth_np_3y` | 归属母公司股东的净利润(近3年增长率) |  |
| `hks_growth_ocf` | 经营活动产生的现金流量净额(N年,增长率) | REPORTDATE、N |
| `hks_growth_op` | 营业利润(N年,增长率) | REPORTDATE、N |
| `hks_growth_op_1y` | 营业利润(近1年增长率) |  |
| `hks_growth_op_3y` | 营业利润(近3年增长率) |  |
| `hks_growth_operateincome` | 经营活动净收益(N年,增长率) | REPORTDATE、N |
| `hks_growth_or` | 营业收入(N年,增长率) | REPORTDATE、N |
| `hks_growth_profittosales` | 销售利润率(N年,增长率) | REPORTDATE、N |
| `hks_growth_roe` | 净资产收益率(N年,增长率) | REPORTDATE、N |
| `hks_growth_sales_1y` | 营业收入(近1年增长率) |  |
| `hks_growth_sales_3y` | 营业收入(近3年增长率) |  |
| `hks_growth_totalequity` | 股东权益(N年,增长率) | REPORTDATE、N |
| `hks_growth_totalequity_1y` | 股东权益(近1年增长率) |  |
| `hks_growth_totalequity_3y` | 股东权益(近3年增长率) |  |
| `hks_holder_equitytype` | 大股东权益类型 | DEALDATE、TopN |
| `hks_holder_name` | 股东名称 |  |
| `hks_holder_pct` | 持股比例 |  |
| `hks_holder_quantity` | 持股数量 |  |
| `hks_info_address` | 注册地详细地址 |  |
| `hks_info_area` | 注册地所在国家或地区 |  |
| `hks_info_auditor` | 审计机构 |  |
| `hks_info_banks` | 主要往来银行 |  |
| `hks_info_capital` | 注册资本 |  |
| `hks_info_chairman` | 集团主席(法人代表) |  |
| `hks_info_cik` | CIK代码 |  |
| `hks_info_code` | 交易代码 |  |
| `hks_info_codechangedate` | 证券代码变更日期 | TRADEDATE |
| `hks_info_compname` | 中文名称 |  |
| `hks_info_compnameeng` | 英文名称 |  |
| `hks_info_cur` | 记帐本位币 |  |
| `hks_info_cur2` | 记账本位币 | REPORTDATE |
| `hks_info_email` | 电邮地址 |  |
| `hks_info_fax` | 传真号码 |  |
| `hks_info_fiscaldate` | 会计年结日 |  |
| `hks_info_founddate` | 成立日期 |  |
| `hks_info_indexcode_citic` | 所属中信证券港股通指数代码(港股) | TRADEDATE、TYPE |
| `hks_info_indexcode_us` | 所属Wind行业指数代码(美股) | TRADEDATE、TYPE |
| `hks_info_indexcode_wind` | 所属Wind行业指数代码(港股) | TRADEDATE、TYPE |
| `hks_info_indexn_us` | 所属Wind行业指数名称(美股) | TRADEDATE、TYPE |
| `hks_info_indexname_citic` | 所属中信证券港股通指数名称(港股) | TRADEDATE、TYPE |
| `hks_info_indexname_hs` | 所属恒生综合行业指数名称 | TRADEDATE |
| `hks_info_industry_citic` | 所属中信行业名称(港股) | TRADEDATE、TYPE |
| `hks_info_industry_citiccode` | 所属中信行业代码(港股) | TRADEDATE、TYPE |
| `hks_info_industry_gics` | GICS行业 |  |
| `hks_info_industry_gicscode` | GICS行业代码 |  |
| `hks_info_industry_hs` | 所属恒生行业 | Category |
| `hks_info_industry_hscode` | 所属恒生行业代码 | TYPE |
| `hks_info_industry_sic` | 所属SIC行业名称(美股) | TRADEDATE、TYPE |
| `hks_info_industry_siccode` | 所属SIC行业代码(美股) | TRADEDATE、TYPE |
| `hks_info_industry_sw` | 所属申万行业名称(港股) | TRADEDATE、TYPE |
| `hks_info_industry_sw_2021` | 所属申万行业名称(港股)(2021) | TRADEDATE、TYPE |
| `hks_info_industry_swcode` | 所属申万行业代码(港股) | TRADEDATE、TYPE |
| `hks_info_industry_swcode_2021` | 所属申万行业代码(港股)(2021) | TRADEDATE、TYPE |
| `hks_info_isincode` | ISIN代码 |  |
| `hks_info_listmarket` | 上市地 |  |
| `hks_info_lotsize` | 每手股数 | DEALDATE |
| `hks_info_name` | 证券简称 |  |
| `hks_info_parvalue` | 每股面值 |  |
| `hks_info_phone` | 电话号码 |  |
| `hks_info_precode` | 证券曾用Wind代码 | TRADEDATE |
| `hks_info_ro` | 每份DR代表股数 |  |
| `hks_info_ro2` | 每份DR代表股份数 | TRADEDATE |
| `hks_info_secy` | 公司秘书 |  |
| `hks_info_spacornot` | 是否SPAC上市 |  |
| `hks_info_tradecur` | 交易币种 |  |
| `hks_info_volunit` | 单位交易量 |  |
| `hks_info_website` | 公司网址 |  |
| `hks_ipo_acpdt` | 证监会接收境外发行材料日期 |  |
| `hks_ipo_amount` | 首发数量 |  |
| `hks_ipo_announcedate` | 招股公告日 |  |
| `hks_ipo_backmechanism` | 是否触发回拨机制 |  |
| `hks_ipo_bank` | 首发收款银行 |  |
| `hks_ipo_collection` | 首发募资总额 |  |
| `hks_ipo_collection_oldshares` | 股东售股金额 |  |
| `hks_ipo_cspro` | 首发基石投资者合计申购比例 |  |
| `hks_ipo_dtooratio_pl` | 申购一手中签率 |  |
| `hks_ipo_expectedcollection` | 首发预计募集资金 |  |
| `hks_ipo_expense` | 首发发行费用 |  |
| `hks_ipo_findt` | 证监会境外发行备案日期 |  |
| `hks_ipo_greenshoe` | 是否行使超额配售权 |  |
| `hks_ipo_hearingdate` | 聆讯日期 |  |
| `hks_ipo_idc` | 首发信息披露费 |  |
| `hks_ipo_industrycons` | 首发行业顾问 |  |
| `hks_ipo_intsubratio` | 国际发行有效申购倍数 |  |
| `hks_ipo_intvsshares` | 国际发行有效申购数量 |  |
| `hks_ipo_issuedate_e` | 申购截止日 |  |
| `hks_ipo_issuedate_o` | 申购起始日 |  |
| `hks_ipo_legaladvisor_cmpy` | 首发发行人律师 |  |
| `hks_ipo_listeddate` | 首发上市日 |  |
| `hks_ipo_maxprice` | 招股价区间上限 |  |
| `hks_ipo_minprice` | 招股价区间下限 |  |
| `hks_ipo_minsubscription_pl` | 稳购1手最低申购股数 |  |
| `hks_ipo_name_cornerstone` | 首发基石投资者名称 | Sequence |
| `hks_ipo_netcollection` | 首发募资净额 |  |
| `hks_ipo_netcollection_ture` | 首发募集资金净额 |  |
| `hks_ipo_overallot_prop_vol` | 拟超额配售数量 |  |
| `hks_ipo_pct_cornerstone` | 首发基石投资者持股比例 | Sequence |
| `hks_ipo_pe` | 预测发行市盈率（发行价） |  |
| `hks_ipo_pemax` | 预测发行市盈率（最高价） |  |
| `hks_ipo_pemin` | 预测发行市盈率（最低价） |  |
| `hks_ipo_posthearing` | 聆讯后资料公告日 |  |
| `hks_ipo_price` | 首发价格 |  |
| `hks_ipo_price2` | 首发价格 |  |
| `hks_ipo_pricingdate` | 定价日 |  |
| `hks_ipo_quantity_cornerstone` | 首发基石投资者持股数量 | Sequence |
| `hks_ipo_resultdate` | 发行结果公告日 |  |
| `hks_ipo_sfee` | 首发保荐费用 |  |
| `hks_ipo_stabilizingmanager` | 首发稳价人 |  |
| `hks_ipo_subnum` | 公开发售申购人数 |  |
| `hks_ipo_subnum_a` | 公开发售甲组申购人数 |  |
| `hks_ipo_subnum_b` | 公开发售乙组申购人数 |  |
| `hks_ipo_subratio` | 网上发行有效认购倍数 |  |
| `hks_ipo_tbps_max` | 每股有形资产净值上限 |  |
| `hks_ipo_tbps_min` | 每股有形资产净值下限 |  |
| `hks_ipo_tpctcs` | 首发基石投资者持股比例合计 |  |
| `hks_ipo_tquacs` | 首发基石投资者持股数量合计 |  |
| `hks_ipo_type` | 发行方式 |  |
| `hks_ipo_ufee` | 首发承销费用 |  |
| `hks_ipo_usfeerate_fix` | 首发基础承销费率 |  |
| `hks_ipo_usfeerate_float` | 首发浮动承销费率 |  |
| `hks_ipo_usfees` | 首发承销保荐费用 |  |
| `hks_ipo_wpipreleasingdate` | 网上预览资料公告日 |  |
| `hks_is_ebitda_ard` | EBITDA(公布值) | REPORTDATE |
| `hks_is_ebitda_ard1` | EBITDA(公布值) | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `hks_is_investmentproperty_ard` | 投资物业公允价值变动(公布值) | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `hks_is_sales_ard` | 总营业收入(公布值) | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `hks_is_sharepayments` | 股权激励支出 | REPORTDATE |
| `hks_is_sharepayments_ard` | 股权激励支出 | YEARBASIS、REPORTINGBASIS、REPORTDATE、TYPE |
| `hks_mq_amount` | 月成交额(币种转换) | TRADEDATE |
| `hks_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `hks_pq_avgamount1` | 区间日均成交额(币种转换) | StartDate、DATE |
| `hks_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `hks_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `hks_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `hks_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `hks_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `hks_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `hks_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `hks_pq_pctchange_10d` | 近10日涨跌幅 |  |
| `hks_pq_pctchange_1m` | 近1月涨跌幅 |  |
| `hks_pq_pctchange_1y` | 近1年涨跌幅 |  |
| `hks_pq_pctchange_3m` | 近3月涨跌幅 |  |
| `hks_pq_pctchange_5d` | 近5日涨跌幅 |  |
| `hks_pq_pctchange_6m` | 近6月涨跌幅 |  |
| `hks_pq_pctchange_mtd` | 本月至今涨跌幅 |  |
| `hks_pq_pctchange_qtd` | 季度至今涨跌幅 |  |
| `hks_pq_pctchange_ytd` | 年迄今涨跌幅 |  |
| `hks_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `hks_pq_relpctchange` | 区间相对指数涨跌幅 | BEGINDATE、EndDate |
| `hks_pq_relpctchange_10d` | 近10日相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_1m` | 近1月相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_1y` | 近1年相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_3m` | 近3月相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_5d` | 近5日相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_6m` | 近6月相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_mtd` | 本月至今相对指数涨跌幅 | TYPE |
| `hks_pq_relpctchange_ytd` | 年迄今相对指数涨跌幅 | TYPE |
| `hks_pq_relrelpctchange_mtd` | 季度至今相对指数涨跌幅 | TYPE |
| `hks_pq_tradedays` | 区间交易天数 | StartDate、EndDate |
| `hks_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `hks_qfa_deductedprofit` | 单季度.扣除非经常损益后净利润 | REPORTDATE、TYPE、CURTYPE |
| `hks_qfa_eps_basic` | 单季度.基本每股收益EPS | REPORTDATE、TYPE、CURTYPE |
| `hks_qfa_eps_diluted` | 单季度.稀释每股收益EPS | REPORTDATE、TYPE、CURTYPE |
| `hks_qfa_grossprofitmargin` | 单季度.销售毛利率 | REPORTDATE、TYPE |
| `hks_qfa_netprofitmargin` | 单季度.销售净利率 | REPORTDATE、TYPE |
| `hks_qfa_nogaapprofit` | 单季度.净利润(Non-GAAP) | REPORTDATE、TYPE、CURTYPE |
| `hks_qfa_roa` | 单季度.总资产净利率ROA | REPORTDATE、TYPE |
| `hks_qfa_roe` | 单季度.净资产收益率ROE | REPORTDATE、TYPE |
| `hks_qfa_yoynpt` | 单季度.净利润(同比增长率)_GSD | REPORTDATE |
| `hks_qfa_yoysales` | 单季度.营业收入(同比增长率) | REPORTDATE |
| `hks_qstm_cs` | 单季度现金流量表 | ITEMSCODE、REPORTDATE |
| `hks_qstm_is` | 单季度利润表 | ITEMSCODE、REPORTDATE |
| `hks_qstm_is_1078` | 单季度.综合收益 | REPORTDATE |
| `hks_qstm_is_15` | 单季度.管理费用_GSD | REPORTDATE、TYPE |
| `hks_qstm_is_47` | 单季度.销售费用_GSD | REPORTDATE、TYPE |
| `hks_qstm_is_60` | 单季度.除税后利润 | REPORTDATE、TYPE、CURTYPE |
| `hks_risk_avgreturn` | 平均收益率 | BEGINDATE、EndDate |
| `hks_risk_avgreturn_yearly` | 平均收益率(年化) | BEGINDATE、EndDate |
| `hks_risk_stdev` | 波动率 | BEGINDATE、EndDate |
| `hks_risk_stdev_yearly` | 波动率(年化) | BEGINDATE、EndDate |
| `hks_share_a_pct` | A股/已发行普通股 |  |
| `hks_share_b_pct` | B股/已发行普通股 |  |
| `hks_share_cn` | 中资中介机构持股数量 | TRADEDATE |
| `hks_share_cpct_cn` | 中资中介机构持股/香港股 | TRADEDATE |
| `hks_share_cpct_hk` | 香港本地中介机构持股/香港股 | TRADEDATE |
| `hks_share_cpct_hks` | 港股通持股/香港股 | TRADEDATE |
| `hks_share_cpct_hksh` | 沪市港股通持股/香港股 | TRADEDATE |
| `hks_share_cpct_hksz` | 深市港股通持股/香港股 | TRADEDATE |
| `hks_share_cpct_os` | 国际中介机构持股/香港股 | TRADEDATE |
| `hks_share_h` | 香港上市股 |  |
| `hks_share_h_pct` | 香港股/已发行普通股 |  |
| `hks_share_hk` | 香港本地中介机构持股数量 | TRADEDATE |
| `hks_share_hks` | 港股通持股数量 | TRADEDATE |
| `hks_share_hksh` | 沪市港股通持股数量 | TRADEDATE |
| `hks_share_hksz` | 深市港股通持股数量 | TRADEDATE |
| `hks_share_liqa` | 流通A股 |  |
| `hks_share_nontradable` | 非流通股 | TRADEDATE |
| `hks_share_os` | 国际中介机构持股数量 | TRADEDATE |
| `hks_share_oversea` | 海外上市股 |  |
| `hks_share_oversea_pct` | 海外股/已发行普通股 |  |
| `hks_share_pct_cn` | 中资中介机构持股占比 | TRADEDATE |
| `hks_share_pct_hk` | 香港本地中介机构持股占比 | TRADEDATE |
| `hks_share_pct_hks` | 港股通持股占比 | TRADEDATE |
| `hks_share_pct_hksh` | 沪市港股通持股占比 | TRADEDATE |
| `hks_share_pct_hksz` | 深市港股通持股占比 | TRADEDATE |
| `hks_share_pct_os` | 国际中介机构持股占比 | TRADEDATE |
| `hks_share_prefer` | 优先股 |  |
| `hks_share_restricteda` | 限售A股 |  |
| `hks_share_shortamount` | 持有淡仓金额合计 | TRADEDATE |
| `hks_share_shortshares` | 持有淡仓股数合计 | TRADEDATE |
| `hks_share_total` | 已发行普通股 |  |
| `hks_share_totala` | A股合计 |  |
| `hks_share_totalb` | B股合计 |  |
| `hks_ss_daystocover` | 空头回补天数 | TRADEDATE |
| `hks_ss_shortintrestpct` | 未平仓卖空数占总股本比例 | TRADEDATE |
| `hks_ss_turnover` | 全日卖空金额 | TRADEDATE |
| `hks_ss_turnover_h` | 上午收盘卖空股数 | EndDate |
| `hks_ss_turnoverpct` | 卖空金额占市场卖空总额比率 | EndDate |
| `hks_ss_volume` | 全日卖空股数 | EndDate |
| `hks_ss_volume_h` | 上午收盘卖空股数 | DEALDATE |
| `hks_ss_volumepct` | 卖空量占成交量比率 | EndDate |
| `hks_ss_volumetohshares` | 卖空量占香港流通股百分比 | EndDate |
| `hks_ssbpco` | 单季度.主营构成(按产品)-项目成本 | REPORTDATE、TopN |
| `hks_ssbpgp` | 单季度.主营构成(按产品)-项目毛利 | REPORTDATE、TopN |
| `hks_ssbpgpm` | 单季度.主营构成(按产品)-项目毛利率 | REPORTDATE、TopN |
| `hks_ssbpit` | 单季度.主营构成(按产品)-项目名称 | REPORTDATE、TopN |
| `hks_ssbpre` | 单季度.主营构成(按产品)-项目收入 | REPORTDATE、TopN |
| `hks_ssbrco` | 单季度.主营构成(按地区)-项目成本 | REPORTDATE、TopN |
| `hks_ssbrgp` | 单季度.主营构成(按地区)-项目毛利 | REPORTDATE、TopN |
| `hks_ssbrgpm` | 单季度.主营构成(按地区)-项目毛利率 | REPORTDATE、TopN |
| `hks_ssbrit` | 单季度.主营构成(按地区)-项目名称 | REPORTDATE、TopN |
| `hks_ssbrre` | 单季度.主营构成(按地区)-项目收入 | REPORTDATE、TopN |
| `hks_stm_announceddeducteddebttoassets` | 剔除预收账款的资产负债率(公告值) | REPORTDATE |
| `hks_stm_ap` | 预收款项 | REPORTDATE、TYPE |
| `hks_stm_bs` | 资产负债表 | ITEMSCODE、REPORTDATE |
| `hks_stm_bs_10` | 交易性金融资产 | REPORTDATE |
| `hks_stm_bs_1017` | 非流动负债合计 | REPORTDATE |
| `hks_stm_bs_1021` | 储备 | REPORTDATE |
| `hks_stm_bs_1028` | 总负债及总权益 | REPORTDATE |
| `hks_stm_bs_1030` | 土地使用权 | REPORTDATE |
| `hks_stm_bs_1035` | 应收款项合计 | REPORTDATE |
| `hks_stm_bs_1037` | 其它应收款 | REPORTDATE |
| `hks_stm_bs_1039` | 其他流动资产 | REPORTDATE |
| `hks_stm_bs_1041` | 其他长期投资 | REPORTDATE |
| `hks_stm_bs_1042` | 持有至到期投资 | REPORTDATE |
| `hks_stm_bs_1043` | 可供出售投资 | REPORTDATE |
| `hks_stm_bs_1045` | 其他非流动资产 | REPORTDATE |
| `hks_stm_bs_1049` | 其他流动负债 | REPORTDATE |
| `hks_stm_bs_1052` | 其他非流动负债 | REPORTDATE |
| `hks_stm_bs_1053` | 优先股 | REPORTDATE |
| `hks_stm_bs_1062` | 客户贷款及垫款净额 | REPORTDATE |
| `hks_stm_bs_1065` | 交易性金融负债 | REPORTDATE |
| `hks_stm_bs_1070` | 商誉及无形资产 | REPORTDATE |
| `hks_stm_bs_1073` | 应收再保 | REPORTDATE |
| `hks_stm_bs_1074` | 应收保费 | REPORTDATE |
| `hks_stm_bs_1075` | 递延保单获得成本 | REPORTDATE |
| `hks_stm_bs_1076` | 保险合同负债 | REPORTDATE |
| `hks_stm_bs_1077` | 投资合同负债 | REPORTDATE |
| `hks_stm_bs_1080` | 其他储备 | REPORTDATE |
| `hks_stm_bs_1082` | 其他资产 | REPORTDATE |
| `hks_stm_bs_1083` | 其他负债 | REPORTDATE |
| `hks_stm_bs_1084` | 其他短期投资 | REPORTDATE |
| `hks_stm_bs_1085` | 库存股 | REPORTDATE |
| `hks_stm_bs_1086` | 其他综合性收益 | REPORTDATE |
| `hks_stm_bs_1087` | 普通股权益总额 | REPORTDATE |
| `hks_stm_bs_1092` | 拆出资金 | REPORTDATE |
| `hks_stm_bs_1093` | 抵押担保证券 | REPORTDATE |
| `hks_stm_bs_1094` | 可供出售贷款 | REPORTDATE |
| `hks_stm_bs_1095` | 总存款 | REPORTDATE |
| `hks_stm_bs_1096` | 拆入资金 | REPORTDATE |
| `hks_stm_bs_1097` | 抵押担保融资 | REPORTDATE |
| `hks_stm_bs_1099` | 其他投资 | REPORTDATE |
| `hks_stm_bs_1102` | 应付再保 | REPORTDATE |
| `hks_stm_bs_1109` | 抵押贷款与票据净额 | REPORTDATE |
| `hks_stm_bs_1110` | 房地产物业相关资产净值 | REPORTDATE |
| `hks_stm_bs_1111` | 其他固定资产净值 | REPORTDATE |
| `hks_stm_bs_12` | 应收账款净额 | REPORTDATE |
| `hks_stm_bs_123` | 分出再保险合同资产 | REPORTDATE、TYPE |
| `hks_stm_bs_124` | 分出再保险合同负债 | REPORTDATE、TYPE |
| `hks_stm_bs_125` | 保险合同资产 | REPORTDATE、TYPE |
| `hks_stm_bs_126` | 投资合同资产 | REPORTDATE、TYPE |
| `hks_stm_bs_128` | 总负债 | REPORTDATE |
| `hks_stm_bs_129` | 普通股股本 | REPORTDATE |
| `hks_stm_bs_130` | 股本溢价 | REPORTDATE |
| `hks_stm_bs_131` | 留存收益 | REPORTDATE |
| `hks_stm_bs_136` | 少数股东权益 | REPORTDATE |
| `hks_stm_bs_140` | 归属母公司股东权益 | REPORTDATE |
| `hks_stm_bs_145` | 股东权益合计 | REPORTDATE |
| `hks_stm_bs_17` | 存货 | REPORTDATE |
| `hks_stm_bs_25` | 流动资产合计 | REPORTDATE |
| `hks_stm_bs_29` | 权益性投资 | REPORTDATE |
| `hks_stm_bs_31` | 固定资产净值 | REPORTDATE |
| `hks_stm_bs_46` | 非流动资产合计 | REPORTDATE |
| `hks_stm_bs_74` | 总资产 | REPORTDATE |
| `hks_stm_bs_78` | 应付账款及票据 | REPORTDATE |
| `hks_stm_bs_81` | 应交税金 | REPORTDATE |
| `hks_stm_bs_88` | 短期借贷及长期借贷当期到期部分 | REPORTDATE |
| `hks_stm_bs_9` | 现金及现金等价物 | REPORTDATE |
| `hks_stm_bs_93` | 流动负债合计 | REPORTDATE |
| `hks_stm_bs_94` | 长期借贷 | REPORTDATE |
| `hks_stm_cl` | 合同负债 | REPORTDATE、TYPE |
| `hks_stm_cs` | 现金流量表 | ITEMSCODE、REPORTDATE |
| `hks_stm_cs_1019` | 折旧与摊销 | REPORTDATE |
| `hks_stm_cs_1020` | 资本性支出 | REPORTDATE |
| `hks_stm_cs_1021` | 债务减少 | REPORTDATE |
| `hks_stm_cs_1022` | 债务增加 | REPORTDATE |
| `hks_stm_cs_1025` | 净利润 | REPORTDATE |
| `hks_stm_cs_1026` | 营运资本变动 | REPORTDATE |
| `hks_stm_cs_1027` | 其他非现金调整 | REPORTDATE |
| `hks_stm_cs_1028` | 出售固定资产收到的现金 | REPORTDATE |
| `hks_stm_cs_1029` | 投资增加 | REPORTDATE |
| `hks_stm_cs_1030` | 投资减少 | REPORTDATE |
| `hks_stm_cs_1031` | 其他投资活动产生的现金流量净额 | REPORTDATE |
| `hks_stm_cs_1032` | 股本增加 | REPORTDATE |
| `hks_stm_cs_1033` | 股本减少 | REPORTDATE |
| `hks_stm_cs_1034` | 支付的股利合计 | REPORTDATE |
| `hks_stm_cs_1035` | 其他筹资活动产生的现金流量净额 | REPORTDATE |
| `hks_stm_cs_1036` | 其他现金流量调整 | REPORTDATE |
| `hks_stm_cs_39` | 经营活动产生的现金流量净额 | REPORTDATE |
| `hks_stm_cs_59` | 投资活动产生的现金流量净额 | REPORTDATE |
| `hks_stm_cs_77` | 筹资活动产生的现金流量净额 | REPORTDATE |
| `hks_stm_cs_78` | 汇率变动影响 | REPORTDATE |
| `hks_stm_cs_82` | 现金及现金等价物净增加额 | REPORTDATE |
| `hks_stm_cs_83` | 现金及现金等价物期初余额 | REPORTDATE |
| `hks_stm_cs_84` | 现金及现金等价物期末余额 | REPORTDATE |
| `hks_stm_deducteddebttoassets` | 剔除预收账款后的资产负债率 | REPORTDATE |
| `hks_stm_is` | 利润表 | ITEMSCODE、REPORTDATE |
| `hks_stm_is_10` | 营业成本 | REPORTDATE |
| `hks_stm_is_100` | 保险服务业绩 | REPORTDATE、TYPE |
| `hks_stm_is_101` | 净投资业绩 | REPORTDATE、TYPE |
| `hks_stm_is_1011` | 其他营业收入 | REPORTDATE |
| `hks_stm_is_1016` | 除税前利润 | REPORTDATE |
| `hks_stm_is_102` | 承保财务损失 | REPORTDATE、TYPE |
| `hks_stm_is_103` | 分出再保险财务损益 | REPORTDATE、TYPE |
| `hks_stm_is_1030` | 研发费用 | REPORTDATE |
| `hks_stm_is_1032` | 总营业支出 | REPORTDATE |
| `hks_stm_is_1033` | 利息支出 | REPORTDATE |
| `hks_stm_is_1034` | 权益性投资损益 | REPORTDATE |
| `hks_stm_is_1035` | 其他非经营性损益 | REPORTDATE |
| `hks_stm_is_1038` | 非持续经营净利润 | REPORTDATE |
| `hks_stm_is_1039` | 其他特殊项 | REPORTDATE |
| `hks_stm_is_1040` | 销售、行政及一般费用 | REPORTDATE |
| `hks_stm_is_1041` | 营业利润 | REPORTDATE |
| `hks_stm_is_1045` | 持续经营净利润 | REPORTDATE |
| `hks_stm_is_1048` | 利息收入 | REPORTDATE |
| `hks_stm_is_1050` | 利息净收入 | REPORTDATE |
| `hks_stm_is_1051` | 手续费及佣金收入 | REPORTDATE |
| `hks_stm_is_1052` | 手续费及佣金开支 | REPORTDATE |
| `hks_stm_is_1053` | 手续费及佣金净收入 | REPORTDATE |
| `hks_stm_is_1054` | 交易账户净收入 | REPORTDATE |
| `hks_stm_is_1058` | 保单持有人利益 | REPORTDATE |
| `hks_stm_is_1060` | 贷款损失准备 | REPORTDATE |
| `hks_stm_is_1063` | 净已赚保费 | REPORTDATE |
| `hks_stm_is_1073` | 利息及股息收入 | REPORTDATE |
| `hks_stm_is_1074` | 优先股利及其他调整项 | REPORTDATE |
| `hks_stm_is_1075` | 归属普通股东净利润 | REPORTDATE |
| `hks_stm_is_1076` | 非经常项目前利润 | REPORTDATE |
| `hks_stm_is_1077` | 非经常项目损益 | REPORTDATE |
| `hks_stm_is_1078` | 综合收益 | REPORTDATE |
| `hks_stm_is_1079` | 经纪佣金收入 | REPORTDATE |
| `hks_stm_is_1080` | 承销与投资银行费收入 | REPORTDATE |
| `hks_stm_is_1081` | 资产管理费收入 | REPORTDATE |
| `hks_stm_is_1082` | 自营业务收入 | REPORTDATE |
| `hks_stm_is_1083` | 扣除贷款损失准备前收入 | REPORTDATE |
| `hks_stm_is_1084` | 租金收入 | REPORTDATE |
| `hks_stm_is_1085` | 租户认缴物业维护综合费 | REPORTDATE |
| `hks_stm_is_1086` | 房地产销售收入 | REPORTDATE |
| `hks_stm_is_1087` | 抵押贷款相关收入 | REPORTDATE |
| `hks_stm_is_15` | 管理费用_GSD | REPORTDATE、TYPE |
| `hks_stm_is_47` | 销售费用_GSD | REPORTDATE、TYPE |
| `hks_stm_is_56` | 所得税 | REPORTDATE |
| `hks_stm_is_61` | 净利润 | REPORTDATE |
| `hks_stm_is_62` | 少数股东损益 | REPORTDATE |
| `hks_stm_is_83` | 总营业收入 | REPORTDATE |
| `hks_stm_is_9` | 主营收入 | REPORTDATE |
| `hks_stm_is_92` | 营业开支 | REPORTDATE、TYPE、CURTYPE |
| `hks_stm_is_97` | 保险服务收入 | REPORTDATE、TYPE |
| `hks_stm_is_98` | 保险服务费用 | REPORTDATE、TYPE |
| `hks_stm_is_99` | 再保险合同产生的费用净额 | REPORTDATE、TYPE |
| `hks_stm_issuingdate2` | 定期报告预计披露日期 | REPORTDATE |
| `hks_stm_rf` | 受限资金 | REPORTDATE、TYPE |
| `hks_stmnote_af` | 审计费用 | REPORTDATE、TYPE |
| `hks_stmnote_ar` | 应收账款合计 | REPORTDATE、TYPE |
| `hks_stmnote_arf` | 审计相关费用 | REPORTDATE、TYPE |
| `hks_stmnote_aualaccmdiv` | 现金分红总额 | REPORTDATE |
| `hks_stmnote_fa_1` | 在建工程 | REPORTDATE、TYPE |
| `hks_stmnote_mgmt_ben` | 管理层年度薪酬总额 |  |
| `hks_stmnote_mgmt_ben_bc` | 董事长薪酬 |  |
| `hks_stmnote_mgmt_ben_ceo` | 总经理薪酬 |  |
| `hks_stmnote_mgmt_ben_cfo` | 财务总监薪酬 |  |
| `hks_stmnote_mgmt_ben_discloser` | 董事会秘书薪酬 |  |
| `hks_stmnote_mgmt_ben_id` | 独立董事薪酬 | Year |
| `hks_stmnote_mgmt_ben_top3b` | 金额前三的董事薪酬合计 |  |
| `hks_stmnote_mgmt_ben_top3m` | 金额前三的高管薪酬合计 |  |
| `hks_val_dividendyield` | 股息率 |  |
| `hks_val_ev` | 企业股权价值 |  |
| `hks_val_ev1` | 企业总价值 |  |
| `hks_val_ev2` | 企业总价值(剔除货币资金) |  |
| `hks_val_mv` | 总市值 |  |
| `hks_val_mv_ard` | 总市值2 | TRADEDATE、CURTYPE |
| `hks_val_pb` | 市净率(PB) |  |
| `hks_val_pb_lyr` | 市净率(PB, LYR) |  |
| `hks_val_pb_mrq` | 市净率(PB, MRQ) |  |
| `hks_val_pcf` | 市现率(PCF) |  |
| `hks_val_pcf_lyr` | 市现率(PCF, LYR) |  |
| `hks_val_pcf_ttm` | 市现率(PCF, TTM) |  |
| `hks_val_pe` | 市盈率(PE) |  |
| `hks_val_pe_lyr` | 市盈率(LYR) |  |
| `hks_val_pe_ttm` | 市盈率(TTM) |  |
| `hks_val_ps` | 市销率(PS) |  |
| `hks_val_ps_lyr` | 市销率(PS, LYR) |  |
| `hks_val_ps_ttm` | 市销率(PS, TTM) |  |
| `hks_west_avgebt_surprise` | 预测利润总额Surprise(可选类型) | Year、TYPE |
| `hks_west_avgoc_surprise` | 预测营业成本Surprise(可选类型) | Year、TYPE |
| `hks_west_avgoperatingprofit_surprise` | 预测营业利润Surprise(可选类型) | Year、TYPE |
| `hks_west_bps_surprise` | 预测每股净资产Surprise(可选类型) | Year、TYPE |
| `hks_west_eps_surprise` | 预测每股收益Surprise(可选类型) | Year、TYPE |
| `hks_west_netprofit_surprise` | 预测净利润Surprise(可选类型) | Year、TYPE |
| `hks_west_sales_surprise` | 预测营业收入Surprise(可选类型) | Year、TYPE |
| `hks_wq_amount` | 周成交额(币种转换) | TRADEDATE |
| `hks_yq_amount` | 年成交额(币种转换) | TRADEDATE |

<a id="分类-台股"></a>

## 台股（665 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `tws_dir_d_num` | 董事总人数 |  |
| `tws_dir_d_sharenum` | 董事持股数量 |  |
| `tws_dir_dp_num` | 一般董事人数 |  |
| `tws_dir_ds_pledged` | 董监质押股数量 |  |
| `tws_dir_ds_pledgedpct` | 董监质押股比例 |  |
| `tws_dir_ds_sharenum` | 董监持股数量 |  |
| `tws_dir_ds_sharepct` | 董监持股比例 |  |
| `tws_dir_id_num` | 独立董事人数 |  |
| `tws_dir_is_num` | 独立监察人数 |  |
| `tws_dir_mag_sharenum` | 经理人持股数量 |  |
| `tws_dir_mag_sharepct` | 经理人持股比例 |  |
| `tws_dir_od_num` | 常董人数 |  |
| `tws_dir_os_num` | 常监人数 |  |
| `tws_dir_osp_num` | 一般监察人数 |  |
| `tws_dir_s_num` | 监察总人数 |  |
| `tws_dir_s_sharenum` | 监察持股数量 |  |
| `tws_dir_td_num` | 董事长人数 |  |
| `tws_dir_vtd_num` | 副董事长人数 |  |
| `tws_div_cash` | 现金股利 |  |
| `tws_div_cpl` | 公积配股 |  |
| `tws_div_dec` | 减资 |  |
| `tws_div_drdate` | 董事会日期 |  |
| `tws_div_ebcash` | 员工分红-现金 |  |
| `tws_div_ebstock` | 员工分红-配股 |  |
| `tws_div_ecexdate` | 除权日(现增) |  |
| `tws_div_edexdate` | 除息日 |  |
| `tws_div_elongbegin` | 停资起始日 |  |
| `tws_div_elongd3` | 资券恢复日 |  |
| `tws_div_elongend` | 停资终止日 |  |
| `tws_div_emexdate` | 除权日(配股) |  |
| `tws_div_epexdate` | 除权日(减资) |  |
| `tws_div_eregbegin` | 停止过户-起 |  |
| `tws_div_eregend` | 停止过户-迄 |  |
| `tws_div_ern` | 盈余配股 |  |
| `tws_div_eshortbegin` | 停券起始日 |  |
| `tws_div_eshortd2` | 融券最后回补日 |  |
| `tws_div_eshortend` | 停券终止日 |  |
| `tws_div_gdr` | 现金增资(GDR) |  |
| `tws_div_mdate` | 股东会日期 |  |
| `tws_div_mer` | 无偿配股合计 |  |
| `tws_div_rightissue` | 现金增资额 |  |
| `tws_div_subprice` | 认购价格 |  |
| `tws_div_totamount` | 股息总额 |  |
| `tws_dq_amount` | 成交额 | TRADEDATE |
| `tws_dq_change` | 涨跌 | TRADEDATE |
| `tws_dq_close` | 收盘价 | TRADEDATE |
| `tws_dq_closeask` | 最后揭示卖价 | TRADEDATE |
| `tws_dq_closebid` | 最后揭示买价 | TRADEDATE |
| `tws_dq_high` | 最高价 | TRADEDATE |
| `tws_dq_limit` | 涨跌停 | TRADEDATE |
| `tws_dq_low` | 最低价 | TRADEDATE |
| `tws_dq_notice_a` | 注意股票(A) | TRADEDATE |
| `tws_dq_notice_d` | 处置股票(D) | TRADEDATE |
| `tws_dq_notice_y` | 全额交割(Y) | TRADEDATE |
| `tws_dq_open` | 开盘价 | TRADEDATE |
| `tws_dq_pctchange` | 涨跌幅 | TRADEDATE |
| `tws_dq_pmkt` | 市场别 | TRADEDATE |
| `tws_dq_ticks` | 成交笔数 | TRADEDATE |
| `tws_dq_turn` | 换手率 | TRADEDATE |
| `tws_dq_volume` | 成交量 | TRADEDATE |
| `tws_fa_arturndays` | 应收账款收现天数 | REPORTDATE |
| `tws_fa_asset_co` | 资产总额(无保留意见) | REPORTDATE |
| `tws_fa_bps` | 每股净资产 | REPORTDATE |
| `tws_fa_branchnum` | 分行家数(金融) | REPORTDATE |
| `tws_fa_contractloss` | 违约金损失率(证券) | REPORTDATE |
| `tws_fa_current` | 流动比率 | REPORTDATE |
| `tws_fa_debttoassets` | 负债比率 | REPORTDATE |
| `tws_fa_deductedprofit` | 常续性利益(税后) | REPORTDATE |
| `tws_fa_deptose` | 存款/净资产(金融) | REPORTDATE |
| `tws_fa_ebit` | 税前息前净利 | REPORTDATE |
| `tws_fa_ebitda` | 税前息前折旧前摊销前净利 | REPORTDATE |
| `tws_fa_ebittointerest` | 利息保障倍数 | REPORTDATE |
| `tws_fa_ebt_co` | 税前净利(无保留意见) | REPORTDATE |
| `tws_fa_ebtps` | 每股税前净利 | REPORTDATE |
| `tws_fa_employeenum` | 员工人数(一般产业) | REPORTDATE |
| `tws_fa_eps_basic` | 基本每股收益 | REPORTDATE |
| `tws_fa_eps_diluted` | 稀释每股收益 | REPORTDATE |
| `tws_fa_equity_co` | 股东权益(无保留意见) | REPORTDATE |
| `tws_fa_errorbookingloss` | 错账损失率(证券) | REPORTDATE |
| `tws_fa_exptorev_fin` | 金融业务成本率(保险、金融) | REPORTDATE |
| `tws_fa_faturn` | 固定资产周转率 | REPORTDATE |
| `tws_fa_grossprofitmargin` | 营业毛利率 | REPORTDATE |
| `tws_fa_intcost` | 存借款平均利息(金融) | REPORTDATE |
| `tws_fa_inttorev` | 放款利益率(金融) | REPORTDATE |
| `tws_fa_invturndays` | 平均售货天数(一般产业) | REPORTDATE |
| `tws_fa_loantodep` | 放款/存款(金融) | REPORTDATE |
| `tws_fa_netprofitmargin` | 税后净利率 | REPORTDATE |
| `tws_fa_np_co` | 税后净利(无保留意见) | REPORTDATE |
| `tws_fa_oips` | 每股营业利益 | REPORTDATE |
| `tws_fa_oprprofitmargin` | 营业利益率 | REPORTDATE |
| `tws_fa_ortoeps` | 收支比率(保险、金融) | REPORTDATE |
| `tws_fa_profitmargin` | 税前净利率 | REPORTDATE |
| `tws_fa_quick` | 速动比率(一般产业、证券) | REPORTDATE |
| `tws_fa_retntion` | 内部保留比率 | REPORTDATE |
| `tws_fa_roa` | 资产报酬率 | REPORTDATE |
| `tws_fa_roe` | 净值报酬率(ROE) | REPORTDATE |
| `tws_fa_share_basic` | 加权平均股本 | REPORTDATE |
| `tws_fa_sps` | 每股营业额 | REPORTDATE |
| `tws_fa_tradingloss` | 买卖损失率(证券) | REPORTDATE |
| `tws_fa_yoy_assets` | 总资产(同比增长率) | REPORTDATE |
| `tws_fa_yoy_ebt` | 税前净利(同比增长率) | REPORTDATE |
| `tws_fa_yoy_equity` | 净资产(同比增长率) | REPORTDATE |
| `tws_fa_yoy_fa` | 折旧性固定资产(同比增长率) | REPORTDATE |
| `tws_fa_yoy_np` | 税后净利(同比增长率) | REPORTDATE |
| `tws_fa_yoy_oi` | 营业利益(同比增长率) | REPORTDATE |
| `tws_fa_yoy_or` | 营业收入(同比增长率) | REPORTDATE |
| `tws_gin_close` | 当日收盘价 | TRADEDATE |
| `tws_gin_long_bal` | 融资余额 | TRADEDATE |
| `tws_gin_long_buy` | 融资买进 | TRADEDATE |
| `tws_gin_long_cash` | 现金偿还 | TRADEDATE |
| `tws_gin_long_inc` | 融资增减 | TRADEDATE |
| `tws_gin_long_incpct` | 融资增减比率 | TRADEDATE |
| `tws_gin_long_sell` | 融资卖出 | TRADEDATE |
| `tws_gin_long_usepct` | 融资使用率 | TRADEDATE |
| `tws_gin_longtovolume` | 融资(买+卖)/成交量 | TRADEDATE |
| `tws_gin_offset` | 当日冲销 | TRADEDATE |
| `tws_gin_short_bal` | 融券余额 | TRADEDATE |
| `tws_gin_short_buy` | 融券买进 | TRADEDATE |
| `tws_gin_short_cash` | 现券偿还 | TRADEDATE |
| `tws_gin_short_inc` | 融券增减 | TRADEDATE |
| `tws_gin_short_incpct` | 融券增减比率 | TRADEDATE |
| `tws_gin_short_sell` | 融券卖出 | TRADEDATE |
| `tws_gin_short_usepct` | 融券使用率 | TRADEDATE |
| `tws_gin_shorttolong` | 券资比 | TRADEDATE |
| `tws_gin_shorttovolume` | 融券(买+卖)/成交量 | TRADEDATE |
| `tws_holder_name` | 大股东名称 | DEALDATE |
| `tws_holder_pct` | 大股东持股比例 | DEALDATE |
| `tws_holder_quantity` | 大股东持股数量 | DEALDATE |
| `tws_info_cfo` | 财务经理 |  |
| `tws_info_chairman` | 董事长 |  |
| `tws_info_compname` | 公司中文名称 |  |
| `tws_info_compnameeng` | 公司英文全称 |  |
| `tws_info_emm` | 会计月份 |  |
| `tws_info_employee` | 员工人数 |  |
| `tws_info_fax` | 传真 |  |
| `tws_info_founddate` | 设立日期 |  |
| `tws_info_industry_tse` | 所属行业(TSE行业) |  |
| `tws_info_isincode` | ISIN代码 |  |
| `tws_info_listeddate` | 上市日期 |  |
| `tws_info_listemg` | 兴柜日期 |  |
| `tws_info_listotc` | 上柜日期 |  |
| `tws_info_mkt` | 交易市场 |  |
| `tws_info_office` | 公司地址 |  |
| `tws_info_phone` | 电话 |  |
| `tws_info_president` | 总经理 |  |
| `tws_info_product1` | 主要产品1 |  |
| `tws_info_product2` | 主要产品2 |  |
| `tws_info_product3` | 主要产品3 |  |
| `tws_info_product_c` | 主要产品比重 |  |
| `tws_info_spokes` | 发言人 |  |
| `tws_info_unlistdate` | 下市日期 |  |
| `tws_info_website` | 网址 |  |
| `tws_inshd_dlr_buy` | 自营商买进数量 | DEALDATE |
| `tws_inshd_dlr_ex` | 自营买卖超 | DEALDATE |
| `tws_inshd_dlr_exmv` | 自营买卖超市值 | DEALDATE |
| `tws_inshd_dlr_sell` | 自营商卖出数量 | DEALDATE |
| `tws_inshd_fund_buy` | 投信买进数量 | DEALDATE |
| `tws_inshd_fund_ex` | 投信买卖超 | DEALDATE |
| `tws_inshd_fund_exmv` | 投信买卖超市值 | DEALDATE |
| `tws_inshd_fund_sell` | 投信卖出数量 | DEALDATE |
| `tws_inshd_qfii_buy` | 外资买进数量 | DEALDATE |
| `tws_inshd_qfii_ex` | 外资买卖超 | DEALDATE |
| `tws_inshd_qfii_exmv` | 外资买卖超市值 | DEALDATE |
| `tws_inshd_qfii_sell` | 外资卖出数量 | DEALDATE |
| `tws_inshd_ttl_ex` | 合计买卖超 | DEALDATE |
| `tws_inshd_ttl_exmv` | 合计买卖超市值 | DEALDATE |
| `tws_inv_amt` | 累计台湾汇出总额(新台币,千元) |  |
| `tws_inv_camt` | 累计汇出总额(原币,千元) |  |
| `tws_inv_cquota` | 经济部规定限额(原币,千元) |  |
| `tws_inv_cquotaamt` | 经济部核准金额(原币,千元) |  |
| `tws_inv_endinv1` | 期末账面值(新台币,千元) |  |
| `tws_inv_epscontribute` | 税前每股收益贡献度(新台币,元) |  |
| `tws_inv_inctoebt` | 投资损益/税前利润(母) |  |
| `tws_inv_quota` | 经济部规定限额(新台币,千元) |  |
| `tws_inv_quotaamt` | 经济部核准金额(新台币,千元) |  |
| `tws_inv_taddamt1` | 本期汇出金额(新台币,千元) |  |
| `tws_inv_tbegamt1` | 期初累计汇出金额(新台币,千元) |  |
| `tws_inv_tendamt1` | 期末累计汇出金额(新台币,千元) |  |
| `tws_inv_tinvch` | 投资损益(新台币,千元) |  |
| `tws_inv_tminamt1` | 本期收回金额(新台币,千元) |  |
| `tws_inv_tremt` | 汇回台湾投资收益(新台币,千元) |  |
| `tws_inv_tsecap1` | 实收资本额(新台币,千元) |  |
| `tws_ipo_close` | 首日收盘价 |  |
| `tws_ipo_exdate` | 承销日 |  |
| `tws_ipo_inq_anncdt` | 招股(圈购)公告日 |  |
| `tws_ipo_inq_findt` | 招股(圈购)完成日 |  |
| `tws_ipo_inq_max` | 招股(圈购)价上限 |  |
| `tws_ipo_inq_min` | 招股(圈购)价下限 |  |
| `tws_ipo_leaduw` | 主办证券商 |  |
| `tws_ipo_lisedate` | 承销时上市日期 |  |
| `tws_ipo_mkt` | 承销时上市别 |  |
| `tws_ipo_prisellvolume` | 自行洽商销售 |  |
| `tws_ipo_totaluw` | 总承销股数 |  |
| `tws_ipo_uw_begindt` | 公开承销-起 |  |
| `tws_ipo_uw_drawdt` | 承销抽签日 |  |
| `tws_ipo_uw_enddt` | 公开承销-迄 |  |
| `tws_ipo_uw_paydtbegin` | 承销缴款-起 |  |
| `tws_ipo_uw_paydtend` | 承销缴款-迄 |  |
| `tws_ipo_uw_price` | 承销价格 |  |
| `tws_ipo_uw_pubdt` | 承销公告日 |  |
| `tws_ipo_uw_share` | 承销股数 |  |
| `tws_ipo_uw_type` | 承销类别 |  |
| `tws_ipo_uwsellvolume` | 券商承销数 |  |
| `tws_mr_accuebt` | 累计税前盈余 |  |
| `tws_mr_accuebt_ly` | 去年累计税前盈余 |  |
| `tws_mr_accuebt_yoy` | 累计税前盈余(同比增长率) |  |
| `tws_mr_accunp` | 累计税后盈余 |  |
| `tws_mr_accunp_ly` | 去年累计税后盈余 |  |
| `tws_mr_accunp_yoy` | 累计税后盈余(同比增长率) |  |
| `tws_mr_accusales` | 累计营收 |  |
| `tws_mr_accusales_ly` | 去年累计营收 |  |
| `tws_mr_accusales_yoy` | 累计营收(同比增长率) |  |
| `tws_mr_bps` | 每股净值 |  |
| `tws_mr_bv` | 净值 |  |
| `tws_mr_conlib` | 背书保证余额 |  |
| `tws_mr_conlibtobv` | 背书保证占净值比 |  |
| `tws_mr_ebt_totarget` | 累计税前盈余达标率 |  |
| `tws_mr_ebtps` | 累计每股税前盈余 |  |
| `tws_mr_ebtps_wa` | 累计每股税前盈余(WA) |  |
| `tws_mr_eps` | 累计每股税后盈余 |  |
| `tws_mr_eps_wa` | 累计每股税后盈余(WA) |  |
| `tws_mr_est_anncdt` | 预估盈余发布日 |  |
| `tws_mr_estebt` | 预估税前盈余 |  |
| `tws_mr_estnp` | 预估税后盈余 |  |
| `tws_mr_estsales` | 预估营收 |  |
| `tws_mr_estsales_anncdt` | 预估营收发布日 |  |
| `tws_mr_loanto` | 资金贷放余额 |  |
| `tws_mr_loantobv` | 资金贷放占净值比 |  |
| `tws_mr_np_totarget` | 累计税后盈余达标率 |  |
| `tws_mr_npl` | 广义逾放比率 |  |
| `tws_mr_sales` | 单月营收 |  |
| `tws_mr_sales_ly` | 去年单月营收 |  |
| `tws_mr_sales_mom` | 单月营收(环比增长率) |  |
| `tws_mr_sales_totarget` | 营收达标率 |  |
| `tws_mr_sales_yoy` | 单月营收(同比增长率) |  |
| `tws_mr_sps` | 累计每股营收 |  |
| `tws_mr_ssps` | 单月每股营收 |  |
| `tws_mr_trshare` | 流通在外股数 |  |
| `tws_pq_amount` | 区间成交额 | StartDate、DATE |
| `tws_pq_avgprice` | 区间成交均价 | StartDate、DATE |
| `tws_pq_change` | 区间涨跌 | StartDate、DATE |
| `tws_pq_close` | 区间收盘价 | StartDate、DATE |
| `tws_pq_high` | 区间最高价 | StartDate、DATE |
| `tws_pq_low` | 区间最低价 | StartDate、DATE |
| `tws_pq_open` | 区间开盘价 | StartDate、DATE |
| `tws_pq_pctchange` | 区间涨跌幅 | StartDate、DATE |
| `tws_pq_pctchange_10d` | 近10日涨跌幅 |  |
| `tws_pq_pctchange_1m` | 近1月涨跌幅 |  |
| `tws_pq_pctchange_1y` | 近1年涨跌幅 |  |
| `tws_pq_pctchange_3m` | 近3月涨跌幅 |  |
| `tws_pq_pctchange_5d` | 近5日涨跌幅 |  |
| `tws_pq_pctchange_6m` | 近6月涨跌幅 |  |
| `tws_pq_pctchange_mtd` | 本月至今涨跌幅 |  |
| `tws_pq_pctchange_qtd` | 季度至今涨跌幅 |  |
| `tws_pq_pctchange_ytd` | 年迄今涨跌幅 |  |
| `tws_pq_volume` | 区间成交量 | StartDate、DATE |
| `tws_qfa_arturndays` | 单季度.应收账款收现天数 |  |
| `tws_qfa_bps` | 单季度.每股净资产 |  |
| `tws_qfa_branchnum` | 单季度.分行家数(金融) |  |
| `tws_qfa_contractloss` | 单季度.违约金损失率(证券) |  |
| `tws_qfa_current` | 单季度.流动比率 |  |
| `tws_qfa_debttoassets` | 单季度.负债比率 |  |
| `tws_qfa_deptose` | 单季度.存款/净资产(金融) |  |
| `tws_qfa_ebittointerest` | 单季度.利息保障倍数 |  |
| `tws_qfa_ebtps` | 单季度.每股税前净利 |  |
| `tws_qfa_employeenum` | 单季度.员工人数(一般产业) |  |
| `tws_qfa_eps_basic` | 单季度.基本每股收益 |  |
| `tws_qfa_eps_diluted` | 单季度.稀释每股收益 |  |
| `tws_qfa_errorbookingloss` | 单季度.错账损失率(证券) |  |
| `tws_qfa_exptorev_fin` | 单季度.金融业务成本率(保险、金融) |  |
| `tws_qfa_faturn` | 单季度.固定资产周转率 |  |
| `tws_qfa_grossprofitmargin` | 单季度.营业毛利率 |  |
| `tws_qfa_intcost` | 单季度.存借款平均利息(金融) |  |
| `tws_qfa_inttorev` | 单季度.放款利益率(金融) |  |
| `tws_qfa_invturndays` | 单季度.平均售货天数(一般产业) |  |
| `tws_qfa_loantodep` | 单季度.放款/存款(金融) |  |
| `tws_qfa_netprofitmargin` | 单季度.税后净利率 |  |
| `tws_qfa_oips` | 单季度.每股营业利益 |  |
| `tws_qfa_oprprofitmargin` | 单季度.营业利益率 |  |
| `tws_qfa_ortoeps` | 单季度.收支比率(保险、金融) |  |
| `tws_qfa_profitmargin` | 单季度.税前净利率 |  |
| `tws_qfa_qoq_np` | 单季度.税后净利(环比增长率) |  |
| `tws_qfa_qoq_op` | 单季度.营业利益(环比增长率) |  |
| `tws_qfa_qoq_or` | 单季度.营业收入(环比增长率) |  |
| `tws_qfa_quick` | 单季度.速动比率(一般产业、证券) |  |
| `tws_qfa_retntion` | 单季度.内部保留比率 |  |
| `tws_qfa_roa` | 单季度.资产报酬率 |  |
| `tws_qfa_roe` | 单季度.净值报酬率(ROE) |  |
| `tws_qfa_share_basic` | 单季度.加权平均股本 |  |
| `tws_qfa_sps` | 单季度.每股营业额 |  |
| `tws_qfa_tradingloss` | 单季度.买卖损失率(证券) |  |
| `tws_qfa_yoy_assets` | 单季度.总资产(同比增长率) |  |
| `tws_qfa_yoy_ebt` | 单季度.税前净利(同比增长率) |  |
| `tws_qfa_yoy_equity` | 单季度.净资产(同比增长率) |  |
| `tws_qfa_yoy_fa` | 单季度.折旧性固定资产(同比增长率) |  |
| `tws_qfa_yoy_np` | 单季度.税后净利(同比增长率) |  |
| `tws_qfa_yoy_oi` | 单季度.营业利益(同比增长率) |  |
| `tws_qfa_yoy_or` | 单季度.营业收入(同比增长率) |  |
| `tws_qstm_cs` | 单季度.来自营运之现金流量 |  |
| `tws_qstm_is` | 单季度.持续经营利润(税前) |  |
| `tws_share_total` | 总股数 | DEALDATE |
| `tws_share_totaltradable` | 流通在外股数 | DEALDATE |
| `tws_stm_auditdate` | 签证日 | REPORTDATE |
| `tws_stm_auditopin` | 会计师意见 | REPORTDATE |
| `tws_stm_auditor` | 会计师事务所 | REPORTDATE |
| `tws_stm_bs` | 流动资产合计 | ITEMSCODE、REPORTDATE |
| `tws_stm_bs_011a` | 附卖回票券投资 | REPORTDATE |
| `tws_stm_bs_016z` | 应收证券借贷款项 | REPORTDATE |
| `tws_stm_bs_017l` | 生物资产流动 | REPORTDATE |
| `tws_stm_bs_017n` | 生物资产非流动 | REPORTDATE |
| `tws_stm_bs_017o` | 应收款项 | REPORTDATE |
| `tws_stm_bs_017p` | 分出未满期保费准备净额 | REPORTDATE |
| `tws_stm_bs_017q` | 分出赔款准备净额 | REPORTDATE |
| `tws_stm_bs_017r` | 分出保费不足准备净额 | REPORTDATE |
| `tws_stm_bs_017s` | 分出其他保险准备净额 | REPORTDATE |
| `tws_stm_bs_017z` | 合约资产－流动 | REPORTDATE |
| `tws_stm_bs_018l` | 预付退休费(流动) | REPORTDATE |
| `tws_stm_bs_01aa` | 分出责任准备净额 | REPORTDATE |
| `tws_stm_bs_01ab` | 分出负债适足准备净额 | REPORTDATE |
| `tws_stm_bs_01ac` | 再保险合约资产净额 | REPORTDATE |
| `tws_stm_bs_01as` | 杠杆保证金契约交易客户保证金专户 | REPORTDATE |
| `tws_stm_bs_01au` | 应收借贷款项－不限用途 | REPORTDATE |
| `tws_stm_bs_01ba` | 透过损益按公允价值衡量之金融资产 | REPORTDATE |
| `tws_stm_bs_01bb` | 按摊销后成本衡量之金融资产 | REPORTDATE |
| `tws_stm_bs_031w` | 长投—基金 | REPORTDATE |
| `tws_stm_bs_032c` | 长投—特别准备金 | REPORTDATE |
| `tws_stm_bs_081a` | 递延取得成本 | REPORTDATE |
| `tws_stm_bs_082c` | 发展中之无形资产 | REPORTDATE |
| `tws_stm_bs_082j` | 特许权 | REPORTDATE |
| `tws_stm_bs_089j` | 分离账户保险商品资产 | REPORTDATE |
| `tws_stm_bs_089l` | 存出保证金 | REPORTDATE |
| `tws_stm_bs_089m` | 存出再保责任准备金 | REPORTDATE |
| `tws_stm_bs_089q` | 递延借项－非流动 | REPORTDATE |
| `tws_stm_bs_089y` | 其他什项资产 | REPORTDATE |
| `tws_stm_bs_112k` | 附买回票券投资 | REPORTDATE |
| `tws_stm_bs_112m` | 透过损益按公允价值衡量之金融负债 | REPORTDATE |
| `tws_stm_bs_112n` | 按摊销后成本衡量之金融负债 | REPORTDATE |
| `tws_stm_bs_113e` | 应付再保赔款与给付 | REPORTDATE |
| `tws_stm_bs_1140` | 应付代理店款 | REPORTDATE |
| `tws_stm_bs_117d` | 其它应付款 | REPORTDATE |
| `tws_stm_bs_118e` | 合约负债－流动 | REPORTDATE |
| `tws_stm_bs_118h` | 专户分户帐客户权益 | REPORTDATE |
| `tws_stm_bs_118i` | 杠杆保证金契约交易交易人权益 | REPORTDATE |
| `tws_stm_bs_119p` | 借券存入保证金 | REPORTDATE |
| `tws_stm_bs_119q` | 代收款项 | REPORTDATE |
| `tws_stm_bs_1226` | 租赁负债─流动 | REPORTDATE |
| `tws_stm_bs_123a` | 负债准备－流动 | REPORTDATE |
| `tws_stm_bs_140` | 应收代理店款 | REPORTDATE |
| `tws_stm_bs_1444` | 长期递延收入 | REPORTDATE |
| `tws_stm_bs_1446` | 租赁负债 | REPORTDATE |
| `tws_stm_bs_148a` | 其它金融负债 | REPORTDATE |
| `tws_stm_bs_1491` | 递延手续费收入 | REPORTDATE |
| `tws_stm_bs_1569` | 其他负债准备 | REPORTDATE |
| `tws_stm_bs_156k` | 员工福利负债准备 | REPORTDATE |
| `tws_stm_bs_156l` | 除役负债准备 | REPORTDATE |
| `tws_stm_bs_156n` | 员工福利－应计退休金负债 | REPORTDATE |
| `tws_stm_bs_156p` | 合约负债-非流动 | REPORTDATE |
| `tws_stm_bs_1590` | 其他非流动负债 | REPORTDATE |
| `tws_stm_bs_175a` | 其他保险准备 | REPORTDATE |
| `tws_stm_bs_1770` | 负债适足准备 | REPORTDATE |
| `tws_stm_bs_1780` | 保险契约准备－金融商品性质 | REPORTDATE |
| `tws_stm_bs_1790` | 外汇价格变动准备 | REPORTDATE |
| `tws_stm_bs_200e` | 归属母公司股东权益 | REPORTDATE |
| `tws_stm_bs_211e` | 股本 | REPORTDATE |
| `tws_stm_bs_231k` | 处分子公司价差公积 | REPORTDATE |
| `tws_stm_bs_231l` | 限制员工权利股票公积 | REPORTDATE |
| `tws_stm_bs_2341` | 保留盈余 | REPORTDATE |
| `tws_stm_bs_2461` | 透过其他综合损益按公允价值衡量之金融资产未实现损益 | REPORTDATE |
| `tws_stm_bs_246b` | 避险工具损益 | REPORTDATE |
| `tws_stm_bs_2471` | 员工未赚得酬劳 | REPORTDATE |
| `tws_stm_bs_2472` | 指定按公允价值衡量之金融负债信用风险变动影响数 | REPORTDATE |
| `tws_stm_bs_2473` | 确定福利计划再衡量数 | REPORTDATE |
| `tws_stm_bs_2474` | 采用覆盖法重分类之其他综合损益 | REPORTDATE |
| `tws_stm_bs_2480` | 其他权益 | REPORTDATE |
| `tws_stm_bs_2801` | 共同控制下前手权益 | REPORTDATE |
| `tws_stm_bs_2802` | 合并前非属共同控制股权 | REPORTDATE |
| `tws_stm_bs_374` | 受限制资产 | REPORTDATE |
| `tws_stm_bs_391` | 合约资产－非流动 | REPORTDATE |
| `tws_stm_bs_813` | 递延所得税资产(BS) | REPORTDATE |
| `tws_stm_bs_814` | 其他递延资产净额 | REPORTDATE |
| `tws_stm_bs_846` | 长期预付租金 | REPORTDATE |
| `tws_stm_bs_847` | 预付设备款 | REPORTDATE |
| `tws_stm_bs_902` | 特殊用途基金 | REPORTDATE |
| `tws_stm_bs_960` | 非流动资产 | REPORTDATE |
| `tws_stm_bs_966` | 使用权资产 | REPORTDATE |
| `tws_stm_cpa1` | 会计师1 | REPORTDATE |
| `tws_stm_cpa2` | 会计师2 | REPORTDATE |
| `tws_stm_cpa3` | 会计师3 | REPORTDATE |
| `tws_stm_cs` | 本期产生现金流量 | ITEMSCODE、REPORTDATE |
| `tws_stm_cs_7002` | 税前净利－CFO | REPORTDATE |
| `tws_stm_cs_720c` | 收取之利息－CFO | REPORTDATE |
| `tws_stm_cs_721j` | 利息收入－CFO | REPORTDATE |
| `tws_stm_cs_721k` | 利息费用－CFO | REPORTDATE |
| `tws_stm_cs_721m` | 利息净收益－CFO | REPORTDATE |
| `tws_stm_cs_721n` | 金融资产重分类净损失(利益) | REPORTDATE |
| `tws_stm_cs_721p` | 透过损益按公允价值衡量金融资产及负债之净损(益)－CFO | REPORTDATE |
| `tws_stm_cs_721r` | 除列按摊销后成本衡量金融资产净损(益)－CFO | REPORTDATE |
| `tws_stm_cs_721s` | 金融资产重分类净损失(利益)－CFO | REPORTDATE |
| `tws_stm_cs_721t` | 采覆盖法重分类之损(益) | REPORTDATE |
| `tws_stm_cs_722f` | 处分投资性不动产损(益)－CFO | REPORTDATE |
| `tws_stm_cs_722g` | 处分无形资产损(益)－CFO | REPORTDATE |
| `tws_stm_cs_722h` | 买回公司债损失(利益)－CFO | REPORTDATE |
| `tws_stm_cs_7231` | 透过损益按公允价值衡量之金融资产(增)减－CFO | REPORTDATE |
| `tws_stm_cs_7232` | 透过损益按公允价值衡量金融负债增加(减少)－CFO | REPORTDATE |
| `tws_stm_cs_7236` | 按摊销后成本衡量之债务工具投资(增)减－CFO | REPORTDATE |
| `tws_stm_cs_7241` | 具金融商品性质之保险契约准备净变动－CFO | REPORTDATE |
| `tws_stm_cs_724d` | 各项保险负债净变动－CFO | REPORTDATE |
| `tws_stm_cs_724g` | 外汇价格变动准备净变动－CFO | REPORTDATE |
| `tws_stm_cs_724k` | 其他各项负债准备净变动－CFO | REPORTDATE |
| `tws_stm_cs_724l` | 收取之股利－CFO | REPORTDATE |
| `tws_stm_cs_724m` | 存放央行及拆借同业(增)减 | REPORTDATE |
| `tws_stm_cs_724n` | 非投资之预期信用减损(回转)-CFO | REPORTDATE |
| `tws_stm_cs_724p` | 借券存入保证金增(减) | REPORTDATE |
| `tws_stm_cs_724q` | 应收证券借贷款项(增)减 | REPORTDATE |
| `tws_stm_cs_724r` | 违约证券(增)减 | REPORTDATE |
| `tws_stm_cs_724s` | 转融通借入款增(减) | REPORTDATE |
| `tws_stm_cs_724t` | 转融通保证金(增)减 | REPORTDATE |
| `tws_stm_cs_724w` | 应收转融通担保价款(增) | REPORTDATE |
| `tws_stm_cs_724x` | 借券担保价款(增)减 | REPORTDATE |
| `tws_stm_cs_724y` | 借券存出保证金(增)减 | REPORTDATE |
| `tws_stm_cs_724z` | 融券存入保证金增(减) | REPORTDATE |
| `tws_stm_cs_7261` | 保证责任准备净变动－CFO | REPORTDATE |
| `tws_stm_cs_7262` | 融资承诺准备净变动－CFO | REPORTDATE |
| `tws_stm_cs_726a` | 呆账费用、承诺及保证责任准备提存－CFO | REPORTDATE |
| `tws_stm_cs_726b` | 资产证券化损失(利益)－CFO | REPORTDATE |
| `tws_stm_cs_727b` | 客户保证金专户(增)减 | REPORTDATE |
| `tws_stm_cs_727c` | 应收证券融资款(增)减 | REPORTDATE |
| `tws_stm_cs_727d` | 金融资产重分类净损(益) | REPORTDATE |
| `tws_stm_cs_727g` | 营业外金融商品按公允价值衡量之损失(利益) | REPORTDATE |
| `tws_stm_cs_727h` | 未实现认购(售)权证发行损失(利益) | REPORTDATE |
| `tws_stm_cs_727i` | 附卖回票券投资(增)减 | REPORTDATE |
| `tws_stm_cs_727j` | 附买回票券负债增(减) | REPORTDATE |
| `tws_stm_cs_727k` | 应计退休金负债增(减) | REPORTDATE |
| `tws_stm_cs_727l` | 合约资产(增加)减少－CFO | REPORTDATE |
| `tws_stm_cs_727n` | 生物性资产(增加)减少－CFO | REPORTDATE |
| `tws_stm_cs_727z` | 附买回债券负债增(减) | REPORTDATE |
| `tws_stm_cs_728c` | 应付融券担保价款增(减) | REPORTDATE |
| `tws_stm_cs_728d` | 递延手续费收入增(减) | REPORTDATE |
| `tws_stm_cs_729c` | 调整项(出货)－CFO | REPORTDATE |
| `tws_stm_cs_7301` | 存出保证金增加－CFI | REPORTDATE |
| `tws_stm_cs_7302` | 存出保证金减少－CFI | REPORTDATE |
| `tws_stm_cs_7303` | 存出再保责任准备金增加－CFI | REPORTDATE |
| `tws_stm_cs_7304` | 存出再保责任准备金减少－CFI | REPORTDATE |
| `tws_stm_cs_7309` | 金融资产证券化款项－CFI | REPORTDATE |
| `tws_stm_cs_732c` | 营业保证金(增)减－CFI | REPORTDATE |
| `tws_stm_cs_732d` | 交割结算金(增)减－CFI | REPORTDATE |
| `tws_stm_cs_732e` | 其他应收款(增)减－CFI | REPORTDATE |
| `tws_stm_cs_7340` | 投资性不动产出售(购买)－CFI | REPORTDATE |
| `tws_stm_cs_7353` | 处分子公司现金流出 | REPORTDATE |
| `tws_stm_cs_736a` | 金融资产证券化款项 | REPORTDATE |
| `tws_stm_cs_736c` | 透过损益按公允价值衡量之金融资产(增)减－CFI | REPORTDATE |
| `tws_stm_cs_736d` | 按摊销后成本衡量之金融资产(增)减－CFI | REPORTDATE |
| `tws_stm_cs_736e` | (买)卖避险之金融资产及负债－CFI | REPORTDATE |
| `tws_stm_cs_739b` | 收取之股利－CFI | REPORTDATE |
| `tws_stm_cs_739c` | 收取之利息－CFI | REPORTDATE |
| `tws_stm_cs_739d` | 退还(支付)之所得税－CFI | REPORTDATE |
| `tws_stm_cs_739e` | 调整项(出货)－CFI | REPORTDATE |
| `tws_stm_cs_7401` | 存入保证金增加－CFF | REPORTDATE |
| `tws_stm_cs_7402` | 存入保证金减少－CFF | REPORTDATE |
| `tws_stm_cs_7403` | 存入再保责任准备金增加－CFF | REPORTDATE |
| `tws_stm_cs_7404` | 存入再保责任准备金减少－CFF | REPORTDATE |
| `tws_stm_cs_7411` | 短期借款增(减) | REPORTDATE |
| `tws_stm_cs_7412` | 应付短期票券增(减) | REPORTDATE |
| `tws_stm_cs_7433` | 按摊销后成本衡量之金融负债增加(减少)－CFF | REPORTDATE |
| `tws_stm_cs_7434` | 透过损益FV金负增(减)－CFF | REPORTDATE |
| `tws_stm_cs_7448` | 发行特别股负债 | REPORTDATE |
| `tws_stm_cs_7449` | 偿还特别股负债 | REPORTDATE |
| `tws_stm_cs_744a` | 取得子公司股权 | REPORTDATE |
| `tws_stm_cs_744b` | 处分子公司股权 | REPORTDATE |
| `tws_stm_cs_744d` | 金融资产证券化款项－CFF | REPORTDATE |
| `tws_stm_cs_744e` | 短期借款增加 | REPORTDATE |
| `tws_stm_cs_744f` | 应付商业本票增(减) | REPORTDATE |
| `tws_stm_cs_744h` | 短期借款减少 | REPORTDATE |
| `tws_stm_cs_744i` | 应付商业本票减少 | REPORTDATE |
| `tws_stm_cs_7460` | 退还(支付)之所得税－CFF | REPORTDATE |
| `tws_stm_cs_74ab` | 处分子公司股权－CFF | REPORTDATE |
| `tws_stm_cs_7501` | 存出保证金(增)减 | REPORTDATE |
| `tws_stm_cs_7502` | 存出再保责任准备金(增)减 | REPORTDATE |
| `tws_stm_cs_7503` | 应付再保赔款与给付增(减) | REPORTDATE |
| `tws_stm_cs_7504` | 存入保证金增(减) | REPORTDATE |
| `tws_stm_cs_7505` | 存入再保责任准备金增(减) | REPORTDATE |
| `tws_stm_cs_7515` | 合约负债增加(减少)－CFO | REPORTDATE |
| `tws_stm_cs_7531` | 存货(增加)减少－CFO | REPORTDATE |
| `tws_stm_cs_7532` | 存货跌价损失增加(减少)－CFO | REPORTDATE |
| `tws_stm_cs_7533` | 存货盘(盈)亏及报废－CFO | REPORTDATE |
| `tws_stm_cs_7546` | 负债准备增加(减少)－CFO | REPORTDATE |
| `tws_stm_cs_7568` | 再保险合约资产(增)减－CFO | REPORTDATE |
| `tws_stm_cs_7712` | 支付之利息－CFF | REPORTDATE |
| `tws_stm_cs_7713` | 支付之股利－CFO | REPORTDATE |
| `tws_stm_cs_7714` | 支付之利息－CFO | REPORTDATE |
| `tws_stm_cs_7721` | 退还(支付)之所得税－CFO | REPORTDATE |
| `tws_stm_cs_7911` | IAS7现金定义附卖回票债券 | REPORTDATE |
| `tws_stm_cs_7917` | 资产负债表帐列现金 | REPORTDATE |
| `tws_stm_cs_7918` | 其他符合之约当现金 | REPORTDATE |
| `tws_stm_cs_7919` | IAS7现金定义－存拆同业 | REPORTDATE |
| `tws_stm_cs_w39g` | 代收款增(减) | REPORTDATE |
| `tws_stm_is` | 营业收入 | ITEMSCODE、REPORTDATE |
| `tws_stm_is_211f` | 加权平均股数 | REPORTDATE |
| `tws_stm_is_211i` | 加权平均股数－稀释 | REPORTDATE |
| `tws_stm_is_2402` | 税前息前净利 | REPORTDATE |
| `tws_stm_is_2403` | 税前息前折旧前净利 | REPORTDATE |
| `tws_stm_is_240d` | 库藏股数－母公司 | REPORTDATE |
| `tws_stm_is_240e` | 库藏股数－子公司持有母公司股票或其他 | REPORTDATE |
| `tws_stm_is_240g` | 库藏股数(母持及子持母) | REPORTDATE |
| `tws_stm_is_3101` | 营收－处分投资收入 | REPORTDATE |
| `tws_stm_is_3102` | 营收－租金收入 | REPORTDATE |
| `tws_stm_is_3103` | 营收－投资收益 | REPORTDATE |
| `tws_stm_is_3105` | 营业收入毛额 | REPORTDATE |
| `tws_stm_is_310a` | 营收－处分土地收入 | REPORTDATE |
| `tws_stm_is_310f` | 投资预期信用减损损失及回转利益 | REPORTDATE |
| `tws_stm_is_3115` | 出售证券净利损－自营 | REPORTDATE |
| `tws_stm_is_3116` | 出售证券净利损－承销 | REPORTDATE |
| `tws_stm_is_311b` | 借贷款项手续费收入 | REPORTDATE |
| `tws_stm_is_311c` | 借券收入 | REPORTDATE |
| `tws_stm_is_311d` | 应付抵缴保证证券回利 | REPORTDATE |
| `tws_stm_is_311e` | 应付抵缴保证证券评利 | REPORTDATE |
| `tws_stm_is_311f` | 出售票券利益 | REPORTDATE |
| `tws_stm_is_311g` | 财务管理业务净收益 | REPORTDATE |
| `tws_stm_is_311i` | 指定为透过损益按公允价值衡量之金融资产净利益 | REPORTDATE |
| `tws_stm_is_311j` | 指定为透过损益按公允价值衡量之金融负债净利益 | REPORTDATE |
| `tws_stm_is_311k` | 透过FVOCI债务工具投资已实现净利益(损) | REPORTDATE |
| `tws_stm_is_312a` | 期货管理费收入 | REPORTDATE |
| `tws_stm_is_312b` | 经理费收入 | REPORTDATE |
| `tws_stm_is_312c` | 证券佣金收入 | REPORTDATE |
| `tws_stm_is_312m` | 衍生工具净利益(损失)－柜台－换利净(损)益 | REPORTDATE |
| `tws_stm_is_312n` | 业外－金融资产透过公允价值衡量之净利益(损失) | REPORTDATE |
| `tws_stm_is_312o` | 业外－金融负债透过公允价值衡量之净利益(损失) | REPORTDATE |
| `tws_stm_is_312p` | 业外－其他利益及损失 | REPORTDATE |
| `tws_stm_is_312s` | 业外－选择权契约净利益(损失) | REPORTDATE |
| `tws_stm_is_312t` | 业外－期货契约净利益(损失) | REPORTDATE |
| `tws_stm_is_312u` | 业外－利息收支 | REPORTDATE |
| `tws_stm_is_312v` | 衍生工具净(损)益－柜台－其他衍生工具净(损)益 | REPORTDATE |
| `tws_stm_is_312w` | 衍生工具净利益(损失)－柜台－资产交换选择权净(损)益 | REPORTDATE |
| `tws_stm_is_312x` | 衍生工具净利益(损失)－柜台－利率选择权净(损)益 | REPORTDATE |
| `tws_stm_is_312y` | 衍生工具净利益(损失)－期货－选择权交易净(损)益 | REPORTDATE |
| `tws_stm_is_312z` | 衍生工具净利益(损失)－期货－期货契约净(损)益 | REPORTDATE |
| `tws_stm_is_3130` | 退回及折让 | REPORTDATE |
| `tws_stm_is_3140` | 出售证券净利损－避险 | REPORTDATE |
| `tws_stm_is_3149` | 发行权证利益－到期前履约利益 | REPORTDATE |
| `tws_stm_is_314a` | 发行权证利益－逾期失效利益 | REPORTDATE |
| `tws_stm_is_314b` | 发行权证费用 | REPORTDATE |
| `tws_stm_is_3166` | 发行权证净损益－负债价值变动净利益(损失) | REPORTDATE |
| `tws_stm_is_3167` | 发行权证净损益－再买回价值变动净利益(损失) | REPORTDATE |
| `tws_stm_is_3175` | 营业证券透过公允价值衡量之净利益(损失)－自营 | REPORTDATE |
| `tws_stm_is_3176` | 营业证券透过公允价值衡量之净利益(损失)－承销 | REPORTDATE |
| `tws_stm_is_3177` | 营业证券透过公允价值衡量之净利益(损失)－避险 | REPORTDATE |
| `tws_stm_is_3178` | 应回补债券透过公允价值衡量之净利益(损失)－避险 | REPORTDATE |
| `tws_stm_is_317e` | 透过损益按公允价值衡量之金融资产及负债损益 | REPORTDATE |
| `tws_stm_is_3203` | 成本－租金成本 | REPORTDATE |
| `tws_stm_is_3204` | 成本－处分投资成本 | REPORTDATE |
| `tws_stm_is_3205` | 成本－投资损失 | REPORTDATE |
| `tws_stm_is_3206` | 销货成本 | REPORTDATE |
| `tws_stm_is_320a` | 成本－出售土地 | REPORTDATE |
| `tws_stm_is_321e` | 承销作业手续费支出 | REPORTDATE |
| `tws_stm_is_321g` | 借券交易损失 | REPORTDATE |
| `tws_stm_is_321h` | 转融通手续费支出 | REPORTDATE |
| `tws_stm_is_3359` | 证券佣金支出 | REPORTDATE |
| `tws_stm_is_335h` | 期货管理费支出 | REPORTDATE |
| `tws_stm_is_336l` | 其他营业费用(营业费用) | REPORTDATE |
| `tws_stm_is_339r` | 其他收益及费损净额 | REPORTDATE |
| `tws_stm_is_339s` | 其他费用 | REPORTDATE |
| `tws_stm_is_339t` | 预期信用减损(损失)利益－营业费用 | REPORTDATE |
| `tws_stm_is_340c` | 签单保费收入 | REPORTDATE |
| `tws_stm_is_340d` | 再保费收入 | REPORTDATE |
| `tws_stm_is_340e` | 自留满期保费收入 | REPORTDATE |
| `tws_stm_is_340f` | 业外－营业外损益合计 | REPORTDATE |
| `tws_stm_is_341z` | 利息以外净损益 | REPORTDATE |
| `tws_stm_is_344h` | 业外－金融资产减损(损)益 | REPORTDATE |
| `tws_stm_is_345c` | 不动产、厂房及设备减损回转利益 | REPORTDATE |
| `tws_stm_is_345d` | 无形资产减损回转利益 | REPORTDATE |
| `tws_stm_is_345e` | 其他减损回转利益 | REPORTDATE |
| `tws_stm_is_348c` | 其他收入－其他 | REPORTDATE |
| `tws_stm_is_348d` | 被避险项目之净损益－公允价值避险 | REPORTDATE |
| `tws_stm_is_348e` | 外汇价格变动准备净变动IS | REPORTDATE |
| `tws_stm_is_348h` | 证券承销收入净额 | REPORTDATE |
| `tws_stm_is_348i` | 证券自营费用 | REPORTDATE |
| `tws_stm_is_348j` | 其他净投资损益 | REPORTDATE |
| `tws_stm_is_348k` | 其他营业收入－利息收入 | REPORTDATE |
| `tws_stm_is_348l` | 其他营业收入－其他 | REPORTDATE |
| `tws_stm_is_348r` | 债务协商修改净损益 | REPORTDATE |
| `tws_stm_is_3491` | 违约金收入 | REPORTDATE |
| `tws_stm_is_3493` | 冲销逾期应付帐款利益 | REPORTDATE |
| `tws_stm_is_3494` | 预期信用减损利益 | REPORTDATE |
| `tws_stm_is_3498` | 赔偿收入 | REPORTDATE |
| `tws_stm_is_349d` | 证券经纪收入净额 | REPORTDATE |
| `tws_stm_is_349e` | 避险工具之净损益－公允价值避险 | REPORTDATE |
| `tws_stm_is_34a9` | 其他利息以外净损益 | REPORTDATE |
| `tws_stm_is_34aw` | 权利金收入 | REPORTDATE |
| `tws_stm_is_34ax` | 廉价购买收益 | REPORTDATE |
| `tws_stm_is_34ay` | 资产评价利益 | REPORTDATE |
| `tws_stm_is_34bd` | 透过损益按公允价值衡量之金融资产(负债)利益 | REPORTDATE |
| `tws_stm_is_34be` | 买回公司债利益 | REPORTDATE |
| `tws_stm_is_34bf` | 补助收益 | REPORTDATE |
| `tws_stm_is_34bg` | 按摊销后成本衡量之金融负债利益 | REPORTDATE |
| `tws_stm_is_34bk` | 预期信用减损(损失)利益 | REPORTDATE |
| `tws_stm_is_34bl` | 除列按摊销后成本金资损益 | REPORTDATE |
| `tws_stm_is_34bm` | 金融资产重分类损益 | REPORTDATE |
| `tws_stm_is_34bn` | 避险工具之利益 | REPORTDATE |
| `tws_stm_is_34bp` | 采用覆盖法重分类之损益 | REPORTDATE |
| `tws_stm_is_34bq` | 其他投资减损(损失)回转 | REPORTDATE |
| `tws_stm_is_34z9` | 其他什项损益 | REPORTDATE |
| `tws_stm_is_3501` | 财务成本 | REPORTDATE |
| `tws_stm_is_3505` | 未满期保费准备净变动 | REPORTDATE |
| `tws_stm_is_3506` | 责任准备净变动 | REPORTDATE |
| `tws_stm_is_350j` | 承保费用 | REPORTDATE |
| `tws_stm_is_350k` | 佣金费用 | REPORTDATE |
| `tws_stm_is_351n` | 财务成本－其他 | REPORTDATE |
| `tws_stm_is_351r` | 优存超额利息 | REPORTDATE |
| `tws_stm_is_351s` | 利息支出－租赁负债 | REPORTDATE |
| `tws_stm_is_3520` | 自留保险赔款与给付 | REPORTDATE |
| `tws_stm_is_3525` | 负债适足准备净变动 | REPORTDATE |
| `tws_stm_is_3527` | 其他准备净变动 | REPORTDATE |
| `tws_stm_is_3528` | 保险契约准备净变动－金融商品 | REPORTDATE |
| `tws_stm_is_354w` | 不动产、厂房及设备减损损失 | REPORTDATE |
| `tws_stm_is_354x` | 无形资产减损损失 | REPORTDATE |
| `tws_stm_is_354z` | 其他减损损失 | REPORTDATE |
| `tws_stm_is_3551` | 呆账费用、承诺及保证责任准备提存 | REPORTDATE |
| `tws_stm_is_3552` | 保证责任准备提存 | REPORTDATE |
| `tws_stm_is_3553` | 其他各项提存∕回转 | REPORTDATE |
| `tws_stm_is_3556` | 融资承诺准备提存 | REPORTDATE |
| `tws_stm_is_358e` | 合约损失 | REPORTDATE |
| `tws_stm_is_3599` | 停工损失 | REPORTDATE |
| `tws_stm_is_359a` | 赔偿损失 | REPORTDATE |
| `tws_stm_is_359t` | 资产评价损失 | REPORTDATE |
| `tws_stm_is_359u` | 透过损益按公允价值衡量之金融资产(负债)损失 | REPORTDATE |
| `tws_stm_is_359v` | 其他利益及损失－其他 | REPORTDATE |
| `tws_stm_is_359w` | 其他利益及损失 | REPORTDATE |
| `tws_stm_is_35bd` | 买回公司债损失 | REPORTDATE |
| `tws_stm_is_35bg` | 按摊销后成本衡量之金融负债损失 | REPORTDATE |
| `tws_stm_is_35bn` | 避险工具之损失 | REPORTDATE |
| `tws_stm_is_3700` | 营业外收入及支出 | REPORTDATE |
| `tws_stm_is_3701` | 营业外收入及支出－其他 | REPORTDATE |
| `tws_stm_is_3942` | 不重分类至损益之项目－OCI | REPORTDATE |
| `tws_stm_is_3943` | 后续可能重分类至损益之项目－OCI | REPORTDATE |
| `tws_stm_is_3944` | 合并前非属共同控制股权综合损益－OCI | REPORTDATE |
| `tws_stm_is_3947` | 其他综合损益－OCI | REPORTDATE |
| `tws_stm_is_3948` | 不动产重估价之利益(损失)－不重分类－OCI | REPORTDATE |
| `tws_stm_is_3949` | 确定福利计划之再衡量数－不重分类－OCI | REPORTDATE |
| `tws_stm_is_394a` | 国外营运机构财务报表换算之兑换差额－可重分类－OCI | REPORTDATE |
| `tws_stm_is_394b` | 透FVOCI衡量债务工具投资未实现评价损益－可重分类－OCI | REPORTDATE |
| `tws_stm_is_394e` | 透FVOCI衡量权益工具投资未实现评价损益－不重分类－OCI | REPORTDATE |
| `tws_stm_is_394i` | 指定按公允价值衡量金融负债信用风险变动影响－不重分－OCI | REPORTDATE |
| `tws_stm_is_394j` | 待售待分业主非流资(处分群组)直接相关权益－不重分－OCI | REPORTDATE |
| `tws_stm_is_394k` | 采权益法认列关联企业及合资其他综合损益份额－不重分－OCI | REPORTDATE |
| `tws_stm_is_394l` | 其他综合损益－其他－不重分类－OCI | REPORTDATE |
| `tws_stm_is_394m` | 与其他综合损益组成部分相关之所得税－不重分类－OCI | REPORTDATE |
| `tws_stm_is_394n` | 待售待分业主非流资(处分群组)直接相关权益－可重分－OCI | REPORTDATE |
| `tws_stm_is_394o` | 采权益法认列关联企业及合资其他综合损益份额－可重分－OCI | REPORTDATE |
| `tws_stm_is_394p` | 其他综合损益－其他－可重分类－OCI | REPORTDATE |
| `tws_stm_is_394q` | 与其他综合损益组成部分相关之所得税－可重分类－OCI | REPORTDATE |
| `tws_stm_is_394r` | 避险工具之损益－不重分类－OCI | REPORTDATE |
| `tws_stm_is_394s` | 避险工具之损益－可重分类－OCI | REPORTDATE |
| `tws_stm_is_394t` | 采覆盖法重分类－可重分类－OCI | REPORTDATE |
| `tws_stm_is_3956` | 综合损益归属母公司 | REPORTDATE |
| `tws_stm_is_395s` | 稀释税后净利 | REPORTDATE |
| `tws_stm_is_3961` | 综合损益归属非控制权益 | REPORTDATE |
| `tws_stm_is_3964` | 归属共同控制下前手权益净利(损) | REPORTDATE |
| `tws_stm_is_3966` | 合并前非属共同控制股权损益 | REPORTDATE |
| `tws_stm_is_3967` | 综合损益归属共同控制下前手权益 | REPORTDATE |
| `tws_stm_is_3971` | 本期综合损益 | REPORTDATE |
| `tws_stm_is_r531` | 常续性税后净利 | REPORTDATE |
| `tws_stm_is_w34w` | 业外－其他利益及损失－其他 | REPORTDATE |
| `tws_val_mv` | 市值 | DEALDATE |
| `tws_val_pb_new` | 市净率(最新报告) | DEALDATE |
| `tws_val_pe_ttm` | 市盈率(前推12月) | DEALDATE |

<a id="分类-通用-指数"></a>

## 通用/指数（534 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `w_active_atm_code` | 主力平值期权代码 | TRADEDATE、OptionType、UnderType |
| `w_active_op_undly` | 活跃期权标的代码 | TRADEDATE、Exercisetype、TermType、Multipliertype |
| `w_anal_actualleverageratio` | 实际杠杆倍数 |  |
| `w_anal_amtratio` | 成交额认沽认购比率 | SettlementMonth、TRADEDATE |
| `w_anal_breakevenpoint` | 盈亏平衡点 |  |
| `w_anal_delta_exch` | Delta(交易所) | TRADEDATE |
| `w_anal_expiryamtratio` | 到期日期权成交额认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_anal_expiryoiratio` | 到期日期权持仓量认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_anal_expiryvolumeratio` | 到期日期权成交量认沽认购比率 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_anal_gamma_exch` | Gamma(交易所) | TRADEDATE |
| `w_anal_impliedvol_exch` | 期权隐含波动率(交易所) | TRADEDATE |
| `w_anal_intrinctvalue` | 内在价值 |  |
| `w_anal_leverageratio` | 杠杆倍数 |  |
| `w_anal_mid_impliedvol` | 期权中价隐含波动率 | TRADEDATE |
| `w_anal_oiratio` | 持仓量认沽认购比率 | SettlementMonth、TRADEDATE |
| `w_anal_premiumratio` | 溢价率 |  |
| `w_anal_pricedegree` | 价内外程度 |  |
| `w_anal_rho_exch` | Rho(交易所) | TRADEDATE |
| `w_anal_theoryvalue` | 理论价格 |  |
| `w_anal_theta_exch` | Theta(交易所) | TRADEDATE |
| `w_anal_timevalue` | 时间价值 |  |
| `w_anal_underlyinghisvol` | 正股历史波动率 |  |
| `w_anal_underlyinghisvol_30d` | 标的30日历史波动率 | TRADEDATE |
| `w_anal_underlyinghisvol_90d` | 标的90日历史波动率 | TRADEDATE |
| `w_anal_underlyingimpliedvol` | 正股隐含波动率 |  |
| `w_anal_underlyingtotalshare` | 正股总股本 |  |
| `w_anal_undimpvolchg` | 期权波动率涨跌 | TRADEDATE |
| `w_anal_vega_exch` | Vega(交易所) | TRADEDATE |
| `w_anal_volumeratio` | 成交量认沽认购比率 | SettlementMonth、TRADEDATE |
| `w_cont_atm_code` | 连续平值期权代码 | TRADEDATE、Month、OptionType、UnderType、Strike、AdjustmentState |
| `w_dq_amount` | 成交额 |  |
| `w_dq_avgprice` | 成交均价 |  |
| `w_dq_change` | 涨跌 |  |
| `w_dq_close` | 收盘价 |  |
| `w_dq_high` | 最高价 |  |
| `w_dq_highlimit` | 涨停价 |  |
| `w_dq_low` | 最低价 |  |
| `w_dq_lowlimit` | 跌停价 |  |
| `w_dq_open` | 开盘价 |  |
| `w_dq_pctchange` | 涨跌幅 |  |
| `w_dq_preclose` | 前收盘价 |  |
| `w_dq_quote_ask` | 最优报卖价 | TRADEDATE |
| `w_dq_quote_bid` | 最优报买价 | TRADEDATE |
| `w_dq_quote_mid` | 最优报中价 | TRADEDATE |
| `w_dq_swing` | 振幅 |  |
| `w_dq_turn` | 换手率 |  |
| `w_dq_us_amount` | 正股成交额 |  |
| `w_dq_us_avgprice` | 正股均价 |  |
| `w_dq_us_change` | 正股涨跌 |  |
| `w_dq_us_close` | 正股收盘价 |  |
| `w_dq_us_high` | 正股最高价 |  |
| `w_dq_us_low` | 正股最低价 |  |
| `w_dq_us_open` | 正股开盘价 |  |
| `w_dq_us_pctchange` | 正股涨跌幅 |  |
| `w_dq_us_preclose` | 正股前收盘价,w_dq_us_preclose, |  |
| `w_dq_us_swing` | 正股振幅 |  |
| `w_dq_us_turn` | 正股换手率 |  |
| `w_dq_us_volume` | 正股成交量 |  |
| `w_dq_volume` | 成交量 |  |
| `w_forward_adjust_date` | 期权到期日展期 | TRADEDATE、EndDate、TermAdjust、ActiveAdjust |
| `w_info_adjustratio` | 行权价及比例调整公式 |  |
| `w_info_callput` | 行权方式(认购/认沽) |  |
| `w_info_code` | 交易代码 |  |
| `w_info_d_vol_surface` | 品种隐含波动率曲面(按Delta) | TRADEDATE、Delta、Term、Construction、Exercisetype、Multipliertype |
| `w_info_dailyclosefee` | 期权平今手续费 | DEALDATE |
| `w_info_delta_atmcode` | Delta平值期权代码 | TRADEDATE、OptionalExpir、OptionType、Delta、AdjustmentState、Exercisetype、TermType、Multipliertype |
| `w_info_enddate` | 存续截止日期 |  |
| `w_info_equitycovered` | 权证类型(股本/备兑) |  |
| `w_info_euroamericanbermuda` | 行权类型(欧式/美式/百慕大式) |  |
| `w_info_exercisefee` | 期权行权履约手续费 | DEALDATE |
| `w_info_exercisingend` | 最后行权日 |  |
| `w_info_exercisingstart` | 行权起始日 |  |
| `w_info_exercode` | 行权代码 |  |
| `w_info_exername` | 行权简称 |  |
| `w_info_expirycallamount` | 到期日认购期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expirycalloi` | 到期日认购期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expirycallvolume` | 到期日认购期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryoptionamount` | 到期日期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryoptionoi` | 到期日期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryoptionvolume` | 到期日期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryputamount` | 到期日认沽期权成交额 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryputoi` | 到期日认沽期权持仓量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_expiryputvolume` | 到期日认沽期权成交量 | TRADEDATE、ExpirationDate、Exercisetype、TermType、Multipliertype |
| `w_info_guarantor` | 担保人 |  |
| `w_info_gurexpltn` | 担保说明 |  |
| `w_info_hedgefee` | 期权套保手续费 | DEALDATE |
| `w_info_inistrikeprice` | 初始行权价格 |  |
| `w_info_inistrikeratio` | 初始行权比例 |  |
| `w_info_issuer` | 发行人 |  |
| `w_info_issuer_iponum` | 首发数量 |  |
| `w_info_issuer_obj` | 发行对象，w_info_issuer_obj |  |
| `w_info_issuer_type` | 发行方式 |  |
| `w_info_issuernum` | 上市数量 |  |
| `w_info_lasttradingdate` | 最后交易日 |  |
| `w_info_listeddate` | 上市日期 |  |
| `w_info_m_atmcode` | 平值期权代码(价值状态) | TRADEDATE、ExpirationDate、OptionType、Moneyness、AdjustmentState、Exercisetype、TermType、Multipliertype |
| `w_info_m_vol_sufpctl` | 品种波动率曲面分位数 | TRADEDATE、Moneyness、Term、Method、Exercisetype、Multipliertype、StartDate、DATE |
| `w_info_m_vol_surface` | 品种隐含波动率曲面(按价值状态) | TRADEDATE、Moneyness、Term、Construction、Exercisetype、Multipliertype |
| `w_info_moneyness` | 价值状态 | TRADEDATE |
| `w_info_name` | 权证简称 |  |
| `w_info_nth_atmcode` | N挡平值期权代码 | TRADEDATE、OptionExpir、OptionType、StrikeRank、AdjustmentState、Exercisetype、TermType、Multipliertype |
| `w_info_op_cat` | 证券类型(期权用) | Level |
| `w_info_oplimitcust` | 客户期权持仓限额 | TRADEDATE、Category、Limit |
| `w_info_oplimitfutu` | 期货公司会员期权持仓限额 | TRADEDATE、Category、Limit |
| `w_info_oplimitmark` | 做市商期权持仓限额 | TRADEDATE、Category、Limit |
| `w_info_oplimitnonfu` | 非期货公司会员期权持仓限额 | TRADEDATE、Category、Limit |
| `w_info_opriskfreerate` | 期权无风险利率 | TRADEDATE |
| `w_info_orgshareholderratio` | 原股东配售比率 |  |
| `w_info_ptm` | 剩余存续期 | DEALDATE、TYPE |
| `w_info_ptmday` | 剩余存续期(天) |  |
| `w_info_ptmtradeday` | 剩余存续期(交易日) | TRADEDATE |
| `w_info_ptmyear` | 剩余存续期(年) |  |
| `w_info_refprice` | 上市首日参考价 |  |
| `w_info_repurchaseexpltn` | 回购说明 |  |
| `w_info_repurchaseprice` | 回购价格 |  |
| `w_info_settlementmethod` | 结算方式 |  |
| `w_info_startdate` | 存续起始日期 |  |
| `w_info_stoptradingdate` | 停止交易日 |  |
| `w_info_strikeprice` | 行权价格 |  |
| `w_info_strikeratio` | 行权比例 |  |
| `w_info_totaltm` | 总存续期 |  |
| `w_info_tradecode` | 期权代码(指定行权价) | SettlementMonth、ExercisePrice |
| `w_info_tradefee` | 期权交易手续费 | DEALDATE |
| `w_info_udly_maturity` | 期权标的及到期日列表 | TRADEDATE |
| `w_info_underlyingcode` | 正股代码 |  |
| `w_info_underlyingname` | 正股简称 |  |
| `w_info_underlyingwindcode` | 正股Wind代码 |  |
| `w_info_undly_variety` | 标的品种代码 |  |
| `w_info_whetheradjust` | 行权价及比例是否调整 |  |
| `w_iv_1m1000` | 1个月100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1000_n` | 1个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1000_nr` | 1个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1025` | 1个月102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1025_n` | 1个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1025_nr` | 1个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1050` | 1个月105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1050_n` | 1个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1050_nr` | 1个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m10dc_n` | 1个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m10dc_nr` | 1个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m10dp_n` | 1个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m10dp_nr` | 1个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1100` | 1个月110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1100_n` | 1个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1100_nr` | 1个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1200` | 1个月120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1200_n` | 1个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1200_nr` | 1个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1300` | 1个月130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m1300_n` | 1个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m1300_nr` | 1个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m15dc_n` | 1个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m15dc_nr` | 1个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m15dp_n` | 1个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m15dp_nr` | 1个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m25dc_n` | 1个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m25dc_nr` | 1个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m25dp_n` | 1个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m25dp_nr` | 1个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m35dc_n` | 1个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m35dc_nr` | 1个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1m35dp_n` | 1个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m35dp_nr` | 1个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1m50d_n` | 1个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_1m50d_nr` | 1个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_1m600` | 1个月60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m600_n` | 1个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m600_nr` | 1个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m800` | 1个月80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m800_n` | 1个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m800_nr` | 1个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m900` | 1个月90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m900_n` | 1个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m900_nr` | 1个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m950` | 1个月95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m950_n` | 1个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m950_nr` | 1个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m975` | 1个月97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1m975_n` | 1个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1m975_nr` | 1个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1000` | 1年100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1000_n` | 1年100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1000_nr` | 1年100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1025` | 1年102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1025_n` | 1年102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1025_nr` | 1年102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1050` | 1年105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1050_n` | 1年105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1050_nr` | 1年105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y10dc_n` | 1年10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y10dc_nr` | 1年10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y10dp_n` | 1年10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y10dp_nr` | 1年10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1100` | 1年110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1100_n` | 1年110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1100_nr` | 1年110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1200` | 1年120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1200_n` | 1年120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1200_nr` | 1年120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1300` | 1年130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y1300_n` | 1年130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y1300_nr` | 1年130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y15dc_n` | 1年15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y15dc_nr` | 1年15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y15dp_n` | 1年15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y15dp_nr` | 1年15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y25dc_n` | 1年25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y25dc_nr` | 1年25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y25dp_n` | 1年25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y25dp_nr` | 1年25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y35dc_n` | 1年35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y35dc_nr` | 1年35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_1y35dp_n` | 1年35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y35dp_nr` | 1年35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_1y50d_n` | 1年50d隐含波动率 | TRADEDATE、Model |
| `w_iv_1y50d_nr` | 1年50d隐含波动率 | TRADEDATE、Model |
| `w_iv_1y600` | 1年60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y600_n` | 1年60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y600_nr` | 1年60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y800` | 1年80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y800_n` | 1年80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y800_nr` | 1年80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y900` | 1年90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y900_n` | 1年90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y900_nr` | 1年90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y950` | 1年95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y950_n` | 1年95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y950_nr` | 1年95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y975` | 1年97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_1y975_n` | 1年97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_1y975_nr` | 1年97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1000` | 2个月100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1000_n` | 2个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1000_nr` | 2个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1025` | 2个月102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1025_n` | 2个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1025_nr` | 2个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1050` | 2个月105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1050_n` | 2个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1050_nr` | 2个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m10dc_n` | 2个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m10dc_nr` | 2个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m10dp_n` | 2个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m10dp_nr` | 2个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1100` | 2个月110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1100_n` | 2个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1100_nr` | 2个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1200` | 2个月120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1200_n` | 2个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1200_nr` | 2个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1300` | 2个月130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m1300_n` | 2个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m1300_nr` | 2个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m15dc_n` | 2个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m15dc_nr` | 2个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m15dp_n` | 2个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m15dp_nr` | 2个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m25dc_n` | 2个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m25dc_nr` | 2个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m25dp_n` | 2个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m25dp_nr` | 2个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m35dc_n` | 2个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m35dc_nr` | 2个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_2m35dp_n` | 2个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m35dp_nr` | 2个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_2m50d_n` | 2个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_2m50d_nr` | 2个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_2m600` | 2个月60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m600_n` | 2个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m600_nr` | 2个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m800` | 2个月80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m800_n` | 2个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m800_nr` | 2个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m900` | 2个月90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m900_n` | 2个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m900_nr` | 2个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m950` | 2个月95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m950_n` | 2个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m950_nr` | 2个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m975` | 2个月97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_2m975_n` | 2个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_2m975_nr` | 2个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1000` | 3个月100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1000_n` | 3个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1000_nr` | 3个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1025` | 3个月102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1025_n` | 3个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1025_nr` | 3个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1050` | 3个月105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1050_n` | 3个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1050_nr` | 3个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m10dc_n` | 3个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m10dc_nr` | 3个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m10dp_n` | 3个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m10dp_nr` | 3个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1100` | 3个月110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1100_n` | 3个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1100_nr` | 3个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1200` | 3个月120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1200_n` | 3个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1200_nr` | 3个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1300` | 3个月130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m1300_n` | 3个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m1300_nr` | 3个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m15dc_n` | 3个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m15dc_nr` | 3个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m15dp_n` | 3个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m15dp_nr` | 3个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m25dc_n` | 3个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m25dc_nr` | 3个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m25dp_n` | 3个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m25dp_nr` | 3个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m35dc_n` | 3个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m35dc_nr` | 3个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_3m35dp_n` | 3个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m35dp_nr` | 3个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_3m50d_n` | 3个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_3m50d_nr` | 3个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_3m600` | 3个月60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m600_n` | 3个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m600_nr` | 3个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m800` | 3个月80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m800_n` | 3个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m800_nr` | 3个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m900` | 3个月90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m900_n` | 3个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m900_nr` | 3个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m950` | 3个月95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m950_n` | 3个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m950_nr` | 3个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m975` | 3个月97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_3m975_n` | 3个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_3m975_nr` | 3个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1000` | 6个月100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1000_n` | 6个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1000_nr` | 6个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1025` | 6个月102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1025_n` | 6个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1025_nr` | 6个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1050` | 6个月105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1050_n` | 6个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1050_nr` | 6个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m10dc_n` | 6个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m10dc_nr` | 6个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m10dp_n` | 6个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m10dp_nr` | 6个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1100` | 6个月110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1100_n` | 6个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1100_nr` | 6个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1200` | 6个月120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1200_n` | 6个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1200_nr` | 6个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1300` | 6个月130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m1300_n` | 6个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m1300_nr` | 6个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m15dc_n` | 6个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m15dc_nr` | 6个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m15dp_n` | 6个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m15dp_nr` | 6个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m25dc_n` | 6个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m25dc_nr` | 6个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m25dp_n` | 6个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m25dp_nr` | 6个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m35dc_n` | 6个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m35dc_nr` | 6个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_6m35dp_n` | 6个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m35dp_nr` | 6个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_6m50d_n` | 6个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_6m50d_nr` | 6个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_6m600` | 6个月60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m600_n` | 6个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m600_nr` | 6个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m800` | 6个月80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m800_n` | 6个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m800_nr` | 6个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m900` | 6个月90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m900_n` | 6个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m900_nr` | 6个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m950` | 6个月95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m950_n` | 6个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m950_nr` | 6个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m975` | 6个月97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_6m975_n` | 6个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_6m975_nr` | 6个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1000` | 9个月100%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1000_n` | 9个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1000_nr` | 9个月100%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1025` | 9个月102.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1025_n` | 9个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1025_nr` | 9个月102.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1050` | 9个月105%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1050_n` | 9个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1050_nr` | 9个月105%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m10dc_n` | 9个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m10dc_nr` | 9个月10dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m10dp_n` | 9个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m10dp_nr` | 9个月10dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1100` | 9个月110%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1100_n` | 9个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1100_nr` | 9个月110%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1200` | 9个月120%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1200_n` | 9个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1200_nr` | 9个月120%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1300` | 9个月130%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m1300_n` | 9个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m1300_nr` | 9个月130%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m15dc_n` | 9个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m15dc_nr` | 9个月15dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m15dp_n` | 9个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m15dp_nr` | 9个月15dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m25dc_n` | 9个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m25dc_nr` | 9个月25dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m25dp_n` | 9个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m25dp_nr` | 9个月25dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m35dc_n` | 9个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m35dc_nr` | 9个月35dc隐含波动率 | TRADEDATE、Model |
| `w_iv_9m35dp_n` | 9个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m35dp_nr` | 9个月35dp隐含波动率 | TRADEDATE、Model |
| `w_iv_9m50d_n` | 9个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_9m50d_nr` | 9个月50d隐含波动率 | TRADEDATE、Model |
| `w_iv_9m600` | 9个月60%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m600_n` | 9个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m600_nr` | 9个月60%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m800` | 9个月80%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m800_n` | 9个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m800_nr` | 9个月80%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m900` | 9个月90%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m900_n` | 9个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m900_nr` | 9个月90%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m950` | 9个月95%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m950_n` | 9个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m950_nr` | 9个月95%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m975` | 9个月97.5%价值状态隐含波动率 | TRADEDATE |
| `w_iv_9m975_n` | 9个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_iv_9m975_nr` | 9个月97.5%价值状态隐含波动率 | TRADEDATE、Model |
| `w_mq_close` | 月收盘价 |  |
| `w_mq_high` | 月最高价 |  |
| `w_mq_low` | 月最低价 |  |
| `w_mq_open` | 月开盘价 |  |
| `w_mq_preclose` | 月前收盘价 |  |
| `w_mq_us_amount` | 正股月成交额 |  |
| `w_mq_us_avgprice` | 正股月均价 |  |
| `w_mq_us_avgturn` | 正股月平均换手率 |  |
| `w_mq_us_change` | 正股月涨跌 |  |
| `w_mq_us_close` | 正股月收盘价 |  |
| `w_mq_us_high` | 正股月最高价 |  |
| `w_mq_us_highclose` | 正股月最高收盘价 |  |
| `w_mq_us_low` | 正股月最低价 |  |
| `w_mq_us_lowclose` | 正股月最低收盘价 |  |
| `w_mq_us_open` | 正股月开盘价 |  |
| `w_mq_us_pctchange` | 正股月涨跌幅 |  |
| `w_mq_us_preclose` | 正股月前收盘价 |  |
| `w_mq_us_swing` | 正股月振幅 |  |
| `w_mq_us_turn` | 正股月换手率 |  |
| `w_mq_us_volume` | 正股月成交量 |  |
| `w_op_active_undly` | 期权主力标的代码 | TRADEDATE |
| `w_op_multipliertype` | 期权规模类型 |  |
| `w_op_termtype` | 期权期限类型 |  |
| `w_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `w_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `w_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `w_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `w_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `w_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `w_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `w_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `w_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `w_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `w_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `w_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `w_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `w_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `w_pq_us_amount` | 正股区间成交额 |  |
| `w_pq_us_avgprice` | 正股区间均价 |  |
| `w_pq_us_avgturn` | 正股区间平均换手率 |  |
| `w_pq_us_change` | 正股区间涨跌 |  |
| `w_pq_us_close` | 正股区间收盘价 |  |
| `w_pq_us_high` | 正股区间最高价 |  |
| `w_pq_us_highclose` | 正股区间最高收盘价 |  |
| `w_pq_us_low` | 正股区间最低价 |  |
| `w_pq_us_lowclose` | 正股区间最低收盘价 |  |
| `w_pq_us_open` | 正股区间开盘价 |  |
| `w_pq_us_pctchange` | 正股区间涨跌幅 |  |
| `w_pq_us_preclose` | 正股区间前收盘价 |  |
| `w_pq_us_swing` | 正股区间振幅 |  |
| `w_pq_us_turn` | 正股区间换手率 |  |
| `w_pq_us_volume` | 正股区间成交量 |  |
| `w_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `w_unit_accumulativeexercised` | 累计行权数量 |  |
| `w_unit_activated` | 创设余额 |  |
| `w_unit_activatorhold` | 创设人持有余额 |  |
| `w_unit_current` | 流通余额 |  |
| `w_unit_latest` | 最新余额 |  |
| `w_unit_over5pctholder` | 超过5%持有人 |  |
| `w_wq_close` | 周收盘价 |  |
| `w_wq_high` | 周最高价 |  |
| `w_wq_low` | 周最低价 |  |
| `w_wq_open` | 周开盘价 |  |
| `w_wq_preclose` | 周前收盘价 |  |
| `w_wq_us_amount` | 正股周成交额 |  |
| `w_wq_us_avgprice` | 正股周均价 |  |
| `w_wq_us_avgturn` | 正股周平均换手率 |  |
| `w_wq_us_change` | 正股周涨跌 |  |
| `w_wq_us_close` | 正股周收盘价 |  |
| `w_wq_us_high` | 正股周最高价 |  |
| `w_wq_us_highclose` | 正股周最高收盘价 |  |
| `w_wq_us_low` | 正股周最低价 |  |
| `w_wq_us_lowclose` | 正股周最低收盘价 |  |
| `w_wq_us_open` | 正股周开盘价 |  |
| `w_wq_us_pctchange` | 正股周涨跌幅 |  |
| `w_wq_us_preclose` | 正股周前收盘价 |  |
| `w_wq_us_swing` | 正股周振幅 |  |
| `w_wq_us_turn` | 正股周换手率 |  |
| `w_wq_us_volume` | 正股周成交量 |  |
| `w_yq_close` | 年收盘价 |  |
| `w_yq_high` | 年最高价 |  |
| `w_yq_low` | 年最低价 |  |
| `w_yq_open` | 年开盘价 |  |
| `w_yq_preclose` | 年前收盘价 |  |
| `w_yq_us_amount` | 正股年成交额 |  |
| `w_yq_us_avgprice` | 正股年均价 |  |
| `w_yq_us_avgturn` | 正股年平均换手率 |  |
| `w_yq_us_change` | 正股年涨跌 |  |
| `w_yq_us_close` | 正股年收盘价 |  |
| `w_yq_us_high` | 正股年最高价 |  |
| `w_yq_us_highclose` | 正股年最高收盘价 |  |
| `w_yq_us_low` | 正股年最低价 |  |
| `w_yq_us_lowclose` | 正股年最低收盘价 |  |
| `w_yq_us_open` | 正股年开盘价 |  |
| `w_yq_us_pctchange` | 正股年涨跌幅 |  |
| `w_yq_us_preclose` | 正股年前收盘价 |  |
| `w_yq_us_swing` | 正股年振幅 |  |
| `w_yq_us_turn` | 正股年换手率 |  |
| `w_yq_us_volume` | 正股年成交量 |  |

<a id="分类-基金专项"></a>

## 基金(专项)（196 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `fs_dq_amount` | 成交额 |  |
| `fs_dq_avgprice` | 成交均价 |  |
| `fs_dq_change` | 涨跌 |  |
| `fs_dq_change_settlement` | 涨跌（结算价） |  |
| `fs_dq_close` | 收盘价 |  |
| `fs_dq_high` | 最高价 |  |
| `fs_dq_low` | 最低价 |  |
| `fs_dq_oi` | 持仓量 |  |
| `fs_dq_oichange` | 持仓变化 |  |
| `fs_dq_open` | 开盘价 |  |
| `fs_dq_pctchange` | 涨跌幅 |  |
| `fs_dq_pctchange_settlement` | 涨跌幅（结算价） |  |
| `fs_dq_presettle` | 前结算价 |  |
| `fs_dq_settle` | 结算价 |  |
| `fs_dq_swing` | 振幅 |  |
| `fs_dq_volume` | 成交量 |  |
| `fs_info_cdmonths` | 合约月份说明 |  |
| `fs_info_ceabb` | 合约英文简称 |  |
| `fs_info_cename` | 合约英文名称 |  |
| `fs_info_changelt` | 涨跌幅限制 |  |
| `fs_info_code` | 期货代码 |  |
| `fs_info_ddate` | 交割日期 |  |
| `fs_info_dlmonth` | 交割月份 |  |
| `fs_info_exname` | 交易所简称 |  |
| `fs_info_ftdate` | 开始交易日 |  |
| `fs_info_ftmargins` | 最初交易保证金 |  |
| `fs_info_lddate` | 最后交割日 |  |
| `fs_info_lprice` | 挂牌基准价 |  |
| `fs_info_ltdate` | 最后交易日 |  |
| `fs_info_ltdated` | 最后交易日说明 |  |
| `fs_info_margin` | 交易保证金 |  |
| `fs_info_mfprice` | 最小变动价位 |  |
| `fs_info_name` | 期货简称 |  |
| `fs_info_punit` | 报价单位 |  |
| `fs_info_sccode` | 标准合约代码 |  |
| `fs_info_thours` | 交易时间说明 |  |
| `fs_info_tunit` | 交易单位 |  |
| `fs_info_windcode` | Wind代码 |  |
| `fs_mq_amount` | 月成交额 |  |
| `fs_mq_avgamount` | 月日均成交额 |  |
| `fs_mq_avgaoi` | 月日均持仓量 |  |
| `fs_mq_avgprice` | 月成交均价 |  |
| `fs_mq_avgvolume` | 月日均成交量 |  |
| `fs_mq_change` | 月涨跌 |  |
| `fs_mq_change_settlement` | 月涨跌（结算价） |  |
| `fs_mq_close` | 月收盘价 |  |
| `fs_mq_high` | 月最高价 |  |
| `fs_mq_high_date` | 月最高价日 |  |
| `fs_mq_highclose` | 月最高收盘价 |  |
| `fs_mq_highclose_date` | 月最高收盘价日 |  |
| `fs_mq_highsettle` | 月最高结算价 |  |
| `fs_mq_highswing_date` | 月最高结算价日 |  |
| `fs_mq_low` | 月最低价 |  |
| `fs_mq_low_date` | 月最低价日 |  |
| `fs_mq_lowclose` | 月最低收盘价 |  |
| `fs_mq_lowclose_date` | 月最低收盘价日 |  |
| `fs_mq_lowsettle` | 月最低结算价 |  |
| `fs_mq_lowswing_date` | 月最低结算价日 |  |
| `fs_mq_oi` | 月持仓量 |  |
| `fs_mq_oichange` | 月持仓变化 |  |
| `fs_mq_open` | 月开盘价 |  |
| `fs_mq_pctchange` | 月涨跌幅 |  |
| `fs_mq_pctchange_settlement` | 月涨跌幅（结算价） |  |
| `fs_mq_preclose` | 月前收盘价 |  |
| `fs_mq_presettle` | 月前结算价 |  |
| `fs_mq_settle` | 月结算价 |  |
| `fs_mq_swing` | 月振幅 |  |
| `fs_mq_volume` | 月成交量 |  |
| `fs_oi_lname` | 持买单量进榜会员名称 |  |
| `fs_oi_loi` | 持买单量 |  |
| `fs_oi_sname` | 持卖单量进榜会员名称 |  |
| `fs_oi_soi` | 持卖单量 |  |
| `fs_oi_vname` | 成交量进榜会员名称 |  |
| `fs_oi_volume` | 成交量 |  |
| `fs_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `fs_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `fs_pq_avgaoi` | 区间日均持仓量 | BEGINDATE、EndDate |
| `fs_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `fs_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `fs_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `fs_pq_change_settlement` | 区间涨跌（结算价） | BEGINDATE、EndDate |
| `fs_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `fs_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `fs_pq_high_date` | 区间最高价日 | BEGINDATE、EndDate |
| `fs_pq_highclose` | 区间最高收盘价 | BEGINDATE、EndDate |
| `fs_pq_highclose_date` | 区间最高收盘价日 | BEGINDATE、EndDate |
| `fs_pq_highsettle` | 区间最高结算价 | BEGINDATE、EndDate |
| `fs_pq_highswing_date` | 区间最高结算价日 | BEGINDATE、EndDate |
| `fs_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `fs_pq_low_date` | 区间最低价日 | BEGINDATE、EndDate |
| `fs_pq_lowclose` | 区间最低收盘价 | BEGINDATE、EndDate |
| `fs_pq_lowclose_date` | 区间最低收盘价日 | BEGINDATE、EndDate |
| `fs_pq_lowsettle` | 区间最低结算价 | BEGINDATE、EndDate |
| `fs_pq_lowswing_date` | 区间最低结算价日 | BEGINDATE、EndDate |
| `fs_pq_oi` | 区间持仓量 | BEGINDATE、EndDate |
| `fs_pq_oichange` | 区间持仓变化 | BEGINDATE、EndDate |
| `fs_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `fs_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `fs_pq_pctchange_settlement` | 区间涨跌幅（结算价） | BEGINDATE、EndDate |
| `fs_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `fs_pq_presettle` | 区间前结算价 | BEGINDATE、EndDate |
| `fs_pq_settle` | 区间结算价 | BEGINDATE、EndDate |
| `fs_pq_swing` | 区间振幅 | BEGINDATE、EndDate |
| `fs_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `fs_qq_amount` | 季成交额 |  |
| `fs_qq_avgamount` | 季日均成交额 |  |
| `fs_qq_avgaoi` | 季日均持仓量 |  |
| `fs_qq_avgprice` | 季成交均价 |  |
| `fs_qq_avgvolume` | 季日均成交量 |  |
| `fs_qq_change` | 季涨跌 |  |
| `fs_qq_change_settlement` | 季涨跌（结算价） |  |
| `fs_qq_close` | 季收盘价 |  |
| `fs_qq_high` | 季最高价 |  |
| `fs_qq_high_date` | 季最高价日 |  |
| `fs_qq_highclose` | 季最高收盘价 |  |
| `fs_qq_highclose_date` | 季最高收盘价日 |  |
| `fs_qq_highsettle` | 季最高结算价 |  |
| `fs_qq_highswing_date` | 季最高结算价日 |  |
| `fs_qq_low` | 季最低价 |  |
| `fs_qq_low_date` | 季最低价日 |  |
| `fs_qq_lowclose` | 季最低收盘价 |  |
| `fs_qq_lowclose_date` | 季最低收盘价日 |  |
| `fs_qq_lowsettle` | 季最低结算价 |  |
| `fs_qq_lowswing_date` | 季最低结算价日 |  |
| `fs_qq_oi` | 季持仓量 |  |
| `fs_qq_oichange` | 季持仓变化 |  |
| `fs_qq_open` | 季开盘价 |  |
| `fs_qq_pctchange` | 季涨跌幅 |  |
| `fs_qq_pctchange_settlement` | 季涨跌幅（结算价） |  |
| `fs_qq_preclose` | 季前收盘价 |  |
| `fs_qq_presettle` | 季前结算价 |  |
| `fs_qq_settle` | 季结算价 |  |
| `fs_qq_swing` | 季振幅 |  |
| `fs_qq_volume` | 季成交量 |  |
| `fs_st_efforecast` | 有效预报 | TRADEDATE |
| `fs_st_stock` | 注册仓单数量 |  |
| `fs_wq_amount` | 周成交额 |  |
| `fs_wq_avgamount` | 周日均成交额 |  |
| `fs_wq_avgaoi` | 周日均持仓量 |  |
| `fs_wq_avgprice` | 周成交均价 |  |
| `fs_wq_avgvolume` | 周日均成交量 |  |
| `fs_wq_change` | 周涨跌 |  |
| `fs_wq_change_settlement` | 周涨跌（结算价） |  |
| `fs_wq_close` | 周收盘价 |  |
| `fs_wq_high` | 周最高价 |  |
| `fs_wq_high_date` | 周最高价日 |  |
| `fs_wq_highclose` | 周最高收盘价 |  |
| `fs_wq_highclose_date` | 周最高收盘价日 |  |
| `fs_wq_highsettle` | 周最高结算价 |  |
| `fs_wq_highswing_date` | 周最高结算价日 |  |
| `fs_wq_low` | 周最低价 |  |
| `fs_wq_low_date` | 周最低价日 |  |
| `fs_wq_lowclose` | 周最低收盘价 |  |
| `fs_wq_lowclose_date` | 周最低收盘价日 |  |
| `fs_wq_lowsettle` | 周最低结算价 |  |
| `fs_wq_lowswing_date` | 周最低结算价日 |  |
| `fs_wq_oi` | 周持仓量 |  |
| `fs_wq_oichange` | 周持仓变化 |  |
| `fs_wq_open` | 周开盘价 |  |
| `fs_wq_pctchange` | 周涨跌幅 |  |
| `fs_wq_pctchange_settlement` | 周涨跌幅（结算价） |  |
| `fs_wq_preclose` | 周前收盘价 |  |
| `fs_wq_presettle` | 周前结算价 |  |
| `fs_wq_settle` | 周结算价 |  |
| `fs_wq_swing` | 周振幅 |  |
| `fs_wq_volume` | 周成交量 |  |
| `fs_yq_amount` | 年成交额 |  |
| `fs_yq_avgamount` | 年日均成交额 |  |
| `fs_yq_avgaoi` | 年日均持仓量 |  |
| `fs_yq_avgprice` | 年成交均价 |  |
| `fs_yq_avgvolume` | 年日均成交量 |  |
| `fs_yq_change` | 年涨跌 |  |
| `fs_yq_change_settlement` | 年涨跌（结算价） |  |
| `fs_yq_close` | 年收盘价 |  |
| `fs_yq_high` | 年最高价 |  |
| `fs_yq_high_date` | 年最高价日 |  |
| `fs_yq_highclose` | 年最高收盘价 |  |
| `fs_yq_highclose_date` | 年最高收盘价日 |  |
| `fs_yq_highsettle` | 年最高结算价 |  |
| `fs_yq_highswing_date` | 年最高结算价日 |  |
| `fs_yq_low` | 年最低价 |  |
| `fs_yq_low_date` | 年最低价日 |  |
| `fs_yq_lowclose` | 年最低收盘价 |  |
| `fs_yq_lowclose_date` | 年最低收盘价日 |  |
| `fs_yq_lowsettle` | 年最低结算价 |  |
| `fs_yq_lowswing_date` | 年最低结算价日 |  |
| `fs_yq_oi` | 年持仓量 |  |
| `fs_yq_oichange` | 年持仓变化 |  |
| `fs_yq_open` | 年开盘价 |  |
| `fs_yq_pctchange` | 年涨跌幅 |  |
| `fs_yq_pctchange_settlement` | 年涨跌幅（结算价） |  |
| `fs_yq_preclose` | 年前收盘价 |  |
| `fs_yq_presettle` | 年前结算价 |  |
| `fs_yq_settle` | 年结算价 |  |
| `fs_yq_swing` | 年振幅 |  |
| `fs_yq_volume` | 年成交量 |  |

<a id="分类-指数"></a>

## 指数（90 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `i_anal_basepointvalue` | 平均基点价值 | TRADEDATE |
| `i_anal_basis` | 基差(股指期货) | TRADEDATE |
| `i_anal_basisannualyield` | 基差年化收益率(股指期货) | TRADEDATE |
| `i_anal_basispercent` | 基差率(股指期货) | TRADEDATE |
| `i_anal_capconvexity` | 平均市值法凸性 | TRADEDATE |
| `i_anal_capduration` | 平均市值法久期 | TRADEDATE |
| `i_anal_capytm` | 平均市值法到期收益率 | TRADEDATE |
| `i_anal_cashflowconvexity` | 平均现金流法凸性 | TRADEDATE |
| `i_anal_cashflowduration` | 平均现金流法久期 | TRADEDATE |
| `i_anal_cashflowytm` | 平均现金流法到期收益率 | TRADEDATE |
| `i_anal_ipratio` | 平均派息率 | TRADEDATE |
| `i_anal_period` | 平均待偿期 | TRADEDATE |
| `i_div_compindex` | 成份分红对指数影响 | TRADEDATE |
| `i_dq_amount` | 成交额 |  |
| `i_dq_amount_cnbd` | 现券结算量(中债) | TRADEDATE |
| `i_dq_avgprice` | 成交均价 |  |
| `i_dq_change` | 涨跌 |  |
| `i_dq_change_cnbd` | 涨跌(中债) | TRADEDATE |
| `i_dq_close` | 收盘价 |  |
| `i_dq_close_cnbd` | 指数值(中债) | TRADEDATE |
| `i_dq_high` | 最高价 |  |
| `i_dq_low` | 最低价 |  |
| `i_dq_oi` | 持仓量(商品指数) | TRADEDATE |
| `i_dq_open` | 开盘价 |  |
| `i_dq_pctchange` | 涨跌幅 |  |
| `i_dq_pctchange_cnbd` | 涨跌幅(中债) | TRADEDATE |
| `i_dq_preclose` | 前收盘价 |  |
| `i_dq_turn` | 换手率 |  |
| `i_dq_volume` | 成交量 |  |
| `i_info_basedate` | 基期 |  |
| `i_info_basevalue` | 基点 |  |
| `i_info_firstdayofconstituents` | 最早成份日期 |  |
| `i_info_fullyieldindex` | 全收益指数代码 |  |
| `i_info_launchdate` | 发布日期 |  |
| `i_info_majorindexcode` | 主指数代码 |  |
| `i_info_methodology` | 加权方式 |  |
| `i_info_netyieldindex` | 净收益指数代码 |  |
| `i_info_numberofconstituents` | 成份个数 |  |
| `i_info_numberofconstituents2` | 成份个数(支持历史) | TRADEDATE |
| `i_info_officialstyle` | 指数风格 |  |
| `i_info_returntype` | 收益处理方式 |  |
| `i_info_subindexcode` | 副指数代码 |  |
| `i_info_superiorcode` | 上级行业指数代码 | TYPE |
| `i_info_trackedbyfunds` | 跟踪标的基金代码 | TRADEDATE |
| `i_info_trackedbyfundsnum` | 跟踪标的基金数量 | TRADEDATE |
| `i_info_windtype` | 指数分类(Wind) |  |
| `i_pq_amount` | 区间成交额 | BEGINDATE、EndDate |
| `i_pq_avgamount` | 区间日均成交额 | BEGINDATE、EndDate |
| `i_pq_avgprice` | 区间成交均价 | BEGINDATE、EndDate |
| `i_pq_avgturn` | 区间日均换手率 | BEGINDATE、EndDate |
| `i_pq_avgvolume` | 区间日均成交量 | BEGINDATE、EndDate |
| `i_pq_change` | 区间涨跌 | BEGINDATE、EndDate |
| `i_pq_close` | 区间收盘价 | BEGINDATE、EndDate |
| `i_pq_high` | 区间最高价 | BEGINDATE、EndDate |
| `i_pq_low` | 区间最低价 | BEGINDATE、EndDate |
| `i_pq_open` | 区间开盘价 | BEGINDATE、EndDate |
| `i_pq_pctchange` | 区间涨跌幅 | BEGINDATE、EndDate |
| `i_pq_preclose` | 区间前收盘价 | BEGINDATE、EndDate |
| `i_pq_tradedays` | 区间交易天数 | BEGINDATE、EndDate |
| `i_pq_turn` | 区间换手率 | BEGINDATE、EndDate |
| `i_pq_volume` | 区间成交量 | BEGINDATE、EndDate |
| `i_risk_returnyearly` | 指数年化收益率 | StartDate、EndDate、CalcMethod |
| `i_risk_returnyearly_naturalday` | 区间收益率(自然日年化) | StartDate、EndDate |
| `i_tech_downnum` | 指数成份下跌数量 | TRADEDATE |
| `i_tech_limitdownnum` | 指数成份跌停数量 | TRADEDATE |
| `i_tech_limitupnum` | 指数成份涨停数量 | TRADEDATE |
| `i_tech_upnum` | 指数成份上涨数量 | TRADEDATE |
| `i_techanal_stagehigh_num` | 成份创阶段新高数量 | TRADEDATE、NDAYS |
| `i_techanal_stagelow_num` | 成份创阶段新低数量 | TRADEDATE、NDAYS |
| `i_val_dividend_percentile` | 股息率分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_dividendyield2_issuer` | 发布方股息率(近12个月) | TRADEDATE |
| `i_val_dividendyield2_issuer2` | 发布方股息率(近12个月,调整) | TRADEDATE |
| `i_val_mv` | 指数总市值 | TRADEDATE |
| `i_val_pb_lf_issuer` | 发布方市净率PB(LF) | TRADEDATE |
| `i_val_pb_median` | 市净率PB(LF,中位数) | TRADEDATE |
| `i_val_pb_mrqwgt` | 市净率PB(MRQ,加权) | TRADEDATE |
| `i_val_pb_percentile` | 市净率分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_pcf_ocfttmwgt` | 市现率PCF(经营现金流TTM,加权) | TRADEDATE |
| `i_val_pcf_percentile` | 市现率分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_pe_median` | 市盈率PE(TTM,中位数) | TRADEDATE |
| `i_val_pe_nonnegative` | 市盈率PE(TTM,剔除负值) | TRADEDATE |
| `i_val_pe_nonnegative_wgt` | 市盈率PE(TTM,剔除负值,加权) | TRADEDATE |
| `i_val_pe_percentile` | 市盈率分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_pe_ttm_issuer` | 发布方市盈率PE(TTM) | TRADEDATE |
| `i_val_pe_ttm_issuer2` | 发布方市盈率PE(TTM,调整) | TRADEDATE |
| `i_val_pe_ttmwgt` | 市盈率PE(TTM,加权) | TRADEDATE |
| `i_val_pe_wgt` | 市盈率PE(LYR,加权) | TRADEDATE |
| `i_val_penonngtv_percentile` | 市盈率PE(TTM,剔除负值)分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_ps_percentile` | 市销率分位数 | TRADEDATE、StartDate、EndDate |
| `i_val_ps_ttmwgt` | 市销率PS(TTM,加权) | TRADEDATE |

<a id="分类-期货"></a>

## 期货（43 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `fut_anal_basis_stkidx` | 基差(股指期货) | TRADEDATE |
| `fut_anal_basisannualyield_stkidx` | 基差年化收益率(股指期货) | TRADEDATE |
| `fut_anal_basispercent_stkidx` | 基差率(股指期货) | TRADEDATE |
| `fut_anyield_roll` | 期货合约展期年化收益率 | TRADEDATE |
| `fut_dq_change_close` | 涨跌(收盘价) | TRADEDATE |
| `fut_dq_close_night` | 夜盘收盘价(支持复权) | TRADEDATE |
| `fut_dq_oiamount` | 持仓额变化 | TRADEDATE |
| `fut_dq_price_commodity` | 商品期货特殊时点价 | TRADEDATE、Point |
| `fut_dq_price_premetals` | 贵金属现货特殊时点价 | TRADEDATE |
| `fut_dq_settle` | 结算价(支持复权) | TRADEDATE |
| `fut_info_capitalflow` | 资金流向 | TRADEDATE |
| `fut_info_concept` | 所属概念板块 | TRADEDATE |
| `fut_info_excode` | 月合约代码(交易所) | TRADEDATE |
| `fut_info_fndate` | 第一通知日 | TRADEDATE |
| `fut_info_hedgelong_margin` | 期货套保多头保证金(支持历史) | TRADEDATE |
| `fut_info_hedgeshort_margin` | 期货套保空头保证金(支持历史) | TRADEDATE |
| `fut_info_initargin` | 期货合约初始保证金 | TRADEDATE |
| `fut_info_mainmargin` | 期货合约维持保证金 | TRADEDATE |
| `fut_info_maxoq` | 期货合约最大下单量 | TRADEDATE、TYPE |
| `fut_info_minoq` | 期货合约最小开仓量下单量 | TRADEDATE、TYPE |
| `fut_info_oplimit_client` | 期货公司客户期货开仓限额 | TRADEDATE |
| `fut_info_oplimit_ftcom` | 期货公司会员期货开仓限额 | TRADEDATE |
| `fut_info_oplimit_nonft` | 非期货公司会员期货开仓限额 | TRADEDATE |
| `fut_info_sddate` | 开始交割日(支持历史) | TRADEDATE |
| `fut_info_sunkcapital` | 沉淀资金 | TRADEDATE |
| `fut_limit_cust` | 客户持仓限额 | TRADEDATE |
| `fut_limit_futu` | 期货公司会员持仓限额 | TRADEDATE |
| `fut_limit_indi` | 自然人客户持仓限额 | TRADEDATE |
| `fut_limit_nonfu` | 非期货公司会员持仓限额 | TRADEDATE |
| `fut_oi_ncoi` | 净持仓(合约) | TRADEDATE、TopN |
| `fut_oi_unpribu` | ICE棉花未点价买单 | TRADEDATE |
| `fut_oi_unprise` | ICE棉花未点价卖单 | TRADEDATE |
| `fut_pq_highsettle_date` | 区间最高结算价日(支持复权) | StartDate、DATE |
| `fut_pq_lowsettle_date` | 区间最低结算价日(支持复权) | StartDate、DATE |
| `fut_pq_newh` | 创N日新高 | SDATE、DATE、AdjustType、PriceType |
| `fut_pq_newl` | 创N日新低 | SDATE、DATE、AdjustType、PriceType |
| `fut_pq_pctchange_close` | 区间涨跌幅(收盘价) | SDATE、DATE |
| `fut_ra_coposiware` | 虚实盘比(合约) | TRADEDATE |
| `fut_ra_vaposiware` | 虚实盘比(品种) | TRADEDATE |
| `fut_rating_numofbearish` | 期货品种看空研报数量 | TRADEDATE |
| `fut_rating_numofbullish` | 期货品种看多研报数量 | TRADEDATE |
| `fut_rating_numofneutral` | 期货品种中性研报数量 | TRADEDATE |
| `fut_windrating_report` | 期货品种观点Wind评分 | TRADEDATE |

<a id="分类-财务分析"></a>

## 财务分析（42 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `fa_apturn` | 应付账款周转率 | REPORTDATE |
| `fa_apturndays` | 应付账款周转天数 | REPORTDATE |
| `fa_bookvaluetodebt` | 股东权益合计（含少数）／负债总计 | REPORTDATE |
| `fa_cashtocurrentdebt` | 现金比率 | REPORTDATE |
| `fa_currentdebttoequity` | 流动负债权益比率 | REPORTDATE |
| `fa_debttotangibleequity` | 有形净值债务率 | REPORTDATE |
| `fa_deducteddebttoassets` | 剔除预收账款后的资产负债率 | REPORTDATE |
| `fa_ebitdatointerest` | EBITDA/利息费用 | REPORTDATE |
| `fa_ebittoassets` | 息税前利润／总资产 | REPORTDATE |
| `fa_equitytodebt` | 当日总市值／负债总计 | REPORTDATE |
| `fa_fcftocf` | 筹资活动产生的现金流量净额占比 | REPORTDATE |
| `fa_icftocf` | 投资活动产生的现金流量净额占比 | REPORTDATE |
| `fa_impairtoop` | 资产减值损失/营业利润 | REPORTDATE |
| `fa_longcapitaltoinvestment` | 长期资产适合率 | REPORTDATE |
| `fa_longdebttodebt` | 长期负债占比 | REPORTDATE |
| `fa_longdebttoequity` | 非流动负债权益比率 | REPORTDATE |
| `fa_longdebttolongcaptial` | 长期资本负债率 | REPORTDATE |
| `fa_maintenance` | 资本项目规模维持率 | REPORTDATE |
| `fa_ncatoequity` | 资本固定化比率 | REPORTDATE |
| `fa_netturndays` | 净营业周期 | REPORTDATE |
| `fa_non_currentassetsturn` | 非流动资产周转率 | REPORTDATE |
| `fa_nptocostexpense` | 成本费用利润率 | REPORTDATE |
| `fa_ocficftocurrentdebt` | 非筹资性现金净流量与流动负债的比率 | REPORTDATE |
| `fa_ocficftodebt` | 非筹资性现金净流量与负债总额的比率 | REPORTDATE |
| `fa_ocftoassets` | 全部资产现金回收率 | REPORTDATE |
| `fa_ocftocf` | 经营活动产生的现金流量净额占比 | REPORTDATE |
| `fa_ocftodividend` | 现金股利保障倍数 | REPORTDATE |
| `fa_ocftointerest` | 现金流量利息保障倍数 | REPORTDATE |
| `fa_ocftoinveststockdividend` | 现金满足投资比率 | REPORTDATE |
| `fa_ocftolongdebt` | 经营活动产生的现金流量净额/非流动负债 | REPORTDATE |
| `fa_ocftoop` | 现金营运指数 | REPORTDATE |
| `fa_ocftoquickdebt` | 现金到期债务比 | REPORTDATE |
| `fa_operatecaptialturn` | 营运资本周转率 | REPORTDATE |
| `fa_optoebt` | 主营业务比率 | REPORTDATE |
| `fa_retainedearningstoassets` | 留存收益／总资产 | REPORTDATE |
| `fa_revenuetoassets` | 营业收入／总资产 | REPORTDATE |
| `fa_roic_ttm` | 投入资本回报率(TTM) | REPORTDATE |
| `fa_rop` | 人力投入回报率（ROP) | REPORTDATE |
| `fa_score` | Z值 | REPORTDATE |
| `fa_workingcapitaltoassets` | 营运资本／总资产 | REPORTDATE |
| `fa_yoy_cash` | 货币资金增长率 | REPORTDATE |
| `fa_yoy_fixedassets` | 固定资产投资扩张率 | REPORTDATE |

<a id="分类-历史行情"></a>

## 历史行情（17 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `his_avgprice` | 成交均价_期货历史同月 | DATE |
| `his_change` | 涨跌_期货历史同月 | DATE |
| `his_change_settlement` | 涨跌(结算价)_期货历史同月 | DATE |
| `his_close` | 收盘价_期货历史同月 | DATE |
| `his_close_night` | 收盘价(夜盘)_期货历史同月 | TRADEDATE |
| `his_high` | 最高价_期货历史同月 | DATE |
| `his_low` | 最低价_期货历史同月 | DATE |
| `his_oi` | 持仓量_期货历史同月 | DATE |
| `his_oichange` | 持仓变化_期货历史同月 | DATE |
| `his_open` | 开盘价_期货历史同月 | DATE |
| `his_pctchange` | 涨跌幅_期货历史同月 | DATE |
| `his_pctchange_settlement` | 涨跌幅(结算价)_期货历史同月 | DATE |
| `his_presettle` | 前结算价_期货历史同月 | DATE |
| `his_settle` | 结算价_期货历史同月 | DATE |
| `his_swing` | 振幅_期货历史同月 | DATE |
| `his_turnover` | 成交额_期货历史同月 | TRADEDATE |
| `his_volume` | 成交量_期货历史同月 | DATE |

<a id="分类-融资融券"></a>

## 融资融券（8 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `mrg_bal_int_avg` | 区间融资融券余额均值 |  |
| `mrg_long_amt_int` | 区间融资买入额 |  |
| `mrg_long_bal_int_avg` | 区间融资余额均值 |  |
| `mrg_long_repay_int` | 区间融资偿还额 |  |
| `mrg_short_bal_int_avg` | 区间融券余额均值 |  |
| `mrg_short_vol_bal_int_avg` | 区间融券余量均值 |  |
| `mrg_short_vol_int` | 区间融券卖出量 |  |
| `mrg_short_vol_repay_int` | 区间融券偿还量 |  |

<a id="分类-单季财务"></a>

## 单季财务（6 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `qfa_fcftocf` | 单季度.筹资活动产生的现金流量净额占比 | REPORTDATE |
| `qfa_icftocf` | 单季度.投资活动产生的现金流量净额占比 | REPORTDATE |
| `qfa_impairtoop` | 单季度.资产减值损失/营业利润 | REPORTDATE |
| `qfa_nptocostexpense` | 单季度.成本费用利润率 | REPORTDATE |
| `qfa_ocftocf` | 单季度.经营活动产生的现金流量净额占比 | REPORTDATE |
| `qfa_optoebt` | 单季度.主营业务比率 | REPORTDATE |

<a id="分类-技术指标-其他"></a>

## 技术指标/其他（148 个字段）

| 字段代码 | 中文名 | 参数 |
|---|---|---|
| `accrint_dayend_cnbd` | 日终应计利息 | TRADEDATE |
| `adtm` | ADTM动态买卖气指标 |  |
| `advancecredit_desc` | 信托项目关联企业名称 |  |
| `amaccode_windcode` | 基金业协会编码提取Wind代码 | SECNAME |
| `anticipateyield_desc` | 信用增级情况 |  |
| `arbr` | ARBR人气意愿指标 |  |
| `atr` | ATR真实波幅 |  |
| `bbi` | BBI多空指数 |  |
| `bbiboll` | BBIBOLL多空布林线 |  |
| `bias` | BIAS乖离率 |  |
| `boll` | BOLL布林带 |  |
| `bondsettle_average` | 平均结算价格 |  |
| `bondsettle_avgvolume` | 平均每笔结算金额 |  |
| `bondsettle_change` | 结算价格涨跌幅 |  |
| `bondsettle_close` | 收盘结算价格 |  |
| `bondsettle_high` | 最高结算价格 |  |
| `bondsettle_low` | 最低结算价格 |  |
| `bondsettle_open` | 开盘结算价格 |  |
| `bondsettle_transaction` | 结算笔数 |  |
| `bondsettle_ytm` | 平均到期收益率 |  |
| `bookrunner` | 簿记管理人 |  |
| `bottom` | 筑底指标 |  |
| `bwmpcode_windcode` | 理财产品登记编码提取Wind代码 | WMP_Record_Code |
| `cci` | CCI顺势指标 |  |
| `cdp` | CDP逆势操作 |  |
| `cnvxty_cnbd` | 加权平均结算价凸性 | TRADEDATE |
| `code_windcode` | 交易代码转Wind代码 | stock、ExchangeType |
| `collateralcode` | 质押券代码 |  |
| `collateralname` | 质押券简称 |  |
| `corporatename_enterprisecode` | 公司名称提取发债企业代码 | CompanyFullname |
| `corporatename_windbondcode` | 公司名称提取Wind债券代码 | company |
| `corporatename_windbondcode_1st` | 公司名称提取Wind债券代码(首只债券) | CompanyName、BondType |
| `cr` | CR能量指标 |  |
| `cusip_windcode` | CUSIP对应Wind代码 | CUSIP、ExchangeType |
| `dbcd` | DBCD异同离差乖离率 |  |
| `ddi` | DDI方向标准离差指数 |  |
| `dirty_dayend_cnbd` | 日终估价全价 | TRADEDATE |
| `dma` | DMA平均线差 |  |
| `dmi` | DMI趋向指标 |  |
| `dmi_2` | DMI趋向标准 | TRADEDATE |
| `dpo` | DPO区间震荡线 |  |
| `env` | ENV指标 |  |
| `expma` | EXPMA指数平均数 |  |
| `firstradeday_s` | 最早交易日期 |  |
| `fullname_windcode` | 证券全称提取Wind代码 | FullName |
| `fund_navcur` | 单位净值币种 |  |
| `fund_stockvalue_industry` | 股票投资市值(分行业) | REPORTDATE |
| `fund_stockvalue_industrytoasset` | 分行业市值占基金资产总值比 | REPORTDATE |
| `fund_stockvalue_industrytonav` | 分行业市值占基金资产净值比 | REPORTDATE |
| `fund_subshareproportion` | 分级份额占比 |  |
| `fundnetasset_total` | 资产净值(合计) | REPORTDATE |
| `fundshare_total` | 基金份额(合计) |  |
| `getvaliddate_new` | 取正确格式的日期new(不进行当前日期的填充直接发送空值) | DatePara、ADefDate |
| `holder_pctbyhf` | 阳光私募持股比例 |  |
| `holder_totalbyhf` | 阳光私募持股数量 |  |
| `hq_close` | 收盘价(不前推) | TRADEDATE、AdjustType |
| `hq_close2` | 收盘价(外汇) | TRADEDATE、CloseTime |
| `hq_close_n` | 收盘价(不前推,停牌返回空) | TRADEDATE、AdjustType |
| `hq_high` | 最高价(不前推) | TRADEDATE、AdjustType |
| `hq_high_n` | 最高价(不前推,停牌返回空) | TRADEDATE、AdjustType |
| `hq_low` | 最低价(不前推) | TRADEDATE、AdjustType |
| `hq_low_n` | 最低价(不前推,停牌返回空) | TRADEDATE、AdjustType |
| `hq_nav_unit` | 单位净值(不前推) | TRADEDATE |
| `hq_open` | 开盘价(不前推) | TRADEDATE、AdjustType |
| `hq_open_n` | 开盘价(不前推,停牌返回空) | TRADEDATE、AdjustType |
| `idxcnxt_cnbd` | 加权平均结算价利率凸性 | TRADEDATE |
| `idxdura_cnbd` | 加权平均结算价利率久期 | TRADEDATE |
| `isin_windcode` | ISIN提取Wind代码 | ISINCODE |
| `isin_windcode_1` | ISIN提取Wind代码(可选交易所) | ISINCODE、ExchangeType |
| `issuercode_windcode` | 发行机构自编代码提取Wind代码 | Issuer_Code |
| `issuerrating` | 发行时主体评级 |  |
| `kdj` | KDJ随机指标 |  |
| `kduration_nextcash` | 下一付息日久期 | TRADEDATE |
| `lastradeday_s` | 最近交易日期 |  |
| `lwr` | LWR威廉指标 |  |
| `ma` | MA简单移动平均 |  |
| `macd` | MACD指数平滑异同平均 |  |
| `mass` | MASS梅丝指标 |  |
| `mfi` | MFI资金流向指标 |  |
| `mi` | MI动量指标 |  |
| `micd` | MICD异同离差动力指数 |  |
| `mike` | MIKE麦克指标 |  |
| `modidura_cnbd` | 加权平均结算价修正久期 | TRADEDATE |
| `mtm` | MTM动力指标 |  |
| `obv` | OBV能量潮 |  |
| `paymentdate` | 年付息日 |  |
| `pb_mrq` | 市净率PB(MRQ) | TRADEDATE |
| `pb_o` | 市净率(PB) |  |
| `pcf_ncf_o` | 市现率(PCF,现金净流量) |  |
| `pcf_ocf_o` | 市现率(PCF,经营现金流) |  |
| `pe_o` | 市盈率(PE) |  |
| `prdstrong` | 阶段强势指标 |  |
| `prdweak` | 阶段弱势指标 |  |
| `priceosc` | PRICEOSC价格振荡指标 |  |
| `prt_stockvalue_industrytostock` | 分行业市值占股票投资市值比 | REPORTDATE |
| `ps_o` | 市销率(PS) |  |
| `psy` | PSY心理指标 |  |
| `pvt` | PVT量价趋势指标 |  |
| `pwmi` | 大盘同步指标 |  |
| `rccd` | RCCD异同离差变化率指数 |  |
| `risk_avgreturn` | 平均收益率 |  |
| `risk_beta` | 波Beta | StartDate、EndDate、Period、TYPE、INDEX |
| `risk_stdev` | 波动率 |  |
| `roc` | ROC变动速率 |  |
| `rsi` | RSI相对强弱指标 |  |
| `sar` | SAR抛物转向 |  |
| `sec_fa_apturndays_avg_chn` | 应付账款周转天数(算术平均) | REPORTDATE |
| `sec_fa_apturndays_avg_glb` | 应付账款周转天数(算术平均) | REPORTDATE |
| `sec_fa_apturndays_overall_chn` | 应付账款周转天数(整体法) | REPORTDATE |
| `sec_fa_apturndays_overall_glb` | 应付账款周转天数(整体法) | REPORTDATE |
| `selfwrittencode_windcode` | Wind自编代码转Wind代码 |  |
| `share_freesharesmv` | 自由流通市值 |  |
| `si` | SI摆动指标 |  |
| `slowkd` | SLOWKD慢速KD |  |
| `sobv` | SOBV能量潮 |  |
| `sprcnxt_cnbd` | 加权平均结算价利差凸性 | TRADEDATE |
| `sprdura_cnbd` | 加权平均结算价利差久期 | TRADEDATE |
| `spreadyield_cnbd` | 点差收益率 | TRADEDATE |
| `srdm` | SRDM动向速度比率 |  |
| `srmi` | SRMI MI修正指标 |  |
| `std` | STD标准差 |  |
| `stmnote_ar_cat` | 应收账款-坏账准备(按性质) | REPORTDATE、Category |
| `stmnote_finexp_13` | 利息资本化金额 | DATE |
| `tapi` | TAPI加权指数成交值 |  |
| `td` | 取前推的最近交易日 | DEALDATE |
| `to_tradecode1` | 证券简称提取交易代码 | SECNAME、ExchangeType |
| `to_windcode1` | 证券简称提取Wind代码(可选交易所) | SECNAME、ExchangeType |
| `to_windcode_index` | 指数简称提取指数的Wind代码 | SECNAME |
| `trix` | TRIX三重指数平滑平均 |  |
| `trust_investfield` | 信托投资领域 |  |
| `trust_relatedfirm` | 预期收益率说明 |  |
| `trust_sourcetype` | 信托产品类别 |  |
| `trust_type` | 信托类别 |  |
| `vhf` | VHF纵横指标 |  |
| `vma` | VMA量简单移动平均 |  |
| `vmacd` | VMACD量指数平滑异同平均 |  |
| `vobp_cnbd` | 加权平均结算价基点价值 | TRADEDATE |
| `volati` | VOLATI佳庆波动率 |  |
| `volumeratio` | 量比 |  |
| `vosc` | VOSC成交量震荡 |  |
| `vr` | VR成交量比率 |  |
| `vroc` | VROC量变动速率 |  |
| `vrsi` | VRSI量相对强弱 |  |
| `vstd` | VSTD成交量标准差 |  |
| `wad` | WAD威廉聚散指标 |  |
| `wr` | WR威廉指标 |  |
| `wvad` | WVAD威廉变异离散量 |  |
| `yccode` | 默认收益率曲线代码 |  |
