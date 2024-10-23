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

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
    ]
)

#header section
header = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand([
            html.I(className="fas fa-brain me-2"),
            "AI Impact Dashboard"
        ], className="ms-2")
    ], fluid=True),
    className="mb-4"
)
# Footer Section
footer = html.Footer(
    dbc.Container([
        html.P("AI Impact Dashboard © 2024. All rights reserved.",
               className="footer-text"),
        html.Div([
            "Connect with me on ",
            html.A(
                [
                    html.I(className="fab fa-linkedin me-1"),
                    "LinkedIn"
                ],
                href="https://www.linkedin.com/in/aditya-kartikeyan-46a0b6166/",
                target="_blank",
                className="footer-link",
                style={
                    'color': '#0077b5',
                    'textDecoration': 'none',
                    'fontWeight': 'bold'
                }
            )
        ], className="footer-text"),
    ], fluid=True),
    className="dashboard-footer"
)

def create_metric_card(title, value, icon_class):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon_class} fa-2x mb-3"),
                html.H6(title, className="metric-card card-title text-center"),
                html.H2(value, className="metric-card card-text text-center")
            ], className="text-center")
        ])
    ], className="dashboard-card metric-card")

def create_chart_section(title, dropdown_label, dropdown_id, dropdown_options, dropdown_value, graph_id, source ,multi=False):
    return dbc.Card([
        dbc.CardBody([
            html.H4(title, className="section-title text-center"),
            html.Div([
                html.Label(dropdown_label),
                dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    value=dropdown_value,
                    multi=multi,
                    className="dash-dropdown"
                ),
                dcc.Graph(id=graph_id, className="graph-container"),
                 html.Div([
                    html.I(className="fas fa-info-circle me-2"),
                    "Source: ",
                    html.Span(source, style={'fontStyle': 'italic'})
                ], className="source-citation")
            ])
        ])
    ], className="dashboard-card")



# General overview section with cards
general_overview_section = dbc.Container([
    dbc.Row([
        dbc.Col(create_metric_card(
            "Total AI Jobs", 
            f"{total_jobs:,}", 
            "fas fa-briefcase"
        ), width=3),
        dbc.Col(create_metric_card(
            "Growth Rate", 
            f"{growth_percentage:.1f}%", 
            "fas fa-chart-line"
        ), width=3),
        dbc.Col(create_metric_card(
            "Average Salary", 
            f"${average_salary:,.0f}", 
            "fas fa-dollar-sign"
        ), width=3),
        dbc.Col(create_metric_card(
            "Top Skill", 
            most_in_demand_skill, 
            "fas fa-star"
        ), width=3),
    ], className="g-4")
], fluid=True)


# Job trends chart section
job_trends_section = create_chart_section(
    "Job Trends Over Time",
    "Country:",
    "job-country-filter",
    [{'label': country, 'value': country} for country in ai_compute_job_demand['Country'].unique()],
    'Global',
    'job-trends-line-chart',
    "LinkedIn Economic Graph"
)

#skills penetration section
skills_penetration_section = create_chart_section(
    "AI Skills Penetration by Industry",
    "Country:",
    "ai-country-filter",
    [{'label': country, 'value': country} for country in ai_skills_penetration['Country'].unique()],
    [ai_skills_penetration['Country'].unique()[0]],
    'ai-skills-penetration-bar-chart',
    "LinkedIn Economic Graph",
    multi=True
)

# Job displacement vs AI jobs created section
job_displacement_section = dbc.Card([
    dbc.CardBody([
        html.H4("AI Jobs Created vs Job Displacement", className="section-title text-center"),
        dbc.Row([
            dbc.Col([
                html.Label("Country:"),
                dcc.Dropdown(
                    id='country-filter',
                    options=[{'label': country, 'value': country} 
                            for country in ai_job_statistics_displacement['Country'].unique()],
                    value='United States',
                    className="dash-dropdown"
                ),
            ], width=6),
            dbc.Col([
                html.Label("Industry:"),
                dcc.Dropdown(
                    id='industry-filter',
                    options=[{'label': industry, 'value': industry} 
                            for industry in ai_job_statistics_displacement['Industry'].unique()],
                    value='Technology',
                    className="dash-dropdown"
                ),
            ], width=6),
        ]),
        dcc.Graph(id='job-displacement-vs-ai-jobs-created', className="graph-container"),
        html.Div([
            html.I(className="fas fa-info-circle me-2"),
            "Source: World Economic Graph"
        ], className="source-citation")
    
    ])
], className="dashboard-card")

