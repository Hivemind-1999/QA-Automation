from selenium.webdriver.common.by import By
from BasePage import BasePage

class Locators:

    USERNAME = (By.CSS_SELECTOR, "")

class LoginPage(BasePage):

    def __init__(self):
        super().__init__()

    def login(self, username, password):
        usernameField = self.enter_text(Locators.USERNAME, "username")
