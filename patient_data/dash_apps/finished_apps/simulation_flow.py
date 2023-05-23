from importlib.resources import path
import dash_bootstrap_components.themes
import numpy
from dash import dcc, html
from django_plotly_dash import DjangoDash
from pkg_resources import to_filename
import plotly.express as px
import datetime
from dash import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from pandas.tseries.offsets import BDay
from ...models import User, Simulation, SimStatus
from django.utils import timezone
from log2d import Log

log_datetime = Log('simflow_getdb', to_file=True, path='./logs')

now = timezone.now()
Log.simflow_getdb.info(f"Todays Date: {now}")


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

def fig01(records_df):
    diff = datetime.timedelta(14)
    mydatesHigh = now + diff
    mydatesHigh = pd.to_datetime(mydatesHigh)
    # mydatesHigh = datetime.datetime.combine(mydatesHigh, datetime.datetime.min.time())
    compdate = now - datetime.timedelta(3)
    compdate = pd.to_datetime(compdate)
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
    fig = px.bar(data_frame=newdf, y='Implementation Date', height=400, width=600,
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

    return fig

    # def get_df():
    #     diff = datetime.timedelta(60)
    #     date4filter = datetime.date.today() - diff
    #     # temp_data1 = Simulation.objects.filter(simdate__gte=date4filter)
    #     # data = serializers.serialize('json', temp_data1)
    #     data = Simulation.objects.all().values()
    #     df = pandas.DataFrame(data)
    #
    #     return df


# temp_data1 = Simulation.objects.all().values()
# temp_data2 = S7Assessment.objects.all().values()

def get_df():
    records_df1 = pd.DataFrame(Simulation.objects.all().values())  # Simulation table dataframe
    # records_df2 = pd.DataFrame(temp_data2)  # Assessment table table dataframe
    # TODO create options for second phase
    # Creating a new dataframe by adding each row for other phases of rt plans
    data_list = []
    users1 = User.objects.all().values()
    users = {}
    for u in users1:
        users[u.get('id')] = u.get('username')
    # users = {
    #     1: "Dr Kundan S Chufal",
    #     4: "Dr Irfan Ahmad",
    #     5: "Arti Shukla",
    #     6: "Dr Rahul",
    #     7: "Dr Ismail",
    #     10: "Preetha"
    # }
    for row in records_df1.itertuples(index=False):
        assignedto = users.get(row.assignedto_id)
        if not assignedto:
            assignedto = "Not Assigned"
        if pd.isna(row.totalfractions):
            PlannedFractions = "Data Not avialable"
        else:
            PlannedFractions = row.totalfractions


        if pd.isna(row.donefr):
            remaining_fr_total = row.totalfractions
            remaining_fr_ph1 = row.fxphase1
        else:
            remaining_fr_total = row.totalfractions - row.donefr
            remaining_fr_ph1 = row.fxphase1 - row.donefr

        if now == row.impdate:
            Log.simflow_getdb.info(f"Imp Date: {row.impdate}")
            if pd.isna(row.fxphase2) or row.fxphase2 == 0:
                ph2_imp_impdate = None
            else:
                ph2_imp_impdate = datetime.datetime.today() + BDay((remaining_fr_ph1 + 1))
            if pd.isna(row.fxphase3) or row.fxphase3 == 0:
                ph3_imp_impdate = ph2_imp_impdate + BDay((row.fxphase3 + 1))
            else:
                ph3_imp_impdate = None
            dynamic_completion_date = datetime.datetime.today() + BDay(remaining_fr_total)
        elif now > row.impdate:
            try:
                dynamic_completion_date = row.as_date + BDay(remaining_fr_total)
            except TypeError:
                dynamic_completion_date = None
            if pd.isna(row.fxphase2) or row.fxphase2 == 0:
                ph2_imp_impdate = None
            else:
                if row.as_date:
                    ph2_imp_impdate = row.as_date + BDay(remaining_fr_ph1 + 1)
                else:
                    ph2_imp_impdate = row.impdate + BDay(remaining_fr_ph1 + 1)
            if pd.isna(row.fxphase3) or row.fxphase3 == 0:
                ph3_imp_impdate = None
            else:
                ph3_imp_impdate = ph2_imp_impdate + BDay((row.fxphase3 + 1))
        else:
            ph2_imp_impdate = None
            ph3_imp_impdate = None
            dynamic_completion_date = None
        data_dict = {"simID": row.simid,
                     "CRN": row.simparent_id,
                     "Name": row.name,
                     "SimDate": row.simdate,
                     "Implementation Date": row.impdate, "Status": row.initialstatus_id,
                     "RT Volumes": row.volumes_id,
                     "Intent": row.intent_id,
                     "Technique": row.technique_id,
                     "Assigned to": assignedto,
                     "Phase1 Dose": row.dosephase1,
                     "Phase1 Fractions": row.fxphase1,
                     "Phase2 Dose": row.dosephase2,
                     "Phase2 Fractions": row.fxphase2,
                     "Phase3 Dose": row.dosephase3,
                     "Phase3 Fractions": row.fxphase3,
                     "Total Dose": row.totaldose,
                     "Planned Fractions": PlannedFractions,
                     "Done Fractions": row.donefr,
                     "Assessment Date": row.as_date,
                     "Total Fractions Remaining": remaining_fr_total,
                     "Phase1 Fractions Remaining": remaining_fr_ph1,
                     "Phase2 Imp Date": ph2_imp_impdate,
                     "Completion Date": dynamic_completion_date,
                     "Tentative Completion Date": row.tentativecompletiondate,
                     "ActualCompletionDate": row.actualcompletiondate,
                     "Phase 3 Imp Date": ph3_imp_impdate}
        data_list.append(data_dict)
    # Creating a new dataframe with boost phase as a separate row
    new_df = pd.DataFrame(data_list)
    try:
        df = new_df[new_df["Phase2 Imp Date"].notna()]
        phase2impdate = df["Phase2 Imp Date"].to_list()
        df.loc[:, "Implementation Date"] = phase2impdate
        df.loc[:, "Status"] = "Boost"
        df.loc[:, "RT Volumes"] = "Boost Volume"
        df.loc[:, "Planned Fractions"] = df["Phase2 Fractions"]
        new_df = new_df.append(df)
    except:
        pass
    return new_df


external_stylesheets = [dash_bootstrap_components.themes.BOOTSTRAP]
app = DjangoDash('simulation_flow', external_stylesheets=external_stylesheets)
# fig = fig01(get_df())
app.layout = html.Div([
    html.Div(
        [html.H4('Radiotherapy Planning Status'),
         dbc.Button('Refresh', id='refresh-page', color='primary')], style={'padding': '1rem'}
    ),
    # html.Div(get_df().to_json(orient='values')),
    dcc.Graph(id='bar-graph1', style={'padding': '0rem'}),
])


@app.callback(
    Output('bar-graph1', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def refresh_button_clicked(n_clicks):
    if n_clicks:
        fig = fig01(get_df())
    else:
        fig = fig01(get_df())
    return fig


# @app.callback(
#     Output('intermediate-value', 'data'),
#     Output('status-lbl', 'children'),
#     Input('btn-submit-status', 'n_clicks'),
#     State('drop1', 'value'),
#     State('bar-graph1', 'clickData'), prevent_initial_call=True
# )
# def click_fig1(n, choice_value, clickData):
#     # changed_id = [p['prop_id'] for p in callback_context.triggered][0]
#     new_df = get_df()
#     new_value = "Click on Patient Bar and choose new status from Dropdown Menu"
#     # if n and ('btn-submit-status' in changed_id):
#     if n:
#         if clickData:
#             simid = clickData['points'][0]['customdata'][0]
#             status = clickData['points'][0]['customdata'][-1]
#             patient = Simulation.objects.get(pk=simid)
#             patient.initialstatus_id = choice_value
#             patient.save()
#             new_df.loc[new_df["simID"] == simid, "Status"] = choice_value
#             new_value = f"You have Changed status to -->  {choice_value} for CRNumber: {patient.simparent_id}"
#     # return json.dumps(clickData, indent=2), new_df.to_json(date_format='iso', orient='split')
#     return new_df.to_json(date_format='iso', orient='split'), new_value

# @app.callback(
#     Output('head', 'children'),
#     Input('bar-graph1', 'clickData')
# )
# def test(clickData):
#     if clickData:
#         simid = clickData['points'][0]['customdata'][0]
#         status = clickData['points'][0]['customdata'][-1]
#         patient = Simulation.objects.get(pk=simid)
#         patient.InitialStatus = choice_value
#         return patient
#     return "Not Clicked"
