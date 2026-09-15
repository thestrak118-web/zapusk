# Logistika vebinar — 3 ta landing varianti

Figma "Untitled" / Page 1 dan 1:1 ko'chirilgan statik saytlar.
**19-sentyabr, soat 20:00** — bepul vebinar, 10 000$ lik grant.

```
zapusk/
├── a/          → Figma "Site 1" (390×1380) — oq fon, ko'k CTA
├── b/          → Figma "Site 2" (390×1781) — qora fon, to'q sariq CTA
├── c/          → Figma "Site 3" (390×1925) — oq fon, qizil CTA
├── index.html  → uchalasini yonma-yon ko'rish
├── tools/      → Figma SVG'dan sayt yig'adigan generator va sinovlar
└── arxiv/      → eski kampaniyalar (BIR, uStudy) va eski tekshiruv vositalari
```

Har bir papka **mustaqil**: `index.html`, `css/`, `js/`, `assets/`, `fonts/`,
`thankYou.html`. Bittasini olib hostingga tashlasangiz, ishlaydi.

## Ishga tushirish

```bash
cd zapusk && python3 -m http.server 8899
# http://localhost:8899/     — uchalasi yonma-yon
# http://localhost:8899/a/   (b, c)
```

## Sozlash — `<variant>/js/config.js`

| Kalit | Vazifasi |
|---|---|
| `endpointUrl` | Ariza yoziladigan Google Apps Script manzili |
| `sheetName` | **Majburiy.** Jadvaldagi varaq nomi — bo'sh bo'lsa endpoint `MISSING_SHEET` xatosini qaytaradi va ariza yozilmaydi |
| `telegramUrl` | Rahmat sahifasidagi kanal tugmasi |
| `pixelId` | Meta Pixel ID (faqat raqam bo'lsa ishlaydi) |

Meta eventlari: sahifa ochilganda `PageView`, har bir CTA bosilganda
**`CompleteRegistration`** (standart event). `pixelId` bo'sh bo'lsa hech qanday
so'rov ketmaydi.

Oqim: forma to'ldiriladi → `sessionStorage` ga yoziladi → darhol `thankYou.html`
ochiladi → so'rov orqa fonda ketadi. Forma sahifada turmaydi: `js/main.js` uni
birinchi CTA bosilganda o'zi qo'shadi, sahifada faqat
`<button type="button" data-register>` bo'ladi.

## Qayta yig'ish

Sahifalar **qo'lda tahrirlanmaydi** — `tools/svg2site.py` ularni Figma SVG
eksportidan chiqaradi.

```bash
# Figma: freymni tanlab Export → SVG (Site 1.svg, Site 2.svg, Site 3.svg)
python3 tools/build.py ~/Downloads/figma-svg      # uchalasi
python3 tools/build.py ~/Downloads/figma-svg a    # bittasi
```

Har bir yig'ishda: SVG → sahifa → lokal shrift subseti → ro'yxatdan o'tish oqimi.
Sozlamalar fayli (`js/config.js`) saqlanib qoladi.

## Tezlik

Lighthouse (mobil, siqish yoqilgan hosting sharoitida):

| Variant | Ball | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|
| a | 0.99 | 626 ms | 1503 ms | 139 ms | 0 |
| b | 0.98 | 631 ms | 1801 ms | 128 ms | 0 |
| c | 0.99 | 629 ms | 1726 ms | 135 ms | 0 |

Nima qilingan:

- **Shriftlar lokal va subset.** Har bir shriftdan faqat sahifada uchraydigan
  harflar olinadi (1–5 KB), Google Fonts'ga so'rov yo'q.
- **CSS sahifa ichida.** Render to'sadigan tashqi so'rov qolmagan.
- **Rasmlar AVIF, 2x.** WebP 3x bilan solishtirganda ~2 barobar yengil.
- **LCP rasmi `preload`** bilan oldindan so'raladi.
- Qolgan TBT — Meta Pixel'ning `fbevents.js` fayli (~108 KB, tashqi).

## Figma bilan aniqlik

Headless Chrome renderi Figma'ning 2x eksporti bilan piksel darajasida
solishtiriladi:

| Variant | O'rtacha farq (0–255) | >32 farqli piksel |
|---|---|---|
| a | 2.14 | 1.4% |
| b | 2.55 | 1.9% |
| c | 2.22 | 1.1% |

Qolgan farq — joylashuv emas, harf chetlarining silliqlanishi.

Litsenziyali HelveticaNeue **Arimo** bilan almashtirilgan (metrik jihatdan mos).

## Sinov

```bash
python3 -m http.server 8899      # boshqa terminalda
python3 tools/test_flow.py
```

Uchala variantda 11 tadan tekshiruv: CTA tugmalari, modal, forma maydonlari,
`+998`, bo'sh/qisqa raqamda o'tkazmaslik, `thankYou.html` ga o'tish.
Google Sheets so'rovi sinov paytida bloklanadi — jadvalga sinov qatori tushmaydi.
