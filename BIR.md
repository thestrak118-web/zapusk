# BIR vebinar saytlar

`a/`, `b/`, `c/` — mustaqil variantlar. Har birida HTML, minifikatsiya qilingan CSS, JS, AVIF va lokal WOFF2 mavjud. Root index.html variantlarni solishtirish uchun.

Hero kengligi 425px gacha. Ism va telefon tekshirilgach thankYou.html darhol ochiladi; ariza Google Sheets’ga fonda yuboriladi. Yuklanish va muvaffaqiyat matni ko‘rsatilmaydi. Xatoda qo‘lda qayta yuborish mumkin. Telegram havolasi yangi tabda ochiladi.

Sozlamalar: har bir variantdagi js/config.js. Sheet: Lead. Maydonlar: Ism, Telefon raqam, Royhatdan o'tgan vaqti. Pixel ID va video URL’lari hali berilmagan.

Ariza sessionStorage’da vaqtincha saqlanadi, server tasdig‘idan keyin o‘chiriladi. Joriy server dublikatdan himoyalanmagan: server javobi yo‘qolsa, qayta urinish takror qator yaratishi mumkin.

Tekshiruv: uchala variantda lokal brauzer orqali fon yuborish, xato/qayta urinish, tasdiqdan keyin tozalash, qayta yuklashda takror yubormaslik, qora matn va yashirin yuklanish holati tekshirildi. Oxirgi endpointga bitta sintetik jonli ariza yuborilib server muvaffaqiyatni tasdiqladi. Qator alohida Sheets API orqali o‘qilmadi.

Oldingi uStudy variantlari example/ ichida saqlangan.
