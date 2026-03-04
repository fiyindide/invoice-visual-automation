import json
import os
import pytest
import selenium.webdriver
from datetime import datetime
from applitools.selenium import Eyes, BatchInfo

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
invoice_batch = BatchInfo(f"Invoice Project - {timestamp}")

@pytest.fixture(scope='session')
def config():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    assert config_data['browser'] in ['Firefox', 'Chrome', 'Headless Chrome']
    return config_data


@pytest.fixture
def browser(config):
    if config['browser'] == 'Chrome':
        download_dir = os.path.abspath(config['download_dir'])
        os.makedirs(download_dir, exist_ok=True)

        chrome_opts = selenium.webdriver.ChromeOptions()
        chrome_opts.add_experimental_option('prefs', {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'plugins.always_open_pdf_externally': True
        })
        b = selenium.webdriver.Chrome(options=chrome_opts)

    elif config['browser'] == 'Firefox':
        b = selenium.webdriver.Firefox()

    elif config['browser'] == 'Headless Chrome':
        download_dir = os.path.abspath(config['download_dir'])
        chrome_opts = selenium.webdriver.ChromeOptions()
        chrome_opts.add_argument('--headless')
        chrome_opts.add_experimental_option('prefs', {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'plugins.always_open_pdf_externally': True
        })
        b = selenium.webdriver.Chrome(options=chrome_opts)

    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    b.maximize_window()
    yield b
    b.quit()


@pytest.fixture
def eyes(config):
    if not config.get('run_visual_test', False):
        return None

    eyes = Eyes()
    eyes.api_key = config['applitools_api_key']
    eyes.batch = invoice_batch
    eyes.save_new_tests = True
    return eyes

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"{screenshots_dir}/{item.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved to: {screenshot_path}")