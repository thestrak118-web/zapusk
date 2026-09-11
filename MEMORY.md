# MEMORY.md — loyiha xotirasi

> Bu fayl **har bir ishdan keyin yangilanadi**. Yangi ish qilinsa — "Ish jurnali"
> bo'limiga yozuv qo'shiladi; dizayn qiymati o'zgarsa — "Dizayn tizimi" yangilanadi.

---

## 1. Manba

| | |
|---|---|
| Figma fayl | **"Untitled"** — `gAx3LlafiCUAtWgLze0tbH` |
| Sahifa | **Page 2** (`1:2`) |
| Freymlar | `1:90` Site 1 (390×2913) → `example/a`<br>`1:162` Site 2 (390×1877) → `example/b`<br>`1:4` Site 3 (390×2292) → `example/c` |
| Mavzu | uStudy — AI bo'yicha bepul onlayn dars, 18–19-sentabr, soat 20:00 |

**Figma token** — `/home/erwin/qwertyu/.env` faylida, `FIGMA_TOKEN` kaliti
(`chmod 600`, git repodan tashqarida, hech qachon commit qilinmaydi).

```bash
export $(grep FIGMA_TOKEN /home/erwin/qwertyu/.env | xargs)
curl -H "X-Figma-Token: $FIGMA_TOKEN" "https://api.figma.com/v1/files/gAx3LlafiCUAtWgLze0tbH"
```

> ⚠️ Bu token bir marta chatga ochiq yozilgan — imkoni bo'lsa Figma sozlamalaridan
> bekor qilib, yangisini olib `.env` ga yozib qo'ying.

---

## 2. Qat'iy qoidalar (o'zgartirilmaydi)

1. **Absolyut joylashuv.** Har bir element Figma koordinatasida:
   `left / top / width / height`. CSS'dagi raqam = Figma'dagi raqam.
   Hech qachon "taxminan" yoki flex/grid bilan qayta qurilmaydi.
2. **390px kanvas.** `<meta name="viewport" content="width=390">` —
   brauzer o'zi telefon ekraniga proporsional kattalashtiradi.
3. **Pullik shriftlar SVG kontur bilan.** Herokid, YU Buyan, Buyan,
   Helvetica Neue — bepul emas. Ular Figma'dan `format=svg&svg_outline_text=true`
   bilan eksport qilinadi (`assets/txt/*.svg`), `alt` da matn qoldiriladi.
4. **Bepul shriftlar asl holida.** Inter, Inter Tight, Karantina — Google Fonts.
5. **Qator uzilishlari `<br>` bilan qat'iy.** Brauzer Inter'ni Figma'dan
   ~1% kengroq chizadi, shuning uchun avtomatik o'ralishga tayanilmaydi.
6. **`→` (U+2192)** — Google Fonts Inter subsetida yo'q. Shu belgi uchun
   Inter mikro-subseti loyihada: `assets/fonts/inter-arrow.woff2` (3 KB),
   `base.css` dagi `@font-face` + `unicode-range:U+2192`.
