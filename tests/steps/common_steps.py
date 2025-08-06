from pytest_bdd import given, when, then
from selenium.webdriver.remote.webdriver import WebDriver

from components.base.base_wait import WaitUntil
from components.config.urls import TRADING_URL_PATTERN
from components.pages.login_page.login_page import LoginPage


@given("I am on the login page")
def i_am_on_login_page(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.go_to_page()
    return login_page


@when("I click the login button")
def click_login_button(driver: WebDriver):
    login_page = LoginPage(driver)
    login_page.click_login_button()


@then("I should be logged in successfully")
def should_be_logged_in_successfully(driver: WebDriver):
    wait = WaitUntil(driver)
    wait.wait_for_url_contains(TRADING_URL_PATTERN)
    current_url = driver.current_url
    assert TRADING_URL_PATTERN in current_url


@then("I should see validation error")
def should_see_validation_errors(driver: WebDriver):
    login_page = LoginPage(driver)
    assert login_page.is_validation_error_overlay_present()
