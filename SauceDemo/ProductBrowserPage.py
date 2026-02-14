from BasePage import BasePage
from selenium.webdriver.common.by import By

class Locators:

    INVENTORY_LIST = (By.CLASS_NAME, "[data-test='inventory-list']")
    PRODUCT_INFOS = (By.CSS_SELECTOR, "[data-test='inventory-item-description']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='add-to-cart*']")

    def getItemByID(self, id):
        return (By.ID, f"item_{id}_title_link") 

class ProductBrowserPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def getReady(self):
        return self.find(Locators.INVENTORY_LIST)
    
    def getAllProducts(self):
        return self.find_all(Locators.PRODUCT_INFOS)

    def getAllProductNames(self):
        return [item.text for item in self.find_all(Locators.PRODUCT_NAMES)]
    
    def addProductToCart(self, name):
        items = self.getAllProducts()
        for item in items:
            if item.text == name:
                addButton = self.find(Locators.ADD_TO_CART_BUTTON)
                addButton.click()