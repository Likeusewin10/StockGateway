// iFinD 命令生成器后台接口 —— 结构采样脚本
// 用法:在【已登录 quantapi.51ifind.com 的普通浏览器】里 F12 → Console → 粘贴本文件全部内容 → 回车
// 然后把控制台打印的 TREE / LIST0 / BLOCK 三段复制回给 Claude
(async () => {
  const F = (u) =>
    fetch(u, { credentials: "include", headers: { Accept: "application/json" } }).then((r) => r.json());
  const base = "https://quantapi.51ifind.com/quantapigw";
  const out = {};
  try {
    out.tree = await F(base + "/xlsslug_bff/config/get_api_function_tree");
  } catch (e) {
    out.tree = String(e);
  }
  try {
    out.list0 = await F(base + "/data_browser_web/index_tree/list_by_seq?seq=0&type=stk");
  } catch (e) {
    out.list0 = String(e);
  }
  try {
    out.block = await F(
      base + "/data_browser_web/block_tree/block_from_config?business=quantApi&func=BasicData&type=stk"
    );
  } catch (e) {
    out.block = String(e);
  }
  const peek = (o) => {
    const s = JSON.stringify(o);
    return s.length > 1500 ? s.slice(0, 1500) + " …[+" + (s.length - 1500) + " chars]" : s;
  };
  console.log("=== TREE ===\n" + peek(out.tree));
  console.log("=== LIST0 ===\n" + peek(out.list0));
  console.log("=== BLOCK ===\n" + peek(out.block));
  window.__ifindProbe = out; // 完整结果留在 window.__ifindProbe,需要时可再取
})();
