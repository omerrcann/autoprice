from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
import os

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

toplam_sayfa = 50
ilan_linkleri = []
csv_dosyasi = "zengin_arac_verisi.csv"

if os.path.exists(csv_dosyasi):
    os.remove(csv_dosyasi)

try:
    print("--- 1. AŞAMA: İlan Linkleri Toplanıyor ---")
    for page in range(1, toplam_sayfa + 1):
        url = f"https://www.arabam.com/ikinci-el/otomobil?page={page}"
        driver.get(url)
        time.sleep(random.uniform(4, 6))

        listings = driver.find_elements(By.CSS_SELECTOR, "tr.listing-list-item")
        for listing in listings:
            try:
                link_element = listing.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")
                if href and href not in ilan_linkleri:
                    ilan_linkleri.append(href)
            except:
                continue
        print(f"Sayfa {page} tarandı. Toplam link: {len(ilan_linkleri)}")

    print(f"\n--- 2. AŞAMA: {len(ilan_linkleri)} İlanın Detaylarına Giriliyor ---")

    for i, link in enumerate(ilan_linkleri):
        print(f"[{i + 1}/{len(ilan_linkleri)}] İlan analiz ediliyor...")
        try:
            driver.get(link)
            time.sleep(random.uniform(3, 5))

            def bilgiyi_al(etiket_adi):
                try:
                    xpath = f"//div[contains(@class, 'property-key') and normalize-space(text())='{etiket_adi}']/following-sibling::div[contains(@class, 'property-value')]"
                    return driver.find_element(By.XPATH, xpath).text.strip()
                except:
                    return None

            try:
                fiyat = driver.find_element(By.CSS_SELECTOR, "div.desktop-information-price").text.strip()
            except:
                fiyat = None

            arac = {
                "Marka": bilgiyi_al("Marka"),
                "Seri": bilgiyi_al("Seri"),
                "Model": bilgiyi_al("Model"),
                "Yil": bilgiyi_al("Yıl"),
                "Kilometre": bilgiyi_al("Kilometre"),
                "Vites": bilgiyi_al("Vites tipi"),
                "Yakit": bilgiyi_al("Yakıt tipi"),
                "Fiyat": fiyat
            }

            if arac["Marka"] and arac["Vites"] and arac["Yakit"] and arac["Fiyat"]:
                df_tek_satir = pd.DataFrame([arac])
                df_tek_satir.to_csv(csv_dosyasi, mode='a', header=not os.path.exists(csv_dosyasi), index=False,
                                    encoding="utf-8-sig")

        except Exception as e:
            continue

finally:
    driver.quit()
    print("\nVeri çekme işlemi tamamlandı! Tarayıcı kapatıldı.")