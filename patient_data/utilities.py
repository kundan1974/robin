from patient_data.models import S1ParentMain, S3CarePlan, PreSimulation, Simulation, S2Diagnosis, S8FUP


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
