from page import Page
from selenium.common.exceptions import NoSuchElementException

LOGIN_PAGE_URL = 'https://app.pluralsight.com/id?redirectTo=%2Fid%2Fdashboard'
LOGIN_INPUT = "//input[@name='Username']"
PASSWORD_INPUT = "//input[@name='Password']"
LOGIN_BUTTON = "//button[@id='login']"


class Login(Page):
    def is_user_logged_in(self):
        try:
            self.find_by("login")
        except NoSuchElementException:
            return False
        return True

    def login(self, login, password):
        self.open_page(LOGIN_PAGE_URL)
        self.find_by(LOGIN_INPUT).send_keys(login)
        self.find_by(PASSWORD_INPUT).send_keys(password)
        self.find_by(LOGIN_BUTTON).click()
        self.wait_a_bit(10)
