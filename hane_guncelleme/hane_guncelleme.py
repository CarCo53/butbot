# hane_guncelleme/hane_guncelleme.py
# YENİ UZMAN GÖREV MODÜLÜ v2
# GÜNCELLENDİ v2.2: 'ara_ve_bul' için benzerlik eşiği 0.80'e düşürüldü.

import os
import sys
import time
import pyautogui

# --- Kütüphaneyi Dışarıdan Çağırma ---
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..')
sys.path.append(ANA_PROJE_DIZINI)

try:
    from gorev_yardimcilari import foto_ara_ve_bekle, foto_tikla
    from gorev_yardimcilari.foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
    from gorev_yardimcilari.foto_birini_bekle import ara_ve_bul
except ImportError:
    print("HATA: 'gorev_yardimcilari' kütüphanesi bulunamadı.")
    sys.exit(1)

try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    sys.exit(1)


# --- Görüntü Dosyalarının Tam Yolları (Dosya listenize göre) ---
IMG_MERKEZI_GUNCELLE = os.path.join(SCRIPT_DIZINI, "Merkezi_guncelle.PNG")
IMG_BILGI_MESAJI = os.path.join(SCRIPT_DIZINI, "bilgi_mesaji.PNG")
IMG_MESAJ = os.path.join(SCRIPT_DIZINI, "mesaj.PNG")
IMG_KAPAT = os.path.join(SCRIPT_DIZINI, "kapat.PNG")
IMG_SUNUCU_HATA = os.path.join(SCRIPT_DIZINI, "sunucuda_hata.PNG")
IMG_KAPAT2 = os.path.join(SCRIPT_DIZINI, "kapat2.PNG")

def calistir_hane_guncelleme():
    """
    Hane güncelleme işlemini 3 kez deneme mantığıyla çalıştırır.
    İşlem 60sn yanıt vermezse 'SistemiYenidenBaslatHatasi' fırlatır.
    """
    print("--- Uzman Görev Başladı: Hane Güncelleme (v2 Hata Yönetimi) ---")
    
    # 3 kez deneme döngüsü
    for i in range(3):
        print(f"Hane Güncelleme: Deneme {i+1}/3...")
        
        try:
            if not foto_tikla.tikla(IMG_MERKEZI_GUNCELLE, maks_bekleme_saniyesi=10):
                print("Merkezi güncelleme butonu bulunamadı. Tekrar denenecek...")
                time.sleep(1) 
                continue 

            if not ara_ve_kaybolmasini_bekle(IMG_BILGI_MESAJI, bulmak_icin_maks_bekleme=60, kaybolmak_icin_maks_bekleme=60):
                print("Bilgi mesajı gelmedi veya kaybolmadı. Tekrar denenecek...")
                time.sleep(3)
                continue 

            print("İşlem sonucu bekleniyor ('mesaj.PNG' VEYA 'sunucuda_hata.PNG')...")
            
            # --- ANA DÜZELTME BURADA ---
            # Testiniz 83% bulduğu için, eşiği 85%'ten 80%'e çekiyoruz.
            gelen_mesaj = ara_ve_bul(
                IMG_MESAJ,           # Hedef "A"
                IMG_SUNUCU_HATA,     # Hedef "B"
                maks_bekleme_saniyesi=60,
                benzerlik=0.80  # <-- DEĞİŞİKLİK (0.85 idi)
            )

            if gelen_mesaj == "A":
                print("Bilgi/Hata mesajı bulundu.")
                foto_tikla.tikla(IMG_KAPAT, maks_bekleme_saniyesi=5)
                print("Mesaj kapatıldı. Bu hane için işlem sonlandırılıyor.")
                return True 

            elif gelen_mesaj == "B":
                print("Sunucu hatası bulundu.")
                foto_tikla.tikla(IMG_KAPAT2, maks_bekleme_saniyesi=5)
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