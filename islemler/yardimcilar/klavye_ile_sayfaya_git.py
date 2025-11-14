# gorev_yardimcilari/klavye_ile_sayfaya_git.py
# GÜNCELLENDİ v2.1: Standart 120sn bekleme kuralı düzeltildi.
#               'bekle_bilgi_mesaji' çağrısındaki özel süreler kaldırıldı.

import pyautogui
import time
import os
import sys

# --- Kütüphaneyi Dışarıdan Çağırma ---
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..')
sys.path.append(ANA_PROJE_DIZINI)

try:
    from gorev_yardimcilari import foto_tikla
    from gorev_yardimcilari import islem_bekle
except ImportError:
    print("HATA: Gerekli 'gorev_yardimcilari' kütüphaneleri bulunamadı.")
    sys.exit(1)

try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    sys.exit(1)


# Fonksiyon tanımından 'img_bilgi_mesaji_yolu' parametresi kaldırıldı
def git(sayfa_numarasi, img_sayfa_git_yolu):
    """
    Bir butona tıklar, 'sayfa_numarasi' kadar aşağı ok tuşuna basar,
    Enter'a basar ve merkezi 'islem_bekle' fonksiyonunu çağırır.
    
    Başarılı olursa True, olmazsa False döndürür (veya hata fırlatır).
    """
    print(f"\n--- Klavye ile Sayfaya Gitme Görevi Başladı ---")
    print(f"Hedef sayfa (veya satır): {sayfa_numarasi}")
    
    try:
        # 1. 'sayfayagit.png' resmine %80 benzerlikle sol üste tıkla
        print(f"'{os.path.basename(img_sayfa_git_yolu)}' butonu aranıyor...")
        basarili_mi = foto_tikla.tikla(
            img_sayfa_git_yolu,
            konum="sol_ust",
            benzerlik=0.80, 
            maks_bekleme_saniyesi=10,
            offset=5 
        )
        
        if not basarili_mi:
            print(f"HATA: '{os.path.basename(img_sayfa_git_yolu)}' butonu bulunamadı.")
            return False

        print("Butona tıklandı. 1 saniye bekleniyor...")
        time.sleep(1) 

        # 2. 'sayfa_numarasi' kadar 'aşağı ok' tuşuna bas
        if sayfa_numarasi > 0:
            print(f"{sayfa_numarasi} kez 'aşağı ok' tuşuna basılıyor...")
            for i in range(sayfa_numarasi):
                pyautogui.press('down')
                time.sleep(0.05) 
        
        # 3. Enter tuşuna bas
        print("Enter tuşuna basılıyor...")
        pyautogui.press('enter')

        # --- DÜZELTME: Artık standart 120sn kuralını kullanıyor ---
        print("İşlemin onaylanması (bilgi mesajı) bekleniyor...")
        
        # Özel 'maks_bekleme' süreleri kaldırıldı.
        # Bu fonksiyon artık 'islem_bekle.py' içindeki varsayılan 
        # (10sn bulma, 120sn kaybolma) sürelerini kullanacak.
        basarili_mi = islem_bekle.bekle_bilgi_mesaji()
        
        if not basarili_mi:
            print("HATA: Bilgi mesajı işlemi başarısız oldu.")
            return False
            
        print("Sayfaya başarıyla gidildi.")
        return True

    except SistemiYenidenBaslatHatasi:
        raise 
    except Exception as e:
        print(f"Klavye ile sayfaya gitme sırasında beklenmedik hata: {e}")
        return False