# Agri-Tech Data Analyzer 🌾📊

A professional Python web application for analyzing agricultural data. Upload your CSV or Excel files and get instant insights with beautiful interactive visualizations.

## 🎯 Project Overview

This portfolio project showcases:
- **Web Application**: Flask-based web interface with beautiful UI
- **File Upload**: Support for CSV and Excel files (xlsx, xls)
- **Data Validation**: Robust error handling for dirty data
- **Interactive Visualizations**: Plotly charts with instant analysis
- **Real-time Processing**: Instant results after file upload
- **Responsive Design**: Works seamlessly on desktop and mobile

## ✨ Features

### Core Functionality
✅ Upload CSV or Excel files via intuitive drag-and-drop interface  
✅ Automatic data validation and cleaning  
✅ Real-time statistical analysis and correlation calculation  
✅ Interactive 4-panel dashboard with Plotly charts  
✅ Weekly rainfall and crop growth trend analysis  
✅ Download sample template for testing  

### Error Handling & Data Quality
✅ Missing file detection and validation  
✅ Missing column detection with helpful error messages  
✅ Data type validation and automatic conversion  
✅ Handling negative/invalid values automatically  
✅ Forward/backward fill for missing data points  
✅ Detailed warning messages for data quality issues  

### User Interface
✅ Beautiful, modern dashboard design  
✅ Drag-and-drop file upload zone  
✅ Real-time file selection feedback  
✅ Loading animation during analysis  
✅ Responsive statistics cards  
✅ Interactive charts with hover information  
✅ Mobile-friendly responsive layout  

## 📁 Project Structure

```
Data Analyzer/
├── app.py                    # Flask application with analysis logic
├── data_analyzer.py          # CLI version (original script)
├── daily_crop_data.csv       # Sample dataset
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Beautiful web interface
├── uploads/                 # Temporary upload directory
└── README.md
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jackyphuti/Data-Analyzer.git
cd Data-Analyzer

# Install dependencies
pip install -r requirements.txt
```

### Run the Web App

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

### Run the CLI Version

```bash
python data_analyzer.py
```

## 📊 What You Can Do

1. **Upload Data**: Drag-and-drop your agricultural CSV or Excel file
2. **Instant Analysis**: Get immediate results with:
   - Average, total, and max rainfall
   - Average and max crop growth
   - Correlation between rainfall and growth
   - Date range and total records
3. **Visualize**: Interactive 4-panel dashboard showing:
   - Daily rainfall patterns (bar chart)
   - Crop growth trends (line chart)
   - Rainfall vs growth correlation (scatter plot with trend line)
   - Weekly aggregated trends

## 🔧 Technical Stack

### Backend
- **Flask**: Lightweight web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Plotly.js**: Interactive charts
- **Font Awesome**: Beautiful icons
- **Vanilla JavaScript**: Clean, fast interactions

## 📈 Data Format Requirements

Your CSV or Excel file should contain:

| Date | Rainfall_mm | Crop_Growth_cm | Temperature_C |
|------|-------------|-----------------|---------------|
| 2025-01-01 | 0.0 | 2.3 | 15.2 |
| 2025-01-02 | 2.5 | 2.5 | 16.1 |

- **Date**: YYYY-MM-DD format
- **Rainfall_mm**: Daily rainfall in millimeters
- **Crop_Growth_cm**: Daily growth in centimeters
- **Temperature_C**: (Optional) Average daily temperature

Download the sample template from the app to see the exact format!

## 💡 Why This Impresses BBD (Data Engineering Focus)

### Real-world Problem Solving
- Handles messy, incomplete agricultural data
- Demonstrates understanding of data quality issues
- Shows production-ready error handling patterns

### Complete Data Pipeline
- **Extract**: File upload with format support
- **Transform**: Data cleaning and validation
- **Load**: In-memory processing
- **Analyze**: Statistical calculations
- **Visualize**: Beautiful interactive charts

### Scalability & Extensibility
- Easy to add more data sources
- Can integrate with weather APIs
- Ready for machine learning models
- Database integration possible

### Professional Code Quality
- Modular function design
- Comprehensive error handling
- User-friendly feedback
- Clean, well-commented code

## 🎨 User Experience Highlights

- **Intuitive Interface**: No learning curve, immediately obvious how to use
- **Visual Feedback**: Clear status messages and loading states
- **Beautiful Design**: Modern gradient backgrounds and smooth animations
- **Fast Processing**: Instant analysis of uploaded files
- **Responsive**: Perfect on desktop, tablet, and mobile
- **Accessibility**: High contrast and readable fonts

## 📈 Analysis Insights

The dashboard automatically calculates:
- **Correlation Coefficient**: Shows relationship strength between rainfall and growth
  - Strong (>0.7): More rain = significantly more growth
  - Moderate (>0.4): Some relationship detected
  - Weak: Little to no relationship

- **Weekly Statistics**: Aggregated trends over weeks
- **Growth Patterns**: Daily trends and extremes
- **Rainfall Impact**: Visual correlation analysis

## 🔒 Security & Reliability

- File type validation (only CSV/xlsx/xls allowed)
- File size limit (16MB max)
- Automatic cleanup of temporary files
- Input sanitization for file names
- Error handling for all edge cases

## 🚀 Future Enhancement Ideas

- **Predictive Analysis**: Add ML models to predict crop growth
- **Multi-region Support**: Analyze data from multiple farms
- **Historical Comparison**: Year-over-year trend analysis
- **Export Reports**: Generate PDF reports with analysis
- **Database Integration**: Store analyses in SQL database
- **Real API Integration**: Connect to weather services
- **User Accounts**: Save and manage analyses
- **Advanced Filtering**: Filter data by date range or conditions

## 📝 License

This is a portfolio project for educational and demonstration purposes.

## 🤝 Contact

Built as a portfolio project for data engineering and agricultural technology positions.

---

**Made with ❤️ for AgriKonnect and BBD Data Engineering**
