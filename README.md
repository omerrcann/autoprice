# 🚗 AutoPrice Predictor

**AutoPrice Predictor**, Türkiye ikinci el otomobil piyasasındaki araç fiyatlarını tahmin etmek amacıyla geliştirilmiş, uçtan uca (**end-to-end**) bir veri mühendisliği ve makine öğrenmesi projesidir.

Proje; **veri toplama, veri temizleme, özellik mühendisliği, model eğitimi ve interaktif web arayüzü** aşamalarının tamamını kapsar.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://autoprice-vzatmdcncah4utunhcto5u.streamlit.app/)

---

## 🏗️ Proje Mimarisi

Proje temel olarak dört ana aşamadan oluşmaktadır:

### 1. Dinamik Web Scraping — Selenium

İlan sitelerindeki dinamik HTML yapıları, tutarsız CSS sınıfları ve iç içe geçmiş özellik tabloları veri toplama sürecinde çeşitli zorluklar oluşturmuştur.

Bu problemleri aşmak için:

* **Selenium** ve **WebDriver Manager** kullanıldı.
* Dinamik DOM yapıları için **XPath** ve **CSS Selectors** kullanıldı.
* İlan sayfaları arasında gezinmek için otomatik tarama sistemi geliştirildi.
* Bağlantı kopmaları ve olası bellek problemlerine karşı **Auto-Save** mekanizması oluşturuldu.
* Toplanan her ilan, veri kaybını önlemek amacıyla CSV dosyasına **append** modunda kaydedildi.

---

### 2. Veri Temizleme ve Feature Engineering — Pandas & Regex

Toplanan ham veriler, doğrudan makine öğrenmesi modelinde kullanılabilecek durumda değildi.

Karşılaşılan temel problemler:

* Birleşik veya indirimli fiyat etiketleri
* String formatındaki kilometre değerleri
* Eksik veya tutarsız veriler
* Piyasa dışı aykırı değerler (outliers)
* Kategorik değişkenlerin metin formatında bulunması

Bu problemleri çözmek için:

* **Pandas** ile veri temizleme ve filtreleme işlemleri gerçekleştirildi.
* **Regex** kullanılarak metin içerisindeki sayısal veriler ayrıştırıldı.
* Piyasa dışı değerler filtrelenerek veri setinden çıkarıldı.
* Model için gerekli kategorik ve sayısal değişkenler hazırlandı.

---

### 3. Makine Öğrenmesi — Random Forest Regressor

Model geliştirme süreci iki temel aşamada gerçekleştirildi.

#### İlk Model

İlk aşamada yalnızca temel araç özellikleri kullanıldı:

* Model
* Yıl
* Kilometre

İlk modelin sonuçları:

| Metrik |      Sonuç |
| ------ | ---------: |
| RMSE   | 796.620 TL |
| R²     |      0.126 |

Bu sonuçlar, yalnızca temel araç özelliklerinin fiyat değişkenliğini yeterince açıklayamadığını gösterdi.

#### Feature Engineering ve Optimizasyon

Model performansını artırmak amacıyla scraper genişletildi ve aşağıdaki değişkenler veri setine dahil edildi:

* Marka
* Seri
* Model
* Donanım Paketi
* Vites Tipi
* Yakıt Tipi
* Yıl
* Kilometre

Kategorik değişkenler için **One-Hot Encoding** uygulanarak modelin kullanımına uygun hale getirildi.

#### Final Model

Feature Engineering sonrasında model performansında önemli bir iyileşme elde edildi:

| Metrik |  İlk Model |    Final Model |
| ------ | ---------: | -------------: |
| RMSE   | 796.620 TL | **323.025 TL** |
| R²     |      0.126 |      **0.737** |

Bu sonuçlarla modelin fiyat değişkenliğini açıklama kapasitesi önemli ölçüde artırılmıştır.

---

### 4. İnteraktif Web Arayüzü — Streamlit

Eğitilen **Random Forest Regressor** modeli `joblib` kullanılarak `.pkl` formatında kaydedildi ve **Streamlit** tabanlı bir web uygulamasına entegre edildi.

Uygulamada:

* Araç marka seçimi
* Seriye göre dinamik filtreleme
* Donanım paketine göre filtreleme
* Araç özelliklerinin girilmesi
* Tahmini araç fiyatının hesaplanması

gibi işlemler gerçekleştirilebilmektedir.

Arayüzdeki filtreler, seçilen markaya bağlı olarak ilgili seri ve donanım seçeneklerini dinamik olarak günceller.

---

## 🧰 Kullanılan Teknolojiler

| Alan             | Teknolojiler                          |
| ---------------- | ------------------------------------- |
| Veri Toplama     | Python, Selenium, WebDriver Manager   |
| Veri İşleme      | Pandas, NumPy, Regex                  |
| Makine Öğrenmesi | Scikit-Learn, Random Forest Regressor |
| Model Kaydetme   | Joblib                                |
| Web Arayüzü      | Streamlit                             |
| Veri Formatı     | CSV                                   |

---

## 📂 Proje Akışı

```text
Web Scraping
     │
     ▼
Raw Data (CSV)
     │
     ▼
Data Cleaning
     │
     ▼
Feature Engineering
     │
     ▼
One-Hot Encoding
     │
     ▼
Random Forest Regressor
     │
     ▼
Model (.pkl)
     │
     ▼
Streamlit Web Application
     │
     ▼
Estimated Vehicle Price
```

---

## 🚀 Kurulum

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/omerrcann/AutoPrice-Predictor.git
cd AutoPrice-Predictor
```

### 2. Gerekli Kütüphaneleri Yükleyin

```bash
pip install pandas numpy scikit-learn selenium webdriver-manager streamlit joblib
```

### 3. Web Uygulamasını Başlatın

```bash
streamlit run app.py
```

Uygulama başlatıldıktan sonra Streamlit tarafından sağlanan lokal adres üzerinden web arayüzüne erişebilirsiniz.

---

## 📊 Model Performansı

Final modelinin elde ettiği sonuçlar:

**R² Score:** `0.737`

**RMSE:** `323.025 TL`

Model, kullanılan veri seti ve özellikler kapsamında araç fiyatlarındaki varyansın yaklaşık **%73,7'sini** açıklayabilmektedir.

---

## 📌 Proje Özeti

AutoPrice Predictor; gerçek dünyadan veri toplama, ham veriyi temizleme, özellik mühendisliği, makine öğrenmesi modeli geliştirme ve modeli kullanıcıların erişebileceği bir web uygulamasına dönüştürme süreçlerini tek bir proje içerisinde birleştirmektedir.

Projenin temel amacı, Türkiye ikinci el otomobil piyasasındaki araç özelliklerinden yararlanarak **tahmini araç fiyatı** üretmektir.
