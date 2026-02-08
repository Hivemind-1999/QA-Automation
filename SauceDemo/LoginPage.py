from BasePage import BasePage
from selenium.webdriver.common.by import By

class Locators:

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By. ID, "login-button")

class LoginPage(BasePage):

    ERROR_BOX = (By.CSS_SELECTOR, "div[class='login-box']")

    def __init__(self, driver):
        super().__init__(driver)

    def getReady(self):
        return self.find((By.ID, "user-name"))

    def login(self, username, password):
        self.enter_text(Locators.USERNAME, username)
        self.enter_text(Locators.PASSWORD, password)
        self.click(Locators.LOGIN_BUTTON)

    def getErrorMessage(self):
        error_widget = self.find(self.ERROR_BOX)
        return error_widget.find_element(By.TAG_NAME, "h3").text
    
    def clearLogin(self):
        self.clear_input(Locators.USERNAME)
        self.clear_input(Locators.PASSWORD)