# islemler/yardimcilar/islem_bekle.py
# GÜNCELLENDİ v10: Kök dizini (2 seviye yukarı) sys.path'e ekleme düzeltmesi yapıldı.

import sys
import os

# --- DÜZELTME: Kök Dizini sys.path'e ekle ---
try:
    # Bu dosyanın bulunduğu dizinden 2 seviye yukarı çık (kök dizine)
    ANA_PROJE_DIZINI = os.path.join(os.path.dirname(__file__), '..', '..')
    if ANA_PROJE_DIZINI not in sys.path:
        sys.path.append(ANA_PROJE_DIZINI)
    from config import IMG_BILGI_MESAJI_YOLU
except ImportError:
    print("HATA: config.py (IMG_BILGI_MESAJI_YOLU) bulunamadı.")
    sys.exit(1)
# --- Düzeltme Sonu ---

try:
    # Kendi kütüphanemizdeki (aynı klasördeki) ana bekleme fonksiyonunu import et
    from .foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
except ImportError:
    print("HATA: 'foto_kaybolmasini_bekle.py' kütüphanesi bulunamadı.")
    sys.exit(1)


def bekle_bilgi_mesaji(bulmak_icin_maks_bekleme=10, 
                         kaybolmak_icin_maks_bekleme=120, 
                         benzerlik=0.9):
    """
    Proje genelindeki 'bilgi_mesaji.PNG'nin gelmesini ve gitmesini bekler.
    
    Varsayılan 'kaybolma' süresi 120 saniyedir.
    (Bu fonksiyonun iç mantığı değişmedi)
    """
    
    print("--- Merkezi Bilgi Mesajı Bekleniyor ---")
    
    return ara_ve_kaybolmasini_bekle(
        goruntu_tam_yolu=IMG_BILGI_MESAJI_YOLU,
        bulmak_icin_maks_bekleme=bulmak_icin_maks_bekleme,
        kaybolmak_icin_maks_bekleme=kaybolmak_icin_maks_bekleme,
        benzerlik=benzerlik
    )
