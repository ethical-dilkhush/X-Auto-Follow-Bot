import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# X (Twitter) login URL
LOGIN_URL = "https://x.com/login"
MAIN_ACCOUNT_URL = "https://x.com/ethicaldilkhush"

# Load accounts from CSV file
accounts_df = pd.read_csv("accounts.csv", dtype=str)

# Initialize Undetected ChromeDriver
driver = uc.Chrome()

def login_to_twitter(username, password):
    """Logs into a Twitter account"""
    driver.get(LOGIN_URL)
    time.sleep(5)  # Allow page to load
    
    try:
        # Find and enter username/email
        username_input = driver.find_element(By.TAG_NAME, "input")  # Dynamic selector
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Click "Next" if required
        try:
            next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
            next_button.click()
            time.sleep(3)
        except:
            pass  # No "Next" button, continue

        # Enter password
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Check if login was successful
        if "login" in driver.current_url:
            print(f"❌ Failed to log in: {username}")
            return False
        print(f"✅ Logged in: {username}")
        return True
    
    except Exception as e:
        print(f"❌ Login error ({username}): {e}")
        return False

def follow_main_account():
    """Navigates to main account and follows if not already following"""
    driver.get(MAIN_ACCOUNT_URL)
    time.sleep(5)

    try:
        follow_button = driver.find_element(By.XPATH, "//span[contains(text(),'Follow')]")
        follow_button.click()
        print("✅ Followed main account!")
        time.sleep(3)
    except Exception:
        print("⚠️ Already following or button not found.")

def logout():
    """Logs out of Twitter"""
    try:
        driver.get("https://x.com/logout")
        time.sleep(3)
        confirm_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log out')]")
        confirm_button.click()
        print("✅ Logged out successfully!")
        time.sleep(3)
    except Exception:
        print("⚠️ Logout failed.")

# Loop through each account
for index, row in accounts_df.iterrows():
    username = row["username"]
    password = row["Password"]

    print(f"\n🔄 Logging in with: {username}")
    
    if login_to_twitter(username, password):
        follow_main_account()
        logout()

# Close browser
driver.quit()
print("\n✅ Process complete!")