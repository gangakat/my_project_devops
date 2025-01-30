import os
import pytest
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Gmail Credentials (Use environment variables instead of hardcoding)
EMAIL = os.getenv("GMAIL_USER", "your-email@gmail.com")
PASSWORD = os.getenv("GMAIL_PASS", "your-password")
RECIPIENT = "recipient@example.com"
SUBJECT = "Test Email with Attachment"
BODY = "This is an automated test email with an attachment."

# File to Attach (macOS Example)
FOLDER_PATH = os.path.expanduser("~/Documents/TestFolder")
ATTACHMENT = "testfile.txt"
FILE_PATH = os.path.join(FOLDER_PATH, ATTACHMENT)


@pytest.fixture(scope="function")
def setup_teardown():
    """Fixture to initialize and quit WebDriver for each test."""
    service = Service("/usr/local/bin/chromedriver")  # Update path if needed
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    yield driver, wait

    driver.quit()


def test_gmail_compose(setup_teardown):
    """Test composing and sending an email with an attachment in Gmail."""
    driver, wait = setup_teardown

    # Step 1: Open Gmail & Log In
    driver.get("https://mail.google.com/")

    wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(EMAIL, Keys.ENTER)
    time.sleep(2)  # Allow page load

    wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(PASSWORD, Keys.ENTER)
    time.sleep(5)  # Wait for Gmail to load

    # Step 2: Click Compose Button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Compose')]"))).click()
    time.sleep(2)

    # Step 3: Fill in Email Details
    wait.until(EC.presence_of_element_located((By.NAME, "to"))).send_keys(RECIPIENT, Keys.TAB)
    wait.until(EC.presence_of_element_located((By.NAME, "subjectbox"))).send_keys(SUBJECT, Keys.TAB)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Message Body']"))).send_keys(BODY)

    # Step 4: Attach File (MacOS)
    attach_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@command='Files']")))
    attach_button.click()
    time.sleep(3)  # Wait for the Mac file picker to open

    # Use PyAutoGUI to enter file path in macOS file dialog
    time.sleep(2)
    pyautogui.write(FILE_PATH)
    time.sleep(1)
    pyautogui.press("return")  # Press Enter to select the file

    time.sleep(5)  # Allow upload

    # Step 5: Send Email
    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Send')]")))
    send_button.click()
    time.sleep(5)  # Wait for sending

    # Step 6: Verify Email in Sent Folder
    driver.get("https://mail.google.com/mail/u/0/#sent")
    time.sleep(5)
    assert SUBJECT in driver.page_source, "Email not found in Sent folder!"

    print("✅ Test Passed: Email sent successfully with attachment.")
    print("hi, this is my first project")