# Salary insights section
salary_insights_section = dbc.Card([
    dbc.CardBody([
        html.H4("Average Salary by Job Role", className="section-title text-center"),
        html.Div([
            html.Label("Industry:", className="dropdown-label"),
            dcc.Dropdown(
                id='salary-industry-filter',
                options=[{'label': industry, 'value': industry} 
                        for industry in ai_salaries['Industry'].unique()],
                value='Technology',
                multi=False,
                className="dash-dropdown"
            ),
            dcc.Graph(
                id='role-salary-comparison-bar-chart',
                className="graph-container"
            ),
             html.Div([
            html.I(className="fas fa-info-circle me-2"),
            "Source: Payscale, Glassdoor"
        ], className="source-citation")
        ])
    ])
], className="dashboard-card")


# Top skills section
top_skills_section = dbc.Card([
    dbc.CardBody([
        html.H4("Top AI Skills by Global Ranking", className="section-title text-center"),
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
                labels={
                    'SkillWithRank': 'AI Skills',
                    'InverseRank': 'Importance Score'
                },
                color='InverseRank',
                color_continuous_scale=['#182848', '#4b6cb7']  # Theme gradient
            ).update_layout(
                title={
                    'text': 'Top AI Skills by Global Ranking',
                    'x': 0.5,
                    'y': 0.95,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2c3e50'}
                },
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'color': '#2c3e50'},
                margin={'t': 80, 'r': 30, 'l': 30, 'b': 150},
                showlegend=False,
                xaxis=dict(
                    tickangle=45,
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(0,0,0,0.1)',
                    linecolor='rgba(0,0,0,0.1)'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(0,0,0,0.1)',
                    linecolor='rgba(0,0,0,0.1)'
                )
            )
        ),
        html.Div([
            html.I(className="fas fa-info-circle me-2"),
            "Source: OECD.AI"
        ], className="source-citation")
    ])
], className="dashboard-card")


# Career roadmap section
career_roadmap_section = dbc.Card([
    dbc.CardBody([
        html.H4("Career Pathway", className="section-title text-center"),
        html.Div([
            html.Label("Select a Role:", className="dropdown-label"),
            dcc.Dropdown(
                id='role-dropdown',
                options=[{'label': role, 'value': role} 
                        for role in ai_career_pathway_dataset['Role'].unique()],
                value='Machine Learning Engineer',
                className="dash-dropdown"
            ),
            html.Div([
                dbc.ButtonGroup([
                    dbc.Button(
                        "BEGINNER",
                        id='beginner',
                        className="roadmap-btn",
                        color="outline-primary",
                        n_clicks=0
                    ),
                    dbc.Button(
                        "INTERMEDIATE",
                        id='intermediate',
                        className="roadmap-btn",
                        color="outline-primary",
                        n_clicks=0
                    ),
                    dbc.Button(
                        "ADVANCED",
                        id='advanced',
                        className="roadmap-btn",
                        color="outline-primary",
                        n_clicks=0
                    ),
                ], className="roadmap-level")
            ]),
            html.Div(id='level-details', className="level-details")
        ], className="career-pathway-container"),
        html.Div([
            html.I(className="fas fa-info-circle me-2"),
            "Source: Coursera, Khan Academy, DataCamp"
        ], className="source-citation")
    ])
], className="dashboard-card")

# app Layout 
app.layout = dbc.Container([
    header,
    general_overview_section,
    dbc.Row([
        dbc.Col(job_trends_section, md=6),
        dbc.Col(skills_penetration_section, md=6) 
    ], className="g-4"),
    dbc.Row([
        dbc.Col(job_displacement_section, md=6),
        dbc.Col(salary_insights_section, md=6)
    ], className="g-4"),
    dbc.Row([
        dbc.Col(top_skills_section, md=8),
        dbc.Col(career_roadmap_section, md=4)
    ], className="g-4"),
    footer
], fluid=True)

