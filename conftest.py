import os
import json
import pytest
from selenium import webdriver

@pytest.fixture
def config(scope="session"):

    with open(os.getcwd() + "\\config\\test_config.json") as config_file:
        config = json.load(config_file)
    
    return config

print(os.getcwd() + "/conftest.py")

def set_options(options, config):

    if config["mode"] == "Headless":
        options.add_argument("--headless=new")
    options.page_load_strategy == config["page_load_strategy"]

@pytest.fixture
def driver(config):

    if config["browser"] == "Firefox":

        options = webdriver.FirefoxOptions()
        set_options(options, config)
        driver = webdriver.Firefox(options)

    else:

        raise Exception("Unknown type of browser")
    
    driver.implicitly_wait(config["implicit_wait"])

    yield driver

    driver.quit()