from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Locators:

    PRODUCT_TILES = (By.CSS_SELECTOR, "[data-test='inventory-item-description']")
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BUTTON = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    SORT_FEATURE = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

class ProductBrowserPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
    
    def getAllProducts(self):
        return self.find_all(Locators.PRODUCT_TILES)

    def getAllProductNames(self):
        return [item.text for item in self.find_all(Locators.PRODUCT_NAME)]
    
    def getAllProductPrices(self):
        prices = [item.text for item in self.find_all(Locators.PRODUCT_PRICE)]
        return [float(price[1:]) for price in prices]
    
    def goToCart(self):
        self.find(Locators.CART_BUTTON).click()
        from CartPage import CartPage
        return CartPage(self.driver)
    
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
    
    def sort(self, mode):
        sortButton = self.find(Locators.SORT_FEATURE)
        sortButtonSelector = Select(sortButton)
        sortButtonSelector.select_by_value(mode)
        match mode:
            case "az" | "za":
                return self.getAllProductNames()
            case "lohi" | "hilo":
                return self.getAllProductPrices()
            case _:
                return None