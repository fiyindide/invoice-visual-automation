# Invoice Visual Automation

A Python-based test automation framework for web UI and PDF visual validation of invoice generation workflows. Built using Selenium WebDriver, Applitools Eyes, and the Applitools ImageTester utility, following the Page Object Model (POM) design pattern.

---

## Table of Contents

- [What This Project Tests](#what-this-project-tests)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Page Objects](#page-objects)
- [Test Descriptions](#test-descriptions)
- [How to Run](#how-to-run)
- [Visual Testing Dashboard](#visual-testing-dashboard)
- [How Visual Testing Works](#how-visual-testing-works)
- [Screenshots on Failure](#screenshots-on-failure)
- [Known Behaviors](#known-behaviors)

---

## What This Project Tests

This project automates and visually validates the invoice generation workflow on [invoiceto.me](https://invoiceto.me) — a free, browser-based invoice generator.

The test suite covers:

- **Functional testing** — verifying that the invoice form behaves correctly under various input conditions, including valid data, edge cases, and invalid inputs
- **Visual testing** — capturing snapshots of the web form at key moments and validating the rendered PDF using Applitools Eyes and ImageTester

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| pytest | Test framework and test runner |
| Selenium WebDriver 4.x | Browser automation |
| Applitools Eyes (eyes-selenium) | Web UI visual validation |
| Applitools ImageTester (JAR) | PDF visual validation |
| Java (JDK/JRE) | Required to run ImageTester JAR |
| Google Chrome | Browser used for test execution |

---

## Prerequisites

Before running this project, ensure the following are installed on your machine:

### 1. Python 3.12
Download from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
# Expected: Python 3.12.x
```

### 2. Java (JDK or JRE)
Download from [adoptium.net](https://adoptium.net/) or use an existing IntelliJ JDK.

Verify Java is accessible from your terminal:
```bash
java -version
# Expected: java version "17.x.x" or similar
```

> **Important:** Java must be on your system PATH, not just bundled inside an IDE. If `java -version` fails in your terminal, add Java to your PATH before proceeding.

### 3. Google Chrome
Download from [google.com/chrome](https://www.google.com/chrome/)

> Selenium Manager (included in Selenium 4.6+) automatically manages ChromeDriver. No manual ChromeDriver installation is required.

### 4. Applitools Account
Sign up for a free account at [applitools.com](https://applitools.com) to obtain your API key.

### 5. ImageTester JAR
Download the latest `ImageTester.jar` from the [Applitools ImageTester GitHub releases page](https://github.com/applitools/ImageTester/releases) and place it in the project root directory.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/invoice-visual-automation.git
cd invoice-visual-automation
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get a PowerShell execution policy error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up configuration
Copy the example config and add your Applitools API key:
```bash
copy config.example.json config.json
```
Then open `config.json` and replace `YOUR_API_KEY_HERE` with your actual Applitools API key.

---

## Configuration

The project is driven by `config.json` in the root directory:

```json
{
    "browser": "Chrome",
    "applitools_api_key": "YOUR_API_KEY_HERE",
    "run_visual_test": true,
    "download_dir": "downloads",
    "image_tester_jar": "ImageTester.jar"
}
```

| Key | Description | Options |
|---|---|---|
| `browser` | Browser to run tests in | `Chrome`, `Firefox`, `Headless Chrome` |
| `applitools_api_key` | Your Applitools API key | String |
| `run_visual_test` | Enable or disable visual testing | `true`, `false` |
| `download_dir` | Folder where PDFs are saved | Relative path string |
| `image_tester_jar` | Path to ImageTester JAR file | Filename or relative path |

> **Toggling visual tests off:** Set `"run_visual_test": false` to run only functional tests without sending results to Applitools. All Selenium interactions and assertions still run normally.

---

## Project Structure

```
invoice-visual-automation/
│
├── pages/
│   ├── base_page.py            # Shared Selenium actions and visual check method
│   └── invoiceHomePage.py      # Page object for invoiceto.me
│
├── tests/
│   ├── test_invoice_functional.py   # Functional test suite
│   └── test_invoice_visual.py       # Visual test suite
│
├── utils/
│   └── pdf_utils.py            # Shared helpers: wait_for_pdf, clear_downloads, run_image_tester
│
├── downloads/                  # Downloaded PDFs land here (auto-created)
├── screenshots/                # Failure screenshots saved here (auto-created)
│
├── ImageTester.jar             # Applitools PDF validator (not committed to repo)
├── conftest.py                 # pytest fixtures: browser, eyes, config
├── config.json                 # Local config with API key (not committed to repo)
├── config.example.json         # Safe config template for new users
├── requirements.txt            # Python dependencies
└── README.md
```

---

## Page Objects

### `BasePage`
The foundation class inherited by all page objects. Provides:

| Method | Description |
|---|---|
| `find_visible(locator)` | Waits for element to be visible |
| `find_present(locator)` | Waits for element to be present in DOM |
| `find_all_present(locator)` | Waits for multiple elements in DOM |
| `click(locator)` | Waits for element to be clickable then clicks |
| `type(locator, text)` | Clears and types into a visible input field |
| `get_text(locator)` | Returns visible text of an element |
| `get_attribute(locator, attribute)` | Returns an attribute value of an element |
| `visual_check(tag)` | Captures Applitools snapshot if Eyes is initialized |

### `InvoiceHomePage`
Handles all interactions on [invoiceto.me](https://invoiceto.me):

| Method | Description |
|---|---|
| `load()` | Navigates to invoiceto.me |
| `enterCompanyName(name)` | Types into the company name field |
| `clearAndFillRow1(desc, qty, price)` | Clears defaults and fills row 1 |
| `fillRow2–8(desc, qty, price)` | Fills rows 2 through 8 |
| `triggerUpdate()` | Clicks body to trigger total recalculation |
| `clickGetPDFButton()` | Clicks the Get PDF button |
| `clickDownloadPDF()` | Clicks Download PDF Invoice in the popup |
| `getRow1Total()` | Returns the calculated total for row 1 |
| `getSubtotal()` | Returns the subtotal value |
| `getTax()` | Returns the tax value |
| `getTotal()` | Returns the overall total value |

---

## Test Descriptions

### Functional Tests (`test_invoice_functional.py`)

| Test | Description | Assertion |
|---|---|---|
| `test_singleItemInvoice` | Fills only row 1, downloads PDF | PDF file exists in downloads folder |
| `test_maxItemsInvoice[Anthropic Ltd]` | Fills all 8 rows with Anthropic data | PDF file exists in downloads folder |
| `test_maxItemsInvoice[Google Inc]` | Fills all 8 rows with Google data | PDF file exists in downloads folder |
| `test_emptyCompanyName` | Skips company name, fills row 1 | PDF still downloads successfully |
| `test_invalidQuantityWithPrice` | Enters "abc" as quantity with valid price | Row total equals price (qty defaults to 1) |
| `test_invalidQuantityWithoutPrice` | Enters "abc" as quantity, no price | Subtotal displays "NaN" |
| `test_invalidPrice` | Enters "abc" as price with valid quantity | Total displays "NaN" |
| `test_zeroQuantity` | Enters "0" as quantity with valid price | Row total displays "-" |

### Visual Tests (`test_invoice_visual.py`)

| Test | Checkpoints | Description |
|---|---|---|
| `test_invoiceVisual` | 3 web snapshots + 1 PDF validation | Captures form initial state, filled state, PDF popup, then validates downloaded PDF with ImageTester |

---

## How to Run

### Run all tests
```bash
pytest tests/ -v
```

### Run only functional tests
```bash
pytest tests/test_invoice_functional.py -v
```

### Run only visual tests
```bash
pytest tests/test_invoice_visual.py -v
```

### Run a specific test
```bash
pytest tests/test_invoice_functional.py::test_singleItemInvoice -v
```

### Run with print output visible
```bash
pytest tests/ -v -s
```

### Run headless (no browser window)
Update `config.json`:
```json
{
    "browser": "Headless Chrome"
}
```

---

## Visual Testing Dashboard

When `run_visual_test` is `true`, results are sent to your Applitools Eyes dashboard at [eyes.applitools.com](https://eyes.applitools.com).

**Dashboard structure:**
```
Batch: "Invoice Project - YYYY-MM-DD_HH-MM"
└── Test: "Invoice Visual Test"
    ├── Step 1: Invoice Form - Initial State
    ├── Step 2: Invoice Form - Filled
    └── Step 3: PDF Popup
        + ImageTester PDF validation
```

**First run:** All steps are saved as the baseline and marked as **New**. Review and approve them on the dashboard.

**Subsequent runs:** New screenshots are compared against the approved baseline. Any visual differences are flagged for review.

---

## How Visual Testing Works

This project uses two complementary Applitools tools:

### 1. Applitools Eyes (`eyes-selenium`)
Captures snapshots of the live web page at key moments during the test. Uses `MatchLevel.LAYOUT` which validates structural layout while ignoring dynamic content like changing values or timestamps.

### 2. Applitools ImageTester (JAR)
Validates the downloaded PDF by converting each page into an image and sending it to Applitools for comparison against a baseline. This catches PDF rendering regressions — wrong totals, shifted layout, missing fields — that web snapshots cannot detect.

```
Web snapshots  →  eyes.check_window()  →  Applitools Dashboard
PDF validation →  ImageTester JAR      →  Applitools Dashboard
```

Both results appear in the same batch on the Applitools dashboard.

---

## Screenshots on Failure

When any test fails, a screenshot is automatically saved to the `screenshots/` folder:

```
screenshots/
└── test_invalidPrice_2026-03-03_14-23-45.png
```

Screenshot filenames include the test name and timestamp for easy identification.

---

## Known Behaviors

These are confirmed site behaviors on [invoiceto.me](https://invoiceto.me) that the test suite documents and asserts against:

| Scenario | Expected Behavior |
|---|---|
| Empty company name | Invoice still downloads successfully |
| Invalid quantity + valid price | Quantity defaults to 1, total equals price |
| Invalid quantity + no price | Subtotal, tax, and total display "NaN" |
| Valid quantity + invalid price | Total displays "NaN" |
| Invalid quantity + invalid price | Total displays "NaN" |
| Zero quantity + valid price | Row total displays "-" |
