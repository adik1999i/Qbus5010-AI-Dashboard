# Qbus5010-AI-Dashboard

Here's a comprehensive README.md that covers all environments:

# AI Impact Dashboard

A comprehensive interactive dashboard visualizing AI's impact on the job market, including job trends, skills analysis, salary insights, and career pathways in the AI field.

<img width="1439" alt="Screenshot 2024-10-23 at 4 47 06 PM" src="https://github.com/user-attachments/assets/d469ca46-d82e-4cb7-8a05-acbf56797c18">

## Features

- 📊 Real-time job market analytics
- 📈 Industry-wise AI skills penetration
- 💰 Salary trends across AI roles
- 🎯 Career pathway guidance
- 🔄 Job displacement vs creation analysis
- ⭐ Global AI skills ranking

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Development Setup](#development-setup)
- [Data Description](#data-description)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Methods

#### 1. Using pip
bash
# Clone the repository
git clone [your-repository-url]
cd ai-impact-dashboard

# Create and activate virtual environment
python -m venv venv

# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

#### 2. Using conda
bash
# Create and activate conda environment
conda create -n ai-dashboard python=3.9
conda activate ai-dashboard

# Install dependencies
pip install -r requirements.txt


#### 3. For Ed Workspace
bash
# Install directly in Ed environment
pip install -r requirements.txt


## Project Structure

ai-impact-dashboard/
├── assets/
│   └── style.css          # Dashboard styling
├── data/
│   ├── AI_Career_Pathway_Dataset (1).csv
│   ├── AI_Compute_Job_Demand.csv
│   ├── AI_Job_Statistics_Displacement_Undisplacement.csv
│   ├── AI_Salaries_2020_2024.csv
│   ├── AI_Skills_Penetration_by_Industry.csv
│   ├── AI_Talent_Concentration_by_Country_Industry_Corrected.csv
│   ├── Global_Top_Skills (1).csv
│   └── Skill_Distribution_by_Job_Cluster.csv
├── app.py                 # Main application file
├── requirements.txt       # Package dependencies
└── README.md             # Documentation


## Running the Application

### Local Development
```bash
python app.py
```
Navigate to http://127.0.0.1:8050/ in your browser

### VS Code
1. Open the project in VS Code
2. Ensure Python extension is installed
3. Select your Python interpreter (venv or conda)
4. Run app.py using the play button or terminal

### PyCharm
1. Open the project
2. Configure Python interpreter
3. Right-click app.py and select 'Run'

### Ed Workspace
1. Run `python app.py`
2. Click on the "ports" tab and find port 8050

## Development Setup

### VS Code Recommended Extensions
- Python
- Pylance
- Python Docstring Generator
- GitLens

### Code Style
bash

# Install development dependencies
pip install -r requirements-dev.txt

# Run formatters
black app.py
isort app.py

# Run linters
flake8 app.py
pylint app.py


## Dashboard Components

### 1. Overview Metrics
- Total AI jobs count
- AI job market growth rate
- Average salary metrics
- Top skill demand

### 2. Interactive Visualizations
- Job trends by country
- Skills penetration analysis
- Displacement impact analysis
- Salary comparisons
- Skills ranking

### 3. Career Guidance
- Role-based pathways
- Skill requirement mapping
- Resource recommendations

## Data Description

The dashboard utilizes multiple datasets:
python
datasets = {
    'career_pathway': 'Career progression paths',
    'job_demand': 'Job posting trends',
    'displacement': 'AI impact on employment',
    'salaries': 'Role-based salary data',
    'skills_penetration': 'Industry AI adoption',
    'global_skills': 'Skill importance ranking'
}


## Browser Support
- Chrome (80+)
- Firefox (75+)
- Safari (13+)
- Edge (80+)

## Troubleshooting

### Common Issues

1. Port Conflicts
python
# Modify in app.py
port = int(os.environ.get('PORT', 8051))  # Change port number


2. Data Loading Errors
python
# Check file paths
import os
print("Working Directory:", os.getcwd())
print("Available Files:", os.listdir('data'))


3. Package Conflicts
bash
pip install --upgrade -r requirements.txt


### Environment-Specific Solutions

#### VS Code
- Set Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
- Debug: Use launch.json configuration

#### PyCharm
- Set Project Interpreter: Settings → Project → Python Interpreter
- Debug: Use built-in debugger

#### Ed Workspace
- Check port availability
- Verify file permissions

## Performance Optimization

python
# Memory optimization
def optimize_dataframes():
    for df in [df_list]:
        for col in df.select_dtypes(['object']):
            df[col] = df[col].astype('category')


## Contributing

1. Fork the repository
2. Create feature branch
bash
git checkout -b feature/AmazingFeature

3. Commit changes
bash
git commit -m 'Add AmazingFeature'

4. Push to branch
bash
git push origin feature/AmazingFeature

5. Open Pull Request

## Dependencies

Core packages:
- dash==2.11.0
- dash-bootstrap-components==1.4.2
- pandas==1.5.3
- plotly==5.13.1

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Data sources
- Dash documentation
- Plotly community
- Bootstrap components

## Contact & Support
linkedin - https://www.linkedin.com/in/aditya-kartikeyan-46a0b6166/


