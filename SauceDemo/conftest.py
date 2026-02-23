import pytest
from selenium import webdriver
from LoginPage import LoginPage
from ProductBrowserPage import ProductBrowserPage

def set_options(options, config):

    if config["mode"] == "Headless":
        options.add_argument("--headless=new")
    options.page_load_strategy == config["page_load_strategy"]

@pytest.fixture(scope="function")
def productBrowser(config):

    if config["browser"] == "Firefox":

        options = webdriver.FirefoxOptions()
        set_options(options, config)
        driver = webdriver.Firefox(options)
        productBrowserPage = LoginPage.open(driver).login("standard_user", "secret_sauce")
        
        yield productBrowserPage

        driver.quit()