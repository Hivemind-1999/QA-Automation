import pytest
import random
from LoginPage import LoginPage

PRODUCT_NAMES = ["Sauce Labs Backpack",     "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", 
                 "Sauce Labs Fleece Jacket","Sauce Labs Onesie",     "Test.allTheThings() T-Shirt (Red)"]
PRODUCT_PRICES = [29.99, 9.99, 15.99, 49.99, 7.99, 15.99]
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

    names = productBrowser.getAllProductNames()
    assert names == PRODUCT_NAMES

    reversedNames = productBrowser.sort("za")
    assert reversedNames == PRODUCT_NAMES[::-1]

    prices = productBrowser.sort("lohi")
    assert prices == sorted(PRODUCT_PRICES)

    reversedPrices = productBrowser.sort("hilo")
    assert reversedPrices == sorted(PRODUCT_PRICES, reverse=True)



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

    # Get price for each item in Cart, convert to cents to avoid float math
    order = checkoutPage.getCartProducts()
    orderCents = [round(price * 100) for price in order]

    # Get values calculated by the checkout, convert to cents to avoid float math
    subtotal, tax, total = checkoutPage.getDisplayedTotals()
    subtotalCents, taxCents, totalCents = round(subtotal * 100), round(tax * 100), round(total * 100)

    # Check all items together equal displayed subtotal
    assert sum(orderCents) == subtotalCents, f"Subtotal mismatch: {sum(orderCents)} != {subtotalCents}"

    # Check the tax is correctly 8% of the subtotal
    assert taxCents == int(((subtotalCents * SALES_TAX) / 100) + 0.5), f"Tax mismatch: {taxCents} != {int(((subtotalCents * SALES_TAX) / 100) + 0.5)}"

    # Check the subtotal plus tax equal the total asked
    assert totalCents == subtotalCents + taxCents, f"Total mismatch: {totalCents} != {subtotalCents + taxCents}"

    checkoutPage.pressFinish()

    assert checkoutPage.getConfirmationMessage() == "Thank you for your order!"

    productBrowser = checkoutPage.backToProducts()

    