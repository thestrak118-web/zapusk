# Hozirgi BIR saytlar

Yangi variantlar: [a](a/), [b](b/), [c](c/). [Sozlash va tekshiruvlar](BIR.md). Asosiy index.html shu variantlarni ochadi.

Quyida oldingi `example/` loyihasi hujjati saqlangan.

# Zapusk — AI vebinar landing (3 ta variant)

Figma fayl **"Untitled"** (`gAx3LlafiCUAtWgLze0tbH`), **Page 2** dan 1:1 ko'chirilgan statik sayt.

```
zapusk/
├── example/a/   → Figma "Site 1" (1:90, 390×2913) — oq fon, ko'k CTA
├── example/b/   → Figma "Site 2" (1:162, 390×1877) — qora fon, oltin CTA
├── example/c/   → Figma "Site 3" (1:4, 390×2292) — oq fon, to'q sariq CTA
├── index.html   → uchalasini yonma-yon ko'rish (bosh sahifa)
├── _check/      → Figma bilan solishtirish vositasi (saytga kirmaydi)
└── MEMORY.md    → loyiha xotirasi: dizayn tizimi, qoidalar, ish jurnali
```

Har bir papka **mustaqil**: `index.html`, `css/`, `js/`, `assets/`. Bittasini
olib hostingga tashlasangiz, ishlaydi.

## Ishga tushirish

```bash
cd zapusk && python3 -m http.server 8899
# http://localhost:8899/            — uchala variant yonma-yon
# http://localhost:8899/example/a/   (b, c)
# http://localhost:8899/            (uchala variant yonma-yon)
```

Hosting: kerakli papkani Netlify / Vercel / GitHub Pages / nginx'ga qo'ying.

## Sozlash — `example/<variant>/js/config.js`

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
