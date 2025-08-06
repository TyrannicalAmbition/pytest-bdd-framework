import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ex_con

from components.base.base_wait import WaitUntil
from components.locators.base_element import BaseElement
from components.locators.buttons import ButtonElement
from components.locators.text_inputs import InputElement


class BasePage:
    def __init__(self, driver: WebDriver, page_url: str):
        self.driver = driver
        self.page_url = page_url
        self.wait = WaitUntil(driver)

    def is_opened(self):
        with allure.step(f"Page {self.page_url} is opened"):
            return self.wait.safe_until(ex_con.url_to_be(self.page_url))

    def go_to_page(self):
        with allure.step(f"Open {self.page_url} page"):
            self.driver.get(self.page_url)
        self.is_opened()

    def element(self, by: str, locator: str, timeout: float = 10) -> BaseElement:
        return BaseElement(self.driver, by, locator, timeout)

    def input_element(self, by: str, locator: str, timeout: float = 10) -> InputElement:
        return InputElement(self.driver, by, locator, timeout)

    def button_element(
        self, by: str, locator: str, timeout: float = 10
    ) -> ButtonElement:
        return ButtonElement(self.driver, by, locator, timeout)
