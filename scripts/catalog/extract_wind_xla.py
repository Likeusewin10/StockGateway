"""从 Wind Excel 插件 WindFunc.xla(OLE2)提取全量字段字典 —— catalog 方法 A。

WindFunc.xla 是 Excel 版 Wind 函数向导,内嵌 ~15000 字段。字段代码+中文名在
VBA 模块流(NewFunc2/NewFunc3)里,用 MS-OVBA 压缩。本脚本:
  1. 纯 stdlib 解析 OLE2 复合文档,取出 VBA 模块流;
  2. 按 MS-OVBA(MS-VBA 2.4.1)解压 CompressedContainer;
  3. 从解压源码里提取「字段代码 → 中文名」配对。

产出:docs/catalog/_raw/windfunc_decompressed/*.bas(解压源码,gitignored)
      docs/catalog/wind/xla_fields.csv(提取的字段字典)

用法:.venv-api\\Scripts\\python scripts\\catalog\\extract_wind_xla.py
"""
import os
import re
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLA = r"C:\Wind\Wind.NET.Client\WindNET\DataBrowse\XLA\WindFunc.xla"
RAW = os.path.join(ROOT, "docs", "catalog", "_raw", "windfunc_decompressed")
OUT = os.path.join(ROOT, "docs", "catalog", "wind", "xla_fields.csv")


