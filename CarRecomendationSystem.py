from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import math
import pandas as pd
import os

from helper import Car

def scrapeCars(brand: str = '', model: str = '', price_form: str = '', price_to: str = '', year_from: str = ''):

    existingData = pd.read_csv("cars.csv")['linkToArticle'].values

    # Disable Image Loading, Bad handshake errors and run chrome headless (without a window)
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--log-level=1")
    options.add_argument("--headless=true")

    # Start Chrome with chrome options
    driver = webdriver.Chrome(options=options)

    # Web page link
    webPageLink = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page={}&sort=basic&brand={}&model%5B0%5D={}&price_from={}&price_to={}&year_from={}&chassis%5B0%5D=2631&city_distance=0&showOldNew=all&without_price=1&door_num=3013'

    numberOfPages = 1
    # Go to first page
    driver.get(webPageLink.format(1, brand, model, price_form, price_to, year_from))
    numberOfPagesText = driver.find_element(By.XPATH, '//div[@class="js-hide-on-filter"]/small').text

    # Find all numeric sequences (X, Y, and Z)
    numeric_values = re.findall(r'\d+', numberOfPagesText)

    # Extract the value of X (assuming it's the last numeric value)
    if numeric_values:
        numberOfPages = math.ceil(int(numeric_values[-1])/int(numeric_values[1]))
    else:
        print("No numeric values found in the string.")

    linksToArticlePages = []
    pricesMap = {}

    for pageNumber in range(1, numberOfPages+1):
        # Navigate to the webpage and apply search parameters
        if pageNumber != 1:
            driver.get(webPageLink.format(pageNumber, brand, model, price_form, price_to, year_from))

        # Extract data from the webpage
        carLinks = driver.find_elements(By.XPATH, '//article[@data-ownerid]')

        for car in carLinks:
            link = car.find_element(By.XPATH, './/div[@class="image"]/a').get_property('href')
            if link not in existingData:
                linksToArticlePages.append(link)
                pricesMap[link] = car.get_attribute('data-price')

    carDetails = []

    def getCarDetail(detail):
        try:
            return driver.find_element(By.XPATH, f'//div[contains(text(), "{detail}")]/following-sibling::div[@class="uk-width-1-2 uk-text-bold"]').text
        except:
            return None

    carAmount = len(linksToArticlePages)
    i = 0
    limit_selection = None

    # Extract data from the car pages
    for link in linksToArticlePages:
        i+=1
        if limit_selection is not None and i >= limit_selection:
            break
        print(f"Scraping car {i}/{carAmount} - {link}", flush=True)
        
        # Go to the car's page and scrape the data
        try:
            driver.get(link)
        except:
            continue
        # Extract data from the webpage
        state = getCarDetail("Stanje:")
        brand = getCarDetail("Marka")
        model = getCarDetail("Model")
        year = getCarDetail("Godište")
        distanceTraveled = getCarDetail("Kilometraža")
        bodyType = getCarDetail("Karoserija")
        fuelType = getCarDetail("Gorivo")
        cubicCapacity = getCarDetail("Kubikaža")
        motorStrength = getCarDetail("Snaga motora")
        fixedPrice = getCarDetail("Fiksna cena") == "DA"
        exchange = getCarDetail("Zamena:") == "DA"
        linkToArticle = link
        numberOfDoors = getCarDetail("Broj vrata")
        numberOfSeats = getCarDetail("Broj sedišta")
        color = getCarDetail("Boja")
        condition = getCarDetail("Oštećenje")
        price = pricesMap[link]

        car = Car(brand=brand, model=model, year=year, distanceTraveled=distanceTraveled, bodyType=bodyType, fuelType=fuelType, cubicCapacity=cubicCapacity, 
                motorStrength=motorStrength, fixedPrice=fixedPrice, exchange=exchange, linkToArticle=linkToArticle, numberOfDoors=numberOfDoors, 
                numberOfSeats=numberOfSeats, color=color, condition=condition, price=price, state=state)
        carDetails.append(car)

    outputData = "cars.csv"

    df = pd.DataFrame([vars(car) for car in carDetails])

    if not df.empty:
        print(df[['brand','model','year','distanceTraveled','fuelType','linkToArticle','price']])
        df.to_csv(outputData, mode='a', index=False, header=not os.path.exists(outputData))
    else:
        print("No new articles detected.")

    driver.quit()


parameters = {
    'brand': 'renault',
    'model': 'clio',
    'price_from': '3000',
    'price_to': '7000',
    'year_from': '2014',
}

scrapeCars(parameters['brand'], parameters['model'], parameters['price_from'], parameters['price_to'], parameters['year_from'])
