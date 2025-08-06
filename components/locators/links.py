from components.locators.base_element import BaseElement


class LinkElement(BaseElement):
    def get_href(self) -> str:
        return self.get_attribute("href")

    def click_and_wait_for_page_load(self) -> "LinkElement":
        self.click()
        self.wait.safe_until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
        return self
