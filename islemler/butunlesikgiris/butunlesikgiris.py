# islemler/butunlesikgiris/butunlesikgiris.py
# GÜNCELLENDİ: v10 - Kök dizini (2 seviye yukarı) sys.path'e ekleme düzeltmesi yapıldı.

import os
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

try:
    import pyautogui
    import pygetwindow as gw
except ImportError:
    print("HATA: 'pip install pyautogui pygetwindow' ile kütüphaneleri kurun.")
    exit()

# --- DÜZELTME: Kök Dizini sys.path'e ekle ---
try:
    # Bu dosyanın bulunduğu dizinden 2 seviye yukarı çık (kök dizine)
    ANA_PROJE_DIZINI = os.path.join(os.path.dirname(__file__), '..', '..')
    if ANA_PROJE_DIZINI not in sys.path:
        sys.path.append(ANA_PROJE_DIZINI)
    
    # Artık kök dizindeki modülleri import edebiliriz
    from config import (
        DRIVER_YOLU_PAKETLI, CHROME_EXE_YOLU_DIS, ENV_YOLU_DIS,
        BG_IZIN_VER_YOLU, BG_ANASAYFA_YOLU
    )
    # Ve 'islemler' paketindeki diğer modülleri
    from islemler.yardimcilar.foto_ara_ve_bekle import ara_ve_bekle
    
except ImportError as e:
    print(f"HATA: 'butunlesikgiris' başlatılırken import hatası: {e}")
    print("     Kök dizin (config.py'nin olduğu yer) yola eklenemedi.")
    sys.exit(1)
# --- Düzeltme Sonu ---


# --- Ayarlar (config'den geliyor, değişiklik yok) ---
CHROME_BASLATMA_KOMUTU = (
    f'"{CHROME_EXE_YOLU_DIS}" '
    r"--remote-debugging-port=9222 "
    r"--allow-outdated-plugins "
    r"--always-authorize-plugins "
    r"--incognito"
)
HEDEFL_URL = "https://butunlesik.aile.gov.tr/VO/LoginPage.jsp"
KULLANICI_ADI_ID = "j_username"
SIFRE_ID = "j_password"
LOGIN_BUTON_NAME = "login"
FLASH_LINK_PARTIAL_TEXT = "Adobe Flash player" 
ANA_SAYFA_BEKLEME_SURESI = 60
_IZIN_VER_BUTON_YOLU = BG_IZIN_VER_YOLU
_ANA_SAYFA_YOLU = BG_ANASAYFA_YOLU


def _gizli_verileri_yukle():
    """
    .env dosyasını 'EXE_DIZINI'nden yükler.
    (Bu fonksiyon değişmedi)
    """
    env_yolu = ENV_YOLU_DIS
    if not os.path.exists(env_yolu):
        print(f"HATA: .env dosyası bulunamadı! .exe'nin yanına kopyalayın.")
        print(f"Aranan yer: {env_yolu}")
        return None
    load_dotenv(dotenv_path=env_yolu)
    kullanici_adi = os.environ.get("IS_YERI_KULLANICI_ADI")
    sifre = os.environ.get("IS_YERI_SIFRE")
    if not kullanici_adi or not sifre:
        print("HATA: .env dosyasında kimlik bilgisi eksik.")
        return None
    return {"kullanici_adi": kullanici_adi, "sifre": sifre}

def _on_kontrolleri_yap():
    """
    Script'in çalışması için temel kontrolleri yapar.
    (Bu fonksiyon değişmedi)
    """
    print("\n--- On Kontroller Baslatiliyor (Hibrit Model) ---")
    
    guncel_cozunurluk = pyautogui.size()
    print(f"BILGI: Mevcut ekran cozunurlugu: {guncel_cozunurluk}")
    if guncel_cozunurluk not in [(1920, 1080), (1600, 900)]:
        print(f"UYARI: Bot, 1920x1080 veya 1600x900 olmayan bir çözünürlükte çalıştırılıyor.")
    
    for goruntu_yolu in [_IZIN_VER_BUTON_YOLU, _ANA_SAYFA_YOLU]:
        if not os.path.exists(goruntu_yolu):
            print(f"HATA: (Paket içi) Gerekli '{os.path.basename(goruntu_yolu)}' dosyasi eksik.")
            print(f"Aranan yer: {goruntu_yolu}")
            return False
            
    if not os.path.exists(DRIVER_YOLU_PAKETLI):
        print(f"HATA: (Paket içi) 'chromedriver.exe' bulunamadı!")
        print(f"Aranan yer: {DRIVER_YOLU_PAKETLI}")
        return False
        
    if not os.path.exists(CHROME_EXE_YOLU_DIS):
        print(f"HATA: (Dış) 'GoogleChromePortable.exe' bulunamadı!")
        print(f"Aranan yer: {CHROME_EXE_YOLU_DIS}")
        return False
        
    if not os.path.exists(ENV_YOLU_DIS):
        print(f"HATA: (Dış) '.env' dosyası bulunamadı!")
        print(f"Aranan yer: {ENV_YOLU_DIS}")
        return False
        
    print("On kontroller (iç/dış tüm dosyalar) başarılı.")
    return True