# ---------- OLE2 复合文档(纯 stdlib) ----------
class Ole:
    def __init__(self, data):
        self.d = data
        self.sect = 1 << struct.unpack("<H", data[30:32])[0]
        self.msect = 1 << struct.unpack("<H", data[32:34])[0]
        self.minicut = struct.unpack("<i", data[56:60])[0]
        dirstart = struct.unpack("<i", data[48:52])[0]
        difat = [x for x in struct.unpack("<109i", data[76:512]) if x >= 0]
        fat = b"".join(self._sec(s) for s in difat)
        self.FAT = struct.unpack("<%di" % (len(fat) // 4), fat)
        self.dir = self._big(dirstart)
        self.ents = self._read_dir()
        root = self.ents["Root Entry"]
        self.ministream = self._big(root[1])
        mfat = self._big(struct.unpack("<i", data[60:64])[0])
        self.MFAT = struct.unpack("<%di" % (len(mfat) // 4), mfat)

    def _sec(self, n):
        off = 512 + n * self.sect
        return self.d[off:off + self.sect]

    def _chain(self, s, F):
        o = []
        while 0 <= s < len(F) and s != -2 and len(o) < 4000000:
            o.append(s)
            s = F[s]
        return o

    def _big(self, start):
        return b"".join(self._sec(x) for x in self._chain(start, self.FAT))

    def _read_dir(self):
        ents = {}
        for i in range(0, len(self.dir), 128):
            e = self.dir[i:i + 128]
            if len(e) < 128:
                break
            nl = struct.unpack("<H", e[64:66])[0]
            if not nl:
                continue
            nm = e[:nl - 2].decode("utf-16le", "ignore")
            ents[nm] = (e[66], struct.unpack("<i", e[116:120])[0],
                        struct.unpack("<I", e[120:124])[0])
        return ents

    def get(self, nm):
        _t, start, size = self.ents[nm]
        if size < self.minicut:
            data = b"".join(self.ministream[x * self.msect:(x + 1) * self.msect]
                            for x in self._chain(start, self.MFAT))
            return data[:size]
        return self._big(start)[:size]


# ---------- MS-OVBA 解压(MS-VBA §2.4.1) ----------
def decompress(buf):
    if not buf or buf[0] != 0x01:
        return b""
    out = bytearray()
    i = 1
    n = len(buf)
    while i < n:
        # CompressedChunkHeader: 2 bytes
        hdr = struct.unpack("<H", buf[i:i + 2])[0]
        i += 2
        size = (hdr & 0x0FFF) + 3
        flag_comp = (hdr & 0x8000) != 0
        end = i + size - 2
        if not flag_comp:
            out += buf[i:i + 4096]
            i += 4096
            continue
        chunk_start = len(out)
        while i < end and i < n:
            flags = buf[i]
            i += 1
            for bit in range(8):
                if i >= end or i >= n:
                    break
                if not (flags >> bit) & 1:
                    out.append(buf[i])
                    i += 1
                else:
                    tok = struct.unpack("<H", buf[i:i + 2])[0]
                    i += 2
                    diff = len(out) - chunk_start
                    bcount = 4
                    while (1 << bcount) < diff:
                        bcount += 1
                    bcount = max(4, min(bcount, 12))
                    lmask = 0xFFFF >> bcount
                    length = (tok & lmask) + 3
                    offset = (tok >> (16 - bcount)) + 1
                    for _ in range(length):
                        out.append(out[len(out) - offset])
    return bytes(out)


def module_offsets(ole):
    """解析 VBA `dir` 流(MS-OVBA),返回 {模块名: MODULEOFFSET}。
    MODULEOFFSET(rid 0x0031)指向模块流里真正压缩源码的起点,跳过 PerformanceCache。"""
    d = decompress(ole.get("dir"))
    offs = {}
    p = 0
    while True:
        p = d.find(b"\x19\x00", p)   # MODULENAME(0x0019)
        if p < 0:
            break
        sz = struct.unpack("<I", d[p + 2:p + 6])[0]
        if 0 < sz < 64:
            raw_nm = d[p + 6:p + 6 + sz]
            if all(c >= 0x20 or c > 127 for c in raw_nm):
                nm = raw_nm.decode("gbk", "ignore")
                o = d.find(b"\x31\x00\x04\x00\x00\x00", p)  # MODULEOFFSET(0x0031,size4)
                if o >= 0:
                    offs[nm] = struct.unpack("<I", d[o + 6:o + 10])[0]
        p += 2
    return offs


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ole = Ole(open(XLA, "rb").read())
    offs = module_offsets(ole)
    modules = [n for n in ole.ents if n.startswith("NewFunc")]
    print("VBA 模块流:", modules, "offsets:", {m: offs.get(m) for m in modules})

    text = ""
    for m in modules:
        raw = ole.get(m)
        off = offs.get(m)
        if off is None or off >= len(raw):
            print(f"  {m}: 无有效 MODULEOFFSET,跳过")
            continue
        # 真源码压缩容器从 MODULEOFFSET 起(跳过 PerformanceCache)
        src = decompress(raw[off:]).decode("gbk", "ignore")
        open(os.path.join(RAW, m + ".bas"), "w", encoding="utf-8").write(src)
        text += "\n" + src
        kw = src.count("Function") + src.count("Sub ")
        print(f"  {m}: raw {len(raw)} @off {off} -> 源码 {len(src)} 字符 (VBA关键字 {kw})")

    _extract_pairs(text)


def _extract_pairs(text):
    """从解压 VBA 源码提取字段。每字段一个 Function,其上一行注释为
    `'中文名,字段代码`(代码即 Function 名,大写形式)。同时抓 Function 形参作参数列。
    例:
        '预测每股收益(明细值),S_Est_EPS_Inst
        Function s_est_eps_inst(WINDCODE_ As Variant, RPTYEAR_ As Integer, ParamArray ...) As Variant
    """
    rows = {}
    lines = text.replace("\r", "").split("\n")
    func_re = re.compile(r"^\s*(?:Public\s+|Private\s+)?Function\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)", re.I)
    for i, ln in enumerate(lines):
        m = func_re.match(ln)
        if not m:
            continue
        code = m.group(1).lower()
        params = m.group(2)
        # 上一行注释取中文名
        cname = ""
        if i > 0:
            c = lines[i - 1].strip()
            if c.startswith("'"):
                body = c[1:].strip()
                # 形如 中文名,Code —— 末段是代码,前段是中文名
                if "," in body:
                    head, tail = body.rsplit(",", 1)
                    if tail.strip().lower() == code:
                        cname = head.strip()
                    else:
                        cname = body
                else:
                    cname = body
        if not re.search(r"[一-鿿]", cname):
            continue   # 无中文名的(内部辅助函数)跳过
        # 形参名(去掉类型/可选/ParamArray)作可读参数
        pnames = []
        for seg in params.split(","):
            seg = seg.strip()
            if not seg:
                continue
            pn = re.sub(r"^(ByVal|ByRef|Optional|ParamArray)\s+", "", seg, flags=re.I)
            pn = pn.split(" As ")[0].split("(")[0].strip().rstrip("_")
            if pn and pn.lower() not in ("windcode", "paramset", "optionalparams"):
                pnames.append(pn)
        rows[code] = (cname, "、".join(pnames))
    print(f"\n提取字段(带中文名): {len(rows)}")
    import csv
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["字段代码", "字段(大写)", "中文名", "参数"])
        for code in sorted(rows):
            cname, pn = rows[code]
            w.writerow([code, code.upper(), cname, pn])
    print("样例:", [(c, rows[c][0]) for c in list(rows)[:12]])
    print("->", OUT)


if __name__ == "__main__":
    main()
