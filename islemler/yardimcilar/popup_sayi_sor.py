# gorev_yardimcilari/popup_sayi_sor.py
# YENİ YARDIMCI: Kullanıcıya 'prompt' penceresi gösterir ve sayı alır.

import pyautogui

def sor(baslik, metin, varsayilan_deger="1"):
    """
    Kullanıcıya bir soru sormak için bir popup penceresi gösterir.
    Girişi alır ve sayıya (int) dönüştürerek döndürür.
    
    Kullanım:
    sayfa_numarasi = sor(
        baslik="Sayfa Numarası", 
        metin="Kaçıncı sayfadan başlamak istiyorsunuz?"
    )
    """
    print(f"Kullanıcıya popup gösteriliyor: '{metin}'")
    
    try:
        # PyAutoGUI'nin 'prompt' fonksiyonunu kullan
        girilen_deger = pyautogui.prompt(
            text=metin, 
            title=baslik, 
            default=varsayilan_deger
        )
        
        if girilen_deger is None:
            # Kullanıcı 'İptal'e bastı
            print(f"Kullanıcı 'İptal'e bastı. Varsayılan ({varsayilan_deger}) kullanılacak.")
            return int(varsayilan_deger)
            
        # Girilen değerin bir sayı olduğundan emin ol
        girilen_sayi = int(girilen_deger.strip())
        
        print(f"Kullanıcı '{girilen_sayi}' değerini girdi.")
        return girilen_sayi

    except (ValueError, TypeError):
        # Kullanıcı 'abc' gibi geçersiz bir metin girdi
        print(f"Geçersiz giriş. Varsayılan ({varsayilan_deger}) kullanılacak.")
        return int(varsayilan_deger)
    except Exception as e:
        print(f"Popup gösterilirken hata oluştu: {e}. Varsayılan ({varsayilan_deger}) kullanılacak.")
        return int(varsayilan_deger)