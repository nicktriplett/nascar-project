# JGR Project Results (UPDATED)
# Nicholas Triplett

import os
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

current_dir = os.path.dirname(os.path.abspath(__file__))

pages_folder = os.path.join(current_dir, 'pages')

data_file = os.path.join(pages_folder, 'playoff_driver_racing_data.csv')

df = pd.read_csv(data_file, header=None, encoding='latin-1')
df.columns = df.iloc[0]
df = df[1:]
df = df.reset_index(drop=True)
df[['Start','Finish','Wins','Top 5s','Top 10s','DNFs','Laps Led','Points','Playoff Points Earned','Laps Completed']] = df[['Start','Finish','Wins','Top 5s','Top 10s','DNFs','Laps Led','Points','Playoff Points Earned','Laps Completed']].apply(pd.to_numeric, errors='coerce').astype('Int64')

displayed_df = df[['Driver Full Name', 'Race ID', 'Track Name', 'Season','Race','Start','Finish','Interval', 'Wins', 'Top 5s', 'Top 10s', 'DNFs','Points']].copy()
second_round_average_figures = displayed_df

custom_driver_order = ['Christopher Bell','Ryan Blaney','Alex Bowman','Chase Briscoe','William Byron','Austin Cindric','Chase Elliott','Denny Hamlin','Kyle Larson','Joey Logano','Tyler Reddick','Daniel Suárez']
custom_track_order = ['Kansas Speedway','Talladega Superspeedway','Charlotte Motor Speedway Road Course']

driver_options = [{'label': driver, 'value': driver} for driver in custom_driver_order if driver in displayed_df['Driver Full Name'].unique()]
driver_options = [{'label': driver, 'value': driver} for driver in custom_driver_order if driver in  second_round_average_figures['Driver Full Name'].unique()]
track_options = [{'label': track, 'value': track} for track in custom_track_order if track in displayed_df['Track Name'].unique()]

X = df[['Race ID']]
y = df['Points']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = LinearRegression()
model.fit(X_train, y_train)

app = Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.title = "Nicholas Triplett JGR Project"

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(
                children=[
                    html.Img(
                    src='https://raw.githubusercontent.com/nicktriplett/jgr-performance-project/main/assets/nascarplayoffslogo.png',
                    style={
                        'width':'100%',
                        'height':'auto',
                        'vertical-align':'',
                        'object-fit':'contain'}
                    )
                ],
                width={'size': 2}
            ),
            dbc.Col(
                children=[
                    html.H3('Nicholas Triplett - NASCAR Second Round Performance Project',className='text-center mt-4'),
                ],
                width={'size': 8}
                ),
            dbc.Col(
                children=[
                    html.Img(
                    src='https://raw.githubusercontent.com/nicktriplett/jgr-performance-project/main/assets/jgrlogo.png',
                    style={
                        'width':'100%',
                        'height':'auto',
                        'vertical-align':'top',
                        'object-fit':'contain',
                        'margin-top':'-6px',
                        }
                    )
                ],
                width={'size': 2},
                style={'display': 'flex', 'align-items': 'center'}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.P('Driver and Track Selection',className='fs-4 text-center mt-0')
                ],
                width=12,
            )
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    dcc.Dropdown(
                        id='driver-dropdown',
                        options=driver_options,
                        value='Denny Hamlin',
                        clearable=False,
                        className='mb-3 mt-0',
                    )
                ],
                width=4,
                className='offset-md-1'
            ),
            dbc.Col(
                children=[
                    dcc.Dropdown(
                        id='race-dropdown',
                        options=track_options,
                        value='Kansas Speedway',
                        clearable=False,
                        className='mb-5 mt-0',
                    )
                ],
                width=4,
                className='offset-md-2'
            )
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    dash_table.DataTable(
                        id='datatable-interactivity',
                        columns=[{"name": i, "id": i, "deletable": False} for i in displayed_df.columns if i not in ['Driver Full Name', 'Race ID','Track Name','Wins','Top 5s','Top 10s','DNFs']], 
                        data=displayed_df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current=0,
                        page_size=20,
                        style_cell={'textAlign': 'center','backgroundColor': 'white','color': '#000','padding': '10px','border': '1px solid black',},
                        style_header={'backgroundColor': 'black','fontWeight': 'bold','color': 'white','textAlign': 'center'},
                        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'lightgrey',},{'if': {'row_index': 'even'},'backgroundColor': 'white'}],
                        style_table={'height': '250px','margin-left':'45px'}
                    ),
                ],
                width=5,
                className='offset-md-0'
            ),
            dbc.Col(
                children=[
                    dcc.Graph(
                        id='fill-chart',
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '250px',
                            'margin-top':'-45px',
                            'margin-left':'35px',}
                    ),
                ],
                width=5,
                className='offset-md-1'
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.P('Starts',className='fs-5 text-center mb-0 mt-4')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('Wins',className='fs-5 text-center mb-0 mt-4')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('Top 5s',className='fs-5 text-center mb-0 mt-4')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('Top 10s',className='fs-5 text-center mb-0 mt-4')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('DNFs',className='fs-5 text-center mb-0 mt-4')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('Points Per Race',className='fs-5 text-center mb-0 mt-3')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.P('NOTE: Hovering over points on the area chart above highlight what season and race is associated with each point.',className='fs-5 text-center mb-0 mt-3 mx-2')
                ]
            )
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.Div(id='starts', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.Div(id='wins', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.Div(id='top-5s', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.Div(id='top-10s', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.Div(id='dnfs', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
            dbc.Col(
                children=[
                    html.Div(id='average-points', className='fs-5 text-center mt-1')
                ],
                width=1
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.P('Average Three Track Finish',className='fs-5 text-center mb-0 mt-3')
                ],
                width=3
            ),
            dbc.Col(
                children=[
                    html.P('Three Track Points Average',className='fs-5 text-center mb-0 mt-3')
                ],
                width=3
            ),
            dbc.Col(
                children=[
                    html.P('Slope',className='fs-5 text-center mb-0 mt-1')
                ],
                width=3
            ),
            dbc.Col(
                children=[
                    html.P('Intercept Point',className='fs-5 text-center mb-0 mt-1')
                ],
                width=3
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=[
                    html.Div(id='average-finish',className='fs-5 text-center mt-2')
                ],
                width=3
            ),
            dbc.Col(
                children=[
                    html.Div(id='average-points-per-driver',className='fs-5 text-center mt-2')
                ],
                width=3
            ),
            dbc.Col(
                    children=
                        [html.Div
                            (id='coefficient',
                            className='fs-5 text-center mt-1')
                        ],
                    width=3,
                ),
            dbc.Col(
                    children=[
                        html.Div
                            (id='intercept',
                            className='fs-5 text-center mt-1')
                            ],
                    width=3
                )
        ])        
    ]
)

