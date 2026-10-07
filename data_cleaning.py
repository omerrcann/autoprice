import pandas as pd
import re

df = pd.read_csv("zengin_arac_verisi.csv")
print(f"--- Ham Zengin Veri Yüklendi ({len(df)} Satır) ---")

def son_sayiyi_bul(metin):
    if pd.isna(metin):
        return None
    metin_noktasiz = str(metin).replace('.', '')
    sayilar = re.findall(r'\d+', metin_noktasiz)
    if sayilar:
        return int(sayilar[-1])
    return None

df['Fiyat'] = df['Fiyat'].apply(son_sayiyi_bul)
df['Kilometre'] = df['Kilometre'].apply(son_sayiyi_bul)
df['Yil'] = df['Yil'].apply(son_sayiyi_bul)

df = df.dropna(subset=['Fiyat', 'Kilometre', 'Yil', 'Marka', 'Seri', 'Model', 'Vites', 'Yakit'])
df['Fiyat'] = df['Fiyat'].astype(int)
df['Kilometre'] = df['Kilometre'].astype(int)
df['Yil'] = df['Yil'].astype(int)
df = df[(df['Fiyat'] > 200000) & (df['Fiyat'] < 5000000)]
df = df[(df['Kilometre'] > 1000) & (df['Kilometre'] < 400000)]

print("\n--- Temizleme Sonrası İlk 5 Satır ---")
print(df.head())

df.to_csv("temiz_zengin_veri.csv", index=False, encoding="utf-8-sig")
print(f"\nVeri temizleme tamamlandı! Hatalı ilanlar silindikten sonra {len(df)} geçerli satır 'temiz_zengin_veri.csv' olarak kaydedildi.")