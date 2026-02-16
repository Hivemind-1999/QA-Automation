from selenium.webdriver.common.by import By
from BasePage import BasePage

BASE_URL = "https://www.saucedemo.com/checkout-step-one.html"

class Locators:

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CONTINUE = (By.CSS_SELECTOR, "#continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url=BASE_URL)

    def getReady(self):
        return self.find(Locators.TITLE)

    def getErrorMessage(self):
        return self.find(Locators.ERROR_MESSAGE).text

    def pressContinue(self):
        self.find(Locators.CONTINUE).click()