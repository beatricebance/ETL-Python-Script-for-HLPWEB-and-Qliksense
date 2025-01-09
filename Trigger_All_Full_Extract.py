import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time

# Load password from environment variable
PASSWORD = os.getenv('PASSWORD_ALSTOM')
USERNAME = os.getenv('USERNAME')

# Check if the password was loaded successfully
if PASSWORD is None:
    print("Error: PASSWORD environment variable is not set.")
    exit(1)

# Specify the path to the WebDriver executable
driver_path = r'C:\Program Files\edgedriver_win64\msedgedriver.exe'

# Set up options for Edge
edge_options = Options()
edge_options.use_chromium = True
edge_options.add_argument("--inprivate")

# Set up the Selenium WebDriver for Edge with options
driver = webdriver.Edge(service=EdgeService(driver_path), options=edge_options)

def wait_for_overlay_to_disappear(by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print("Overlay did not disappear in time:", e)

def click_element_with_js(driver, element):
    driver.execute_script("arguments[0].click();", element)

try:
    # Step 1: Go to the Alstom user login link
    print("Opening the Alstom user login page...")
    driver.get("https://alstom.hlpweb.net/alstom")

    WebDriverWait(driver, 60).until(lambda d: d.title != "")
    print("Page title is:", driver.title)

    # Step 2: Fill the username (email) field
    print("Filling in the username...")
    username_field = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.NAME, "loginfmt"))
    )
    username_field.send_keys(USERNAME)
    username_field.send_keys(Keys.RETURN)
    print("Username submitted.")

    # Define the elements' XPATHs
    button_paths = [
        ('//a[contains(@class, "toolBarNGP")]', '//*[@id="button-1174-btnInnerEl"]', '//*[@id="menuitem-1176-textEl"]'),        
        ('//a[contains(@class, "toolBarAudit")]', '//*[@id="button-1142-btnInnerEl"]', '//*[@id="menuitem-1144-textEl"]'),
        ('//a[contains(@class, "toolBarProjet")]', '//*[@id="button-1226-btnInnerEl"]', '//*[@id="menuitem-1228-textEl"]'),
        ('//a[contains(@class, "toolBarDEROGATION")]', '//*[@id="button-1159-btnInnerEl"]', '//*[@id="menuitem-1161-textEl"]'),
        ('//a[contains(@class, "toolBarNCR")]', '//*[@id="button-1119-btnInnerEl"]', '//*[@id="menuitem-1121-textEl"]'),
        ('//a[contains(@class, "toolBarSUMO")]', '//*[@id="button-1093-btnInnerEl"]', '//*[@id="menuitem-1095-textEl"]'),
        ('//a[contains(@class, "toolBarAPM")]', '//*[@id="button-1088-btnInnerEl"]', '//*[@id="menuitem-1090-textEl"]')
    ]

    for link_str, full_extract_button_str, dropdown_option_str in button_paths:
        try:
            # Step 3: Wait for the audit link to become clickable
            print("Waiting for the link to become clickable...")
            audit_link = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, link_str))
            )
            audit_link.click()
            print("Navigated to the functions page.")

            # Step 4: Click on 'Full extract' button
            print("Waiting for 'Full extract' button to become clickable...")
            full_extract_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, full_extract_button_str))
            )
            # Wait for any overlay to disappear
            wait_for_overlay_to_disappear(By.CLASS_NAME, "x-mask")
            click_element_with_js(driver, full_extract_button)
            print("'Full extract' button clicked.")

            # Step 5: Click on the dropdown option 'Full Extract'
            print("Clicking on 'Full extract' dropdown button directly...")
            dropdown_option = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, dropdown_option_str))
            )
            click_element_with_js(driver, dropdown_option)
            print("'Full Extract' option clicked.")
            
        except ElementClickInterceptedException as e:
            print(f"Exception {e}: Retrying with JavaScript click")
            click_element_with_js(driver, full_extract_button if full_extract_button.is_displayed() else dropdown_option)
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
    time.sleep(10)
finally:
    print("Exiting script.")
    driver.quit()
