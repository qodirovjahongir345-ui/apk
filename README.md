# O'qish Taymeri — APK qilib qurish yo'riqnomasi

Men bu yerda (sandbox muhitida) haqiqiy APK compile qila olmayman —
buning uchun Android SDK/NDK kerak (bir necha GB), va bu yerning
tarmog'i buni yuklab olishga ruxsat bermaydi. Shuning uchun eng oson
yo'l — GitHub'ning bepul serverlarida (GitHub Actions) qurdirish.
Sizga hech qanday Linux/Android Studio kerak emas, faqat GitHub
akkaunt kifoya.

## 1-usul: GitHub Actions orqali (eng oson, kompyuter kerak emas)

1. github.com'da yangi repository oching (masalan `oqish-taymeri`).
2. Shu papkadagi 3 ta faylni (`main.py`, `buildozer.spec`,
   `.github/workflows/build.yml`) o'sha repoga yuklang (papka
   tuzilishini saqlab qoling — `.github/workflows/build.yml` aynan
   shu joyda turishi kerak).
3. Repo sahifasida "Actions" bo'limiga o'ting — qurilish avtomatik
   boshlanadi (10-20 daqiqa davom etadi).
4. Qurilish tugagach, shu Action ishining sahifasida pastda
   "Artifacts" bo'limidan `oqish-taymeri-apk` faylini yuklab oling —
   ichida tayyor `.apk` bo'ladi.
5. APK'ni telefoningizga ko'chirib, o'rnating (Sozlamalar'da
   "noma'lum manbalardan o'rnatish"ga ruxsat bering).

## 2-usul: O'zingizning kompyuteringizda (Linux/WSL)

```
pip install buildozer cython
buildozer android debug
```

Birinchi marta ishga tushirganda Android SDK/NDK avtomatik yuklab
olinadi (~3-4 GB, uzoq vaqt oladi). Tayyor APK
`bin/oqishtaymeri-1.0-arm64-v8a_armeabi-v7a-debug.apk` yo'lida
paydo bo'ladi.

## O'rnatgandan keyin ESLATMA

APK o'rnatilgandan so'ng, ilova ishlashidan oldin albatta:

**Sozlamalar → Xavfsizlik (yoki Ilovalar) → "App pinning"** ni
yoqib qo'ying. Bu bo'lmasa, ilova ekranni qulflay olmaydi —
bu Android'ning o'zining xavfsizlik cheklovi, uni kod orqali
chetlab o'tib bo'lmaydi.
