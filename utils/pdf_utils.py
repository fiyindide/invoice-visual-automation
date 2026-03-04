import os
import time
import subprocess


def wait_for_pdf(download_dir, timeout=30):
    """Waits for a PDF file to appear in the download directory"""
    for _ in range(timeout):
        files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]
        if files:
            return os.path.join(download_dir, files[0])
        time.sleep(1)
    return None


def clear_downloads(download_dir):
    """Clears the downloads folder before each test"""
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            if f.endswith('.pdf'):
                os.remove(os.path.join(download_dir, f))


def run_image_tester(api_key, jar_path, pdf_path):
    """Runs ImageTester JAR on the downloaded PDF"""
    result = subprocess.run(
        [
            "java", "-jar", jar_path,
            "-k", api_key,
            "-f", pdf_path
        ],
        capture_output=True,
        text=True
    )
    print(f"ImageTester output: {result.stdout}")
    if result.returncode != 0:
        raise Exception(f"ImageTester failed: {result.stderr}")