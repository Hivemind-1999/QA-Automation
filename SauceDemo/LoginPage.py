from BasePage import BasePage, Locators

class LoginPage(BasePage):

    ERROR_BOX = (By.CSS_SELECTOR, "div[class='login-box']")

    def __init__(self, driver):
        super().__init__(driver)
        print("Hello")

    def login(self, username, password):
        self.enter_text(Locators.USERNAME, username)
        self.enter_text(Locators.PASSWORD, password)
        self.click(Locators.LOGIN_BUTTON)

    def getErrorMessage(self):
        error_widget = self.find(self.ERROR_BOX)
        return error_widget.find_element(By.TAG_NAME, "h3").text