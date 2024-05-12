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

SPORTINGLIFE = {
    "store": "sportinglife",
    "search_field": "//input[@id='q']",
    "img": "//a[@class='thumb-link test']/img[1]",
    "name": "//span[@class='product-name']",
    "oldPrice": "//span[@class='price-standard']",
    "newPrice": "//span[@class='price-sales has-standard-price']",
    "link": "//a[@class='thumb-link test']",
    "load_tag": "//div[@class='infinite-scroll-placeholder']/button[1]"
}


def search(selectors):
    search_selector = driver.find_element(
        By.XPATH, selectors["search_field"])
    action.click(search_selector)  # First click clears any popups
    action.perform()

    time.sleep(2)

    action.click(search_selector)
    action.perform()
    time.sleep(2)
    search_selector.send_keys("Skis")
    search_selector.send_keys(Keys.RETURN)


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

    if (selectors["store"] == "sportinglife"):
        for itemName, itemLink, itemImg, itemOld, itemNew in zip(itemNameCollection, itemLinkCollection, itemImgCollection, itemOldCollection, itemNewCollection):
            # style_selector = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('{}')".format(selectors["unique_Element"]), itemNew)
            itemData = {
                "Item": itemName.text,
                "Img": itemImg.get_attribute("src"),
                "OldPrice": itemOld.text[1:].replace(",", ""),
                "NewPrice": itemNew.text[1:].replace(",", ""),
                "Link": itemLink.get_attribute("href")
            }
            productList.append(itemData)
    return productList


def load_more(selector):
    while True:
        try:
            load_more_button = wait.until(EC.presence_of_element_located(
                ((By.XPATH, selector["load_tag"]))))
            load_more_button.click()
            time.sleep(0.6)
        except TimeoutException:
            return False


def find_sales():
    salesTab = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".refinement.c-accordion.isOnSale")))
    action.click(salesTab)
    action.perform()

    salesLink = wait.until(EC.presence_of_element_located(
        ((By.CSS_SELECTOR, ".refinement.c-accordion.isOnSale div.refinement-link-name"))))
    action.click(salesLink)
    action.perform()


def run():
    driver.get("https://www.sportinglife.ca/en-CA/homepage")
    Collection = db["SportingLifeSkis"]
    Collection.delete_many({})

    search(SPORTINGLIFE)

    find_sales()

    time.sleep(1)

    load_more(SPORTINGLIFE)

    itemData = get_all_product(SPORTINGLIFE)
    store_data(itemData, Collection)

    driver.quit()
