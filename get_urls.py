from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import argparse

# Create the output folder if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

parser = argparse.ArgumentParser(description='Search open table')
parser.add_argument('--latitude')
parser.add_argument('--longitude')

args = parser.parse_args()

latitude = str(args.latitude)
longitude = str(args.longitude)

# Set up the Chrome browser driver
driver = webdriver.Chrome()

# Initialize an empty list to store the URLs
urls = []

# Set the page number to 1
page_num = 1

# Set the maximum number of pages to scrape
max_pages = 13

csv_filename = f'output/urls.csv'

# Initialize the CSV file and write the header row to it
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

while True:
    # Navigate to the search results page for the current page number
    url = f'https://www.opentable.com/s?latitude={latitude}&longitude={longitude}&shouldUseLatLongSearch=true&page={page_num}'
    driver.get(url)

    # Keep scrolling down until we see new businesses appear
    while True:
        try:
            # Find all the businesses in the search results
            businesses = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'CZSRtRus5QKZeZX0z27m'))
            )
        except:
            # If no businesses are found, break the loop
            break

        time.sleep(2)

        # Store the URLs of the businesses
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for business in businesses:
                try:
                    url = business.get_attribute('href')
                    if url and url not in urls:
                        urls.append(url)
                        writer.writerow([url])
                except:
                    print("error getting business url")
                # Scroll down to load more businesses
                driver.execute_script("arguments[0].scrollIntoView();", businesses[-1])
                # time.sleep(1)

        try:
            # Check if new businesses are loaded
            new_businesses = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'CZSRtRus5QKZeZX0z27m'))
            )
            if len(new_businesses) == len(businesses):
                # If no new businesses are loaded, we've reached the bottom of the page
                break
        except:
            # If an exception occurs, we've probably reached the bottom of the page
            break

    # Increment the page number
    page_num += 1

    # Check if we've reached the maximum number of pages
    business = []
    new_businesses = []
    if page_num > max_pages:
        break

# Close the driver
driver.quit()

print("Scraping completed.")
print("collected: " + str(page_num-1) + " pages of urls to scan")
