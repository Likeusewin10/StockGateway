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


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ole = Ole(open(XLA, "rb").read())
    modules = [n for n in ole.ents if n.startswith("NewFunc")]
    print("VBA 模块流:", modules)

    text = ""
    for m in modules:
        raw = ole.get(m)
        # VBA 模块流 = PerformanceCache + CompressedSourceCode。
        # 压缩容器从某个 0x01 字节起;扫描首个 0x01 后能成功解压的位置。
        best = b""
        for off in range(0, min(len(raw), 8192)):
            if raw[off] == 0x01:
                try:
                    dec = decompress(raw[off:])
                except Exception:
                    continue
                if len(dec) > len(best):
                    best = dec
                if len(best) > 100000:
                    break
        src = best.decode("gbk", "ignore")
        open(os.path.join(RAW, m + ".bas"), "w", encoding="utf-8").write(src)
        text += "\n" + src
        print(f"  {m}: raw {len(raw)} -> 解压 {len(best)} bytes")

    _extract_pairs(text)


def _extract_pairs(text):
    # 字段代码↔中文名配对:VBA 源码里常见模式如
    #   "字段代码","中文名"  /  Array("code","中文")  / code = "中文"
    pairs = {}
    for code, name in re.findall(r'["\x27]([a-zA-Z][a-zA-Z0-9_]{1,30})["\x27]\s*,\s*["\x27]([^"\x27]{1,40})["\x27]', text):
        if re.search(r"[一-鿿]", name) and "_" in code or code.islower():
            pairs.setdefault(code.lower(), name)
    print(f"\n提取『代码→中文』配对: {len(pairs)}")
    import csv
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["字段代码", "中文名"])
        for code in sorted(pairs):
            w.writerow([code, pairs[code]])
    print("样例:", list(pairs.items())[:15])
    print("->", OUT)


if __name__ == "__main__":
    main()
