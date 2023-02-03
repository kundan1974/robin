import datetime
import pandas as pd
from dash import html, dash_table
from django.utils import timezone


def check_data(df):
    try:
        df['SimDate'] = pd.to_datetime(df['SimDate'], format='%d/%m/%Y').dt.normalize()
        df['Implementation Date'] = pd.to_datetime(df['Implementation Date'], format='%d/%m/%Y').dt.normalize()
        df['Tentative Completion Date'] = pd.to_datetime(df['Tentative Completion Date'], format='%d/%m/%Y').dt.normalize()
        today = timezone.now()
        # today = datetime.datetime(today.year, today.month, today.day)
        check_df_compdate = df[(df['Tentative Completion Date'] < today) & (df.ActualCompletionDate.isna())]
        check_df_compdate = check_df_compdate[
            ['CRN', 'Name', 'Tentative Completion Date', 'Planned Fractions', 'Status', 'ActualCompletionDate']]
        with pd.option_context('mode.chained_assignment', None):
            check_df_compdate['Tentative Completion Date'] = check_df_compdate['Tentative Completion Date'].apply(
                lambda x: x.strftime('%d/%m/%Y'))
        check_df_update = df[(df['Implementation Date'] < today) & (df['Tentative Completion Date'] < today) &
                             ((df['Status'] == 'Simulation') | (df['Status'] == 'Planning'))]
        check_df_update = check_df_update[['CRN', 'Name', 'Status', 'Implementation Date', 'ActualCompletionDate']]
        with pd.option_context('mode.chained_assignment', None):
            check_df_update['Implementation Date'] = check_df_update['Implementation Date'].apply(
                lambda x: x.strftime('%d/%m/%Y'))

        check_df_issues = df[
            (df['ActualCompletionDate'] == '') | (df['ActualCompletionDate'] == 'D') | (df['ActualCompletionDate'] == 'C')]
        check_df_issues = check_df_issues[
            ['CRN', 'Name', 'Tentative Completion Date', 'Planned Fractions', 'Status', 'ActualCompletionDate']]
        with pd.option_context('mode.chained_assignment', None):
            check_df_issues['Tentative Completion Date'] = check_df_issues['Tentative Completion Date'].apply(
                lambda x: x.strftime('%d/%m/%Y'))

        table1 = dash_table.DataTable(
            id='table01',
            columns=[{"name": i, "id": i} for i in check_df_compdate.columns],
            data=check_df_compdate.to_dict('records'),
        )

        table2 = dash_table.DataTable(
            id='table02',
            columns=[{"name": i, "id": i} for i in check_df_update.columns],
            data=check_df_update.to_dict('records'),
        )

        table3 = dash_table.DataTable(
            id='table03',
            columns=[{"name": i, "id": i} for i in check_df_issues.columns],
            data=check_df_issues.to_dict('records'),
        )

        datacheck_layout = html.Div(
            [
                html.H4("Patient's having issues with updated Completion Date", className="display-5"),
                html.Hr(),
                html.Div(table1, id='check-comp-date'),
                html.Hr(),

                html.H4("Patient's having issues with status", className="display-6"),
                html.Hr(),
                html.Div(table2, id='check-update-status'),

                html.H4("Patient's with blank or invalid actual completion date", className="display-6"),
                html.Hr(),
                html.Div(table3, id='check-update-status'),
            ], className='ml-4 mr-2'
        )
    except:
        return html.Div("No Data to display")

    return html.Div(datacheck_layout)
