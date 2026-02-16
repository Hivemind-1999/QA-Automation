import pytest
import random
from CartPage import CartPage
from ProductBrowserPage import ProductBrowserPage
from LoginPage import LoginPage

def login(driver):
    loginPage = LoginPage.navigate(driver)
    #loginPage.navigate_to()
    loginPage.getReady()

    loginPage.login("standard_user", "secret_sauce")

def test_GetAllProducts(driver):

    login(driver)

    productBrowser = ProductBrowserPage.navigate(driver)
    productBrowser.getReady()
    products = productBrowser.getAllProductNames()

    assert products[0] == "Sauce Labs Backpack"
    assert products[1] == "Sauce Labs Bike Light"
    assert products[2] == "Sauce Labs Bolt T-Shirt"
    assert products[3] == "Sauce Labs Fleece Jacket"
    assert products[4] == "Sauce Labs Onesie"
    assert products[5] == "Test.allTheThings() T-Shirt (Red)"

#@pytest.mark.parametrize("numItems", [(2),(3),(4)])
@pytest.mark.parametrize("numItems", [(1)])
def test_AddProductsToCart(driver, numItems):
    
    login(driver)

    productBrowser = ProductBrowserPage(driver)
    productBrowser.getReady()
    products = productBrowser.getAllProducts()

    if numItems > len(products):
        raise Exception("Error! Not enough item types")

    itemOrder = random.sample(range(len(products)), numItems)
    cartDetails = []

    for i in itemOrder:
        itemDetails = productBrowser.addProduct(i)
        cartDetails.append(itemDetails)

    assert numItems == productBrowser.getCartBadgeNum()

    cartPage = CartPage.navigate(driver)
    cartPage.getReady()

    for item in cartDetails:
        assert item["name"] == cartPage.getAllProductsInCart()[0]