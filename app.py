import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# datasets
ai_career_pathway_dataset = pd.read_csv('data/AI_Career_Pathway_Dataset (1).csv')
ai_compute_job_demand = pd.read_csv('data/AI_Compute_Job_Demand.csv')
ai_job_statistics_displacement = pd.read_csv('data/AI_Job_Statistics_Displacement_Undisplacement.csv')
ai_salaries = pd.read_csv('data/AI_Salaries_2020_2024.csv')
ai_skills_penetration = pd.read_csv('data/AI_Skills_Penetration_by_Industry.csv')
ai_talent_concentration = pd.read_csv('data/AI_Talent_Concentration_by_Country_Industry_Corrected.csv')
global_top_skills = pd.read_csv('data/Global_Top_Skills (1).csv')
skill_distribution_by_job_cluster = pd.read_csv('data/Skill_Distribution_by_Job_Cluster.csv')

global_jobs_data = ai_compute_job_demand[ai_compute_job_demand['Country'] == 'Global']

# Total jobs created by AI (aggregated from compute job demand dataset for Global)
total_jobs = global_jobs_data['Total_Job_postings'].sum()

# Average AI role salary (across all countries and industries)
average_salary = ai_salaries['Salary'].mean()

# Most in-demand AI skill (from the global top skills dataset)
most_in_demand_skill = global_top_skills.loc[global_top_skills['Ranking'].idxmin(), 'Skill']


def calculate_growth_percentage(data):
    global_jobs_data = data[data['Country'] == 'Global']
    job_postings_per_year = global_jobs_data.groupby('Year')['Total_Job_postings'].sum().reset_index()
    if len(job_postings_per_year) < 2:
        return 0
    # Calculate growth between the most recent and the previous year
    most_recent = job_postings_per_year.iloc[-1]['Total_Job_postings']
    previous = job_postings_per_year.iloc[-2]['Total_Job_postings']
    growth_percentage = ((most_recent - previous) / previous) * 100 if previous != 0 else 0
    return growth_percentage

growth_percentage = calculate_growth_percentage(ai_compute_job_demand)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    # KPI Cards
     dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H5("Total AI-related jobs available", className="card-title text-center"),
            html.H2(f"{total_jobs:,}", className="card-text text-center")  
        ])]), width=3, className='mb-4'),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H5("Growth in AI Jobs (Last Year)", className="card-title text-center"),
            html.H2(f"{growth_percentage:.2f}%", className="card-text text-center") 
        ])]), width=3, className='mb-4'),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H5("Average AI Role Salary", className="card-title text-center"),
            html.H2(f"${average_salary:,.2f}", className="card-text text-center")  
        ])]), width=3, className='mb-4'),
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H5("Top Skill in Demand", className="card-title text-center"),
            html.H2(most_in_demand_skill, className="card-text text-center")  
        ])]), width=3, className='mb-4')
    ], className='g-4 p-3'),

    # Overview Chart for Job Trends
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='job-trends-line-chart',
                figure=px.line(
                    global_jobs_data.groupby('Year')['Total_Job_postings'].sum().reset_index(),
                    x='Year',
                    y='Total_Job_postings',
                    title='Job Trends Over Time (Global)'
                )
            )
        ])
    ])
])



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
