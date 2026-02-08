import pytest
from selenium.webdriver.common.by import By

from LoginPage import LoginPage

@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_Success(driver, username, password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.getReady()

	loginPage.login(username, password)

	site_header = loginPage.find((By.CLASS_NAME, "title")).text
	assert site_header == "Products"

@pytest.mark.parametrize("username, password", [("standard_user", "12345")])
def test_Wrong_Password(driver, username, password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.getReady()

	loginPage.login(username, password)

	error_message = loginPage.getErrorMessage()
	assert error_message == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.parametrize("username, password", [("locked_out_user", "secret_sauce")])
def test_User_Locked_Out(driver, username, password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.getReady()

	loginPage.login(username, password)

	error_message = loginPage.getErrorMessage()
	assert error_message == "Epic sadface: Sorry, this user has been locked out."

@pytest.mark.parametrize("username, incorrect_password, correct_password", [("standard_user", "12345", "secret_sauce")])
def test_Relogin_After_Error(driver, username, incorrect_password, correct_password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.getReady()

	loginPage.login(username, incorrect_password)
	loginPage.clearLogin()
	loginPage.login(username, correct_password)

	site_header = loginPage.find((By.CLASS_NAME, "title")).text
	assert site_header == "Products"