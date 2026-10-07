import streamlit as st
import pandas as pd
import joblib

model = joblib.load("arac_fiyat_modeli_zengin.pkl")
model_sutunlari = joblib.load("model_sutunlari_zengin.pkl")
df = pd.read_csv("temiz_zengin_veri.csv")

st.set_page_config(page_title="AutoPrice Predictor", page_icon="🚗", layout="wide")
st.title("🚗 AutoPrice: İkinci El Fiyat Tahminleyicisi")
st.markdown("Gelişmiş Random Forest makine öğrenmesi modeli ile aracınızın güncel piyasa değerini hesaplayın.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    marka = st.selectbox("Marka", df['Marka'].dropna().sort_values().unique())
with col2:
    filtrelenmis_seri = df[df['Marka'] == marka]['Seri'].dropna().sort_values().unique()
    seri = st.selectbox("Seri", filtrelenmis_seri)
with col3:
    filtrelenmis_model = df[df['Seri'] == seri]['Model'].dropna().sort_values().unique()
    model_secim = st.selectbox("Model / Donanım", filtrelenmis_model)

col4, col5, col6, col7 = st.columns(4)

with col4:
    yil = st.number_input("Üretim Yılı", min_value=1990, max_value=2024, value=2015, step=1)
with col5:
    km = st.number_input("Kilometre", min_value=0, max_value=400000, value=100000, step=5000)
with col6:
    vites = st.selectbox("Vites Tipi", df['Vites'].dropna().unique())
with col7:
    yakit = st.selectbox("Yakıt Tipi", df['Yakit'].dropna().unique())

st.divider()

if st.button("Piyasa Değerini Hesapla", type="primary", use_container_width=True):
    input_data = pd.DataFrame([[marka, seri, model_secim, yil, km, vites, yakit]],
                              columns=['Marka', 'Seri', 'Model', 'Yil', 'Kilometre', 'Vites', 'Yakit'])

    input_encoded = pd.get_dummies(input_data)

    for col in model_sutunlari:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    input_encoded = input_encoded[model_sutunlari]
    tahmin = model.predict(input_encoded)[0]

    st.success(f"Tahmini Piyasa Değeri: **{tahmin:,.0f} TL**")