import pytest
import random
from CartPage import CartPage
from ProductBrowserPage import ProductBrowserPage
from LoginPage import LoginPage
from CheckoutPage import CheckoutPage

def login(driver):
    loginPage = LoginPage.open(driver)
    loginPage.getReady()

    loginPage.login("standard_user", "secret_sauce")

def test_GetAllProducts(driver):

    login(driver)

    productBrowser = ProductBrowserPage.open(driver)
    productBrowser.getReady()
    products = productBrowser.getAllProductNames()

    assert products[0] == "Sauce Labs Backpack"
    assert products[1] == "Sauce Labs Bike Light"
    assert products[2] == "Sauce Labs Bolt T-Shirt"
    assert products[3] == "Sauce Labs Fleece Jacket"
    assert products[4] == "Sauce Labs Onesie"
    assert products[5] == "Test.allTheThings() T-Shirt (Red)"

@pytest.mark.parametrize("numItems", [(3),(4)])
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

    cartPage = CartPage.open(driver)
    cartPage.getReady()

    itemsInCard = [item.text for item in cartPage.getAllProductsInCart()]

    i = 0
    for item in cartDetails:
        assert item["name"] == itemsInCard[i]
        i += 1

@pytest.mark.parametrize("itemIndex", [(0)])
def test_RemoveFromCart(driver, itemIndex):

    login(driver)

    productBrowser = ProductBrowserPage.open(driver)
    productBrowser.getReady()
    productBrowser.addProduct(itemIndex)

    cartPage = CartPage.open(driver)
    cartPage.getReady()
    cartPage.removeItem()
    assert cartPage.confirmEmptyCart()

@pytest.mark.parametrize("itemIndex, quantity", [(0, 1)])
def test_PurchaseFlow(driver, itemIndex, quantity):

    login(driver)
    productBrowser = ProductBrowserPage.open(driver)
    productBrowser.getReady()
    productBrowser.addProduct(itemIndex)

    checkoutPage = CheckoutPage.open(driver)
    checkoutPage.getReady()
    checkoutPage.pressContinue()

    assert checkoutPage.getErrorMessage() == "Error: First Name is required"