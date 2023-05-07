from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# Create the output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

# Set up the Chrome browser driver
driver = webdriver.Chrome()

csv_urls_filename = "output/urls.csv"
csv_filename = "output/data.csv"

with open(csv_urls_filename, "r") as csvfile:
    urls = csv.reader(csvfile)
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "name",
                "cuisine_type",
                "rating",
                "reviews",
                "price_band",
                "url",
                "popular_dish_name 1",
                "popular_dish_name 2",
                "popular_dish_name 3",
            ]
        )
        for row in urls:
            url = row[0]
            if url and isinstance(url, str):
                driver.get(url)

                time.sleep(1)

                try:
                    name = (
                        WebDriverWait(driver, 2)
                        .until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/main/div/div[2]/div[1]/section[2]/h1",)))
                        .text
                    )
                except Exception as e:
                    name = ""

                try:
                    rating = (
                        WebDriverWait(driver, 2)
                        .until(EC.presence_of_element_located((By.ID, "ratingInfo")))
                        .text
                    )
                except Exception as e:
                    rating = ""

                try:
                    reviews = (
                        WebDriverWait(driver, 2)
                        .until(EC.presence_of_element_located((By.ID, "reviewInfo")))
                        .text
                    )
                    reviews = reviews.replace("Reviews", "").strip()
                except Exception as e:
                    reviews = ""

                try:
                    price_band = (
                        WebDriverWait(driver, 2)
                        .until(EC.presence_of_element_located((By.ID, "priceBandInfo")))
                        .text
                    )
                except Exception as e:
                    price_band = ""

                try:
                    cuisine_type = (
                        WebDriverWait(driver, 2)
                        .until(EC.presence_of_element_located((By.ID, "cuisine_type")))
                        .text
                    )
                except Exception as e:
                    cuisine_type = ""
                
                try:
                    popular_dishes = []
                    # Scrape the popular dishes
                    popular_dishes_elements = driver.find_elements(By.CSS_SELECTOR, "button[data-testid='dish-card']")

                    if popular_dishes_elements:
                        for dish in popular_dishes_elements:
                            popular_dish_name = dish.find_element(By.TAG_NAME, "h3").text
                            popular_dishes.append(popular_dish_name)

                except Exception as e:
                    print("No popular dishes found...")

                finally:
                    if name and cuisine_type and rating and price_band and reviews and popular_dishes:
                        writer = csv.writer(csvfile)
                        writer.writerow([name, cuisine_type, rating, reviews, price_band, *popular_dishes])
                    elif name and cuisine_type and rating and price_band and reviews:
                        writer = csv.writer(csvfile)
                        writer.writerow([name, cuisine_type, rating, reviews, price_band, url])
                    popular_dishes = []
            else:
                print(f"Invalid URL format: {url}")
        # Close the driver
        driver.quit()