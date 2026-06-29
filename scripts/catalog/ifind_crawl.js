// iFinD 命令生成器 —— 全量指标树爬虫
// 用法:在【已登录 quantapi.51ifind.com 的普通浏览器】F12 → Console → 粘贴全部 → 回车
// 跑完会自动下载 ifind_catalog.json;同时结果存在 window.__ifindCatalog
// 进度会实时打印。整个过程预计几分钟,期间别关页面。

(async () => {
  const GW = "https://quantapi.51ifind.com/quantapigw";
  const F = (u) =>
    fetch(u, { credentials: "include", headers: { Accept: "application/json" } }).then((r) => r.json());
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // ---- 并发限速器(最多 5 并发,避免触发反爬) ----
  function pool(items, worker, limit = 5) {
    return new Promise((resolve) => {
      const results = [];
      let i = 0, active = 0, done = 0;
      const next = () => {
        while (active < limit && i < items.length) {
          const idx = i++;
          active++;
          Promise.resolve(worker(items[idx], idx))
            .then((r) => (results[idx] = r))
            .catch((e) => (results[idx] = { __err: String(e) }))
            .finally(() => {
              active--; done++;
              if (done === items.length) resolve(results);
              else next();
            });
        }
      };
      if (!items.length) resolve(results);
      else next();
    });
  }

  // ---- 1) 取函数树,收集所有品种 type ----
  let funcTree;
  try {
    funcTree = await F(GW + "/xlsslug_bff/config/get_api_function_tree");
  } catch (e) {
    console.error("函数树获取失败,可能登录态失效:", e);
    return;
  }
  if (funcTree.errorcode && funcTree.errorcode !== 0) {
    console.error("函数树返回错误(登录态可能失效):", funcTree.errmsg || funcTree.errorcode);
    return;
  }

  const typeMap = {};   // type -> {title, isBlock}
  for (const fn of Object.keys(funcTree)) {
    const arr = funcTree[fn];
    if (!Array.isArray(arr)) continue;
    for (const v of arr) {
      if (!v || !v.type) continue;
      if (!typeMap[v.type]) typeMap[v.type] = { title: v.title, isBlock: v.isBlock === "1" };
      else if (v.isBlock === "1") typeMap[v.type].isBlock = true;
    }
  }
  const indexTypes = Object.keys(typeMap).filter((t) => !typeMap[t].isBlock);
  const blockTypes = Object.keys(typeMap).filter((t) => typeMap[t].isBlock);
  console.log("品种(指标树):", indexTypes.join(", "));
  console.log("品种(板块树,暂记录不深爬):", blockTypes.join(", ") || "(无)");

  // ---- 2) 逐品种递归爬 list_by_seq ----
  async function crawlType(type) {
    const nodes = [];
    const seen = new Set();
    let queue = [0];          // 从 seq=0 起
    let depthGuard = 0;
    while (queue.length && depthGuard < 100000) {
      const batch = queue.splice(0, 200);
      const resps = await pool(
        batch,
        async (seq) => {
          if (seen.has(seq)) return null;
          seen.add(seq);
          await sleep(20 + Math.floor(Math.random() * 40));
          return F(`${GW}/data_browser_web/index_tree/list_by_seq?seq=${seq}&type=${type}`);
        },
        5
      );
      const nextQueue = [];
      for (const r of resps) {
        if (!r || r.__err || !r.data || !Array.isArray(r.data)) continue;
        for (const n of r.data) {
          nodes.push({
            type,
            seq: n.seq,
            idxId: n.idxId || "",
            idxName: n.idxName || "",
            idxEnName: n.idxEnName || "",
            idxUnit: n.idxUnit || "",
            idxPath: n.idxPath || "",
            children: n.children,
            dateSequence: n.dateSequence,
            indexType: n.indexType || "",
            paramList: n.paramList && n.paramList.length ? JSON.stringify(n.paramList) : "",
          });
          // 有子节点则继续展开;inline son 也并入
          if (n.children && n.seq != null && !seen.has(n.seq)) nextQueue.push(n.seq);
          if (Array.isArray(n.son)) {
            for (const s of n.son) {
              if (s && s.seq != null && s.children && !seen.has(s.seq)) nextQueue.push(s.seq);
            }
          }
        }
      }
      queue = queue.concat(nextQueue);
      depthGuard++;
      console.log(`  [${type}] 已收集 ${nodes.length} 节点,待展开 ${queue.length}`);
    }
    return nodes;
  }

  const catalog = { _meta: { ts: new Date().toISOString(), types: typeMap }, index: {}, block: {} };
  for (const t of indexTypes) {
    console.log(`▶ 开始爬品种: ${t} (${typeMap[t].title})`);
    try {
      catalog.index[t] = await crawlType(t);
      console.log(`✔ ${t} 完成: ${catalog.index[t].length} 节点`);
    } catch (e) {
      console.error(`�’ ${t} 失败:`, e);
      catalog.index[t] = [];
    }
  }

  // ---- 3) 板块类只取一层根(深爬待定) ----
  for (const t of blockTypes) {
    try {
      const r = await F(
        `${GW}/data_browser_web/block_tree/block_from_config?business=quantApi&func=BasicData&type=${t}`
      );
      catalog.block[t] = r && r.data ? r.data : r;
    } catch (e) {
      catalog.block[t] = { __err: String(e) };
    }
  }

  window.__ifindCatalog = catalog;
  const total = Object.values(catalog.index).reduce((a, b) => a + b.length, 0);
  console.log(`=== 全部完成,指标树节点合计 ${total} ===`);

  // ---- 4) 下载 JSON ----
  const blob = new Blob([JSON.stringify(catalog)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ifind_catalog.json";
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log("已触发下载 ifind_catalog.json(若被浏览器拦截,运行 copy(JSON.stringify(window.__ifindCatalog)) 手动复制)");
})();
