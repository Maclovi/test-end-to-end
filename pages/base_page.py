import math

from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .locators import BasePageLocators


class BasePage:
    def __init__(self, browser: WebDriver, url: str, timeout: int = 10) -> None:
        self.browser = browser
        self.url = url
        browser.implicitly_wait(timeout)

    def open(self) -> None:
        self.browser.get(self.url)

    def jump_to_busket(self) -> None:
        self.browser.find_element(*BasePageLocators.JUMP_TO_BUSKET).click()

    def is_element_present(self, how: str, what: str) -> bool:
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(
        self, how: str, what: str, timeout: int = 4
    ) -> bool:
        try:
            WebDriverWait(self.browser, timeout).until(
                ec.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how: str, what: str, timeout: int = 4) -> bool:
        try:
            WebDriverWait(
                self.browser, timeout, 1, [TimeoutException]
            ).until_not(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def go_to_login_page(self) -> None:
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def should_be_login_link(self) -> None:
        assert self.is_element_present(
            *BasePageLocators.LOGIN_LINK
        ), "Login link is not presented"

    def should_be_authorized_user(self) -> None:
        assert self.is_element_present(
            *BasePageLocators.USER_ICON
        ), "User icon is not presented, probably unauthorised user"

    def solve_quiz_and_get_code(self) -> None:
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs(12 * math.sin(float(x)))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")
