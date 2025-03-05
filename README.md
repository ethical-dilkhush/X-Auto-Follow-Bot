# 🚀 X Auto Follow Bot

This Python script automates logging into multiple X accounts, following a specific main account, and logging out. It uses **Selenium** with **Undetected ChromeDriver** to bypass detection mechanisms.

---

## 📌 Requirements

- Python 3.x
- **Selenium** for browser automation
- **Undetected ChromeDriver** to avoid detection
- **Pandas** for handling account credentials stored in CSV format
- **Google Chrome** installed

---

## 🔧 Installation

Before running the script, install the required dependencies:

```bash
pip install selenium undetected-chromedriver pandas
```

---

## 📂 Account Credentials (CSV Format)

Create a CSV file named **`accounts.csv`** in the same directory with the following format:

```csv
username,password
username1,password1
username2,password2
...
```

---

## 📝 Usage

1. Ensure **Google Chrome** is installed and up to date.
2. Place your **accounts.csv** file in the same directory as the script.
3. Run the script:

   ```bash
   python auto_follow.py
   ```

---

## ⚠️ Important Notes

- **Google Chrome** must be installed for **Undetected ChromeDriver** to work.
- X's login structure may change, requiring adjustments to the script.
- Running this script excessively may lead to account suspension.

---

## 🎯 Features

✅ Automates login for multiple accounts  
✅ Follows the main account if not already following  
✅ Logs out after following  
✅ Uses Undetected ChromeDriver to bypass detection  

---

## 📢 Disclaimer

This script is for **educational purposes only**. Automating actions on X may violate their [terms of service](https://twitter.com/en/tos). Use responsibly to avoid any account restrictions.

---

### 🚀 Enjoy Automating X Safely!