@callback(
    Output('datatable-interactivity','data'),
    Output('fill-chart','figure'),
    Output('starts','children'),
    Output('wins','children'),
    Output('top-5s','children'),
    Output('top-10s','children'),
    Output('dnfs','children'),
    Output('average-points', 'children'),
    Output('average-finish','children'),
    Output('average-points-per-driver','children'),
    Output('coefficient','children'),
    Output('intercept','children'),
    Input('driver-dropdown','value'),
    Input('race-dropdown','value')
)

def results(selected_driver,selected_track):
    filtered_df = displayed_df[(displayed_df['Driver Full Name'] == selected_driver) &
                               (displayed_df['Track Name'] == selected_track)]
    filtered_df1 = displayed_df[(displayed_df['Driver Full Name'] == selected_driver)]

    filtered_df['Season and Race'] = filtered_df['Season'].astype(str) + ' ' + filtered_df['Race'].astype(str)

    X = filtered_df[['Race ID']]
    y = filtered_df['Points']
    
    if not filtered_df.empty:
        model = LinearRegression()
        model.fit(X, y)
        coefficient = model.coef_[0]
        intercept = model.intercept_
    else:
        coefficient = 0
        intercept = 0

    total_starts = len(filtered_df)
    total_wins = filtered_df['Wins'].sum()
    total_top_5s = filtered_df['Top 5s'].sum()
    total_top_10s = filtered_df['Top 10s'].sum()
    total_dnfs = filtered_df['DNFs'].sum()
    total_points = filtered_df['Points'].sum()
    average_points = total_points / total_starts if total_starts > 0 else 0

    average_points_text = f'{average_points:.1f}'

    average_finish = filtered_df1['Finish'].sum() / len(filtered_df1)
    average_finish_text = f'{average_finish:.1f}'

    average_points_per_track = filtered_df1.groupby('Track Name')['Points'].mean()
    average_points_per_driver = average_points_per_track.sum()
    average_points_per_driver_text = f'{average_points_per_driver:.1f}'

    fill_chart_fig = px.area(
        filtered_df,
        x='Race ID',
        y='Points',
        color='Driver Full Name',
        hover_data={
            'Season and Race': True,
            'Points': True,
            'Race ID': False
        },
        color_discrete_map={
            "Alex Bowman":'#50104a',
            "Austin Cindric":'black',
            "Chase Briscoe":'#720000',
            "Chase Elliott":'#001489',
            "Kyle Larson":'#023ca6',
            "Christopher Bell":'#febd17',
            "Daniel Suárez":'#ff7f00',
            "Denny Hamlin":'#4d148c',
            "Joey Logano":'#ffd500',
            "Ryan Blaney":'#FEEF01',
            "Tyler Reddick":'#95d600',
            "William Byron":'#002d62',
        },
    )

    fill_chart_fig.update_xaxes(
        title_font={
            'size': 14,
            'color': 'black'
            },
            tickfont=dict(
                size=12,
                color='black'
            ),
            showline=True,
            linewidth=1,
            linecolor='black',
        )

    fill_chart_fig.update_yaxes(
        title_font={
            'size': 14,
            'color': 'black'
            },
            tickfont=dict(
                size=12,
                color='black'
            ),
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=True,
            gridwidth=1,
            gridcolor='black',
        )

    fill_chart_fig.update_layout(
        margin=dict(l=20, r=20, b=20),
        height=320,
        width=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    return filtered_df.to_dict('records'), fill_chart_fig, total_starts, total_wins, total_top_5s, total_top_10s, total_dnfs, average_points_text, average_finish_text, average_points_per_driver_text, f'{coefficient:.2f}',f'{intercept:.2f}'

if __name__ == '__main__':
    app.run_server(debug=True)
