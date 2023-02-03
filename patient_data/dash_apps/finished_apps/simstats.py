from dash import dcc, html
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from ...models import (Simulation, S2Diagnosis, S4RT,
                       S7Assessment, User, S1ParentMain,
                       PrimaryDVH)
import datetime

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def fig_rt_tech():
    pat_reg = S1ParentMain.objects.all().values()
    df = pd.DataFrame(pat_reg)
    pat_dx = S2Diagnosis.objects.all().values()
    df_dx = pd.DataFrame(pat_dx)
    pat_rt = S4RT.objects.all().values()
    df_rt = pd.DataFrame(pat_rt)
    pat_dvh = PrimaryDVH.objects.all().values()
    df_dvh = pd.DataFrame(pat_dvh)
    pat_as = S7Assessment.objects.all().values()
    df_as = pd.DataFrame(pat_as)

    df.rename(columns={'crnumber': 'parent_id_id'}, inplace=True)
    # df_dvh.rename(columns={'dvhParent_ID': 'Parent_ID'}, inplace=True)
    # We are using the suffix = _remove for duplicate columns
    final_df = pd.merge(df, df_dx, how='inner', on=['parent_id_id'], suffixes=('', '_remove'))
    final_df = pd.merge(final_df, df_rt, how='inner', on=['parent_id_id'], suffixes=('', '_remove'))
    # final_dvh = pd.merge(final_df, df_dvh, how='inner', on=['Parent_ID'], suffixes=('', '_remove'))
    # final_dvh = pd.merge(final_dvh, df_as, how='inner', on=['Parent_ID'], suffixes=('', '_remove'))
    # # Now dropping the columns name with _remove as suffix
    final_df.drop([i for i in final_df.columns if 'remove' in i],
                  axis=1, inplace=True)
    # final_dvh.drop([i for i in final_dvh.columns if 'remove' in i],
    #                axis=1, inplace=True)
    #
    # final_dvh = final_dvh[final_dvh.HeartAvg.notna()]
    # final_dvh = final_dvh[final_dvh.ptv1PD.notna()]
    # final_dvh = final_dvh[final_dvh.body105.notna()]
    # final_dvh = final_dvh[final_dvh.ptv1_V105.notna()]
    # final_dvh = final_dvh[final_dvh.Dermatitis.notna()]
    # final_dvh = final_dvh[final_dvh.ptv1_Avg.notna()]
    # final_dvh = final_dvh[final_dvh.ptv1Vol.notna()]

    col = ['s1_id', 'parent_id_id', 'first_name', 'last_name', 'age', 'weight',
           'height', 'reg_date', 'gender', 'ecog', 'doc_type', 'doc_id', 'city_id',
           'smoking', 'smoking_status', 'smoking_volume', 'email', 'mobile',
           'notes', 'user_id', 'updated_by', 'last_updated', 's2_id',
           'diagnosis_id', 'laterality', 'dx_type_id', 'icd_main_topo_id',
           'icd_topo_code_id', 'icd_path_code_id', 'dx_date', 'biopsy_no',
           'biopsy', 'biopsy_date', 'biopsy_grade_id', 'confirmed_by', 'c_t_id',
           'c_n_id', 'c_m_id', 'c_stage_group_id', 'c_ajcc_edition_id', 'er', 'pr',
           'her2neu', 'braca1', 'braca2', 'egfr', 'alk', 'ros', 'pdl_1',
           'pdl_1_levels', 'braf', 'met', 'ret', 'hpv', 's4_id', 's2_id_id',
           's3_id_id', 'simid_id', 'rtindication_id', 'simdate', 'rtsitecode_id',
           'rtdose1', 'rtdosefr1', 'modality1', 'tech1_id', 'rtdose2', 'rtdosefr2',
           'modality2', 'tech2_id', 'rtdose3', 'rtdosefr3', 'modality3',
           'tech3_id', 'rtdose4', 'rtdosefr4', 'modality4', 'tech4_id',
           'rtstartdate', 'rtfinishdate', 'rtmachine_id', 'rtstatus_id',
           'institution', 'user_id_id']
    final_df = final_df[
        ["parent_id_id", "first_name", "reg_date", "diagnosis_id", "icd_topo_code_id", "icd_path_code_id",
         "tech1_id", "rtstartdate", "rtmachine_id"]]

    # final_dvh = final_dvh[["Parent_ID", "Dx_ID", "Laterality", "ICDTopo", "Tech1", "RTStartDate",
    #                        "RTmachine", "Dermatitis", "As_Date", "ptv1_Avg", "ptv1_V105", "ptv1Vol",
    #                        "body105"]]
    # final_dvh["RTStartDate"] = final_dvh["RTStartDate"].dt.date
    # final_dvh["As_Date"] = final_dvh["As_Date"].dt.date
    # # final_dvh = final_dvh[final_dvh.Dermatitis == "Grade 3"]

    #
    final_df["reg_date"] = final_df["reg_date"].dt.date
    final_df["rtstartdate"] = final_df["rtstartdate"].dt.date
    final_df.rename(columns={'tech1_id': 'Technique', 'rtstartdate': 'Year'}, inplace=True)
    final_df = final_df[final_df.Year > datetime.date(2017, 8, 1)]
    final_df.loc[final_df["Technique"].isin(["SBRT", "SRS"]), "Technique"] = 'SRS/SRT'
    final_df.loc[final_df["Technique"].isin(["FIFIMRT", "DIBH_FIFIMRT"]), "Technique"] = 'DIBH_IMRT'
    final_df.loc[final_df["Technique"].isin(["ILRT", "ICRT", "IIRT"]), "Technique"] = 'Brachytherapy'
    final_df["Technique"].fillna('Unknown', inplace=True)
    final_df.loc[final_df["Technique"] == "", "Technique"] = 'Unknown'

    final_df.loc[final_df["icd_topo_code_id"].isin([24, 29, 47, 60, 82, 86, 92, 98, 132, 148, 152,
                                                    174, 329, 335, 338, 518, 534, 546, 550, 633, 730,
                                                    1022, 1040, 1194, 1195, 1197, 1198,
                                                    1257]), "icd_topo_code_id"] = 'HeadNeck'

    final_df.loc[final_df["icd_topo_code_id"].isin([375, 376]), "icd_topo_code_id"] = 'Thymus'
    final_df.loc[final_df["icd_topo_code_id"].isin([211, 238, 239, 250, 261, 387, 479, 482, 485, 487,
                                               488, 490, 498, 503, 572, 599, 608, 637, 659, 680,
                                               709, 779, 806, 809, 828, 873, 889, 894, 909, 910,
                                               911, 915, 923, 924, 926, 927, 939, 966, 989, 990,
                                               1011, 1013, 1150, 1169, 1205, 1207, 1221, 1222,
                                               1225, 1226, 1227, 1229, 1232, 1233, 1235, 1237,
                                               1238, 1239, 1242, 1315, 1317, 1339, 1340,
                                               1341]), "icd_topo_code_id"] = 'Others'

    final_df.loc[final_df["icd_topo_code_id"].isin([467, 473, 475, 702]), "icd_topo_code_id"] = 'Spine'
    final_df.loc[final_df["icd_topo_code_id"].isin([553, 1070, 1073, 1094, 1105, 1112, 1116, 1118,
                                               1119, 1127, 1154]), "icd_topo_code_id"] = 'Brain, NOS'
    final_df.loc[final_df["icd_topo_code_id"].isin([177, 178, 179, 180, 181, 182, 183, 184, 185,
                                               186, 187]), "icd_topo_code_id"] = 'Esophagus, NOS'
    final_df.loc[final_df["icd_topo_code_id"].isin([564, 1206, 1201, 388, 371, 571, 673, 797,
                                               1203, 356, 357, 790, 372, ]), "icd_topo_code_id"] = 'Thorax'
    final_df.loc[final_df["icd_topo_code_id"].isin([425, 484, 490, 398, 409, 571, 673, 797,
                                               1203, 356, 357, 790, 372]), "icd_topo_code_id"] = 'Bone, NOS'
    final_df.loc[final_df["icd_topo_code_id"].isin([864, 871, 581, 855, 858, 859, 860, 861, 862, 863, 864,
                                               865, 866, 867, 868, 869, 870, 871]), "icd_topo_code_id"] = 'Breast, NOS'

    count = final_df['Technique'].value_counts()
    y = count.values
    x = count.index.values

    fig1 = px.histogram(final_df, x='Year', y='parent_id_id', histfunc='count', color='Technique')
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False)
    fig1.update_layout(height=400, margin={'l': 0, 'b': 10, 'r': 10, 't': 10})
    fig1.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig2 = px.bar(y=y, x=x, labels={'x': 'Technique', 'y': 'Numbers', 'color': 'Technique'}, color=count.index.values)
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(height=400, margin={'l': 0, 'b': 10, 'r': 10, 't': 10})
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig3 = px.histogram(final_df, x='Year', y='parent_id_id', histfunc='count', color='icd_topo_code_id')
    fig3.update_xaxes(showgrid=False)
    fig3.update_yaxes(showgrid=False)
    fig3.update_layout(height=400, margin={'l': 0, 'b': 10, 'r': 10, 't': 10})
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig1, fig2, fig3


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = DjangoDash('simstats', external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(
        [html.H4('Simulation Distribution - Technique', className='me-2'),
         dbc.Button('Refresh', id='refresh1', color='primary'),
         dcc.Graph(id='bar-graph3', style={'padding': '0rem'})], style={'padding': '1rem'}
    ),
    html.Div(
        [html.H4('Technique Used ', className='me-2'),
         dbc.Button('Refresh', id='refresh2', color='primary'),
         dcc.Graph(id='bar-graph4', style={'padding': '0rem'})], style={'padding': '1rem'}
    ),
    html.Div(
        [html.H4('Site  Distribution ', className='me-2'),
         dbc.Button('Refresh', id='refresh3', color='primary'),
         dcc.Graph(id='bar-graph5', style={'padding': '0rem'})], style={'padding': '1rem'}
    ),
], style={'background-color': "#fac4c4"})


@app.callback(
    Output('bar-graph3', 'figure'),
    Output('bar-graph4', 'figure'),
    Output('bar-graph5', 'figure'),
    [Input('refresh1', 'n_clicks'),
     Input('refresh2', 'n_clicks'),
     Input('refresh3', 'n_clicks')]
)
def creatfig1(n1, n2, n3):
    if n1:
        fignew1, fignew2, fignew3 = fig_rt_tech()
        return fignew1, fignew2, fignew3
    if n2:
        fignew1, fignew2, fignew3 = fig_rt_tech()
        return fignew1, fignew2, fignew3
    if n3:
        fignew1, fignew2, fignew3 = fig_rt_tech()
        return fignew1, fignew2, fignew3
    fignew1, fignew2, fignew3 = fig_rt_tech()
    return fignew1, fignew2, fignew3

# @app.callback(
#     Output('bar-graph4', 'figure'),
#     Input('refresh-page1', 'n_clicks')
# )
# def creatfig2(n):
#     if n:
#         fignew1, fignew2, fignew3 = fig_rt_tech()
#         return fignew1, fignew2, fignew3
#     fignew1, fignew2, fignew3 = fig_rt_tech()
#     return fignew2
