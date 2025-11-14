# gorev_yardimcilari/klavye_ile_sayfaya_git.py
# YENİ YARDIMCI: Belirli bir sayfaya klavye ile (ok tuşları) gider.

import pyautogui
import time
import os
import sys

# --- Kütüphaneyi Dışarıdan Çağırma ---
# Bu script'in, bir üst dizindeki 'hatalar.py' dosyasını bulabilmesi için
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..')
sys.path.append(ANA_PROJE_DIZINI)

try:
    from gorev_yardimcilari import foto_tikla
    from gorev_yardimcilari.foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
except ImportError:
    print("HATA: Gerekli 'gorev_yardimcilari' kütüphaneleri bulunamadı.")
    sys.exit(1)

try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    sys.exit(1)


def git(sayfa_numarasi, img_sayfa_git_yolu, img_bilgi_mesaji_yolu):
    """
    Bir butona tıklar, 'sayfa_numarasi' kadar aşağı ok tuşuna basar,
    Enter'a basar ve bilgi mesajının kaybolmasını bekler.
    
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
            benzerlik=0.80, # İsteğiniz üzerine %80
            maks_bekleme_saniyesi=10,
            offset=5 # Sol üst köşeden 5 piksel içeri
        )
        
        if not basarili_mi:
            print(f"HATA: '{os.path.basename(img_sayfa_git_yolu)}' butonu bulunamadı.")
            return False

        print("Butona tıklandı. 1 saniye bekleniyor...")
        time.sleep(1) # Kullanıcının istediği 1 sn bekleme

        # 2. 'sayfa_numarasi' kadar 'aşağı ok' tuşuna bas
        # (sayfa 1 için hiç basmaması, sayfa 2 için 1 kez basması gerekir)
        # (Bu yüzden 1'den başlatıyoruz)
        if sayfa_numarasi > 0:
            print(f"{sayfa_numarasi} kez 'aşağı ok' tuşuna basılıyor...")
            for i in range(sayfa_numarasi):
                pyautogui.press('down')
                time.sleep(0.05) # Tuş basımları arası çok kısa bir bekleme
        
        # 3. Enter tuşuna bas
        print("Enter tuşuna basılıyor...")
        pyautogui.press('enter')

        # 4. 'bilgi_mesaji.png'nin gelip gitmesini bekle
        print("İşlemin onaylanması (bilgi mesajı) bekleniyor...")
        # 'ara_ve_kaybolmasini_bekle' fonksiyonu, eğer donarsa
        # 'SistemiYenidenBaslatHatasi' fırlatacaktır (zaten istediğimiz şey bu).
        basarili_mi = ara_ve_kaybolmasini_bekle(
            img_bilgi_mesaji_yolu,
            bulmak_icin_maks_bekleme=15,
            kaybolmak_icin_maks_bekleme=15
        )
        
        if not basarili_mi:
            # Bu durumun olmaması lazım (hata fırlatması gerekir),
            # ancak garanti olsun diye ekliyoruz.
            print("HATA: Bilgi mesajı işlemi başarısız oldu.")
            return False
            
        print("Sayfaya başarıyla gidildi.")
        return True

    except SistemiYenidenBaslatHatasi:
        # Bu hatayı yakalama, main.py'ye fırlat
        raise 
    except Exception as e:
        print(f"Klavye ile sayfaya gitme sırasında beklenmedik hata: {e}")
        return False