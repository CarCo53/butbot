# main.py
# ANA ORKESTRA ŞEFİ v8
# GÜNCELLENDİ: Tüm importlar 'islemler' paket yapısına
#               uyacak şekilde güncellendi.

import time
import os
import subprocess
import sys 

# --- GÜNCELLENEN İMPORT YOLLARI ---
try:
    # 1. Giriş Modülü
    from islemler.butunlesikgiris.butunlesikgiris import giris_yap_ve_dogrula
    
    # 2. Görev Modülü
    from islemler.guncellemeler.merkeziguncelleme.merkeziguncelleme import calistir_merkezi_guncelleme
    
    # 3. Yardımcı Modül (Popup)
    from islemler.yardimcilar.popup_sayi_sor import sor as popup_sor
    
    # 4. Kök Modüller (Ana dizinde oldukları için yolları değişmedi)
    from hatalar import SistemiYenidenBaslatHatasi
    
except ImportError as e:
    print(f"HATA: Gerekli bir modül import edilemedi: {e}")
    print("Tüm modülleri 'islemler' klasörü altına taşıdığınızdan")
    print("ve __init__.py dosyalarını eklediğinizden emin olun.")
    
    # Hata durumunda loglama (Derlenmiş .exe için)
    try:
        from config import EXE_DIZINI
        log_path = os.path.join(EXE_DIZINI, "hata_logu.txt")
        with open(log_path, "a") as f:
            f.write(f"IMPORT HATASI: {e}\n")
    except Exception:
        pass # config'i bile bulamazsa yapacak bir şey yok
        
    os.system("pause")
    sys.exit(1)
# ------------------------------------


def _force_kill_chrome_processes():
    """
    Tüm 'zombi' chrome ve chromedriver işlemlerini zorla sonlandırır.
    (Bu fonksiyon değişmedi)
    """
    print("Agresif Temizlik: Tüm 'chrome.exe' ve 'chromedriver.exe' işlemleri sonlandırılıyor...")
    try:
        subprocess.run("taskkill /F /IM chrome.exe", shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM chromedriver.exe", shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Agresif Temizlik tamamlandı.")
    except Exception as e:
        print(f"Agresif Temizlik sırasında hata (sorun değil): {e}")

def _kullanicidan_baslangic_sayfasini_iste():
    """
    Program ilk açıldığında kullanıcıya başlangıç sayfasını sorar.
    """
    print("Kullanıcıdan başlanacak sayfa/satır numarası isteniyor...")
    
    # --- DEĞİŞİKLİK: Doğrudan import edilen 'sor' fonksiyonu çağrılıyor ---
    baslangic_sayisi = popup_sor(
        baslik="Görev Başlangıcı",
        metin="Kaçıncı sayfadan/satırdan başlamak istiyorsunuz? (1'den başlayarak)"
    )
    
    if baslangic_sayisi < 1:
        print(f"Geçersiz giriş ({baslangic_sayisi}). Varsayılan olarak 1'den başlanacak.")
        baslangic_sayisi = 1
        
    print(f"Global Başlangıç Sayfası {baslangic_sayisi} olarak ayarlandı.")
    return baslangic_sayisi


def ana_program():
    print(">>> ANA PROGRAM BAŞLATILDI (Yeniden Başlatma Döngüsü Aktif) <<<")
    
    try:
        global_baslangic_sayisi = _kullanicidan_baslangic_sayfasini_iste()
    except Exception as e:
        print(f"Popup alınırken kritik hata: {e}. Varsayılan 1 olarak ayarlandı.")
        global_baslangic_sayisi = 1

    
    while True:
        driver = None
        browser_process = None
        
        try:
            # --- GÖREV 1: GİRİŞ YAP ---
            print("\n--- Döngü Adımı: Giriş Modülü Çağrılıyor ---")
            
            driver, browser_process = giris_yap_ve_dogrula()
            
            if driver is None or browser_process is None:
                print("Ana Program: Giriş modülü başarısız oldu. 1dk bekleyip tekrar denenecek.")
                time.sleep(60)
                continue 

            print("\n--- Ana Program: Giriş Başarılı. Görevler başlıyor... ---")
            
            print(f"Merkezi Güncelleme modülü, {global_baslangic_sayisi}. sayfadan başlayacak şekilde çağrılıyor...")
            
            # --- DEĞİŞİKLİK: Doğrudan import edilen 'calistir_merkezi_guncelleme' çağrılıyor ---
            gorev_basarili_mi = calistir_merkezi_guncelleme(
                baslangic_sayisi=global_baslangic_sayisi
            )
            
            if not gorev_basarili_mi:
                raise Exception("Ana Program: Merkezi Güncelleme görevi başarısız oldu.")
                
            print("\n--- TÜM GÖREVLER BAŞARIYLA TAMAMLANDI ---")
            print("Program normal şekilde sonlanıyor.")
            break 

        except SistemiYenidenBaslatHatasi as e:
            print("\n---!!! KRİTİK HATA: YENİDEN BAŞLATMA ALINDI !!! ---")
            print(f"Hata Sebebi: {e}")
            print("Sistem (main.py kapanmadan) 5 saniye içinde yeniden başlatılacak...")
            print(f"(Bir sonraki denemede yine {global_baslangic_sayisi}. sayfadan başlanacak.)")
            time.sleep(5)
            continue 

        except Exception as e:
            print(f"\n---!!! BEKLENMEDİK ANA PROGRAM HATASI !!! ---")
            print(f"İş akışında beklenmedik bir hata oluştu: {e}")
            print("Program tamamen durduruluyor.")
            break 
        
        finally:
            print("\n>>> DÖNGÜ SONU TEMİZLİK <<<")
            if browser_process:
                print(f"Başlatıcı (PID: {browser_process.pid}) sonlandırılıyor...")
                browser_process.terminate()
            _force_kill_chrome_processes()
            print("Temizlik tamamlandı. Döngü devam ediyor...")

# --- Programı Başlat ---
if __name__ == "__main__":
    ana_program()