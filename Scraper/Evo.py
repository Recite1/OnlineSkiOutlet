from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pymongo
import time

client = pymongo.MongoClient(
    "YOUR MANGODB URL (CONNECTION STRING)")
db = client["SkiItems"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1250,1000")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--enable-chrome-browser-cloud-management")

driver = webdriver.Chrome(
    options=chrome_options)
wait = WebDriverWait(driver, 3)
action = ActionChains(driver)

EVO = {
    "img": "//span[@class='product-thumb-image-wrapper js-product-thumb-link']/img[1]",
    "name": "//span[@class='product-thumb-title']",
    "oldPrice": "//span[@class='product-thumb-price']",
    "newPrice": "//span[@class='product-thumb-price']",
    "link": "//a[@class='product-thumb-link js-product-thumb-details-link']",
    "load_tag": "//a[@class='results-next icon-arrow-right-medium results-link']"
}


def store_data(document, collections):
    collections.insert_many(document)


def get_all_product(selectors):
    productList = []
    itemImgCollection = driver.find_elements(
        By.XPATH, selectors["img"])
    itemNameCollection = driver.find_elements(
        By.XPATH, selectors["name"])
    itemOldCollection = driver.find_elements(
        By.XPATH, selectors["oldPrice"])
    itemNewCollection = driver.find_elements(
        By.XPATH, selectors["newPrice"])
    itemLinkCollection = driver.find_elements(
        By.XPATH, selectors["link"])

    print(len(itemImgCollection))
    print(len(itemNameCollection))
    print(len(itemOldCollection))
    print(len(itemNewCollection))
    print(len(itemLinkCollection))

    oldPriceTracker = 0
    itemSalePriceCollection = driver.find_elements(
        By.XPATH, "//span[@class='product-thumb-price slash']")
    print("Pric SLash: ", len(itemSalePriceCollection))

    for itemName, itemLink, itemImg, itemOld, itemNew in zip(itemNameCollection, itemLinkCollection, itemImgCollection, itemOldCollection, itemNewCollection):
        itemData = {
            "Item": itemName.text,
            "Img": itemImg.get_attribute("src"),
            "OldPrice": itemOld.text[2:].replace(",", "").replace(" ", ""),
            "NewPrice": itemNew.text[2:-4].replace(",", "").replace(" ", ""),
            "Link": itemLink.get_attribute("href")
        }
        if (itemData["OldPrice"][-4:] == "SALE" or itemData["OldPrice"][-4:] == "ANCE"):
            if itemData["NewPrice"][:5] == "tlet:":
                itemData["NewPrice"] = itemData["NewPrice"][7:]
            itemData["OldPrice"] = itemSalePriceCollection[oldPriceTracker].text[2:].replace(
                ",", "").replace(" ", "")
            oldPriceTracker += 1
            productList.append(itemData)
    print("Total Itemes Added:", len(productList))
    return productList


def run():
    driver.get(
        "https://www.evo.com/en-ca/shop/sale/ski/skis/mens/womens/shipsto_canada/skis_no-bindings/rpp_400")
    Collection = db["EvoSkis"]
    Collection.delete_many({})

    productList = get_all_product(EVO)
    store_data(productList, Collection)

    driver.quit()
