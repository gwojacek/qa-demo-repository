class MainPage:
    URL = "https://en.wikipedia.org/wiki/Main_Page"

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def get_title(self):
        return self.driver.title

    def search_input_exists(self):
        return self.driver.find_element("name", "search") is not None
