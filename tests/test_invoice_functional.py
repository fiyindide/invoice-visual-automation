import os
import pytest
from pages.invoice_page import InvoiceHomePage
from utils.pdf_utils import wait_for_pdf, clear_downloads

def test_singleItemInvoice(browser, config):
    download_dir = os.path.abspath(config['download_dir'])
    clear_downloads(download_dir)

    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    invoice_page.enterCompanyName("Anthropic Ltd")
    invoice_page.fillRow1("Software Development Services", "10", "500.00")

    invoice_page.clickGetPDFButton()
    invoice_page.clickDownloadPDF()

    pdf_file = wait_for_pdf(download_dir)
    assert pdf_file is not None, "PDF was not downloaded within 30 seconds"

@pytest.mark.parametrize("company, rows", [
    ("Anthropic Ltd", [
        ("Software Development", "10", "500.00"),
        ("Consulting Services", "5", "300.00"),
        ("UI Design", "8", "200.00"),
        ("QA Testing", "12", "150.00"),
        ("DevOps Support", "6", "400.00"),
        ("Project Management", "4", "350.00"),
        ("Technical Writing", "3", "250.00"),
        ("Code Review", "7", "175.00"),
    ]),
    ("Google Inc", [
        ("Cloud Infrastructure", "20", "150.00"),
        ("Data Engineering", "15", "200.00"),
        ("ML Pipeline", "10", "300.00"),
        ("Security Audit", "5", "400.00"),
        ("API Development", "8", "250.00"),
        ("Database Admin", "6", "175.00"),
        ("DevOps", "4", "350.00"),
        ("Documentation", "3", "100.00"),
    ]),
])


def test_maxItemsInvoice(browser, config, company, rows):
    download_dir = os.path.abspath(config['download_dir'])
    clear_downloads(download_dir)

    invoice_page = InvoiceHomePage(browser)
    invoice_page.load()
    invoice_page.enterCompanyName(company)

    fill_methods = [
        invoice_page.fillRow1,
        invoice_page.fillRow2,
        invoice_page.fillRow3,
        invoice_page.fillRow4,
        invoice_page.fillRow5,
        invoice_page.fillRow6,
        invoice_page.fillRow7,
        invoice_page.fillRow8,
    ]

    for fill_method, (description, quantity, price) in zip(fill_methods, rows):
        fill_method(description, quantity, price)

    invoice_page.clickGetPDFButton()
    invoice_page.clickDownloadPDF()

    pdf_file = wait_for_pdf(download_dir)
    assert pdf_file is not None, f"PDF was not downloaded for company: {company}"

def test_emptyCompanyName(browser, config):
    download_dir = os.path.abspath(config['download_dir'])
    clear_downloads(download_dir)

    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    # Deliberately skip enterCompanyName
    invoice_page.fillRow1("Software Development", "10", "500.00")

    invoice_page.clickGetPDFButton()
    invoice_page.clickDownloadPDF()

    pdf_file = wait_for_pdf(download_dir)
    assert pdf_file is not None, "PDF should download even without company name"


def test_invalidQuantityWithPrice(browser):
    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    invoice_page.fillRow1("Software Development", "abc", "500.00")

    row_total = invoice_page.getRow1Total()
    assert row_total == "500.00", f"Expected 500.00 (qty treated as 1) but got: {row_total}"


def test_invalidQuantityWithoutPrice(browser):
    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    invoice_page.fillRow1("Software Development", "abc", "")

    subtotal = invoice_page.getSubtotal()
    assert "NaN" in subtotal, f"Expected NaN in subtotal but got: {subtotal}"


def test_invalidPrice(browser):
    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    invoice_page.fillRow1("Software Development", "10", "abc")

    total = invoice_page.getTotal()
    assert "NaN" in total, f"Expected NaN in total but got: {total}"


def test_zeroQuantity(browser):
    invoice_page = InvoiceHomePage(browser)

    invoice_page.load()
    invoice_page.fillRow1("Software Development", "0", "500.00")

    row_total = invoice_page.getRow1Total()
    assert row_total == "-", f"Expected 0.00 but got: {row_total}"


# def test_invoiceGeneration(browser, eyes, config):
#     invoice_page = InvoiceHomePage(browser, eyes)
#
#     try:
#         if eyes:
#             eyes.open(browser, "Invoice", "Invoice Generation Visual Test",
#                       viewport_size={'width': 1200, 'height': 800})
#
#         # 1. Load page
#         invoice_page.load()
#         invoice_page.visual_check("Invoice Form - Initial State")
#
#         # 2. Fill in the form
#         invoice_page.enterCompanyName("Anthropic Ltd")
#         invoice_page.fillRow1("Software Development Services", "10", "500.00")
#         invoice_page.fillRow2("Consulting Services", "5", "300.00")
#         invoice_page.visual_check("Invoice Form - Filled")
#
#         # 3. Download the PDF
#         invoice_page.clickGetPDFButton()
#         invoice_page.visual_check("PDF Popup")
#         invoice_page.clickDownloadPDF()
#
#         # 4. Wait for PDF to land in downloads folder
#         download_dir = os.path.abspath(config['download_dir'])
#         pdf_file = wait_for_pdf(download_dir)
#         assert pdf_file is not None, "PDF was not downloaded within 30 seconds"
#
#         # 5. Run ImageTester on the downloaded PDF
#         if eyes:
#             run_image_tester(
#                 config['applitools_api_key'],
#                 config['image_tester_jar'],
#                 pdf_file
#             )
#
#     finally:
#         if eyes:
#             results = eyes.close(False)
#             print(f"Visual results: {results.url}")
#
#
