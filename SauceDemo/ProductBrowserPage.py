from BasePage import BasePage
from selenium.webdriver.common.by import By

class Locators:

    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name ")

    def getItemByID(self, id):
        return (By.ID, f"item_{id}_title_link") 



class ProductBrowserPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def getReady(self):
        return self.find((By.CLASS_NAME, "inventory_list"))

    def getAllProducts(self):

        names = []
        products = self.find_all(Locators.INVENTORY_LIST)

        for product in products:
            name = product.find_element(*Locators.ITEM_NAME).text
            names.append(name)

        return names