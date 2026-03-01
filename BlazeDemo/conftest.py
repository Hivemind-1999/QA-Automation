import pytest
from selenium import webdriver
from FlightSelectorPage import FlightSelectorPage

@pytest.fixture(scope="function")
def flightSelector(config):

    if config["browser"] == "Firefox":
        
        options = webdriver.FirefoxOptions()

        if config["mode"] == "Headless":
            options.add_argument("--headless=new")
        
        options.page_load_strategy = config["page_load_strategy"]

        driver = webdriver.Firefox(options)
        flightSelector = FlightSelectorPage.open(driver)

        yield flightSelector

        driver.quit()


