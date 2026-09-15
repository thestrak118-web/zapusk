# Zapusk — landing variantlari

Figma fayl **"Untitled"** (`gAx3LlafiCUAtWgLze0tbH`) dan 1:1 ko'chirilgan statik
saytlar. Ikki kampaniya, har birida 3 ta variant.

```
zapusk/
├── example/d/   → Page 1 "Site 1" (390×1380) — oq fon, ko'k CTA      ┐ logistika
├── example/e/   → Page 1 "Site 2" (390×1781) — qora fon, sariq CTA   │ 19-sentyabr
├── example/f/   → Page 1 "Site 3" (390×1925) — oq fon, qizil CTA     ┘ 20:00
├── example/a/   → Page 2 "Site 1" (1:90, 390×2913) — oq fon, ko'k CTA    ┐ uStudy
├── example/b/   → Page 2 "Site 2" (1:162, 390×1877) — qora fon, oltin    │ AI darsi
├── example/c/   → Page 2 "Site 3" (1:4, 390×2292) — oq fon, to'q sariq   ┘
├── index.html   → hammasini yonma-yon ko'rish (bosh sahifa)
├── tools/       → d·e·f ni Figma SVG'dan yig'adigan generator va sinov
├── _check/      → Figma bilan solishtirish vositasi (saytga kirmaydi)
└── MEMORY.md    → loyiha xotirasi: dizayn tizimi, qoidalar, ish jurnali
```

## Logistika variantlari (d · e · f) — qanday yig'iladi

Bu uchtasi **qo'lda yozilmaydi**: `tools/svg2site.py` Figma freymining SVG
eksportidan `index.html` va `css/site.css` ni o'zi chiqaradi.

```bash
# Figma: freymni tanlab Export → SVG (Site 1.svg, Site 2.svg, Site 3.svg)
python3 tools/build.py ~/Downloads/figma-svg        # uchalasi
python3 tools/build.py ~/Downloads/figma-svg d      # bittasi
```

Yig'ilgandan keyin `logistics-launch/integration.py` ro'yxatdan o'tish oqimini
o'rnatadi: `js/main.js`, `thankYou.html`, shriftlar. Forma sahifada turmaydi —
`main.js` uni birinchi CTA bosilganda o'zi qo'shadi, sahifada faqat
`<button type="button" data-register>` bo'ladi.

Sozlash — `example/<v>/js/config.js` ichidagi `LOGISTICS_CONFIG`:
`endpointUrl` (lead yoziladigan manzil), `telegramUrl` (rahmat sahifasidagi
kanal tugmasi), `pixelId`, `sheetName`. Bo'sh qoldirilsa — o'sha imkoniyat
halol ravishda o'chirilgan holatda qoladi.

