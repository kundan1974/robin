from dash import dcc, html
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash import Input, Output, State
import dash_bootstrap_components as dbc
from .simulation_flow import get_df

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def fig02(records_df):
    try:
        mask = records_df['Status'].str.contains('Started', case=False, na=False)
        new_df = records_df[mask]
        new_df.sort_values(by='Done Fractions', inplace=True, ascending=False)
        patient_no = len(new_df)
        fig = px.bar(new_df, y='Name', x=['Done Fractions', 'Phase1 Fractions', 'Planned Fractions'], height=800,
                     width=1000,
                     barmode='overlay', orientation='h',
                     title=f'RT Status of Patients: Total {patient_no}',
                     hover_name='Name', hover_data={'CRN': True, "Status": True, 'Implementation Date': True,
                                                    "Assessment Date": True, "Completion Date": True},
                     labels={'value': 'No of fractions', 'variable': 'Status',
                             'TentativeCompletionDate': 'Completion Date',
                             'CRN': 'CRNumber'},
                     color_discrete_sequence=['blue', 'orange', 'black'])
        fig.update_xaxes(dtick=4)
    except:
        fig = px.bar()
    return fig


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = DjangoDash('rt_status_zoom', external_stylesheets=external_stylesheets)
# fig = fig01(get_df())
app.layout = html.Div([
    html.Div(
        [html.H4('On Treatment Radiotherapy Status ', className='me-2'),
         dbc.Button('Refresh', id='refresh-page1', color='primary')], style={'padding': '1rem'}
    ),
    # html.Div(get_df().to_json(orient='values')),
    dcc.Graph(id='bar-graph2', style={'padding': '0rem'}),
])


@app.callback(
    Output('bar-graph2', 'figure'),
    Input('refresh-page1', 'n_clicks')
)
def creatfig2(n):
    if n:
        newdf = get_df()
        fignew = fig02(newdf)
        return fignew
    newdf = get_df()
    fignew = fig02(newdf)
    return fignew
