# hatalar.py
# Proje genelindeki özel hata sınıflarını tanımlar.

class SistemiYenidenBaslatHatasi(Exception):
    """
    Bot'un kurtarılamaz bir duruma girdiğini 
    ve tüm sürecin (giriş dahil) yeniden başlatılması 
    gerektiğini belirten özel hata.
    """
    pass