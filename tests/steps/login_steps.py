from pytest_bdd import when, then, parsers
from selenium.webdriver.remote.webdriver import WebDriver

from components.pages.login_page.login_page import LoginPage


@when(parsers.parse('I fill in the email field with "{email}"'))
def fill_email_field(driver: WebDriver, email: str):
    login_page = LoginPage(driver)
    login_page.fill_email(email)


@when(parsers.parse('I fill in the password field with "{password}"'))
def fill_password_field(driver: WebDriver, password: str):
    login_page = LoginPage(driver)
    login_page.fill_password(password)


@then("the login form should be visible")
def login_form_should_be_visible(driver: WebDriver):
    login_page = LoginPage(driver)
    assert login_page.is_login_form_present()


@then("the email field should be empty")
def email_field_should_be_empty(driver: WebDriver):
    login_page = LoginPage(driver)
    email_value = login_page.get_email_value()
    assert email_value == "" or email_value is None


@then("the password field should be empty")
def password_field_should_be_empty(driver: WebDriver):
    login_page = LoginPage(driver)
    password_value = login_page.get_password_value()
    assert password_value == "" or password_value is None


@then(parsers.parse('the email field should contain "{expected_email}"'))
def email_field_should_contain(driver: WebDriver, expected_email: str):
    login_page = LoginPage(driver)
    actual_email = login_page.get_email_value()
    assert actual_email == expected_email


@then(parsers.parse('the password field should contain "{expected_password}"'))
def password_field_should_contain(driver: WebDriver, expected_password: str):
    login_page = LoginPage(driver)
    actual_password = login_page.get_password_value()
    assert actual_password == expected_password


@then("I should see email validation error")
def should_see_email_validation_error(driver: WebDriver):
    login_page = LoginPage(driver)
    assert login_page.is_email_validation_error_present()
