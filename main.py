from bs4 import BeautifulSoup
import lxml
import requests
import smtplib


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

listing_urls = []
all_prices = []

for a in links:
   url = (a['href'])
   listing_urls.append(url)
   
for p in prices: 
    price = p.getText().strip()
    all_prices.append(price)
    
print (all_prices)
print (listing_urls)
   