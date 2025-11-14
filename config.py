# config.py
# GÜNCELLENDİ v5: Tüm proje 'islemler' paketi altına taşındı.
# Tüm modüllerin (giriş, güncelleme, yardımcılar)
# tam yolları artık burada merkezi olarak tanımlanıyor.

import sys
import os

def get_ana_dizin_temp():
    """ 
    .exe'nin içine paketlenen dosyaların (png, chromedriver)
    çalışma zamanında çıkarıldığı GEÇİCİ klasörü bulur.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        # .py olarak çalışırken, bu dosyanın olduğu ana dizini al
        return os.path.dirname(os.path.abspath(__file__))

def get_ana_dizin_exe():
    """
    .exe dosyasının KENDİSİNİN bulunduğu kalıcı klasörü bulur.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# ANA_DIZIN: .exe'nin İÇİNDEKİLER için (png'ler, chromedriver, tüm .pyc'ler)
ANA_DIZIN = get_ana_dizin_temp()

# EXE_DIZINI: .exe'nin DIŞINDAKİLER için (.env, GoogleChromePortable.exe)
EXE_DIZINI = get_ana_dizin_exe()

# --- Dış (EXE Yanı) Dosyalar ---
CHROME_EXE_YOLU_DIS = os.path.join(EXE_DIZINI, "GoogleChromePortable.exe")
ENV_YOLU_DIS = os.path.join(EXE_DIZINI, ".env")

# --- İç (Paketlenmiş) Dosyalar ---
DRIVER_YOLU_PAKETLI = os.path.join(ANA_DIZIN, "chromedriver.exe")

# --- 'islemler' Paket Yolları (KODUN ÇALIŞMA DİZİNİ) ---
ISLEMLER_DIZINI = os.path.join(ANA_DIZIN, "islemler")

# 'yardimcilar' Yolları
YARDIMCILAR_DIZINI = os.path.join(ISLEMLER_DIZINI, "yardimcilar")
# (Yardımcıların kendi yolları yok, sadece fonksiyonları var)

# 'butunlesikgiris' Yolları
BG_DIZINI = os.path.join(ISLEMLER_DIZINI, "butunlesikgiris")
BG_IZIN_VER_YOLU = os.path.join(BG_DIZINI, "izin_ver.png")
BG_ANASAYFA_YOLU = os.path.join(BG_DIZINI, "anasayfaacildi.PNG")

# 'guncellemeler' Yolları
GUNCELLEMELER_DIZINI = os.path.join(ISLEMLER_DIZINI, "guncellemeler")

# 'merkeziguncelleme' Resim Yolları
MG_DIZINI = os.path.join(GUNCELLEMELER_DIZINI, "merkeziguncelleme")
MG_SOSYAL_GUNCEL_OLMAYAN = os.path.join(MG_DIZINI, "sosyal_guncel_olmayan.PNG")
MG_SOSYAL_ANA_EKRAN = os.path.join(MG_DIZINI, "sosyal_guncel_olmayan_anaekran.PNG")
MG_ISLEMLER = os.path.join(MG_DIZINI, "islemler.PNG")
MG_SAYFA_SAYISI_HESAPLA = os.path.join(MG_DIZINI, "sayfa_sayisini_hesapla.PNG")
MG_SORGULAMA_GIZLE = os.path.join(MG_DIZINI, "Sorgulama_kriterlerini_gizle.PNG")
MG_HANE = os.path.join(MG_DIZINI, "hane.PNG")
MG_HANEDEN_CIK = os.path.join(MG_DIZINI, "haneden_cik.PNG")
MG_SONRAKI = os.path.join(MG_DIZINI, "sonraki.PNG")
MG_SAYFAYAGIT = os.path.join(MG_DIZINI, "sayfayagit.PNG")
MG_BILGI_MESAJI = os.path.join(MG_DIZINI, "bilgi_mesaji.PNG")

# 'hane_guncelleme' Resim Yolları (HATAYI ÇÖZECEK YER)
HG_DIZINI = os.path.join(GUNCELLEMELER_DIZINI, "hane_guncelleme")
HG_MERKEZI_GUNCELLE = os.path.join(HG_DIZINI, "Merkezi_guncelle.PNG")
HG_BILGI_MESAJI = os.path.join(HG_DIZINI, "bilgi_mesaji.PNG")
HG_MESAJ = os.path.join(HG_DIZINI, "mesaj.PNG")
HG_KAPAT = os.path.join(HG_DIZINI, "kapat.PNG")
HG_SUNUCU_HATA = os.path.join(HG_DIZINI, "sunucuda_hata.PNG")
HG_KAPAT2 = os.path.join(HG_DIZINI, "kapat2.PNG")

# --- Merkezi (Paylaşılan) Yollar ---
# 'islem_bekle' kütüphanesinin kullanacağı yol
# (merkezi güncellemedekini ana olarak kullanıyoruz)
IMG_BILGI_MESAJI_YOLU = MG_BILGI_MESAJI