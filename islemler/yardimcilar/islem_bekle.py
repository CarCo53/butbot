# gorev_yardimcilari/islem_bekle.py
# YENİ KÜTÜPHANE: Proje genelindeki 'bilgi_mesaji.PNG' bekleme
#                 işlemini merkezileştirir.

import sys
import os

# --- Gerekli Kütüphaneleri ve Yolları Import Et ---
try:
    # 'config.py'den merkezi 'bilgi mesajı' yolunu al
    from config import IMG_BILGI_MESAJI_YOLU
except ImportError:
    # (Bu try/except bloğu, .py olarak çalışırken yolları bulamazsa diye
    # ana dizini sys.path'e ekler)
    try:
        ANA_PROJE_DIZINI = os.path.join(os.path.dirname(__file__), '..')
        sys.path.append(ANA_PROJE_DIZINI)
        from config import IMG_BILGI_MESAJI_YOLU
    except ImportError:
        print("HATA: config.py (IMG_BILGI_MESAJI_YOLU) bulunamadı.")
        sys.exit(1)

try:
    # Kendi kütüphanemizdeki ana bekleme fonksiyonunu import et
    from .foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
except ImportError:
    print("HATA: 'foto_kaybolmasini_bekle.py' kütüphanesi bulunamadı.")
    sys.exit(1)


def bekle_bilgi_mesaji(bulmak_icin_maks_bekleme=10, 
                         kaybolmak_icin_maks_bekleme=120, 
                         benzerlik=0.9):
    """
    Proje genelindeki 'bilgi_mesaji.PNG'nin gelmesini ve gitmesini bekler.
    
    Varsayılan 'kaybolma' süresi, kullanıcı isteği üzerine 120 saniyedir
    (120 saniye içinde kaybolmazsa 'SistemiYenidenBaslatHatasi' fırlatır).
    
    Not: Bu fonksiyonun parametreleri, özel durumlar için (örn: daha hızlı 
    bekleme gereken bir yer) override edilebilir.
    """
    
    print("--- Merkezi Bilgi Mesajı Bekleniyor ---")
    
    # 'ara_ve_kaybolmasini_bekle' fonksiyonunu
    # 'config.py'den gelen merkezi yol ile çağır
    return ara_ve_kaybolmasini_bekle(
        goruntu_tam_yolu=IMG_BILGI_MESAJI_YOLU,
        bulmak_icin_maks_bekleme=bulmak_icin_maks_bekleme,
        kaybolmak_icin_maks_bekleme=kaybolmak_icin_maks_bekleme,
        benzerlik=benzerlik
    )