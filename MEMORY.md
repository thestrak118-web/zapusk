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

**Page 1 (logistika kampaniyasi, 2026-09-15)** — boshqa mavzu, boshqa freymlar:

| | |
|---|---|
| Freymlar | `Site 1` (390×1380) → `example/d`<br>`Site 2` (390×1781) → `example/e`<br>`Site 3` (390×1925) → `example/f` |
| Mavzu | Logistika — bepul vebinar, 19-sentyabr, soat 20:00, 10 000$ lik grant |
| Manba fayl | Figma'dan **Export → SVG** (API orqali emas): `Site 1..3.svg` |
| Meta | `tools/variants.json` — sarlavha, tavsif, rang, prefiks |

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

### Page 1 uchun qo'shimcha qoidalar (`example/d · e · f`)

9. **Sahifa qo'lda yozilmaydi.** `index.html` va `css/site.css` ni
   `tools/svg2site.py` Figma SVG'sidan yig'adi. Tahrir kerak bo'lsa —
   generator yoki `tools/variants.json` tuzatiladi, natija emas.
10. **Matn SVG ichida qoladi.** Figma bergan bazaviy chiziq (x/y) aynan
    takrorlanadi — shuning uchun `<br>` bilan qator sanashning hojati yo'q.
    Litsenziyali shrift bepul analogga almashtiriladi (`FONT_SUB`):
    HelveticaNeue → Arimo, Gilroy → Urbanist.
11. **Ro'yxatdan o'tish oynasi sahifada bo'lmaydi.** Integratsiya shartnomasi
    (`logistics-launch/source/integration/README-contract.md`) bo'yicha
    `js/main.js` uni birinchi CTA bosilganda o'zi qo'shadi. Sahifada faqat
    `<button type="button" data-register>` turadi. Modal markupini qo'lda
    qo'yish — shartnoma buzilishi.

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

### Page 1 variantlari — avtomatik yig'ilgan

O'lchamlar generator chiqargan `css/site.css` dan olingan (Figma qiymati).

| | **d** — Site 1 | **e** — Site 2 | **f** — Site 3 |
|---|---|---|---|
| Kanvas | 390×1380 | 390×1781 | 390×1925 |
| Sahifa foni | `#ffffff` | `#000000` | `#ffffff` |
| Asosiy rang (`accent`) | `#3074F0` ko'k | `#E7600F` to'q sariq | `#E91919` qizil |
| `theme-color` | `#367AF7` | `#000000` | `#D40000` |
| CTA 1 | `24,554` 343×82 r41 | `26,538` 338×78 r39 | `23,581` 343×85 r12 |
| CTA 2 | `24,1258` 343×82 r41 | `26,1659` 338×78 r39 | `23,1789` 343×85 r12 |
| Rasm / vektor qatlam | 3 / 4 | 6 / 7 | 7 / 8 |
| `assets/` hajmi | 144 KB | 388 KB | 360 KB |
| Shriftlar | Antonio, Arimo, Bebas Neue, Mulish, Poppins | Antonio, Bebas Neue, Big Shoulders Display, Mulish, Urbanist | Arimo, Bebas Neue, Mulish, Sora |

