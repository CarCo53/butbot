# islemler/yardimcilar/foto_kaybolmasini_bekle.py
# GÜNCELLENDİ v5: 'islemler/yardimcilar' altındaki yeni yerine uyarlandı.
# 'sys.path' ana dizin yolu (2 seviye yukarı) düzeltildi.

import pyautogui
import time
import os
import sys

# Kendi kütüphanemizden 'ara_ve_bekle' fonksiyonunu import ediyoruz
# ('.', bu dosya ile aynı klasörde demektir)
from .foto_ara_ve_bekle import ara_ve_bekle

# --- GÜNCELLENEN YOL ---
# Ana dizindeki (hatalar.py) özel hata tanımımızı import ediyoruz
try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    # Eğer .py olarak çalıştırılırsa ve bulamazsa, ana dizini (2 seviye yukarı) eklemeyi dene
    try:
        ANA_PROJE_DIZINI = os.path.join(os.path.dirname(__file__), '..', '..') # <-- DEĞİŞTİ
        sys.path.append(ANA_PROJE_DIZINI)
        from hatalar import SistemiYenidenBaslatHatasi
    except ImportError:
        print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
        sys.exit(1)
# -------------------------


def ara_ve_kaybolmasini_bekle(goruntu_tam_yolu,
                             bulmak_icin_maks_bekleme=10,
                             kaybolmak_icin_maks_bekleme=15,
                             benzerlik=0.9):
    """
    Bir görüntünün önce EKRANA GELMESİNİ, sonra EKRANDAN KAYBOLMASINI bekler.
    Kaybolmazsa (donarsa), 'SistemiYenidenBaslatHatasi' fırlatır.
    (İç mantık değişmedi)
    """
    goruntu_adi = os.path.basename(goruntu_tam_yolu)
    
    print(f"[{goruntu_adi}] görüntüsünün ekrana gelmesi bekleniyor...")
    konum = ara_ve_bekle(goruntu_tam_yolu, maks_bekleme_saniyesi=bulmak_icin_maks_bekleme, benzerlik=benzerlik)
    
    if konum is None:
        print(f"BILGI: [{goruntu_adi}] görüntüsü ilk etapta bulunamadı (Zaten görünür değil).")
        return True 

    print(f"[{goruntu_adi}] görüntüsü bulundu. (1 sn bekle)")
    time.sleep(1)

    print(f"[{goruntu_adi}] görüntüsünün kaybolması bekleniyor (Maks {kaybolmak_icin_maks_bekleme} sn)...")
    baslangic_zamani = time.time()
    
    while time.time() - baslangic_zamani < kaybolmak_icin_maks_bekleme:
        
        konum_hala_var = None 
        try:
            konum_hala_var = pyautogui.locateCenterOnScreen(
                goruntu_tam_yolu,
                confidence=benzerlik,
                grayscale=True
            )
        except Exception:
            konum_hala_var = None 

        if konum_hala_var is None:
            print(f"[{goruntu_adi}] görüntüsü başarıyla kayboldu. (1 sn bekle)")
            time.sleep(1)
            return True
        else:
            print(f"[{goruntu_adi}] hala ekranda, kaybolması bekleniyor...")
            time.sleep(1) 

    print(f"\n---!!! SİSTEM DONMA HATASI !!! ---")
    print(f"HATA: [{goruntu_adi}] görüntüsü {kaybolmak_icin_maks_bekleme} saniye içinde kaybolmadı.")
    raise SistemiYenidenBaslatHatasi(f"{goruntu_adi} ekranda takili kaldi.")