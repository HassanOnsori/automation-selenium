# Web Automation Test

A Selenium-based test automation for web application testing.

## Features

- Object-oriented test architecture with modular design
- Human-like interaction patterns
- Logging and reporting
- Anti-bot detection measures
- Robust error handling
- Configurable headless/visible browser modes (headless mode will be implemented soon)

## Setup

### Prerequisites
- Python 3.13+
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

# Run in headless mode will be implemented soon
HEADLESS=true python lectra_automation.py
```

## Structure

```
├── lectra_automation.py    
├── requirements.txt        
├── README.md             
└── .gitignore           
```

## Test Scenario

The automation covers a web navigation scenario including:
- Search functionality testing
- Multi-page navigation
- Cookie consent handling
- Menu navigation
- Form interactions
- Tab management
