# TFG

## Entorno Python (Importante)

Este proyecto usa un unico entorno virtual dentro de esta carpeta:

- `env/` (ruta completa desde la raiz del repo: `TFG/Code/env`)

Si ejecutas el codigo en macOS (especialmente con iCloud Drive), usa `env.nosync` para evitar que Apple sincronice/corrompa el entorno virtual:

- `env.nosync/` (ruta completa desde la raiz del repo: `TFG/Code/env.nosync`)

No debes crear otros entornos en la raiz del repositorio ni con nombres alternativos (`.env`, `.venv`, `venv`).

## ⚡ Quick Start

### 1. Navigate to the correct directory
```bash
# You must be in the Code directory
cd TFG/Code
```

### 2. Activate the virtual environment
```bash
# macOS (recomendado con iCloud Drive)
source env.nosync/bin/activate

# Linux
source env/bin/activate

# Windows
env\Scripts\activate
```

### 3. Run your scripts
```bash
python src/your_script.py
```

---

## Installation (First Time Setup)

### 1. Clone the repository
```bash
git clone https://github.com/marioguerra2002/TFG.git
cd TFG/Code
```

### 2. Create and activate virtual environment (Python 3.13 o superior)
```bash
# Create virtual environment (macOS + iCloud Drive recomendado)
python3 -m venv env.nosync --upgrade-deps

# Alternative for non-macOS environments
# python3 -m venv env --upgrade-deps

# Activate on macOS/Linux
source env.nosync/bin/activate

# Or activate on Windows
env.nosync\Scripts\activate

# Or, if you used env instead
# env\Scripts\activate
```

### 3. Install Python packages
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Reinitialize environment (clean setup)
If your environment gets corrupted, reset it from `TFG/Code`:

```bash
# macOS + iCloud Drive
rm -rf env.nosync
python3 -m venv env.nosync --upgrade-deps
source env.nosync/bin/activate

# Alternative for non-macOS environments
# rm -rf env
# python3 -m venv env --upgrade-deps
# source env/bin/activate

pip install --upgrade pip setuptools wheel
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

### Important: Always use the correct directory
```bash
# Navigate to the Code subdirectory
cd TFG/Code
```

### Activate Environment
```bash
# macOS (recomendado con iCloud Drive)
source env.nosync/bin/activate

# Linux
source env/bin/activate

# Windows
env\Scripts\activate
```

### Deactivate Environment
```bash
deactivate
```

### Run Python Scripts
```bash
# After activating (recommended)
python src/your_script.py

# Or directly without activating
./env.nosync/bin/python src/your_script.py

# Alternative for non-macOS environments
# ./env/bin/python src/your_script.py
```

## Libraries Used

### Built-in Python Modules
- `os` - Operating system interface
- `re` - Regular expressions for text matching
- `unicodedata` - Unicode normalization (accent removal and text normalization)
- `collections` (`Counter`) - Counting keyword matches for diagnostics
- `time` - Time access and conversions
- `pickle` - Python object serialization
- `random` - Random number generation
- `glob` - Unix style pathname pattern expansion
- `urllib` - URL handling modules

### External Libraries

#### Data Science & Analysis
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing (dependency of pandas/spacy)
- **matplotlib** - Base plotting library for charts and figures
- **seaborn** - Statistical data visualization built on top of matplotlib

Note: `requirements.txt` reflects the external pip dependencies used in this project.

#### Web Scraping & Automation
- **selenium** (>=4.0.0) - Browser automation framework
- **undetected-chromedriver** (>=3.5.0) - Patched ChromeDriver to avoid bot detection

#### Natural Language Processing
- **langid** (>=1.1.6) - Language identification library
- **spacy** (>=3.8.0) - Industrial-strength NLP library
  - Model: `es_core_news_md` (Spanish medium-sized model)
- **pysentimiento** - Sentiment analysis and social media NLP models

#### Deep Learning
- **torch** - Core PyTorch tensor and deep learning library


#### Utilities
- **tqdm** (>=4.65.0) - Progress bar library
