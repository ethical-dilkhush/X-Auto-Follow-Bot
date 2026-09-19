#!/usr/bin/env python3
"""X Auto Follow Bot — Selenium automation that logs into multiple X (Twitter)
accounts from a CSV credential list, follows a configurable target account, and
logs out. Uses Undetected ChromeDriver to reduce automation detection.

Usage examples:
  python autoFollow.py
  python autoFollow.py --csv my_accounts.csv --target https://x.com/example
  python autoFollow.py --headless --target https://x.com/example
"""

import argparse
import sys
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------
# Defaults — all overridable via CLI flags
# ---------------------------------------------------------------------------
DEFAULT_LOGIN_URL = "https://x.com/login"
DEFAULT_CSV_PATH = "accounts.csv"
DEFAULT_TIMEOUT = 10  # seconds for explicit waits

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Log into multiple X accounts, follow a target, and log out."
    )
    p.add_argument(
        "--csv", "-c",
        default=DEFAULT_CSV_PATH,
        help=f"Path to accounts CSV (default: {DEFAULT_CSV_PATH})",
    )
    p.add_argument(
        "--target", "-t",
        default=None,
        help="Target X profile URL to follow (default: https://x.com/ethicaldilkhush)",
    )
    p.add_argument(
        "--headless", "-H",
        action="store_true",
        help="Run Chrome in headless mode (no visible browser window)",
    )
    p.add_argument(
        "--timeout", "-w",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Explicit wait timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    return p


# ---------------------------------------------------------------------------
# Browser helpers
# ---------------------------------------------------------------------------
def create_driver(headless: bool) -> uc.Chrome:
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Undetected ChromeDriver already applies stealth tweaks.
    return uc.Chrome(options=options)


def login_to_twitter(
    driver: uc.Chrome,
    username: str,
    password: str,
    timeout: int,
) -> bool:
    """Attempt to log into X with the given credentials. Returns True on success."""
    driver.get(DEFAULT_LOGIN_URL)
    wait = WebDriverWait(driver, timeout)

    try:
        # --- username / email step ---
        username_input = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Click "Next" if the page shows a secondary button
        try:
            next_button = driver.find_element(
                By.XPATH, "//span[contains(text(), 'Next')]"
            )
            next_button.click()
            time.sleep(3)
        except Exception:
            pass  # No separate "Next" step on this account flow

        # --- password step ---
        password_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password']")
            )
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        if "login" in driver.current_url.lower():
            print(f"❌ Failed to log in: {username}")
            return False

        print(f"✅ Logged in: {username}")
        return True

    except Exception as exc:
        print(f"❌ Login error ({username}): {exc}")
        return False


def follow_target(driver: uc.Chrome, target_url: str, timeout: int) -> None:
    """Navigate to *target_url* and follow if the Follow button is visible."""
    driver.get(target_url)
    time.sleep(5)

    try:
        follow_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Follow')]")
            )
        )
        follow_button.click()
        print("✅ Followed target account!")
        time.sleep(3)
    except Exception:
        print("⚠️ Already following or Follow button not found.")


def logout(driver: uc.Chrome, timeout: int) -> None:
    """Attempt to log out of the current X session."""
    try:
        driver.get("https://x.com/logout")
        time.sleep(3)
        confirm_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Log out')]")
            )
        )
        confirm_button.click()
        print("✅ Logged out successfully!")
        time.sleep(3)
    except Exception:
        print("⚠️ Logout failed.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    target_url = args.target or "https://x.com/ethicaldilkhush"

    # --- load credentials ---
    try:
        accounts_df = pd.read_csv(args.csv, dtype=str)
    except FileNotFoundError:
        print(f"❌ Accounts file not found: {args.csv}")
        sys.exit(1)
    except Exception as exc:
        print(f"❌ Failed to read {args.csv}: {exc}")
        sys.exit(1)

    if "username" not in accounts_df.columns or "password" not in accounts_df.columns:
        print("❌ accounts.csv must contain 'username' and 'password' columns.")
        sys.exit(1)

    if accounts_df.empty:
        print("⚠️ accounts.csv is empty — nothing to do.")
        return

    driver = create_driver(args.headless)

    try:
        for _, row in accounts_df.iterrows():
            username = row["username"]
            password = row["password"]

            print(f"\n🔄 Logging in with: {username}")

            if login_to_twitter(driver, username, password, args.timeout):
                follow_target(driver, target_url, args.timeout)
                logout(driver, args.timeout)
    finally:
        driver.quit()

    print("\n✅ Process complete!")


if __name__ == "__main__":
    main()
