# Agri-Tech Data Analyzer 🌾📊

A professional Python data analysis project demonstrating data engineering skills with a focus on agricultural data processing.

## Project Overview

This portfolio project showcases:
- **Data Loading & Validation**: Robust CSV parsing with error handling
- **Data Cleaning**: Handling missing values and dirty data
- **Statistical Analysis**: Weekly aggregations and correlation analysis
- **Data Visualization**: Multi-plot analysis using Matplotlib
- **Error Handling**: Comprehensive validation and user feedback

## Features

### Core Functionality
✓ Reads daily rainfall and crop growth data from CSV  
✓ Calculates weekly rainfall aggregates  
✓ Computes correlation between rainfall and crop growth  
✓ Generates professional visualization dashboard  

### Error Handling
✓ Missing file detection  
✓ Missing column validation  
✓ Data type validation and conversion  
✓ Handling negative/invalid values  
✓ Forward/backward fill for missing data points  
✓ Informative error messages  

## Files

- `daily_crop_data.csv` - 30-day sample dataset with:
  - Date (YYYY-MM-DD format)
  - Rainfall_mm (daily rainfall in millimeters)
  - Crop_Growth_cm (daily growth in centimeters)
  - Temperature_C (average daily temperature)

- `data_analyzer.py` - Main Python script with:
  - Data loading and validation
  - Statistical calculations
  - Visualization generation

## Requirements

```bash
pip install pandas matplotlib numpy
```

## Usage

```bash
python data_analyzer.py
```

### Output

The script generates:
1. **Console Output**: Detailed analysis summary with validation steps
2. **agri_tech_analysis.png**: 4-panel visualization showing:
   - Daily rainfall patterns
   - Crop growth trends
   - Rainfall-growth correlation scatter plot
   - Weekly trend analysis

## Data Analysis Results

The sample dataset demonstrates:
- **Correlation**: Positive relationship between rainfall and crop growth
- **Weekly Trends**: Identifies optimal rainfall patterns for growth
- **Data Quality**: Handles real-world messy data scenarios

## Portfolio Highlights

### Why This Impresses BBD (Data Engineering Focus)

1. **Real-world Problem**: Agricultural data is inherently messy
2. **Robust Error Handling**: Shows production-ready code practices
3. **Data Pipeline**: Load → Validate → Clean → Analyze → Visualize
4. **Scalability**: Code structure allows easy extension with more data sources
5. **Professional Output**: Publication-quality visualizations

### Technical Skills Demonstrated

- **Pandas**: DataFrames, resampling, grouping, correlation
- **Matplotlib**: Multi-subplot layouts, styling, data visualization best practices
- **NumPy**: Polynomial fitting for trend lines
- **Python**: Error handling, data validation, modular code design
- **Data Engineering**: ETL pipeline, data quality checks

## Extension Ideas

- Add multi-year trend analysis
- Implement predictive modeling (ML)
- Add soil moisture data
- Export results to HTML report
- Database integration (SQL)
- Real API data integration from weather services

## License

This is a portfolio project for educational and demonstration purposes.
