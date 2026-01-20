"""
Agri-Tech Data Analyzer - Web Application
A beautiful Flask web app for analyzing agricultural data
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_data(filepath):
    """Load CSV or Excel file"""
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        return df, None
    except Exception as e:
        return None, str(e)


def validate_data(df):
    """Validate and clean data"""
    errors = []
    warnings = []
    
    # Check required columns
    required_columns = ['Date', 'Rainfall_mm', 'Crop_Growth_cm']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        # Try to find similar columns (case-insensitive)
        available_cols = df.columns.tolist()
        for req_col in required_columns:
            if req_col not in df.columns:
                similar = [col for col in available_cols if req_col.lower().replace('_', '').replace('mm', '').replace('cm', '') 
                          in col.lower().replace('_', '').replace('mm', '').replace('cm', '')]
                if not similar:
                    errors.append(f"Missing required column: {req_col}")
    
    if errors:
        return None, errors, warnings
    
    # Handle missing values
    if df.isnull().any().any():
        warnings.append(f"Found {df.isnull().sum().sum()} missing values - filling with forward fill")
        df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Convert data types
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Rainfall_mm'] = pd.to_numeric(df['Rainfall_mm'])
        df['Crop_Growth_cm'] = pd.to_numeric(df['Crop_Growth_cm'])
    except Exception as e:
        errors.append(f"Data type conversion failed: {str(e)}")
        return None, errors, warnings
    
    # Check for negative values
    if (df['Rainfall_mm'] < 0).any():
        warnings.append("Found negative rainfall values - setting to 0")
        df.loc[df['Rainfall_mm'] < 0, 'Rainfall_mm'] = 0
    
    if (df['Crop_Growth_cm'] < 0).any():
        warnings.append("Found negative growth values - removing those rows")
        df = df[df['Crop_Growth_cm'] >= 0]
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df, errors, warnings


def calculate_statistics(df):
    """Calculate key statistics"""
    stats = {
        'total_records': len(df),
        'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
        'avg_rainfall': round(df['Rainfall_mm'].mean(), 2),
        'max_rainfall': round(df['Rainfall_mm'].max(), 2),
        'total_rainfall': round(df['Rainfall_mm'].sum(), 2),
        'avg_growth': round(df['Crop_Growth_cm'].mean(), 2),
        'max_growth': round(df['Crop_Growth_cm'].max(), 2),
        'correlation': round(df['Rainfall_mm'].corr(df['Crop_Growth_cm']), 4),
    }
    return stats


def create_visualizations(df):
    """Create interactive Plotly visualizations"""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Daily Rainfall", "Daily Crop Growth", 
                       "Rainfall vs Growth Correlation", "Weekly Trends"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": True}]]
    )
    
    # Plot 1: Daily Rainfall (Bar chart)
    fig.add_trace(
        go.Bar(x=df['Date'], y=df['Rainfall_mm'], name='Rainfall (mm)',
               marker=dict(color='steelblue'), showlegend=True),
        row=1, col=1
    )
    
    # Plot 2: Daily Crop Growth (Line chart)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Crop_Growth_cm'], name='Growth (cm)',
                   mode='lines+markers', line=dict(color='green', width=2),
                   fill='tozeroy', fillcolor='rgba(0, 128, 0, 0.2)', showlegend=True),
        row=1, col=2
    )
    
    # Plot 3: Scatter plot with trend line
    correlation = df['Rainfall_mm'].corr(df['Crop_Growth_cm'])
    
    fig.add_trace(
        go.Scatter(x=df['Rainfall_mm'], y=df['Crop_Growth_cm'], name='Data Points',
                   mode='markers', marker=dict(size=6, color='darkgreen', opacity=0.6),
                   showlegend=True),
        row=2, col=1
    )
    
    # Add trend line
    z = np.polyfit(df['Rainfall_mm'], df['Crop_Growth_cm'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df['Rainfall_mm'].min(), df['Rainfall_mm'].max(), 100)
    
    fig.add_trace(
        go.Scatter(x=x_trend, y=p(x_trend), name=f'Trend (R={correlation:.2f})',
                   mode='lines', line=dict(color='red', width=2, dash='dash'),
                   showlegend=True),
        row=2, col=1
    )
    
    # Plot 4: Weekly aggregates
    weekly_data = df.set_index('Date').resample('W').agg({
        'Rainfall_mm': 'sum',
        'Crop_Growth_cm': 'mean'
    }).reset_index()
    
    fig.add_trace(
        go.Bar(x=weekly_data['Date'], y=weekly_data['Rainfall_mm'], 
               name='Weekly Rainfall (mm)', marker=dict(color='lightblue'),
               showlegend=True),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=weekly_data['Date'], y=weekly_data['Crop_Growth_cm'],
                   name='Avg Weekly Growth (cm)', mode='lines+markers',
                   line=dict(color='red', width=2), marker=dict(size=6),
                   showlegend=True),
        row=2, col=2, secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title_text="Agri-Tech Data Analysis Dashboard",
        height=900,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1, gridcolor='white')
    fig.update_xaxes(title_text="Date", row=1, col=2, gridcolor='white')
    fig.update_xaxes(title_text="Rainfall (mm)", row=2, col=1, gridcolor='white')
    fig.update_xaxes(title_text="Date", row=2, col=2, gridcolor='white')
    
    fig.update_yaxes(title_text="Rainfall (mm)", row=1, col=1, gridcolor='white')
    fig.update_yaxes(title_text="Growth (cm)", row=1, col=2, gridcolor='white')
    fig.update_yaxes(title_text="Growth (cm)", row=2, col=1, gridcolor='white')
    fig.update_yaxes(title_text="Weekly Rainfall (mm)", row=2, col=2, gridcolor='white')
    fig.update_yaxes(title_text="Growth (cm)", row=2, col=2, secondary_y=True)
    
    return fig.to_html(include_plotlyjs='cdn')


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle file upload and analysis"""
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'File must be CSV or Excel (xlsx/xls)'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load data
        df, error = load_data(filepath)
        if error:
            return jsonify({'success': False, 'error': f'Failed to load file: {error}'}), 400
        
        # Validate data
        df, errors, warnings = validate_data(df)
        if errors:
            return jsonify({'success': False, 'error': ', '.join(errors)}), 400
        
        # Calculate statistics
        stats = calculate_statistics(df)
        
        # Create visualizations
        html_plot = create_visualizations(df)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'stats': stats,
            'warnings': warnings,
            'plot': html_plot
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'An error occurred: {str(e)}'}), 500


@app.route('/template')
def download_template():
    """Download sample CSV template"""
    try:
        template_path = 'daily_crop_data.csv'
        return send_file(template_path, as_attachment=True, download_name='template.csv')
    except:
        return jsonify({'success': False, 'error': 'Template not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
