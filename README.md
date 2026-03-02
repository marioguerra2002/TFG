# TFG

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/marioguerra2002/TFG.git
cd TFG/Code
```

### 2. Create and activate virtual environment (Python 3.13 recommended)
```bash
# Create virtual environment
python3.13 -m venv env

# Activate on macOS/Linux
source env/bin/activate

# Or activate on Windows
env\Scripts\activate
```

### 3. Install Python packages
```bash
pip install -U pip
pip install -r requirements.txt
```

### 4. Download spaCy language model for Spanish
```bash
python -m spacy download es_core_news_md
```

### 5. Chrome WebDriver Setup
The project uses `undetected-chromedriver` which automatically manages ChromeDriver. Make sure you have Google Chrome installed on your system.

### 6. Verify Installation
```bash
# Check Python version
python --version

# Verify spaCy and model
python -c "import spacy; nlp = spacy.load('es_core_news_md'); print('✓ spaCy works!')"

# List all installed packages
pip list
```

## Usage

### Activate Environment
```bash
# Navigate to Code directory
cd Code

# Activate environment on macOS/Linux
source env/bin/activate

# Or on Windows
env\Scripts\activate
```

### Deactivate Environment
```bash
deactivate
```

### Run Python Scripts
```bash
# With environment activated
python src/your_script.py

# Or directly without activating
./env/bin/python src/your_script.py
```

## Libraries Used

### Built-in Python Modules
- `os` - Operating system interface
- `time` - Time access and conversions
- `pickle` - Python object serialization
- `random` - Random number generation
- `glob` - Unix style pathname pattern expansion
- `urllib` - URL handling modules

### External Libraries

#### Data Science & Analysis
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing (dependency of pandas/spacy)

#### Web Scraping & Automation
- **selenium** (>=4.0.0) - Browser automation framework
- **undetected-chromedriver** (>=3.5.0) - Patched ChromeDriver to avoid bot detection

#### Natural Language Processing
- **langid** (>=1.1.6) - Language identification library
- **spacy** (>=3.8.0) - Industrial-strength NLP library
  - Model: `es_core_news_md` (Spanish medium-sized model)

#### Utilities
- **tqdm** (>=4.65.0) - Progress bar library
