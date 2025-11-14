# butunlesikgiris.py
# GÜNCELLENDİ v5: Hibrit Dağıtım Modeli
# .env ve GoogleChromePortable 'EXE_DIZINI'nden (dışarıdan)
# chromedriver ve .png'ler 'ANA_DIZIN'den (içeriden/paketten) okunacak.

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

# YENİ: İki farklı dizini de config'den al
try:
    from config import ANA_DIZIN, EXE_DIZINI
except ImportError:
    print("HATA: config.py bulunamadı.")
    sys.exit(1)

try:
    from gorev_yardimcilari.foto_ara_ve_bekle import ara_ve_bekle
except ImportError:
    print("HATA: 'gorev_yardimcilari' kütüphanesi bulunamadı.")
    exit()

# --- Ayarlar (Hibrit Yollara Göre Güncellendi) ---

# 1. PAKETİN İÇİNDEN (ANA_DIZIN = Temp)
DRIVER_YOLU = os.path.join(ANA_DIZIN, "chromedriver.exe")

# 2. .EXE'NİN YANINDAN (EXE_DIZINI = Kalıcı Klasör)
CHROME_EXE_YOLU = os.path.join(EXE_DIZINI, "GoogleChromePortable.exe")
CHROME_BASLATMA_KOMUTU = (
    f'"{CHROME_EXE_YOLU}" '
    r"--remote-debugging-port=9222 "
    r"--allow-outdated-plugins "
    r"--always-authorize-plugins"
)

HEDEFL_URL = "https://butunlesik.aile.gov.tr/VO/LoginPage.jsp"

# Selenium Seçicileri
KULLANICI_ADI_ID = "j_username"
SIFRE_ID = "j_password"
LOGIN_BUTON_NAME = "login"
FLASH_LINK_PARTIAL_TEXT = "Adobe Flash player" 

# 3. PAKETİN İÇİNDEN (ANA_DIZIN = Temp)
IZIN_VER_BUTON_GORSEL = "izin_ver.png" 
ANA_SAYFA_GORSEL = "anasayfaacildi.png" 
ANA_SAYFA_BEKLEME_SURESI = 60

_IZIN_VER_BUTON_YOLU = os.path.join(ANA_DIZIN, IZIN_VER_BUTON_GORSEL)
_ANA_SAYFA_YOLU = os.path.join(ANA_DIZIN, ANA_SAYFA_GORSEL)


def _gizli_verileri_yukle():
    """
    .env dosyasını (.exe'nin yanındaki) 'EXE_DIZINI'nden yükler.
    """
    # DEĞİŞİKLİK: Artık 'EXE_DIZINI' kullanılıyor.
    env_yolu = os.path.join(EXE_DIZINI, ".env")
    
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
    Hangi dosyanın içeride, hangisinin dışarıda olduğunu bilir.
    """
    print("\n--- On Kontroller Baslatiliyor (Hibrit Model) ---")
    
    # 1. Çözünürlük Kontrolü (Esnek)
    guncel_cozunurluk = pyautogui.size()
    print(f"BILGI: Mevcut ekran cozunurlugu: {guncel_cozunurluk}")
    if guncel_cozunurluk not in [(1920, 1080), (1600, 900)]:
        print(f"UYARI: Bot, 1920x1080 veya 1600x900 olmayan bir çözünürlükte çalıştırılıyor.")
    
    # 2. İÇERİDEKİ (Paketlenmiş) Dosyaların Kontrolü (ANA_DIZIN)
    for goruntu_yolu in [_IZIN_VER_BUTON_YOLU, _ANA_SAYFA_YOLU]:
        if not os.path.exists(goruntu_yolu):
            print(f"HATA: (Paket içi) Gerekli '{os.path.basename(goruntu_yolu)}' dosyasi eksik.")
            print(f"Aranan yer: {goruntu_yolu}")
            return False
            
    if not os.path.exists(DRIVER_YOLU):
        print(f"HATA: (Paket içi) 'chromedriver.exe' bulunamadı!")
        print(f"Aranan yer: {DRIVER_YOLU}")
        return False
        
    # 3. DIŞARIDAKİ (.exe'nin yanındaki) Dosyaların Kontrolü (EXE_DIZINI)
    if not os.path.exists(CHROME_EXE_YOLU):
        print(f"HATA: (Dış) 'GoogleChromePortable.exe' bulunamadı!")
        print(f"Aranan yer: {CHROME_EXE_YOLU}")
        return False
        
    env_yolu = os.path.join(EXE_DIZINI, ".env")
    if not os.path.exists(env_yolu):
        print(f"HATA: (Dış) '.env' dosyası bulunamadı!")
        print(f"Aranan yer: {env_yolu}")
        return False
        
    print("On kontroller (iç/dış tüm dosyalar) başarılı.")
    return True

# --- ANA GİRİŞ FONKSİYONU ---
def giris_yap_ve_dogrula():
    """
    Sisteme tam otomatik giriş yapar ve ana sayfanın yüklendiğini doğrular.
    (Bu fonksiyonun iç mantığı, yolları doğru tanımladığımız için değişmedi)
    """
    if not _on_kontrolleri_yap():
        return None, None 

    driver = None 
    browser_process = None 
    
    try:
        # 1. Tarayıcıyı Başlat (Dışarıdaki .exe'yi çağırır)
        print("Giris Modulu: Tarayıcı başlatılıyor...")
        browser_process = subprocess.Popen(CHROME_BASLATMA_KOMUTU, shell=True)
        print(f"Tarayıcı işlemi PID: {browser_process.pid} ile başlatıldı.")
        time.sleep(5) 

        # 2. Selenium ile Bağlan (İçerideki chromedriver'ı kullanır)
        print("Giris Modulu: Selenium bağlanıyor...")
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_service = Service(executable_path=DRIVER_YOLU)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        print("Giris Modulu: Selenium bağlandı.")
        
        # 3. Giriş Adımları (Dışarıdaki .env'den okur)
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

        # 4. Flash Adımları
        flash_linki = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, FLASH_LINK_PARTIAL_TEXT)))
        flash_linki.click()
        print("Giris Modulu: Flash linkine tıklandı.")

        # 5. Pencereyi Öne Getir
        current_title = driver.title 
        browser_windows = gw.getWindowsWithTitle(current_title)
        if browser_windows:
            browser_windows[0].activate() 
            print("Giris Modulu: Tarayıcı öne getirildi.")
            time.sleep(1.0)
        else:
            raise Exception(f"PyAutoGUI hedef pencereyi ('{current_title}') bulamadi.")
        
        # 6. "İzin ver" Butonuna Tıkla (İçerideki .png'yi arar)
        izin_ver_konum = ara_ve_bekle(_IZIN_VER_BUTON_YOLU, maks_bekleme_saniyesi=10)
        
        if izin_ver_konum:
            pyautogui.click(izin_ver_konum)
            print("Giris Modulu: 'Izin ver' butonuna tıklandı.")
        else:
            raise Exception("PyAutoGUI 'Izin ver' butonunu bulamadi.")

        # 7. Ana Sayfayı Doğrula (İçerideki .png'yi arar)
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