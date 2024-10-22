import dash
from dash import dcc, html, Input, Output, ctx
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
#header section
header = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("AI Impact Dashboard", className="ms-2"),
    ],fluid=True),
    color="dark",
    dark=True,
    sticky="top",
    className="mb-4",
    
)

# Footer Section
footer = dbc.Container(
    html.Div([
        html.P("AI Impact Dashboard © 2024. All rights reserved.",
               className="text-center text-muted"),
        html.P("Contact us at: contact@ai-dashboard.com",
               className="text-center text-muted"),
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa'}),
    fluid=True
)

# General overview section with cards
general_overview_section = dbc.Container([
    dbc.Row(
        [
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Total AI-related jobs available", className="card-title text-center"),
                html.H2(f"{total_jobs:,}", className="card-text text-center")
            ]), className='mb-4'), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Growth in AI Jobs (Last Year)", className="card-title text-center"),
                html.H2(f"{growth_percentage:.2f}%", className="card-text text-center")
            ]), className='mb-4'), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Average AI Role Salary", className="card-title text-center"),
                html.H2(f"${average_salary:,.2f}", className="card-text text-center")
            ]), className='mb-4'), width=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Top Skill in Demand", className="card-title text-center"),
                html.H2(most_in_demand_skill, className="card-text text-center")
            ]), className='mb-4'), width=3),
        ],
        className='g-4'
    )
], fluid=True)

# Job trends chart section
job_trends_section = dbc.Card(
    dbc.CardBody([
        html.H4("Job Trends Over Time (Global)", className="card-title text-center"),
        dcc.Graph(
            id='job-trends-line-chart',
            figure=px.line(
                global_jobs_data.groupby('Year')['Total_Job_postings'].sum().reset_index(),
                x='Year',
                y='Total_Job_postings',
                title='Job Trends Over Time (Global)'
            ).update_layout(title_x=0.5)
        )
    ]),
    className='mb-4'
)

# Job displacement vs AI jobs created section
job_displacement_section = dbc.Card(
    dbc.CardBody([
        html.H4("AI Jobs Created vs Job Displacement", className="card-title text-center"),
        html.Div([
            html.Label('Country:'),
            dcc.Dropdown(
                id='country-filter',
                options=[{'label': country, 'value': country} for country in ai_job_statistics_displacement['Country'].unique()],
                value='United States',
                multi=False
            ),
            html.Label('Industry:'),
            dcc.Dropdown(
                id='industry-filter',
                options=[{'label': industry, 'value': industry} for industry in ai_job_statistics_displacement['Industry'].unique()],
                value='Technology',
                multi=False
            )
        ], style={'padding': '10px'}),
        dcc.Graph(id='job-displacement-vs-ai-jobs-created')
    ]),
    className='mb-4'
)

# Salary insights section
salary_insights_section = dbc.Card(
    dbc.CardBody([
        html.H4("Average Salary by Job Role", className="card-title text-center"),
        html.Div([
            html.Label('Industry:'),
            dcc.Dropdown(
                id='salary-industry-filter',
                options=[{'label': industry, 'value': industry} for industry in ai_salaries['Industry'].unique()],
                value='Technology',
                multi=False
            )
        ], style={'padding': '10px'}),
        dcc.Graph(id='role-salary-comparison-bar-chart')
    ]),
    className='mb-4'
)

# Top skills section
top_skills_section = dbc.Card(
    dbc.CardBody([
        html.H4("Top AI Skills by Global Ranking", className="card-title text-center"),
        dcc.Graph(
            id='top-skills-bar-chart',
            figure=px.bar(
                global_top_skills.assign(
                    InverseRank=21 - global_top_skills['Ranking'],
                    SkillWithRank=global_top_skills.apply(
                        lambda x: f"#{x['Ranking']} {x['Skill']}", axis=1
                    )
                ).sort_values('Ranking'),
                x='SkillWithRank',
                y='InverseRank',
                title='Top AI Skills by Global Ranking',
                labels={
                    'SkillWithRank': 'AI Skills',
                    'InverseRank': 'Importance Score (Higher is Better)'
                },
                color='InverseRank',
                orientation='v',
                color_continuous_scale='Viridis',
                height=600
            ).update_layout(
                title_x=0.5,
                xaxis=dict(tickangle=45, title_font=dict(size=14)),
                yaxis=dict(title_font=dict(size=14), showgrid=True),
                showlegend=False,
                margin=dict(b=150)
            )
        )
    ]),
    className='mb-4'
)

