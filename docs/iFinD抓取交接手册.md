# iFinD 全量指标字段抓取 —— 交接手册 / 提示词

> **给本地那台能正常登录 iFinD 的电脑上的 Claude 执行。**
> 远程那台机器的出口 IP（180.154.18.25）被 iFinD 登录服务 `upass.51ifind.com` 拦截了
> （`/login` 端点对该 IP 返回 forbidden 并回显 IP，主站/其他端点正常 → 确认是针对性 IP 拦截），
> 所以 iFinD 网页抓取必须换一台 IP 没被拦的机器做。本机（你现在用的这台）正常登录 iFinD 即可。

---

## 一、目标

拿到同花顺 iFinD **全量指标字段字典**（指标代码 + 中文名 + 单位 + 参数 + 适用范围 / 报表字段），
整理成给客户做产品设计用的 Markdown 手册，和已完成的东方财富版对齐。

**对照参考**：东方财富 EM 已用同一套方法抓完，产出 `docs/catalog/东方财富EM指标字段手册.md`
（18512 字段）。iFinD 要做的是它的同花顺版。

---

## 二、为什么走"网页命令生成器后台接口"这条路（别走弯路）

抓 iFinD 全量字段，已排除的死路（不要再试）：
1. **iFinD Python SDK 无目录函数** —— 所有 THS_* 函数都是取数的，没有"列出全部指标"的枚举接口；
   `THS_DataPool('report'/'indicator', ...)` 报 `params error`，只有 `block` 等已知池能用。
2. **SDK 自带字典文件加密** —— `iFinDAPI/.../etc/datacube/excel.xml`(36MB)、`excel_description.xml`(6MB)
   就是完整指标字典，但同花顺私有加密（头部哈希+乱码），只有它 DLL 能解，无法直接读。
3. **桌面客户端超级命令** —— 测试账号无导出权限。

**唯一可行**：iFinD 数据接口官网 `quantapi.51ifind.com` 登录后的**可视化函数/命令生成界面**，
它和东方财富一样，背后用**明文 JSON 接口**返回指标分类树和明细。登录后用浏览器 devtools
调这些接口递归抓取即可。

---

## 三、给本地 Claude 的执行提示词（直接复制给它）

```
我需要你帮我抓取同花顺 iFinD 数据接口官网的全量指标字段字典，方法和之前抓东方财富一样。

背景：
- 我已在浏览器登录 iFinD 数据接口站 https://quantapi.51ifind.com/ （账号密码登录，本机 IP 未被拦）。
- 这个站登录后有"可视化函数/命令生成"界面，里面的指标树是通过后台 JSON 接口加载的。
- 之前抓东方财富时，对应接口是：分类树 GetIndicatorCategoryInfos、叶子明细
  GetLeafNodeOnIndicatorCategoryInfoBy?id=xxx、专题报表 GetReportNodes。iFinD 的接口名不同，
  需要你用浏览器 devtools 的 network 面板抓出来。

请按这个流程做：
1. 用 chrome-devtools MCP 连到我已登录的浏览器（list_pages 找到 quantapi.51ifind.com 的标签）。
2. 进入它的"命令生成/可视化取数"界面，展开左侧指标品种/分类树。
3. 在 network 面板（list_network_requests，过滤 fetch/xhr）找出加载指标树和指标明细的后台接口
   —— 找返回 JSON、含指标分类或指标代码(类似 EngName/IndicatorName/字段名)的请求。
4. 确认接口的 URL 模式和参数后，用 evaluate_script 在已登录页面里 fetch 这些接口
   （带 credentials:'include'），递归遍历整棵指标树：先拿分类树，再对每个叶子分类拿指标明细。
   分批跑（每批 100-200 个分类），把结果累积到 window.__thsRows，避免单次脚本超时。
5. 落盘不要用浏览器下载（自动化浏览器下载不稳定/会被 Chrome 拦连续下载）。改用本地 HTTP 接收器：
   先在仓库根跑 scripts/catalog/recv.py（监听 127.0.0.1:8799），
   再在浏览器里 fetch('http://127.0.0.1:8799/save', {method:'POST', body: JSON.stringify({name:'ths_css', rows})})
   把数据 POST 回去写成 CSV。（recv.py 已支持 csd/ctr/css，给 iFinD 用新 name 即可，必要时在 recv.py
   的 HEADERS 里加 iFinD 对应表头。）
6. 抓全后，仿照 scripts/catalog/gen_md.py 写一个生成器，把 iFinD 的 CSV 合并成
   docs/catalog/同花顺iFinD指标字段手册.md（结构和东方财富那份一致：品种→分类→指标表，
   每条带 指标代码/中文名/单位/参数/适用范围）。

关键经验（抓东方财富时踩过的坑）：
- 接口靠浏览器已登录的 cookie 鉴权，必须在已登录页面用 evaluate_script 调（credentials:include），
  不能用外部 curl（cookie 是 HttpOnly，且可能有反爬）。
- 指标树可能是懒加载的多层结构：叶子明细接口返回的可能还是子分类（带 isParent 标记），
  Entity!=null（或类似"有指标代码字段"）的才是真正的指标，需要递归展开。
- evaluate_script 里不要用中文变量名（会解析报错），用 ASCII 标识符。
- 抓取量可能很大（iFinD 官网宣传"2000+报表、千万级宏观指标"），先抓基础数据/财务/估值/行情
  这些核心维度验证流程，宏观 EDB（数万条）可先跳过或按领域单独拉。
- 注意 iFinD 单点登录：如果本机有 iFinD SDK 服务在用同一账号，网页登录会和它互相挤。
  抓取时建议先停掉本机 SDK 服务（或用另一个 iFinD 账号登网页）。

先从第 1-3 步开始：连上浏览器，找到指标树的后台接口，把接口 URL 和返回的 JSON 结构样例给我看，
我们确认对了再开始递归抓取。
```

