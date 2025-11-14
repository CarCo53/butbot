# islemler/guncellemeler/hane_guncelleme/hane_guncelleme.py
# GÜNCELLENDİ v4: 'islemler' paketi altındaki yeni yerine uyarlandı.
# Tüm importlar ve resim yolları düzeltildi.

import os
import sys
import time
import pyautogui

# --- Kütüphaneyi Dışarıdan Çağırma (Yol Düzeltildi) ---
# Bu dosya artık 'islemler/guncellemeler/hane_guncelleme' içinde
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..', '..', '..') # 3 seviye yukarı
sys.path.append(ANA_PROJE_DIZINI)

try:
    # --- GÜNCELLENEN İMPORT YOLLARI (YARDIMCILAR) ---
    from islemler.yardimcilar import foto_ara_ve_bekle, foto_tikla
    from islemler.yardimcilar.foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
    from islemler.yardimcilar.foto_birini_bekle import ara_ve_bul
    from islemler.yardimcilar import islem_bekle
except ImportError:
    print("HATA: 'islemler/yardimcilar' kütüphanesi bulunamadı.")
    sys.exit(1)

try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    sys.exit(1)

# --- GÜNCELLENEN GÖRÜNTÜ YOLLARI (CONFIG'DEN ALINIYOR) ---
try:
    from config import (
        HG_MERKEZI_GUNCELLE, HG_BILGI_MESAJI, HG_MESAJ, HG_KAPAT,
        HG_SUNUCU_HATA, HG_KAPAT2
    )
except ImportError:
    print("HATA: config.py'den 'HG_' (Hane Güncelleme) yolları okunamadı.")
    sys.exit(1)


def calistir_hane_guncelleme():
    """
    Hane güncelleme işlemini 3 kez deneme mantığıyla çalıştırır.
    (İç mantık değişmedi, sadece yol değişkenleri değişti)
    """
    print("--- Uzman Görev Başladı: Hane Güncelleme (v3 Merkezi Bekleme) ---")
    
    for i in range(3):
        print(f"Hane Güncelleme: Deneme {i+1}/3...")
        
        try:
            # Artık 'config.py'den gelen doğru yolu kullanıyor
            if not foto_tikla.tikla(HG_MERKEZI_GUNCELLE, maks_bekleme_saniyesi=10):
                print("Merkezi güncelleme butonu bulunamadı. Tekrar denenecek...")
                time.sleep(1) 
                continue 

            # Artık merkezi 'islem_bekle' fonksiyonunu çağırıyor
            if not islem_bekle.bekle_bilgi_mesaji(bulmak_icin_maks_bekleme=60, kaybolmak_icin_maks_bekleme=60):
                print("Bilgi mesajı gelmedi veya kaybolmadı. Tekrar denenecek...")
                time.sleep(3)
                continue 

            print("İşlem sonucu bekleniyor ('mesaj.PNG' VEYA 'sunucuda_hata.PNG')...")
            
            gelen_mesaj = ara_ve_bul(
                HG_MESAJ,           # Hedef "A" (Config'den)
                HG_SUNUCU_HATA,     # Hedef "B" (Config'den)
                maks_bekleme_saniyesi=60,
                benzerlik=0.80
            )

            if gelen_mesaj == "A":
                print("Bilgi/Hata mesajı bulundu.")
                foto_tikla.tikla(HG_KAPAT, maks_bekleme_saniyesi=5) # Config'den
                print("Mesaj kapatıldı. Bu hane için işlem sonlandırılıyor.")
                return True 

            elif gelen_mesaj == "B":
                print("Sunucu hatası bulundu.")
                foto_tikla.tikla(HG_KAPAT2, maks_bekleme_saniyesi=5) # Config'den
                print("Sunucu hatası kapatıldı. Tekrar denenecek...")
                time.sleep(3) 
                continue 

            elif gelen_mesaj is None:
                print("KRİTİK HATA: 60 saniyede beklenen mesajlar (mesaj.png, sunucuda_hata.png) gelmedi.")
                raise SistemiYenidenBaslatHatasi("Hane güncelleme ekranı 60 saniyede yanıt vermedi.")

        except SistemiYenidenBaslatHatasi:
             raise 
             
        except Exception as e:
            print(f"Hane Güncelleme Deneme {i+1} HATA: {e}")
            time.sleep(2)
            continue

    print("HATA: 3 deneme de başarısız oldu. Bu hane atlanıyor.")
    return False