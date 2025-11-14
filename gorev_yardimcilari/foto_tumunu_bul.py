# gorev_yardimcilari/foto_tumunu_bul.py
import pyautogui
import time
import os

def bul_tumunu(goruntu_tam_yolu, maks_bekleme_saniyesi=10, benzerlik=0.9):
    """
    Belirtilen 'tam yoldaki' görüntünün ekrandaki TÜM örneklerini arar.
    Bir liste olarak tüm merkez konumlarını döndürür.
    Bulamazsa boş bir liste [] döndürür.
    """
    goruntu_adi = os.path.basename(goruntu_tam_yolu)
    
    print(f"[{goruntu_adi}] görüntüsünün TÜM örnekleri ekranda aranıyor (Maks {maks_bekleme_saniyesi} sn)...")
    
    if not os.path.exists(goruntu_tam_yolu):
        print(f"HATA: Görüntü dosyası bulunamadı: {goruntu_tam_yolu}")
        return [] # Boş liste döndür

    baslangic_zamani = time.time()
    while time.time() - baslangic_zamani < maks_bekleme_saniyesi:
        try:
            # locateAllOnScreen bir 'generator' döndürür
            konumlar_generator = pyautogui.locateAllOnScreen(
                goruntu_tam_yolu, 
                confidence=benzerlik,
                grayscale=True
            )
            
            # Konumları bir listeye çevir
            konum_listesi = [pyautogui.center(konum) for konum in konumlar_generator]
            
            if konum_listesi:
                print(f"[{goruntu_adi}] bulundu: {len(konum_listesi)} adet.")
                return konum_listesi
                
        except pyautogui.PyAutoGUIException:
            pass 
        
        time.sleep(0.5)
    
    print(f"BILGI: {maks_bekleme_saniyesi} saniye icinde '{goruntu_adi}' bulunamadı.")
    return [] # Boş liste döndür