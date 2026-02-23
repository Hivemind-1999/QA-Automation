from selenium.webdriver.common.by import By
from BasePage import BasePage

class Locators:

    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CART_ITEM_TEXT = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "#checkout")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove-']")

class CartPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
    
    def getAllProductsInCart(self):
        return self.find_all(Locators.CART_ITEM_TEXT)
    
    def confirmEmptyCart(self):
        """Verifies if the cart is empty by checking for item presence."""
        from selenium.common.exceptions import TimeoutException
        try:
            self.not_found(Locators.CART_ITEM)
            return True
        except TimeoutException:
            return False
    
    def goToCheckout(self):
        self.find(Locators.CHECKOUT_BUTTON).click()
        from CheckoutPage import CheckoutPage
        return CheckoutPage(self.driver)
    
    def removeItem(self):
        self.click(Locators.REMOVE_BUTTONS)