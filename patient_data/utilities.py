from patient_data.forms import S2DiagnosisForm
from patient_data.models import S1ParentMain, S3CarePlan, PreSimulation, Simulation, S2Diagnosis, S8FUP, S4RT, \
    S5ChemoProtocol, S6Surgery, TNM, BreastGroupTNM, StageGroup, EsoGroupTNM, NSCLCGroupTNM, LarynxGroupTNM, \
    OralGroupTNM
from django import forms
from django.db import connection
import re


def db_homestatus(crnumber=None):
    presim = False
    sim = False
    presimdetails = None
    dx = False
    mx = False
    rt = False
    pft = False
    cm = False
    res = False
    fu = False
    try:
        fu = S8FUP.objects.filter(parent_id=crnumber)
        if fu:
            fu = True
    except:
        fu = False
    try:
        res = S1ParentMain.objects.filter(crnumber=crnumber)
        if res:
            try:
                mx = S3CarePlan.objects.filter(parent_id=res[0].crnumber)

                if mx:
                    dx = True
                    try:
                        presim = PreSimulation.objects.filter(presimparent=res[0].crnumber)
                        if presim:
                            presimdetails = presim.first()
                            presim = True
                            try:
                                sim = Simulation.objects.filter(simparent=res[0].crnumber)
                                if sim:
                                    sim = True
                                else:
                                    sim = False
                            except:
                                sim = False
                        else:
                            presim = False
                            try:
                                sim = Simulation.objects.filter(simparent=res[0].crnumber)
                                if sim:
                                    sim = True
                                else:
                                    sim = False
                            except:
                                sim = False
                    except:
                        presim = False
                        try:
                            sim = Simulation.objects.filter(simparent=res[0].crnumber)
                            if sim:
                                sim = True
                            else:
                                sim = False
                        except:
                            sim = False
                else:
                    mx = False
                    try:
                        dx = S2Diagnosis.objects.filter(parent_id=res[0].crnumber)
                        if dx:
                            dx = True
                    except:
                        dx = False
            except:
                mx = False
                try:
                    # print("You Are Here 000")
                    dx = S2Diagnosis.objects.filter(parent_id=res[0].crnumber)
                    if dx:
                        dx = True
                except:
                    dx = False
        else:
            res = False
    except:
        res = False
    status = {'fu': fu, 'res': res, 'presim': presim, 'sim': sim, 'dx': dx, 'mx': mx, 'rt': rt,
              'pft': pft, 'cm': cm, 'presimdetails': presimdetails, 'crnumber': crnumber}
    return status


