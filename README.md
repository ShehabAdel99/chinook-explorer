# 🎵 Chinook Explorer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive Python package for analyzing and visualizing Chinook music store data with business intelligence capabilities.

## Introduction

**Chinook Explorer** transforms raw music store data into actionable business insights. Built for the "Introduction to Python Programming" course at TU Dortmund University, it demonstrates advanced data science techniques including ETL pipelines, customer segmentation, and business intelligence analytics.

### Key Features
- **Revenue Analysis**: Monthly trends, seasonal patterns, and growth metrics
- **Customer Intelligence**: Lifetime value calculation and RFM segmentation  
- **Product Performance**: Top-performing artists, genres, and tracks
- **Geographic Insights**: Country-based revenue analysis
- **Advanced Visualizations**: Professional matplotlib and seaborn charts

## Installation

```bash
# Clone the repository
git clone https://github.com/ShehabAdel99/chinook-explorer.git
cd chinook-explorer

# Install the package
pip install -e .
```

**Requirements**: Python 3.10+, pandas ≥ 2.0.0, matplotlib ≥ 3.5.0, seaborn ≥ 0.12.0, numpy ≥ 1.21.0

## Usage

```python
from chinook_explorer.io import ChinookLoader
from chinook_explorer.modeling import ChinookModel  
from chinook_explorer.analytics import ChinookAnalyzer

# Load and model data
loader = ChinookLoader(data_dir="data/")
tables = loader.load_tables()

model = ChinookModel(tables)
sales_data = model.sales_line_items()
catalog_data = model.catalog()

# Analyze and visualize
analyzer = ChinookAnalyzer(sales_data, catalog_data)
monthly_revenue = analyzer.revenue_by_month()
top_countries = analyzer.top_countries_by_revenue()
```

**Interactive Tutorial**: See `notebooks/tutorial.ipynb` for a complete analysis workflow.

## Project Structure

```
chinook-explorer/
├── src/chinook_explorer/           # Main package
│   ├── __init__.py                 # Package initialization
│   ├── io.py                       # Data loading and validation
│   ├── modeling.py                 # Data modeling and joins
│   ├── analytics.py                # Business intelligence
│   └── viz.py                      # Data visualization
├── data/                           # Chinook database CSV files
├── notebooks/tutorial.ipynb       # Complete analysis tutorial
├── requirements.txt                # Dependencies
├── pyproject.toml                  # Package configuration
└── README.md                       # This file
```

### Core Modules

- **`io.py`**: `ChinookLoader` for CSV loading with schema validation
- **`modeling.py`**: `ChinookModel` for creating analysis-ready datasets  
- **`analytics.py`**: `ChinookAnalyzer` for business intelligence metrics
- **`viz.py`**: `ChinookVisualizer` for professional-grade plotting

## Authors

- **Shehab Moharram** - shehab.moharram@tu-dortmund.de
- **Mohamed Elgabry** - mohamed.elgabry@tu-dortmund.de

*Master's students at TU Dortmund University*

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.