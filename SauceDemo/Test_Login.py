import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from LoginPage import LoginPage

URL = "https://www.saucedemo.com"

@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_Success(driver, username, password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.find((By.ID, "user-name"))

	loginPage.login(username, password)

	site_header = loginPage.find((By.CLASS_NAME, "title"))
	assert site_header == "Products"

@pytest.mark.parametrize("username, password", [("standard_user", "12345")])
def test_Wrong_Password(driver, username, password):

	loginPage = LoginPage(driver)
	loginPage.navigate_to()
	loginPage.find((By.ID, "user-name"))

	loginPage.login(username, password)

	error_message = loginPage.getErrorMessage()
	assert error_message == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.parametrize("username, password", [("locked_out_user", "secret_sauce")])
def test_User_Locked_Out(driver, username, password):

	driver.get(URL)
	wait = WebDriverWait(driver, 5)

	PageReady = EC.presence_of_element_located((By.ID, "user-name"))
	username_input = wait.until(PageReady)

	password_input = driver.find_element(By.ID, "password")
	login_button = driver.find_element(By. ID, "login-button")

	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	ErrorReady = EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='login-box']"))
	wait.until(ErrorReady)

	error_block = wait.until(ErrorReady)
	error_text = error_block.find_element(By.TAG_NAME, "h3").text

	assert error_text == "Epic sadface: Sorry, this user has been locked out."

@pytest.mark.parametrize("username, password", [("standard_user", "12345")])
def test_Relogin_After_Error(driver, username, password):

	driver.get(URL)
	wait = WebDriverWait(driver, 5)

	PageReady = EC.presence_of_element_located((By.ID, "user-name"))
	username_input = wait.until(PageReady)

	password_input = driver.find_element(By.ID, "password")
	login_button = driver.find_element(By. ID, "login-button")

	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	ErrorReady = EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='login-box']"))
	wait.until(ErrorReady)

	username_input.send_keys("standard_user")
	password_input.send_keys("secret_sauce")

	login_button.click()

	LoginComplete = EC.title_is("Swag Labs")
	wait.until(LoginComplete)

	assert driver.title == "Swag Labs"