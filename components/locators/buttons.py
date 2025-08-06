from components.locators.base_element import BaseElement


class ButtonElement(BaseElement):
    def is_disabled(self) -> bool:
        return not self.is_enabled()

    def get_button_text(self) -> str:
        return self.text()
