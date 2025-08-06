from typing import List

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ex_con

from components.base.base_wait import WaitUntil


class BaseElement:
    def __init__(self, driver: WebDriver, by: str, locator: str, timeout: float):
        self.driver = driver
        self.by = self._resolve_by(by)
        self.locator = locator
        self.wait = WaitUntil(driver, timeout)

    @staticmethod
    def _resolve_by(find_by: str) -> str:
        find_by = find_by.lower()
        locating = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "class_name": By.CLASS_NAME,
            "id": By.ID,
            "link_text": By.LINK_TEXT,
            "name": By.NAME,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "tag_name": By.TAG_NAME,
        }
        return locating[find_by]

    def find(self) -> WebElement:
        return self.wait.safe_until(
            ex_con.presence_of_element_located((self.by, self.locator)),
            message=f"Can't find element by {self.by}='{self.locator}'",
        )

    def find_visible(self) -> WebElement:
        return self.wait.safe_until(
            ex_con.visibility_of_element_located((self.by, self.locator)),
            message=f"Can't find visible element by {self.by}='{self.locator}'",
        )

    def find_all(self) -> List[WebElement]:
        return self.driver.find_elements(self.by, self.locator)

    def scroll_into(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click(self) -> "BaseElement":
        element = self.find()
        self.scroll_into(element)
        element.click()
        return self

    def common_click(self) -> "BaseElement":
        element = self.find()
        self.scroll_into(element)
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def safe_click(self) -> "BaseElement":
        element = self.find()
        self.scroll_into(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return self

    def text(self) -> str:
        return self.find().text

    def send_keys(self, value: str) -> "BaseElement":
        element = self.find()
        self.scroll_into(element)
        element.send_keys(value)
        return self

    def get_attribute(self, attr: str) -> str:
        return self.find().get_attribute(attr)

    def value(self) -> str:
        return self.find().get_attribute("value")

    def int_value(self) -> int:
        return int(self.value())

    def clear_and_send_value(self, value: str) -> "BaseElement":
        element = self.find()
        self.scroll_into(element)
        element.clear()
        element.send_keys(value)
        return self

    def is_present(self) -> bool:
        try:
            self.driver.find_element(self.by, self.locator)
            return True
        except Exception:
            return False

    def is_visible(self) -> bool:
        try:
            element = self.find()
            return element.is_displayed()
        except Exception:
            return False

    def is_enabled(self) -> bool:
        try:
            element = self.find()
            return element.is_enabled()
        except Exception:
            return False

    def is_disabled(self) -> bool:
        try:
            element = self.find()
            return (
                element.get_attribute("disabled") is not None
                or not element.is_enabled()
            )
        except Exception:
            return False

    def wait_for_presence(self) -> "BaseElement":
        self.wait.safe_until(
            ex_con.presence_of_element_located((self.by, self.locator))
        )
        return self

    def wait_for_clickable(self) -> "BaseElement":
        self.wait.safe_until(ex_con.element_to_be_clickable((self.by, self.locator)))
        return self

    def wait_for_invisibility(self) -> "BaseElement":
        self.wait.safe_until(
            ex_con.invisibility_of_element_located((self.by, self.locator))
        )
        return self
