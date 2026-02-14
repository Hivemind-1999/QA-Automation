from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com"
TIMEOUT = 10

class BasePage:

    @classmethod
    def navigate(cls, driver):
        page = cls(driver)
        page.navigate_to()
        return page

    def __init__(self, driver, url=BASE_URL):
        self.driver = driver
        self.url = url

    def find(self, locator):
        return WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located(locator))
    
    def find_all(self, locator):
        return WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_all_elements_located(locator))
    
    def navigate_to(self):
        return self.driver.get(self.url)
    
    def click(self, locator):
        return self.find(locator).click()
    
    def enter_text(self, locator, text):
        return self.find(locator).send_keys(text)
    
    def clear_input(self, locator):
        return self.find(locator).clear()
    
    def getTitle(self):
        return self.driver.title