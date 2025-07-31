# 🧠 Ollama Fact Generator

This Python script uses the Ollama large language model to generate **unique, verifiable, and interesting facts** about a given keyword and saves them into an Excel file.

## 📌 Features

- Generates **up to 2500** unique, cleaned, and character-length-controlled facts.
- Utilizes the **Ollama LLM** (default: `llama3`) via CLI.
- Saves output in **Excel format** with keyword, fact number, and character count.
- Includes:
  - Duplicate detection
  - Fact cleaning (removal of bullets, numbering, etc.)
  - Graceful handling of timeouts, subprocess errors, and user interrupts

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- [Ollama](https://ollama.com/) installed and accessible via CLI (`ollama`)
- Install required Python packages:

```bash
pip install pandas openpyxl
```
## 🚀 Usage

```bash
python main.py
```

### 🗂️ Sheet Contents:

The Excel sheet will include the following columns:

- **Fact_Number** – Serial number of the fact  
- **Fact** – The actual generated fact  
- **Keyword** – The keyword you provided  
- **Character_Count** – Number of characters in each fact