7. **Soyali elementlar** Figma'ning *render bounds* o'lchamida joylashtiriladi
   (rasm eksporti soyani ham o'z ichiga oladi), `absoluteBoundingBox` emas.
8. **Har bir variant mustaqil.** `example/<v>/` ichida o'z `css/ js/ assets/`.
   Bittasini ko'chirib olsangiz ham ishlaydi.

---

## 3. Dizayn tizimi

### Umumiy
| | |
|---|---|
| Kanvas | 390px, `.page{position:relative;width:390px;overflow:hidden}` |
| Element klassi | `.n { position:absolute }` |
| Logotip | `assets/logo.webp` — a/c: 68×68 (`172,-2` / `181,-3`), b: 52×52 (`162,1`) |
| Sana / soat | 18-19-Sentabr · Soat 20:00 |

### Variant **a** — oq fon / ko'k CTA
```
--blue      #3164FB      --blue-dark #2455E4      --line #797979
sahifa foni #f2f4f8      kanvas #FFFFFF
```
| Element | Qiymat |
|---|---|
| H1 | Herokid 600 / 38 / lh 41.8 / center / UPPER → `txt/h1.svg` (`32.2, 77.1`) |
| H2 | Herokid 600 / 36 va 38 → `txt/h2-gifts.svg`, `txt/h2-learn.svg` |
| Taymer | Herokid 600 / 24 / lh 33.6 → **Bebas Neue** (jonli sanoq) |
| Asosiy matn | Inter 400 / 14 / lh 19.6 |
| Kichik matn | Inter 400 / 12 / lh 15.6 |
| Header | Inter 400 / 16 / lh 16 |
| CTA yozuvi | Inter 700 / 19.47 / UPPER, `white-space:nowrap` |
| CTA tugma | 339×86, `radius 95.74`, `#3164FB`,<br>`0 3.83px 17.7px rgba(49,100,251,.4)`, `0 3.54px 0 #2455E4`,<br>`inset 0 ±3.83px 3.83px rgba(255,255,255,.15)` |
| Sovg'a kartochka | 340×272, `radius 16`, `#fff`, `0 0 22.8px rgba(0,0,0,.18)`, rasm 308×138 r16 |
| "O'rganasiz" kartochka | 339×167, `radius 15`, `1px solid #797979`, **`7px 7px 0 #3164FB`** |
| Hero | shisha ikonkalar `9,223` va `218,220`; spiker `67,186` 239×281; ko'k nur `110,311` 144px `blur(75px)` |

### Variant **b** — qora fon / oltin CTA
```
--ink #1A1919   --gold #FFD899   --gold-1 #FFDF70   --gold-2 #FFE9A6
--gold-ink #492F0A   nuqta ichi #433116   sahifa foni #0b0b0b
oltin gradient: linear-gradient(140deg,#FFDF70,#FFE9A6 50%,rgba(255,223,112,.83))
```
| Element | Qiymat |
|---|---|
| H1 / H2 | **Karantina 400 / 46 / lh 46** / UPPER (asl shrift, Google Fonts) |
| H1 rangi | oq + "DAROMADGA CHIQISH" oltin gradient (`background-clip:text`) |
| Raqamlar 01–05 | Karantina 300 / 80 / lh 80 (`01` ls .05em, qolgani −.01em) |
| Ro'yxat matni | Inter 400 / 14 / lh 18.2 / oq |
| Sovg'a matni | **Inter Tight** 400 / 16 / lh 24 / qora |
| Taymer | Herokid 600 / 42 → **Bebas Neue**, 3 ta slot (`02:05:35` tartibi) |
| CTA | rasm-tugma `s2-btn.webp` (ticket shakli, soya bilan 380×140, `−15,−11`),<br>yozuv → `txt/cta1..3.svg` (Herokid 600 / 28 / ls 1.4 / `#492F0A`) |
| Sovg'a qatori | 358×111, `radius 20`, `#fff`, rasm 106×91 `radius 14` |
| Hero | fon rasm `0,-24` 390×657; gradient `0,434` 390×218 (`rgba(26,25,25,0)→#1A1919 56%`);<br>halqalar `26,312` 344px (.05) va `66,376` 264px (.10); oltin nur `114,317` 147px `blur(50px)` |

### Variant **c** — oq fon / to'q sariq CTA
```
--orange #FF5722   --orange-2 #FF7F57   --orange-dark #DC4D1F
--soft #F5F5F5     --dot #FFDACE        --circle #FFA284
```
| Element | Qiymat |
|---|---|
| H1 / H2 | YU Buyan 700 / 32 / lh 40 → `txt/h1.svg` (`20.5,79.2`), `txt/h2.svg` (`40.2,625.2`) |
| Chip yozuvlari | YU Buyan 700 / 14 / ls .28 → `txt/date.svg`, `txt/time.svg` |
| Kartochka matni | Helvetica Neue 400 / 14 / lh 18.2 / center → `txt/t1..t5.svg` |
| Taymer | Buyan 700 / 28 → **Bebas Neue** (`170, 568.5`) |
| CTA | 337.7×80.7, `radius 74.07`, `linear-gradient(90deg,#FF7F57,#FF5722)`,<br>`0 4px 0 #DC4D1F`; oq disk 56px (`270,13`); yozuv → `txt/cta1..2.svg` |
| Kartochka | 300×280 `radius 20` `#F5F5F5`; rasm 320×180 (render bounds, `−10,−6`)<br>`radius 20` `1px solid #fff` `0 4px 10px rgba(0,0,0,.1)`; check 23px `#FF5722` |
| Chip | 40×40 (o'ng 38×38), `radius 12.26`, `.817px solid #FF5722`, `#F5F5F5` |
| Telefon "pill" | 350×48 `radius 24` `1px solid #F4F4F4` `0 4px 4px rgba(107,107,107,.15)`.<br>**Figma qatlam tartibi:** pill spiker rasmi *ostida*, "+" va strelka *ustida*.<br>Nomer kiritish maydoni yo'q — butun pill CTA havolasi. |
| Orbit | `assets/s3-orbit.webp` `−52, 210` 494×240 (freymdan kengroq, `.page` kesadi) |
| Nuqtalar | 8px `#FFDACE` — `45,297` · `123,268` · `258,267` · `336,296` |

---

## 4. Sozlamalar (`example/<v>/js/config.js`)

| Kalit | Hozirgi qiymat | Izoh |
|---|---|---|
| `ctaUrl` | `https://t.me/ustudy_uz` | **almashtirilishi kerak** — haqiqiy bot havolasi |
| `eventDate` | `2026-09-18T20:00:00+05:00` | ma'lumot uchun |
| `timerMinutes` | `2` | `01:59` dan sanaydi (Figma'dagi raqam) |
| `metrikaId`, `pixelId` | bo'sh | analitika (ixtiyoriy) |

CTA havolasiga `?start=v<variant>_<joy>` qo'shiladi — masalan `start=v2_hero`.
Shu orqali bot tomonda qaysi variant va qaysi tugma ishlagani ko'rinadi.

---

## 5. Tekshirish usuli

```bash
cd /home/erwin/qwertyu/zapusk && python3 -m http.server 8899
# brauzerda: http://localhost:8899/_check/diff.html?v=a
#   difference rejimi — QORA = aynan mos
#   &m=side yonma-yon · &b=4 farqni yorqinlashtirish · &s=0.3 butun sahifa
```

Raqamli tekshiruv (headless Chrome → Figma renderi bilan piksel taqqoslash):
`_check/ref/{a,b,c}.png` — Figma'ning 2x renderi (etalon).

**Oxirgi natija** (o'rtacha farq 0–255 shkalada; 0 = ideal):

| Variant | O'rtacha | >32 farqli piksel |
|---|---|---|
| a | 7.6 | 4.4% |
| b | 7.1 | 4.3% |
| c | 2.4 | 1.5% |

Qolgan farq — joylashuv emas, faqat harf chetlarining silliqlanishi
(Figma va brauzer matnni bir xil rasterlashtirmaydi).

---

## 6. Ish jurnali

### 2026-09-08
- Figma fayldan 3 ta freym o'qildi; barcha rasm va ikonkalar 3x PNG → WebP
  qilib eksport qilindi (`assets/`), vektor ikonkalar SVG.
- Dastlab flex/oqim (flow) layout bilan qurildi → Figma bilan mos kelmadi.
  **Absolyut Figma koordinatalariga** o'tkazildi.
- `zoom` orqali masshtablash olib tashlandi → `<meta viewport width=390>`.
- Shriftlar: Herokid (W Type Foundry, pullik) topildi → SVG konturga o'tildi.
  Karantina asl shrift ekani aniqlandi (Google Fonts'da bor).
- Taymer uchun 6 ta bepul shrift raqamli o'lchovdan o'tkazildi →
  **Bebas Neue** eng yaqini (xato 18.5; keyingi nomzod 32.8).
- Animatsiyalar butunlay olib tashlandi (foydalanuvchi talabi).
- Papka tuzilishi `example/a · b · c` ga o'tkazildi, har biri mustaqil.
- Topilgan va tuzatilgan xatolar:
  - `.btn{width:100%}` + margin → tugmalar chetdan chiqib ketardi
  - `img{max-width:100%}` → orbit va tugma rasmlari kesilardi
  - b: tugma rasmi soyasiz o'lchamda qo'yilgan edi (`350×110` → `380×140`)
  - a: "Hisobot, prezentatsiya…" 4 qatorga tushib ketardi
  - b: sovg'a matni, 01-blok, "…ulguring!" — qator soni noto'g'ri
  - `→` belgisi Google Inter subsetida yo'qligi → mikro-subset joylashtirildi
- Variant c: telefon kiritish maydoni olib tashlandi, Figma pill'i qoldi.
- Taymer 120 → **2 daqiqa**, format `mm:ss` (a/c) va `hh:mm:ss` (b).
- GitHub: https://github.com/thestrak118-web/zapusk (public, `main`).

---

## 7. Keyingi ishlar

- [ ] `ctaUrl` ni haqiqiy Telegram bot havolasiga almashtirish
- [ ] GitHub Pages yoqish (`thestrak118-web.github.io/zapusk/`)
- [ ] Figma tokenni yangilash (chatga ochiq yozilgan edi)
- [ ] Herokid / Buyan `.woff2` topilsa — `base.css` dagi `--font-display` va
      `--font-buyan` boshiga qo'shish, taymer ham asl shriftga o'tadi

## BIR saytlar qo‘shildi

Foydalanuvchi tayyorlangan BIR a/b/c variantlarini ushbu repoga push qilishni so‘radi. Yangi saytlar ildizdagi a/, b/, c/ papkalarida; root index.html ularga yo‘naltirilgan. Oldingi Page 2 example/ fayllari saqlangan. Yangi variantlar foydalanuvchining joriy qoidalariga ko‘ra responsive 425px hero, AVIF, WOFF2 subset va defer JS bilan ishlaydi. Sheets so‘rovi thankYou sahifasida ko‘rinmasdan fonda yuboriladi. Tafsilotlar BIR.md da.