def giris_yap_ve_dogrula():
    """
    Sisteme tam otomatik giriş yapar ve ana sayfanın yüklendiğini doğrular.
    (Bu fonksiyonun iç mantığı değişmedi)
    """
    if not _on_kontrolleri_yap():
        return None, None 

    driver = None 
    browser_process = None 
    
    try:
        print("Giris Modulu: Tarayıcı başlatılıyor (Gizli Modda)...")
        browser_process = subprocess.Popen(CHROME_BASLATMA_KOMUTU, shell=True)
        print(f"Tarayıcı işlemi PID: {browser_process.pid} ile başlatıldı.")
        time.sleep(5) 

        print("Giris Modulu: Selenium bağlanıyor...")
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_service = Service(executable_path=DRIVER_YOLU_PAKETLI)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        print("Giris Modulu: Selenium bağlandı.")
        
        driver.get(HEDEFL_URL)
        kimlik_bilgileri = _gizli_verileri_yukle()
        if kimlik_bilgileri is None: raise Exception("Kimlik bilgileri okunamadi.")
        
        wait = WebDriverWait(driver, 10)
        kullanici_adi_kutusu = wait.until(EC.visibility_of_element_located((By.ID, KULLANICI_ADI_ID)))
        kullanici_adi_kutusu.send_keys(kimlik_bilgileri["kullanici_adi"])
        sifre_kutusu = wait.until(EC.presence_of_element_located((By.ID, SIFRE_ID)))
        sifre_kutusu.send_keys(kimlik_bilgileri["sifre"])
        login_butonu = wait.until(EC.element_to_be_clickable((By.NAME, LOGIN_BUTON_NAME)))
        login_butonu.click()
        wait.until(EC.staleness_of(login_butonu))
        print("Giris Modulu: Login yapıldı, sayfa yenilendi.")

        flash_linki = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, FLASH_LINK_PARTIAL_TEXT)))
        flash_linki.click()
        print("Giris Modulu: Flash linkine tıklandı.")

        current_title = driver.title 
        browser_windows = gw.getWindowsWithTitle(current_title)
        if browser_windows:
            browser_windows[0].activate() 
            print("Giris Modulu: Tarayıcı öne getirildi.")
            time.sleep(1.0)
        else:
            raise Exception(f"PyAutoGUI hedef pencereyi ('{current_title}') bulamadi.")
        
        izin_ver_konum = ara_ve_bekle(_IZIN_VER_BUTON_YOLU, maks_bekleme_saniyesi=10)
        
        if izin_ver_konum:
            pyautogui.click(izin_ver_konum)
            print("Giris Modulu: 'Izin ver' butonuna tıklandı.")
        else:
            raise Exception("PyAutoGUI 'Izin ver' butonunu bulamadi.")

        ana_sayfa_konum = ara_ve_bekle(_ANA_SAYFA_YOLU, maks_bekleme_saniyesi=ANA_SAYFA_BEKLEME_SURESI)
        
        if ana_sayfa_konum:
            print("\n--- GIRIS MODULU BASARILI ---")
            return driver, browser_process
        else:
            raise Exception("Ana sayfa 1 dakika icinde yuklenemedi.")

    except Exception as e:
        print(f"\n---!!! GIRIS MODULU HATASI !!! ---")
        print(f"Hata: {e}")
        if browser_process:
            print("Hata nedeniyle tarayıcı sonlandırılıyor...")
            browser_process.terminate()
        return None, None