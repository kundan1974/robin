import datetime
import dash_bootstrap_components.themes
from dash import dcc, html
from django_plotly_dash import DjangoDash
from dash import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from ...models import Simulation, SimStatus
from django.utils import timezone
from .simulation_flow import get_df

now = timezone.now()
sim_choices = SimStatus.objects.all()
choices = []
for choice in sim_choices:
    choices.append(choice.status)

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
}
content = html.Div(id="page-content",
                   children=["Initial"],
                   style=CONTENT_STYLE)
display_content = html.Div(id='click-data',
                           children=[html.Label("Click on Patient Bar and choose new status from Dropdown Menu",
                                                id="status-lbl", style={'font-weight': 'bold'}),
                                     dcc.Dropdown(options=choices, id='drop1',
                                                  style={'width': '550px'}),
                                     dbc.Button("Submit", id='btn-submit-status', n_clicks=0, className='mt-2',
                                                color='primary')],
                           style=CONTENT_STYLE)
def fig01(records_df):
    diff = datetime.timedelta(14)
    mydatesHigh = now + diff
    mydatesHigh = pd.to_datetime(mydatesHigh)
    # mydatesHigh = datetime.datetime.combine(mydatesHigh, datetime.datetime.min.time())
    compdate = now - datetime.timedelta(3)
    compdate = pd.to_datetime(compdate)
    try:
        datedata = pd.to_datetime(records_df['Implementation Date'])
        newdf = records_df[
            (datedata >= compdate) &
            (datedata < mydatesHigh)]
        colors = {}
        for j in newdf['Status']:
            if j == 'Simulation':
                colors[j] = 'black'
            elif j[0:4] == 'Plan':
                colors[j] = '#FF0000'
            elif j[0:4] == 'Star':
                colors[j] = 'green'
            elif j[0:5] == 'Ready':
                colors[j] = 'pink'
            elif j == "PhotonBoost Planning Due":
                colors[j] = 'black'
            elif j[0:4] == "Comp":
                colors[j] = 'cyan'
            elif (j == "Cancelled/Defaulted") | (j == "On Hold"):
                colors[j] = 'grey'
            else:
                colors[j] = 'orange'
        fig = px.bar(data_frame=newdf, y='Implementation Date', height=600, width=1000,
                     color='Status',
                     color_discrete_map=colors,
                     orientation='h',
                     hover_data={'simID': True, 'CRN': True, 'Intent': True, 'Technique': True,
                                 'RT Volumes': True, 'Planned Fractions': True, 'Assigned to': True,
                                 'Status': True},
                     hover_name=newdf['Name'],
                     labels={'count': 'n'})
        fig.update_layout(clickmode='event+select')
        fig.update_xaxes(title="Patients", dtick=1)
        fig.update_yaxes(title="Dates", dtick="D")
        fig.update_layout(barmode='stack', hovermode='closest', plot_bgcolor="white",
                          paper_bgcolor='white')
    except:
        fig = px.bar()
    return fig

external_stylesheets = [dash_bootstrap_components.themes.BOOTSTRAP]
app = DjangoDash('simulation_flow_zoom', external_stylesheets=external_stylesheets)
# fig = fig01(get_df())
app.layout = html.Div([
    dcc.Store(id='intermediate-value'),
    html.Div(
        [html.H4('Radiotherapy Planning Status'),
         dbc.Button('Refresh', id='refresh-page', color='primary')], style={'padding': '1rem'}
    ),
    display_content,
    # html.Div(get_df().to_json(orient='values')),
    dcc.Graph(id='bar-graph1', style={'padding': '0rem'}),
])


@app.callback(
    Output('bar-graph1', 'figure'),
    [Input('refresh-page', 'n_clicks'),
     Input('intermediate-value', 'data')]
)
def refresh_button_clicked(n_clicks, jsonified_data):
    if jsonified_data:
        new_df = pd.read_json(jsonified_data, orient='split')
        new_df["SimDate"] = new_df["SimDate"].astype('datetime64[ns]')
        # new_df["Implementation Date"] = new_df["Implementation Date"].astype('datetime64[ns]')
        new_df["Implementation Date"] = new_df["Implementation Date"]
        new_df["Assessment Date"] = new_df["Assessment Date"].astype('datetime64[ns]')
        new_df["Phase2 Imp Date"] = new_df["Phase2 Imp Date"].astype('datetime64[ns]')
        new_df["Completion Date"] = new_df["Completion Date"].astype('datetime64[ns]')
        new_df["Tentative Completion Date"] = new_df["Tentative Completion Date"].astype('datetime64[ns]')
        new_df["ActualCompletionDate"] = new_df["ActualCompletionDate"].astype('datetime64[ns]')
        fig = fig01(new_df)
    else:
        fig = fig01(get_df())
    return fig


@app.callback(
    Output('intermediate-value', 'data'),
    Output('status-lbl', 'children'),
    Input('btn-submit-status', 'n_clicks'),
    State('drop1', 'value'),
    State('bar-graph1', 'clickData'), prevent_initial_call=True
)
def click_fig1(n, choice_value, clickData):
    # changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    new_df = get_df()
    new_value = "Click on Patient Bar and choose new status from Dropdown Menu"
    # if n and ('btn-submit-status' in changed_id):
    if n:
        if clickData:
            simid = clickData['points'][0]['customdata'][0]
            status = clickData['points'][0]['customdata'][-1]
            patient = Simulation.objects.get(pk=simid)
            patient.initialstatus_id = choice_value
            patient.save()
            new_df.loc[new_df["simID"] == simid, "Status"] = choice_value
            new_value = f"You have Changed status to -->  {choice_value} for CRNumber: {patient.simparent_id}"
    # return json.dumps(clickData, indent=2), new_df.to_json(date_format='iso', orient='split')
    return new_df.to_json(date_format='iso', orient='split'), new_value

