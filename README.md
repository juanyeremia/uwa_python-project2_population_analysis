# 🧮 UWA Python Project 2: Population Analysis

This is a data analysis project for **CITS1401: Computational Thinking with Python** at The University of Western Australia.

The goal is to analyze population data across Australian states, SA2, and SA3 statistical areas using **pure Python** — without any external libraries like `csv` or `math`. The project emphasizes file handling, data cleaning, and algorithmic thinking.

---

## 📁 Project Structure

uwa_python-project2_population_analysis/
├── data/ # CSV files (provided)
│ ├── SampleData_Areas_P2.csv
│ └── SampleData_Populations_P2.csv
├── src/ # Main source code
│ └── main.py
├── docs/ # Instruction PDF
│ └── Instruction.pdf
├── debug_log/ # Debugging reflections
│ └── debugging_notes.md
└── test/ # Optional: test cases


---

## 🚀 Features

- Reads and processes two real-world CSV datasets without using `csv` module.
- Cleans invalid, missing, and duplicated data before processing.
- Calculates:
  - 📊 **OP1**: State/SA3/SA2 with max population by age group.
  - 🧮 **OP2**: Nested population and standard deviation analysis for large SA3s.
  - 🔎 **OP3**: Cosine similarity between SA2s with similar age distributions.

---

## 🧠 Skills Demonstrated

- Custom file parsing and validation
- Dictionary and list manipulation
- Handling corner cases
- Modular function design
- Debugging and documentation

---

## ⚙️ How to Run

```bash
# Inside the project folder
cd src
python main.py

---

See debug_log/debugging_notes.md for insights into error handling and learning from mistakes during development.
