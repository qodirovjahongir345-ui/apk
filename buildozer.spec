[app]
title = O'qish Taymeri
package.name = oqishtaymeri
package.domain = org.jahongir

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 1

android.permissions = WAKE_LOCK

# minSDK 21+ tavsiya etiladi, lock task API shu versiyalarda barqaror ishlaydi
android.minapi = 21
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True

# APK arxitekturasi (aksariyat telefonlar uchun ikkalasi ham qamrab olinadi)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
