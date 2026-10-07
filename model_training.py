import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

df = pd.read_csv("temiz_zengin_veri.csv")

X = df[['Marka', 'Seri', 'Model', 'Yil', 'Kilometre', 'Vites', 'Yakit']]
y = df['Fiyat']

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Zenginleştirilmiş model eğitiliyor, lütfen bekleyin...")
model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n--- Zengin Model Performansı ---")
print(f"R2 Skoru: {r2:.3f}")
print(f"Ortalama Tahmin Hatası (RMSE): {rmse:,.0f} TL")

joblib.dump(model, "arac_fiyat_modeli_zengin.pkl")
joblib.dump(list(X.columns), "model_sutunlari_zengin.pkl")
print("Model ve sütun yapısı başarıyla kaydedildi!")