# call backs for all charts
@app.callback(
    Output('job-trends-line-chart', 'figure'),
    [Input('job-country-filter', 'value')]
)

def update_job_trends_chart(selected_country):
    filtered_data = ai_compute_job_demand[ai_compute_job_demand['Country'] == selected_country]
    
    figure = px.line(
        filtered_data.groupby('Year')['Total_Job_postings'].sum().reset_index(),
        x='Year',
        y='Total_Job_postings',
        line_shape='spline',  
        markers=True  
    )

   
    figure.update_traces(
        line_color='#4b6cb7',
        marker=dict(size=8, color='#4b6cb7', line=dict(color='white', width=2))
    )
    
    figure.update_layout(
        title={
            'text': f'Job Trends Over Time ({selected_country})',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': '#2c3e50'},
        margin={'t': 80, 'r': 30, 'l': 30, 'b': 30},
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        )
    )
    return figure


@app.callback(
    Output('ai-skills-penetration-bar-chart', 'figure'),
    [Input('ai-country-filter', 'value')]
)
def update_ai_skills_penetration_chart(selected_countries):
    filtered_data = ai_skills_penetration[ai_skills_penetration['Country'].isin(selected_countries)]
    
    figure = px.bar(
        filtered_data,
        x='Industry',
        y='Relative_AI_Skills_Penetration',
        color='Country',
        color_discrete_sequence=['#4b6cb7', '#182848', '#6a8fd4', '#2c4a89']  # Theme colors
    )
    
    figure.update_layout(
        title={
            'text': 'AI Skills Penetration by Industry',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': '#2c3e50'},
        margin={'t': 80, 'r': 30, 'l': 30, 'b': 30},
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        )
    )
    return figure


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
        barmode='group',
        color_discrete_sequence=['#4b6cb7', '#182848']  # Theme colors
    )
    
    figure.update_layout(
        title={
            'text': f'AI Jobs Created vs Job Displacement in {selected_country} - {selected_industry}',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': '#2c3e50'},
        margin={'t': 80, 'r': 30, 'l': 30, 'b': 30},
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)'
        )
    )
    return figure


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
        color_discrete_sequence=['#4b6cb7']  # Theme color
    )
    
    figure.update_layout(
        title={
            'text': f'Average Salary by Job Role in {selected_industry} Industry',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': '#2c3e50'},
        margin={'t': 80, 'r': 30, 'l': 30, 'b': 30},
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)',
            tickangle=45
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            linecolor='rgba(0,0,0,0.1)',
            title='Average Salary ($)'
        )
    )
    
    
    figure.update_yaxes(tickprefix="$", tickformat=",.0f")
    
    return figure


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
       
        filtered_data = ai_career_pathway_dataset[
            (ai_career_pathway_dataset['Role'] == selected_role) & 
            (ai_career_pathway_dataset['Level'] == level)
        ]
        if not filtered_data.empty:
            skills = filtered_data.iloc[0]['Skills']
            resources = filtered_data.iloc[0]['Resources'].split(',') 
            
            # Create course links
            course_links = []
            for i, resource in enumerate(resources, 1):
                course_links.append(
                    html.A(
                        f"Course {i}",
                        href=resource.strip(),
                        target="_blank",
                        className="course-link",
                        style={
                            'display': 'inline-block',
                            'padding': '8px 16px',
                            'margin': '5px',
                            'backgroundColor': '#4b6cb7',
                            'color': 'white',
                            'borderRadius': '4px',
                            'textDecoration': 'none',
                            'transition': 'background-color 0.3s'
                        }
                    )
                )
            
            return html.Div([
                html.H3(f"{level} Level Skills:", 
                       style={'color': '#2c3e50', 'marginBottom': '1rem'}),
                html.P([skill.strip(",") for skill in skills.split(',')],
                      style={'color': '#6c757d', 'marginBottom': '2rem'}),
                html.H3("Recommended Courses:", 
                       style={'color': '#2c3e50', 'marginBottom': '1rem'}),
                html.Div(course_links, 
                        style={'marginBottom': '1rem'})
            ])
            
    return html.Div("Please click on a level to see the details.",
                   style={'textAlign': 'center', 'color': '#6c757d'})

server = app.server

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

