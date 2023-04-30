from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Section1 - Models for option data

class City(models.Model):
    city = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.city}'


class Comorbidity(models.Model):
    code = models.CharField(max_length=250, primary_key=True, unique=True)
    comorbidity = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.comorbidity}'


class Referredby(models.Model):
    refby = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.refby}'


class OurDiagnosis(models.Model):  # used for reg_diagnosis field in PatientRegistration Model
    our_diagnosis = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.our_diagnosis}'


class HPE(models.Model):
    code = models.CharField(max_length=250)
    hpe = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.hpe}'


class Site(models.Model):
    code = models.CharField(max_length=250)
    site = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.site}'


class ChemoProtocolNew(models.Model):
    code = models.CharField(max_length=250, unique=True)
    protocol = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.protocol}'


class FollowupVisitsType(models.Model):
    code = models.CharField(max_length=250, unique=True)
    visittype = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.visittype}'


class FollowupActions(models.Model):
    code = models.CharField(max_length=250, unique=True)
    actions = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.actions}'


class StrType(models.Model):
    code = models.CharField(max_length=250, unique=True)
    strtype = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.strtype}'


class StrName(models.Model):
    code = models.CharField(max_length=250, unique=True)
    strname = models.CharField(max_length=250)  # As Per FMAID

    def __str__(self):
        return f'{self.strname}'


class StrNameClassifierBase(models.Model):
    code = models.CharField(max_length=250, unique=True)
    classifier = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.classifier}'


class StrNameClassifierNumber(models.Model):
    code = models.CharField(max_length=250, unique=True)
    classifier = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.classifier}'


class StrNameClassifierImage(models.Model):
    code = models.CharField(max_length=250, unique=True)
    classifier = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.classifier}'


class StrNameClassifierDose(models.Model):
    code = models.CharField(max_length=250, unique=True)
    classifier = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.classifier}'


class StrNameClassifierCustom(models.Model):
    code = models.CharField(max_length=250, unique=True)
    classifier = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.classifier}'


class DVHParameters(models.Model):
    code = models.CharField(max_length=250, unique=True)
    Description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


# Models for radiation oncology SIMULATION TABLE CHOICES