Sinov: `python3 -m http.server 8899` ishlab turganda `python3 tools/test_flow.py`
— uchala variantda modal, validatsiya va `thankYou.html` ga o'tish tekshiriladi
(Google Sheets so'rovi ataylab bloklanadi, jadvalga sinov lidi tushmaydi).

Har bir papka **mustaqil**: `index.html`, `css/`, `js/`, `assets/`. Bittasini
olib hostingga tashlasangiz, ishlaydi.

## Ishga tushirish

```bash
cd zapusk && python3 -m http.server 8899
# http://localhost:8899/            — hammasi yonma-yon
# http://localhost:8899/example/d/   (e, f — logistika)
# http://localhost:8899/example/a/   (b, c — uStudy)
```

Hosting: kerakli papkani Netlify / Vercel / GitHub Pages / nginx'ga qo'ying.

## Sozlash — uStudy variantlari (a · b · c) `js/config.js`

> d · e · f boshqacha sozlanadi — yuqoridagi `LOGISTICS_CONFIG` bo'limiga qarang.

| Kalit | Vazifasi |
|---|---|
| `ctaUrl` | "Bepul qatnashish" havolasi (Telegram bot/kanal). Havolaga `start=v1_hero` qo'shiladi — qaysi variant va qaysi tugma ishlaganini bot tomonda ko'rasiz. |
| `eventDate` | Vebinar sanasi (ma'lumot uchun). |
| `timerMinutes` | Taymer uzunligi. 120 → Figma'dagidek `01:59` dan boshlanadi. `localStorage`da saqlanadi, tugagach qaytadan boshlanadi. |

Variant **c** dagi oq maydon ("+" va strelka) — Figma dizaynidagi ko'rinish;
telefon kiritish maydoni emas, bosilganda `ctaUrl` ga olib boradi.

## Qanday qilib Figma bilan aynan bir xil qilingan

**1. Koordinatalar.** Har bir element Figma REST API'dan olingan absolyut
koordinatada joylashtirilgan (`left/top/width/height`), 390px kanvas ichida.
Hech qanday "taxminan" yo'q — CSS'dagi raqamlar Figma'dagi raqamlarning o'zi.

**2. Ekranga moslashish.** `<meta name="viewport" content="width=390">` —
brauzerning o'zi 390px maketni telefon ekraniga proporsional kattalashtiradi.
Nisbatlar hech qachon buzilmaydi.

**3. Shriftlar.**

| Figma'da | Saytda | Izoh |
|---|---|---|
| Inter, Inter Tight, Karantina | **o'sha shriftning o'zi** (Google Fonts) | jonli matn, tanlanadi, SEO uchun ochiq |
| Herokid, YU Buyan, Buyan, Helvetica Neue | **Figma'dan SVG kontur** (`assets/txt/*.svg`) | bepul emas, shuning uchun Figma'ning o'zidan vektor qilib eksport qilingan — piksel-piksel aynan o'sha shrift. `alt` atributida matn qoldirilgan (SEO va skrinrider uchun) |
| Herokid/Buyan — faqat **taymer** | Bebas Neue | taymer jonli, raqamlari o'zgarib turadi, shuning uchun rasm qilib bo'lmaydi. 6 ta bepul shrift raqamli o'lchovdan o'tkazilib, eng yaqini tanlangan (xato 18.5 — keyingi nomzod 32.8) |

Agar sizda Herokid / Buyan `.woff2` bo'lsa: `css/base.css` dagi `--font-display`
va `--font-buyan` ro'yxati boshiga qo'shsangiz, taymer ham asl shriftga o'tadi.

**4. Rasmlar.** Barchasi Figma node'laridan 3x PNG qilib eksport qilinib WebP'ga
o'girilgan. Soyasi bor elementlar (tugma, kartochka rasmi) Figma'ning
*render bounds* o'lchamida joylashtirilgan, shuning uchun soyalar ham mos tushadi.

**5. Tekshirish.** Har bir sahifa headless Chrome'da 390×balandlik qilib
render qilinib, Figma renderi bilan piksel darajasida solishtirilgan:

| Variant | O'rtacha farq (0–255) | Sezilarli farqli piksel |
|---|---|---|
| a | 7.9 | 4.6% |
| b | 7.4 | 4.4% |
| c | 2.5 | 1.5% |
| d | 2.72 | 1.9% |
| e | 2.46 | 1.9% |
| f | 2.48 | 1.4% |

Qolgan farq — joylashuv emas, faqat harf chetlarining silliqlanishi
(Figma va brauzer matnni bir xil rasterlashtirmaydi). Ko'z bilan farqi bilinmaydi.

Qayta tekshirish: `http://localhost:8899/_check/diff.html?v=a`
(`difference` rejimi — **qora = aynan mos**). Parametrlar: `&m=side` yonma-yon,
`&b=4` farqni yorqinlashtirish, `&s=0.3` butun sahifani ko'rish.

## Figma'dan ataylab qilingan 2 ta farq

1. **Taymer** — Figma'da qotib qolgan matn (`01:59`, `02:05:35`), bu yerda jonli
   sanoq: a va c — `hh:mm`, b — `hh:mm:ss`.
2. **Variant c** dagi oq maydon Figma'dagi qatlam tartibi bilan aynan chizilgan
   (spiker rasmi ostida, "+" va strelka ustida), lekin telefon kiritish maydoni
   emas — butun maydon `ctaUrl` ga havola.
