import pytest

from ProductBrowserPage import ProductBrowserPage
from LoginPage import LoginPage

def login(driver):
    loginPage = LoginPage(driver)
    loginPage.navigate_to()
    loginPage.getReady()

    loginPage.login("standard_user", "secret_sauce")

def test_GetAllProducts(driver):

    login(driver)

    productBrowser = ProductBrowserPage(driver)
    productBrowser.getReady()
    products = productBrowser.getAllProductNames()

    assert products[0] == "Sauce Labs Backpack"
    assert products[1] == "Sauce Labs Bike Light"
    assert products[2] == "Sauce Labs Bolt T-Shirt"
    assert products[3] == "Sauce Labs Fleece Jacket"
    assert products[4] == "Sauce Labs Onesie"
    assert products[5] == "Test.allTheThings() T-Shirt (Red)"