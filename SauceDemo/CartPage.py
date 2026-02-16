from selenium.webdriver.common.by import By
from BasePage import BasePage

BASE_URL = "https://www.saucedemo.com/cart.html"

class Locators:

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")

class CartPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, url=BASE_URL)

    def getReady(self):
        return self.find(Locators.TITLE)
    
    def getAllProductsInCart(self):
        items = self.find_all(Locators.CART_ITEM)
        return [item.text for item in items]