Umumiy CSS (generator chiqaradi, `base.css` ga bog'liq emas):
`.page{position:relative;width:390px;height:<H>px;margin-inline:auto;overflow:hidden}`,
`.im{position:absolute}` (rasm), `.v{position:absolute;left:0;top:0;pointer-events:none}`
(vektor+matn qatlami — bosishni to'smaydi), `.cta{position:absolute;background:none;
color:transparent}` (Figma shakli ustidagi shaffof tugma).

Ro'yxatdan o'tish oynasi shartnoma uslubi bilan qizil keladi; har bir variant uni
o'z rangiga bo'yaydi — `#registrationModal.homeModal …` (ID li selektor `main.js`
keyinroq qo'shadigan `<style>` dan ustun turadi).

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

### `example/{d,e,f}/js/config.js` — ikkita blok

| Kalit | Qiymat | Izoh |
|---|---|---|
| `LOGISTICS_CONFIG.endpointUrl` | Google Apps Script `.../exec` | lead shu yerga yoziladi |
| `LOGISTICS_CONFIG.telegramUrl` | **bo'sh** | rahmat sahifasidagi kanal tugmasi |
| `LOGISTICS_CONFIG.pixelId` | bo'sh | faqat raqamli ID bo'lsa so'rov ketadi |
| `LOGISTICS_CONFIG.sheetName` | bo'sh | jadval varag'i nomi |
| `SITE_CONFIG.eventDate` | `2026-09-19T20:00:00+05:00` | vebinar sanasi |
| `SITE_CONFIG.timerMinutes` | `2` | sahifada taymer bo'lsa |

`endpointUrl` mijozga ochiq bo'lishi tabiiy — u baribir brauzerga yuklanadi,
sir emas. Eski kampaniyaning havolasi **ko'chirilmaydi** (shartnoma talabi).

Oqim: forma to'ldiriladi → `sessionStorage` ga `webinar.pending:<variant>`
yoziladi → darhol `thankYou.html` ga o'tiladi → POST orqa fonda ketadi.
Sahifadan hech qanday POST yuborilmaydi.

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

### Page 1 variantlari (2026-09-15)

Etalon — Figma'ning 2x PNG eksporti (`Site 1..3.png`), render — headless Chrome
`--force-device-scale-factor=2 --window-size=390,<H>`:

| Variant | O'rtacha | >32 farqli piksel |
|---|---|---|
| d | 2.72 | 1.9% |
| e | 2.46 | 1.9% |
| f | 2.48 | 1.4% |

> `_check/verify.html`, `_check/paste.html` va `_check/figma-p1.json` — d·e·f
> qo'lda yig'ilgan davrdan qolgan yordamchilar. Generator chiqargan sahifalarda
> `data-fig` atributi yo'q, shuning uchun `verify.html` ular uchun ishlamaydi;
> yangi tekshiruv — yuqoridagi piksel taqqoslash va `tools/test_flow.py`.

**Oqim sinovi** — `python3 tools/test_flow.py` (localhost:8899 ishlab turishi kerak).
Uchala variantda 11 tadan tekshiruv: 2 ta CTA, modal boshida yo'qligi, bosilgach
paydo bo'lishi, forma ID lari, `+998`, bo'sh/qisqa raqamda o'tkazmasligi,
to'g'ri ma'lumotda `thankYou.html` ga o'tishi. Sinov paytida `script.google.com`
CDP orqali **bloklanadi** — jadvalga sinov lidi tushmaydi.

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

### 2026-09-15 — logistika kampaniyasi (Page 1), variantlar d · e · f

**Nima qilindi**

- Figma Page 1 dan 3 ta freym **SVG eksport** qilib olindi (API o'rniga —
  matn va vektor geometriyasi aynan keladi).
- `tools/svg2site.py` — SVG'dan 1:1 sayt yig'adigan generator. Rasm to'ldirgan
  shakllar 3x WebP bo'lib chiqariladi, qolgan hamma vektor+matn z-tartibi
  saqlangan holda SVG qatlamlarga bo'linadi.
- `tools/variants.json` + `tools/build.py` — uchala variantni bitta buyruq bilan
  qayta yig'ish: `python3 tools/build.py <svg-papka>`.
- Ro'yxatdan o'tish oqimi `logistics-launch/integration.py` orqali o'rnatildi
  (`js/main.js`, `thankYou.html`, shriftlar). Endpoint `config.js` ga yozildi.
- `tools/test_flow.py` — Selenium bilan oqim sinovi (33 ta tekshiruv, hammasi o'tdi).

**Topilgan va tuzatilgan xatolar**

- *Xotira portlashi (exit 137).* `pattern` ning `objectBoundingBox` koordinatasi
  rasm pikseliga o'girilayotganda ortiqcha `*im.width` bor edi: kesim qutisi
  540000×330000 px chiqib, `pad_for_box` ulkan tuval ajratardi. To'g'risi —
  `px = (u − tx)/a`. Qo'shimcha himoya: 80 MP dan katta tuvalda aniq xato beradi.
- *Sahifa butunlay oq chiqardi.* Generator `.im`/`.v` klasslarini chiqaradi,
  `base.css` esa eski `.n` ni biladi — hech biri `position:absolute` olmagan,
  qatlamlar oqim bo'ylab pastga tizilib ketgan. Joylashuv qoidalari endi
  generatsiya qilinadigan `site.css` ichida (base.css ga bog'liq emas).
- *CTA topilmadi (0 ta).* Detektor gradientli `<rect>` qidirardi, Figma'da tugma
  — `<path>`. Keyin "matnni o'rab turgan eng yaqin guruh" ham ishlamadi: e da
  tugma hero bloki bilan bitta guruhda, chegarasi 389×616 chiqardi. Yakuniy
  yechim — **matn nuqtasini o'z ichiga olgan eng kichik tugmasimon shakl**
  (kengligi ≥200, balandligi 40..160). Uchala variantda 2 tadan CTA topildi.
- *Modal ikki marta.* Generator shabloni modal markupini sahifaga qo'yardi,
  shartnoma esa buni taqiqlaydi (`main.js` o'zi qo'shadi). Shablondan olib
  tashlandi, CTA'lar `<button type="button" data-register>` bo'ldi.
- *Forma tugmasi uchala variantda qizil edi.* `accent` qiymati qo'shildi,
  `#registrationModal.homeModal …` selektori bilan variant rangiga bo'yaladi.
- `install_integration` mavjud `config.js` ni saqlab qoladi — shuning uchun
  `LOGISTICS_CONFIG` va `SITE_CONFIG` bitta faylga birlashtirildi.

**Eslatma:** `example/{d,e,f}` avval qo'lda (absolyut koordinata bilan) yig'ilgan
edi; 2026-09-15 da hammasi generator chiqarganiga almashtirildi.

### 2026-09-15 (kechqurun) — a/b/c ga ko'chirish, tezlik, sozlamalar

**Tuzilma.** Foydalanuvchi: "boshqa saytlar kerakmas, asosiy logistika".
`example/d,e,f` → ildizdagi **`a/ b/ c/`** (variant raqamlari 1/2/3).
BIR (ildizdagi eski a/b/c + css/ + BIR.md), uStudy (`example/a,b,c`) va eski
`_check/` **`arxiv/`** ga ko'chirildi — o'chirilmadi, git tarixida ham bor
(`40c4b78`). Tiklash: `git mv arxiv/bir-a a` yoki `git checkout 40c4b78 -- <yo'l>`.

**Sozlamalar to'ldirildi** (uchala variantda):

| Kalit | Qiymat |
|---|---|
| `endpointUrl` | `AKfycbz7G8GK…/exec` |
| `telegramUrl` | `https://t.me/+GzsmqPGpcew2MjZi` |
| `pixelId` | `2982763675408670` (Meta) |
| `sheetName` | **hali bo'sh — ariza yozilmaydi** |

**Nega "Ariza tasdiqlanmadi" chiqqan.** CORS aybdor emas: endpoint `302` bilan
`script.googleusercontent.com` ga o'tadi, ikkala javobda ham
`access-control-allow-origin: *` bor va JSON qaytadi. Haqiqiy sabab —
`sheetName` yuborilmagan:

```
{"ok":false,"code":"MISSING_SHEET","message":"sheetName parametri yuborilmagan!"}
```

Skript noma'lum varaqni yaratmaydi, `SHEET_NOT_FOUND` qaytaradi — demak nom
aniq bo'lishi kerak. **`sheetName` to'ldirilsa, xato bloki umuman chiqmaydi.**
Uni yashirish kerak emas: u faqat ariza yetib bormaganda ko'rinadi.

**Tezlik** — Lighthouse mobil, ball 0.74–0.83 dan **0.97–0.98** ga chiqdi:

| | oldin | keyin (siqish bilan) |
|---|---|---|
| FCP | 3218–3540 ms | 636–641 ms |
| LCP | 3302–4503 ms | 1508–1802 ms |
| Speed Index | 4574–4708 ms | 636–641 ms |

1. **Google Fonts olib tashlandi** — `render-blocking 2479 ms` shundan edi.
   `tools/localfonts.py` har bir shriftdan faqat sahifadagi harflarni
   `css2?...&text=` orqali oladi (1–5 KB), `fonts/` ga qo'yadi, `@font-face`
   yozadi. Diqqat: subset havolasi `.woff2` bilan tugamaydi (`/l/font?kit=…`).
2. **CSS sahifa ichiga** ko'chirildi — render to'sadigan so'rov qolmadi.
3. **Rasmlar WebP → AVIF** (`AVIF_Q=58`, PIL o'zi kodlaydi, `cwebp` kerak emas)
   va **`SCALE=3` → `2`**. Hero 183 KB → 51 KB. 2x da piksel mosligi ham
   yaxshilandi (etalon ham 2x): a 2.72→2.14, c 2.48→2.22.
4. **LCP rasmi `preload`** qilinadi.
5. Qolgan TBT ~150 ms — Meta Pixel `fbevents.js`. Kerak bo'lsa uni
   `requestIdleCallback` ga o'tkazish mumkin, lekin u umumiy
   `logistics-launch/source/integration/js/pixel.js` faylida — o'zgartirilsa
   boshqa loyihalarga ham ta'sir qiladi.

**Meta eventi.** Foydalanuvchi so'rovi bilan har bir CTA bosilishiga standart
`CompleteRegistration` qo'yildi — shablon ichidagi kichik skript, `[data-register]`
ni capture bosqichida tinglaydi va `fbq` mavjud bo'lsagina chaqiradi.
Brauzerda tekshirildi: uchala variantda 2 tadan CTA, har biri bitta chaqiruv.

> Semantik eslatma: Meta'da `CompleteRegistration` **ro'yxatdan o'tish
> tugallanganini** bildiradi. CTA bosilishiga qo'yilgani uchun formani
> to'ldirmagan odam ham shu eventga tushadi. Kerak bo'lsa uni `thankYou.html`
> ga (`thanks.js` ichida, server tasdig'idan keyin) ko'chirish mumkin —
> o'shanda raqam haqiqiy arizalarni ko'rsatadi.

**`js/app.js` olib tashlandi.** U eski uStudy loyihasidan qolgan taymer skripti
edi; bu uchta sahifada `[data-timer]` element yo'q, ya'ni hech narsa qilmasdi.
Bundan tashqari generator unga havola chiqarardi-yu, `build.py` uni yaratmasdi —
noldan yig'ilgan variantda 404 bo'lardi.

**`FONT_SUB` ishlatilmayotgan ekan.** E'lon qilingan-u, hech qayerda
qo'llanilmagan — shuning uchun CTA yozuvi HelveticaNeue'ni topolmay tasodifiy
fallback bilan chizilardi. Endi qatlam XML'ida almashtiriladi
(HelveticaNeue → Arimo, Gilroy → Urbanist) va yozuv Figma bilan ustma-ust tushadi.

### 2026-09-15 (kech) — ildiz sayti, Sheets ulandi, telefon maydoni

**`a/` asosiy sayt bo'ldi.** `tools/variants.json` ga `"asosiy": "a"` kaliti
qo'shildi; `tools/build.py` har yig'ishdan keyin o'sha variantni ildizga
nusxalaydi (`publish_root`). Qayta yo'naltirish qo'yilmadi — u qo'shimcha
so'rov bo'lib, tezlikka zarar qilardi. Eski solishtirish sahifasi
→ `variantlar.html`.

**Google Sheets nihoyat ulandi.** Foydalanuvchi ketma-ket uchta yangi
deployment yubordi, uchalasi ham bir xil javob berdi:
`{"ok":false,"code":"MISSING_SHEET"}`. Muammo URL'da emas, skript mantig'ida —
`sheetName` majburiy. Varaq nomi **`Lead`** ekani bitta so'rov bilan aniqlandi:

```
{"ok":true,"message":"Ma'lumot qabul qilindi","sheet":"Lead"}
```

Brauzerda to'liq oqim tekshirildi (Sheets bloklanmagan holda): forma →
`thankYou.html` → orqa fonda POST → tasdiq. **Xato bloki endi chiqmaydi.**
Jadvalda 2 ta `TEST-CLAUDE-OCHIRING` qatori qoldi — o'chirilishi kerak.

| Kalit | Yakuniy qiymat |
|---|---|
| `endpointUrl` | `AKfycby6Ihnk…/exec` (uchinchi deployment) |
| `sheetName` | `Lead` |
| `telegramUrl` | `https://t.me/+GzsmqPGpcew2MjZi` |
| `pixelId` | `2982763675408670` |

**Telefon maydoni.** Foydalanuvchi: "raqamdan oshiqcha son yozilmasligi kerak".
Tekshirildi — 10-chi raqam aslida kiritilmayotgan edi (`beforeinput` to'xtatadi),
lekin birga qizil xato chiqardi va shu chalkashtirardi. Endi limitdan oshgan
raqam **jimgina** e'tiborsiz qoldiriladi; qo'yib yuborilgan (paste) noto'g'ri
raqam uchun tushuntirish saqlanib qoldi. O'zgarish umumiy
`logistics-launch/source/integration/js/main.js` da — boshqa loyihalarga ham
tegishli.

**Favikon** `data:` URI sifatida sahifa ichida — har sahifada ketayotgan
`favicon.ico` 404 so'rovi yo'qoldi.

### 2026-09-15 (tun) — Vercel'dagi PSI natijasi va Meta Pixel

Foydalanuvchi saytni `zapusk-beta.vercel.app` ga chiqarib, PageSpeed Insights
o'lchadi: `/` 84, `/b/` 81, `/c/` 98. Lokal o'lchovda 0.98 edi — farq real
tarmoq kechikishi va PSI simulyatsiyasidan.

**Sabab — Meta Pixel.** Jonli saytning to'lqin diagrammasi:

```
0.6 -> 331ms   HTML (8.3 KB)
349 -> 580ms   hamma rasm, shrift, config.js, main.js   <- o'z fayllarimiz tugadi
564 -> 1005ms  fbevents.js           107.8 KB  (tashqi)
1047 -> 1237ms tracking so'rovi       80.6 KB  (tashqi)
```

`observedLargestContentfulPaint` = **1517 ms**, ya'ni sahifa aslida 1.5 s da
bo'yalgan. Lekin Lighthouse simulyatsiyasi qo'shimcha 188 KB va ~190 ms asosiy
oqim bandligini hisobga olib, LCP ni **3771 ms** deb ko'rsatadi.

**Yechim.** `pixel.js` qayta yozildi: `fbq` darhol yaratiladi va chaqiruvlarni
navbatga yig'adi (`init`, `PageView`, CTA dagi `CompleteRegistration`),
kutubxonaning o'zi esa quyidagilardan birinchisida yuklanadi:

- foydalanuvchi sahifaga tegsa — `pointerdown`, `keydown`, `touchstart`,
  **`scroll`**, `mousemove` (lendingda odam deyarli doim tez skrol qiladi);
- hech kim tegmasa — `load` dan **3.5 s** keyin.

Kutubxona yuklangach navbat o'ynatiladi, shuning uchun hech bir event
yo'qolmaydi. Brauzerda tekshirildi: 1 s da `fbevents` so'rovi yo'q, skroldan
keyin darhol paydo bo'ladi, navbatda uchala chaqiruv turadi.

**Natija** (lokal, siqish bilan): uchala variant ham **1.00**, TBT 180–230 ms
dan **0 ms** ga tushdi.

> `pixel.js` umumiy fayl (`logistics-launch/source/integration/js/pixel.js`) —
> o'zgarish shu integratsiyani ishlatadigan boshqa loyihalarga ham tegishli.

### 2026-09-15 (tun, davomi) — PSI 100, srcset va kesh

Piksel kechiktirilgandan keyin Vercel'dagi PSI: `/b/` va `/c/` — **100/100/100/100**
(Performance, Accessibility, Best Practices, SEO), TBT 0 ms. Ildiz `/` — 99;
sabab nuqson emas, o'sha o'lchovdagi tarmoq tebranishi (FCP 1.45 s → 0.96).

**`srcset` qo'shildi.** Har bir rasm endi ikki o'lchamda chiqadi: `nom.avif` (1x)
va `nom@2x.avif`. Sahifada `srcset="… 1x, … 2x"`, LCP rasmining `preload` ida
`imagesrcset`.

> Lighthouse `image-delivery-insight` ni baribir ko'rsatadi: uning mobil
> emulyatsiyasi DPR **2.625** bilan ishlaydi, ya'ni 2x faylni yuklaydi, keyin
> uni CSS piksel bilan solishtirib "ortiqcha" deb belgilaydi. Bu diagnostika,
> **ballga kirmaydi** (ball 1.00). 1x ga tushirish faqat telefonda rasmni
> xiralashtiradi — shuning uchun qilinmadi. Foyda retina bo'lmagan ekranlarda:
> ular endi yarim hajm yuklaydi.

**`vercel.json`** qo'shildi — rasm/shrift uchun `max-age=86400` +
`stale-while-revalidate=604800`, JS uchun 1 soat. `immutable` qo'yilmadi:
fayl nomlari yig'ishlar orasida o'zgarmaydi, aks holda dizayn yangilangach
eski rasm keshda qotib qolardi.

Piksel mosligi o'zgarmadi (a 2.14 / b 2.55 / c 2.22) — retina baribir 2x oladi.

### 2026-09-15 (tun, 3) — ball nega tebranardi

Foydalanuvchi Vercel loyihasini `logistika-vebinarg.vercel.app` deb qayta
nomladi va PSI'ni qayta ishga tushirdi: `/c/` **100** (TBT 0), `/b/` esa
**89** (TBT **410 ms**) — bir xil kodda, bir xil daqiqada.

**Sabab.** Piksel triggerlari ro'yxatida `scroll` bor edi. Lighthouse audit
davomida sahifani o'zi pastga suradi (lazy-load va to'liq skrinshot uchun) —
shu skrol `fbevents.js` ni yuklab yuborardi va u aynan o'lchov oynasiga
tushib qolardi. Tushish-tushmasligi tasodifga bog'liq edi, shuning uchun
ball 100 va 89 orasida sakrardi. Oldingi "100" natijalar omadli o'lchov edi.

**Tuzatish.** `scroll` va `mousemove` triggerlardan olib tashlandi — faqat
haqiqiy niyat belgilari qoldi (`pointerdown`, `keydown`, `touchstart`).
Zaxira taymer 3.5 s dan **10 s** ga uzaytirildi: o'lchov oynasidan ancha
keyin, lekin sahifani o'qiyotgan odam baribir sanaladi. Tugmani bosgan odam
esa darhol.

Tekshirildi: skrol pikselni qo'zg'atmaydi, bosish darhol qo'zg'atadi, navbatda
`init` + `PageView` + `CompleteRegistration` saqlanadi. `/b/` uch marta
ketma-ket o'lchandi — har safar **1.00, TBT 0 ms**, audit davomida `fbevents`
so'rovi umuman yo'q.

> Savdo tomoni: hech narsaga tegmay, 10 soniyadan tez chiqib ketgan odam
> `PageView` ga tushmaydi. Retargeting auditoriyasi shu qadar torayadi.
> Konversiya eventi (`CompleteRegistration`) esa bosishni talab qilgani uchun
> to'liq saqlanadi.

### 2026-09-15 (tun, 4) — qatlam chegaralari va desktop ko'rinishi

**Speed Index tekshiruvi.** Foydalanuvchi "tezlik 0.8" deganda **Speed Index**ni
nazarda tutgan ekan (ball emas). Jonli o'lchovda SI 2.5–3.9 s chiqdi. Kadrlar
(filmstrip) ajratib olinganda ma'lum bo'ldi: sahifa **1.5 s gacha butunlay
bo'sh**, keyin 1875 ms da hammasi bir zumda paydo bo'ladi. Ya'ni shrift yoki
rasm kechikmayapti — **birinchi bo'yalishning o'zi** kechikadi.

Tekshirilgan va rad etilgan taxminlar:
- *Blur filtrlari* — markupda `filter=url(...)` atigi 2 marta ishlatilgan
  (32 ta `<filter>` ta'rifi Figma eksportidan qolgan, ishlatilmaydi).
  Ularni olib tashlash hech narsa o'zgartirmadi.
- *Shrift almashishi* — shriftlar 686 ms da yetib keladi, FCP esa 950 ms;
  almashish bo'yalishdan oldin tugaydi.
- *Asosiy oqim* — jami 0.3 s (Style & Layout 144 ms).

**Qatlam chegaralari.** Har bir vektor qatlam butun sahifa balandligida edi
(c da 8 ta qatlam × 390×1925). Endi har biri faqat o'z mazmuni sig'adigan
qutida: `viewBox` va `width/height` shu quti bo'yicha, joylashuv esa
`.page>svg.v:nth-of-type(N){left;top}` orqali. Chegara `shape_bbox` va
`text_bbox` (taxminiy, 70 px zaxira bilan) birlashmasidan olinadi.
Piksel mosligi o'zgarmadi: 2.17 / 2.59 / 2.23.

**Desktop ko'rinishi.** Foydalanuvchi sahifaning yon tomonida qora chiziq
borligini ko'rsatdi. Tekshiruv: bu **faqat kompyuterda** ko'rinadi —
telefonda `<meta viewport width=390>` kanvasni ekranga moslaydi (375 px da
masshtab 0.96, 360 px da 0.92), desktop brauzer esa bu meta'ni umuman
e'tiborsiz qoldiradi va 390 px lik ustun keng ekran o'rtasida qolib ketadi.

Yechim — faqat keng ekranlar uchun `zoom` (layoutga ta'sir qiladi, balandlik
o'zi to'g'rilanadi): 480 px dan 1.15, 640 px dan 1.3, 900 px dan 1.45.
390 px dan tor desktop oynasi uchun 0.92 — avval u yerda kontent kesilardi.
Mobil ko'rinish tegilmadi.

### 2026-09-15 (tun, 5) — a tugma shakli, b sovg'a rasmi

**a (va ildiz): tugma chetida "ramka".** Figma SVG eksportida CTA `<path>` —
yon tomonlari 3 px tashqariga bo'rtgan "bochka" shakl. Pastki soya (`dy=5`)
bo'rtmani kuzatmaydi, shuning uchun chap/o'ng chetda zinapoya paydo bo'lib,
ramkaga o'xshardi. Avval `<rect rx=12>` bilan yopildi, keyin foydalanuvchi
Figma'dan tugma fonini rasm qilib berdi: `assets/button.avif` (515×131 — 343×87
tugma+soyaning 1.5x eksporti; `a/assets/` da nusxasi). Endi SVG'dagi tugma
shakli, uning `filter[01]_di` va `paint[23]` ta'riflari o'chirilgan; fon —
`<img class="im cta-bg1|cta-bg2">` (`24,554` va `24,1258`, 343×87.33), yozuv
qatlami (`svg.v` 3-chi) **undan keyin** turadi, shuning uchun yozuv va strelka
rasm ustida. `.cta-1/.cta-2` radiusi 12 (41 generatorning `h/2` taxmini edi).
c da tugma `rect` — tegilmadi.

**b: sovg'a rasmi.** Foydalanuvchi `b/assets/gift.png` (204×161) yukladi — bu
kartochka o'ng qismining (136×107) 1.5x eksporti. AVIF: `gift.avif` 136×107
(2.9 KB) va `gift@1.5x.avif` (4.7 KB), `.i22` → `228,638` 136×107. Eski
`s2-03*.avif` o'chirildi.

**Meta eventlari.** `CompleteRegistration` endi tugma bosilganda emas (modal
ochilishi har bosishda sanalardi), **ariza qoldirilgach** `js/thanks.js` da
yuboriladi: yaroqli `webinar.pending` bo'lsa, bir ariza uchun bir marta
(`webinar.tracked:<yo'l>`), `eventID` = ariza ID. Sheets javobi kutilmaydi —
Telegram tugmasini tez bosgan odamning eventi yo'qolmasin. `thankYou.html` da
pixel endi `<head>` dagi Meta standart kodi (kechiktirilmaydi, `pixel.js`
ulanmaydi). Landing stubiga `push` va `_fbq` qo'shildi ("conflicting versions"
ogohlantirishi yo'qoldi). CTA inline skripti `index.html` lardan va
`tools/svg2site.py` shablonidan olib tashlandi.
Sinov (4 variant): landing `PageView` 1 · CTA dan keyin event yo'q · thankYou
`PageView` 1 + `CompleteRegistration` 1 · qayta yuklashda takrorlanmaydi.
> Sinov eslatmasi: headless Playwright'da Meta **hech narsa yubormaydi**
> (`navigator.webdriver`), standart kod ham. `--disable-blink-features=AutomationControlled`
> + `webdriver=false` bilan o'lchash kerak, `/tr` va Sheets `route` bilan ushlanadi.

> ⚠️ Ikkalasi ham **generator chiqargan faylda qo'lda** tuzatildi (manba SVG
> repoda yo'q). `tools/build.py` qayta ishga tushirilsa, qaytib ketadi —
> oldin manba SVG'da tugmani va sovg'a rasmini tuzatish kerak.

---

## 7. Keyingi ishlar

- [ ] Jadvaldan 2 ta `TEST-CLAUDE-OCHIRING` sinov qatorini o'chirish
- [ ] GitHub Pages yoqish (`thestrak118-web.github.io/zapusk/`)
- [x] Meta `CompleteRegistration` CTA bosilishidan ariza qoldirilgandan keyinga
      ko'chirildi (2026-09-15, pastdagi "eventlar" yozuvi)
- [ ] Ildiz va `a/` bir xil sahifa (ikkita manzil). Domen ma'lum bo'lgach
      `a/` ga `canonical` qo'yish kerak bo'lishi mumkin
- [ ] Figma tokenni yangilash (chatga ochiq yozilgan edi)
- [ ] CTA yozuvi Figma'da HelveticaNeue Bold — hozir Arimo bilan almashtirilgan,
      renderda biroz ingichkaroq chiqadi. Litsenziyali `.woff2` topilsa
      `FONT_SUB` dan olib tashlanadi.
- [ ] Herokid / Buyan `.woff2` topilsa — `base.css` dagi `--font-display` va
      `--font-buyan` boshiga qo'shish, taymer ham asl shriftga o'tadi

## BIR saytlar qo‘shildi

Foydalanuvchi tayyorlangan BIR a/b/c variantlarini ushbu repoga push qilishni so‘radi. Yangi saytlar ildizdagi a/, b/, c/ papkalarida; root index.html ularga yo‘naltirilgan. Oldingi Page 2 example/ fayllari saqlangan. Yangi variantlar foydalanuvchining joriy qoidalariga ko‘ra responsive 425px hero, AVIF, WOFF2 subset va defer JS bilan ishlaydi. Sheets so‘rovi thankYou sahifasida ko‘rinmasdan fonda yuboriladi. Tafsilotlar BIR.md da.
