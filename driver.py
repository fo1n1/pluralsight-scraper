from selenium import webdriver


class DriverUtils:
    DRIVER_DIR = r'F:\+pluralsight_dir'
    __driver = None

    @classmethod
    def _create_driver(cls):
        chrome_driver = cls.DRIVER_DIR + "\chromedriver.exe"
        cls.__driver = webdriver.Chrome(chrome_driver)
        cls.__driver.maximize_window()

    @classmethod
    def get_driver(cls):
        if cls.__driver is None:
            cls._create_driver()
        return cls.__driver
