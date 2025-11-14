# islemler/yardimcilar/islem_bekle.py
# GÜNCELLENDİ v5: 'islemler/yardimcilar' altındaki yeni yerine uyarlandı.
# 'sys.path' ana dizin yolu (2 seviye yukarı) düzeltildi.

import sys
import os

# --- Gerekli Kütüphaneleri ve Yolları Import Et ---
# 'config.py'yi (ana dizinde) bulmak için sys.path ayarı
try:
    from config import IMG_BILGI_MESAJI_YOLU
except ImportError:
    try:
        # --- GÜNCELLENEN YOL ---
        ANA_PROJE_DIZINI = os.path.join(os.path.dirname(__file__), '..', '..') # 2 seviye yukarı
        sys.path.append(ANA_PROJE_DIZINI)
        from config import IMG_BILGI_MESAJI_YOLU
    except ImportError:
        print("HATA: config.py (IMG_BILGI_MESAJI_YOLU) bulunamadı.")
        sys.exit(1)

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