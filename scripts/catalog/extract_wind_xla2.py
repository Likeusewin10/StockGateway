"""从 Wind Excel 插件 .xla(OLE2)提取全量字段字典 —— 方法 A 增强版(支持大文件 + 多 .xla)。

相比 extract_wind_xla.py 的改进:
  1. **修 DIFAT 截断 bug**:原解析器只读 header 内 109 个 DIFAT 项(上限寻址 ~7MB),
     大文件(WindFunc_s.xla 22MB,344 个 FAT 扇区)会被截断。本版跟 DIFAT 扩展扇区链,完整读 FAT。
  2. **VBA dir 流容错**:dir 流可能嵌在 VBA storage 子树(扁平名查不到),
     找不到 MODULEOFFSET 时**暴力扫描模块流定位压缩源码起点**(扫 0x01 容器,取解出最多 Function 的偏移)。
  3. 命令行传 xla 路径,自动识别 NewFunc* 模块。

用法:.venv-api\\Scripts\\python scripts\\catalog\\extract_wind_xla2.py <xla路径> <输出csv>
例: ... WindFunc_s.xla docs/catalog/wind/xla_fields_full.csv
"""
import csv
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Ole:
    def __init__(self, data):
        self.d = data
        self.sect = 1 << struct.unpack("<H", data[30:32])[0]
        self.msect = 1 << struct.unpack("<H", data[32:34])[0]
        self.minicut = struct.unpack("<i", data[56:60])[0]
        dirstart = struct.unpack("<i", data[48:52])[0]
        # --- DIFAT: 先取 header 内 109 项,再跟扩展扇区链(修大文件截断) ---
        difat = [x for x in struct.unpack("<109i", data[76:512]) if x >= 0]
        difat_sec = struct.unpack("<i", data[68:72])[0]
        n_difat = struct.unpack("<I", data[72:76])[0]
        per = self.sect // 4
        cnt = 0
        while 0 <= difat_sec and cnt < n_difat + 2:
            sec = self._sec(difat_sec)
            vals = struct.unpack("<%di" % per, sec)
            difat += [x for x in vals[:-1] if x >= 0]
            difat_sec = vals[-1]
            cnt += 1
            if difat_sec in (-1, -2):
                break
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


def decompress(buf):
    if not buf or buf[0] != 0x01:
        return b""
    out = bytearray()
    i = 1
    n = len(buf)
    while i < n:
        if i + 2 > n:
            break
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


def best_source(raw):
    """暴力扫描模块流,找解出最多 Function 的 0x01 压缩容器起点。返回解压源码。"""
    best_src, best_fn = "", 0
    limit = min(len(raw), 300000)
    for off in range(limit):
        if raw[off] != 0x01:
            continue
        try:
            out = decompress(raw[off:])
        except Exception:   # noqa: BLE001
            continue
        if len(out) < 1000:
            continue
        s = out.decode("gbk", "ignore")
        fn = s.lower().count("function ")
        if fn > best_fn:
            best_fn, best_src = fn, s
            if fn > 50:        # 命中真源码,够大就停(避免全扫)
                # 继续扫到 off 之后无更优,简单起见命中大块即返回
                return best_src
    return best_src


PARAM_SKIP = {"windcode", "paramset", "optionalparams"}


def extract_pairs(text):
    rows = {}
    lines = text.replace("\r", "").split("\n")
    func_re = re.compile(r"^\s*(?:Public\s+|Private\s+)?Function\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)", re.I)
    for i, ln in enumerate(lines):
        m = func_re.match(ln)
        if not m:
            continue
        code = m.group(1).lower()
        params = m.group(2)
        cname = ""
        if i > 0:
            c = lines[i - 1].strip()
            if c.startswith("'"):
                body = c[1:].strip()
                if "," in body:
                    head, tail = body.rsplit(",", 1)
                    cname = head.strip() if tail.strip().lower() == code else body
                else:
                    cname = body
        pnames = []
        for seg in params.split(","):
            seg = seg.strip()
            if not seg:
                continue
            pn = re.sub(r"^(ByVal|ByRef|Optional|ParamArray)\s+", "", seg, flags=re.I)
            pn = pn.split(" As ")[0].split("(")[0].strip().rstrip("_")
            if pn and pn.lower() not in PARAM_SKIP:
                pnames.append(pn)
        # 保留所有 Function（含无中文名的，cname 可空）—— 不再丢弃，最大化候选
        if code not in rows or (not rows[code][0] and cname):
            rows[code] = (cname, "、".join(pnames))
    return rows


def main():
    if len(sys.argv) < 3:
        raise SystemExit("用法: extract_wind_xla2.py <xla路径> <输出csv>")
    xla, out = sys.argv[1], sys.argv[2]
    if not os.path.isabs(out):
        out = os.path.join(ROOT, out)
    ole = Ole(open(xla, "rb").read())
    modules = [n for n in ole.ents if n.startswith("NewFunc")]
    print(f"{os.path.basename(xla)} 模块流: {modules}")

    text = ""
    for m in modules:
        raw = ole.get(m)
        src = best_source(raw)
        fn = src.lower().count("function ")
        print(f"  {m}: raw {len(raw)} -> 源码 {len(src)} 字符 (~{fn} Function)")
        text += "\n" + src

    rows = extract_pairs(text)
    with_cn = sum(1 for v in rows.values() if v[0])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["字段代码", "字段(大写)", "中文名", "参数"])
        for code in sorted(rows):
            cname, pn = rows[code]
            w.writerow([code, code.upper(), cname, pn])
    print(f"\n提取 {len(rows)} 字段(含中文名 {with_cn})-> {out}")


if __name__ == "__main__":
    main()
