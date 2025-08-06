import allure

from components.base.base_page import BasePage
from components.config.urls import LOGIN_PAGE_URL


class LoginPage(BasePage):
    def __init__(self, driver, page_url=None):
        if page_url is None:
            page_url = LOGIN_PAGE_URL
        super().__init__(driver, page_url)
        self._init_elements()

    def _init_elements(self):
        self.email_input = self.input_element("css", 'input[type="email"]')
        self.password_input = self.input_element("css", 'input[type="password"]')
        self.login_button = self.button_element("css", 'ion-button[type="button"]')
        self.login_error = self.element("css", 'ion-label[color="danger"]')
        self.validation_error_overlay = self.element(
            "css", 'ion-label[class~="notification__summary"]'
        )

    @allure.step("Fill email field")
    def fill_email(self, email: str) -> "LoginPage":
        self.email_input.click()
        self.email_input.set_value(email)
        return self

    @allure.step("Fill password field")
    def fill_password(self, password: str) -> "LoginPage":
        self.password_input.click()
        self.password_input.set_value(password)
        return self

    @allure.step("Click login button")
    def click_login_button(self) -> "LoginPage":
        if self.login_button.is_disabled():
            return self
        self.login_button.safe_click()
        return self

    @allure.step("Login with credentials")
    def login(self, email: str, password: str) -> "LoginPage":
        self.fill_email(email)
        self.fill_password(password)
        self.click_login_button()
        return self

    @allure.step("Check if login form is visible")
    def is_login_form_present(self) -> bool:
        return (
            self.email_input.is_present()
            and self.password_input.is_present()
            and self.login_button.is_present()
        )

    @allure.step("Get email field value")
    def get_email_value(self) -> str:
        return self.email_input.get_value()

    @allure.step("Get password field value")
    def get_password_value(self) -> str:
        return self.password_input.get_value()

    @allure.step("Check if email validation error is present")
    def is_email_validation_error_present(self) -> bool:
        try:
            self.login_error.wait_for_presence()
            return True
        except Exception:
            return False

    @allure.step("Check if validation error overlay is present")
    def is_validation_error_overlay_present(self) -> bool:
        try:
            self.validation_error_overlay.wait_for_presence()
            return True
        except Exception:
            return False
