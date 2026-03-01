from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from BasePage import BasePage

class Locators:

    ORIGIN = (By.CSS_SELECTOR, "")
    DESTINATION = (By.CSS_SELECTOR, "")

class FlightSelectorPage(BasePage):

    def __init__(self):
        super().__init__()

    def choose_flight(self, origin, destination):

        origin_picker = self.find(Locators.ORIGIN)
        origin_picker_selector = Select(origin_picker)
        origin_picker_selector.select_by_visible_text(origin)