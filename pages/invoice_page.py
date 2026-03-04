
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InvoiceHomePage(BasePage):
    URL = "https://invoiceto.me"

    # Header
    COMPANY_NAME = (By.CSS_SELECTOR, "#header #company")
    BODY = (By.TAG_NAME, "body")

    # Buttons
    GET_PDF_BUTTON = (By.ID, "open_pp")
    DOWNLOAD_PDF_BUTTON = (By.CSS_SELECTOR, ".cta.generate_pdf")

    # Row 1
    ROW1_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(1) td:nth-child(2) input")
    ROW1_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(1) td:nth-child(3) input")
    ROW1_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(1) td:nth-child(4) input")
    ROW1_TOTAL       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(1) td.noteditable:last-child")

    # Row 2
    ROW2_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(2) td:nth-child(2) input")
    ROW2_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(2) td:nth-child(3) input")
    ROW2_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(2) td:nth-child(4) input")

    # Row 3
    ROW3_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(3) td:nth-child(2) input")
    ROW3_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(3) td:nth-child(3) input")
    ROW3_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(3) td:nth-child(4) input")

    # Row 4
    ROW4_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(4) td:nth-child(2) input")
    ROW4_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(4) td:nth-child(3) input")
    ROW4_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(4) td:nth-child(4) input")

    # Row 5
    ROW5_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(5) td:nth-child(2) input")
    ROW5_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(5) td:nth-child(3) input")
    ROW5_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(5) td:nth-child(4) input")

    # Row 6
    ROW6_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(6) td:nth-child(2) input")
    ROW6_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(6) td:nth-child(3) input")
    ROW6_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(6) td:nth-child(4) input")

    # Row 7
    ROW7_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(7) td:nth-child(2) input")
    ROW7_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(7) td:nth-child(3) input")
    ROW7_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(7) td:nth-child(4) input")

    # Row 8
    ROW8_DESCRIPTION = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(8) td:nth-child(2) input")
    ROW8_QUANTITY    = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(8) td:nth-child(3) input")
    ROW8_PRICE       = (By.CSS_SELECTOR, "#invoice tbody tr:nth-child(8) td:nth-child(4) input")

    # Summary fields
    SUBTOTAL = (By.ID, "formsubtotal")
    TAX      = (By.ID, "formtax")
    TOTAL    = (By.ID, "formtotal")

    # ---------- ACTIONS ----------

    def load(self):
        self.browser.get(self.URL)

    def enterCompanyName(self, name):
        self.type(self.COMPANY_NAME, name)

    def triggerUpdate(self):
        self.click(self.BODY)

    def fillRow(self, description_locator, quantity_locator, price_locator,
                description, quantity, price):
        self.type(description_locator, description)
        self.type(quantity_locator, quantity)
        self.type(price_locator, price)
        self.triggerUpdate()

    def fillRow1(self, description, quantity, price):
        self.fillRow(self.ROW1_DESCRIPTION, self.ROW1_QUANTITY,
                     self.ROW1_PRICE, description, quantity, price)

    def fillRow2(self, description, quantity, price):
        self.fillRow(self.ROW2_DESCRIPTION, self.ROW2_QUANTITY,
                     self.ROW2_PRICE, description, quantity, price)

    def fillRow3(self, description, quantity, price):
        self.fillRow(self.ROW3_DESCRIPTION, self.ROW3_QUANTITY,
                     self.ROW3_PRICE, description, quantity, price)

    def fillRow4(self, description, quantity, price):
        self.fillRow(self.ROW4_DESCRIPTION, self.ROW4_QUANTITY,
                     self.ROW4_PRICE, description, quantity, price)

    def fillRow5(self, description, quantity, price):
        self.fillRow(self.ROW5_DESCRIPTION, self.ROW5_QUANTITY,
                     self.ROW5_PRICE, description, quantity, price)

    def fillRow6(self, description, quantity, price):
        self.fillRow(self.ROW6_DESCRIPTION, self.ROW6_QUANTITY,
                     self.ROW6_PRICE, description, quantity, price)

    def fillRow7(self, description, quantity, price):
        self.fillRow(self.ROW7_DESCRIPTION, self.ROW7_QUANTITY,
                     self.ROW7_PRICE, description, quantity, price)

    def fillRow8(self, description, quantity, price):
        self.fillRow(self.ROW8_DESCRIPTION, self.ROW8_QUANTITY,
                     self.ROW8_PRICE, description, quantity, price)

    def clickGetPDFButton(self):
        self.click(self.GET_PDF_BUTTON)

    def clickDownloadPDF(self):
        self.click(self.DOWNLOAD_PDF_BUTTON)

    # ---------- GETTERS ----------

    def getRow1Total(self):
        return self.get_text(self.ROW1_TOTAL)

    def getSubtotal(self):
        return self.get_text(self.SUBTOTAL)

    def getTax(self):
        return self.get_text(self.TAX)

    def getTotal(self):
        return self.get_text(self.TOTAL)