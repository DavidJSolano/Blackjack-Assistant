# Blackjack-Assistant

This is a simple Blackjack AI assistant designed to help players practice and improve their Blackjack strategies. It includes card counting, true count calculations, and a graphical user interface (GUI) built with PyQt.

## Authors

- **David Solano**
- **Esteban Escartin**
- **Joel Daniel Rico**

---

## Features

- Hi-Lo card counting and true count calculations
- Card shuffling mechanics
- PyQt-based GUI for an interactive Blackjack experience
- Optional CLI-based Blackjack logic for simplicity

---

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/DavidJSolano/Blackjack-Assistant.git blackjack-assistant
cd blackjack-assistant
```

### 2. Create a Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv

# On Windows
python -m venv venv
```

#### Activate the Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

> Note: Use `python` on Windows if `python3` is not present!

```python
python3 pyqt_blackjack.py
```

## File Structure

```
blackjack-assistant/
│
├── .gitignore           # Files to ignore in Git
├── README.md            # Project documentation
├── README.txt            # Project documentation (txt)
├── blackjack.py         # Core Blackjack logic
├── gui_blackjack.py     # Tkinter-based GUI (deprecated)
├── pyqt_blackjack.py    # PyQt-based GUI (main application)
├── shuffling_deck.py    # Card shuffling and deck management
├── requirements.txt     # Python dependencies
└── venv/                # Virtual environment directory (generated locally)
```
