from BasePage import BasePage
from selenium.webdriver.common.by import By

BASE_URL = "https://www.saucedemo.com/inventory.html"

class Locators:

    INVENTORY_LIST = (By.CSS_SELECTOR, "[data-test='inventory-list']")
    PRODUCT_TILES = (By.CSS_SELECTOR, "[data-test='inventory-item-description']")
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def getItemByID(self, id):
        return (By.ID, f"item_{id}_title_link") 

class ProductBrowserPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, url=BASE_URL)

    def getReady(self):
        return self.find(Locators.INVENTORY_LIST)
    
    def getAllProducts(self):
        return self.find_all(Locators.PRODUCT_TILES)

    def getAllProductNames(self):
        return [item.text for item in self.find_all(Locators.PRODUCT_NAME)]
    
    def getCartBadgeNum(self):
        badgeText = self.find(Locators.CART_BADGE).text
        return int(badgeText)
    
    def addProduct(self, index):
        products = self.getAllProducts()
        item = products[index]
        name = item.find_element(*Locators.PRODUCT_NAME).text
        price = item.find_element(*Locators.PRODUCT_PRICE).text
        item.find_element(*Locators.ADD_TO_CART_BUTTON).click()
        return {"name": name, "price": price}