import pytest
import random
from decimal import Decimal, ROUND_HALF_UP
from LoginPage import LoginPage

PRODUCT_NAMES = ["Sauce Labs Backpack",     "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", 
                 "Sauce Labs Fleece Jacket","Sauce Labs Onesie",     "Test.allTheThings() T-Shirt (Red)"]
PRODUCT_PRICES = [Decimal("29.99"), Decimal("9.99"), Decimal("15.99"), Decimal("49.99"), Decimal("7.99"), Decimal("15.99")]
SALES_TAX = Decimal("0.08")

def test_GetAllProducts(driver):

    productBrowser = LoginPage.open(driver).login("standard_user", "secret_sauce")
    products = productBrowser.getAllProductNames()

    assert products == PRODUCT_NAMES


@pytest.mark.parametrize("numItems", range(1, 7))
def test_AddProductsToCart(productBrowser, numItems):
    
    products = productBrowser.getAllProductNames()
    if numItems > len(products):
        pytest.skip("Requested to add more distinguished item types than we sell!")

    # Pick a random selection of X items, where X = numItems
    itemOrder = random.sample(range(len(products)), numItems)
    cartDetails = []

    for i in itemOrder:
        itemDetails = productBrowser.addProduct(i)
        cartDetails.append(itemDetails["name"])

        # Test the Shopping Cars icon tracks the items we add
        assert len(cartDetails) == productBrowser.getCartBadgeNum()

    cartPage = productBrowser.goToCart()

    itemsInCart = [item.text for item in cartPage.getAllProductsInCart()]

    assert cartDetails == itemsInCart


def test_Sorting(productBrowser):

    # Test A-Z sorting (default view of the Products page)
    names = productBrowser.getAllProductNames()
    assert names == PRODUCT_NAMES

    # Test Z-A sorting
    reversedNames = productBrowser.sort("za")
    assert reversedNames == PRODUCT_NAMES[::-1]

    # Test Low-High Price sorting
    prices = productBrowser.sort("lohi")
    assert prices == sorted(PRODUCT_PRICES)

    # Test High-Low Price sorting
    reversedPrices = productBrowser.sort("hilo")
    assert reversedPrices == sorted(PRODUCT_PRICES, reverse=True)


@pytest.mark.parametrize("itemIndex", range(1))
def test_RemoveFromCart(productBrowser, itemIndex):

    productBrowser.addProduct(itemIndex)
    cartPage = productBrowser.goToCart()

    assert cartPage.getAllProductsInCart()

    cartPage.removeItem()
    assert cartPage.confirmEmptyCart()

@pytest.mark.parametrize("itemIndex", [1])
def test_PurchaseFlow(productBrowser, itemIndex):

    productBrowser.addProduct(itemIndex)
    cartPage = productBrowser.goToCart()
    checkoutPage = cartPage.goToCheckout()

    assert checkoutPage.getTitle() == "Checkout: Your Information"

    checkoutPage.enterBuyerInfo("First", "Last", "12345")
    checkoutPage.pressContinue()

    assert checkoutPage.getTitle() == "Checkout: Overview"

    order_items = checkoutPage.getCartProducts() 
    subtotal, tax, total = checkoutPage.getDisplayedTotals()

    assert sum(order_items) == subtotal, f"Subtotal mismatch: {sum(order_items)} != {subtotal}"

    expected_tax = (subtotal * SALES_TAX).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    assert tax == expected_tax, f"Tax mismatch: {tax} != {expected_tax}"

    assert total == subtotal + tax, f"Total mismatch: {total} != {subtotal + tax}"

    checkoutPage.pressFinish()
    assert checkoutPage.getConfirmationMessage() == "Thank you for your order!"

    productBrowser = checkoutPage.backToProducts()
    assert productBrowser.getTitle() == "Products"

@pytest.mark.parametrize("itemIndex", [(1)])
def test_IncorrectCheckout(productBrowser, itemIndex):

    productBrowser.addProduct(itemIndex)
    cartPage = productBrowser.goToCart()
    checkoutPage = cartPage.goToCheckout()

    checkoutPage.pressContinue()
    assert checkoutPage.getErrorMessage() == "Error: First Name is required"

    checkoutPage.enterFirstName("First")
    
    checkoutPage.pressContinue()
    assert checkoutPage.getErrorMessage() == "Error: Last Name is required"

    checkoutPage.enterLastName("Last")
    
    checkoutPage.pressContinue()
    assert checkoutPage.getErrorMessage() == "Error: Postal Code is required"

    checkoutPage.enterZip("12345")
    checkoutPage.pressContinue()

    assert checkoutPage.getTitle() == "Checkout: Overview"