import math
import pytest
import random
from LoginPage import LoginPage

PRODUCT_NAMES = ["Sauce Labs Backpack",     "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", 
                 "Sauce Labs Fleece Jacket","Sauce Labs Onesie",     "Test.allTheThings() T-Shirt (Red)"]
SALES_TAX = 8

def test_GetAllProducts(driver):

    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")
    products = productBrowser.getAllProductNames()

    assert products == PRODUCT_NAMES

@pytest.mark.parametrize("numItems", [(3),(4)])
def test_AddProductsToCart(driver, numItems):
    
    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")
    products = productBrowser.getAllProductNames()

    if numItems > len(products):
        raise Exception("Error! Not enough item types")

    itemOrder = random.sample(range(len(products)), numItems)
    cartDetails = []

    for i in itemOrder:
        itemDetails = productBrowser.addProduct(i)
        cartDetails.append(itemDetails)

    assert numItems == productBrowser.getCartBadgeNum()

    cartPage = productBrowser.goToCart()
    cartPage.getReady()

    itemsInCard = [item.text for item in cartPage.getAllProductsInCart()]

    i = 0
    for item in cartDetails:
        assert item["name"] == itemsInCard[i]
        i += 1

def test_Sorting(driver):

    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")

    products = productBrowser.getAllProductNames()
    assert products == PRODUCT_NAMES

    reversedOrder = productBrowser.sort("za")
    assert reversedOrder == PRODUCT_NAMES[::-1]

    products = productBrowser.productBrowser.sort("lohi")
    #assert products == PRODUCT_NAMES

    reversedOrder = productBrowser.sort("hilo")
    #assert reversedOrder == PRODUCT_NAMES[::-1]



@pytest.mark.parametrize("itemIndex", [(0)])
def test_RemoveFromCart(driver, itemIndex):

    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")
    productBrowser.addProduct(itemIndex)

    cartPage = productBrowser.goToCart()
    #cartPage.getReady()
    cartPage.removeItem()
    assert cartPage.confirmEmptyCart()

@pytest.mark.parametrize("itemIndex", [(1)])
def test_PurchaseFlow(driver, itemIndex):

    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")
    productBrowser.addProduct(itemIndex)

    cartPage = productBrowser.goToCart()
    checkoutPage = cartPage.goToCheckout()

    assert checkoutPage.getPageTitle() == "Checkout: Your Information"
    
    #checkoutPage.pressContinue()
    #assert checkoutPage.getErrorMessage() == "Error: First Name is required"

    checkoutPage.enterFirstName("First")
    
    #checkoutPage.pressContinue()
    #assert checkoutPage.getErrorMessage() == "Error: Last Name is required"

    checkoutPage.enterLastName("Last")
    
    #checkoutPage.pressContinue()
    #assert checkoutPage.getErrorMessage() == "Error: Postal Code is required"

    checkoutPage.enterZip("12345")
    checkoutPage.pressContinue()

    assert checkoutPage.getPageTitle() == "Checkout: Overview"

    order = checkoutPage.getCartProducts()
    subtotal, tax, total = checkoutPage.getDisplayedTotals()
    subtotal = int(subtotal * 100)
    tax = int(tax * 100)
    total = int(total * 100)

    assert sum(order) * 100 == subtotal
    assert tax == int(subtotal / SALES_TAX)
    assert total == subtotal + tax

    