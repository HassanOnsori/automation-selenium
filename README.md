# Web Automation Test Suite

A Selenium-based test automation for web application testing.

## Features

- Object-oriented test architecture with modular design
- Robust error handling and retry mechanisms
- Configurable headless/visible browser modes
- Human-like interaction patterns
- Comprehensive logging and reporting
- Anti-bot detection measures

## Setup

### Prerequisites
- Python 3.8+
- Chrome browser

### Installation

```bash
# Clone the repository
git clone https://github.com/HassanOnsori/exercise.git
cd exercise

# Create virtual environment
python3 -m venv .qavenv
source .qavenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run with visible browser (development/debugging)
python lectra_automation.py

# Run in headless mode
HEADLESS=true python lectra_automation.py
```

## Configuration

- `headless=False/True`: Control browser visibility
- `timeout=10`: Adjust wait timeouts (seconds)
- Logging level can be modified in the class initialization

## Project Structure

```
├── lectra_automation.py    # Main test automation class
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore patterns
```

## Test Scenario

The automation covers a web navigation scenario including:
- Search functionality testing
- Multi-page navigation
- Cookie consent handling
- Menu navigation
- Form interactions
- Tab management

## Notes

- Tests are designed to handle dynamic web elements
- Includes fallback strategies for element location
- Supports both local development and CI/CD integration