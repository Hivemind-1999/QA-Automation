from selenium.webdriver.common.by import By
from BasePage import BasePage

BASE_URL = "https://www.saucedemo.com/cart.html"

class Locators:

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CART_ITEM_TEXT = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    #CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")

class CartPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, url=BASE_URL)

    def getReady(self):
        return self.find(Locators.TITLE)
    
    def getAllProductsInCart(self):
        return self.find_all(Locators.CART_ITEM_TEXT)
    
    def confirmEmptyCart(self):
        return self.confirmAbsence(Locators.CART_ITEM)
    
    #def proceedToCheckout(self):
    #    self.find(Locators.CHECKOUT_BUTTON).click()
    
    def removeItem(self):
        itemToRemove = self.find_all(Locators.CART_ITEM)[0]
        removeButton = itemToRemove.find_element(By.CSS_SELECTOR, "[data-test^='remove']")
        removeButton.click()