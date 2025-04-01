# AdFramework

## 📄 Project Overview

**AdFramework** is an automated testing framework designed for advertisement-related modules. It helps QA teams and developers efficiently validate the display, availability, and interaction of advertising content across web platforms.

This framework supports fast, scalable, and stable advertisement testing with clear and maintainable code structure.

## 🚀 Features

- Detect and verify advertisement containers on the webpage.
- Validate if ad elements (images, text, buttons) are visible and loaded correctly.
- Confirm ad click-through redirects to valid URLs.
- Validate HTTP response status codes for ad landing pages.
- Monitor dynamic ad content and asynchronous loading behavior.
- Provide test reports and logs for quick issue tracking.

## 🛠️ Tech Stack

| Technology | Description |
|:-:|:-|
| **Python** | Programming Language |
| **Playwright** | Browser automation framework |
| **Pytest** | Python testing framework |
| **pytest-asyncio** | Async test case support |
| **Ruff** | Python linter for code quality |
| **Allure** (optional) | Test reporting |

---

## 📥 Installation

1. Clone the repository:

```bash
git clone https://github.com/liuyan0828/adframework.git
cd adframework
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

## 🚦 How to Run

Run all test cases:

```bash
pytest tests/ -s
```

Run specific test file:

```bash
pytest tests/test_ad_case.py -s
```

Generate HTML report:

```bash
pytest tests/ --html=report.html
```

Check code format:

```bash
ruff check .
```

---

## 📄 Directory Structure

```
adframework/
├── tests/                     # Test cases for ad validation
│   └── test_ad_case.py        # Sample test file
├── conftest.py                # Pytest configuration
├── pytest.ini                 # Pytest settings
├── playwright.config.json     # Playwright settings
├── requirements.txt           # Dependencies
└── README.md                  # Project Description
```

---

## ✅ Usage Scenarios

- Online advertisement placement verification
- Daily ad monitoring and link validation
- Automated regression testing for ad-related UI
- Ad content compliance checks

## 🔥 Future Plans

- Support scheduled monitoring
- Add integration with Slack/Email alerts
- Enable cross-platform browser compatibility testing
- Add visual comparison testing for ads

---

Feel free to fork, contribute, or open issues to improve this framework.
