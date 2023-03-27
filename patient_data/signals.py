from django.db.models.signals import post_save

from patient_data.models import S7Assessment, Simulation, S3CarePlan, S8FUP, S4RT, RTStatus


def simulationUpdate(sender, instance, created, **kwargs):
    patient_sim = Simulation.objects.get(simid=instance.s4_id.simid.simid)
    patient_sim.donefr = instance.fxdone
    patient_sim.as_date = instance.as_date
    if instance.txstatus == "Last Day":
        patient_sim.finalstatus = 1  # treatment completed 1
    else:
        patient_sim.finalstatus = 0  # treatment ongoing 0
    patient_sim.save()


def careplanUpdate(sender, instance, created, **kwargs):
    if instance.visitaction.code == "CC-STC":
        patient_mx = S3CarePlan.objects.get(pk=instance.s3_id.s3_id)
        patient_mx.enddate = instance.visitdate
        patient_mx.save()
    else:
        if S3CarePlan.objects.filter(parent_id=instance.parent_id):
            try:
                patient_mx = S3CarePlan.objects.get(pk=instance.s3_id.s3_id)
                patient_mx.enddate = None
                patient_mx.save()
            except AttributeError:
                pass
        else:
            pass


def radiotherapyUpdate(sender, instance, created, **kwargs):
    patient_rt = S4RT.objects.get(s4_id=instance.s4_id.s4_id)
    rt_status = RTStatus.objects.get(pk="1")
    if instance.txstatus == "Last Day":
        patient_rt.rtstatus = rt_status  # treatment completed 1
        patient_rt.rtfinishdate = instance.as_date
    else:
        rt_status = RTStatus.objects.get(pk="0")
        patient_rt.rtstatus = rt_status

    patient_rt.save()


post_save.connect(simulationUpdate, sender=S7Assessment)
post_save.connect(radiotherapyUpdate, sender=S7Assessment)
post_save.connect(careplanUpdate, sender=S8FUP)
