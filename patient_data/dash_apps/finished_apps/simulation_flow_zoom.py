import datetime
import json
import dash
from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components.themes
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from ...models import Simulation, SimStatus
from django.utils import timezone
from .simulation_flow import get_df
from django.conf import settings

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
                                                id="status-lbl1", style={'font-weight': 'bold'}),
                                     html.Label("", id="status-lbl2", style={'font-weight': 'bold'}),
                                     html.Br(),
                                     html.A("", id="gotodb", href='#', target="_blank"),
                                     html.Br(),
                                     html.A("", id="simupdate", href='#', target="_blank"),
                                     dcc.Dropdown(options=choices, id='drop1',
                                                  style={'width': '550px'}),
                                     dbc.Button("Submit", id='btn-submit-status', n_clicks=0, className='mt-2',
                                                color='primary'),
                                     dbc.Button("Database Entry", id='btn-submit-db', n_clicks=0, className='mt-2 ml-2',
                                                color='success'),
                                     html.Br(),
                                     html.Label("", id="status-lbl3", style={'font-weight': 'bold'}),
                                     ],

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
            if j is None:
                colors[j] = 'gray'
            elif j == 'Simulation':
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
    except ValueError:
        fig = px.bar()

    return fig


external_stylesheets = [dash_bootstrap_components.themes.BOOTSTRAP]
app = DjangoDash('simulation_flow_zoom', external_stylesheets=external_stylesheets)
# fig = fig01(get_df())
app.layout = html.Div([
    dcc.Store(id='intermediate-value'),
    dcc.Store(id='intermediate-value2'),
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
    Output('intermediate-value2', 'data'),
    [Input('refresh-page', 'n_clicks'),
     Input('intermediate-value', 'data')]
)
def refresh_button_clicked(n_clicks, jsonified_data):
    # ctx = dash.callback_context
    # if ctx.triggered:
        # triggred_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # print(f"Trigger on refresh: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {n_clicks}")
    refresh_data = {"new_value1": n_clicks}
    n_clicks = 0
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
    return fig, json.dumps(refresh_data)


@app.callback(
    Output('intermediate-value', 'data'),
    Output('status-lbl1', 'children'),
    Output('status-lbl2', 'children'),
    Output('status-lbl3', 'children'),
    Output('gotodb', 'href'),
    Output('gotodb', 'children'),
    Output('simupdate', 'children'),
    Output('simupdate', 'href'),
    Output('refresh-page', 'n_clicks'),
    Input('btn-submit-status', 'n_clicks'),
    Input('btn-submit-db', 'n_clicks'),
    Input('intermediate-value2', 'data'),
    State('drop1', 'value'),
    State('bar-graph1', 'clickData'), prevent_initial_call=True
)
def click_fig1(n, n2, refresh_data, choice_value, clickData):
    # changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # refresh_data = pd.read_json(refresh_data, orient='split')
    ctx = dash.callback_context
    triggred_id = ctx.triggered[0]['prop_id'].split('.')[0]
    refresh_data = json.loads(refresh_data)
    clicks = refresh_data["new_value1"]
    # print(f"Trigger on main: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")

    new_df = get_df()
    new_value1 = "Click on Patient Bar and choose new status from Dropdown Menu"
    new_value2 = ""
    new_value3 = ""
    href = "#"
    custom_text = ""
    href_simupdate = ""
    text_simupdate = ""
    # if n and ('btn-submit-status' in changed_id):
    if triggred_id == "btn-submit-status":
        if clickData:
            simid = clickData['points'][0]['customdata'][0]
            status = clickData['points'][0]['customdata'][-1]
            crn = clickData['points'][0]['customdata'][1]
            # print(f"Trigger on submit1: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
            if choice_value:
                patient = Simulation.objects.get(pk=simid)
                patient.initialstatus_id = choice_value
                patient.save()
                new_df.loc[new_df["simID"] == simid, "Status"] = choice_value
                new_value1 = f"You have Changed status to -->  {choice_value} for: {patient.name} ({patient.simparent_id})"
                choice_value = False
                # print(f"Trigger on submit2: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
    if triggred_id == "btn-submit-db":
        # print(f"Trigger on DB1: {ctx.triggered[0]} and click: {clicks}")
        if clickData:
            simid = clickData['points'][0]['customdata'][0]
            patient = Simulation.objects.get(pk=simid)
            crn = clickData['points'][0]['customdata'][1]
            new_value3 = f"You have selected patient -- {patient.name} ({crn})"
            new_value1 = "Click on Patient Bar and choose new status from Dropdown Menu"
            base = settings.CUSTOM_HOST
            href = base + f'patient_data/db_operations/{crn}/'
            custom_text = f"Click here to go to database entry for {patient.name} ({crn})"
            href_simupdate = base + f'patient_data/radonc-simulation/{simid}/update/?next=/patient_data/radonc-simulation/{crn}/list/'
            text_simupdate = f"Click here to update simulation details for {patient.name} ({crn}"
            clicks = 0
            # print(f"Trigger on DB2: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
    if clicks:
        # print(f"Trigger on if Clicks: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
        if clicks > 0:
            new_value1 = "Click on Patient Bar and choose new status from Dropdown Menu"
            href = "#"
            custom_text = ""
            href_simupdate = ""
            text_simupdate = ""
            clicks = 0
            # print(f"Trigger on if Clicks > 0: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
    # print(f"Trigger before function returns: {ctx.triggered[0]['prop_id'].split('.')[0]} and click: {clicks}")
    return new_df.to_json(date_format='iso',
                          orient='split'), new_value1, new_value2, new_value3, href, custom_text, text_simupdate, href_simupdate, clicks