def get_timeline(crnumber):
    if S1ParentMain.objects.filter(crnumber=crnumber).exists():
        regdetails = S1ParentMain.objects.filter(crnumber=crnumber).last()
        if regdetails.height and regdetails.weight:
            bsa = 0.007184 * (float(regdetails.height) ** 0.725) * (float(regdetails.weight) ** 0.425)
        else:
            bsa = None
        reg_date = regdetails.reg_date
    else:
        reg_date = None
        regdetails = None
        bsa = None
    secondary = False
    new_primary = False
    primary_hpe = False
    if S2Diagnosis.objects.filter(parent_id=crnumber).exists():
        dxdetails = S2Diagnosis.objects.filter(parent_id=crnumber).all()
        dxinfo = []
        for num, dx in enumerate(dxdetails):
            if num == 1:
                if dx.icd_path_code:
                    primary_hpe = dx.icd_path_code.hpe
                else:
                    primary_hpe = None
            if dx.diagnosis:
                if dx.dx_type != "Second Malignancy":
                    primary = dx.diagnosis.our_diagnosis
                else:
                    primary = None
                    secondary = True
                    new_primary = dx.diagnosis.our_diagnosis
            else:
                primary = None
            if dx.icd_topo_code:
                main_topo = dx.icd_topo_code.site
            else:
                main_topo = None
            if dx.dx_type:
                dx_type = dx.dx_type.type
            else:
                dx_type = None
            if dx.icd_path_code:
                path_code = dx.icd_path_code.hpe
            else:
                path_code = None
            if dx.c_t:
                cT = dx.c_t
            elif dx.t_new:
                cT = dx.t_new
            else:
                cT = None
            if dx.c_n:
                cN = dx.c_n
            elif dx.n_new:
                cN = dx.n_new
            else:
                cN = None
            if dx.c_m:
                cM = dx.c_m
            elif dx.m_new:
                cM = dx.m_new
            else:
                cM = None
            if dx.c_stage_group:
                stage = dx.c_stage_group
            elif dx.stage_new:
                stage = dx.stage_new
            else:
                stage = None
            if dx.er:
                ER = dx.er
            else:
                ER = None
            if dx.pr:
                PR = dx.pr
            else:
                PR = None
            if dx.her2neu:
                HER2Neu = dx.her2neu
            else:
                HER2Neu = None
            if dx.egfr:
                EGFR = dx.egfr
            else:
                EGFR = None
            if dx.alk:
                ALK = dx.alk
            else:
                ALK = None
            if dx.ros:
                ROS = dx.ros
            else:
                ROS = None
            if dx.pdl_1:
                PDL1 = dx.pdl_1
            else:
                PDL1 = dx.pdl_1
            if dx.pdl_1_levels:
                PDL1Levels = dx.pdl_1_levels
            else:
                PDL1Levels = dx.pdl_1_levels
            dxinfo.append((dx.dx_date.date(), main_topo, dx_type, path_code, cT, cN, cM, stage, ER, PR, HER2Neu,
                           EGFR, ALK, ROS, PDL1, PDL1Levels, primary_hpe, primary, secondary, new_primary))
    else:
        dxinfo = None

    if S3CarePlan.objects.filter(parent_id=crnumber).exists():
        mxdetails = S3CarePlan.objects.filter(parent_id=crnumber).all()
        mxinfo = []
        for mx in mxdetails:
            siminfo = []
            rtinfo = []
            cheminfo = []
            sxinfo = []

            # Getting Radiation details
            if mx.sim_careplan_id.all():
                for sim in mx.sim_careplan_id.all():
                    siminfo.append(sim)
            if mx.s5chemoprotocol_set.all():
                for chemo in mx.s5chemoprotocol_set.all():
                    cheminfo.append(chemo)
            if mx.s4rt.all().exists():
                for rt in mx.s4rt.all():
                    rtinfo.append(rt)
            if mx.s6surgery_set.all().exists():
                for sx in mx.s6surgery_set.all():
                    sxinfo.append(sx)

            mxinfo.append((mx.startdate, mx.enddate, mx.surgery, mx.radiotherapy, mx.chemotherapy, mx.targettherapy,
                           mx.hormone, mx.immunotherapy, rtinfo, sxinfo, siminfo, cheminfo))
            # print(f"CHECK: RT info for {mx.s3_id}--{rtinfo}")
            # Todo same to be done for chemo, followup as done for radiotherapy above
    else:
        mxinfo = None
    if S4RT.objects.filter(parent_id=crnumber).exists():
        rtdetails = S4RT.objects.filter(parent_id=crnumber).all()
    if S5ChemoProtocol.objects.filter(parent_id=crnumber):
        chemodetails = S5ChemoProtocol.objects.filter(parent_id=crnumber).all()
    if S6Surgery.objects.filter(parent_id=crnumber):
        sxdetails = S6Surgery.objects.filter(parent_id=crnumber).all()
    if S8FUP.objects.filter(parent_id=crnumber).all():
        fupdetails = S6Surgery.objects.filter(parent_id=crnumber).all()

    return regdetails, reg_date, dxinfo, mxinfo, bsa


def getnewsimulation_choices(n):
    pass


