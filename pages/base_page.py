
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from applitools.selenium import MatchLevel

class BasePage:
    def __init__(self, browser, eyes = None, timeout=10):
        self.browser = browser
        self.eyes = eyes
        self.wait = WebDriverWait(browser, timeout)

    def visual_check(self, tag):
        if self.eyes:
            self.eyes.match_level = MatchLevel.LAYOUT
            self.eyes.check_window(tag)

    def find_visible(self, locator):
        """User-visible interaction: element is present AND visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator):
        """DOM-level checks: Element exists in DOM but may be hidden"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all_present(self, locator):
        """Lists, results, tables: Multiple elements present in DOM"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ---------- ACTIONS ----------

    def click(self, locator):
        """Clicks when element is clickable"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def type(self, locator, text, clear=True):
        """Types into visible input field"""
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)
        return element

    # ---------- UTILITIES ----------

    def get_text(self, locator):
        return self.find_visible(locator).text

    def get_attribute(self, locator, attribute):
        return self.find_present(locator).get_attribute(attribute)
