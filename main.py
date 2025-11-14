# main.py
# ANA ORKESTRA ŞEFİ v4
# GÜNCELLENDİ: Artık başlangıç sayfasını SADECE BİR KEZ sorar
# ve bu bilgiyi 'global' bir değişken olarak saklar.

import time
import os
import subprocess
import butunlesikgiris 

from merkeziguncelleme import merkeziguncelleme

try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    exit()

# --- YENİ IMPORT: Soru sorma sorumluluğu artık 'main'de ---
try:
    from gorev_yardimcilari import popup_sayi_sor
except ImportError:
    print("HATA: 'popup_sayi_sor' kütüphanesi bulunamadı.")
    exit()


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

# --- YENİ FONKSİYON: Kullanıcıdan Girdiyi Sadece Bir Kez Al ---
def _kullanicidan_baslangic_sayfasini_iste():
    """
    Program ilk açıldığında kullanıcıya başlangıç sayfasını sorar.
    Geçerli bir sayı (1 veya daha büyük) alana kadar tekrar deneyebilir
    (veya varsayılanı kullanır).
    """
    print("Kullanıcıdan başlanacak sayfa/satır numarası isteniyor...")
    
    baslangic_sayisi = popup_sayi_sor.sor(
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
    
    # --- DEĞİŞİKLİK: Soru sorma işlemi 'while' döngüsünün DIŞINA alındı ---
    # Bu kod, program boyunca SADECE BİR KEZ çalışacak.
    try:
        global_baslangic_sayisi = _kullanicidan_baslangic_sayfasini_iste()
    except Exception as e:
        print(f"Popup alınırken kritik hata: {e}. Varsayılan 1 olarak ayarlandı.")
        global_baslangic_sayisi = 1

    
    # --- Yeniden Başlatma Döngüsü ---
    while True:
        driver = None
        browser_process = None
        
        try:
            # --- GÖREV 1: GİRİŞ YAP ---
            print("\n--- Döngü Adımı: Giriş Modülü Çağrılıyor ---")
            driver, browser_process = butunlesikgiris.giris_yap_ve_dogrula()
            
            if driver is None or browser_process is None:
                print("Ana Program: Giriş modülü başarısız oldu. 1dk bekleyip tekrar denenecek.")
                time.sleep(60)
                continue 

            print("\n--- Ana Program: Giriş Başarılı. Görevler başlıyor... ---")
            
            # --- GÖREV 2: MERKEZİ GÜNCELLEME ---
            # --- DEĞİŞİKLİK: Hafızadaki 'global_baslangic_sayisi' parametre olarak aktarılıyor ---
            print(f"Merkezi Güncelleme modülü, {global_baslangic_sayisi}. sayfadan başlayacak şekilde çağrılıyor...")
            gorev_basarili_mi = merkeziguncelleme.calistir_merkezi_guncelleme(
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