from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.forms.formsets import formset_factory
from .models import S1ParentMain, Comorbidity, PreSimulation, S2Diagnosis, S3CarePlan, Simulation, S4RT, S7Assessment, \
    S6Surgery, S6HPE, S5Chemo, S8FUP, PrimaryDVH, PFTDetails, CardiacMarkers, Site, RTTech, StudyGroup, ICDMainSites, \
    InvestigationsImaging, Prescription

from .options import (GENDER, YES_NO, SMOKE_FREQ, SMOKE_DUR, PS, INTENT_CHOICES, CP_CHOICES,
                      DOC_TYPE_CHOICES, RT_LATE_TOXICITY, visit_choices, deathcause_choices,
                      frequency_choices, unit_choices, route_choices, drugs_choices,
                      symp_type_choices, txstatus_choices, toxicity_choices)


# Created class to use date time picker
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
class DateInput(forms.DateInput):
    input_type = 'date'


class SearchCRN(forms.Form):
    s_crnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))


class S1PatientRegForm(ModelForm):
    reg_date = forms.DateTimeField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = S1ParentMain
        email = forms.EmailField()
        fields = ['crnumber', 'first_name', 'last_name', 'age', 'weight', 'height',
                  'reg_date', 'gender', 'ecog', 'doc_type', 'doc_id', 'city', 'smoking', 'smoking_status',
                  'smoking_volume', 'comorbidity', 'email', 'mobile', 'notes', 'user', 'updated_by']

        widgets = {
            'crnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'reg_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(choices=GENDER, attrs={'class': 'form-control'}),
            'ecog': forms.Select(choices=PS, attrs={'class': 'form-control'}),
            'doc_type': forms.Select(choices=DOC_TYPE_CHOICES, attrs={'class': 'form-control'}),
            'doc_id': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'smoking': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'smoking_status': forms.Select(choices=SMOKE_DUR, attrs={'class': 'form-control'}),
            'smoking_volume': forms.Select(choices=SMOKE_FREQ, attrs={'class': 'form-control'}),
            'comorbidity': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 12,
                                           'placeholder': "You can paste all your  important clinical notes"}),
        }

    def clean_reg_date(self, *args, **kwargs):
        date = self.cleaned_data['reg_date']
        if date > timezone.now():
            raise forms.ValidationError("Registration Date cannot be later than today.")
        return date


