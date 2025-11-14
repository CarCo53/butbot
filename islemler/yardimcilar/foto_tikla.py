# gorev_yardimcilari/foto_tikla.py
# GÜNCELLENDİ: v2 - Esnek Tıklama Konumları (merkez, sag_ust, vb.)

import pyautogui
import time
import os

def tikla(goruntu_tam_yolu, 
          konum="merkez", 
          maks_bekleme_saniyesi=10, 
          benzerlik=0.9,
          offset=5):
    """
    Bir 'tam yoldaki' görüntüyü ekranda arar ve belirtilen konumuna tıklar.
    Başarılıysa True, bulamazsa False döndürür.

    Args:
        goruntu_tam_yolu (str): Aranan görüntünün tam dosya yolu.
        konum (str, optional): Nereye tıklanacağı. 
            Seçenekler: "merkez" (varsayılan), "sag_ust", "sol_ust", 
                         "sag_alt", "sol_alt".
        maks_bekleme_saniyesi (int, optional): Görüntüyü aramak için maks süre.
        benzerlik (float, optional): Görüntü benzerlik oranı (confidence).
        offset (int, optional): Köşelerden kaç piksel "içeriye" tıklanacağı.
    """
    goruntu_adi = os.path.basename(goruntu_tam_yolu)
    
    if not os.path.exists(goruntu_tam_yolu):
        print(f"HATA: Görüntü dosyası bulunamadı: {goruntu_tam_yolu}")
        return False

    print(f"[{goruntu_adi}] görüntüsü aranıyor (Konum: {konum}, Maks {maks_bekleme_saniyesi} sn)...")
    
    baslangic_zamani = time.time()
    box_konumu = None
    
    # --- Görüntüyü Bulma Döngüsü ---
    # Bu fonksiyon artık 'ara_ve_bekle'yi kullanmıyor, işi kendisi yapıyor.
    while time.time() - baslangic_zamani < maks_bekleme_saniyesi:
        try:
            # locateOnScreen, 'Box(left, top, width, height)' nesnesi döndürür
            box_konumu = pyautogui.locateOnScreen(
                goruntu_tam_yolu, 
                confidence=benzerlik,
                grayscale=True
            )
            if box_konumu:
                print(f"[{goruntu_adi}] bulundu: {box_konumu}")
                break # Görüntü bulundu, döngüden çık
        except pyautogui.PyAutoGUIException:
            pass 
        time.sleep(0.5)
        
    # --- Tıklama Mantığı ---
    if box_konumu:
        # Görüntü bulundu, şimdi nereye tıklayacağımızı hesaplayalım
        x, y = 0, 0
        
        if konum == "merkez":
            # Varsayılan: Merkeze tıkla
            merkez_noktasi = pyautogui.center(box_konumu)
            x = int(merkez_noktasi.x)
            y = int(merkez_noktasi.y)
            
        elif konum == "sag_ust":
            # İsteğiniz: Sağ Üst (offset ile 5 piksel içeride)
            x = int(box_konumu.left + box_konumu.width - offset)
            y = int(box_konumu.top + offset)
            
        elif konum == "sol_ust":
            x = int(box_konumu.left + offset)
            y = int(box_konumu.top + offset)
            
        elif konum == "sag_alt":
            x = int(box_konumu.left + box_konumu.width - offset)
            y = int(box_konumu.top + box_konumu.height - offset)
            
        elif konum == "sol_alt":
            x = int(box_konumu.left + offset)
            y = int(box_konumu.top + box_konumu.height - offset)
            
        else:
            print(f"HATA: Geçersiz konum '{konum}'. Merkeze tıklanacak.")
            merkez_noktasi = pyautogui.center(box_konumu)
            x = int(merkez_noktasi.x)
            y = int(merkez_noktasi.y)

        # Tıklama işlemi
        try:
            print(f"[{goruntu_adi}] görüntüsüne tıklanıyor (Konum: {konum}, Koordinat: {x}, {y})")
            pyautogui.click(x, y)
            return True
        except Exception as e:
            print(f"HATA: Tıklama sırasında hata oluştu: {e}")
            return False
            
    else:
        # Görüntü bulunamadı
        print(f"HATA: Tıklanacak [{goruntu_adi}] görüntüsü {maks_bekleme_saniyesi} saniyede bulunamadı.")
        return False