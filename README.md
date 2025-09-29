# 🎵 Chinook Explorer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive Python package for analyzing and visualizing data from the Chinook music store database, featuring advanced business intelligence capabilities and interactive visualizations.

## 🎯 Project Overview

**Chinook Explorer** is a production-ready Python package that transforms raw music store data into actionable business insights. Built as a master's-level final project for "Introduction to Python Programming" at TU Dortmund University, it demonstrates advanced data science techniques including ETL pipelines, customer segmentation, and business intelligence analytics.

The package provides a complete end-to-end solution for music retail analytics, from data loading and validation to sophisticated customer behavior analysis and compelling visualizations.

## ✨ Key Features

### 📊 **Comprehensive Analytics Engine**
- **Revenue Analysis**: Monthly trends, seasonal patterns, and growth metrics
- **Customer Intelligence**: Lifetime value calculation and RFM segmentation
- **Product Performance**: Top-performing artists, genres, and tracks
- **Geographic Insights**: Country-based revenue distribution and market analysis
- **Text Analytics**: Track title analysis and content insights

### 🔧 **Robust Data Pipeline**
- **Smart Data Loading**: Automatic CSV detection with schema validation
- **Data Modeling**: Sophisticated table joins and feature engineering
- **Quality Assurance**: Built-in data validation and relationship checks
- **Performance Optimized**: Efficient pandas operations and memory management

### 📈 **Advanced Visualizations**
- **Interactive Dashboards**: Multi-panel business intelligence displays
- **Publication-Ready Charts**: Professional matplotlib and seaborn visualizations
- **Customer Segmentation**: RFM analysis with visual clustering
- **Trend Analysis**: Time-series plots with statistical insights

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ShehabAdel99/chinook-explorer.git
cd chinook-explorer

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Requirements
- Python 3.10 or higher
- pandas >= 2.0.0
- matplotlib >= 3.5.0
- seaborn >= 0.12.0
- numpy >= 1.21.0

### Basic Usage

```python
from chinook_explorer.io import ChinookLoader
from chinook_explorer.modeling import ChinookModel
from chinook_explorer.analytics import ChinookAnalyzer
from chinook_explorer.viz import ChinookVisualizer

# Load and validate data
loader = ChinookLoader(data_dir="data/")
tables = loader.load_tables()

# Build analysis-ready datasets
model = ChinookModel(tables)
sales_data = model.sales_line_items()
catalog_data = model.catalog()

# Perform business intelligence analysis
analyzer = ChinookAnalyzer(sales_data, catalog_data)
monthly_revenue = analyzer.revenue_by_month()
customer_segments = analyzer.rfm_analysis()
top_countries = analyzer.top_countries_by_revenue()

# Create visualizations
visualizer = ChinookVisualizer()
visualizer.plot_revenue_trend(monthly_revenue)
visualizer.plot_customer_segments(customer_segments)
```

## 📁 Project Structure

```
chinook-explorer/
├── 📂 src/
│   └── 📂 chinook_explorer/
│       ├── 📄 __init__.py          # Package initialization
│       ├── 📄 io.py                # Data loading and validation
│       ├── 📄 modeling.py          # Data modeling and feature engineering
│       ├── 📄 analytics.py         # Business intelligence analytics
│       └── 📄 viz.py               # Data visualization functions
├── 📂 data/                        # Chinook database CSV files
│   ├── 📄 Album.csv
│   ├── 📄 Artist.csv
│   ├── 📄 Customer.csv
│   ├── 📄 Employee.csv
│   ├── 📄 Genre.csv
│   ├── 📄 Invoice.csv
│   ├── 📄 InvoiceLine.csv
│   ├── 📄 MediaType.csv
│   ├── 📄 Playlist.csv
│   ├── 📄 PlaylistTrack.csv
│   └── 📄 Track.csv
├── 📂 notebooks/
│   └── 📄 tutorial.ipynb           # Comprehensive tutorial and demo
├── 📄 requirements.txt             # Production dependencies
├── 📄 pyproject.toml              # Modern Python packaging config
├── 📄 setup.cfg                   # Additional build configuration
├── 📄 README.md                   # This file
└── 📄 LICENSE.txt                 # MIT License
```

## 🎮 Interactive Tutorial

The best way to explore Chinook Explorer is through our comprehensive Jupyter notebook:

```bash
# Start Jupyter Lab
jupyter lab

# Open the tutorial notebook
# Navigate to: notebooks/tutorial.ipynb
```

The tutorial demonstrates:
- 📊 **Complete data analysis workflow** from CSV to insights
- 🔍 **Advanced customer segmentation** using RFM analysis
- 📈 **Professional visualizations** with business context
- 💡 **Real-world business recommendations** based on data

## 🧩 Core Modules

### 1. **Data Loading (`io.py`)**
- `ChinookLoader`: Intelligent CSV loading with automatic schema validation
- Handles missing data and type conversion
- Provides comprehensive data quality reports

### 2. **Data Modeling (`modeling.py`)**
- `ChinookModel`: Creates analysis-ready datasets through sophisticated joins
- Builds fact and dimension tables optimized for analytics
- Adds calculated fields and business metrics

### 3. **Analytics Engine (`analytics.py`)**
- `ChinookAnalyzer`: Comprehensive business intelligence toolkit
- Revenue analysis, customer segmentation, product performance
- Statistical analysis and trend identification

### 4. **Visualization (`viz.py`)**
- `ChinookVisualizer`: Professional-grade plotting functions
- Interactive dashboards and publication-ready charts
- Customizable themes and layouts

## 📊 Sample Output

When you run the analysis, you'll get insights like:

**Revenue Performance:**
- Total Revenue: $2,328.60 across 2009-2013
- Peak Revenue Month: March 2010 ($52.62)
- Average Monthly Revenue: $47.79

**Market Leaders:**
- Top Country: USA ($523.06, 22.5% of total revenue)
- Top Genre: Rock ($826.65, 35.5% of total revenue)  
- Top Artist: Iron Maiden ($138.60)

**Customer Intelligence:**
- 59 unique customers analyzed
- Average Customer Lifetime Value: $39.12
- High-value segment identified through RFM analysis

## 🎓 Project Context

This project was developed as a **final assignment for a master's-level "Introduction to Python Programming" course**, demonstrating:

- **Advanced Python Programming**: Object-oriented design, type hints, and modern Python practices
- **Data Science Pipeline**: Complete ETL workflow with pandas and numpy
- **Business Intelligence**: Customer segmentation, statistical analysis, and KPI calculation
- **Data Visualization**: Professional charts using matplotlib and seaborn
- **Software Engineering**: Package structure, documentation, and testing
- **Academic Excellence**: Comprehensive analysis with actionable business insights

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🙏 Acknowledgments

- **Chinook Database**: Sample database representing a digital music store
- **TU Dortmund University**: Academic institution supporting this research
- **Python Community**: For the excellent libraries that made this project possible

---

**⭐ Star this repository if you found it helpful!**
- playlist_track.csv
- tracks.csv

Each file must contain the required columns as documented in the schema.

## Development

### Setting up a development environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Author

ShehabAdel99 (shehab.adel@tu-dortmund.de)

## Acknowledgments

- TU Dortmund University Data Science Program
- The Chinook Database Project