class PreSimulationForm(ModelForm):
    class Meta:
        model = PreSimulation
        fields = ["presimparent", 's3_id', "day1date", "ul_amp_d1", "ll_amp_d1", "average_amp_d1",
                  "ahd_d1", "al_d1", "d1remarks", "assessedby_day1", "day1status", "day2date",
                  "ul_amp_d2", "ll_amp_d2", "average_amp_d2", "ahd_d2", "al_d2", "d2remarks",
                  "assessedby_day2", "day2status", "day3date", "ul_amp_d3", "ll_amp_d3",
                  "average_amp_d3", "ahd_d3", "al_d3", "d3remarks", "assessedby_day3",
                  "day3status", "day4date", "ul_amp_d4", "ll_amp_d4", "average_amp_d4",
                  "ahd_d4", "al_d4", "d4remarks", "assessedby_day4", "day4status", "day5date",
                  "ul_amp_d5", "ll_amp_d5", "average_amp_d5", "ahd_d5", "al_d5", "d5remarks",
                  "assessedby_day5", "day5status", "xray_status", "final_status", "final_remarks",
                  "user", "updated_by", "last_updated", ]
        widgets = {
            'presimparent': forms.TextInput(attrs={'class': 'form-control'}),
            'day1date': DateInput(attrs={'class': 'form-control'}),
            'ul_amp_d1': forms.NumberInput(attrs={'class': 'form-control'}),
            'll_amp_d1': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_amp_d1': forms.NumberInput(attrs={'class': 'form-control'}),
            'ahd_d1': forms.NumberInput(attrs={'class': 'form-control'}),
            'd1remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assessedby_day1': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'day1status': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'day2date': DateInput(attrs={'class': 'form-control'}),
            'ul_amp_d2': forms.NumberInput(attrs={'class': 'form-control'}),
            'll_amp_d2': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_amp_d2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ahd_d2': forms.NumberInput(attrs={'class': 'form-control'}),
            'd2remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assessedby_day2': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'day2status': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'day3date': DateInput(attrs={'class': 'form-control'}),
            'ul_amp_d3': forms.NumberInput(attrs={'class': 'form-control'}),
            'll_amp_d3': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_amp_d3': forms.NumberInput(attrs={'class': 'form-control'}),
            'ahd_d3': forms.NumberInput(attrs={'class': 'form-control'}),
            'd3remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assessedby_day3': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'day3status': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'day4date': DateInput(attrs={'class': 'form-control'}),
            'ul_amp_d4': forms.NumberInput(attrs={'class': 'form-control'}),
            'll_amp_d4': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_amp_d4': forms.NumberInput(attrs={'class': 'form-control'}),
            'ahd_d4': forms.NumberInput(attrs={'class': 'form-control'}),
            'd4remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assessedby_day4': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'day4status': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'day5date': DateInput(attrs={'class': 'form-control'}),
            'ul_amp_d5': forms.NumberInput(attrs={'class': 'form-control'}),
            'll_amp_d5': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_amp_d5': forms.NumberInput(attrs={'class': 'form-control'}),
            'ahd_d5': forms.NumberInput(attrs={'class': 'form-control'}),
            'd5remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assessedby_day5': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'day5status': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'final_status': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'final_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class S2DiagnosisForm(ModelForm):
    class Meta:
        model = S2Diagnosis
        fields = "__all__"
        exclude = ["s2_id", "last_updated"]
        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'diagnosis': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'laterality': forms.Select(choices=[("NA", "NA"),
                                                ("Right", "Right"),
                                                ("Left", "Left"),
                                                ("Central", "Central")],
                                       attrs={'class': 'form-control'}),
            'dx_type': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'icd_main_topo': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'icd_topo_code': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'icd_path_code': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'dx_date': DateInput(attrs={'class': 'form-control'}),
            'biopsy_no': forms.TextInput(attrs={'class': 'form-control'}),
            'biopsy_date': DateInput(attrs={'class': 'form-control'}),
            'biopsy': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'biopsy_grade': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'confirmed_by': forms.Select(choices=[("NA", "NA"),
                                                  ("FNAC", "FNAC"),
                                                  ("Biopsy", "Biopsy"),
                                                  ("Imaging", "Imaging")], attrs={'class': 'form-control'}),
            'c_t': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'c_n': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'c_m': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'c_stage_group': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'c_ajcc_edition': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'er': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'pr': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'her2neu': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'braca1': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'braca2': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'egfr': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'alk': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'ros': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'pdl_1': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'pdl_1_levels': forms.TextInput(attrs={'class': 'form-control'}),
            'braf': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'met': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'ret': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'hpv': forms.Select(choices=YES_NO, attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

        }


class S3CarePlanForm(ModelForm):
    startdate = forms.DateTimeField(widget=DateInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = S3CarePlan
        fields = "__all__"
        exclude = ["s3_id", "last_updated"]
        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control'}),
            's2_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'hidden': True}),
            'mcourse': forms.TextInput(attrs={'class': 'form-control'}),
            # 'startdate': DateInput(attrs={'class': 'form-control', 'required': True}),
            'enddate': DateInput(attrs={'class': 'form-control'}),
            'intent': forms.Select(choices=INTENT_CHOICES, attrs={'class': 'form-control'}),
            'radiotherapy': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'surgery': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'chemotherapy': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'brachytherapy': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'hormone': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'immunotherapy': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'bmt': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'targettherapy': forms.Select(choices=CP_CHOICES, attrs={'class': 'form-control'}),
            'studyprotocol': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SimulationForm(ModelForm):
    class Meta:
        model = Simulation
        fields = ['simparent', 'presimid', 's2_id', 's3_id', 'name', 'simdate', 'simnotes',
                  'impdate', 'impnotes', 'initialstatus', 'futureplan', 'site', 'icdmainsite',
                  'technique', 'intent', 'volumes', 'dosephase1', 'fxphase1', 'dosephase2',
                  'fxphase2', 'dosephase3', 'fxphase3', 'dosephase4', 'fxphase4', 'totaldose', 'totalfractions',
                  'assignedto',
                  'remarks', 'tentativecompletiondate',
                  'actualcompletiondate', 'as_date', 'donefr', 'user', 'updated_by', 'send_mail']
        widgets = {
            'simparent': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'simdate': DateInput(attrs={'class': 'form-control'}),
            'simnotes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'impdate': DateInput(attrs={'class': 'form-control'}),
            'impnotes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'initialstatus': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'futureplan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'site': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'icdmainsite': forms.SelectMultiple(choices=[], attrs={'class': 'form-control'}),
            'technique': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'intent': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'volumes': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'dosephase1': forms.NumberInput(attrs={'class': 'form-control'}),
            'fxphase1': forms.NumberInput(attrs={'class': 'form-control'}),
            'dosephase2': forms.NumberInput(attrs={'class': 'form-control'}),
            'fxphase2': forms.NumberInput(attrs={'class': 'form-control'}),
            'dosephase3': forms.NumberInput(attrs={'class': 'form-control'}),
            'fxphase3': forms.NumberInput(attrs={'class': 'form-control'}),
            'dosephase4': forms.NumberInput(attrs={'class': 'form-control'}),
            'fxphase4': forms.NumberInput(attrs={'class': 'form-control'}),
            'totaldose': forms.NumberInput(attrs={'class': 'form-control'}),
            'totalfractions': forms.NumberInput(attrs={'class': 'form-control'}),
            'assignedto': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tentativecompletiondate': DateInput(attrs={'class': 'form-control', 'readonly': True}),
            'actualcompletiondate': DateInput(attrs={'class': 'form-control'}),
            'as_date': DateInput(attrs={'class': 'form-control', 'readonly': True}),
            'donefr': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'presimid': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            's2_id': forms.Select(choices=[], attrs={'class': 'form-control'}),
            's3_id': forms.Select(choices=[], attrs={'class': 'form-control'}),
        }


class S4RTForm(ModelForm):
    class Meta:
        model = S4RT
        fields = "__all__"
        exclude = ["s4_id", "last_updated"]
        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control'}),
            's3_id': forms.NumberInput(attrs={'class': 'form-control', 'hidden': True}),
            'simid': forms.Select(attrs={'class': 'form-control'}),
            'rtindication': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'simdate': DateInput(attrs={'class': 'form-control'}),
            'rtsite_main': forms.SelectMultiple(attrs={'class': 'form-control'}),

            'rtsitecode': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'rtdose1': forms.NumberInput(attrs={'class': 'form-control'}),
            'rtdosefr1': forms.NumberInput(attrs={'class': 'form-control'}),
            'modality1': forms.Select(choices=[("", ""),
                                               ("Photons", "Photons"),
                                               ("Electrons", "Electrons"),
                                               ("Protons", "Protons")],
                                      attrs={'class': 'form-control'}),
            'tech1': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'rtdose2': forms.NumberInput(attrs={'class': 'form-control'}),
            'rtdosefr2': forms.NumberInput(attrs={'class': 'form-control'}),
            'modality2': forms.Select(choices=[("", ""),
                                               ("Photons", "Photons"),
                                               ("Electrons", "Electrons"),
                                               ("Protons", "Protons")],
                                      attrs={'class': 'form-control'}),
            'tech2': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'rtdose3': forms.NumberInput(attrs={'class': 'form-control'}),
            'rtdosefr3': forms.NumberInput(attrs={'class': 'form-control'}),
            'modality3': forms.Select(choices=[("", ""),
                                               ("Photons", "Photons"),
                                               ("Electrons", "Electrons"),
                                               ("Protons", "Protons")],
                                      attrs={'class': 'form-control'}),
            'tech3': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'rtdose4': forms.NumberInput(attrs={'class': 'form-control'}),
            'rtdosefr4': forms.NumberInput(attrs={'class': 'form-control'}),
            'modality4': forms.Select(choices=[("", ""),
                                               ("Photons", "Photons"),
                                               ("Electrons", "Electrons"),
                                               ("Protons", "Protons")],
                                      attrs={'class': 'form-control'}),
            'tech4': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'rtstartdate': DateInput(attrs={'class': 'form-control'}),
            'rtfinishdate': DateInput(attrs={'class': 'form-control'}),
            'rtmachine': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'rtstatus': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'institution': forms.Select(choices=[('RGCIRC', 'RGCIRC'),
                                                 ('BHMRC', 'BHMRC'),
                                                 ('Apollo Delhi', 'Apollo Delhi')],
                                        attrs={'class': 'form-control'}),
            'studygp': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'studygp2': forms.Select(choices=[], attrs={'class': 'form-control'}),
            # 'studygp3': forms.Select(choices=[], attrs={'class': 'form-control'}),
            # 'studygp4': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class S6SurgeryForm(ModelForm):
    class Meta:
        model = S6Surgery
        fields = "__all__"
        exclude = ["s6_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control'}),
            's3_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'sxunit': forms.Select(attrs={'class': 'form-control'}),
            'admissiondate': DateInput(attrs={'class': 'form-control'}),
            'sxdate': DateInput(attrs={'class': 'form-control'}),
            'dischargedate': DateInput(attrs={'class': 'form-control'}),
            'sxtype': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class S6HPEForm(ModelForm):
    class Meta:
        model = S6HPE
        fields = "__all__"
        exclude = ["s6hpe_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control'}),
            's6_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'hpedate': DateInput(attrs={'class': 'form-control'}),
            'hpeno': forms.TextInput(attrs={'class': 'form-control'}),
            'hpegrade': forms.Select(attrs={'class': 'form-control'}),
            'icd_path_code': forms.Select(attrs={'class': 'form-control'}),
            'pt': forms.Select(attrs={'class': 'form-control'}),
            'pn': forms.Select(attrs={'class': 'form-control'}),
            'pm': forms.Select(attrs={'class': 'form-control'}),
            'pstagegroup': forms.Select(attrs={'class': 'form-control'}),
            'pajccedition': forms.Select(attrs={'class': 'form-control'}),
            'gleasonsp': forms.NumberInput(attrs={'class': 'form-control'}),
            'gleasonss': forms.NumberInput(attrs={'class': 'form-control'}),
            'gleasonst': forms.NumberInput(attrs={'class': 'form-control'}),
            'gleasons': forms.NumberInput(attrs={'class': 'form-control'}),
            'psa_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'psa_date': DateInput(attrs={'class': 'form-control'}),
            'tumorsized1': forms.NumberInput(attrs={'class': 'form-control'}),
            'tumorsized2': forms.NumberInput(attrs={'class': 'form-control'}),
            'tumorsized3': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl1': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl1': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl2': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl2': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl3': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl3': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl4': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl4': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl5': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl5': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl6': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl6': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl7': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl7': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl8': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl8': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl9': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl9': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl10': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl10': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl11': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl11': forms.NumberInput(attrs={'class': 'form-control'}),
            'nrl12': forms.NumberInput(attrs={'class': 'form-control'}),
            'npl12': forms.NumberInput(attrs={'class': 'form-control'}),
            'nodesr': forms.NumberInput(attrs={'class': 'form-control'}),
            'nodesp': forms.NumberInput(attrs={'class': 'form-control'}),
            'lvi_vi': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'pni': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'ene': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'margins': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginb': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginv': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginp': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginpp': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginvp': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginprox': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'margindist': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'margincircum': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginmedial': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'marginlateral': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'er': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'pr': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'her2neu': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'braca1': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'braca2': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'egfr': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'alk': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'ros': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'pdl1': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'pdl1_val': forms.NumberInput(attrs={'class': 'form-control'}),
            'braf': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'met': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'ret': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'hpv': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class S5ChemoForm(ModelForm):
    class Meta:
        model = S5Chemo
        fields = "__all__"
        exclude = ["s4_id", "last_updated"]
        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's3_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'chemo_protocol': forms.Select(attrs={'class': 'form-control'}),
            'cycleno': forms.NumberInput(attrs={'class': 'form-control'}),
            'chemo_day': forms.TextInput(attrs={'class': 'form-control'}),
            'chemodate': DateInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'drug1': forms.Select(attrs={'class': 'form-control'}),
            'd1dose': forms.NumberInput(attrs={'class': 'form-control'}),
            'sdate1': DateInput(attrs={'class': 'form-control'}),
            'fdate1': DateInput(attrs={'class': 'form-control'}),
            'drug2': forms.Select(attrs={'class': 'form-control'}),
            'd2dose': forms.NumberInput(attrs={'class': 'form-control'}),
            'sdate2': DateInput(attrs={'class': 'form-control'}),
            'fdate2': DateInput(attrs={'class': 'form-control'}),
            'drug3': forms.Select(attrs={'class': 'form-control'}),
            'd3dose': forms.NumberInput(attrs={'class': 'form-control'}),
            'sdate3': DateInput(attrs={'class': 'form-control'}),
            'fdate3': DateInput(attrs={'class': 'form-control'}),
            'drug4': forms.Select(attrs={'class': 'form-control'}),
            'd4dose': forms.NumberInput(attrs={'class': 'form-control'}),
            'sdate4': DateInput(attrs={'class': 'form-control'}),
            'fdate4': DateInput(attrs={'class': 'form-control'}),
            'drug5': forms.Select(attrs={'class': 'form-control'}),
            'd5dose': forms.NumberInput(attrs={'class': 'form-control'}),
            'sdate5': DateInput(attrs={'class': 'form-control'}),
            'fdate5': DateInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class S7AssessmentForm(ModelForm):
    class Meta:
        model = S7Assessment
        fields = "__all__"
        exclude = ["s7_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's4_id': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'simid': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'as_date': DateInput(attrs={'class': 'form-control'}),
            'txstatus': forms.Select(attrs={'class': 'form-control'}, choices=txstatus_choices),
            'ecog': forms.Select(attrs={'class': 'form-control'}, choices=PS),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'fatigue': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'apetite': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'pain': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'dermatitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_axilla': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_scf': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_imf': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_uoq': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_loq': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_uiq': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'skin_liq': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'mucositis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'esophagitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'naus_vom': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'cough': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'pruritis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'dysphagia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hiccups': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hoarseness': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'vertigo': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'conjunctivitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'dryeye': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'constipation': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'diarrhea': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'vomiting': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'edemaLimbs': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'fever': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'gaitDisturbance': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'localizedEdema': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'malaise': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'otitisexterna': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'otitismedia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'papulopustularrash': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'rashacneiform': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'rashmaculpapular': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'rashpustular': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'pharyngitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'tracheitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hypercalcemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hyperkalemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hypokalemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hypernatremia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hypoalbuminemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hypocalcemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hyponatremia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'tls': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'arthralgia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'bonepain': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'trismus': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'ataxia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'cognitivedisturbance': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'concentration': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'consciousness': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'dysgeusia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'headache': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'somnolence': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'lethargy': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'memoryimpairment': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'radiculitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'anxiety': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'confusion': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'depression': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'insomnia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hematuria': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'aspiration': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'epistaxis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'dyspnea': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'laryngealedema': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'pneumonitis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'pulmonaryfibrosis': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'alopecia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'hotflashes': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'anemia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'platelet': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'leukopenia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'neutropenia': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'symp1': forms.TextInput(attrs={'class': 'form-control'}),
            'symp2': forms.TextInput(attrs={'class': 'form-control'}),
            'symp3': forms.TextInput(attrs={'class': 'form-control'}),
            'symp4': forms.TextInput(attrs={'class': 'form-control'}),
            'symp5': forms.TextInput(attrs={'class': 'form-control'}),
            'symp6': forms.TextInput(attrs={'class': 'form-control'}),
            'symp7': forms.TextInput(attrs={'class': 'form-control'}),
            'symp1type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp2type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp3type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp4type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp5type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp6type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'symp7type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'drugrx1': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'drugrx2': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'drugrx3': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'drugrx4': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'drugrx5': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'drugrx6': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'rx1fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx2fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx3fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx4fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx5fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx6fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'rx1route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx2route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx3route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx4route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx5route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx6route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'rx1dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx2dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx3dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx4dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx5dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx6dur': forms.TextInput(attrs={'class': 'form-control'}),
            'rx1inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rx2inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rx3inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rx4inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rx5inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rx6inst': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose1': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose2': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose3': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose4': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose5': forms.TextInput(attrs={'class': 'form-control'}),
            'rxdose6': forms.TextInput(attrs={'class': 'form-control'}),
            'rxunit1': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'rxunit2': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'rxunit3': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'rxunit4': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'rxunit5': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'rxunit6': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'fxdone': forms.NumberInput(attrs={'class': 'form-control'}),
            'intervention1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'intervention2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'intervention3': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'intervention4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }


class S8FUPForm(ModelForm):
    class Meta:
        model = S8FUP
        fields = "__all__"
        exclude = ["s8_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control'}),
            's2_id': forms.NumberInput(attrs={'class': 'form-control'}),
            's3_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'visitdate': DateInput(attrs={'class': 'form-control'}),
            'visittype': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'visitaction': forms.Select(attrs={'class': 'form-control'}),
            'Weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'PerfStatus': forms.Select(attrs={'class': 'form-control'}, choices=PS),
            'Nextvisit': DateInput(attrs={'class': 'form-control'}),
            'RecordRecc': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}, choices=YES_NO),
            'LRstatus': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'RRstatus': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'DMstatus': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'Death': forms.Select(attrs={'class': 'form-control'}, choices=YES_NO),
            'CauseDeath': forms.Select(attrs={'class': 'form-control'}, choices=deathcause_choices),
            'Datedeath': DateInput(attrs={'class': 'form-control'}),
            # LATE TOXICITY
            'ToxType1': forms.Select(attrs={'class': 'form-control'}, choices=RT_LATE_TOXICITY),
            'SeverityT1': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'ToxType2': forms.Select(attrs={'class': 'form-control'}, choices=RT_LATE_TOXICITY),
            'SeverityT2': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'ToxType3': forms.Select(attrs={'class': 'form-control'}, choices=RT_LATE_TOXICITY),
            'SeverityT3': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'ToxType4': forms.Select(attrs={'class': 'form-control'}, choices=RT_LATE_TOXICITY),
            'SeverityT4': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            'ToxType5': forms.Select(attrs={'class': 'form-control'}, choices=RT_LATE_TOXICITY),
            'SeverityT5': forms.Select(attrs={'class': 'form-control'}, choices=toxicity_choices),
            # RECORD SYMPTOMS
            'Symp1': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp2': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp3': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp4': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp5': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp6': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp7': forms.TextInput(attrs={'class': 'form-control'}),
            'Symp1Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp2Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp3Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp4Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp5Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp6Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            'Symp7Type': forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            # PRESCRIPTIONS
            'DrugRx1': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'DrugRx2': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'DrugRx3': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'DrugRx4': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'DrugRx5': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'DrugRx6': forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            'Rx1Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx2Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx3Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx4Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx5Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx6Fx': forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            'Rx1Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx2Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx3Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx4Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx5Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx6Route': forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            'Rx1Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx2Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx3Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx4Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx5Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx6Dur': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx1Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx2Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx3Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx4Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx5Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'Rx6Inst': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose1': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose2': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose3': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose4': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose5': forms.TextInput(attrs={'class': 'form-control'}),
            'RxDose6': forms.TextInput(attrs={'class': 'form-control'}),
            'RxUnit1': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'RxUnit2': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'RxUnit3': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'RxUnit4': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'RxUnit5': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            'RxUnit6': forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            # INTERVENTIONS
            'Intervention1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'Intervention2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'Intervention3': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'Intervention4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # PETCT
            'PETCTSite': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTSite1': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTSite2': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTSite3': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTSite4': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCT': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCT1': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCT2': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCT3': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCT4': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTNotes1': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTNotes2': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTNotes3': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTNotes4': forms.TextInput(attrs={'class': 'form-control'}),
            'PETCTReport': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # CT & USG
            'CTSite': forms.TextInput(attrs={'class': 'form-control'}),
            'CTSite1': forms.TextInput(attrs={'class': 'form-control'}),
            'CTSite2': forms.TextInput(attrs={'class': 'form-control'}),
            'CTSite3': forms.TextInput(attrs={'class': 'form-control'}),
            'CTSite4': forms.TextInput(attrs={'class': 'form-control'}),
            'CECT': forms.TextInput(attrs={'class': 'form-control'}),
            'CECT1': forms.TextInput(attrs={'class': 'form-control'}),
            'CECT2': forms.TextInput(attrs={'class': 'form-control'}),
            'CECT3': forms.TextInput(attrs={'class': 'form-control'}),
            'CECT4': forms.TextInput(attrs={'class': 'form-control'}),
            'CECTNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'CECTNotes1': forms.TextInput(attrs={'class': 'form-control'}),
            'CECTNotes2': forms.TextInput(attrs={'class': 'form-control'}),
            'CECTNotes3': forms.TextInput(attrs={'class': 'form-control'}),
            'CECTNotes4': forms.TextInput(attrs={'class': 'form-control'}),
            'LDCT': forms.TextInput(attrs={'class': 'form-control'}),
            'LDCTNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'UGIE': forms.TextInput(attrs={'class': 'form-control'}),
            'UGIENotes': forms.TextInput(attrs={'class': 'form-control'}),
            # XRAY
            'XRaySite': forms.TextInput(attrs={'class': 'form-control'}),
            'XRaySite1': forms.TextInput(attrs={'class': 'form-control'}),
            'XRaySite2': forms.TextInput(attrs={'class': 'form-control'}),
            'XRaySite3': forms.TextInput(attrs={'class': 'form-control'}),
            'XRaySite4': forms.TextInput(attrs={'class': 'form-control'}),
            'XRay': forms.TextInput(attrs={'class': 'form-control'}),
            'XRay1': forms.TextInput(attrs={'class': 'form-control'}),
            'XRay2': forms.TextInput(attrs={'class': 'form-control'}),
            'XRay3': forms.TextInput(attrs={'class': 'form-control'}),
            'XRay4': forms.TextInput(attrs={'class': 'form-control'}),
            'XRayNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'XRayNotes1': forms.TextInput(attrs={'class': 'form-control'}),
            'XRayNotes2': forms.TextInput(attrs={'class': 'form-control'}),
            'XRayNotes3': forms.TextInput(attrs={'class': 'form-control'}),
            'XRayNotes4': forms.TextInput(attrs={'class': 'form-control'}),
            # MRI
            'MRSite': forms.TextInput(attrs={'class': 'form-control'}),
            'MRSite1': forms.TextInput(attrs={'class': 'form-control'}),
            'MRSite2': forms.TextInput(attrs={'class': 'form-control'}),
            'MRSite3': forms.TextInput(attrs={'class': 'form-control'}),
            'MRSite4': forms.TextInput(attrs={'class': 'form-control'}),
            'MR': forms.TextInput(attrs={'class': 'form-control'}),
            'MR1': forms.TextInput(attrs={'class': 'form-control'}),
            'MR2': forms.TextInput(attrs={'class': 'form-control'}),
            'MR3': forms.TextInput(attrs={'class': 'form-control'}),
            'MR4': forms.TextInput(attrs={'class': 'form-control'}),
            'MRNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'MRNotes1': forms.TextInput(attrs={'class': 'form-control'}),
            'MRNotes2': forms.TextInput(attrs={'class': 'form-control'}),
            'MRNotes3': forms.TextInput(attrs={'class': 'form-control'}),
            'MRNotes4': forms.TextInput(attrs={'class': 'form-control'}),
            # BIOPSY
            'BiopsySite': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsySite1': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsySite2': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsySite3': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsySite4': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyResult': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyResult1': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyResult2': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyResult3': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyResult4': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyNotes': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyNotes1': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyNotes2': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyNotes3': forms.TextInput(attrs={'class': 'form-control'}),
            'BiopsyNotes4': forms.TextInput(attrs={'class': 'form-control'}),
            # NOTES
            'Notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }


class InvestigationsImagingForm(ModelForm):
    class Meta:
        model = InvestigationsImaging
        fields = "__all__"
        exclude = ["s8_imaging_id", "last_updated"]


        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's8_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            "imaging_date": DateInput(attrs={'class': 'form-control'}),
            "imaging_type": forms.Select(attrs={'class': 'form-control'}),
            "imaging_location": forms.Select(attrs={'class': 'form-control'}),
            "imaging_result": forms.Select(attrs={'class': 'form-control'}),
            "imaging_result_details": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            "lab_name": forms.Select(attrs={'class': 'form-control'}),
            "lab_contact": forms.TextInput(attrs={'class': 'form-control'}),
            "notes": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = "__all__"
        exclude = ["s8_prescription_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's8_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            "symptoms": forms.TextInput(attrs={'class': 'form-control'}),
            "symptoms_type": forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            "symp_duration": forms.NumberInput(attrs={'class': 'form-control'}),
            "drug_name": forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            "dosage": forms.TextInput(attrs={'class': 'form-control'}),
            "unit": forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            "route": forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            "frequency": forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            "duration": forms.TextInput(attrs={'class': 'form-control'}),
            "notes": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class InvestigationsPathForm(ModelForm):
    class Meta:
        model = Prescription
        fields = "__all__"
        exclude = ["s8_path_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's8_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            "path_type": forms.TextInput(attrs={'class': 'form-control'}),
            "guided_by": forms.Select(attrs={'class': 'form-control'}, choices=symp_type_choices),
            "biopsy_date": forms.NumberInput(attrs={'class': 'form-control'}),
            "biopsy_location": forms.Select(attrs={'class': 'form-control'}, choices=drugs_choices),
            "biopsy_result": forms.TextInput(attrs={'class': 'form-control'}),
            "biopsy_result_details": forms.Select(attrs={'class': 'form-control'}, choices=unit_choices),
            "lab_name": forms.Select(attrs={'class': 'form-control'}, choices=route_choices),
            "lab_contact": forms.Select(attrs={'class': 'form-control'}, choices=frequency_choices),
            "molecular_profile": forms.TextInput(attrs={'class': 'form-control'}),
            "molecular_profile_status": forms.TextInput(attrs={'class': 'form-control'}),
            "notes": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class PrimaryDVHForm(ModelForm):
    class Meta:
        model = PrimaryDVH
        fields = "__all__"
        exclude = ['s4_dvh_id', "last_updated"]

        widgets = {
            "s4_id": forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'str_type': forms.Select(attrs={'class': 'form-control'}),
            'str_name': forms.Select(attrs={'class': 'form-control'}),
            'target_class_base': forms.Select(attrs={'class': 'form-control'}),
            'target_class_number': forms.Select(attrs={'class': 'form-control'}),
            'target_class_image': forms.Select(attrs={'class': 'form-control'}),
            'target_class_dose': forms.Select(attrs={'class': 'form-control'}),
            'target_class_custom': forms.Select(attrs={'class': 'form-control'}),
            'vol': forms.NumberInput(attrs={'class': 'form-control'}),
            'parameters': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PFTDetailsForm(ModelForm):
    class Meta:
        model = PFTDetails
        fields = "__all__"
        exclude = ["pft_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's8_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            "StudyDate": DateInput(attrs={'class': 'form-control'}),
            "DLCO": forms.NumberInput(attrs={'class': 'form-control'}),
            "DLCOpred": forms.NumberInput(attrs={'class': 'form-control'}),
            "DLCO_VA": forms.NumberInput(attrs={'class': 'form-control'}),
            "DLCO_VApred": forms.NumberInput(attrs={'class': 'form-control'}),
            "prFEV1": forms.NumberInput(attrs={'class': 'form-control'}),
            "prFEV1pred": forms.NumberInput(attrs={'class': 'form-control'}),
            "poFEV1": forms.NumberInput(attrs={'class': 'form-control'}),
            "poFEV1pred": forms.NumberInput(attrs={'class': 'form-control'}),
            "FEV1_change": forms.NumberInput(attrs={'class': 'form-control'}),
            "prFEV1_FVC": forms.NumberInput(attrs={'class': 'form-control'}),
            "prFEV1_FVCpred": forms.NumberInput(attrs={'class': 'form-control'}),
            "poFEV1_FVC": forms.NumberInput(attrs={'class': 'form-control'}),
            "poFEV1_FVCpred": forms.NumberInput(attrs={'class': 'form-control'}),
            "FEV1_FVC_change": forms.NumberInput(attrs={'class': 'form-control'}),
            "Notes": forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class CardiacMarkersForm(ModelForm):
    class Meta:
        model = CardiacMarkers
        fields = "__all__"
        exclude = ["cm_id", "last_updated"]

        widgets = {
            'parent_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            's8_id': forms.NumberInput(attrs={'class': 'form-control'}),
            "date": DateInput(attrs={'class': 'form-control'}),
            "trop_i": forms.NumberInput(attrs={'class': 'form-control'}),
            "hs_crp": forms.NumberInput(attrs={'class': 'form-control'}),
            "nt_probnp": forms.NumberInput(attrs={'class': 'form-control'}),
            "rtstartdate": DateInput(attrs={'class': 'form-control'}),
            "planned_fr": forms.NumberInput(attrs={'class': 'form-control'}),
            "notes": forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


all_sites = Site.objects.all()
site_choices = [(e.site, e.site) for e in all_sites]
site_choices.insert(0, ('', ''))

all_main_sites = ICDMainSites.objects.all()
main_site_choices = [(e.site, e.site) for e in all_main_sites]
main_site_choices.insert(0, ('', ''))

all_tech = RTTech.objects.all()
tech_choices = [(e.tech, e.tech) for e in all_tech]
tech_choices.insert(0, ('', ''))

all_studygp = StudyGroup.objects.all()
studygp_choices = [(e.id, e.id) for e in all_studygp]
studygp_choices.insert(0, ('', ''))


class FilterRTStarted(forms.Form):
    s_date = forms.DateField(required=False,
                             widget=DateInput(attrs={'class': 'form-control form-control-lg', 'readonly': True}))
    f_date = forms.DateField(required=False,
                             widget=DateInput(attrs={'class': 'form-control form-control-lg', 'readonly': True}))
    # main_site = forms.ChoiceField(required=False,
    #                               widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
    #                               choices=main_site_choices)
    # subsite_site = forms.ChoiceField(required=False,
    #                          widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
    #                          choices=site_choices)
    technique = forms.ChoiceField(required=False,
                                  widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
                                  choices=[])
    intent = forms.ChoiceField(required=False,
                               widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
                               choices=[])
    studygp = forms.ChoiceField(required=False,
                                widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
                                choices=[])
