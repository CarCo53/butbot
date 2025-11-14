# merkeziguncelleme/merkeziguncelleme.py
# YÖNETİCİ GÖREV MODÜLÜ
# GÜNCELLENDİ: v7 - Tüm 'bilgi_mesaji' beklemeleri merkezi 'islem_bekle'
#               kütüphanesini kullanacak şekilde tamamlandı.

import os
import sys
import time
import pyautogui
from collections import Counter 

# --- Kütüphaneyi Dışarıdan Çağırma ---
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..')
sys.path.append(ANA_PROJE_DIZINI)

try:
    # Mevcut kütüphanelerimiz
    from gorev_yardimcilari import foto_ara_ve_bekle, foto_tikla
    # 'foto_kaybolmasini_bekle' import'u kaldırıldı
    from gorev_yardimcilari.foto_tumunu_bul import bul_tumunu
    from gorev_yardimcilari import popup_sayi_sor
    from gorev_yardimcilari import klavye_ile_sayfaya_git
    
    # --- YENİ KÜTÜPHANE IMPORT'U ---
    from gorev_yardimcilari import islem_bekle
    
except ImportError:
    print("HATA: 'gorev_yardimcilari' kütüphanesi bulunamadı (islem_bekle.py eksik olabilir).")
    sys.exit(1)

try:
    from hane_guncelleme import hane_guncelleme
except ImportError:
    print("HATA: 'hane_guncelleme' modülü bulunamadı.")
    sys.exit(1)
    
try:
    from hatalar import SistemiYenidenBaslatHatasi
except ImportError:
    print("HATA: 'hatalar.py' dosyası ana dizinde bulunamadı.")
    sys.exit(1)

# --- Görüntü Dosyalarının Tam Yolları ---
try:
    from config import ANA_DIZIN
except ImportError:
    print("HATA: config.py bulunamadı.")
    ANA_DIZIN = os.path.join(SCRIPT_DIZINI, '..') 

_GOREV_DIZINI = os.path.join(ANA_DIZIN, "merkeziguncelleme")

IMG_SOSYAL_GUNCEL_OLMAYAN = os.path.join(_GOREV_DIZINI, "sosyal_guncel_olmayan.PNG")
IMG_SOSYAL_ANA_EKRAN = os.path.join(_GOREV_DIZINI, "sosyal_guncel_olmayan_anaekran.PNG")
IMG_ISLEMLER = os.path.join(_GOREV_DIZINI, "islemler.PNG")
IMG_SAYFA_SAYISI_HESAPLA = os.path.join(_GOREV_DIZINI, "sayfa_sayisini_hesapla.PNG")
# IMG_BILGI_MESAJI yolu buradan kaldırıldı (artık config'de)
IMG_SORGULAMA_GIZLE = os.path.join(_GOREV_DIZINI, "Sorgulama_kriterlerini_gizle.PNG")
IMG_HANE = os.path.join(_GOREV_DIZINI, "hane.PNG")
IMG_HANEDEN_CIK = os.path.join(_GOREV_DIZINI, "haneden_cik.PNG")
IMG_SONRAKI = os.path.join(_GOREV_DIZINI, "sonraki.png")
IMG_SAYFAYAGIT = os.path.join(_GOREV_DIZINI, "sayfayagit.png")


def _dongu_baslangic_noktasi():
    """
    ANA HANE DÖNGÜSÜ VE SAYFALAMA
    (Bu fonksiyonda değişiklik yok, v3 ile aynı)
    """
    print("\n-----------------------------------------------------")
    print("Merkezi Guncelleme: ANA HANE DÖNGÜSÜ BAŞLANGIÇ NOKTASI.")
    print("-----------------------------------------------------")
    
    sayfa_numarasi = 1 
    
    while True:
        print(f"\n--- Sayfa {sayfa_numarasi} İşleniyor ---")
        print("Ekranda 'hane.PNG' örnekleri aranıyor...")
        
        tum_haneler = bul_tumunu(IMG_HANE, maks_bekleme_saniyesi=10, benzerlik=0.9)
        
        if not tum_haneler:
            print(f"BILGI: Sayfa {sayfa_numarasi} üzerinde 'hane.PNG' bulunamadı.")
        else:
            print(f"Toplam {len(tum_haneler)} adet ham 'hane.PNG' görüntüsü bulundu.")

        filtrelenmis_haneler = []
        if tum_haneler:
            try:
                x_koordinatlari = [round(konum.x / 5.0) * 5 for konum in tum_haneler]
                x_sayaci = Counter(x_koordinatlari)
                en_sik_x_grupu = x_sayaci.most_common(1)[0][0]
                filtrelenmis_haneler = [konum for konum in tum_haneler if (round(konum.x / 5.0) * 5) == en_sik_x_grupu]
                
                print(f"Filtreleme: Ana sütun X={en_sik_x_grupu} civarı olarak belirlendi.")
                print(f"İşlenecek hane sayısı: {len(filtrelenmis_haneler)}")

            except Exception as e:
                print(f"HATA: Hane X-koordinat filtrelemesi başarısız: {e}")
                return False 
        
        for i, hane_konumu in enumerate(filtrelenmis_haneler):
            print(f"\n--- Hane {i+1}/{len(filtrelenmis_haneler)} (Sayfa {sayfa_numarasi}) işleniyor (Konum: {hane_konumu}) ---")
            
            try:
                print(f"Hane {i+1}'e tıklanıyor...")
                pyautogui.click(int(hane_konumu.x), int(hane_konumu.y))
                time.sleep(1) 

                print("'hane_guncelleme' uzman modülü çağrılıyor...")
                guncelleme_basarili_mi = hane_guncelleme.calistir_hane_guncelleme()
                
                if not guncelleme_basarili_mi:
                    print(f"UYARI: Hane {i+1} güncellenemedi (3 deneme de başarısız oldu).")
                
                print(f"Hane {i+1} için işlem bitti. '{os.path.basename(IMG_HANEDEN_CIK)}' aranıyor...")
                if not foto_tikla.tikla(IMG_HANEDEN_CIK, 
                                         konum="sag_ust", 
                                         maks_bekleme_saniyesi=10, 
                                         offset=10):
                    
                    raise Exception(f"KRİTİK HATA: '{os.path.basename(IMG_HANEDEN_CIK)}' butonu bulunamadı.")
                
                print(f"Hane {i+1}'den çıkıldı (sağ üste tıklandı).")
                time.sleep(1.5)
            
            except SistemiYenidenBaslatHatasi:
                raise # Bu hatayı yakalama, main.py'ye fırlat
            except Exception as e:
                print(f"Hane {i+1} işlenirken KRİTİK HATA: {e}")
                continue
                
        print(f"\n--- Sayfa {sayfa_numarasi} tamamlandı. ---")
        print(f"'{os.path.basename(IMG_SONRAKI)}' butonu aranıyor...")
        
        if foto_tikla.tikla(IMG_SONRAKI, 
                             konum="sol_ust", 
                             maks_bekleme_saniyesi=5,
                             offset=5):
            
            print("Sonraki sayfaya tıklandı. Yeni sayfanın yüklenmesi bekleniyor...")
            sayfa_numarasi += 1
            time.sleep(5) 
            continue
            
        else:
            print("Tüm sayfalar tamamlandı ('sonraki.png' bulunamadı).")
            break 
            
    print("\n--- Tüm Haneler ve Sayfalar İşlendi ---")
    return True

