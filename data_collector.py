from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

car_data_list = []
toplam_sayfa = 50

try:
    for page in range(1, toplam_sayfa + 1):
        url = f"https://www.arabam.com/ikinci-el/otomobil?page={page}"
        print(f"Sayfa {page} yükleniyor...")
        driver.get(url)
        time.sleep(random.uniform(5, 8))

        listings = driver.find_elements(By.CSS_SELECTOR, "tr.listing-list-item")
        print(f"Sayfa {page} üzerinde {len(listings)} adet ilan tarandı.")

        for listing in listings:
            try:
                sutunlar = listing.find_elements(By.TAG_NAME, "td")

                if len(sutunlar) >= 7:
                    satir_verileri = [td.text.replace('\n', ' ').strip() for td in sutunlar]
                    dolu_veriler = [veri for veri in satir_verileri if veri != ""]

                    if len(dolu_veriler) >= 5:
                        model = dolu_veriler[0]
                        yil = dolu_veriler[2]
                        km = dolu_veriler[3]

                        fiyat = next((v for v in dolu_veriler if "TL" in v), dolu_veriler[-1])

                        car_data_list.append({
                            "Model": model,
                            "Yil": yil,
                            "Kilometre": km,
                            "Fiyat": fiyat
                        })
            except Exception:
                continue

finally:
    driver.quit()

df = pd.DataFrame(car_data_list)
df.to_csv("ham_arac_verisi.csv", index=False, encoding="utf-8-sig")
print(f"\nToplam {len(df)} araç verisi kaydedildi.")