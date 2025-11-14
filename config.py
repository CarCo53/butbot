# config.py
# GÜNCELLENDİ v3: Hibrit Dağıtım Modeli
# İki farklı dizin tanımlar:
# 1. ANA_DIZIN (sys._MEIPASS): .exe'nin içindeki paketlenmiş dosyalar (png, chromedriver)
# 2. EXE_DIZINI (.exe'nin olduğu yer): .exe'nin dışındaki dosyalar (.env, ChromePortable)

import sys
import os

def get_ana_dizin_temp():
    """ 
    .exe'nin içine paketlenen dosyaların (png, chromedriver)
    çalışma zamanında çıkarıldığı GEÇİCİ klasörü bulur.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Program .exe olarak derlenmişse: Geçici klasör ('_MEIPASS')
        return sys._MEIPASS
    else:
        # Program .py script olarak çalışıyorsa (test ortamı)
        # Bu .py dosyasının olduğu ana dizini al.
        return os.path.dirname(os.path.abspath(__file__))

def get_ana_dizin_exe():
    """
    .exe dosyasının KENDİSİNİN bulunduğu kalıcı klasörü bulur.
    .env ve GoogleChromePortable.exe burada aranacak.
    """
    if getattr(sys, 'frozen', False):
        # Program .exe olarak derlenmişse, .exe'nin bulunduğu dizin
        return os.path.dirname(sys.executable)
    else:
        # Program .py script olarak çalışıyorsa (test ortamı)
        # Bu .py dosyasının olduğu ana dizini al.
        return os.path.dirname(os.path.abspath(__file__))

# ANA_DIZIN: .exe'nin İÇİNDEKİLER için (png'ler, chromedriver)
ANA_DIZIN = get_ana_dizin_temp()

# EXE_DIZINI: .exe'nin DIŞINDAKİLER için (.env, GoogleChromePortable.exe)
EXE_DIZINI = get_ana_dizin_exe()