# --- ANA FONKSİYON GÜNCELLENDİ ---
def calistir_merkezi_guncelleme(baslangic_sayisi):
    """
    Merkezi Güncelleme görevinin ana iş akışını yürütür.
    'baslangic_sayisi' parametresi main.py'den gelir.
    """
    print("\n--- GÖREV BAŞLADI: Merkezi Güncelleme ---")
    
    try:
        # Adım 1: 'sosyal_guncel_olmayan.png' tıkla
        if not foto_tikla.tikla(IMG_SOSYAL_GUNCEL_OLMAYAN, maks_bekleme_saniyesi=15):
            raise Exception(f"Başlangıç butonu '{os.path.basename(IMG_SOSYAL_GUNCEL_OLMAYAN)}' bulunamadı.")

        # Adım 2: 'sosyal_guncel_olmayan_anaekran.png' bekle
        if not foto_ara_ve_bekle.ara_ve_bekle(IMG_SOSYAL_ANA_EKRAN, maks_bekleme_saniyesi=20):
            raise Exception(f"Ana ekran '{os.path.basename(IMG_SOSYAL_ANA_EKRAN)}' yüklenmedi.")
        
        # Adım 3: 'islemler.png' tıkla
        if not foto_tikla.tikla(IMG_ISLEMLER, maks_bekleme_saniyesi=10):
            raise Exception(f"İşlemler butonu '{os.path.basename(IMG_ISLEMLER)}' bulunamadı.")
        
        # Adım 4: 'sayfa_sayisini_hesapla.png' tıkla
        print("Sayfa sayısı hesaplanıyor...")
        if not foto_tikla.tikla(IMG_SAYFA_SAYISI_HESAPLA, maks_bekleme_saniyesi=10):
            raise Exception(f"'{os.path.basename(IMG_SAYFA_SAYISI_HESAPLA)}' butonu bulunamadı.")

        # --- DEĞİŞİKLİK 1: Artık merkezi 'islem_bekle' fonksiyonunu çağırıyoruz ---
        print("Sayfa sayısı hesaplama onayı (bilgi mesajı) bekleniyor...")
        # 'ara_ve_kaybolmasini_bekle' çağrısı, 'islem_bekle' ile değiştirildi.
        # Bu, 120sn'lik standart donma kuralını kullanacak.
        islem_bekle.bekle_bilgi_mesaji()
            
        # Adım 6: 'Sorgulama_kriterlerini_gizle.png' tıkla
        if not foto_tikla.tikla(IMG_SORGULAMA_GIZLE, maks_bekleme_saniyesi=10):
            raise Exception(f"'{os.path.basename(IMG_SORGULAMA_GIZLE)}' butonu bulunamadı.")
        time.sleep(1) 

        # Adım 7: (Soru sorma) 'main.py'ye taşınmıştı.
        
        # 1. sayfa/satır için 0 kez, 2. için 1 kez, vb. basılması için
        asagi_ok_sayisi = baslangic_sayisi - 1
        
        # Adım 8: Klavye ile O Sayfaya Git
        print(f"'{os.path.basename(IMG_SAYFAYAGIT)}' kullanılarak {baslangic_sayisi}. sayfaya/satıra gidiliyor...")
        
        # --- DEĞİŞİKLİK 2: 'git' fonksiyonu artık 'img_bilgi_mesaji_yolu' parametresi almıyor ---
        if not klavye_ile_sayfaya_git.git(
            sayfa_numarasi=asagi_ok_sayisi, 
            img_sayfa_git_yolu=IMG_SAYFAYAGIT
        ):
            raise Exception("Klavye ile sayfaya gitme işlemi başarısız oldu.")
        
        # Adım 9: Ana Döngüyü Başlat
        return _dongu_baslangic_noktasi()

    except SistemiYenidenBaslatHatasi:
        raise # Bu hatayı yakalama, main.py'ye fırlat
    except Exception as e:
        print(f"\n---!!! MERKEZI GUNCELLEME KURULUM HATASI !!! ---")
        print(f"Hata: {e}")
        return False