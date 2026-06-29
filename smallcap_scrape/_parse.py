import re, glob, os

seen = {}
rows = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '*.md'))):
    industry = os.path.splitext(os.path.basename(f))[0]
    for line in open(f, encoding='utf-8'):
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        m = re.match(r'^(\d{6})(\.(SZ|SH|BJ))?$', cells[0])
        if not m:
            continue
        code = m.group(1)
        mc = None
        for c in reversed(cells):
            try:
                mc = float(c.replace(',', ''))
                break
            except ValueError:
                continue
        if mc is None:
            continue
        yi = round(mc / 1e8, 2)
        if yi > 300:
            continue
        if code in seen:
            continue
        seen[code] = True
        rows.append((code, yi, industry))

rows.sort(key=lambda r: (r[2], r[0]))
out = os.path.join(os.path.dirname(__file__), '..', 'smallcap_result.csv')
with open(out, 'w', encoding='utf-8') as o:
    for code, yi, ind in rows:
        o.write(f"{code},{yi},{ind}\n")
print('total', len(rows))
from collections import Counter
for k, v in sorted(Counter(r[2] for r in rows).items()):
    print(k, v)
