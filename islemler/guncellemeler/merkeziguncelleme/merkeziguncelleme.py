# islemler/guncellemeler/merkeziguncelleme/merkeziguncelleme.py
# YÖNETİCİ GÖREV MODÜLÜ
# GÜNCELLENDİ: v8 - 'islemler' paketi altındaki yeni yerine uyarlandı.
#               Tüm importlar ve resim yolları düzeltildi.

import os
import sys
import time
import pyautogui
from collections import Counter 

# --- Kütüphaneyi Dışarıdan Çağırma (Yol Düzeltildi) ---
# Bu dosya artık 'islemler/guncellemeler/merkeziguncelleme' içinde
SCRIPT_DIZINI = os.path.dirname(__file__)
ANA_PROJE_DIZINI = os.path.join(SCRIPT_DIZINI, '..', '..', '..') # 3 seviye yukarı
sys.path.append(ANA_PROJE_DIZINI)

# --- GÜNCELLENEN İMPORT YOLLARI ---
try:
    # 1. Yardımcı Modüller (yeni 'yardimcilar' yolu)
    from islemler.yardimcilar import foto_ara_ve_bekle, foto_tikla
    from islemler.yardimcilar.foto_kaybolmasini_bekle import ara_ve_kaybolmasini_bekle
    from islemler.yardimcilar.foto_tumunu_bul import bul_tumunu
    from islemler.yardimcilar import popup_sayi_sor
    from islemler.yardimcilar import klavye_ile_sayfaya_git
    from islemler.yardimcilar import islem_bekle
    
    # 2. Kardeş Görev Modülü (guncellemeler altında)
    from islemler.guncellemeler.hane_guncelleme import hane_guncelleme
    
    # 3. Kök Modüller (Ana dizinden)
    from hatalar import SistemiYenidenBaslatHatasi
    
    # 4. Config (Tüm resim yolları için)
    from config import (
        MG_SOSYAL_GUNCEL_OLMAYAN, MG_SOSYAL_ANA_EKRAN, MG_ISLEMLER,
        MG_SAYFA_SAYISI_HESAPLA, MG_SORGULAMA_GIZLE, MG_HANE,
        MG_HANEDEN_CIK, MG_SONRAKI, MG_SAYFAYAGIT
    )
    
except ImportError as e:
    print(f"HATA: 'merkeziguncelleme' başlatılırken import hatası: {e}")
    print("     Lütfen 'islemler' klasör yapısını ve __init__.py dosyalarını kontrol edin.")
    sys.exit(1)
# ------------------------------------


# --- Görüntü Dosyalarının Tam Yolları ---
# (Tüm yerel IMG_... tanımlamaları kaldırıldı, artık config'den geliyorlar)


def _dongu_baslangic_noktasi():
    """
    ANA HANE DÖNGÜSÜ VE SAYFALAMA
    (İç mantık değişmedi, sadece yol değişkenleri değişti)
    """
    print("\n-----------------------------------------------------")
    print("Merkezi Guncelleme: ANA HANE DÖNGÜSÜ BAŞLANGIÇ NOKTASI.")
    print("-----------------------------------------------------")
    
    sayfa_numarasi = 1 
    
    while True:
        print(f"\n--- Sayfa {sayfa_numarasi} İşleniyor ---")
        print("Ekranda 'hane.PNG' örnekleri aranıyor...")
        
        tum_haneler = bul_tumunu(MG_HANE, maks_bekleme_saniyesi=10, benzerlik=0.9)
        
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
                
                print(f"Hane {i+1} için işlem bitti. '{os.path.basename(MG_HANEDEN_CIK)}' aranıyor...")
                if not foto_tikla.tikla(MG_HANEDEN_CIK, 
                                         konum="sag_ust", 
                                         maks_bekleme_saniyesi=10, 
                                         offset=10):
                    
                    raise Exception(f"KRİTİK HATA: '{os.path.basename(MG_HANEDEN_CIK)}' butonu bulunamadı.")
                
                print(f"Hane {i+1}'den çıkıldı (sağ üste tıklandı).")
                time.sleep(1.5)
            
            except SistemiYenidenBaslatHatasi:
                raise # Bu hatayı yakalama, main.py'ye fırlat
            except Exception as e:
                print(f"Hane {i+1} işlenirken KRİTİK HATA: {e}")
                continue
                
        print(f"\n--- Sayfa {sayfa_numarasi} tamamlandı. ---")
        print(f"'{os.path.basename(MG_SONRAKI)}' butonu aranıyor...")
        
        if foto_tikla.tikla(MG_SONRAKI, 
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
        if not foto_tikla.tikla(MG_SOSYAL_GUNCEL_OLMAYAN, maks_bekleme_saniyesi=15):
            raise Exception(f"Başlangıç butonu '{os.path.basename(MG_SOSYAL_GUNCEL_OLMAYAN)}' bulunamadı.")

        # Adım 2: 'sosyal_guncel_olmayan_anaekran.png' bekle
        if not foto_ara_ve_bekle.ara_ve_bekle(MG_SOSYAL_ANA_EKRAN, maks_bekleme_saniyesi=20):
            raise Exception(f"Ana ekran '{os.path.basename(MG_SOSYAL_ANA_EKRAN)}' yüklenmedi.")
        
        # Adım 3: 'islemler.png' tıkla
        if not foto_tikla.tikla(MG_ISLEMLER, maks_bekleme_saniyesi=10):
            raise Exception(f"İşlemler butonu '{os.path.basename(MG_ISLEMLER)}' bulunamadı.")
        
        # Adım 4: 'sayfa_sayisini_hesapla.png' tıkla
        print("Sayfa sayısı hesaplanıyor...")
        if not foto_tikla.tikla(MG_SAYFA_SAYISI_HESAPLA, maks_bekleme_saniyesi=10):
            raise Exception(f"'{os.path.basename(MG_SAYFA_SAYISI_HESAPLA)}' butonu bulunamadı.")

        # Adım 5: Merkezi 'islem_bekle' fonksiyonunu çağır
        print("Sayfa sayısı hesaplama onayı (bilgi mesajı) bekleniyor...")
        islem_bekle.bekle_bilgi_mesaji() # 120sn standart kuralını kullanır
            
        # Adım 6: 'Sorgulama_kriterlerini_gizle.png' tıkla
        if not foto_tikla.tikla(MG_SORGULAMA_GIZLE, maks_bekleme_saniyesi=10):
            raise Exception(f"'{os.path.basename(MG_SORGULAMA_GIZLE)}' butonu bulunamadı.")
        time.sleep(1) 

        # Adım 7: (Soru sorma) 'main.py'ye taşınmıştı.
        
        asagi_ok_sayisi = baslangic_sayisi - 1
        
        # Adım 8: Klavye ile O Sayfaya Git
        print(f"'{os.path.basename(MG_SAYFAYAGIT)}' kullanılarak {baslangic_sayisi}. sayfaya/satıra gidiliyor...")
        
        if not klavye_ile_sayfaya_git.git(
            sayfa_numarasi=asagi_ok_sayisi, 
            img_sayfa_git_yolu=MG_SAYFAYAGIT
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