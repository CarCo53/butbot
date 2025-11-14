# gorev_yardimcilari/foto_birini_bekle.py
import pyautogui
import time
import os

def ara_ve_bul(goruntu_A_yolu, 
               goruntu_B_yolu, 
               maks_bekleme_saniyesi=60, 
               benzerlik=0.75):
    """
    Ekranda iki görüntüden BİRİNİ arar. Hangisini önce bulursa onun
    anahtarını ("A" veya "B") döndürür.
    Süre dolarsa None döndürür.
    """
    goruntu_A_adi = os.path.basename(goruntu_A_yolu)
    goruntu_B_adi = os.path.basename(goruntu_B_yolu)
    
    print(f"Iki hedef aranıyor: '{goruntu_A_adi}' (A) VEYA '{goruntu_B_adi}' (B)")
    print(f"Maksimum bekleme süresi: {maks_bekleme_saniyesi} saniye.")

    baslangic_zamani = time.time()
    while time.time() - baslangic_zamani < maks_bekleme_saniyesi:
        try:
            # Görüntü A'yı ara
            konum_A = pyautogui.locateCenterOnScreen(
                goruntu_A_yolu, 
                confidence=benzerlik,
                grayscale=True
            )
            if konum_A:
                print(f"Hedef A bulundu: '{goruntu_A_adi}'")
                return "A"
                
        except pyautogui.PyAutoGUIException:
            pass # Bulamayınca hata verebilir, normaldir

        try:
            # Görüntü B'yi ara
            konum_B = pyautogui.locateCenterOnScreen(
                goruntu_B_yolu, 
                confidence=benzerlik,
                grayscale=True
            )
            if konum_B:
                print(f"Hedef B bulundu: '{goruntu_B_adi}'")
                return "B"
                
        except pyautogui.PyAutoGUIException:
            pass

        print("Aranıyor (A veya B)...")
        time.sleep(0.5) # Yarım saniyede bir tekrarla
    
    print(f"HATA: {maks_bekleme_saniyesi} saniye icinde iki hedef de (A veya B) bulunamadı.")
    return None