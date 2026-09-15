#!/usr/bin/env python3
"""Yig'ilgan variantni tezlashtiradi: Google Fonts o'rniga lokal subset.

  python3 tools/localfonts.py example/d

Sahifadagi hamma <text> ko'rib chiqiladi, har bir shrift uchun faqat
ishlatilgan harflardan iborat WOFF2 yuklab olinadi (Google css2 `text=`
parametri), `fonts/` ga saqlanadi va `@font-face` bilan ulanadi.
CSS sahifa ichiga ko'chiriladi — render to'sadigan so'rov qolmaydi.
"""
import html as htmlmod
import re, sys, urllib.parse, urllib.request
from pathlib import Path

UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/151.0.0.0 Safari/537.36')
WEIGHT = {'normal': '400', 'bold': '700'}


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode('utf-8')


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def collect(page):
    """(shrift, og'irlik) -> ishlatilgan belgilar."""
    used = {}
    for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', page, re.S):
        attrs, inner = m.group(1), m.group(2)
        fam = re.search(r'font-family="([^"]*)"', attrs)
        if not fam:
            continue
        fam = fam.group(1).split(',')[0].strip().strip("'\"")
        w = re.search(r'font-weight="([^"]*)"', attrs)
        w = (w.group(1) if w else '400').strip()
        w = WEIGHT.get(w, w)
        text = htmlmod.unescape(re.sub(r'<[^>]+>', '', inner))
        used.setdefault((fam, w), set()).update(text)
    return used


def google_woff2(family, weight, chars):
    """css2 `text=` — faqat shu belgilar uchun subset qaytaradi."""
    text = ''.join(sorted(chars))
    base = 'https://fonts.googleapis.com/css2?family='
    for spec in ('%s:wght@%s' % (family.replace(' ', '+'), weight),
                 family.replace(' ', '+')):
        url = base + spec + '&text=' + urllib.parse.quote(text) + '&display=swap'
        try:
            css = fetch(url)
        except Exception:
            continue
        # subset havolasi `.woff2` bilan tugamaydi: /l/font?kit=...
        src = re.search(r"src:\s*url\((https://[^)]+)\)\s*format\('woff2'\)", css)
        if src:
            return fetch(src.group(1), binary=True)
    return None


def main():
    out = Path(sys.argv[1])
    page = (out / 'index.html').read_text(encoding='utf-8')
    used = collect(page)
    if not used:
        sys.exit('%s: <text> topilmadi' % out)

    (out / 'fonts').mkdir(exist_ok=True)
    faces, preloads, got = [], [], []
    for (fam, w), chars in sorted(used.items()):
        data = google_woff2(fam, w, chars)
        if not data:
            print('   OGOHLANTIRISH: %s %s yuklanmadi — Google Fonts qoladi' % (fam, w))
            return
        name = '%s-%s.woff2' % (slug(fam), w)
        (out / 'fonts' / name).write_bytes(data)
        faces.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
                     "font-display:swap;src:url(../fonts/%s) format('woff2')}"
                     % (fam, w, name))
        preloads.append('<link rel="preload" href="fonts/%s" as="font" '
                        'type="font/woff2" crossorigin>' % name)
        got.append('%s %s — %d belgi, %.1f KB' % (fam, w, len(chars), len(data) / 1024))

    (out / 'css/fonts.css').write_text('\n'.join(faces) + '\n', encoding='utf-8')

    # CSS sahifa ichiga: render to'sadigan so'rov qolmaydi
    css = '\n'.join((out / 'css' / f).read_text(encoding='utf-8')
                    for f in ('fonts.css', 'base.css', 'site.css'))
    css = css.replace('../fonts/', 'fonts/')
    page = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', page)
    page = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>\n?', '', page)
    page = re.sub(r'<link rel="stylesheet" href="css/(base|site)\.css">\n?', '', page)

    # LCP rasmini oldindan yuklash
    first = re.search(r'<img class="im [^"]*" src="(assets/[^"]+)"', page)
    if first:
        preloads.insert(0, '<link rel="preload" href="%s" as="image" '
                           'fetchpriority="high">' % first.group(1))
    page = page.replace('</head>',
                        '\n'.join(preloads) + '\n<style>\n' + css + '</style>\n</head>', 1)
    (out / 'index.html').write_text(page, encoding='utf-8')

    print('   lokal shriftlar:')
    for line in got:
        print('     ' + line)
    print('   CSS sahifa ichiga ko\'chirildi, tashqi so\'rov qolmadi')


if __name__ == '__main__':
    main()
