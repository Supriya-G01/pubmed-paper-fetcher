# PubMed Paper Fetcher

**PubMed Paper Fetcher** is a professional-grade Python command-line utility designed to retrieve biomedical research articles from the PubMed database. It supports advanced PubMed query syntax and intelligently filters for papers authored by individuals affiliated with pharmaceutical or biotech companies. The results are exported in a structured CSV format for further analysis or integration.

---

## 📁 Project Structure
```
pubmed-paper-fetcher/
├── papers/
│   ├── __init__.py
│   └── fetcher.py         # Core logic (fetching, filtering, saving)
├── cli.py                 # Command-line interface
├── pyproject.toml         # Poetry config and setup
├── README.md              # Project documentation
└── results.csv            # (optional) Output file from query
```

---

## 🚀 Key Features
- 🎯 Query PubMed using flexible and powerful search syntax
- 🏢 Detect authors from non-academic (industry) affiliations using string heuristics
- 📊 Export results with author and affiliation metadata in CSV format
- 🔍 Debug mode for transparency during execution
- 🔄 Modular architecture separating CLI and business logic

---

## 🛠 Installation Instructions

### ✅ Prerequisites
- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### 📦 Setup
```bash
poetry install
```

This command installs all necessary dependencies and prepares the virtual environment.

---

## ▶️ Usage Guide
To run a search query:
```bash
poetry run get-papers-list "cancer AND immunotherapy" -f results.csv
```

### CLI Options:
- `-h`, `--help` → Show usage help
- `-d`, `--debug` → Enable verbose debug logging
- `-f`, `--file` → Specify the CSV output file (optional)

Example:
```bash
poetry run get-papers-list "covid-19 AND vaccine" --debug
```

If `-f` is not specified, the results are printed directly to the terminal.

---

## 📋 Output Format
The generated CSV contains the following fields:
- `PubmedID`: Unique identifier for the article
- `Title`: Paper title
- `Publication Date`: Year of publication
- `Non-academic Author(s)`: Names of industry-affiliated contributors
- `Company Affiliation(s)`: Associated company or organization
- `Corresponding Author Email`: Extracted email if available

---

## 🧠 Affiliation Filtering Heuristics
To identify non-academic authors, the system applies the following logic:
- **Exclude**: Affiliations containing keywords like `university`, `college`, `institute`, `school`, `hospital`
- **Include**: Affiliations with terms such as `inc`, `ltd`, `biotech`, `pharma`, `therapeutics`, `labs`, `genomics`
- **Email Detection**: Extracted using standard regex patterns from affiliation text

---

## 🧰 Technology Stack
- [Python 3.10+](https://www.python.org/)
- [requests](https://pypi.org/project/requests/) – API interaction
- [argparse](https://docs.python.org/3/library/argparse.html) – CLI parsing
- [Poetry](https://python-poetry.org) – Dependency and script management
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) – Primary data source

Development guidance and technical assistance provided by [ChatGPT](https://openai.com/chatgpt).

---

## 🧪 Optional: Publish to TestPyPI
To publish your package for testing:
1. Sign up at [TestPyPI](https://test.pypi.org/)
2. Add a `__version__` string to your module
3. Add the following to `pyproject.toml`:
```toml
[tool.poetry.scripts]
get-papers-list = "cli:main"
```
4. Run:
```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish --build -r test-pypi
```

---

## 📄 License
MIT License © 2025 Supriya Gudise

Use, modify, and distribute responsibly under the terms of the license.
