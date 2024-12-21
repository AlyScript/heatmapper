from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Load cookies from a file
with open("cookies.json", "r") as file:
    cookies = json.load(file)

# Configuration
leetcode_url = "https://leetcode.com/"
username = "adamaly"  # Replace with your LeetCode username
with open("password.txt", "r") as file:
    password = file.read().strip()
problem_url = "https://leetcode.com/problems/two-sum/"  # URL of the problem
solution_code = """
class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
"""

# Set up Selenium
options = webdriver.ChromeOptions()
# Uncomment "--headless" for silent operation
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)  # Wait timeout of 10 seconds

try:
    # Step 1: Navigate to LeetCode
    print("Navigating to LeetCode...")
    driver.get(leetcode_url)

    for cookie in cookies:
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            del cookie["sameSite"]  # Remove invalid sameSite attribute
        driver.add_cookie(cookie)

    driver.refresh()

    print("Cookies loaded.")

    # # Step 3: Click on Sign In
    # print("Clicking Sign In...")
    # sign_in_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
    # sign_in_link.click()

    # # Step 4: Log In
    # print("Entering username and password...")
    # try:
    #     username_field = wait.until(EC.presence_of_element_located((By.ID, "id_login")))
    #     password_field = wait.until(EC.presence_of_element_located((By.ID, "id_password")))
    #     username_field.send_keys(username)
    #     password_field.send_keys(password)
    #     password_field.send_keys(Keys.RETURN)

    #     # Wait for successful login (e.g., profile avatar or username appears)
    #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "profile-dropdown-indicator")))  # Update this to the correct element
    #     print("Login successful.")
    # except Exception as e:
    #     print("Login failed or an error occurred:", str(e))
    #     driver.quit()
    #     exit()

    # Step 2: Handle cookies consent banner
    print("Checking for cookies consent banner...")
    try:
        # Wait for the dialog container to appear
        consent_popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fc-dialog-container")))

        # Locate the "Consent" button within the dialog container
        consent_button = consent_popup.find_element(By.XPATH, "//p[contains(@class, 'fc-button-label') and text()='Consent']")
        consent_button.click()
        print("Cookies consented.")
    except Exception as e:
        print("No cookies consent banner detected or an error occurred:", str(e))

    # Step 5: Navigate to the specific problem
    print("Navigating to the problem...")
    driver.get(problem_url)



    # # Step 6: Change the language to Python
    # print("Changing language to Python...")
    # language_dropdown = wait.until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "ant-select-selection-item"))
    # )
    # language_dropdown.click()
    # python_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Python']")))
    # python_option.click()
    # print("Language changed to Python.")

    # # Step 7: Interact with the code editor
    # print("Interacting with the code editor...")
    # editor = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror")))
    # editor.click()

    # # Input the solution code
    # print("Entering solution code...")
    # driver.execute_script("arguments[0].CodeMirror.setValue(arguments[1]);", editor, solution_code)

    # Step 8: Submit the solution
    print("Submitting the solution...")
    try:
        submit_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-sm font-medium') and text()='Submit']"))
        )
        # Scroll to the button and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)  # Allow adjustment
        driver.execute_script("arguments[0].click();", submit_button)
        print("Solution submitted successfully!")
    except Exception as e:
        print("Could not find or click the submit button:", str(e))

    # Wait for submission result
    time.sleep(10)

finally:
    # Close the browser
    print("Closing the browser...")
    driver.quit()