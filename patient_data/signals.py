from django.db.models.signals import post_save

from patient_data.models import S7Assessment, Simulation, S3CarePlan, S8FUP


def simulationUpdate(sender, instance, created, **kwargs):
    if not created:
        patient_sim = Simulation.objects.get(simid=instance.s4_id.simid.simid)
        patient_sim.donefr = instance.fxdone
        patient_sim.as_date = instance.as_date
        patient_sim.save()
        print('CREATED:', created)
        print('USER:', instance.updated_by)


def careplanUpdate(sender, instance, created, **kwargs):
    if instance.visitaction.code == "CC-STC":
        patient_mx = S3CarePlan.objects.get(pk=instance.s3_id.s3_id)
        patient_mx.enddate = instance.visitdate
        patient_mx.save()
    else:
        if S3CarePlan.objects.filter(parent_id=instance.parent_id):
            patient_mx = S3CarePlan.objects.get(pk=instance.s3_id.s3_id)
            patient_mx.enddate = None
            patient_mx.save()
        else:
            print("No Careplan")
            pass


post_save.connect(simulationUpdate, sender=S7Assessment)
post_save.connect(careplanUpdate, sender=S8FUP)