def raw_query01(query, params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def mobile(request):
    """Return True if the request comes from a mobile device."""
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def get_tnm(site="Breast"):
    primary = TNM.objects.filter(site=site).values().first()
    optionsT = [("", "")]
    optionsN = [("", "")]
    optionsM = [("", "")]
    options_pT = [("", "")]
    options_pN = [("", "")]
    options_pM = [("", "")]
    for key, value in primary.items():
        # Anatomical T Stage
        if key != "id" and value is not None and key.startswith("c_t"):
            temp_t_list = key.split("_")
            if len(temp_t_list) > 2:
                optionsT.append((temp_t_list[2], "T" + temp_t_list[2] + ": " + value))
            else:
                optionsT.append((temp_t_list[1].split("t")[1], "T" + temp_t_list[1].split("t")[1] + ": " + value))
        # Patholigical T Stage
        if key != "id" and value is not None and key.startswith("p_t"):
            temp_t_list = key.split("_")
            if len(temp_t_list) > 2:
                options_pT.append((temp_t_list[2], "T" + temp_t_list[2] + ": " + value))
            else:
                options_pT.append((temp_t_list[1].split("t")[1], "T" + temp_t_list[1].split("t")[1] + ": " + value))
        # Anatomical N Stage
        if key != "id" and value is not None and key.startswith("c_n"):
            temp_n_list = key.split("_")
            if len(temp_n_list) > 2:
                optionsN.append((temp_n_list[2], "N" + temp_n_list[2] + ": " + value))
            else:
                optionsN.append((temp_n_list[1].split("n")[1], "N" + temp_n_list[1].split("n")[1] + ": " + value))
        # Patholigical N Stage
        if key != "id" and value is not None and key.startswith("p_n"):
            temp_n_list = key.split("_")
            if len(temp_n_list) > 2:
                options_pN.append((temp_n_list[2], "N" + temp_n_list[2] + ": " + value))
            else:
                options_pN.append((temp_n_list[1].split("n")[1], "N" + temp_n_list[1].split("n")[1] + ": " + value))
        # Anatomical M Stage
        if key != "id" and value is not None and key.startswith("c_m"):
            temp_m_list = key.split("_")
            if len(temp_m_list) > 2:
                optionsM.append((temp_m_list[2], "M" + temp_m_list[2] + ": " + value))
            else:
                optionsM.append((temp_m_list[1].split("m")[1], "M" + temp_m_list[1].split("m")[1] + ": " + value))
        # Patholigical M Stage
        if key != "id" and value is not None and key.startswith("p_m"):
            temp_m_list = key.split("_")
            if len(temp_m_list) > 2:
                options_pM.append((temp_m_list[2], "M" + temp_m_list[2] + ": " + value))
            else:
                options_pM.append((temp_m_list[1].split("m")[1], "M" + temp_m_list[1].split("m")[1] + ": " + value))

    # print(optionsT, optionsN, optionsM)
    return optionsT, optionsN, optionsM, options_pT, options_pN, options_pM


def get_stagegroup(request, pathologic=False):
    class DiagnosisForm(S2DiagnosisForm):
        def __init__(self, *args, **kwargs):
            super(DiagnosisForm, self).__init__(*args, **kwargs)
            self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                         widget=forms.Select(
                                                             attrs={'class': 'myselect form-control'}))
            self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))

    stage_choices = [(stage_gp, stage_gp) for stage_gp in StageGroup.objects.all()]
    stage_choices.insert(0, ("", ""))
    stage_message = False
    message_er = False
    message_pr = False
    message_her = False
    message_grade = False
    anatomical_stage_message = False
    if request.POST:
        dx = request.POST['diagnosis']
        # print(dx)
        if pathologic:
            m_status = request.POST['p_m_new']
            type = "Pathologic Prognostic"
            T, N = '_t' + request.POST['p_t_new'], '_n' + request.POST['p_n_new']
        else:
            type = "Clinical Prognostic"
            m_status = request.POST['m_new']
            T, N = '_t' + request.POST['t_new'], '_n' + request.POST['n_new']
        if m_status == "0":
            # class DiagnosisForm(S2DiagnosisForm):
            #     def __init__(self, *args, **kwargs):
            #         super(DiagnosisForm, self).__init__(*args, **kwargs)
            #         self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
            #                                                      widget=forms.Select(
            #                                                          attrs={'class': 'myselect form-control'}))
            #         self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
            #                                                      widget=forms.Select(
            #                                                          attrs={'class': 'myselect form-control'}))

            mets = False
            form = DiagnosisForm()
            # Stage Grouping for Breast
            M = '_m0'
            # T, N = '_t' + request.POST['t_new'], '_n' + request.POST['n_new']
            if dx == "12" or dx == "13":
                if "_t0" in T:
                    T = "_t0"
                elif "_t1" in T:
                    T = "_t1"
                elif "_t2" in T:
                    T = "_t2"
                elif "_t3" in T:
                    T = "_t3"
                elif "_t4" in T:
                    T = "_t4"
                else:
                    T = None
                if "_n1mi" in N or "_n0" in N:
                    N = N
                elif "_n1" in N:
                    N = "_n1"
                elif "_n2" in N:
                    N = "_n2"
                elif "_n3" in N:
                    N = "_n3"
                else:
                    N = None

            er, pr, her2neu = request.POST['er'], request.POST['pr'], request.POST['her2neu']
            try:
                grade = request.POST['biopsy_grade']
            except:
                grade = None
            if not er:
                message_er = "Please select ER status"
            else:
                message_er = None
            if not pr:
                message_pr = "Please select PR status"
            else:
                message_pr = None
            if not her2neu:
                message_her = "Please select HER2Neu status"
            else:
                message_her = None
            if not grade:
                message_grade = "Please select Grade"
            else:
                message_grade = None
            # print(T, N, M)
            if dx == "12":
                stage = BreastGroupTNM.objects.filter(staging_type=type, t=T, n=N, m=M, grade=grade, her2neu=her2neu,
                                                      er=er, pr=pr).first()
            elif dx == "13":
                if N == "_n3" and M == "_m0":
                    stage = EsoGroupTNM.objects.filter(staging_type="Anatomical", n=N, m=M, grade="NA",
                                                       location="NA").first()
                else:
                    stage = EsoGroupTNM.objects.filter(staging_type="Anatomical", t=T, n=N, m=M, grade="NA",
                                                       location="NA").first()
                message_er = None
                message_pr = None
                message_her = None
                message_grade = None
            elif dx == "10":
                if pathologic:
                    stage = NSCLCGroupTNM.objects.filter(staging_type="Pathological", t=T, n=N, m=M).first()
                else:
                    stage = NSCLCGroupTNM.objects.filter(staging_type="Anatomical", t=T, n=N, m=M).first()
                message_er = None
                message_pr = None
                message_her = None
                message_grade = None

            elif dx == "35" or dx == "45" or dx == "46":
                if pathologic:
                    stage = LarynxGroupTNM.objects.filter(staging_type="Pathological", t=T, n=N, m=M).first()
                else:
                    stage = LarynxGroupTNM.objects.filter(staging_type="Anatomical", t=T, n=N, m=M).first()
                message_er = None
                message_pr = None
                message_her = None
                message_grade = None

            elif dx == "3":
                if pathologic:
                    stage = OralGroupTNM.objects.filter(staging_type="Pathological", t=T, n=N, m=M).first()
                else:
                    stage = OralGroupTNM.objects.filter(staging_type="Anatomical", t=T, n=N, m=M).first()
                message_er = None
                message_pr = None
                message_her = None
                message_grade = None

            else:
                stage = None
                message_er = None
                message_pr = None
                message_her = None
                message_grade = None
            # print(type, T, N, M, grade, her2neu, er, pr)
            # print('Stage' + " " + stage.stage.lower())
            if stage:
                stage = 'Stage' + " " + stage.stage.lower()
                stage_message = False
            else:
                anatomical_stage = None
                if dx == "12":
                    anatomical_stage = BreastGroupTNM.objects.filter(staging_type="Anatomical", t=T, n=N, m=M,
                                                                     grade="any", her2neu="any", er="any",
                                                                     pr="any").first()
                if not anatomical_stage:
                    anatomical_stage_message = False
                else:
                    anatomical_stage_message = anatomical_stage.stage
                stage = ""
                stage_message = "Can not auto-populate stage! You can proceed manually"

            current_choice = [(stage, stage)]
            # stage_choices = [(stage_gp, stage_gp) for stage_gp in StageGroup.objects.all()]
            # stage_choices.insert(0, ("", ""))
            if not pathologic:
                form.fields["stage_new"].choices = stage_choices
                form.fields['stage_new'].initial = current_choice[0]
            else:
                form.fields["p_stage_new"].choices = stage_choices
                form.fields['p_stage_new'].initial = current_choice[0]
        elif m_status == "":
            mets = False
            form = DiagnosisForm()
            form.fields["stage_new"].choices = stage_choices
            form.fields["p_stage_new"].choices = stage_choices
            # form = S2DiagnosisForm()
            stage_message = "Please select appropriate M stage to determine the actual Stage Grouping"
        else:
            # class DiagnosisForm(S2DiagnosisForm):
            #     def __init__(self, *args, **kwargs):
            #         super(DiagnosisForm, self).__init__(*args, **kwargs)
            #         self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
            #                                                      widget=forms.Select(
            #                                                          attrs={'class': 'myselect form-control'}))
            #         self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
            #                                                      widget=forms.Select(
            #                                                          attrs={'class': 'myselect form-control'}))

            dx = request.POST['diagnosis']
            form = DiagnosisForm()
            # stage_choices = [(stage_gp, stage_gp) for stage_gp in StageGroup.objects.all()]
            form.fields["stage_new"].choices = stage_choices
            form.fields["p_stage_new"].choices = stage_choices
            M = '_m' + request.POST['m_new']
            pM = '_m' + request.POST['p_m_new']
            if pathologic:
                if dx == "10" and pM == "_m1c":
                    form.fields['p_stage_new'].initial = stage_choices[19]
                elif dx == "10" and (pM == "_m1a" or pM == "_m1b"):
                    form.fields['p_stage_new'].initial = stage_choices[18]
                else:
                    form.fields['p_stage_new'].initial = stage_choices[17]
            else:
                if dx == "10" and M == "_m1c":
                    form.fields['stage_new'].initial = stage_choices[19]
                elif dx == "10" and (M == "_m1a" or M == "_m1b"):
                    form.fields['stage_new'].initial = stage_choices[18]
                else:
                    form.fields['stage_new'].initial = stage_choices[17]
            mets = True

        context = {'form': form, 'mets': mets, "stage_message": stage_message,
                   'message_er': message_er, 'message_pr': message_pr,
                   'message_her': message_her, 'message_grade': message_grade,
                   'anatomical_stage_message': anatomical_stage_message}
        return context
