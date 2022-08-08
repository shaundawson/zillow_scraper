import time
from bs4 import BeautifulSoup
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from keys import CHROME_BINARY_LOC, CHROME_DRIVER_PATH, CHROME_PROFILE_PATH
from selenium.webdriver.common.by import By


zillow_url='https://www.zillow.com/homes/for_rent/2-_beds/?searchQueryState={"usersSearchTerm":"Brooklyn, New York, NY","mapBounds":{"west":-74.07916397460939,"east":-73.81755203613282,"south":40.564209391228374,"north":40.74627045249812},"isMapVisible":true,"filterState":{"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"fore":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fr":{"value":true},"ah":{"value":true},"beds":{"min":2},"mp":{"max":2300},"price":{"max":551266}},"isListVisible":true,"mapZoom":12,"regionSelection":[],"customRegionId":"0c64262e72X1-CR1s8vqrvzqflq_wb2hl"}'


headers={
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

# Scrape Zillow
response = requests.get(zillow_url,headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all(name="a", class_="list-card-link")
prices = soup.find_all(name="div",class_="list-card-price")
locations = soup.find_all(name="address",class_="list-card-addr")



all_listing_urls = []
all_prices = []
all_locations = []

for a in links:
   url = (a['href'])
   if "http" not in url:
       all_listing_urls.append(f"https://www.zillow.com{url}")
   else:
       all_listing_urls.append(url)
   
for p in prices: 
    try:
        price = p.getText().strip()
        all_prices.append(price)
    except IndexError:
        print('Multiple listings for the card')
        price = p.select(".list-card-details li")[0].contents[0]
        
for l in locations: 
    listing_address = l.getText().strip(" ")
    all_locations.append(listing_address)
    
    
def pause():
    time_break = random.randint(4,9)
    return time.sleep(time_break)
    
s=Service(executable_path=CHROME_DRIVER_PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
chrome_options.binary_location=(CHROME_BINARY_LOC)
driver = webdriver.Chrome(service=s, options=chrome_options)
        
for n in range(len(all_listing_urls)):
    driver.get("https://www.docs.google.com/forms/d/e/1FAIpQLSdU9R4zFtWEmwb7PW0w2fBsr7FyBHmw5PQGr4ath2EJvbKeIA/viewform")
    driver.maximize_window()
    pause()
    address = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')
    address.send_keys(all_locations[n]) 
    price.send_keys(all_prices[n])
    link.send_keys(all_listing_urls[n])
    submit_button.click()