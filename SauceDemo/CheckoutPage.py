from selenium.webdriver.common.by import By
from BasePage import BasePage

#BASE_URL = "https://www.saucedemo.com/checkout-step-one.html"

class Locators:

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CONTINUE = (By.CSS_SELECTOR, "#continue")
    FIRST_NAME = (By.CSS_SELECTOR, "#first-name")
    LAST_NAME = (By.CSS_SELECTOR, "#last-name")
    POSTAL_CODE = (By.CSS_SELECTOR, "#postal-code")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    CART_PRODUCTS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "[data-test='item-quantity']")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def getReady(self):
        return self.find(Locators.TITLE)
    
    def enterFirstName(self, text):
        self.enter_text(Locators.FIRST_NAME, text)

    def enterLastName(self, text):
        self.enter_text(Locators.LAST_NAME, text)

    def enterZip(self, text):
        self.enter_text(Locators.POSTAL_CODE, text)

    def getPageTitle(self):
        return self.find(Locators.TITLE).text

    def getErrorMessage(self):
        return self.find(Locators.ERROR_MESSAGE).text

    def pressContinue(self):
        self.find(Locators.CONTINUE).click()

    def getCartProducts(self):
        cartProducts = self.find_all(Locators.CART_PRODUCTS)
        order = []

        for item in cartProducts:
            quantity = item.find_element(*Locators.ITEM_QUANTITY).text
            quantity = int(quantity)
            price = item.find_element(*Locators.ITEM_PRICE).text
            price = float(price[1:])
            order.append(price * quantity)

        return order
    
    def getDisplayedTotals(self):
        subtotal = self.find(Locators.SUBTOTAL).text
        subtotal = subtotal[13:]
        subtotal = float(subtotal)

        tax = self.find(Locators.TAX).text
        tax = tax[6:]
        tax = float(tax)

        total = self.find(Locators.TOTAL).text
        total = total[8:]
        total = float(total)

        return subtotal, tax, total

