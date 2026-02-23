from selenium.webdriver.common.by import By
from BasePage import BasePage
from decimal import Decimal
import re

class Locators:

    CONTINUE = (By.CSS_SELECTOR, "#continue")
    FINISH = (By.CSS_SELECTOR, "#finish")
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
    CONFIRMATION = (By.CSS_SELECTOR, "[data-test='complete-header']")
    BACK_TO_BROWSER = (By.CSS_SELECTOR, "[data-test='back-to-products']")

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def enterFirstName(self, text):
        self.enter_text(Locators.FIRST_NAME, text)

    def enterLastName(self, text):
        self.enter_text(Locators.LAST_NAME, text)

    def enterZip(self, text):
        self.enter_text(Locators.POSTAL_CODE, text)

    def enterBuyerInfo(self, firstName, lastName, zip):
        self.enterFirstName(firstName)
        self.enterLastName(lastName)
        self.enterZip(zip)

    def getErrorMessage(self):
        return self.find(Locators.ERROR_MESSAGE).text

    def pressContinue(self):
        self.find(Locators.CONTINUE).click()

    def pressFinish(self):
        self.find(Locators.FINISH).click()

    def getConfirmationMessage(self):
        return self.find(Locators.CONFIRMATION).text

    def backToProducts(self):
        self.find(Locators.BACK_TO_BROWSER).click()
        from ProductBrowserPage import ProductBrowserPage
        return ProductBrowserPage(self.driver)

    def getCartProducts(self):
        cartProducts = self.find_all(Locators.CART_PRODUCTS)
        order = []

        for item in cartProducts:
            quantity_text = item.find_element(*Locators.ITEM_QUANTITY).text
            quantity = int(quantity_text)
            price_text = item.find_element(*Locators.ITEM_PRICE).text
            price_number = re.search(r"(\d+\.\d+)", price_text)
            if price_number:
                price = Decimal(price_number.group(1))
                order.append(price * quantity)
            else:
                raise ValueError(f"Could not parse price from: {price_text}")

        return order
    
    def getDisplayedTotals(self):
        """ Extracts the totals from the page as Decimal objects, stripping labels like 'Item total: $' or 'Tax: $' """
        subtotal = self.find(Locators.SUBTOTAL).text
        
        def extract_decimal(locator):
            label = self.find(locator).text
            # Find the first sequence that looks like a number (e.g., 29.99)
            match = re.search(r"(\d+\.\d+)", label)
            if match:
                return Decimal(match.group(1))
            raise ValueError(f"Could not find a price in text: '{label}'")


        subtotal = extract_decimal(Locators.SUBTOTAL)
        tax = extract_decimal(Locators.TAX)
        total = extract_decimal(Locators.TOTAL)

        return subtotal, tax, total

