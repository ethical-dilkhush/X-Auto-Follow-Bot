# X Auto Follow Bot

Automates logging into multiple X (Twitter) accounts from a CSV credential list, following a target account, and logging out. It uses Selenium with Undetected ChromeDriver to reduce automation detection.

## Prerequisites

- Python 3.8+
- Google Chrome installed
- ChromeDriver that matches the installed Chrome version
- Stable internet connection

## Dependencies

- Python packages: `selenium`, `undetected-chromedriver`, `pandas`
- System: `google-chrome`

## Setup

1. Clone this repository and open it in your terminal:
```
git clone https://github.com/ethical-dilkhush/X-Auto-Follow-Bot.git
cd X-Auto-Follow-Bot
```

2. Create a virtual environment and install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install selenium undetected-chromedriver pandas
```

3. Create an `accounts.csv` file in the project root with your credential columns.

## Credentials Format

`accounts.csv` must contain at least:

```csv
username,password
```

Do **not** commit real credentials. Keep `accounts.csv` local and add it to `.gitignore` after generating it.

## Usage

Run the automation script with:

```
python autoFollow.py
```

## Project Structure

```
X-Auto-Follow-Bot/
├── autoFollow.py      # Selenium automation flow
├── accounts.csv       # Local credential list (do not commit)
├── README.md          # Project documentation
├── .gitignore         # Ignores local credentials and build artifacts
└── requirements.txt   # Python dependencies
```

## Behavior Overview

The script reads credentials, opens a Chrome session, and iterates through each account:

- Navigates to the X login page and logs in.
- Opens the target account page and follows if not already following.
- Logs out before moving to the next account.
- Closes the browser when complete.

## Security Notes

- Automating actions on X may violate their Terms of Service.
- Storing passwords in CSV increases risk. Prefer secure management over plain text.
- Excessive following behavior can lead to account restrictions or suspension.

## Troubleshooting

- **Login fails**: X may have changed its login DOM. Update selectors in `autoFollow.py`.
- **Chrome launches incorrectly**: Ensure Chrome and ChromeDriver versions match.

## Disclaimer

Use this project only for educational purposes. The author is not responsible for account actions taken by automated tools.
