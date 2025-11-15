from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

import time
import requests
import os

if not os.path.isfile(".env"):
    print("\033[91m" + "No .env file found. Please create one and add your NTFY_URL variable." + "\033[0m")
    exit(1)

load_dotenv()

url = "https://store.steampowered.com/sale/steamdeckrefurbished/"

print("Starting browser...")

while True:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        search_terms = [
            {"name": "Steam Deck 512 GB OLED", "term": "Steam Deck 512 GB OLED - Valve Certified Refurbished"},
            {"name": "Steam Deck 1TB OLED", "term": "Steam Deck 1TB OLED - Valve Certified Refurbished"}
        ]

        time.sleep(3)

        for search_term in search_terms:
            in_stock = False

            div_element_of_search_term = driver.find_element(By.XPATH, "//div[normalize-space(.) = '" + search_term["term"] + "']")
            price_element = div_element_of_search_term.find_element(By.XPATH, "../..//div[contains(normalize-space(text()), '€')]")
            stock_indicator_element = price_element.find_element(By.XPATH, "../..//span")
            is_in_stock = "Out of stock" not in stock_indicator_element.get_attribute('innerHTML')

            print("Produkt: " + search_term["name"])
            print("Preis: " + price_element.get_attribute('innerHTML'))
            print(f"In Stock: {'Yes' if is_in_stock else 'No'}")
            print("\n")

            if is_in_stock:
                print("Messaging via NTFY...")
                headers = {"Title": "Steam Deck Refurbished in Stock!", "Priority": "max", "Actions": f"view, Buy now!, {url}"}
                message = f"\n{search_term['name']} is in stock!\n\nPreis: {price_element.get_attribute('innerHTML')}"
                requests.post(f"{os.getenv('NTFY_URL')}", headers=headers, data=message.encode(encoding="utf-8"))
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        print("Finished check! Idling....")
        time.sleep(900) # 15 minutes