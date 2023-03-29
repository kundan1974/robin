from .dash_utils import check_data
from .simulation_flow import get_df
from django_plotly_dash import DjangoDash
from dash import html, Input, Output
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = DjangoDash('check_data', external_stylesheets=external_stylesheets)
newdf = get_df()
check_table = check_data(newdf)
app.layout = html.Div([
    html.Div(
        [html.H1('Check List - Issues in Data Entry ', className='me-2'),
         dbc.Button('Refresh', id='refresh-page2', color='primary')], style={'padding': '2rem'}
    ),
    html.Div(
        id='check_table', children=[check_table]
    )
], className='container')


@app.callback(
    Output('check_table', 'children'),
    Input('refresh-page2', 'n_clicks'), prevent_initial_call=True
)
def refresh_check(n):
    if n:
        df = get_df()
        table = check_data(df)
        return table
