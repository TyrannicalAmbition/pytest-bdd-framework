import os
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from components.config.urls import BASE_URL

pytest_plugins = [
    "tests.steps.common_steps",
    "tests.steps.login_steps",
]


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for tests: chrome, firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


def create_driver(browser_name: str, headless: bool = False) -> webdriver.Remote:
    browser_name = browser_name.lower()

    if browser_name == "chrome":
        service = Service(ChromeDriverManager().install())
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    return driver


@pytest.fixture(scope="function")
def driver(request) -> Generator[webdriver.Remote, None, None]:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver_instance = create_driver(browser, headless)
    driver_instance.get(BASE_URL)
    yield driver_instance
    driver_instance.quit()


def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(
                screenshot_dir, f"{item.name}_{call.when}.png"
            )
            try:
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to save screenshot: {e}")