class RTSites(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    site = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class ICDMainSites(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    site = models.CharField(max_length=250)
    icd_code = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.code}'


class RTTech(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    tech = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class RTIntent(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    intent = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class RTVolumes(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    volume = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class PreSimStatus(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    status = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class SimStatus(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    status = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class DxType(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    type = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class BiopsyGrade(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    grade = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class ClinT(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    c_t = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class ClinN(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    c_n = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class ClinM(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    c_m = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class StageGroup(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    stage_group = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class AjccEdition(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    ajcc_edition = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class StudyGroup(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    code = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class RTMachines(models.Model):
    code = models.CharField(max_length=250, primary_key=True)
    rtmachines = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class RTStatus(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    code = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.code}'


class ChemoDrugs(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    code = models.CharField(max_length=200)
    drug_class = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        db_table = 'patient_data_drugs'

    def __str__(self):
        return f'{self.code}'


class SxCodes(models.Model):
    code = models.CharField(max_length=45, primary_key=True)
    surgery = models.CharField(max_length=255)

    class Meta:
        db_table = 'patient_data_sxcode'

    def __str__(self):
        return f'{self.surgery}'


class FMAID(models.Model):
    fma_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    shortname = models.CharField(max_length=255)

    class Meta:
        db_table = 'patient_data_fmaid'

    def __str__(self):
        return f'{self.shortname}--{self.description}'


# InvestigationImaging
class ImagingType(models.Model):
    code = models.CharField(max_length=250)
    type = models.CharField(max_length=255)

    class Meta:
        db_table = 'patient_data_imagingtype'

    def __str__(self):
        return f'{self.code}--{self.type}'


class ImageLocation(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    location = models.CharField(max_length=255, unique=True, blank=False, null=False)

    class Meta:
        db_table = 'patient_data_imagelocation'

    def __str__(self):
        return f'{self.location}'


class ImagingResult(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    result = models.CharField(max_length=255, unique=True, blank=False, null=False)

    class Meta:
        db_table = 'patient_data_imagingresult'

    def __str__(self):
        return f'{self.result}'


class LabName(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)

    class Meta:
        db_table = 'patient_data_labname'

    def __str__(self):
        return f'{self.name}'


class CTCV5(models.Model):
    code = models.IntegerField(primary_key=True, blank=False, null=False)
    system = models.CharField(max_length=255, blank=False, null=False)
    term = models.CharField(max_length=255, unique=True, blank=False, null=False)
    grade0 = models.CharField(max_length=25, blank=True, null=True)
    grade1 = models.CharField(max_length=1000, blank=True, null=True)
    grade2 = models.CharField(max_length=1000, blank=True, null=True)
    grade3 = models.CharField(max_length=1000, blank=True, null=True)
    grade4 = models.CharField(max_length=1000, blank=True, null=True)
    grade5 = models.CharField(max_length=255, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ctc_v5_27_11_2017'

    def __str__(self):
        return f'{self.term}'


class GenDrugs(models.Model):
    drug = models.CharField(max_length=255, unique=True, blank=False, null=False)
    composition = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        db_table = 'gen_drugs'

    def __str__(self):
        return f'{self.drug} - {self.composition}'


class TNM(models.Model):
    site = models.CharField(max_length=150, blank=False, null=False)
    c_tx = models.CharField(max_length=500, blank=True, null=True)
    c_t0 = models.CharField(max_length=150, blank=True, null=True)
    c_tis_dcis = models.CharField(max_length=250, blank=True, null=True)
    c_tis_pagets = models.TextField(blank=True, null=True)
    c_t1 = models.TextField(blank=True, null=True)
    c_t1mi = models.TextField(blank=True, null=True)
    c_t1a = models.TextField(blank=True, null=True)
    c_t1a1 = models.TextField(blank=True, null=True)
    c_t1a2 = models.TextField(blank=True, null=True)
    c_t1b = models.TextField(blank=True, null=True)
    c_t1b1 = models.TextField(blank=True, null=True)
    c_t1b2 = models.TextField(blank=True, null=True)
    c_t1b3 = models.TextField(blank=True, null=True)
    c_t1c = models.TextField(blank=True, null=True)
    c_t1d = models.TextField(blank=True, null=True)
    c_t2 = models.TextField(blank=True, null=True)
    c_t2a = models.TextField(blank=True, null=True)
    c_t2a1 = models.TextField(blank=True, null=True)
    c_t2a2 = models.TextField(blank=True, null=True)
    c_t2b = models.TextField(blank=True, null=True)
    c_t2c = models.TextField(blank=True, null=True)
    c_t2d = models.TextField(blank=True, null=True)
    c_t3 = models.TextField(blank=True, null=True)
    c_t3a = models.TextField(blank=True, null=True)
    c_t3b = models.TextField(blank=True, null=True)
    c_t3c = models.TextField(blank=True, null=True)
    c_t3c1 = models.TextField(blank=True, null=True)
    c_t3c2 = models.TextField(blank=True, null=True)
    c_t3d = models.TextField(blank=True, null=True)
    c_t4 = models.TextField(blank=True, null=True)
    c_t4a = models.TextField(blank=True, null=True)
    c_t4b = models.TextField(blank=True, null=True)
    c_t4c = models.TextField(blank=True, null=True)
    c_t4d = models.TextField(blank=True, null=True)
    c_nx = models.TextField(blank=True, null=True)
    c_n0 = models.TextField(blank=True, null=True)
    c_n1 = models.TextField(blank=True, null=True)
    c_n1mi = models.TextField(blank=True, null=True)
    c_n1a = models.TextField(blank=True, null=True)
    c_n1b = models.TextField(blank=True, null=True)
    c_n1c = models.TextField(blank=True, null=True)
    c_n1d = models.TextField(blank=True, null=True)
    c_n2 = models.TextField(blank=True, null=True)
    c_n2a = models.TextField(blank=True, null=True)
    c_n2b = models.TextField(blank=True, null=True)
    c_n2c = models.TextField(blank=True, null=True)
    c_n2d = models.TextField(blank=True, null=True)
    c_n3 = models.TextField(blank=True, null=True)
    c_n3a = models.TextField(blank=True, null=True)
    c_n3b = models.TextField(blank=True, null=True)
    c_n3c = models.TextField(blank=True, null=True)
    c_n3d = models.TextField(blank=True, null=True)
    c_m0 = models.TextField(blank=True, null=True)
    c_m0_iplus = models.TextField(blank=True, null=True)
    c_m1 = models.TextField(blank=True, null=True)
    c_m1a = models.TextField(blank=True, null=True)
    c_m1b = models.TextField(blank=True, null=True)
    c_m1c = models.TextField(blank=True, null=True)

    p_tx = models.CharField(max_length=500, blank=True, null=True)
    p_t0 = models.CharField(max_length=150, blank=True, null=True)
    p_tis_dcis = models.CharField(max_length=250, blank=True, null=True)
    p_tis_pagets = models.TextField(blank=True, null=True)
    p_t1 = models.TextField(blank=True, null=True)
    p_t1mi = models.TextField(blank=True, null=True)
    p_t1a = models.TextField(blank=True, null=True)
    p_t1a1 = models.TextField(blank=True, null=True)
    p_t1a2 = models.TextField(blank=True, null=True)
    p_t1b = models.TextField(blank=True, null=True)
    p_t1b1 = models.TextField(blank=True, null=True)
    p_t1b2 = models.TextField(blank=True, null=True)
    p_t1b3 = models.TextField(blank=True, null=True)
    p_t1c = models.TextField(blank=True, null=True)
    p_t1d = models.TextField(blank=True, null=True)
    p_t2 = models.TextField(blank=True, null=True)
    p_t2a = models.TextField(blank=True, null=True)
    p_t2a1 = models.TextField(blank=True, null=True)
    p_t2a2 = models.TextField(blank=True, null=True)
    p_t2b = models.TextField(blank=True, null=True)
    p_t2c = models.TextField(blank=True, null=True)
    p_t2d = models.TextField(blank=True, null=True)
    p_t3 = models.TextField(blank=True, null=True)
    p_t3a = models.TextField(blank=True, null=True)
    p_t3b = models.TextField(blank=True, null=True)
    p_t3c = models.TextField(blank=True, null=True)
    p_t3c1 = models.TextField(blank=True, null=True)
    p_t3c2 = models.TextField(blank=True, null=True)
    p_t3d = models.TextField(blank=True, null=True)
    p_t4 = models.TextField(blank=True, null=True)
    p_t4a = models.TextField(blank=True, null=True)
    p_t4b = models.TextField(blank=True, null=True)
    p_t4c = models.TextField(blank=True, null=True)
    p_t4d = models.TextField(blank=True, null=True)
    p_nx = models.TextField(blank=True, null=True)
    p_n0 = models.TextField(blank=True, null=True)
    p_n0_iplus = models.TextField(blank=True, null=True)
    p_n0_molplus = models.TextField(blank=True, null=True)
    p_n1 = models.TextField(blank=True, null=True)
    p_n1mi = models.TextField(blank=True, null=True)
    p_n1a = models.TextField(blank=True, null=True)
    p_n1b = models.TextField(blank=True, null=True)
    p_n1c = models.TextField(blank=True, null=True)
    p_n1d = models.TextField(blank=True, null=True)
    p_n2 = models.TextField(blank=True, null=True)
    p_n2a = models.TextField(blank=True, null=True)
    p_n2b = models.TextField(blank=True, null=True)
    p_n2c = models.TextField(blank=True, null=True)
    p_n2d = models.TextField(blank=True, null=True)
    p_n3 = models.TextField(blank=True, null=True)
    p_n3a = models.TextField(blank=True, null=True)
    p_n3b = models.TextField(blank=True, null=True)
    p_n3c = models.TextField(blank=True, null=True)
    p_n3d = models.TextField(blank=True, null=True)
    p_n_sn = models.TextField(blank=True, null=True)
    p_m0 = models.TextField(blank=True, null=True)
    p_m1 = models.TextField(blank=True, null=True)
    p_m1a = models.TextField(blank=True, null=True)
    p_m1b = models.TextField(blank=True, null=True)
    p_m1c = models.TextField(blank=True, null=True)
    limited_stage = models.TextField(blank=True, null=True)
    extensive_stage = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tnm'

    def __str__(self):
        return f'{self.site}'


class BreastGroupTNM(models.Model):
    site = models.CharField(max_length=100, blank=False, null=False)
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    grade = models.CharField(max_length=50, blank=True, null=True)
    her2neu = models.CharField(max_length=50, blank=True, null=True)
    er = models.CharField(max_length=50, blank=True, null=True)
    pr = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_breast_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class STSGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    grade = models.CharField(max_length=50, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_sts_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class NSCLCGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_nsclc_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class OralGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_oral_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class NasoGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_naso_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class OroHpvNegGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_orohypo_hpvneg_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class OroHpvPosGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_oro_hpvpos_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class LarynxGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_larynx_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class PNSGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_pns_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


class EsoGroupTNM(models.Model):
    staging_type = models.CharField(max_length=100, blank=False, null=False)
    t = models.CharField(max_length=50, blank=False, null=False)
    n = models.CharField(max_length=50, blank=False, null=False)
    m = models.CharField(max_length=50, blank=False, null=False)
    grade = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tnm_eso_group'

    def __str__(self):
        return f'{self.t} {self.n} {self.m} {self.stage}'


# Models for Radiation Oncology Database

class S1ParentMain(models.Model):
    s1_id = models.AutoField(primary_key=True, blank=False, null=False)
    crnumber = models.CharField(max_length=16, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.SmallIntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    ecog = models.CharField(max_length=250, blank=True, null=True)
    doc_type = models.CharField(max_length=45, blank=True, null=True)
    doc_id = models.CharField(max_length=45, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True)
    smoking = models.CharField(max_length=45, blank=True, null=True)
    smoking_status = models.CharField(max_length=45, blank=True, null=True)
    smoking_volume = models.CharField(max_length=45, blank=True, null=True)
    comorbidity = models.ManyToManyField(Comorbidity, blank=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.CharField(max_length=45, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 's1_parent_main'
        ordering = ['-last_updated']

    def __str__(self):
        return f'CRN: {self.crnumber} -- Name: {self.first_name} {self.last_name} -- Mobile: {self.mobile}'


class S2Diagnosis(models.Model):
    s2_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, to_field='crnumber', blank=False, null=True)
    # dx_id = models.CharField(max_length=45, blank=False, null=False, unique=True)
    # dx = models.CharField(max_length=100, blank=True, null=True)
    diagnosis = models.ForeignKey(OurDiagnosis, blank=True, null=True, on_delete=models.DO_NOTHING)  # FK
    laterality = models.CharField(max_length=45, blank=True, null=True)
    dx_type = models.ForeignKey(DxType, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    icd_main_topo = models.ForeignKey(ICDMainSites, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    icd_topo_code = models.ForeignKey(Site, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    icd_path_code = models.ForeignKey(HPE, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    # icd_topo = models.CharField(max_length=254, blank=True, null=True)
    # icd_topo_code = models.CharField(max_length=254, blank=True, null=True)
    # icd_path = models.CharField(max_length=254, blank=True, null=True)
    # icd_path_code = models.CharField(max_length=254, blank=True, null=True)
    dx_date = models.DateTimeField(blank=False, null=True)
    biopsy_no = models.CharField(max_length=45, blank=True, null=True)
    biopsy = models.CharField(max_length=254, blank=True, null=True)
    biopsy_date = models.DateTimeField(blank=True, null=True)
    biopsy_grade = models.ForeignKey(BiopsyGrade, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    confirmed_by = models.CharField(max_length=45, blank=True, null=True)
    c_t = models.ForeignKey(ClinT, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    c_n = models.ForeignKey(ClinN, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    c_m = models.ForeignKey(ClinM, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    c_stage_group = models.ForeignKey(StageGroup, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    t_new = models.CharField(max_length=500, blank=True, null=True)
    n_new = models.CharField(max_length=500, blank=True, null=True)
    m_new = models.CharField(max_length=500, blank=True, null=True)
    mets_site = models.ManyToManyField(FMAID, blank=True, related_name="mets_site")
    stage_new = models.CharField(max_length=50, blank=True, null=True)
    p_t_new = models.CharField(max_length=500, blank=True, null=True)
    p_n_new = models.CharField(max_length=500, blank=True, null=True)
    p_m_new = models.CharField(max_length=500, blank=True, null=True)
    p_mets_site = models.ManyToManyField(FMAID, blank=True, related_name="p_mets_site")
    p_stage_new = models.CharField(max_length=50, blank=True, null=True)

    p_t = models.ForeignKey(ClinT, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="path_t")  # FK
    p_n = models.ForeignKey(ClinN, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="path_n")  # FK
    p_m = models.ForeignKey(ClinM, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="path_m")  # FK
    p_stage_group = models.ForeignKey(StageGroup, null=True, blank=True, on_delete=models.DO_NOTHING,
                                      related_name="path_stage_group")  # FK

    c_ajcc_edition = models.ForeignKey(AjccEdition, null=True, blank=True, on_delete=models.DO_NOTHING)  # FK
    er = models.CharField(max_length=45, blank=True, null=True)
    pr = models.CharField(max_length=45, blank=True, null=True)
    her2neu = models.CharField(max_length=45, blank=True, null=True)
    braca1 = models.CharField(max_length=45, blank=True, null=True)
    braca2 = models.CharField(max_length=45, blank=True, null=True)
    egfr = models.CharField(max_length=45, blank=True, null=True)
    alk = models.CharField(max_length=45, blank=True, null=True)
    ros = models.CharField(max_length=45, blank=True, null=True)
    pdl_1 = models.CharField(max_length=45, blank=True, null=True)
    pdl_1_levels = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    braf = models.CharField(max_length=45, blank=True, null=True)
    met = models.CharField(max_length=45, blank=True, null=True)
    ret = models.CharField(max_length=45, blank=True, null=True)
    hpv = models.CharField(max_length=45, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's2_child_dx'

    def __str__(self):
        return f'CRN: {self.parent_id} -- Diagnosis: {self.diagnosis} --Site: {self.icd_topo_code} --HPE: {self.icd_path_code}'


class S3CarePlan(models.Model):
    s3_id = models.AutoField(primary_key=True)
    s2_id = models.ForeignKey(S2Diagnosis, models.CASCADE, blank=False, db_column='s2_id', null=True,
                              to_field='s2_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, to_field='crnumber', blank=False, null=True,
                                  db_column='parent_id')
    # s3_dx_id = models.ForeignKey(S2Diagnosis, models.CASCADE, to_field='dx_id',
    #                              db_column='s3_dx_id', blank=True, null=True, )
    # mx_id = models.CharField(max_length=40, blank=False, null=False, unique=True)
    # mcourse = models.CharField(max_length=40, blank=True, null=True)
    startdate = models.DateTimeField(blank=True, null=True)
    enddate = models.DateTimeField(blank=True, null=True)
    intent = models.CharField(max_length=45, blank=True, null=True)
    radiotherapy = models.CharField(max_length=45, blank=True, null=True)
    surgery = models.CharField(max_length=45, blank=True, null=True)
    chemotherapy = models.CharField(max_length=45, blank=True, null=True)
    brachytherapy = models.CharField(max_length=45, blank=True, null=True)
    hormone = models.CharField(max_length=45, blank=True, null=True)
    immunotherapy = models.CharField(max_length=45, blank=True, null=True)
    bmt = models.CharField(max_length=45, blank=True, null=True)
    targettherapy = models.CharField(max_length=45, blank=True, null=True)
    studyprotocol = models.ManyToManyField(StudyGroup, blank=True)
    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's3_child_cp'

    def __str__(self):
        return f'CRN: {self.parent_id} -- DxID: {self.s3_id} -- Startdate: {self.startdate}'


class PreSimulation(models.Model):
    presimid = models.AutoField(db_column='presimID', primary_key=True)
    presimparent = models.ForeignKey(S1ParentMain, models.CASCADE, to_field='crnumber', blank=False, null=True)
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=True, db_column='s3_id', to_field='s3_id', null=True)
    # Day 1
    day1date = models.DateTimeField(blank=True, null=True)
    ul_amp_d1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp_d1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp_d1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd_d1 = models.IntegerField(blank=True, null=True)  # Average hold duration
    al_d1 = models.BooleanField()  # Air leak
    d1remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby_day1 = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby_day1")
    day1status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True,
                                   related_name='day1status')  # Status on Day 1
    # Day2
    day2date = models.DateTimeField(blank=True, null=True)
    ul_amp_d2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp_d2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp_d2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd_d2 = models.IntegerField(blank=True, null=True)  # Average hold duration
    al_d2 = models.BooleanField()  # Air leak
    d2remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby_day2 = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby_day2")
    day2status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True,
                                   related_name='day2status')  # Status on Day 2
    # Day3
    day3date = models.DateTimeField(blank=True, null=True)
    ul_amp_d3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp_d3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp_d3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd_d3 = models.IntegerField(blank=True, null=True)  # Average hold duration
    al_d3 = models.BooleanField()  # Air leak
    d3remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby_day3 = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby_day3")
    day3status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True,
                                   related_name='day3status')  # Status on Day 3
    # Day4
    day4date = models.DateTimeField(blank=True, null=True)
    ul_amp_d4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp_d4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp_d4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd_d4 = models.IntegerField(blank=True, null=True)  # Average hold duration
    al_d4 = models.BooleanField()  # Air leak
    d4remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby_day4 = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby_day4")
    day4status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True,
                                   related_name='day4status')  # Status on Day 4
    # Day5
    day5date = models.DateTimeField(blank=True, null=True)
    ul_amp_d5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp_d5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp_d5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd_d5 = models.IntegerField(blank=True, null=True)  # Average hold duration
    al_d5 = models.BooleanField()  # Air leak
    d5remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby_day5 = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby_day5")
    day5status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True,
                                   related_name='day5status')  # Status on Day 5
    xray_status = models.BooleanField()  # Pre RT Xray Chest done at RGCIRC or not
    final_status = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True,
                                     related_name="final_status")  # Final Status on Day 3/4/5.
    final_remarks = models.TextField(blank=True, null=True)
    # Options same as technique field in Simulation table
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.CharField(max_length=45, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'presimulation'

    def __str__(self):
        return f'{self.presimparent} -- {self.presimid} -- {self.day1status} -- {self.day2status}-- {self.day3status}'


class NewPreSimulation(models.Model):
    presimid = models.AutoField(db_column='presimID', primary_key=True)
    presimparent = models.ForeignKey(S1ParentMain, models.CASCADE, to_field='crnumber', blank=False, null=True)
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=True, db_column='s3_id', to_field='s3_id', null=True)
    # Day 1
    date = models.DateTimeField(blank=False, null=True)
    day = models.CharField(max_length=45, blank=False, null=True)  # Day 1, Day2, Day3
    ul_amp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Upper limit of amplitude
    ll_amp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Lower limit of amplitude
    average_amp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Average Amp
    ahd = models.IntegerField(blank=True, null=True)  # Average hold duration
    al = models.BooleanField()  # Air leak
    remarks = models.TextField(blank=True, null=True)
    # DIBH Assessment done by
    assessedby = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="assessedby")
    status = models.ForeignKey(PreSimStatus, models.DO_NOTHING, blank=True, null=True)  # Status on Day 1
    final_status = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True)  # Final Status on Day 3/4/5.
    # Options same as technique field in Simulation table
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.CharField(max_length=45, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'new_presimulation'

    def __str__(self):
        return f'CRNumber: {self.presimparent} -- PreSimID: {self.presimid} -- FinalStatus: {self.final_status}'


class Simulation(models.Model):
    simid = models.AutoField(db_column='simID', primary_key=True)  # Field name made lowercase.
    presimid = models.ForeignKey(NewPreSimulation, models.DO_NOTHING, blank=True, null=True)
    simparent = models.ForeignKey(S1ParentMain, models.CASCADE, db_column='simParent_ID', to_field='crnumber',
                                  blank=False, null=True)  # Field name made lowercase.
    s2_id = models.ForeignKey(S2Diagnosis, models.CASCADE, blank=False, null=True,
                              db_column='s2_id', to_field='s2_id', related_name="sim_diagnosis_id")
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=True, null=True,
                              db_column="s3_id", to_field="s3_id", related_name="sim_careplan_id")
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    simdate = models.DateTimeField(db_column='SimDate')  # Field name made lowercase.
    simnotes = models.TextField(db_column='SimNotes', blank=True, null=True)  # Field name made lowercase.
    impdate = models.DateTimeField(db_column='ImpDate')  # Field name made lowercase.
    impnotes = models.TextField(db_column='ImpNotes', blank=True, null=True)  # Field name made lowercase.
    initialstatus = models.ForeignKey(SimStatus, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    finalstatus = models.IntegerField(db_column='finalstatus', blank=True, null=True)  # Field name made lowercase.
    futureplan = models.TextField(db_column='FuturePlan', blank=True, null=True)  # Field name made lowercase.
    site = models.ForeignKey(RTSites, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    icdmainsite = models.ManyToManyField(FMAID, blank=True)
    technique = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    intent = models.ForeignKey(RTIntent, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    volumes = models.ForeignKey(RTVolumes, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    dosephase1 = models.DecimalField(db_column='DosePhase1', max_digits=5, decimal_places=2, blank=True,
                                     null=True)  # Field name made lowercase.
    fxphase1 = models.IntegerField(db_column='FxPhase1', blank=True, null=True)  # Field name made lowercase.
    dosephase2 = models.DecimalField(db_column='DosePhase2', max_digits=5, decimal_places=2, blank=True,
                                     null=True)  # Field name made lowercase.
    fxphase2 = models.IntegerField(db_column='FxPhase2', blank=True, null=True)  # Field name made lowercase.
    dosephase3 = models.DecimalField(db_column='DosePhase3', max_digits=5, decimal_places=2, blank=True,
                                     null=True)  # Field name made lowercase.
    fxphase3 = models.IntegerField(db_column='FxPhase3', blank=True, null=True)  # Field name made lowercase.

    dosephase4 = models.DecimalField(db_column='DosePhase4', max_digits=5, decimal_places=2, blank=True,
                                     null=True)  # Field name made lowercase.
    fxphase4 = models.IntegerField(db_column='FxPhase4', blank=True, null=True)  # Field name made lowercase.

    totaldose = models.DecimalField(db_column='TotalDose', max_digits=5, decimal_places=2, blank=True,
                                    null=True)  # Field name made lowercase.
    totalfractions = models.IntegerField(db_column='TotalFractions', blank=True,
                                         null=True)  # Field name made lowercase.
    assignedto = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name="AssignedTo")
    send_mail = models.BooleanField(default=0)
    remarks = models.TextField(blank=True, null=True)
    tentativecompletiondate = models.DateTimeField(db_column='TentativeCompletionDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    actualcompletiondate = models.DateTimeField(db_column='ActualCompletionDate', blank=True,
                                                null=True)  # Field name made lowercase.
    as_date = models.DateTimeField(db_column='As_Date', blank=True, null=True)  # Field name made lowercase.
    donefr = models.IntegerField(db_column='DoneFr', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.CharField(max_length=45, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'simulation'

    def __str__(self):
        return f'{self.simparent} -- {self.simid} -- {self.name} -- {self.site}'


class S4RT(models.Model):
    s4_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, to_field='crnumber', null=True,
                                  db_column='parent_id')
    s2_id = models.ForeignKey(S2Diagnosis, models.CASCADE, blank=False, null=True,
                              db_column='s2_id', to_field='s2_id', related_name="rt_diagnosis_id")
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=False, null=True,
                              db_column="s3_id", to_field="s3_id", related_name="s4rt")

    simid = models.ForeignKey(Simulation, models.RESTRICT, blank=False, unique=False, db_column='simid', null=True, )
    # rtcourse = models.CharField(max_length=40, blank=False, null=False)
    rtindication = models.ForeignKey(RTIntent, models.CASCADE, db_column='rtindication', blank=True, null=True, )
    simdate = models.DateTimeField(blank=True, null=True)
    rtsite_main = models.ManyToManyField(FMAID, blank=True)  # FK

    rtsitecode = models.ForeignKey(Site, null=True, blank=True, on_delete=models.DO_NOTHING, db_column='rtsitecode')
    rtdose1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rtdosefr1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    modality1 = models.CharField(max_length=45, blank=True, null=True)
    tech1 = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True, db_column='tech1', related_name='tech1')
    rtdose2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rtdosefr2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    modality2 = models.CharField(max_length=45, blank=True, null=True)
    tech2 = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True, db_column='tech2', related_name='tech2')
    rtdose3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rtdosefr3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    modality3 = models.CharField(max_length=45, blank=True, null=True)
    tech3 = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True, db_column='tech3', related_name='tech3')
    rtdose4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rtdosefr4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    modality4 = models.CharField(max_length=45, blank=True, null=True)
    tech4 = models.ForeignKey(RTTech, models.DO_NOTHING, blank=True, null=True, db_column='tech4', related_name='tech4')
    rtstartdate = models.DateTimeField(blank=True, null=True)
    rtfinishdate = models.DateTimeField(blank=True, null=True)
    rtmachine = models.ForeignKey(RTMachines, models.DO_NOTHING, blank=True, null=True, db_column='rtmachine',
                                  related_name='rtmachine')
    rtstatus = models.ForeignKey(RTStatus, models.DO_NOTHING, blank=False, null=True, db_column='rtstatus',
                                 related_name='rtstatus')
    institution = models.CharField(max_length=100, blank=True, null=True)
    studygp = models.ManyToManyField(StudyGroup, blank=True)
    # studygp2 = models.ForeignKey(StudyGroup, models.DO_NOTHING, blank=True, null=True, db_column='studygp2',
    #                              related_name='studygp2')
    # studygp3 = models.ForeignKey(StudyGroup, models.DO_NOTHING, blank=True, null=True, db_column='studygp3',
    #                              related_name='studygp3')
    # studygp4 = models.ForeignKey(StudyGroup, models.DO_NOTHING, blank=True, null=True, db_column='studygp4',
    #                              related_name='studygp4')
    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's4_child_cp_rt'

    def __str__(self):
        return f'CRN: {self.parent_id} -- DxID: {self.s4_id}-- SIMID: {self.simid} -- RT Dose: {self.rtsitecode}'


class PrimaryDVH(models.Model):
    s4_dvh_id = models.AutoField(primary_key=True)
    s4_id = models.ForeignKey(S4RT, models.CASCADE, blank=False, null=False, db_column='s4_id', to_field='s4_id')
    str_type = models.ForeignKey(StrType, models.CASCADE, blank=False, null=True, db_column='str_type', to_field='code')
    str_name = models.ForeignKey(StrName, models.CASCADE, blank=False, null=True, db_column='str_name',
                                 to_field='code')  # As per AAPM report no 263 (Task Group 263) if taget otherwise as per FMAID
    target_class_base = models.ForeignKey(StrNameClassifierBase, models.CASCADE, blank=True, null=True,
                                          db_column='target_class_base',
                                          to_field='code')  # If structure is target. Use calssifier as per AAPM report no. 263 (Task Group 263)
    target_class_number = models.ForeignKey(StrNameClassifierNumber, models.CASCADE, blank=True, null=True,
                                            db_column='target_class_number',
                                            to_field='code')  # If structure is target. Use calssifier as per AAPM report no. 263 (Task Group 263)
    target_class_image = models.ForeignKey(StrNameClassifierImage, models.CASCADE, blank=True, null=True,
                                           db_column='target_class_image',
                                           to_field='code')  # If structure is target. Use calssifier as per AAPM report no. 263 (Task Group 263)
    target_class_dose = models.ForeignKey(StrNameClassifierDose, models.CASCADE, blank=True, null=True,
                                          db_column='target_class_dose',
                                          to_field='code')  # If structure is target. Use calssifier as per AAPM report no. 263 (Task Group 263)
    target_class_custom = models.ForeignKey(StrNameClassifierCustom, models.CASCADE, blank=True, null=True,
                                            db_column='target_class_custom',
                                            to_field='code')  # If structure is target. Use calssifier as per AAPM report no. 263 (Task Group 263)

    vol = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    parameters = models.ForeignKey(DVHParameters, models.CASCADE, blank=False, null=True,
                                   db_column='parameters',
                                   to_field='code')  # As per AAPM report no 263 (Task Group 263)
    value = models.DecimalField(max_digits=15, decimal_places=5, blank=False, null=True)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'primarydvh'

    def __str__(self):
        return f'CRN: {self.s4_id} -- StrType: {self.str_type}-- StrName: {self.str_name} -- Value: {self.value}'


class S7Assessment(models.Model):
    s7_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, to_field='crnumber',
                                  db_column='parent_id')
    s4_id = models.ForeignKey(S4RT, models.CASCADE, to_field='s4_id',
                              db_column='s4_id', blank=False, null=False)
    as_date = models.DateTimeField(blank=False, null=False)
    txstatus = models.CharField(max_length=45, blank=True, null=True)
    ecog = models.CharField(max_length=45, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fatigue = models.CharField(max_length=45, blank=True, null=True)
    apetite = models.CharField(max_length=45, blank=True, null=True)
    pain = models.CharField(max_length=45, blank=True, null=True)
    dermatitis = models.CharField(max_length=45, blank=True, null=True)
    skin_axilla = models.CharField(max_length=45, blank=True, null=True)
    skin_scf = models.CharField(max_length=45, blank=True, null=True)
    skin_imf = models.CharField(max_length=45, blank=True, null=True)
    skin_uoq = models.CharField(max_length=45, blank=True, null=True)
    skin_loq = models.CharField(max_length=45, blank=True, null=True)
    skin_uiq = models.CharField(max_length=45, blank=True, null=True)
    skin_liq = models.CharField(max_length=45, blank=True, null=True)
    mucositis = models.CharField(max_length=45, blank=True, null=True)
    esophagitis = models.CharField(max_length=45, blank=True, null=True)
    naus_vom = models.CharField(max_length=45, blank=True, null=True)
    cough = models.CharField(max_length=45, blank=True, null=True)
    pruritis = models.CharField(max_length=45, blank=True, null=True)
    dysphagia = models.CharField(max_length=45, blank=True, null=True)
    hiccups = models.CharField(max_length=45, blank=True, null=True)
    hoarseness = models.CharField(max_length=45, blank=True, null=True)
    vertigo = models.CharField(max_length=45, blank=True, null=True)
    conjunctivitis = models.CharField(max_length=45, blank=True, null=True)
    dryeye = models.CharField(max_length=45, blank=True, null=True)
    constipation = models.CharField(max_length=45, blank=True, null=True)
    diarrhea = models.CharField(max_length=45, blank=True, null=True)
    vomiting = models.CharField(max_length=45, blank=True, null=True)
    edemaLimbs = models.CharField(max_length=45, blank=True, null=True)
    fever = models.CharField(max_length=45, blank=True, null=True)
    gaitDisturbance = models.CharField(max_length=45, blank=True, null=True)
    localizedEdema = models.CharField(max_length=45, blank=True, null=True)
    malaise = models.CharField(max_length=45, blank=True, null=True)
    otitisexterna = models.CharField(max_length=45, blank=True, null=True)
    otitismedia = models.CharField(max_length=45, blank=True, null=True)
    papulopustularrash = models.CharField(max_length=45, blank=True, null=True)
    rashacneiform = models.CharField(max_length=45, blank=True, null=True)
    rashmaculpapular = models.CharField(max_length=45, blank=True, null=True)
    rashpustular = models.CharField(max_length=45, blank=True, null=True)
    pharyngitis = models.CharField(max_length=45, blank=True, null=True)
    tracheitis = models.CharField(max_length=45, blank=True, null=True)
    hypercalcemia = models.CharField(max_length=45, blank=True, null=True)
    hyperkalemia = models.CharField(max_length=45, blank=True, null=True)
    hypokalemia = models.CharField(max_length=45, blank=True, null=True)
    hypernatremia = models.CharField(max_length=45, blank=True, null=True)
    hypoalbuminemia = models.CharField(max_length=45, blank=True, null=True)
    hypocalcemia = models.CharField(max_length=45, blank=True, null=True)
    hyponatremia = models.CharField(max_length=45, blank=True, null=True)
    tls = models.CharField(max_length=45, blank=True, null=True)
    arthralgia = models.CharField(max_length=45, blank=True, null=True)
    bonepain = models.CharField(max_length=45, blank=True, null=True)
    trismus = models.CharField(max_length=45, blank=True, null=True)
    ataxia = models.CharField(max_length=45, blank=True, null=True)
    cognitivedisturbance = models.CharField(max_length=45, blank=True, null=True)
    concentration = models.CharField(max_length=45, blank=True, null=True)
    consciousness = models.CharField(max_length=45, blank=True, null=True)
    dysgeusia = models.CharField(max_length=45, blank=True, null=True)
    headache = models.CharField(max_length=45, blank=True, null=True)
    somnolence = models.CharField(max_length=45, blank=True, null=True)
    lethargy = models.CharField(max_length=45, blank=True, null=True)
    memoryimpairment = models.CharField(max_length=45, blank=True, null=True)
    radiculitis = models.CharField(max_length=45, blank=True, null=True)
    anxiety = models.CharField(max_length=45, blank=True, null=True)
    confusion = models.CharField(max_length=45, blank=True, null=True)
    depression = models.CharField(max_length=45, blank=True, null=True)
    insomnia = models.CharField(max_length=45, blank=True, null=True)
    hematuria = models.CharField(max_length=45, blank=True, null=True)
    aspiration = models.CharField(max_length=45, blank=True, null=True)
    epistaxis = models.CharField(max_length=45, blank=True, null=True)
    dyspnea = models.CharField(max_length=45, blank=True, null=True)
    laryngealedema = models.CharField(max_length=45, blank=True, null=True)
    pneumonitis = models.CharField(max_length=45, blank=True, null=True)
    pulmonaryfibrosis = models.CharField(max_length=45, blank=True, null=True)
    alopecia = models.CharField(max_length=45, blank=True, null=True)
    hotflashes = models.CharField(max_length=45, blank=True, null=True)
    anemia = models.CharField(max_length=45, blank=True, null=True)
    platelet = models.CharField(max_length=45, blank=True, null=True)
    leukopenia = models.CharField(max_length=45, blank=True, null=True)
    neutropenia = models.CharField(max_length=45, blank=True, null=True)

    symp1 = models.CharField(max_length=100, blank=True, null=True)
    symp2 = models.CharField(max_length=100, blank=True, null=True)
    symp3 = models.CharField(max_length=100, blank=True, null=True)
    symp4 = models.CharField(max_length=100, blank=True, null=True)
    symp5 = models.CharField(max_length=100, blank=True, null=True)
    symp6 = models.CharField(max_length=100, blank=True, null=True)
    symp7 = models.CharField(max_length=100, blank=True, null=True)

    symp1type = models.CharField(max_length=15, blank=True, null=True)
    symp2type = models.CharField(max_length=15, blank=True, null=True)
    symp3type = models.CharField(max_length=15, blank=True, null=True)
    symp4type = models.CharField(max_length=15, blank=True, null=True)
    symp5type = models.CharField(max_length=15, blank=True, null=True)
    symp6type = models.CharField(max_length=15, blank=True, null=True)
    symp7type = models.CharField(max_length=15, blank=True, null=True)

    drugrx1 = models.CharField(max_length=45, blank=True, null=True)
    drugrx2 = models.CharField(max_length=45, blank=True, null=True)
    drugrx3 = models.CharField(max_length=45, blank=True, null=True)
    drugrx4 = models.CharField(max_length=45, blank=True, null=True)
    drugrx5 = models.CharField(max_length=45, blank=True, null=True)
    drugrx6 = models.CharField(max_length=45, blank=True, null=True)

    rx1fx = models.CharField(max_length=15, blank=True, null=True)
    rx2fx = models.CharField(max_length=15, blank=True, null=True)
    rx3fx = models.CharField(max_length=15, blank=True, null=True)
    rx4fx = models.CharField(max_length=15, blank=True, null=True)
    rx5fx = models.CharField(max_length=15, blank=True, null=True)
    rx6fx = models.CharField(max_length=15, blank=True, null=True)

    rx1route = models.CharField(max_length=15, blank=True, null=True)
    rx2route = models.CharField(max_length=15, blank=True, null=True)
    rx3route = models.CharField(max_length=15, blank=True, null=True)
    rx4route = models.CharField(max_length=15, blank=True, null=True)
    rx5route = models.CharField(max_length=15, blank=True, null=True)
    rx6route = models.CharField(max_length=15, blank=True, null=True)

    rx1dur = models.IntegerField(blank=True, null=True)
    rx2dur = models.IntegerField(blank=True, null=True)
    rx3dur = models.IntegerField(blank=True, null=True)
    rx4dur = models.IntegerField(blank=True, null=True)
    rx5dur = models.IntegerField(blank=True, null=True)
    rx6dur = models.IntegerField(blank=True, null=True)

    rx1inst = models.CharField(max_length=100, blank=True, null=True)
    rx2inst = models.CharField(max_length=100, blank=True, null=True)
    rx3inst = models.CharField(max_length=100, blank=True, null=True)
    rx4inst = models.CharField(max_length=100, blank=True, null=True)
    rx5inst = models.CharField(max_length=100, blank=True, null=True)
    rx6inst = models.CharField(max_length=100, blank=True, null=True)

    rxdose1 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rxdose2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rxdose3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rxdose4 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rxdose5 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rxdose6 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    rxunit1 = models.CharField(max_length=10, blank=True, null=True)
    rxunit2 = models.CharField(max_length=10, blank=True, null=True)
    rxunit3 = models.CharField(max_length=10, blank=True, null=True)
    rxunit4 = models.CharField(max_length=10, blank=True, null=True)
    rxunit5 = models.CharField(max_length=10, blank=True, null=True)
    rxunit6 = models.CharField(max_length=10, blank=True, null=True)

    fxdone = models.IntegerField(blank=False, null=True)
    intervention1 = models.CharField(max_length=45, blank=True, null=True)
    intervention2 = models.CharField(max_length=45, blank=True, null=True)
    intervention3 = models.CharField(max_length=45, blank=True, null=True)
    intervention4 = models.CharField(max_length=45, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 's7_child_as'

    def __str__(self):
        return f'CRN: {self.parent_id} -- RTID: {self.s4_id} -- RTPK: {self.s7_id} -- RT ' \
               f'Dose: {self.as_date} -- Status: {self.txstatus}'


class AcuteToxicity(models.Model):
    s8_acutetox_id = models.AutoField(primary_key=True)
    s7_id = models.ForeignKey(S7Assessment, models.CASCADE, blank=False, null=False,
                              db_column='s7_id', to_field='s7_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    tox_system = models.CharField(max_length=255, blank=True, null=True)
    # tox_term = models.ForeignKey(CTCV5, models.CASCADE, blank=False, null=True,
    #                              db_column='tox_term', to_field='term')
    tox_term = models.CharField(max_length=255, blank=True, null=True)
    tox_grade = models.TextField()

    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'acute_toxicity'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FU_ID: {self.s7_id} -- ' \
               f'Symp: {self.tox_system} -- SympDur: {self.tox_term} -- Drug: {self.tox_grade}'


class S6Surgery(models.Model):
    s6_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=False, null=False,
                              db_column="s3_id", to_field="s3_id")
    sxunit = models.ForeignKey(Referredby, models.CASCADE, db_column='sxunit', blank=True, null=True, to_field='refby')
    admissiondate = models.DateTimeField(blank=True, null=True)
    sxdate = models.DateTimeField(blank=True, null=True)
    dischargedate = models.DateTimeField(blank=True, null=True)

    sxtype = models.ManyToManyField(SxCodes, blank=False)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's6_child_cp_sx'

    def __str__(self):
        return f'CRN: {self.parent_id} -- Name: {self.sxdate} {self.sxtype} -- Mobile: {self.sxunit}'


class S6HPE(models.Model):
    s6hpe_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s6_id = models.ForeignKey(S6Surgery, models.CASCADE, blank=False, null=False,
                              db_column="s6_id")
    hpedate = models.DateTimeField(blank=True, null=True)
    hpeno = models.CharField(max_length=45, blank=True, null=True)
    hpegrade = models.ForeignKey(BiopsyGrade, null=True, blank=True, on_delete=models.DO_NOTHING,
                                 db_column='hpegrade')
    icd_path_code = models.ForeignKey(HPE, null=True, blank=True, on_delete=models.DO_NOTHING,
                                      db_column='icd_path_code')

    pt = models.ForeignKey(ClinT, null=True, blank=True, on_delete=models.DO_NOTHING, db_column="pt")  # FK
    pn = models.ForeignKey(ClinN, null=True, blank=True, on_delete=models.DO_NOTHING, db_column="pn")  # FK
    pm = models.ForeignKey(ClinM, null=True, blank=True, on_delete=models.DO_NOTHING, db_column="pm")  # FK
    pstagegroup = models.ForeignKey(StageGroup, null=True, blank=True, on_delete=models.DO_NOTHING,
                                    db_column='pstagegroup')  # FK
    pajccedition = models.ForeignKey(AjccEdition, null=True, blank=True, on_delete=models.DO_NOTHING,
                                     db_column='pajccedition')  # FK

    gleasonsp = models.IntegerField(blank=True, null=True)
    gleasonss = models.IntegerField(blank=True, null=True)
    gleasonst = models.IntegerField(blank=True, null=True)
    gleasons = models.IntegerField(blank=True, null=True)
    psa_level = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    psa_date = models.DateTimeField(blank=True, null=True)

    tumorsized1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tumorsized2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tumorsized3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    nrl1 = models.IntegerField(blank=True, null=True)
    npl1 = models.IntegerField(blank=True, null=True)
    nrl2 = models.IntegerField(blank=True, null=True)
    npl2 = models.IntegerField(blank=True, null=True)
    nrl3 = models.IntegerField(blank=True, null=True)
    npl3 = models.IntegerField(blank=True, null=True)
    nrl4 = models.IntegerField(blank=True, null=True)
    npl4 = models.IntegerField(blank=True, null=True)
    nrl5 = models.IntegerField(blank=True, null=True)
    npl5 = models.IntegerField(blank=True, null=True)
    nrl6 = models.IntegerField(blank=True, null=True)
    npl6 = models.IntegerField(blank=True, null=True)
    nrl7 = models.IntegerField(blank=True, null=True)
    npl7 = models.IntegerField(blank=True, null=True)
    nrl8 = models.IntegerField(blank=True, null=True)
    npl8 = models.IntegerField(blank=True, null=True)
    nrl9 = models.IntegerField(blank=True, null=True)
    npl9 = models.IntegerField(blank=True, null=True)
    nrl10 = models.IntegerField(blank=True, null=True)
    npl10 = models.IntegerField(blank=True, null=True)
    nrl11 = models.IntegerField(blank=True, null=True)
    npl11 = models.IntegerField(blank=True, null=True)
    nrl12 = models.IntegerField(blank=True, null=True)
    npl12 = models.IntegerField(blank=True, null=True)
    nodesr = models.IntegerField(blank=True, null=True)
    nodesp = models.IntegerField(blank=True, null=True)

    textension = models.CharField(max_length=100, blank=True, null=True)
    lvi_vi = models.CharField(max_length=45, blank=True, null=True)
    pni = models.CharField(max_length=45, blank=True, null=True)
    ene = models.CharField(max_length=45, blank=True, null=True)
    margins = models.CharField(max_length=45, blank=True, null=True)
    marginb = models.CharField(max_length=45, blank=True, null=True)
    marginv = models.CharField(max_length=45, blank=True, null=True)
    marginp = models.CharField(max_length=45, blank=True, null=True)
    marginpp = models.CharField(max_length=45, blank=True, null=True)
    marginvp = models.CharField(max_length=45, blank=True, null=True)
    marginprox = models.CharField(max_length=45, blank=True, null=True)
    margindist = models.CharField(max_length=45, blank=True, null=True)
    margincircum = models.CharField(max_length=45, blank=True, null=True)
    marginmedial = models.CharField(max_length=45, blank=True, null=True)
    marginlateral = models.CharField(max_length=45, blank=True, null=True)

    er = models.CharField(max_length=45, blank=True, null=True)
    pr = models.CharField(max_length=45, blank=True, null=True)
    her2neu = models.CharField(max_length=45, blank=True, null=True)
    braca1 = models.CharField(max_length=45, blank=True, null=True)
    braca2 = models.CharField(max_length=45, blank=True, null=True)
    egfr = models.CharField(max_length=45, blank=True, null=True)
    alk = models.CharField(max_length=45, blank=True, null=True)
    ros = models.CharField(max_length=45, blank=True, null=True)
    pdl1 = models.CharField(max_length=45, blank=True, null=True)
    pdl1_val = models.IntegerField(blank=True, null=True)
    braf = models.CharField(max_length=45, blank=True, null=True)
    met = models.CharField(max_length=45, blank=True, null=True)
    ret = models.CharField(max_length=45, blank=True, null=True)
    hpv = models.CharField(max_length=45, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 's6_child_cp_sxhpe'

    def __str__(self):
        return f'CRN: {self.parent_id} -- Sx ID: {self.s6_id} -- Histopath: {self.icd_path_code} -- Date: {self.hpedate}'


# Have to DISCARD THIS TABLE LATER ON
class S5Chemo(models.Model):
    s5_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=False, null=False,
                              db_column="s3_id", to_field="s3_id", related_name="ch_careplan_id")

    chemo_protocol = models.ForeignKey(ChemoProtocolNew, models.DO_NOTHING, blank=True, null=True,
                                       db_column='chemo_protocol_id', to_field='id')
    cycleno = models.IntegerField(blank=True, null=True)
    chemo_day = models.CharField(max_length=45, blank=True, null=True)
    chemodate = models.DateTimeField(blank=True, null=True)
    unit = models.ForeignKey(Referredby, models.CASCADE, db_column='unit', blank=True, null=True, to_field='refby')

    drug1 = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug1', blank=True, null=True,
                              related_name='drug1')
    d1dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sdate1 = models.DateTimeField(blank=True, null=True)
    fdate1 = models.DateTimeField(blank=True, null=True)

    drug2 = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug2', blank=True, null=True,
                              related_name='drug2')
    d2dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sdate2 = models.DateTimeField(blank=True, null=True)
    fdate2 = models.DateTimeField(blank=True, null=True)

    drug3 = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug3', blank=True, null=True,
                              related_name='drug3')
    d3dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sdate3 = models.DateTimeField(blank=True, null=True)
    fdate3 = models.DateTimeField(blank=True, null=True)

    drug4 = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug4', blank=True, null=True,
                              related_name='drug4')
    d4dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sdate4 = models.DateTimeField(blank=True, null=True)
    fdate4 = models.DateTimeField(blank=True, null=True)

    drug5 = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug5', blank=True, null=True,
                              related_name='drug5')
    d5dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sdate5 = models.DateTimeField(blank=True, null=True)
    fdate5 = models.DateTimeField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's5_child_cp_ch'  ##


class S5ChemoProtocol(models.Model):
    s5_protocol_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=False, null=False,
                              db_column="s3_id", to_field="s3_id")
    protocol_date = models.DateTimeField(blank=True, null=True)
    protocol_end_date = models.DateTimeField(blank=True, null=True)

    chemo_protocol = models.ForeignKey(ChemoProtocolNew, models.DO_NOTHING, blank=True, null=True,
                                       db_column='chemo_protocol', to_field='id')
    chemo_cycles = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(Referredby, models.CASCADE, db_column='unit', blank=True, null=True, to_field='refby')

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's5_child_cp_ch_protocol'


class S5ChemoDrugs(models.Model):
    ch_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s5_protocol_id = models.ForeignKey(S5ChemoProtocol, models.CASCADE, blank=False, null=False,
                                       db_column="s5_protocol_id", to_field="s5_protocol_id")
    cycleno = models.IntegerField(blank=True, null=True)
    chemo_day = models.CharField(max_length=45, blank=True, null=True)
    chemodate = models.DateTimeField(blank=True, null=True)

    drug = models.ForeignKey(ChemoDrugs, models.CASCADE, db_column='drug', blank=False, null=True)
    dose = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    measuring_unit = models.CharField(max_length=45, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 's5_child_cp_ch_drugs'


class S8FUP(models.Model):
    s8_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s2_id = models.ForeignKey(S2Diagnosis, models.CASCADE, blank=True, null=True,
                              db_column='s2_id', to_field='s2_id')
    s3_id = models.ForeignKey(S3CarePlan, models.CASCADE, blank=True, null=True,
                              db_column="s3_id", to_field="s3_id")
    visitdate = models.DateTimeField(blank=False, null=False)
    visittype = models.ManyToManyField(FollowupVisitsType, blank=False)
    visitaction = models.ForeignKey(FollowupActions, models.CASCADE, blank=False, null=False, db_column='visitactions',
                                    to_field='code')
    Weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    PerfStatus = models.CharField(max_length=45, blank=True, null=True)
    Nextvisit = models.DateTimeField(blank=True, null=True)
    RecordRecc = models.CharField(max_length=45, blank=True, null=True)
    LRstatus = models.CharField(max_length=45, blank=True, null=True)
    RRstatus = models.CharField(max_length=45, blank=True, null=True)
    DMstatus = models.CharField(max_length=45, blank=True, null=True)
    Death = models.CharField(max_length=45, blank=True, null=True)
    CauseDeath = models.CharField(max_length=45, blank=True, null=True)
    Datedeath = models.DateTimeField(blank=True, null=True)
    Notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 's8_child_fup'

    def __str__(self):
        return f'CRN: {self.parent_id} -- DxID: {self.s2_id} -- Mx_ID: {self.s3_id} -- Date: {self.visitdate}'


class LateToxicity(models.Model):
    s8_latetox_id = models.AutoField(primary_key=True)
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=False, null=False,
                              db_column='s8_id', to_field='s8_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    toxtype = models.CharField(max_length=255, blank=False, null=True)
    toxgrade = models.CharField(max_length=255, blank=True, null=True)
    toxdetails = models.TextField()  # duration in days
    drug_name = models.CharField(max_length=255, blank=True, null=True)
    dosage = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    route = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)  # duration in days
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'late_toxicity'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FU_ID: {self.s8_id} -- ' \
               f'Symp: {self.toxtype} -- SympDur: {self.toxgrade} -- Drug: {self.drug_name}'


class Prescription(models.Model):
    s8_prescription_id = models.AutoField(primary_key=True)
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=True, null=True,
                              db_column='s8_id', to_field='s8_id')
    s7_id = models.ForeignKey(S7Assessment, models.CASCADE, blank=True, null=True,
                              db_column='s7_id', to_field='s7_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    symptoms = models.CharField(max_length=255, blank=False, null=True)
    symptoms_type = models.CharField(max_length=255, blank=True, null=True)
    symp_duration = models.IntegerField()  # duration in days
    drug_name = models.CharField(max_length=255, blank=True, null=True)
    dosage = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    route = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)  # duration in days
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'prescription'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FU_ID: {self.s8_id} -- Symp: {self.symptoms} -- SympDur: {self.symp_duration}'


class InvestigationsImaging(models.Model):
    s8_imaging_id = models.AutoField(primary_key=True)
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=True, null=True,
                              db_column='s8_id', to_field='s8_id')
    s7_id = models.ForeignKey(S7Assessment, models.CASCADE, blank=True, null=True,
                              db_column='s7_id', to_field='s7_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    imaging_date = models.DateTimeField(blank=False, null=False)
    imaging_type = models.ForeignKey(ImagingType, null=True, blank=False, on_delete=models.DO_NOTHING,
                                     db_column='imaging_type')  # CT, MRI, X-Ray, Ultrasound, etc
    imaging_location = models.ForeignKey(ImageLocation, models.CASCADE, blank=True, null=True,
                                         db_column='imaging_location', to_field='id')
    imaging_result = models.ForeignKey(ImagingResult, models.CASCADE, blank=False, null=True,
                                       db_column='imaging_result', to_field='id')
    imaging_result_details = models.TextField(blank=True, null=True)
    lab_name = models.ForeignKey(LabName, models.CASCADE, blank=True, null=True,
                                 db_column='lab_name', to_field='id')
    lab_contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # image = models.FileField(upload_to='images/') # In future we have to provide options for storing images
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'inv_img'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FUID: {self.s8_id} -- Date: {self.imaging_date} -- Type: {self.imaging_type}'


class InvestigationsLabs(models.Model):
    s8_labs_id = models.AutoField(primary_key=True)
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=True, null=True,
                              db_column='s8_id', to_field='s8_id')
    s7_id = models.ForeignKey(S7Assessment, models.CASCADE, blank=True, null=True,
                              db_column='s7_id', to_field='s7_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    test_name = models.CharField(max_length=255, blank=False, null=True)  # CBC, ESR, CRP, Tumor markers, etc
    test_date = models.DateField(blank=True, null=True)
    test_result = models.CharField(max_length=255, blank=False, null=True)
    test_result_details = models.TextField(blank=True, null=True)
    test_unit = models.CharField(max_length=255, blank=True, null=True)
    normal_range_min = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    normal_range_max = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    lab_name = models.CharField(max_length=255, blank=True, null=True)
    lab_contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cancer_related = models.BooleanField(
        default=False)  # True or False
    # image = models.FileField(upload_to='images/')
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'inv_labs'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FUID: {self.s8_id} -- Date: {self.test_date} -- Type: {self.test_name}'


class InvestigationsPath(models.Model):
    s8_path_id = models.AutoField(primary_key=True)
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=True, null=True,
                              db_column='s8_id', to_field='s8_id')
    s7_id = models.ForeignKey(S7Assessment, models.CASCADE, blank=True, null=True,
                              db_column='s7_id', to_field='s7_id')
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    path_type = models.CharField(max_length=255, blank=False,
                                 null=True)  # Fine needle aspiration, Ascitic fluid, Pleural Fluid, core needle biopsy, excisional biopsy, etc
    guided_by = models.CharField(max_length=255, blank=True,
                                 null=True)  # USG, CT, MRI, other investigations
    biopsy_date = models.DateField(blank=True, null=True)
    biopsy_location = models.ForeignKey(FMAID, models.CASCADE, blank=True, null=True, db_column='biopsy_location',
                                        to_field='fma_id')
    biopsy_result = models.ForeignKey(HPE, models.CASCADE, blank=False, null=True, db_column='biopsy_result')
    biopsy_result_details = models.TextField(blank=True, null=True)
    lab_name = models.CharField(max_length=255, blank=True, null=True)
    lab_contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # image = models.FileField(upload_to='images/')
    molecular_profile = models.TextField(blank=True, null=True)  # Done or not done
    molecular_profile_status = models.TextField(blank=True, null=True)  # Awaited, avialbale
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'inv_path'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FUID: {self.s8_id} -- Date: {self.biopsy_date} -- Result: {self.biopsy_result}'


class InvestigationsMolecular(models.Model):
    mol_id = models.AutoField(primary_key=True)
    s8_path_id = models.ForeignKey(InvestigationsPath, on_delete=models.CASCADE, blank=False, null=False,
                                   db_column='s8_path_id')
    parent_id = models.ForeignKey(S1ParentMain, on_delete=models.CASCADE, blank=False, null=False,
                                  db_column='parent_id',
                                  to_field='crnumber')
    mol_type = models.CharField(max_length=255, blank=False,
                                null=True)  # Test name - EGFR, ALK, ROS
    mol_result = models.CharField(max_length=255, blank=False,
                                  null=True)  # Yes, No, Unknown Significance
    mol_value = models.CharField(max_length=255, blank=True,
                                 null=True)  # Value if applicable
    mol_unit = models.CharField(max_length=255, blank=True,
                                null=True)  # If value then measuring unit of that value

    lab_name = models.CharField(max_length=255, blank=True, null=True)
    lab_contact = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'inv_molecular'

    def __str__(self):
        return f'CRN: {self.parent_id} -- FUID: {self.s8_path_id} -- Date: {self.mol_type} -- Result: {self.mol_result}'


# PFT Model
class PFTDetails(models.Model):
    pft_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, blank=False, null=False,
                              db_column='s8_id', to_field='s8_id')
    StudyDate = models.DateTimeField(blank=False, null=False)
    DLCO = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    DLCOpred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    DLCO_VA = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    DLCO_VApred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    prFEV1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    prFEV1pred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    poFEV1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    poFEV1pred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    FEV1_change = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    prFEV1_FVC = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, db_column='prFEV1/FVC')
    prFEV1_FVCpred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                         db_column='prFEV1/FVCpred')
    poFEV1_FVC = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, db_column='poFEV1/FVC')
    poFEV1_FVCpred = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                         db_column='poFEV1/FVCpred')
    FEV1_FVC_change = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                          db_column='FEV1/FVC_change')
    Notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New

    class Meta:
        db_table = 'pftdetails'


# Cardiac Markers
class CardiacMarkers(models.Model):
    cm_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(S1ParentMain, models.CASCADE, blank=False, null=False, db_column='parent_id',
                                  to_field='crnumber')
    s8_id = models.ForeignKey(S8FUP, models.CASCADE, to_field='s8_id',
                              db_column='s8_id', blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    trop_i = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    hs_crp = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    nt_probnp = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    rtstartdate = models.DateTimeField(blank=True, null=True)
    planned_fr = models.IntegerField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    last_updated = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=45, blank=True, null=True)  # New
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cardiacmarkers'
