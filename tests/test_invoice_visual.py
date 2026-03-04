import os
import pytest
from pages.invoice_page import InvoiceHomePage
from utils.pdf_utils import wait_for_pdf, clear_downloads, run_image_tester


def test_invoiceVisual(browser, eyes, config):
    download_dir = os.path.abspath(config['download_dir'])
    clear_downloads(download_dir)

    invoice_page = InvoiceHomePage(browser, eyes)

    try:
        if eyes:
            eyes.open(browser, "Invoice", "Invoice Visual Test",
                      viewport_size={'width': 1200, 'height': 800})

        # 1. Capture initial form state
        invoice_page.load()
        invoice_page.visual_check("Invoice Form - Initial State")

        # 2. Fill form with 3 rows
        invoice_page.enterCompanyName("Anthropic Ltd")
        invoice_page.fillRow1("Software Development", "10", "500.00")
        invoice_page.fillRow2("Consulting Services", "5", "300.00")
        invoice_page.fillRow3("QA Testing", "8", "200.00")
        invoice_page.visual_check("Invoice Form - Filled")

        # 3. Capture PDF popup
        invoice_page.clickGetPDFButton()
        invoice_page.visual_check("PDF Popup")

        # 4. Download PDF
        invoice_page.clickDownloadPDF()
        pdf_file = wait_for_pdf(download_dir)
        assert pdf_file is not None, "PDF was not downloaded within 30 seconds"

        # 5. Run ImageTester on downloaded PDF
        if eyes:
            run_image_tester(
                config['applitools_api_key'],
                config['image_tester_jar'],
                pdf_file
            )

    finally:
        if eyes:
            results = eyes.close(False)
            print(f"Visual results: {results.url}")
