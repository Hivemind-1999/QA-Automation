from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.blazedemo.com"
TIMEOUT = 10

class BasePage:

    @classmethod
    def open(cls, driver):
        page = cls(driver)
        page.driver.get(BASE_URL)
        return page

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator):
        return WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located(locator))
    
    def enter_text(self, locator, text):
        return self.find(locator).send_keys(text)