# Career roadmap section
career_roadmap_section = dbc.Card(
    dbc.CardBody([
        html.H4("Career Pathway", className="card-title text-center"),
        html.Label("Select a Role:"),
        dcc.Dropdown(
            id='role-dropdown',
            options=[{'label': role, 'value': role} for role in ai_career_pathway_dataset['Role'].unique()],
            value='Machine Learning Engineer'
        ),
        html.Div(id='roadmap-container', children=[
            html.Div(className="roadmap-level", children=[
                html.Button("BEGINNER", id='beginner', className="roadmap-circle btn btn-outline-secondary", n_clicks=0),
                html.Button("INTERMEDIATE", id='intermediate', className="roadmap-circle btn btn-outline-secondary", n_clicks=0),
                html.Button("ADVANCED", id='advanced', className="roadmap-circle btn btn-outline-secondary", n_clicks=0)
            ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px'})
        ]),
        html.Div(id='level-details')
    ]),
    className='mb-4'
)

# Layout with container and rows
dashboard_layout = dbc.Container([
    header,
    general_overview_section,
    dbc.Row([
        dbc.Col(job_trends_section, md=12)
    ], className='g-4'),
    dbc.Row([
        dbc.Col(job_displacement_section, md=6),
        dbc.Col(salary_insights_section, md=6)
    ], className='g-4'),
    dbc.Row([
        dbc.Col(top_skills_section, md=8),
        dbc.Col(career_roadmap_section, md=4)
    ], className='g-4'),
    footer
], fluid=True)

app.layout = dashboard_layout

# Callback to update the job displacement vs AI jobs created chart based on filters
@app.callback(
    Output('job-displacement-vs-ai-jobs-created', 'figure'),
    [Input('country-filter', 'value'),
     Input('industry-filter', 'value')]
)
def update_job_displacement_chart(selected_country, selected_industry):
    filtered_data = ai_job_statistics_displacement[
        (ai_job_statistics_displacement['Country'] == selected_country) &
        (ai_job_statistics_displacement['Industry'] == selected_industry)
    ]
    
    figure = px.bar(
        filtered_data,
        x='Year',
        y=['Jobs Created by AI', 'Job Displacement by AI'],
        title=f'AI Jobs Created vs Job Displacement in {selected_country} - {selected_industry}',
        barmode='group',
        labels={'variable': 'Job Type', 'value': 'Number of Jobs'}
    )
    return figure

# Callback to update the role-based salary comparison chart based on selected industry
@app.callback(
    Output('role-salary-comparison-bar-chart', 'figure'),
    [Input('salary-industry-filter', 'value')]
)
def update_role_salary_comparison_chart(selected_industry):
    filtered_data = ai_salaries[ai_salaries['Industry'] == selected_industry]
    
    average_salary_by_role = filtered_data.groupby('Role/Job Type')['Salary'].mean().reset_index()
    
    figure = px.bar(
        average_salary_by_role,
        x='Role/Job Type',
        y='Salary',
        title=f'Average Salary by Job Role in {selected_industry} Industry',
        labels={'Role/Job Type': 'Job Role', 'Salary': 'Average Salary'}
    )
    return figure

# Callback to update level details based on selected role and level
@app.callback(
    Output('level-details', 'children'),
    [Input('role-dropdown', 'value'),
     Input('beginner', 'n_clicks'),
     Input('intermediate', 'n_clicks'),
     Input('advanced', 'n_clicks')]
)
def update_level_details(selected_role, beginner_clicks, intermediate_clicks, advanced_clicks):
    level = None
    triggered_id = ctx.triggered_id if ctx.triggered_id else None
    
    if triggered_id == 'beginner':
        level = 'Beginner'
    elif triggered_id == 'intermediate':
        level = 'Intermediate'
    elif triggered_id == 'advanced':
        level = 'Advanced'
    
    if level:
        # Filter dataset based on selected role and level
        filtered_data = ai_career_pathway_dataset[(ai_career_pathway_dataset['Role'] == selected_role) & (ai_career_pathway_dataset['Level'] == level)]
        if not filtered_data.empty:
            skills = filtered_data.iloc[0]['Skills']
            resources = filtered_data.iloc[0]['Resources']
            return html.Div([
                html.H3(f"{level} Level Skills:"),
                html.P(skills),
                html.H3(f"Recommended Resources:"),
                html.A(f"Learn More", href=resources, target="_blank")
            ])
    return html.Div("Please click on a level to see the details.")

server = app.server

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
