# X Auto Follow Bot

Automates logging into multiple X (Twitter) accounts from a CSV credential list,
follows a configurable target account, and logs out.  Uses Selenium with
Undetected ChromeDriver to reduce automation detection.

## Prerequisites

- Python 3.9+
- Google Chrome installed
- ChromeDriver that matches the installed Chrome version (Undetected
  ChromeDriver bundles its own matching driver)
- Stable internet connection

## Installation

```bash
git clone https://github.com/ethical-dilkhush/X-Auto-Follow-Bot.git
cd X-Auto-Follow-Bot
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Credentials

Create an `accounts.csv` file in the project root with at least:

```csv
username,password
```

Do **not** commit real credentials.  Keep `accounts.csv` local and confirm it
is listed in `.gitignore`.

## Usage

```bash
# Run with defaults (target: https://x.com/ethicaldilkhush, CSV: accounts.csv)
python autoFollow.py

# Specify a different target account and credential file
python autoFollow.py --target https://x.com/example --csv my_accounts.csv

# Run headless (useful for servers / CI)
python autoFollow.py --headless --target https://x.com/example
```

Run `python autoFollow.py --help` for all CLI options.

## CLI Options

| Flag | Description |
|------|-------------|
| `-c`, `--csv` | Path to accounts CSV (default: `accounts.csv`) |
| `-t`, `--target` | Target X profile URL to follow |
| `-H`, `--headless` | Run Chrome in headless mode |
| `-w`, `--timeout` | Explicit wait timeout in seconds (default: 10) |

## Project Structure

```
X-Auto-Follow-Bot/
├── autoFollow.py      # Selenium automation flow with CLI
├── accounts.csv       # Local credential list (do not commit)
├── requirements.txt   # Python dependencies (pinned)
├── README.md          # This file
└── .gitignore         # Ignores local credentials and build artifacts
```

## Behavior Overview

The script reads credentials, opens a Chrome session, and iterates through each
account:

1. Navigates to the X login page and logs in.
2. Opens the target account page and follows if not already following.
3. Logs out before moving to the next account.
4. Closes the browser when complete.

When `--headless` is used the browser runs in the background without a visible
window.

## Security Notes

- Automating actions on X may violate their Terms of Service.
- Storing passwords in CSV increases risk. Prefer secure secret management over
  plain text.
- Excessive following behavior can lead to account restrictions or suspension.

## Troubleshooting

- **Login fails**: X may have changed its login DOM. Update selectors in
  `autoFollow.py`.
- **Chrome launches incorrectly**: Ensure Chrome and ChromeDriver versions
  match. Undetected ChromeDriver downloads a matching driver automatically when
  possible.
- **Headless mode errors**: Some platforms require `--no-sandbox` and
  `--disable-dev-shm-usage`; these are enabled by default when `--headless` is
  passed.

## Disclaimer

Use this project only for educational purposes. The author is not responsible
for account actions taken by automated tools.
