from patient_data.models import S1ParentMain, S3CarePlan, PreSimulation, Simulation, S2Diagnosis, S8FUP, S4RT, \
    S5ChemoProtocol, S6Surgery
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
                    print("You Are Here 000")
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
        reg_date = regdetails.reg_date
    else:
        reg_date = None
        regdetails = None
    if S2Diagnosis.objects.filter(parent_id=crnumber).exists():
        dxdetails = S2Diagnosis.objects.filter(parent_id=crnumber).all()
        dxinfo = []
        for dx in dxdetails:
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
            else:
                cT = None
            if dx.c_n:
                cN = dx.c_n
            else:
                cN = None
            if dx.c_m:
                cM = dx.c_m
            else:
                cM = None
            if dx.c_stage_group:
                stage = dx.c_stage_group
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
                           EGFR, ALK, ROS, PDL1, PDL1Levels))
    else:
        dxinfo = None

    if S3CarePlan.objects.filter(parent_id=crnumber).exists():
        mxdetails = S3CarePlan.objects.filter(parent_id=crnumber).all()
        mxinfo = []
        for mx in mxdetails:
            rtinfo = []
            cheminfo = []
            sxinfo = []

            # Getting Radiation details
            if mx.s4rt.all().exists():
                for rt in mx.s4rt.all():
                    rtinfo.append(rt)
            if mx.s6surgery_set.all().exists():
                for sx in mx.s6surgery_set.all():
                    sxinfo.append(sx)

            mxinfo.append((mx.startdate, mx.enddate, mx.surgery, mx.radiotherapy, mx.chemotherapy, mx.targettherapy,
                           mx.hormone, mx.immunotherapy, rtinfo, sxinfo))
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

    return regdetails, reg_date, dxinfo, mxinfo


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
