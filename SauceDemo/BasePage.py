from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com"
TIMEOUT = 10

class BasePage:

    def __init__(self, driver, url=BASE_URL):
        self.driver = driver
        self.url = url

    def find(self, locator):
        return WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located(locator))
    
    def navigate_to(self):
        return self.driver.get(self.url)
    
    def click(self, locator):
        return self.find(locator).click()
    
    def enter_text(self, locator, text):
        return self.find(locator).send_keys(text)
    
    def getTitle(self):
        return self.driver.title
    

class Locators:

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By. ID, "login-button")

    def getItemByID(self, id):
        return (By.ID, f"item_{id}_title_link")