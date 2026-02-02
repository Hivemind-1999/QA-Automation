import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
driver.get(URL)
#driver.maximize_window()

username_handle = By.ID, "user-name"
username_input = wait.until(EC.presence_of_element_located(username_handle))
password_input = driver.find_element(By.ID, "password")
login_button = driver.find_element(By. ID, "login-button")

def Test_Success(username, password):
	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	header_handle = By.CLASS_NAME, "title"
	site_header = wait.until(EC.presence_of_element_located(header_handle)).text

	assert site_header == "Products"

def Test_Wrong_Password(username, password):
	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button.click()

	header_handle = By.CLASS_NAME, "title"

	error_text_handle = By.CSS_SELECTOR, "div[class='login-box']"
	error_block = wait.until(EC.presence_of_element_located(error_text_handle))
	error_text = error_block.find_element(By.TAG_NAME, "h3").text
	print(error_text)

	assert error_text == "Epic sadface: Username and password do not match any user in this service"

#Test_Success("standard_user", "secret_sauce")
Test_Wrong_Password("standard_user", "12345")
