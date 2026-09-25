# Zepto Data & AI Platform

An end-to-end AI/ML engineering project containing a data engineering pipeline, an analytics and machine learning pipeline, and a planned GenAI support assistant.

## Project Overview

This project is organized into three modules:

1. **Data Pipeline** - Scrapes, cleans, transforms and stores product-style data in a normalized SQLite database.
2. **Analytics Pipeline** - Performs exploratory data analysis and predictive modeling using the Titanic dataset.
3. **Support Assistant** - A planned RAG-based GenAI assistant for answering questions from Zepto policy documents.

All modules are maintained inside a single GitHub repository.

---

# Repository Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── data/
│   ├── database/
│   ├── outputs/
│   ├── database.py
│   ├── pandas_validation.py
│   ├── pipeline.py
│   ├── queries.py
│   ├── scraper.py
│   ├── requirements.txt
│   └── README.md
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.py
│   ├── titanic.csv
│   ├── titanic_pipeline.joblib
│   └── requirements.txt
│
├── support_assistant/
│   └── docs/
│
├── README.md
└── .gitignore