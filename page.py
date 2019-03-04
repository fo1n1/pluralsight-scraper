import time

from driver import DriverUtils


class Page:

    def __init__(self):
        self._driver = DriverUtils.get_driver()

    def find_by(self, xpath):
        return self._driver.find_element_by_xpath(xpath)

    def find_all(self, xpath):
        return self._driver.find_elements_by_xpath(xpath)

    def open_page(self, url):
        self._driver.get(url)

    def wait_a_bit(self, seconds):
        time.sleep(seconds)
