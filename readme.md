# Equity Fund Performance Analysis

## Overview
This project analyzes quarterly financial data from 150 U.S. companies across various industries to support rebalancing decisions for an equity fund. Using Python, the analysis includes data cleaning, statistical summaries by state, financial ratio calculations, and data integration.

## Key Features
- Import and clean financial data from CSV
- Identify and report duplicate entries
- Group companies by state and calculate descriptive statistics (mean, median, min, max) for numeric variables
- Detect businesses with negative debt-to-equity ratios
- Compute debt-to-income ratios (long-term debt / revenue)
- Concatenate new financial metrics into the original dataset

## Technologies Used
- Python
- Pandas
- NumPy
- Jupyter Notebook

## Folder Structure
📁 source_data           → Input source file
📁 .                     → Python scripts
📁 outputs               → Resulting visualizations
📁 utils             → Mapping Column Names in a Pandas DataFrame
