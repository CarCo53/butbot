# gorev_yardimcilari/foto_ara_ve_bekle.py
import pyautogui
import time
import os

# --- GÜNCELLEME ---
# Fonksiyon artık 'goruntu_adi' yerine 'goruntu_tam_yolu' alıyor.
def ara_ve_bekle(goruntu_tam_yolu, maks_bekleme_saniyesi=10, benzerlik=0.9):
    """
    Belirtilen 'tam yoldaki' görüntüyü, ekranda arar.
    Bulursa konumunu (merkez x, y) döndürür, bulamazsa None döndürür.
    """
    # Görüntünün adını loglama için yoldan ayıkla
    goruntu_adi = os.path.basename(goruntu_tam_yolu)
    
    print(f"[{goruntu_adi}] görüntüsü ekranda aranıyor (Maks {maks_bekleme_saniyesi} sn)...")
    
    # --- GÜNCELLEME ---
    # Artık 'os.path.join' yapmıyoruz, çünkü yol zaten tam.
    if not os.path.exists(goruntu_tam_yolu):
        print(f"HATA: Görüntü dosyası bulunamadı: {goruntu_tam_yolu}")
        return None

    baslangic_zamani = time.time()
    while time.time() - baslangic_zamani < maks_bekleme_saniyesi:
        try:
            konum = pyautogui.locateCenterOnScreen(
                goruntu_tam_yolu, # <- Değişti
                confidence=benzerlik,
                grayscale=True
            )
            if konum:
                print(f"[{goruntu_adi}] bulundu: {konum}")
                return konum
        except pyautogui.PyAutoGUIException:
            pass 
        
        time.sleep(0.5)
    
    print(f"HATA: {maks_bekleme_saniyesi} saniye icinde '{goruntu_adi}' bulunamadı.")
    return None