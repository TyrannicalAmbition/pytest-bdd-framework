from components.locators.base_element import BaseElement


class InputElement(BaseElement):
    def set_value(self, value: str) -> "InputElement":
        self.clear_and_send_value(value)
        return self

    def get_value(self) -> str:
        return self.value()

    def get_placeholder(self) -> str:
        return self.get_attribute("placeholder")

    def is_required(self) -> bool:
        return self.get_attribute("required") is not None
