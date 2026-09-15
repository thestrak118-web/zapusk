#!/usr/bin/env python3
"""Barcha variantlarni Figma SVG'laridan qayta yig'adi va ro'yxatdan o'tish
oqimini o'rnatadi.

  python3 tools/build.py <svg-papka> [variant ...]

<svg-papka> ichida tools/variants.json da ko'rsatilgan "Site N.svg" fayllari
bo'lishi kerak (Figma: freymni tanlab Export -> SVG).
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTEGRATION = Path('/home/erwin/qwertyu/logistics-launch')


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    svg_dir = Path(sys.argv[1])
    conf = json.loads((ROOT / 'tools/variants.json').read_text(encoding='utf-8'))
    wanted = sys.argv[2:] or list(conf['variants'])

    sys.path.insert(0, str(INTEGRATION))
    from integration import install_integration

    for name in wanted:
        meta = dict(conf['variants'][name])
        svg = svg_dir / meta.pop('svg')
        if not svg.exists():
            sys.exit('topilmadi: %s' % svg)
        out = ROOT / name
        # eski rasmlar qolib ketmasin
        for pat in ('%s-*.webp', '%s-*.avif'):
          for old in (out / 'assets').glob(pat % meta['prefix']):
              old.unlink()
        subprocess.run([sys.executable, str(ROOT / 'tools/svg2site.py'),
                        str(svg), str(out), json.dumps(meta, ensure_ascii=False)],
                       check=True)
        # Google Fonts -> lokal subset, CSS sahifa ichiga
        subprocess.run([sys.executable, str(ROOT / 'tools/localfonts.py'), str(out)],
                       check=True)
        info = install_integration(out)
        print('   ro\'yxatdan o\'tish oqimi o\'rnatildi (%d bayt), config saqlandi: %s'
              % (info['runtimeBytes'], info['configPreserved']))


if __name__ == '__main__':
    main()