---

## 四、需要随手册一起带过去的文件（本地仓库已有，git pull 即可）

本机改动已提交（commit `b3a34e9`），本地机器在同一仓库 `git pull` 后即有：
- `scripts/catalog/recv.py` —— 本地 HTTP 接收器（浏览器 POST JSON → 写 CSV）。
- `scripts/catalog/gen_md.py` —— CSV → Markdown 生成器（仿它写 iFinD 版）。
- `scripts/catalog/extract_em.py` / `extract_ths.py` —— SDK 程序化榨取示例（参考用）。
- `docs/catalog/东方财富EM指标字段手册.md` —— 成品样例，iFinD 版照此结构产出。

> 若本地机器不是同一个 git 仓库，把 `scripts/catalog/recv.py` 和 `gen_md.py` 两个文件拷过去即可。

---

## 五、recv.py 适配 iFinD（本地 Claude 可能要做的小改）

`recv.py` 的 `HEADERS` 字典目前只有 css/csd/ctr 三个 EM 表头。给 iFinD 用时，
按实际抓到的字段加一行，例如：

```python
HEADERS = {
    # ... 现有 EM 的 ...
    "ths_css": ["品种", "分类", "指标代码", "指标中文名", "单位", "参数", "适用范围"],
    "ths_report": ["品种", "报表名", "报表代码", "字段代码", "字段中文名"],
}
```

POST 时 `name` 用 `ths_css` / `ths_report`，文件会写到 `docs/catalog/em/ths_css_indicators.csv`
（注意 recv.py 默认写到 `docs/catalog/em/`，iFinD 建议改成写 `docs/catalog/ths/`，
改 `OUT` 那一行即可）。

---

## 六、验证 IP 是否还被拦（本地机器先自测）

本地机器开抓前，先确认它的出口 IP 没被 iFinD 登录服务拦：

```bash
# 期望：登录端点不是 401/forbidden（200 或 302 都行），且页面不回显你的 IP
curl -s -o /dev/null -w "login http=%{http_code}\n" \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36" \
  -H "Referer: https://quantapi.51ifind.com/" \
  "https://upass.51ifind.com/login?source=ifind_quantapi"
```

- 若返回 401 → 这台机器 IP 也被拦，换网络/换机器。
- 若返回 200/302 → 可以正常登录，按第三节提示词开干。

---

## 七、产出验收标准

抓完后应得到：
- `docs/catalog/ths/*.csv` —— iFinD 各维度字段 CSV（指标代码/中文名/单位/参数/适用范围）。
- `docs/catalog/同花顺iFinD指标字段手册.md` —— 给客户的手册，结构同东方财富版。
- 最后可做一份 **EM ↔ iFinD 维度对照表**（两家指标体系对应关系），方便客户跨系统设计。

完成后把 CSV + MD 提交一个 commit（如 `feat: iFinD 全量指标字段字典与 Markdown 手册`）。
