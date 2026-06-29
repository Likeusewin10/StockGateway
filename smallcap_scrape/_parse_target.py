import re, glob, os

base = os.path.dirname(__file__)
raw = os.path.join(base, '_raw')

code_re = re.compile(r'(\d{6})\.(SZ|SH|BJ)')
num_re = re.compile(r'^-?\d+(\.\d+)?$')

summary = []
for industry in ['医药生物', '基础化工', '环保']:
    d = os.path.join(raw, industry)
    seen = {}
    order = []
    for path in sorted(glob.glob(os.path.join(d, '*.md'))):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('|'):
                    continue
                if '股票代码' in line or '---' in line:
                    continue
                cells = [c.strip() for c in line.strip('|').split('|')]
                code = None
                for c in cells:
                    m = code_re.search(c)
                    if m:
                        code = m.group(1)
                        break
                if not code:
                    continue
                mktcap = None
                for c in reversed(cells):
                    cc = c.replace(',', '')
                    if num_re.match(cc):
                        mktcap = cc
                        break
                if mktcap is None:
                    continue
                if code not in seen:
                    seen[code] = mktcap
                    order.append(code)
    out = os.path.join(base, industry + '.md')
    with open(out, 'w', encoding='utf-8') as o:
        for code in order:
            o.write(f'|{code}|{seen[code]}|\n')
    summary.append(f'{industry} {len(order)}')

print(', '.join(summary))
