import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com"
@pytest.fixture
def driver():
	options = webdriver.FirefoxOptions()
	options.add_argument("--headless=new")	
	driver = webdriver.Firefox(options=options)
	yield driver

	driver.quit()

@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_Success(driver, username, password):

	driver.get(URL)
	wait = WebDriverWait(driver, 5)
	
	username_handle = (By.ID, "user-name")
	PageReady = EC.presence_of_element_located(username_handle)

	username_input = wait.until(PageReady)
	password_input = driver.find_element(By.ID, "password")
	login_button = driver.find_element(By. ID, "login-button")
	
	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	header_handle = (By.CLASS_NAME, "title")
	site_header = wait.until(EC.presence_of_element_located(header_handle)).text

	assert site_header == "Products"

@pytest.mark.parametrize("username, password", [("standard_user", "12345")])
def test_Wrong_Password(driver, username, password):

	driver.get(URL)
	wait = WebDriverWait(driver, 5)

	username_handle = (By.ID, "user-name")
	PageReady = EC.presence_of_element_located(username_handle)

	username_input = wait.until(PageReady)
	password_input = driver.find_element(By.ID, "password")
	login_button = driver.find_element(By. ID, "login-button")

	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	header_handle = By.CLASS_NAME, "title"

	error_text_handle = By.CSS_SELECTOR, "div[class='login-box']"
	error_block = wait.until(EC.presence_of_element_located(error_text_handle))
	error_text = error_block.find_element(By.TAG_NAME, "h3").text
	print(error_text)

	assert error_text == "Epic sadface: Username and password do not match any user in this service"