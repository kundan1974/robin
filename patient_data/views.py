import pytz
import datetime

from django import forms
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms import modelform_factory, formset_factory
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.db import connection
from django.db.models import Q, F, DateTimeField, ExpressionWrapper, Max, Prefetch
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, FormView

from .forms import (S1PatientRegForm, PreSimulationForm, S2DiagnosisForm, S3CarePlanForm, SimulationForm, S4RTForm,
                    S7AssessmentForm, S6SurgeryForm, S6HPEForm, S5ChemoForm, S8FUPForm, PrimaryDVHForm, PFTDetailsForm,
                    CardiacMarkersForm, FilterRTStarted, InvestigationsImagingForm, PrescriptionForm,
                    InvestigationsPathForm, InvestigationsMolecularForm, InvestigationsLabsForm, LateToxicityForm,
                    S5ChemoProtocolForm, S5ChemoDrugsForm, S5ChemoDrugsFormSet, AcuteToxicityForm, NewPreSimulationForm,
                    NewPreSimulationWithoutCareForm, SimulationWithoutCarePlanForm)
from django.utils import timezone
from django.contrib import messages
import pandas as pd

from .mainsite import mainsite_query, mainsite_subsite_query
from .utilities import db_homestatus, get_timeline, raw_query01, mobile, get_tnm, get_stagegroup
from log2d import Log
from wsgiref.util import FileWrapper

log_datetime = Log('patient_data_logs', to_file=True, path='./logs')
log_cardiac_marker = Log('cardiac_marker', to_file=True, path='./logs')
log_summary_rt = Log('summary_rt', to_file=True, path='./logs')

now = timezone.now()
Log.patient_data_logs.info(f"Todays Date: {now}")

from .forms import SearchCRN

from .models import (Comorbidity, OurDiagnosis, HPE, Site,
                     ChemoProtocolNew, SxCodes, S1ParentMain, SimStatus, RTVolumes, RTStatus, PreSimulation,
                     S2Diagnosis, S3CarePlan, Simulation, S4RT, S7Assessment, S6Surgery, S6HPE, S5Chemo, S8FUP,
                     PrimaryDVH, StrType, StrName, StrNameClassifierBase, StrNameClassifierNumber,
                     StrNameClassifierImage, StrNameClassifierDose, StrNameClassifierCustom, DVHParameters, PFTDetails,
                     CardiacMarkers, ICDMainSites, InvestigationsImaging, ImageLocation, ImagingResult, ImagingType,
                     LabName, Prescription, InvestigationsPath, InvestigationsMolecular, InvestigationsLabs,
                     LateToxicity, S5ChemoProtocol, S5ChemoDrugs, AcuteToxicity, CTCV5, NewPreSimulation, RTTech,
                     GenDrugs, TNM, ClinT, ClinN, ClinM, StageGroup, BreastGroupTNM)


# Simulation, PreSimulation, S2Diagnosis, S3CarePlan, S4RT,
# S5Chemo, S6Surgery, S6HPE, S7Assessment, S8FUP, PrimaryDVH, PFTDetails, CardiacMarkers, CardiacMarkers


def add_business_days(from_date, number_of_days):
    to_date = from_date
    while number_of_days:
        to_date += datetime.timedelta(1)
        if to_date.weekday() < 5:  # i.e. is not saturday or sunday
            number_of_days -= 1
    return to_date


@login_required
def index(request):
    context = cache.get('patient_data')
    if context is not None:
        return render(request, 'patient_data/index.html', context)

    sims = Simulation.objects.all().prefetch_related(
        'site', 'technique', 'initialstatus', 'assignedto'
    )
    full_data = []
    [full_data.append(data) for data in sims]
    # Breast Data
    lt_breast_no = sims.filter(site__code="Left Breast").count()
    rt_breast_no = sims.filter(site__code="Right Breast").count()
    breast_dibh_no = sims.filter(technique__code__contains="DIBH").count()
    breast_imrt_fif_no = sims.filter(site__code__contains="Breast").filter(technique__code__contains="IMRT-FIF").count()
    breast_imrt_inv_no = sims.filter(site__code__contains="Breast").filter(technique__code="IMRT").count()
    breast_tomo_no = sims.filter(site__code__contains="Breast").filter(technique__code="Tomo-IMRT").count()
    # Lung Data
    nsclc_no = sims.filter(site__code__contains="NSCLC").count()
    sclc_no = sims.filter(site__code__startswith="SCLC").count()
    lung_imrt_no = sims.filter((Q(site__code__contains="NSCLC") | Q(site__code__startswith="SCLC")) &
                               Q(technique__code="IMRT")).count()
    lung_igrt_no = sims.filter(Q(site__code__contains='NSCLC') | Q(site__code__startswith='SCLC'),
                               Q(technique__code__contains='IGRT') | Q(technique__code__contains='Tomo-IGRT')).count()
    lung_pall_imrt_no = sims.filter(Q(site__code__contains="NSCLC") | Q(site__code__startswith="SCLC"),
                                    Q(technique__code="Pall IMRT")).count()
    lung_2drt_no = sims.filter(Q(site__code__contains="NSCLC") | Q(site__code__startswith="SCLC"),
                               Q(technique__code="2DRT")).count()
    # Esophagus Data
    eso_no = sims.filter(Q(site__code__startswith="Eso")).count()
    eso_igrt_no = sims.filter(Q(site__code__startswith="Eso")).filter(
        Q(technique__code="IGRT") | Q(technique__code="Tomo-IGRT")).count()
    eso_imrt_no = sims.filter(Q(site__code__startswith="Eso")).filter(technique__code="IMRT").count()
    eso_ilrt_no = sims.filter(Q(site__code__startswith="Eso")).filter(
        Q(technique__code__icontains="ILRT")).count()
    eso_pall_imrt_no = sims.filter(Q(site__code__startswith="Eso")).filter(technique__code="Pall IMRT").count()
    eso_2drt_no = sims.filter(Q(site__code__startswith="Eso")).filter(technique__code="2DRT").count()
    # Brain Data
    brain_no = sims.filter(Q(site__code__istartswith="Brain")).count()
    brain_srs_no = sims.filter(Q(site__code__istartswith="Brain")).filter(Q(technique__code__icontains="SRS")).count()
    brain_2drt_no = sims.filter(Q(site__code__istartswith="Brain")).filter(Q(technique__code__icontains="2DRT")).count()
    brain_pall_imrt_no = sims.filter(Q(site__code__istartswith="Brain")).filter(Q(
        technique__code__icontains="Pall IMRT")).count()
    # Simulation and RT Data
    delta_date_30 = timezone.now() - timezone.timedelta(30)

    sim_no = sims.count()
    sim_last30days = sims.filter(simdate__gte=delta_date_30).count()
    onrt_no = sims.filter(initialstatus__code__icontains="started").count()
    about2complete = sims.filter(donefr=F('totalfractions') - 2).count()
    delta_date_3 = timezone.now() + timezone.timedelta(3)
    near_completion_no = sims.filter(
        tentativecompletiondate__gt=timezone.now().date()).filter(tentativecompletiondate__lte=delta_date_3).count()
    today_imp_no = sims.filter(impdate=timezone.now().date()).count()
    completing_today_no = sims.filter(tentativecompletiondate=timezone.now().date()).count()
    # Cardiac Markers details
    delta_date_18 = timezone.now() - timezone.timedelta(18)
    full_cm_data = []
    cmdata = CardiacMarkers.objects.all().select_related()
    [full_cm_data.append(data) for data in cmdata]
    cmdata_no = len(full_cm_data)
    due_for_test = cmdata.filter(date__lte=delta_date_18)
    try:
        # due_for_test1 = due_for_test.annotate(date2=F('simpk__tentativecompletiondate'))
        due_for_test1 = due_for_test.annotate(
            date2=ExpressionWrapper(F('rtstartdate') + timezone.timedelta(22), output_field=DateTimeField())
        )
        due_for_test = due_for_test1.annotate(
            date3=ExpressionWrapper(F('date2') + timezone.timedelta(90), output_field=DateTimeField())
        )
    except:
        Log.cardiac_marker.error(f"Todays Date: {now}: Issues related to annotate or F")
    # PreSimulation Data
    delta_date_5 = timezone.now() - timezone.timedelta(90)
    full_presimdata = []
    presimdata = NewPreSimulation.objects.prefetch_related().filter(date__gt=delta_date_5).order_by('-date').all()
    [full_presimdata.append(data) for data in presimdata]
    presimdata_no = NewPreSimulation.objects.all().count()
    # Simulation recent data
    delta_date_30 = timezone.now() - timezone.timedelta(30)
    recent_simulations = sims.filter(
        simdate__gte=delta_date_30).filter(Q(initialstatus__code__contains="Planning") |
                                           Q(initialstatus__code__contains="Simulation")).order_by('impdate')
    # User specific simulation
    current_user = request.user
    user_simulations = sims.filter(assignedto=current_user.pk).filter(simdate__gte=delta_date_30)
    all_user_simulations = sims.filter(assignedto=current_user.pk)
    df_user = pd.DataFrame.from_records(all_user_simulations.values())
    try:
        user_site_freq = df_user['site_id'].value_counts()
        user_site_freq_count = len(all_user_simulations)
        user_data = dict([(key, value) for key, value in zip(user_site_freq.index, user_site_freq)])
    except:
        user_site_freq_count = 0
        user_data = None

    user_simulations_completed_no = sims.filter(assignedto=current_user.pk).filter(
        simdate__gte=delta_date_30).filter(
        Q(initialstatus__code__contains="Ready") |
        Q(initialstatus__code__contains="Completed") |
        Q(initialstatus__code__contains="Defaulted") |
        Q(initialstatus__code__contains="Started")).count()
    user_simulations_no = len(user_simulations)
    crnumber = 123456
    if mobile(request):
        is_mobile = True
    else:
        is_mobile = False

    context = {
        'is_mobile': is_mobile,
        'lt_breast_no': lt_breast_no,
        'rt_breast_no': rt_breast_no,
        'breast_dibh_no': breast_dibh_no,
        'breast_imrt_fif_no': breast_imrt_fif_no,
        'breast_imrt_inv_no': breast_imrt_inv_no,
        'breast_tomo_no': breast_tomo_no,
        'nsclc_no': nsclc_no,
        'sclc_no': sclc_no,
        'lung_imrt_no': lung_imrt_no,
        'lung_igrt_no': lung_igrt_no,
        'lung_pall_imrt_no': lung_pall_imrt_no,
        'lung_2drt_no': lung_2drt_no,
        'eso_no': eso_no,
        'eso_igrt_no': eso_igrt_no,
        'eso_imrt_no': eso_imrt_no,
        'eso_ilrt_no': eso_ilrt_no,
        'eso_pall_imrt_no': eso_pall_imrt_no,
        'eso_2drt_no': eso_2drt_no,
        'brain_no': brain_no,
        'brain_srs_no': brain_srs_no,
        'brain_2drt_no': brain_2drt_no,
        'brain_pall_imrt_no': brain_pall_imrt_no,
        'sim_no': sim_no,
        'sim_last30days': sim_last30days,
        'onrt_no': onrt_no,
        'about2complete': about2complete,
        'near_completion_no': near_completion_no,
        'today_imp_no': today_imp_no,
        'completing_today_no': completing_today_no,
        'cm_data': due_for_test,
        'cmdata_no': cmdata_no,
        'presim_data': presimdata,
        'presimdata_no': presimdata_no,
        'simulations': recent_simulations,
        'assigned': user_simulations_no,
        'assignment_completed': user_simulations_completed_no,
        'user_simulations': user_simulations,
        'user_data': user_data,
        'user_site_freq_count': user_site_freq_count,
        'crnumber': crnumber
    }
    cache.set('patient_data', context, 300)  # cache for 300 seconds
    return render(request, 'patient_data/index.html', context)


def index1(request):
    # Try to get the data from cache
    context = cache.get('patient_data')
    if context is not None:
        return render(request, 'patient_data/index1.html', context)

    sims = Simulation.objects.all().prefetch_related(
        'site', 'technique', 'initialstatus', 'assignedto'
    )
    # Breast Data
    lt_breast_no = sims.filter(site__code="Left Breast").count()
    rt_breast_no = sims.filter(site__code="Right Breast").count()
    breast_dibh_no = sims.filter(technique__code__contains="DIBH").count()
    breast_imrt_fif_no = sims.filter(site__code__contains="Breast").filter(technique__code__contains="IMRT-FIF").count()
    breast_imrt_inv_no = sims.filter(site__code__contains="Breast").filter(technique__code="IMRT").count()
    breast_tomo_no = sims.filter(site__code__contains="Breast").filter(technique__code="Tomo-IMRT").count()
    context = {'lt_breast_no': lt_breast_no,
               'rt_breast_no': rt_breast_no,
               'breast_dibh_no': breast_dibh_no,
               'breast_imrt_fif_no': breast_imrt_fif_no,
               'breast_imrt_inv_no': breast_imrt_inv_no,
               'breast_tomo_no': breast_tomo_no, }
    # Store the data in cache
    cache.set('patient_data', context, 300)  # cache for 300 seconds
    return render(request, 'patient_data/index1.html', context)


# db_operations view
@login_required
def radonc_home(request, crnumber=None):
    # presim = False
    # sim = False
    # dx = False
    # mx = False
    # rt = False
    # pft = False
    # cm = False
    # res = False
    # presimdetails = None

    try:
        user_sim = Simulation.objects.filter(assignedto=request.user.pk, initialstatus="Simulation").count()
        request.session["check"] = user_sim
    except:
        request.session["check"] = 0
        user_sim = 0
    if mobile(request):
        is_mobile = True
    else:
        is_mobile = False
    if request.method == 'POST':
        form = SearchCRN(request.POST)
        crnumber = form.data.get('s_crnumber')
        if crnumber:
            request.session['crnumber'] = crnumber
        status = db_homestatus(crnumber)
        status['form'] = form
        status['user_sim'] = user_sim

        regdetails, reg_date, dxinfo, mxinfo = get_timeline(crnumber)
        status['regdetails'] = regdetails
        status['reg_date'] = reg_date
        status['dxinfo'] = dxinfo
        status['mxinfo'] = mxinfo
        status['is_mobile'] = is_mobile

        return render(request, 'patient_data/radonc_db_operations.html', status)
    else:
        if crnumber:
            request.session['crnumber'] = crnumber
            form = SearchCRN()
            form.initial['s_crnumber'] = crnumber
            status = db_homestatus(crnumber)
            status['form'] = form
            status['user_sim'] = user_sim
            return render(request, 'patient_data/radonc_db_operations.html', status)
        else:
            form = SearchCRN()
            status = db_homestatus()
            status['form'] = form
            status['user_sim'] = user_sim
            status['is_mobile'] = is_mobile
            return render(request, 'patient_data/radonc_db_operations.html', status)


@login_required
def s1registration(request, crnumber=123456):
    """
    Patient Registratation
    """
    if request.method == 'POST':
        current_user = User.objects.get(id=request.user.id)
        # YOU HAVE TO COPY THE POST DATA - otherwise it will not work
        # Ref: https://stackoverflow.com/questions/8241001/how-do-i-modify-the-bound-value-for-a-field-in-a-bound-form-in-django
        data = request.POST.copy()
        form = S1PatientRegForm(data=data)
        form.data['user'] = current_user.pk
        if form.is_valid():
            # crn = int(form.data.get('crnumber'))
            form.save()
            crnumber = form.cleaned_data.get('crnumber')
            messages.success(request, f'Data has been saved for CRNumber: {crnumber}')
            return redirect('db_operations', crnumber)
    else:
        if crnumber == 123456:
            form = S1PatientRegForm()
            messages.success(request, f'Please Enter CR Number and press SUBMIT button to proceed')
        else:
            form = S1PatientRegForm(initial={'crnumber': crnumber, 'doc_type': 'Other'})
    return render(request, 'patient_data/patient_registration.html', {'form': form,
                                                                      'crnumber': crnumber})


class S1RegUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S1ParentMain
    form_class = modelform_factory(S1ParentMain, S1PatientRegForm)
    template_name = "patient_data/patient_registration.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S1ParentMain.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.updated_by = current_user.username
        form.instance.user = patient.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S1ParentMain.objects.get(pk=pk)
        # patient = PatientDiagnosis.objects.get(pk=pk)
        return reverse_lazy("db_operations", kwargs={"crnumber": patient.crnumber})

    # def get_queryset(self):
    #     return S1ParentMain.objects.filter(pk=self.kwargs['pk'])

    # To check if form is invalid
    # def form_invalid(self, form):
    #     pk = self.kwargs["pk"]
    #     # print(form.data)
    #     # print(form.errors)
    #     return reverse_lazy("radonc-radonc-reg-update", kwargs={"crnumber": pk})


class S1ListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S1ParentMain
    template_name = 'patient_data/patientlist.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'
    ordering = ['-last_updated']
    paginate_by = 15

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_no = int(self.request.GET.get('page', 1))
        serial_num = (int(self.request.GET.get('page', 1)) - 1) * self.paginate_by + 1
        context['serial_num'] = serial_num - 1
        context['page_no'] = page_no
        return context


# def summary(request, crnumber):
#     return render(request, 'patient_data/summary.html', {'crnumber': crnumber})


# PRESIMULATION

def presimulation(request, crnumber=None, s3_id=None):
    if request.method == "POST":
        # Getting current user
        current_user = User.objects.get(id=request.user.id)
        # Copying request data otherwise it will not work
        # Ref: https://stackoverflow.com/questions/8241001/how-do-i-modify-the-bound-value-for-a-field-in-a-bound-form-in-django
        data = request.POST.copy()
        form = PreSimulationForm(data=data)
        # Setting value of user column to current user
        form.data['user'] = current_user.pk
        if s3_id is not None:
            try:
                mx_details = S3CarePlan.objects.get(pk=s3_id)
                form.data['s3_id'] = mx_details.s3_id
            except:
                pass
        if form.is_valid():
            crn = form.data.get('presimparent')
            form.save()
            messages.success(request, f'Data has been saved for CRNumber: {crn}')
            return redirect('radonc-presimulation-list', crn)
        else:
            print(form.errors)
    else:
        if crnumber:
            # patient = S1ParentMain.objects.filter(crnumber=crnumber).first()
            form = PreSimulationForm(initial={'presimparent': crnumber})
        else:
            form = PreSimulationForm()

    return render(request, 'patient_data/radonc_presimulation.html', {'form': form, 'crnumber': crnumber})


class PreSimulationListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = PreSimulation
    template_name = 'patient_data/radonc_presimulation_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return PreSimulation.objects.filter(presimparent=self.kwargs['crnumber'])


class PreSimulationUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PreSimulation
    form_class = modelform_factory(PreSimulation, PreSimulationForm)
    template_name = "patient_data/radonc_presimulation.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = PreSimulation.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.updated_by = current_user.username
        form.instance.user = patient.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = PreSimulation.objects.get(pk=pk)
        crn = patient.presimparent.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        return reverse_lazy("radonc-presimulation-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(PreSimulationUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = PreSimulation.objects.get(pk=pk)
        updatecrn = patient.presimparent.crnumber
        context['updatecrn'] = updatecrn
        context['update'] = True
        return context

    def form_invalid(self, form):
        pk = self.kwargs["pk"]
        print(form.errors)
        return reverse_lazy("radonc-presimulation-update", kwargs={"pk": pk})


class PreSimulationDeleteView(LoginRequiredMixin, DeleteView):
    model = PreSimulation
    template_name = "patient_data/radonc_presimulation_confirm_delete.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = PreSimulation.objects.get(pk=pk)
        crn = patient.presimparent.crnumber
        return reverse_lazy("radonc-presimulation-list", kwargs={"crnumber": crn})

    # def get_queryset(self):
    #     pk = self.kwargs["pk"]
    #     patient = PreSimulation.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        patient = PreSimulation.objects.get(pk=pk)
        crn = patient.presimparent.crnumber
        try:
            patient.delete()
        except IntegrityError:
            messages.error(self.request, f"{crn}: Cannot Delete as Simulation for this PreSim already exists!!")
            return render(request, 'patient_data/error.html')
        messages.success(self.request, f"Patient's ({crn}) presimulation detail got deleted")
        return render(request, 'patient_data/error.html')


class NewPreSimulationListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = NewPreSimulation
    template_name = 'patient_data/radonc_newpresimulation_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return NewPreSimulation.objects.filter(presimparent=self.kwargs['crnumber'])


# DIAGNOSIS

class DiagnosisCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S2Diagnosis
    form_class = modelform_factory(S2Diagnosis, S2DiagnosisForm)
    template_name = "patient_data/radonc_diagnosis.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        crnumber = self.kwargs['crnumber']
        form.instance.user = current_user
        print(form.errors)
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        # try:
        #     fup = S8FUP.objects.filter(parent_id=crn).last()
        #     dx = S2Diagnosis.objects.filter(parent_id=crn).last()
        #     print(fup)
        #     fup.update(s2_id=dx)
        # except AttributeError:
        #     pass

        if self.request.GET['next'] == "/patient_data/radonc-patientlist/":
            return reverse_lazy("radonc-patientlist")
        return reverse_lazy("db_operations", kwargs={"crnumber": crn})

    # def get_form(self, form_class=form_class):
    #     T, N, M = get_tnm()
    #     form = super().get_form(form_class)
    #     form.fields['t_new'] = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    #     form.fields['n_new'] = forms.ChoiceField(choices=N, widget=forms.Select(attrs={'class': 'form-control'}))
    #     form.fields['m_new'] = forms.ChoiceField(choices=M, widget=forms.Select(attrs={'class': 'form-control'}))
    #     form.fields['stage_new'] = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    #     form.fields['t_new'].choices = T
    #     form.fields['n_new'].choices = N
    #     form.fields['m_new'].choices = M
    #     form.fields['stage_new'].choices = []
    #     return form

    def get_context_data(self, **kwargs):
        context = super(DiagnosisCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        self.request.session["crnumber"] = crnumber
        T, N, M, Stage = [("", "")], [("", "")], [("", "")], [("", "")]
        pT, pN, pM, pStage = [("", "")], [("", "")], [("", "")], [("", "")]
        for value in ClinT.objects.all().values():
            T.append((value["code"], value["code"]))
            pT.append((value["code"], value["code"]))
        for value in ClinN.objects.all().values():
            N.append((value["code"], value["code"]))
            pN.append((value["code"], value["code"]))
        for value in ClinM.objects.all().values():
            M.append((value["code"], value["code"]))
            pM.append((value["code"], value["code"]))
        for value in StageGroup.objects.all().values():
            Stage.append((value["code"], value["code"]))
            pStage.append((value["code"], value["code"]))
        primary_dx = None

        class DiagnosisForm(S2DiagnosisForm):
            def __init__(self, *args, **kwargs):
                super(DiagnosisForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)
                self.fields['t_new'] = forms.ChoiceField(choices=[], required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['n_new'] = forms.ChoiceField(choices=[], required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['m_new'] = forms.ChoiceField(choices=[], required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                             widget=forms.Select(
                                                                 attrs={'class': 'myselect form-control'}))
                self.fields['p_t_new'] = forms.ChoiceField(choices=[], required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_n_new'] = forms.ChoiceField(choices=[], required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_m_new'] = forms.ChoiceField(choices=[], required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                               widget=forms.Select(
                                                                   attrs={'class': 'myselect form-control'}))

        form = DiagnosisForm()
        context['form'] = form
        if S2Diagnosis.objects.filter(parent_id=crnumber).exists():
            primary_dx = S2Diagnosis.objects.filter(parent_id=crnumber).first()
            # context['form'].initial['laterality'] = primary_dx.laterality
            context['form'].initial['diagnosis'] = primary_dx.diagnosis
            context['form'].initial['c_ajcc_edition'] = primary_dx.c_ajcc_edition
            T, N, M, pT, pN, pM = get_tnm(site=primary_dx.diagnosis.our_diagnosis)
        context['primary_dx'] = primary_dx
        patient = S1ParentMain.objects.get(crnumber=crnumber)
        context['patient'] = patient
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        form = context['form']
        form.fields['t_new'].choices = T
        form.fields['n_new'].choices = N
        form.fields['m_new'].choices = M
        form.fields['stage_new'].choices = Stage
        form.fields['p_t_new'].choices = pT
        form.fields['p_n_new'].choices = pN
        form.fields['p_m_new'].choices = pM
        form.fields['p_stage_new'].choices = pStage
        context['form'] = form

        return context

    # def form_invalid(self, form):
    #     # print(form.data)
    #     print(form.errors)
    #     return form.errors


class DiagnosisListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S2Diagnosis
    template_name = 'patient_data/radonc_s2_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return S2Diagnosis.objects.filter(parent_id=self.kwargs['crnumber'])

    def get_context_data(self, **kwargs):
        context = super(DiagnosisListView, self).get_context_data(**kwargs)
        patient_mx = S3CarePlan.objects.filter(parent_id=self.kwargs['crnumber'])

        if patient_mx:
            dx = True
        else:
            patient_dx = S2Diagnosis.objects.filter(parent_id=self.kwargs['crnumber'])
            if patient_dx:
                dx = True
            else:
                dx = False
        context['crnumber'] = self.kwargs['crnumber']
        context['patient_mx'] = patient_mx
        context['dx'] = dx
        return context


class DiagnosisUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S2Diagnosis
    form_class = modelform_factory(S2Diagnosis, S2DiagnosisForm)
    template_name = "patient_data/radonc_diagnosis.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S2Diagnosis.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        # print(form.data)
        form.instance.user = patient.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S2Diagnosis.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-diagnosis-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(DiagnosisUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S2Diagnosis.objects.get(pk=pk)
        # primary_dx = S2Diagnosis.objects.filter(parent_id=patient.parent_id).first()
        if patient.confirmed_by != "Imaging":
            diagnosis_by_hpe = True
        else:
            diagnosis_by_hpe = False
        updatecrn = patient.parent_id.crnumber
        if S2Diagnosis.objects.filter(parent_id=updatecrn).count() > 1:
            first_dx = S2Diagnosis.objects.filter(parent_id=updatecrn).first()
            if first_dx.pk == pk:
                first_dx_update = True
            else:
                first_dx_update = False
        else:
            first_dx_update = True

        class DiagnosisForm(S2DiagnosisForm):
            def __init__(self, *args, **kwargs):
                super(DiagnosisForm, self).__init__(*args, **kwargs)

                if patient.diagnosis.our_diagnosis in ["Breast", "Lung", "Esophagus"]:
                    T, N, M, pT, pN, pM = get_tnm(site=patient.diagnosis.our_diagnosis)
                    Stage, pStage = [("", "")], [("", "")]
                    for value in StageGroup.objects.all().values():
                        Stage.append((value["code"], value["code"]))
                        pStage.append((value["code"], value["code"]))

                else:
                    T, N, M, Stage = [("", "")], [("", "")], [("", "")], [("", "")]
                    pT, pN, pM, pStage = [("", "")], [("", "")], [("", "")], [("", "")]
                    for value in ClinT.objects.all().values():
                        T.append((value["code"], value["code"]))
                        pT.append((value["code"], value["code"]))
                    for value in ClinN.objects.all().values():
                        N.append((value["code"], value["code"]))
                        pN.append((value["code"], value["code"]))
                    for value in ClinM.objects.all().values():
                        M.append((value["code"], value["code"]))
                        pM.append((value["code"], value["code"]))
                    for value in StageGroup.objects.all().values():
                        Stage.append((value["code"], value["code"]))
                        pStage.append((value["code"], value["code"]))

                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

                self.fields['t_new'] = forms.ChoiceField(choices=T, required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['n_new'] = forms.ChoiceField(choices=N, required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['m_new'] = forms.ChoiceField(choices=M, required=False,
                                                         widget=forms.Select(attrs={'class': 'myselect form-control'}))
                self.fields['stage_new'] = forms.ChoiceField(choices=Stage, required=False,
                                                             widget=forms.Select(
                                                                 attrs={'class': 'myselect form-control'}))
                self.fields['p_t_new'] = forms.ChoiceField(choices=pT, required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_n_new'] = forms.ChoiceField(choices=pN, required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_m_new'] = forms.ChoiceField(choices=pM, required=False,
                                                           widget=forms.Select(
                                                               attrs={'class': 'myselect form-control'}))
                self.fields['p_stage_new'] = forms.ChoiceField(choices=pStage, required=False,
                                                               widget=forms.Select(
                                                                   attrs={'class': 'myselect form-control'}))

        form = DiagnosisForm(instance=patient)
        second_malig = False
        # form.fields["t_new"].choices = T
        # form.fields["n_new"].choices = N
        # form.fields["m_new"].choices = M
        # form.fields["stage_new"].choices = Stage
        # form.fields["p_t_new"].choices = pT
        # form.fields["p_n_new"].choices = pN
        # form.fields["p_m_new"].choices = pM
        # form.fields["p_stage_new"].choices = pStage
        context['form'] = form
        try:
            dx = patient.diagnosis.our_diagnosis
            if patient.dx_type.code == "Second Malignancy":
                second_malig = True
            else:
                second_malig = False
            if not first_dx_update:
                diagnosis = OurDiagnosis.objects.filter(our_diagnosis=dx).first().pk
                context['form'].initial['diagnosis'] = diagnosis
        except AttributeError:
            pass
        if patient.m_new == "0":
            mets = False
        elif patient.m_new == "":
            mets = False
        elif patient.m_new is None:
            mets = False
        else:
            mets = True
        if patient.p_m_new == "0":
            p_mets = False
        elif patient.p_m_new == "":
            p_mets = False
        elif patient.p_m_new is None:
            p_mets = False
        else:
            p_mets = True
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['first_dx_update'] = first_dx_update
        context['diagnosis_by_hpe'] = diagnosis_by_hpe
        context['second_malig'] = second_malig
        context['mets'] = mets
        context['p_mets'] = p_mets
        context['dx_id'] = pk
        # print(patient.p_m_new)
        # context['primary_dx'] = primary_dx
        return context

    # def form_invalid(self, form):
    #     print(form.data)
    #     print(form.errors)
    #     return form.errors


# CAREPLAN
class CareplanCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S3CarePlan
    form_class = modelform_factory(S3CarePlan, S3CarePlanForm)
    template_name = "patient_data/radonc_careplan.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        return reverse_lazy("db_operations", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(CareplanCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s2_id = self.kwargs['s2_id']
        patient = S1ParentMain.objects.get(crnumber=crnumber)

        # patient_dx = patient.s2diagnosis_set.get(s2_id=s2_id)
        patient_dx = S2Diagnosis.objects.get(s2_id=s2_id)

        class CareplanForm(S3CarePlanForm):
            def __init__(self, *args, **kwargs):
                super(CareplanForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)
                self.fields['parent_id'].widget.attrs['readonly'] = True
                self.fields['enddate'].widget.attrs['readonly'] = True

        form = CareplanForm()
        context['form'] = form
        context['patient'] = patient
        context['patient_dx'] = patient_dx
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s2_id'] = s2_id

        return context

    # def form_invalid(self, form):
    #     # print(form.data)
    #     print(form.errors)
    #     return form.errors


class CareplanListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S3CarePlan
    template_name = 'patient_data/radonc_s3_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(CareplanListView, self).get_context_data(**kwargs)
        pk = self.kwargs["crnumber"]
        patient_mx = S1ParentMain.objects.select_related().get(crnumber=pk)
        oldpresim = False
        context['patient_mx'] = patient_mx

        context['mx_end'] = True
        try:
            all_presim = patient_mx.newpresimulation_set.all()
            if all_presim:
                diff = timezone.timedelta(21)
                for p in all_presim:
                    if timezone.now() - p.date > diff:
                        oldpresim = True
                    else:
                        oldpresim = False
                    context['oldpresim'] = oldpresim
            else:
                oldpresim = False
        except:
            all_presim = False
            context['oldpresim'] = oldpresim
        try:
            all_sim = patient_mx.simulation_set.all()
        except:
            all_sim = False
        try:
            all_rt = patient_mx.s4rt_set.all()
        except:
            all_rt = False
        try:
            all_dvh = patient_mx.primarydvh_set.all()
        except:
            all_dvh = False
        try:
            all_sx = patient_mx.s6surgery_set.all()
        except:
            all_sx = False
        try:
            all_hpe = patient_mx.s6hpe_set.all()
        except:
            all_hpe = False
        try:
            all_chemo = patient_mx.s5chemo_set.all()
        except:
            all_chemo = False
        try:
            all_ass = patient_mx.s7assessment_set.all()
        except:
            all_ass = False
        try:
            all_fu = patient_mx.s8fup_set.all()
        except:
            all_fu = False
        try:
            all_pft = patient_mx.pftdetails_set.all()
        except:
            all_pft = False
        try:
            all_cm = patient_mx.cardiacmarkers_set.all()
        except:
            all_cm = False
        if all_presim:
            context['presim_check'] = True
            # context['oldpresim'] = oldpresim
        if all_sim:
            context['sim_check'] = True
        if all_rt:
            context['rt_check'] = True
        if all_dvh:
            context['dvh_check'] = True
        if all_sx:
            context['sx_check'] = True
        if all_hpe:
            context['hpe_check'] = True
        if all_chemo:
            context['chemo_check'] = True
        if all_ass:
            context['ass_check'] = True
        if all_fu:
            context['fu_check'] = True
        if all_pft:
            context['pft_check'] = True
        if all_cm:
            context['cm_check'] = True
        # print(all_sx[0].s6hpe_set.all())
        return context

    def get_queryset(self):
        return S3CarePlan.objects.select_related().filter(parent_id=self.kwargs['crnumber'])


class CarePlanUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S3CarePlan
    form_class = modelform_factory(S3CarePlan, S3CarePlanForm)
    template_name = "patient_data/radonc_careplan.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S3CarePlan.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     print(form.errors)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S3CarePlan.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        if self.request.POST.get('careplan'):
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})
        else:
            return reverse_lazy("db_operations", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(CarePlanUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S3CarePlan.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        try:
            fups = patient.s8fup_set.all()
            df_fups = pd.DataFrame.from_records(fups.values())
            if 'Yes' in df_fups['RecordRecc'].values:
                readonly_status = False
            else:
                readonly_status = True
        except:
            readonly_status = True

        class CareplanForm(S3CarePlanForm):
            def __init__(self, *args, **kwargs):
                super(CareplanForm, self).__init__(*args, **kwargs)
                self.fields['parent_id'].widget.attrs['readonly'] = True
                if patient.enddate:
                    self.fields['enddate'].widget.attrs['readonly'] = False
                    self.fields['startdate'].widget.attrs['readonly'] = True
                    # self.fields['intent'].widget.attrs['hidden'] = True
                    # self.fields['radiotherapy'].widget.attrs['hidden'] = True
                    # self.fields['surgery'].widget.attrs['disabled'] = True
                    # self.fields['chemotherapy'].widget.attrs['disabled'] = True
                    # self.fields['brachytherapy'].widget.attrs['disabled'] = True
                    # self.fields['hormone'].widget.attrs['disabled'] = True
                    # self.fields['immunotherapy'].widget.attrs['disabled'] = True
                    # self.fields['bmt'].widget.attrs['disabled'] = True
                    # self.fields['targettherapy'].widget.attrs['disabled'] = True
                    # self.fields['studyprotocol'].widget.attrs['disabled'] = True
                    self.fields['notes'].widget.attrs['readonly'] = True
                    context['mx_end'] = True

        form = CareplanForm(instance=context['data'])
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['form'] = form
        # print(context['data'])

        return context


# SIMULATION VIEWS
def simulation(request, crnumber=None, s3_id=None, presimid=None):
    if request.method == "POST":
        # Getting emails of all the users
        all_users = User.objects.filter(is_active=True)
        emails = [m.email for m in all_users]
        # Getting current user
        current_user = User.objects.get(id=request.user.id)
        # Copying request data otherwise it will not work
        # Ref: https://stackoverflow.com/questions/8241001/how-do-i-modify-the-bound-value-for-a-field-in-a-bound-form-in-django
        data = request.POST.copy()
        form = SimulationForm(data=data)
        try:
            assignedto_id = request.POST['assignedto']
            assigned_to = User.objects.get(pk=assignedto_id)
            assignedto_user = assigned_to.username
        except ValueError:
            assigned_to = User.objects.get(pk=1)
            assignedto_user = assigned_to.username
            messages.warning(request, f"This case was not assigned: Using default user: {assignedto_user} ")
            form.data['assignedto'] = assigned_to

        # Setting value of user column to current user
        form.data['user'] = current_user.pk
        if s3_id is not None:
            form.data['s3_id'] = s3_id
            mx_details = S3CarePlan.objects.get(pk=s3_id)
            s2_id = mx_details.s2_id.s2_id
            form.data['s2_id'] = s2_id

        if form.is_valid():
            crn = form.data.get('simparent')
            form.save()

            mail_status = form.cleaned_data.get('send_mail')
            ctx = {'crnumber': form.cleaned_data.get('simparent'),
                   'simdate': form.cleaned_data.get('simdate'),
                   'impdate': form.cleaned_data.get('impdate'),
                   'site': form.cleaned_data.get('site'),
                   'technique': form.cleaned_data.get('technique'),
                   'intent': form.cleaned_data.get('intent'),
                   'dosephase1': form.cleaned_data.get('dosephase1'),
                   'fxphase1': form.cleaned_data.get('fxphase1'),
                   'dosephase2': form.cleaned_data.get('dosephase2'),
                   'fxphase2': form.cleaned_data.get('fxphase2'),
                   'dosephase3': form.cleaned_data.get('dosephase3'),
                   'fxphase3': form.cleaned_data.get('fxphase3'),
                   'dosephase4': form.cleaned_data.get('dosephase4'),
                   'fxphase4': form.cleaned_data.get('fxphase4'),
                   'totaldose': form.cleaned_data.get('totaldose'),
                   'totalfractions': form.cleaned_data.get('totalfractions'),
                   'assignedto': form.cleaned_data.get('assignedto'),
                   'tentativecompletiondate': form.cleaned_data.get('tentativecompletiondate'),
                   'user': form.cleaned_data.get('user'),
                   'remarks': form.cleaned_data.get('remarks')
                   }
            message = get_template("patient_data/mail.html").render(ctx)
            if mail_status:
                msg = EmailMessage(
                    subject='New Simulation Details',
                    body=message,
                    from_email='rgcirtoffice@gmail.com',
                    to=['kundan25@gmail.com'],
                )
                msg.content_subtype = "html"
                msg.send()
            # print(mail_status)
            messages.success(request,
                             f'Data has been saved for CRNumber: {crn} and is assigned to: {assignedto_user}')
            return redirect('radonc-simulation-list', crn)
        else:
            print(form.errors)

    else:
        initialstatus = "Simulation"
        simdate = timezone.now().date()
        icdmainsite = ""
        site = ""
        technique = ""
        intent = ""
        dosephase1 = ""
        fxphase1 = ""
        dosephase2 = ""
        fxphase2 = ""
        volumes = ""
        if s3_id:
            patient_cp = S3CarePlan.objects.select_related().get(pk=s3_id)
            if patient_cp.s2_id.diagnosis.our_diagnosis == "Breast" and patient_cp.radiotherapy == "Adjuvant":
                dosephase1 = 42.5
                fxphase1 = 16
                if patient_cp.s2_id.laterality == "Right":
                    icdmainsite = 73124
                    site = "Right Breast"
                    technique = "IMRT-FIF"
                    intent = "Adjuvant"
                if patient_cp.surgery:
                    patient_sx = S6Surgery.objects.select_related().filter(s3_id=s3_id).first()
                    try:
                        patient_hpe = S6HPE.objects.select_related().filter(s6_id=patient_sx.pk).first()
                    except:
                        patient_hpe = None
                    if patient_sx:
                        for surgery in patient_sx.sxtype.all():
                            if surgery.surgery.startswith("Lumpectomy"):
                                if patient_hpe:
                                    if patient_hpe.hpegrade.code == "Grade3" or patient_cp.parent_id.age < 50:
                                        dosephase2 = 10
                                        fxphase2 = 4
                                    if patient_hpe.nodesp / patient_hpe.nodesr >= 0.5:
                                        volumes = "B-SCF-AX1,2,3-IMC"
                                    else:
                                        volumes = "B-SCF-AX3"
                            else:
                                if patient_hpe:
                                    if patient_hpe.nodesp / patient_hpe.nodesr >= 0.5:
                                        volumes = "CW-SCF-AX1,2,3-IMC"
                                    else:
                                        volumes = "CW-SCF-AX3"

        presimstatus = False
        utc = pytz.UTC
        end_date = utc.localize(datetime.datetime.today())
        start_date = datetime.datetime.today() - datetime.timedelta(14)
        start_date = utc.localize(start_date)
        mx_details = S3CarePlan.objects.get(pk=s3_id)
        s2_id = mx_details.s2_id.s2_id
        error_msg = ""
        error_status = False
        if crnumber:
            if not dosephase1:
                dosephase1 = 0
            if not dosephase2:
                dosephase2 = 0
            if not fxphase1:
                fxphase1 = 0
            if not fxphase2:
                fxphase2 = 0
            patient = S1ParentMain.objects.select_related().filter(crnumber=crnumber).first()
            if patient.last_name:
                name = patient.first_name + " " + patient.last_name
            else:
                name = patient.first_name
            if presimid:
                presimstatus = True
                pat_presim = NewPreSimulation.objects.get(pk=presimid)
                # print(pat_presim.final_status)
                if pat_presim.final_status is None or pat_presim.final_status == "":
                    error_msg = "Final Status not mentioned in presimulation module. Pleaase complete it and then proceed"
                    error_status = True
                icdmainsite = 73125
                site = "Left Breast"
                intent = "Adjuvant"
                form = SimulationForm(initial={'simparent': crnumber,
                                               'name': name,
                                               's3_id': mx_details.s3_id,
                                               's2_id': s2_id,
                                               'presimid': presimid,
                                               'technique': pat_presim.final_status,
                                               'simdate': simdate,
                                               'initialstatus': initialstatus,
                                               'site': icdmainsite,
                                               'icdmainsite': site,
                                               'intent': intent,
                                               'dosephase1': dosephase1,
                                               'fxphase1': fxphase1,
                                               'dosephase2': dosephase2,
                                               'fxphase2': fxphase2,
                                               'totaldose': dosephase1 + dosephase2,
                                               'totalfractions': fxphase1 + fxphase2,
                                               'volumes': volumes
                                               })

            else:
                form = SimulationForm(initial={'simparent': crnumber,
                                               'name': name,
                                               's3_id': mx_details.s3_id,
                                               's2_id': s2_id,
                                               'simdate': simdate,
                                               'initialstatus': initialstatus,
                                               'site': site,
                                               'icdmainsite': icdmainsite,
                                               'technique': technique,
                                               'intent': intent,
                                               'dosephase1': dosephase1,
                                               'fxphase1': fxphase1,
                                               'dosephase2': dosephase2,
                                               'fxphase2': fxphase2,
                                               'totaldose': dosephase1 + dosephase2,
                                               'totalfractions': fxphase1 + fxphase2,
                                               'volumes': volumes
                                               })

        else:
            form = SimulationForm()

        # return render(request, 'patient_data/radonc_simulation.html', {'form': form, 'presimstatus': presimstatus,
        #                                                                'error_msg': error_msg,
        #                                                                'error_status': error_status})
        return render(request, 'patient_data/partials/partial_simulation.html',
                      {'form': form, 'presimstatus': presimstatus,
                       'error_msg': error_msg,
                       'error_status': error_status})


def simulation2(request, crnumber=None, s3_id=None, presimid=None):
    if request.method == "POST":
        # Getting emails of all the users
        all_users = User.objects.filter(is_active=True)
        emails = [m.email for m in all_users]
        # Getting current user
        current_user = User.objects.get(id=request.user.id)
        # Copying request data otherwise it will not work
        # Ref: https://stackoverflow.com/questions/8241001/how-do-i-modify-the-bound-value-for-a-field-in-a-bound-form-in-django
        data = request.POST.copy()
        form = SimulationForm(data=data)
        try:
            assignedto_id = request.POST['assignedto']
            assigned_to = User.objects.get(pk=assignedto_id)
            assignedto_user = assigned_to.username
        except ValueError:
            assigned_to = User.objects.get(pk=1)
            assignedto_user = assigned_to.username
            messages.warning(request, f"This case was not assigned: Using default user: {assignedto_user} ")
            form.data['assignedto'] = assigned_to

        # Setting value of user column to current user
        form.data['user'] = current_user.pk
        if s3_id is not None:
            form.data['s3_id'] = s3_id
            mx_details = S3CarePlan.objects.get(pk=s3_id)
            s2_id = mx_details.s2_id.s2_id
            form.data['s2_id'] = s2_id

        if form.is_valid():
            crn = form.data.get('simparent')
            form.save()

            mail_status = form.cleaned_data.get('send_mail')
            ctx = {'crnumber': form.cleaned_data.get('simparent'),
                   'simdate': form.cleaned_data.get('simdate'),
                   'impdate': form.cleaned_data.get('impdate'),
                   'site': form.cleaned_data.get('site'),
                   'technique': form.cleaned_data.get('technique'),
                   'intent': form.cleaned_data.get('intent'),
                   'dosephase1': form.cleaned_data.get('dosephase1'),
                   'fxphase1': form.cleaned_data.get('fxphase1'),
                   'dosephase2': form.cleaned_data.get('dosephase2'),
                   'fxphase2': form.cleaned_data.get('fxphase2'),
                   'dosephase3': form.cleaned_data.get('dosephase3'),
                   'fxphase3': form.cleaned_data.get('fxphase3'),
                   'dosephase4': form.cleaned_data.get('dosephase4'),
                   'fxphase4': form.cleaned_data.get('fxphase4'),
                   'totaldose': form.cleaned_data.get('totaldose'),
                   'totalfractions': form.cleaned_data.get('totalfractions'),
                   'assignedto': form.cleaned_data.get('assignedto'),
                   'tentativecompletiondate': form.cleaned_data.get('tentativecompletiondate'),
                   'user': form.cleaned_data.get('user'),
                   'remarks': form.cleaned_data.get('remarks')
                   }
            message = get_template("patient_data/mail.html").render(ctx)
            if mail_status:
                msg = EmailMessage(
                    subject='New Simulation Details',
                    body=message,
                    from_email='rgcirtoffice@gmail.com',
                    to=emails,
                )
                msg.content_subtype = "html"
                msg.send()
            messages.success(request,
                             f'Data has been saved for CRNumber: {crn} and is assigned to: {assignedto_user}')
            return redirect('radonc-simulation-list', crn)
        else:
            print(form.errors)

    else:
        initialstatus = "Simulation"
        simdate = timezone.now().date()
        icdmainsite = ""
        site = ""
        technique = ""
        intent = ""
        dosephase1 = ""
        fxphase1 = ""
        dosephase2 = ""
        fxphase2 = ""
        volumes = ""
        if s3_id:
            patient_cp = S3CarePlan.objects.select_related().get(pk=s3_id)
            if patient_cp.s2_id.diagnosis.our_diagnosis == "Breast" and patient_cp.radiotherapy == "Adjuvant":
                dosephase1 = 42.5
                fxphase1 = 16
                if patient_cp.s2_id.laterality == "Right":
                    icdmainsite = 73124
                    site = "Right Breast"
                    technique = "IMRT-FIF"
                    intent = "Adjuvant"
                if patient_cp.surgery:
                    patient_sx = S6Surgery.objects.select_related().filter(s3_id=s3_id).first()
                    patient_hpe = S6HPE.objects.select_related().filter(s6_id=patient_sx.pk).first()
                    if patient_sx.sxtype:
                        for surgery in patient_sx.sxtype.all():
                            if patient_hpe:
                                if surgery.surgery.startswith("Lumpectomy"):
                                    if patient_hpe.hpegrade.code == "Grade3" or patient_cp.parent_id.age < 50:
                                        dosephase2 = 10
                                        fxphase2 = 4
                                    if patient_hpe.nodesp / patient_hpe.nodesr >= 0.5:
                                        volumes = "B-SCF-AX1,2,3-IMC"
                                    else:
                                        volumes = "B-SCF-AX3"
                            else:
                                if patient_hpe:
                                    if patient_hpe.nodesp / patient_hpe.nodesr >= 0.5:
                                        volumes = "CW-SCF-AX1,2,3-IMC"
                                    else:
                                        volumes = "CW-SCF-AX3"
        presimstatus = False
        utc = pytz.UTC
        end_date = utc.localize(datetime.datetime.today())
        start_date = datetime.datetime.today() - datetime.timedelta(14)
        start_date = utc.localize(start_date)
        mx_details = S3CarePlan.objects.get(pk=s3_id)
        s2_id = mx_details.s2_id.s2_id
        error_msg = ""
        error_status = False
        if crnumber:
            if not dosephase1:
                dosephase1 = 0
            if not dosephase2:
                dosephase2 = 0
            if not fxphase1:
                fxphase1 = 0
            if not fxphase2:
                fxphase2 = 0
            patient = S1ParentMain.objects.filter(crnumber=crnumber).first()
            if patient.last_name:
                name = patient.first_name + " " + patient.last_name
            else:
                name = patient.first_name
            if presimid:
                presimstatus = True
                pat_presim = NewPreSimulation.objects.get(pk=presimid)
                # print(pat_presim.final_status)
                if pat_presim.final_status is None or pat_presim.final_status == "":
                    error_msg = "Final Status not mentioned in presimulation module. Pleaase complete it and then proceed"
                    error_status = True
                icdmainsite = 73125
                site = "Left Breast"
                intent = "Adjuvant"
                form = SimulationForm(initial={'simparent': crnumber,
                                               'name': name,
                                               's3_id': mx_details.s3_id,
                                               's2_id': s2_id,
                                               'presimid': presimid,
                                               'technique': pat_presim.final_status,
                                               'simdate': simdate,
                                               'initialstatus': initialstatus,
                                               'site': icdmainsite,
                                               'icdmainsite': site,
                                               'intent': intent,
                                               'dosephase1': dosephase1,
                                               'fxphase1': fxphase1,
                                               'dosephase2': dosephase2,
                                               'fxphase2': fxphase2,
                                               'totaldose': dosephase1 + dosephase2,
                                               'totalfractions': fxphase1 + fxphase2,
                                               'volumes': volumes
                                               })

            else:
                form = SimulationForm(initial={'simparent': crnumber,
                                               'name': name,
                                               's3_id': mx_details.s3_id,
                                               's2_id': s2_id,
                                               'simdate': simdate,
                                               'initialstatus': initialstatus,
                                               'site': site,
                                               'icdmainsite': icdmainsite,
                                               'technique': technique,
                                               'intent': intent,
                                               'dosephase1': dosephase1,
                                               'fxphase1': fxphase1,
                                               'dosephase2': dosephase2,
                                               'fxphase2': fxphase2,
                                               'totaldose': dosephase1 + dosephase2,
                                               'totalfractions': fxphase1 + fxphase2,
                                               'volumes': volumes
                                               })

        else:
            form = SimulationForm()

        return render(request, 'patient_data/radonc_simulation.html', {'form': form, 'presimstatus': presimstatus,
                                                                       'error_msg': error_msg,
                                                                       'error_status': error_status,
                                                                       'crnumber': crnumber,
                                                                       's3_id': s3_id})
        # return render(request, 'patient_data/partials/partial_simulation.html',
        #               {'form': form, 'presimstatus': presimstatus,
        #                'error_msg': error_msg,
        #                'error_status': error_status})


class SimulationListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Simulation
    template_name = 'patient_data/radonc_simulation_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return Simulation.objects.filter(simparent=self.kwargs['crnumber'])

    def get_context_data(self, **kwargs):
        context = super(SimulationListView, self).get_context_data(**kwargs)
        rt_simids = []
        rt_id = {}
        for sim in context['data']:
            rt_details = S4RT.objects.filter(simid=sim.simid)
            for rt in rt_details:
                if rt.simid.simid == sim.simid:
                    rt_simids.append(rt.simid.simid)
                    rt_id[rt.simid.simid] = rt.s4_id
        context['rt_simids'] = rt_simids
        context['rt_id'] = rt_id
        context['crnumber'] = self.kwargs['crnumber']
        try:
            if self.kwargs['rt']:
                context['rt'] = self.kwargs['rt']
        except:
            pass
        # print(context['data'][0].simid)
        return context


class SimulationUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Simulation
    form_class = modelform_factory(Simulation, SimulationForm)
    template_name = "patient_data/radonc_simulation.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        all_users = User.objects.all()
        emails = [m.email for m in all_users]
        # print(emails)
        pk = self.kwargs["pk"]
        patient = Simulation.objects.get(pk=pk)
        # assignedto_id = patient.assignedto.id
        # if assignedto_id:
        #     assigned_user = User.objects.get(pk=assignedto_id)
        #     form.instance.assignedto = assigned_user
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.updated_by = current_user.username
        form.instance.user = patient.user
        if patient.send_mail:
            msg = EmailMessage(
                subject='New Simulation Details',
                body="TEST MAIL",
                from_email='rgcirtoffice@gmail.com',
                to=['kundan25@gmail.com'],
            )
            msg.content_subtype = "html"
            # msg.send()
            # print(msg.send())

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Simulation.objects.get(pk=pk)
        try:
            rt = patient.s4rt_set.get(simid_id=pk)
            simstatus = patient.initialstatus
            rt_status = rt.rtstatus

            if simstatus.status.startswith("Start"):
                S4RT.objects.filter(simid_id=pk).update(rtstatus=0)
            elif simstatus.status.startswith("Completed"):
                S4RT.objects.filter(simid_id=pk).update(rtstatus=1)
            elif simstatus.status.startswith("Cancelled"):
                S4RT.objects.filter(simid_id=pk).update(rtstatus=8)
            elif simstatus.status.__contains__("Defaulted"):
                S4RT.objects.filter(simid_id=pk).update(rtstatus=8)
            elif simstatus.status.startswith("Simulation"):
                S4RT.objects.filter(simid_id=pk).update(rtstatus=10)
            else:
                pass


        except ObjectDoesNotExist:
            pass

        crn = patient.simparent.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        return reverse_lazy("radonc-simulation-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(SimulationUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = Simulation.objects.get(pk=pk)
        try:
            rt = patient.s4rt_set.get(simid_id=pk)
        except:
            rt = False
        if patient.presimid:
            presimstatus = True
        else:
            presimstatus = False
        updatecrn = patient.simparent.pk
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['rtdetails'] = rt
        context['presimstatus'] = presimstatus
        return context

    def form_invalid(self, form):
        # print(form.data)
        print(f'This is the ERROR{form.errors}')
        print(form.data)
        return form.errors


class SimulationDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Simulation
    template_name = "patient_data/radonc_simulation_confirm_delete.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Simulation.objects.get(pk=pk)
        crn = patient.simparent.crnumber
        s3_id = patient.s3_id.s3_id
        return reverse_lazy("new-simulation", kwargs={"crnumber": crn, 's3_id': s3_id})

    # def get_queryset(self):
    #     pk = self.kwargs["pk"]
    #     patient = PreSimulation.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        patient = Simulation.objects.get(pk=pk)
        crn = patient.simparent.crnumber
        s3_id = patient.s3_id.s3_id
        try:
            patient.delete()
        except IntegrityError:
            messages.error(self.request, f"{crn}: Cannot Delete as RT Details for this Simulation already exists!!")
            return redirect("new-simulation", crn, s3_id)
        messages.success(self.request, f"Patient's ({crn}) presimulation detail got deleted")
        return redirect("new-simulation", crn, s3_id)
        # return render(request, 'patient_data/error.html')


# NEW SIMULATION VIEWS
def new_simulation(request, crnumber, s3_id):
    cp = S3CarePlan.objects.get(pk=s3_id)
    sx = cp.s6surgery_set.all()
    form = NewPreSimulationForm()
    if Simulation.objects.filter(s3_id=s3_id).exists():
        sim = Simulation.objects.filter(s3_id=s3_id).all()
    else:
        sim = None
    if NewPreSimulation.objects.filter(s3_id=s3_id).exists():
        presim = NewPreSimulation.objects.filter(s3_id=s3_id)
    else:
        presim = None

    # Presim with no careplan
    presim_no_careplan = NewPreSimulation.objects.filter(s3_id__isnull=True, presimparent_id=crnumber)

    # Simulations with no careplan
    sim_no_careplan = Simulation.objects.filter(s3_id__isnull=True, simparent=crnumber)

    # print(f"NEW-SIMULATION{request.POST}")

    # if "save" in request.POST:
    #     data = request.POST.copy()
    #     form = NewPreSimulationForm(data=data)
    #     # print(request.POST)
    #     crn = form.data.get('presimparent')
    #     day = form.data.get('day')
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,
    #                          f'DIBH assessment details has been saved for CRNumber: {crn} for DAY-{day}')
    #         return render(request, 'patient_data/partials/partial_presim_display.html',
    #                       {'crnumber': crnumber,
    #                        's3_id': s3_id})
    #     else:
    #         print(form.errors)
    #         error = form.errors
    #         return render(request, 'patient_data/partials/partial_presim_display.html',
    #                       {'crnumber': crnumber,
    #                        's3_id': s3_id,
    #                        'error': error})
    if "to_sim" in request.POST:
        data = request.POST.copy()
        form = NewPreSimulationForm(data=data)
        day = form.data.get('day')
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'DIBH assessment details has been saved for CRNumber: {crnumber} for DAY-{day}')
            presim = NewPreSimulation.objects.filter(presimparent=crnumber).last()
            return redirect('radonc-simulation2', crnumber, s3_id, presim.pk)
        else:
            print(form.errors)

    if "save_sim" in request.POST:
        # Getting emails of all the users
        all_users = User.objects.filter(is_active=True)
        emails = [m.email for m in all_users]
        # Getting current user
        current_user = User.objects.get(id=request.user.id)
        # Copying request data otherwise it will not work
        # Ref: https://stackoverflow.com/questions/8241001/how-do-i-modify-the-bound-value-for-a-field-in-a-bound-form-in-django
        data = request.POST.copy()
        form = SimulationForm(data=data)
        try:
            assignedto_id = request.POST['assignedto']
            assigned_to = User.objects.get(pk=assignedto_id)
            assignedto_user = assigned_to.username
        except ValueError:
            assigned_to = User.objects.get(pk=1)
            assignedto_user = assigned_to.username
            messages.warning(request, f"This case was not assigned: Using default user: {assignedto_user} ")
            form.data['assignedto'] = assigned_to

        # Setting value of user column to current user
        form.data['user'] = current_user.pk
        if s3_id is not None:
            form.data['s3_id'] = s3_id
            mx_details = S3CarePlan.objects.get(pk=s3_id)
            s2_id = mx_details.s2_id.s2_id
            form.data['s2_id'] = s2_id

        if form.is_valid():
            crn = form.data.get('simparent')
            form.save()

            mail_status = form.cleaned_data.get('send_mail')
            ctx = {'crnumber': form.cleaned_data.get('simparent'),
                   'simdate': form.cleaned_data.get('simdate'),
                   'impdate': form.cleaned_data.get('impdate'),
                   'site': form.cleaned_data.get('site'),
                   'technique': form.cleaned_data.get('technique'),
                   'intent': form.cleaned_data.get('intent'),
                   'dosephase1': form.cleaned_data.get('dosephase1'),
                   'fxphase1': form.cleaned_data.get('fxphase1'),
                   'dosephase2': form.cleaned_data.get('dosephase2'),
                   'fxphase2': form.cleaned_data.get('fxphase2'),
                   'dosephase3': form.cleaned_data.get('dosephase3'),
                   'fxphase3': form.cleaned_data.get('fxphase3'),
                   'dosephase4': form.cleaned_data.get('dosephase4'),
                   'fxphase4': form.cleaned_data.get('fxphase4'),
                   'totaldose': form.cleaned_data.get('totaldose'),
                   'totalfractions': form.cleaned_data.get('totalfractions'),
                   'assignedto': form.cleaned_data.get('assignedto'),
                   'tentativecompletiondate': form.cleaned_data.get('tentativecompletiondate'),
                   'user': form.cleaned_data.get('user'),
                   'remarks': form.cleaned_data.get('remarks')
                   }
            message = get_template("patient_data/mail.html").render(ctx)
            if mail_status:
                msg = EmailMessage(
                    subject='New Simulation Details',
                    body=message,
                    from_email='rgcirtoffice@gmail.com',
                    to=emails,
                )
                msg.content_subtype = "html"
                msg.send()
            messages.success(request,
                             f'Data has been saved for CRNumber: {crn} and is assigned to: {assignedto_user}')
            if s3_id is not None:
                return redirect('new-simulation', crn, s3_id)
            else:
                return redirect('radonc-simulation-list', crn)
        else:
            print(form.errors)
    return render(request, 'patient_data/new_simulation.html', {'cp': cp, 's3_id': s3_id, 'sx': sx,
                                                                'crnumber': crnumber, 'form': form,
                                                                'sim': sim, 'presim': presim,
                                                                'presim_no_careplan': presim_no_careplan,
                                                                'sim_no_careplan': sim_no_careplan})


class RadiotherapyCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S4RT
    form_class = modelform_factory(S4RT, S4RTForm)
    template_name = "patient_data/radonc_radiotherapy.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        simid = self.kwargs['simid']
        patient_rt = S4RT.objects.get(simid=simid)

        if patient_rt.rtstatus.code == patient_rt.simid.initialstatus.status:
            messages.warning(self.request,
                             f'SIMULATION & RT STATUS MATCH. NO ACTION REQUIRED. Simulation status is '
                             f'{patient_rt.simid.initialstatus.status} and '
                             f'RTStatus is {patient_rt.rtstatus.code}')
        else:
            messages.error(self.request,
                           f'SIMULATION & RT STATUS DOES NOT MATCH! PLEASE CHANGE EITHER TO MATCH'
                           f'-- Simulation status is '
                           f'{patient_rt.simid.initialstatus.status} while '
                           f'RTStatus is {patient_rt.rtstatus.code}')
        return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(RadiotherapyCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        simid = self.kwargs['simid']
        patient = S1ParentMain.objects.get(crnumber=crnumber)
        patient_sim = patient.simulation_set.get(pk=simid)

        class RTForm(S4RTForm):
            def __init__(self, *args, **kwargs):
                super(RTForm, self).__init__(*args, **kwargs)

        form = RTForm()
        context['form'] = form
        context['patient'] = patient
        context['patient_sim'] = patient_sim
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s2_id'] = patient_sim.s2_id.s2_id
        context['form'].initial['s3_id'] = patient_sim.s3_id.s3_id
        context['form'].initial['simid'] = patient_sim.simid
        context['form'].initial['simdate'] = patient_sim.simdate
        context['form'].initial['rtstartdate'] = patient_sim.impdate
        context['form'].initial['rtsite_main'] = patient_sim.icdmainsite.all()
        context['form'].initial['rtindication'] = patient_sim.intent
        context['form'].initial['rtstatus'] = patient_sim.initialstatus.code
        # context['form'].initial['s3_id'] = patient.s3careplan_set.s3_id

        if patient_sim.initialstatus.status.startswith("Start"):
            context['form'].initial['rtstatus'] = 0
        elif patient_sim.initialstatus.status.startswith("Completed"):
            context['form'].initial['rtstatus'] = 1
        elif patient_sim.initialstatus.status.startswith("Cancelled"):
            context['form'].initial['rtstatus'] = 8
        elif patient_sim.initialstatus.status.__contains__("Defaulted"):
            context['form'].initial['rtstatus'] = 8
        elif patient_sim.initialstatus.status.startswith("Simulation"):
            context['form'].initial['rtstatus'] = 10
        else:
            pass
        # context['form'].initial['rtstatus'] = patient_sim.initialstatus
        if patient_sim.dosephase1:
            context['form'].initial['rtdose1'] = patient_sim.dosephase1
            context['form'].initial['rtdosefr1'] = patient_sim.fxphase1
            context['form'].initial['tech1'] = patient_sim.technique
            context['form'].initial['modality1'] = "Photons"
        if patient_sim.dosephase2:
            context['form'].initial['rtdose2'] = patient_sim.dosephase2
            context['form'].initial['rtdosefr2'] = patient_sim.fxphase2
            context['form'].initial['tech2'] = patient_sim.technique
            context['form'].initial['modality2'] = "Photons"
        if patient_sim.dosephase3:
            context['form'].initial['rtdose3'] = patient_sim.dosephase3
            context['form'].initial['rtdosefr3'] = patient_sim.fxphase3
            context['form'].initial['tech3'] = patient_sim.technique
            context['form'].initial['modality3'] = "Photons"
        if patient_sim.dosephase4:
            context['form'].initial['rtdose4'] = patient_sim.dosephase3
            context['form'].initial['rtdosefr4'] = patient_sim.fxphase3
            context['form'].initial['tech4'] = patient_sim.technique
            context['form'].initial['modality4'] = "Photons"
        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class RadiotherapyListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S4RT
    template_name = 'patient_data/radonc_s4_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(RadiotherapyListView, self).get_context_data(**kwargs)
        patient_ass = S7Assessment.objects.filter(parent_id=self.kwargs['crnumber'])

        if patient_ass:
            ass = True
        else:
            ass = False

        context['crnumber'] = self.kwargs['crnumber']
        context['patient_mx'] = patient_ass
        context['ass'] = ass
        return context

    def get_queryset(self):
        return S4RT.objects.filter(parent_id=self.kwargs['crnumber'])


class RadiotherapyUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S4RT
    form_class = modelform_factory(S4RT, S4RTForm)
    template_name = "patient_data/radonc_radiotherapy.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S4RT.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S4RT.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        patient = S4RT.objects.get(pk=pk)
        if patient.rtstatus.code == patient.simid.initialstatus.status:
            messages.warning(self.request,
                             f'SIMULATION & RT STATUS MATCH. NO ACTION REQUIRED. Simulation status is '
                             f'{patient.simid.initialstatus.status} and '
                             f'RTStatus is {patient.rtstatus.code}')
        else:
            messages.error(self.request,
                           f'SIMULATION & RT STATUS DOES NOT MATCH! PLEASE CHANGE EITHER TO MATCH'
                           f'-- Simulation status is '
                           f'{patient.simid.initialstatus.status} while '
                           f'RTStatus is {patient.rtstatus.code}')
        if self.request.POST.get('careplan'):
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})
        else:
            return reverse_lazy("radonc-database-home", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(RadiotherapyUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S4RT.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        patient_rt = S1ParentMain.objects.get(crnumber=updatecrn)

        all_dx = patient_rt.s2diagnosis_set.all()
        all_mx = patient_rt.s3careplan_set.all()
        all_rt = patient_rt.s4rt_set.all()
        all_sim = patient_rt.simulation_set.all()

        dx_choices = []
        for dx in all_dx:
            dx_choices.append((dx.s2_id, dx.s2_id))

        mx_choices = []
        for mx in all_mx:
            mx_choices.append((mx.s3_id, mx.s3_id))
        sim_choices = []
        for sim in all_sim:
            sim_choices.append((sim.simid, sim.simid))

        context['form'].fields['s3_id'].choices = mx_choices
        context['form'].fields['s2_id'].choices = dx_choices
        context['form'].fields['simid'].choices = sim_choices
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['all_rt'] = all_rt
        return context


# DVH Details
class PrimaryDVHCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PrimaryDVH
    form_class = modelform_factory(PrimaryDVH, PrimaryDVHForm)
    template_name = "patient_data/primarydvh.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s4_id']
        rtdetails = S4RT.objects.get(pk=pk)
        crn = rtdetails.parent_id.crnumber
        return reverse_lazy("radonc-primarydvh", kwargs={"s4_id": pk})

    def get_context_data(self, **kwargs):
        context = super(PrimaryDVHCreateView, self).get_context_data(**kwargs)
        pk = self.kwargs['s4_id']

        rtdetails = S4RT.objects.get(pk=pk)
        patient = S1ParentMain.objects.get(crnumber=rtdetails.parent_id.crnumber)
        context['form'].initial['s4_id'] = rtdetails.s4_id
        context['crnumber'] = rtdetails.parent_id.crnumber
        context['patient'] = patient
        context['s4_id'] = pk

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


# SURGERY
class SurgeryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S6Surgery
    form_class = modelform_factory(S6Surgery, S6SurgeryForm)
    template_name = "patient_data/radonc_surgery.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(SurgeryCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s3_id = self.kwargs['s3_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        # patient_sim = patient.simulation_set.get(pk=simid)

        class SurgeryForm(S6SurgeryForm):
            def __init__(self, *args, **kwargs):
                super(SurgeryForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = SurgeryForm()
        context['form'] = form
        context['patient'] = patient
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s3_id'] = s3_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class SurgeryListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S6Surgery
    template_name = 'patient_data/radonc_s6_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(SurgeryListView, self).get_context_data(**kwargs)
        crnumber = self.kwargs["crnumber"]
        patient_sx = S1ParentMain.objects.get(crnumber=crnumber)
        try:
            all_hpe = patient_sx.s6hpe_set.all()
        except:
            all_hpe = False
        try:
            all_sx = patient_sx.s6surgery_set.all()
        except:
            all_sx = False

        if all_sx:
            # sxids = []
            # for sx_details in all_sx:
            #     sxids.append(sx_details.sx_id)
            if all_hpe:
                hpeids = []
                for hpe_details in all_hpe:
                    hpeids.append(hpe_details.s6_id.s6_id)
                    context['hpeids'] = hpeids
            # print(all_sx[0].s6hpe_set.all())
        return context

    def get_queryset(self):
        return S6Surgery.objects.filter(parent_id=self.kwargs['crnumber'])


class SurgeryUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S6Surgery
    form_class = modelform_factory(S6Surgery, S6SurgeryForm)
    template_name = "patient_data/radonc_surgery.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S6Surgery.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S6Surgery.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-surgery-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(SurgeryUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S6Surgery.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        # patient_sx = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        return context


# HPE Details

class HPECreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S6HPE
    form_class = modelform_factory(S6HPE, S6HPEForm)
    template_name = "patient_data/radonc_hpe.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        return reverse_lazy("radonc-hpe-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(HPECreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s6_id = self.kwargs['s6_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)
        patient_sx = S6Surgery.objects.get(pk=s6_id)

        # patient_sim = patient.simulation_set.get(pk=simid)

        class HPEFormNew(S6HPEForm):
            def __init__(self, *args, **kwargs):
                super(HPEFormNew, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = HPEFormNew()
        context['form'] = form
        context['patient'] = patient
        context['patient_sx'] = patient_sx
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s6_id'] = s6_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class HPEListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S6HPE
    template_name = 'patient_data/radonc_s6hpe_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return S6HPE.objects.filter(parent_id=self.kwargs['crnumber'])


class HPEUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S6HPE
    form_class = modelform_factory(S6HPE, S6HPEForm)
    template_name = "patient_data/radonc_hpe.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S6HPE.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S6HPE.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-hpe-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(HPEUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S6HPE.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        patient_hpe = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        return context


# CHEMOTHERAPY

class ChemotherapyCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S5Chemo
    form_class = modelform_factory(S5Chemo, S5ChemoForm)
    template_name = "patient_data/radonc_chemotherapy.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']
        # s3_id = self.kwargs['s3_id']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        return reverse_lazy("radonc-chemotherapy-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(ChemotherapyCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s3_id = self.kwargs['s3_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class ChemoForm(S5ChemoForm):
            def __init__(self, *args, **kwargs):
                super(ChemoForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = ChemoForm()
        context['form'] = form
        context['patient'] = patient
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s3_id'] = s3_id

        if S5Chemo.objects.filter(parent_id=crnumber).exists():
            last_chemo = S5Chemo.objects.filter(parent_id=crnumber).last()
            last_chemo_dict = model_to_dict(last_chemo)
            context['previous_chemo'] = True
            for field in context['form'].fields:
                context['form'].initial[field] = last_chemo_dict[field]

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class ChemotherapyListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S5Chemo
    template_name = 'patient_data/radonc_s5_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return S5Chemo.objects.filter(parent_id=self.kwargs['crnumber'])


class ChemotherapyUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S5Chemo
    form_class = modelform_factory(S5Chemo, S5ChemoForm)
    template_name = "patient_data/radonc_chemotherapy.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S5Chemo.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S5Chemo.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-chemotherapy-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(ChemotherapyUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S5Chemo.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        patient_ch = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        return context


class ChemotherapyDeleteView(LoginRequiredMixin, DeleteView):
    model = S5Chemo

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S5Chemo.objects.get(pk=pk)
        return reverse_lazy("radonc-chemotherapy-list", kwargs={"crnumber": patient.parent_id.crnumber})


# NEW CHEMOTHERAPY VIEWS
class ChemoProtocolCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S5ChemoProtocol
    form_class = modelform_factory(S5ChemoProtocol, S5ChemoProtocolForm)
    template_name = "patient_data/chemo_protocol_module.html"
    success_message = "Chemo Protocol Created Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        s3_id = self.kwargs['s3_id']
        return reverse_lazy("radonc-chemoprotocol", kwargs={"crnumber": crn, 's3_id': s3_id})

    def get_context_data(self, **kwargs):
        context = super(ChemoProtocolCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s3_id = self.kwargs['s3_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class ChemoProtocolForm(S5ChemoProtocolForm):
            def __init__(self, *args, **kwargs):
                super(ChemoProtocolForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = ChemoProtocolForm()
        context['form'] = form
        context['patient'] = patient
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s3_id'] = s3_id

        if S5ChemoProtocol.objects.filter(parent_id=crnumber).exists():
            protocols = S5ChemoProtocol.objects.filter(parent_id=crnumber).all()
            last_protocol = protocols.last()
            last_protocol_dict = model_to_dict(last_protocol)
            context['previous_protocol'] = True
            context['protocols'] = protocols
            for field in context['form'].fields:
                context['form'].initial[field] = last_protocol_dict[field]

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class ChemoProtocolUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S5ChemoProtocol
    form_class = modelform_factory(S5ChemoProtocol, S5ChemoProtocolForm)
    template_name = "patient_data/chemo_protocol_module.html"
    success_message = "Chemo Protocol Updated Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S5ChemoProtocol.objects.get(pk=pk)
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S5ChemoProtocol.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-chemoprotocol", kwargs={"crnumber": crn,
                                                            's3_id': patient.s3_id.s3_id})

    def get_context_data(self, **kwargs):
        context = super(ChemoProtocolUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S5ChemoProtocol.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        return context


class ChemoProtocolDeleteView(LoginRequiredMixin, DeleteView):
    model = S5ChemoProtocol

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S5ChemoProtocol.objects.get(pk=pk)
        return reverse_lazy("radonc-chemoprotocol",
                            kwargs={"crnumber": patient.parent_id.crnumber, 's3_id': patient.s3_id.s3_id})


# ASSESSMENT Details
class AssCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S7Assessment
    form_class = modelform_factory(S7Assessment, S7AssessmentForm)
    template_name = "patient_data/radonc_assessment.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']
        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        s4_id = self.kwargs["s4_id"]
        rt_details = S4RT.objects.get(pk=s4_id)
        sim_details = Simulation.objects.get(pk=rt_details.simid.simid)
        sim_details.donefr = self.request.POST['fxdone']
        sim_details.as_date = self.request.POST['as_date']
        sim_details.save()
        if 'to_other' in self.request.POST:
            ass = rt_details.s7assessment_set.all().last()
            return reverse_lazy("radonc-ass-update", kwargs={"pk": ass.pk})
        return reverse_lazy("radonc-ass-list", kwargs={"s4_id": s4_id})

    def get_context_data(self, **kwargs):
        context = super(AssCreateView, self).get_context_data(**kwargs)
        s4_id = self.kwargs["s4_id"]
        rt_details = S4RT.objects.get(pk=s4_id)
        crnumber = rt_details.parent_id.crnumber
        patient = S1ParentMain.objects.get(crnumber=crnumber)
        # patient_sim = patient.simulation_set.get(pk=simid)

        rt_choices = [(rt_details.s4_id, rt_details.s4_id)]

        class ASSFormNew(S7AssessmentForm):
            def __init__(self, *args, **kwargs):
                super(ASSFormNew, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)
                self.fields['s4_id'].choices = rt_choices

        form = ASSFormNew()
        context['form'] = form
        context['patient'] = patient
        context['crnumber'] = crnumber
        context['form'].initial['parent_id'] = crnumber
        context['rtdetails'] = rt_details
        context['create'] = True

        return context

    def form_invalid(self, form):
        s4_id = self.kwargs["s4_id"]
        error = form['as_date'].errors
        messages.warning(self.request, error)
        return redirect('radonc-ass', s4_id)


class AssListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S7Assessment
    template_name = 'patient_data/radonc_s7_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return S7Assessment.objects.filter(s4_id=self.kwargs['s4_id'])


class AssUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S7Assessment
    form_class = modelform_factory(S7Assessment, S7AssessmentForm)
    template_name = "patient_data/radonc_assessment.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S7Assessment.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S7Assessment.objects.get(pk=pk)
        # patient = PatientDiagnosis.objects.get(pk=pk)
        # patient.updated_by = self.request.user.username
        # patient.save()
        # sim_details = Simulation.objects.get(pk=patient.s4_id.simid.simid)
        # sim_details.donefr = self.request.POST['fxdone']
        # sim_details.as_date = self.request.POST['as_date']
        # sim_details.save()
        return reverse_lazy("radonc-ass-list", kwargs={"s4_id": patient.s4_id.s4_id})

    def get_context_data(self, **kwargs):
        context = super(AssUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S7Assessment.objects.get(pk=pk)
        pk_s1 = patient.parent_id.pk
        updatecrn = patient.parent_id.crnumber

        rt_choices = [(patient.s4_id.s4_id, patient.s4_id.s4_id)]

        context['form'].fields['s4_id'].choices = rt_choices
        context['form'].initial['updated_by'] = self.request.user.username
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s7_id'] = pk
        return context


# RT ASSESSMENT PRESCRIPTION VIEWS
class RTPrescriptionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = modelform_factory(Prescription, PrescriptionForm)
    template_name = "patient_data/prescription.html"
    success_message = "RT Prescription Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s7_id']
        as_details = S7Assessment.objects.get(s7_id=pk)
        s4_id = as_details.s4_id.s4_id
        crn = as_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-ass-list", kwargs={"s4_id": s4_id})

    def get_context_data(self, **kwargs):
        context = super(RTPrescriptionCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s7_id = self.kwargs['s7_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class PresForm(PrescriptionForm):
            def __init__(self, *args, **kwargs):
                super(PresForm, self).__init__(*args, **kwargs)

        form = PresForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s7_id'] = s7_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s7_id'] = s7_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class RTPrescriptionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = modelform_factory(Prescription, PrescriptionForm)
    template_name = "patient_data/prescription.html"
    success_message = "RT Prescription Updated Successfully!"
    context_object_name = 'view_data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-ass-update", kwargs={"pk": self.request.POST['s7_id']})

    def get_context_data(self, **kwargs):
        context = super(RTPrescriptionUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        drug = patient.drug_name.split(" ")[0]
        drug_name = GenDrugs.objects.filter(drug=drug).first()

        context['form'].initial['drug_name'] = drug_name
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s7_id'] = patient.s7_id.s7_id
        return context


class RTPrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s7_id.s7_id})


# RT ASSESSMENT IMAGING VIEWS

class RTInvImgCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsImaging
    form_class = modelform_factory(InvestigationsImaging, InvestigationsImagingForm)
    template_name = "patient_data/invimgdetails.html"
    success_message = "Imaging Details for RT Assessment Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s7_id']
        as_details = S7Assessment.objects.get(s7_id=pk)
        s4_id = as_details.s4_id.s4_id
        crn = as_details.parent_id.crnumber
        if "to_ass" in self.request.POST:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})

        return reverse_lazy("radonc-ass-list", kwargs={"crnumber": s4_id})

    def get_context_data(self, **kwargs):
        context = super(RTInvImgCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s7_id = self.kwargs['s7_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class InvForm(InvestigationsImagingForm):
            def __init__(self, *args, **kwargs):
                super(InvForm, self).__init__(*args, **kwargs)

        form = InvForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s7_id'] = s7_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s7_id'] = s7_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class RTInvImgUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsImaging
    form_class = modelform_factory(InvestigationsImaging, InvestigationsImagingForm)
    template_name = "patient_data/invimgdetails.html"
    context_object_name = 'data'
    success_message = "Imaging Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-ass-update", kwargs={"pk": self.request.POST['s7_id']})

    def get_context_data(self, **kwargs):
        context = super(RTInvImgUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s7_id'] = patient.s7_id.s7_id
        return context


class RTInvImgDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsImaging

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s7_id.s7_id})


# RT INVESTIGATION PATHLAB DETAILS
class RTInvPathlabCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsPath
    form_class = modelform_factory(InvestigationsPath, InvestigationsPathForm)
    template_name = "patient_data/invpathdetails.html"
    success_message = "Pathology Details Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s7_id']
        as_details = S7Assessment.objects.get(s7_id=pk)
        s4_id = as_details.s4_id.s4_id
        crn = as_details.parent_id.crnumber
        if "to_ass" in self.request.POST:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-ass-list", kwargs={"s4_id": s4_id})

    def get_context_data(self, **kwargs):
        context = super(RTInvPathlabCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s7_id = self.kwargs['s7_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class PathForm(InvestigationsPathForm):
            def __init__(self, *args, **kwargs):
                super(PathForm, self).__init__(*args, **kwargs)

        form = PathForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s7_id'] = s7_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s7_id'] = s7_id
        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class RTInvPathlabUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsPath
    form_class = modelform_factory(InvestigationsPath, InvestigationsPathForm)
    template_name = "patient_data/invpathdetails.html"
    success_message = "Pathlab Investigation Updated Successfully!"
    context_object_name = 'view_data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-ass-update", kwargs={"pk": self.request.POST['s7_id']})

    def get_context_data(self, **kwargs):
        context = super(RTInvPathlabUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s7_id'] = patient.s7_id.s7_id
        return context


class RTInvPathlabDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsPath

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s7_id.s7_id})


# RT INVESTIGATION BASIC LAB DETAILS
class RTInvLabsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsLabs
    form_class = modelform_factory(InvestigationsLabs, InvestigationsLabsForm)
    template_name = "patient_data/invlabdetails.html"
    success_message = "Lab Report Created Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s7_id']
        as_details = S7Assessment.objects.get(s7_id=pk)
        s4_id = as_details.s4_id.s4_id
        crn = as_details.parent_id.crnumber
        if "to_ass" in self.request.POST:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-ass-list", kwargs={"s4_id": s4_id})

    def get_context_data(self, **kwargs):
        context = super(RTInvLabsCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s7_id = self.kwargs['s7_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class InvLabForm(InvestigationsLabsForm):
            def __init__(self, *args, **kwargs):
                super(InvLabForm, self).__init__(*args, **kwargs)

        form = InvLabForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s7_id'] = s7_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s7_id'] = s7_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class RTInvLabsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsLabs
    form_class = modelform_factory(InvestigationsLabs, InvestigationsLabsForm)
    template_name = "patient_data/invlabdetails.html"
    success_message = "Lab Report Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-ass-update", kwargs={"pk": self.request.POST['s7_id']})

    def get_context_data(self, **kwargs):
        context = super(RTInvLabsUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s7_id'] = patient.s7_id.s7_id
        return context


class RTInvLabsDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsLabs

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s7_id.s7_id})


# ACUTE TOXICITY VIEW

class AcuteToxicityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AcuteToxicity
    form_class = modelform_factory(AcuteToxicity, AcuteToxicityForm)
    template_name = 'patient_data/acute_toxicity.html'
    success_message = "Acute Toxicity Created Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        tox_term_code = self.request.POST.get('tox_term', '')
        tox_obj = CTCV5.objects.get(pk=tox_term_code)
        form.instance.tox_term = tox_obj.term

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s7_id']
        as_details = S7Assessment.objects.get(s7_id=pk)
        crn = as_details.parent_id.crnumber
        if "to_ass" in self.request.POST:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-ass-update", kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        context = super(AcuteToxicityCreateView, self).get_context_data(**kwargs)
        # s8_acutetox_id = self.kwargs['pk']
        # obj_acute_tox = AcuteToxicity.objects.get(pk=s8_acutetox_id)
        crnumber = self.kwargs['crnumber']
        s7_id = self.kwargs['s7_id']
        patient = S1ParentMain.objects.get(crnumber=crnumber)
        system_options = CTCV5.objects.values('system').distinct()
        options_system = [(options['system'], options['system']) for options in system_options]

        class AcuteToxForm(AcuteToxicityForm):
            def __init__(self, *args, **kwargs):
                super(AcuteToxForm, self).__init__(*args, **kwargs)

        form = AcuteToxForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['update'] = False
        context['options_system'] = options_system
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s7_id'] = s7_id
        # context['form'].initial['tox_system'].choices = obj_acute_tox.tox_system

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        # print(self.request.POST)
        return form.errors


class AcuteToxicityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AcuteToxicity
    form_class = modelform_factory(AcuteToxicity, AcuteToxicityForm)
    template_name = 'patient_data/acute_toxicity.html'
    success_message = "Acute Toxicity Created Successfully!"
    context_object_name = 'data1'

    def form_valid(self, form):
        pk = self.kwargs["pk"]

        tox_term_code = self.request.POST.get('tox_term', '')
        tox_obj = CTCV5.objects.get(pk=tox_term_code)
        patient = AcuteToxicity.objects.get(pk=pk)

        form.instance.user_id = patient.user_id
        form.instance.tox_term = tox_obj.term
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = AcuteToxicity.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-ass-update", kwargs={"pk": self.request.POST['s7_id']})

    def get_context_data(self, **kwargs):
        context = super(AcuteToxicityUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = AcuteToxicity.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        system_options = CTCV5.objects.values('system').distinct()
        options_system = [(options['system'], options['system']) for options in system_options]

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['options_system'] = options_system
        # context['form'].initial['tox_system'] = patient.tox_system
        return context


class AcuteToxicityDeleteView(LoginRequiredMixin, DeleteView):
    model = AcuteToxicity

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = AcuteToxicity.objects.get(pk=pk)
        return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s7_id.s7_id})


# class AcuteToxicityCreateView(CreateView):
#     model = AcuteToxicity
#     form_class = AcuteToxicityForm
#     template_name = 'patient_data/acute_toxicity.html'
#     success_url = reverse_lazy('acute_toxicity_list')


# FOLLOW-UP Details

class FUPCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = S8FUP
    form_class = modelform_factory(S8FUP, S8FUPForm)
    template_name = "patient_data/radonc_followup.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crn = self.kwargs["crnumber"]
        patient_fu = S8FUP.objects.all().last()
        s8_id = patient_fu.s8_id
        # try:
        #     s3_id = self.kwargs['s3_id']
        # except KeyError:
        #     s8_id = False
        #     return reverse_lazy("db_operations", kwargs={"crnumber": crn})
        # try:
        #     s2_id = self.kwargs['s2_id']
        # except KeyError:
        #     return reverse_lazy("db_operations", kwargs={"crnumber": crn})
        if s8_id:
            if 'to_imaging' in self.request.POST:
                return reverse_lazy("inv-imaging2", kwargs={"crnumber": crn, "s8_id": s8_id})
            if 'to_prescription' in self.request.POST:
                return reverse_lazy("prescription2", kwargs={"crnumber": crn, "s8_id": s8_id})
            if 'to_pathology' in self.request.POST:
                return reverse_lazy("inv-pathlab2", kwargs={"crnumber": crn, "s8_id": s8_id})
            if 'to_labs' in self.request.POST:
                return reverse_lazy("inv-lab2", kwargs={"crnumber": crn, "s8_id": s8_id})

        if S3CarePlan.objects.filter(parent_id=crn).exists():
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})
        else:
            return reverse_lazy("db_operations", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(FUPCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class FUPForm(S8FUPForm):
            def __init__(self, *args, **kwargs):
                super(FUPForm, self).__init__(*args, **kwargs)

        form = FUPForm()
        context['form'] = form
        try:
            s3_id = self.kwargs['s3_id']
            s2_id = self.kwargs['s2_id']
            patient_mx = S3CarePlan.objects.get(pk=s3_id)
            all_fups = patient_mx.s8fup_set.all()
            context['all_fups'] = all_fups
            context['patient_mx'] = patient_mx
            context['form'].initial['s3_id'] = s3_id
            context['form'].initial['s2_id'] = s2_id
            context['form'].initial['parent_id'] = crnumber

        except KeyError:
            if patient.s3careplan_set.all().last():
                patient_mx = patient.s3careplan_set.all().last()
                context['form'].initial['s3_id'] = patient_mx.s3_id
            else:
                patient_mx = False
            context['patient_mx'] = patient_mx
            context['form'].fields['RecordRecc'].widget.attrs['readonly'] = True
            context['form'].fields['RecordRecc'].disabled = True
            context['form'].fields['LRstatus'].widget.attrs['readonly'] = True
            context['form'].fields['LRstatus'].disabled = True
            context['form'].fields['RRstatus'].widget.attrs['readonly'] = True
            context['form'].fields['RRstatus'].disabled = True
            context['form'].fields['DMstatus'].widget.attrs['readonly'] = True
            context['form'].fields['DMstatus'].disabled = True

        try:
            s2_id = self.kwargs['s2_id']
            context['form'].initial['s2_id'] = s2_id
        except KeyError:
            if patient.s3careplan_set.all().last():
                patient_mx = patient.s3careplan_set.all().last()
                context['form'].initial['s2_id'] = patient_mx.s2_id.s2_id
        context['patient'] = patient
        context['crnumber'] = crnumber

        context['form'].initial['parent_id'] = crnumber

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class FUPListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = S8FUP
    template_name = 'patient_data/radonc_s8_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return S8FUP.objects.filter(parent_id=self.kwargs['crnumber'])


class FUPUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = S8FUP
    form_class = modelform_factory(S8FUP, S8FUPForm)
    template_name = "patient_data/radonc_followup.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = S8FUP.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = S8FUP.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        if 'to_imaging' in self.request.POST:
            return reverse_lazy("inv-imaging2", kwargs={"crnumber": crn, "s8_id": pk})
        if 'to_prescription' in self.request.POST:
            return reverse_lazy("prescription2", kwargs={"crnumber": crn, "s8_id": pk})
        if 'to_pathology' in self.request.POST:
            return reverse_lazy("inv-pathlab2", kwargs={"crnumber": crn, "s8_id": pk})
        if 'to_labs' in self.request.POST:
            return reverse_lazy("inv-lab2", kwargs={"crnumber": crn, "s8_id": pk})
        if S3CarePlan.objects.filter(parent_id=crn).exists():
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})
        else:
            return reverse_lazy("db_operations", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(FUPUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = S8FUP.objects.get(pk=pk)
        patient_hp = InvestigationsPath.objects.filter(s8_id=pk)
        mol_path = []
        for path in patient_hp:
            if path.molecular_profile == "Yes":
                mol_path.append(path)
        context['mol_path_list'] = mol_path

        updatecrn = patient.parent_id.crnumber
        if patient.s2_id:
            diagnosis = True
        else:
            diagnosis = False
        if patient.s3_id:
            patient_mx = patient.s3_id
        else:
            patient_mx = False
        # patient_fup = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['diagnosis'] = diagnosis
        context['patient_mx'] = patient_mx
        context['s8_id'] = pk
        if not patient_mx:
            context['form'].fields['RecordRecc'].widget.attrs['readonly'] = True
            context['form'].fields['RecordRecc'].disabled = True
            context['form'].fields['LRstatus'].widget.attrs['readonly'] = True
            context['form'].fields['LRstatus'].disabled = True
            context['form'].fields['RRstatus'].widget.attrs['readonly'] = True
            context['form'].fields['RRstatus'].disabled = True
            context['form'].fields['DMstatus'].widget.attrs['readonly'] = True
            context['form'].fields['DMstatus'].disabled = True
        return context


# INVESTIGATION IMAGING DETAILS
class InvImgCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsImaging
    form_class = modelform_factory(InvestigationsImaging, InvestigationsImagingForm)
    template_name = "patient_data/invimgdetails.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"crnumber": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(InvImgCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class InvForm(InvestigationsImagingForm):
            def __init__(self, *args, **kwargs):
                super(InvForm, self).__init__(*args, **kwargs)
                # self.fields['imaging_type'].choices = imagingtype_choices
                # self.fields['imaging_location'].choices = imaging_location
                # self.fields['imaging_result'].choices = imaging_result
                # self.fields['lab_name'].choices = lab_names

        form = InvForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['s8_id'] = s8_id
        context['patient'] = patient
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class InvImgUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsImaging
    form_class = modelform_factory(InvestigationsImaging, InvestigationsImagingForm)
    template_name = "patient_data/invimgdetails.html"
    context_object_name = 'data'
    success_message = "Imaging Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        # print(patient)
        crn = patient.parent_id.crnumber
        fu_id = patient.s8_id.s8_id
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-fup-update", kwargs={"pk": fu_id})

    def get_context_data(self, **kwargs):
        context = super(InvImgUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        context['s8_id'] = patient.s8_id.s8_id
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        return context


class InvImgDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsImaging

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsImaging.objects.get(pk=pk)
        return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_id.s8_id})


# PRESCRIPTION DETAILS
class PrescriptionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = modelform_factory(Prescription, PrescriptionForm)
    template_name = "patient_data/prescription.html"
    success_message = "Prescription Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(PrescriptionCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class PresForm(PrescriptionForm):
            def __init__(self, *args, **kwargs):
                super(PresForm, self).__init__(*args, **kwargs)
                # self.fields['imaging_type'].choices = imagingtype_choices
                # self.fields['imaging_location'].choices = imaging_location
                # self.fields['imaging_result'].choices = imaging_result
                # self.fields['lab_name'].choices = lab_names

        form = PresForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s8_id'] = s8_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class PrescriptionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = modelform_factory(Prescription, PrescriptionForm)
    template_name = "patient_data/prescription.html"
    success_message = "Prescription Updated Successfully!"
    context_object_name = 'view_data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-fup-update", kwargs={"pk": self.request.POST['s8_id']})

    def get_context_data(self, **kwargs):
        context = super(PrescriptionUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber
        drug = patient.drug_name.split(" ")[0]
        drug_name = GenDrugs.objects.filter(drug=drug).first()

        context['form'].initial['drug_name'] = drug_name
        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s8_id'] = patient.s8_id.s8_id
        return context


class PrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = Prescription.objects.get(pk=pk)
        return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_id.s8_id})


# INVESTIGATION PATHLAB DETAILS
class InvPathlabCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsPath
    form_class = modelform_factory(InvestigationsPath, InvestigationsPathForm)
    template_name = "patient_data/invpathdetails.html"
    success_message = "Pathology Details Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(InvPathlabCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        # imagingtype_choices = []
        # imaging_location = []
        # imaging_result = []
        # lab_names = []
        # for choice in ImagingType.objects.all():
        #     imagingtype_choices.append((choice.id, choice.type))
        # for choice in ImageLocation.objects.all():
        #     imaging_location.append((choice.id, choice.location))
        # for choice in ImagingResult.objects.all():
        #     imaging_result.append((choice.id, choice.result))
        # for choice in LabName.objects.all():
        #     lab_names.append((choice.id, choice.name))

        class PathForm(InvestigationsPathForm):
            def __init__(self, *args, **kwargs):
                super(PathForm, self).__init__(*args, **kwargs)

        form = PathForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['s8_id'] = s8_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id
        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class InvPathlabUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsPath
    form_class = modelform_factory(InvestigationsPath, InvestigationsPathForm)
    template_name = "patient_data/invpathdetails.html"
    success_message = "Pathlab Investigation Updated Successfully!"
    context_object_name = 'view_data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-fup-update", kwargs={"pk": self.request.POST['s8_id']})

    def get_context_data(self, **kwargs):
        context = super(InvPathlabUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        # imagingtype_choices = []
        # imaging_location = []
        # imaging_result = []
        # lab_names = []
        # for choice in ImagingType.objects.all():
        #     imagingtype_choices.append((choice.id, choice.type))
        # for choice in ImageLocation.objects.all():
        #     imaging_location.append((choice.id, choice.location))
        # for choice in ImagingResult.objects.all():
        #     imaging_result.append((choice.id, choice.result))
        # for choice in LabName.objects.all():
        #     lab_names.append((choice.id, choice.name))

        # context['form'].fields['imaging_type'].choices = imagingtype_choices
        # context['form'].fields['imaging_location'].choices = imaging_location
        # context['form'].fields['imaging_result'].choices = imaging_result
        # context['form'].fields['lab_name'].choices = lab_names

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s8_id'] = patient.s8_id.s8_id
        return context


class InvPathlabDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsPath

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsPath.objects.get(pk=pk)
        return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_id.s8_id})


# INVESTIGATION MOL PATHLAB DETAILS
class InvMolPathlabCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsMolecular
    form_class = modelform_factory(InvestigationsMolecular, InvestigationsMolecularForm)
    template_name = "patient_data/invmolpathdetails.html"
    success_message = "Molecular Pathology Details Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_path_id']
        path_details = InvestigationsPath.objects.get(s8_path_id=pk)
        crn = path_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            s8_id = path_details.s8_id.s8_id
            return reverse_lazy("radonc-fup-update", kwargs={"pk": s8_id})
        if "to_ass" in self.request.POST:
            s7_id = path_details.s7_id.s7_id
            return reverse_lazy("radonc-ass-update", kwargs={"pk": s7_id})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(InvMolPathlabCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_path_id = self.kwargs['s8_path_id']
        path_details = InvestigationsPath.objects.get(pk=s8_path_id)

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class MolPathForm(InvestigationsMolecularForm):
            def __init__(self, *args, **kwargs):
                super(MolPathForm, self).__init__(*args, **kwargs)

        form = MolPathForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        if path_details.s8_id:
            context['s8_id'] = path_details.s8_id.s8_id
        if path_details.s7_id:
            context['s7_id'] = path_details.s7_id.s7_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_path_id'] = s8_path_id
        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class InvMolPathlabUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsMolecular
    form_class = modelform_factory(InvestigationsMolecular, InvestigationsMolecularForm)
    template_name = "patient_data/invmolpathdetails.html"
    success_message = "Molecular Pathology Details Updated Successfully!"
    context_object_name = 'view_data'

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsMolecular.objects.get(pk=pk)
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsMolecular.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        if patient.s8_path_id.s8_id:
            s8_id = patient.s8_path_id.s8_id.s8_id
            return reverse_lazy("radonc-fup-update", kwargs={"pk": s8_id})
        else:
            s7_id = patient.s8_path_id.s7_id.s7_id
            return reverse_lazy("radonc-ass-update", kwargs={"pk": s7_id})

    def get_context_data(self, **kwargs):
        context = super(InvMolPathlabUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsMolecular.objects.get(pk=pk)
        # s8_id = patient.s8_path_id.s8_id.s8_id
        updatecrn = patient.parent_id.crnumber

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        if patient.s8_path_id.s8_id:
            context['s8_id'] = patient.s8_path_id.s8_id.s8_id
        else:
            context['s7_id'] = patient.s8_path_id.s7_id.s7_id
        return context


class InvMolPathlabDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsMolecular

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsMolecular.objects.get(pk=pk)
        if patient.s8_path_id.s8_id:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_path_id.s8_id.s8_id})
        else:
            return reverse_lazy("radonc-ass-update", kwargs={"pk": patient.s8_path_id.s7_id.s7_id})


# INVESTIGATION BASIC LAB DETAILS
class InvLabsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = InvestigationsLabs
    form_class = modelform_factory(InvestigationsLabs, InvestigationsLabsForm)
    template_name = "patient_data/invlabdetails.html"
    success_message = "Lab Report Created Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(InvLabsCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class InvLabForm(InvestigationsLabsForm):
            def __init__(self, *args, **kwargs):
                super(InvLabForm, self).__init__(*args, **kwargs)

        form = InvLabForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['s8_id'] = s8_id
        context['patient'] = patient
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class InvLabsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = InvestigationsLabs
    form_class = modelform_factory(InvestigationsLabs, InvestigationsLabsForm)
    template_name = "patient_data/invlabdetails.html"
    success_message = "Lab Report Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-fup-update", kwargs={"pk": self.request.POST['s8_id']})

    def get_context_data(self, **kwargs):
        context = super(InvLabsUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s8_id'] = patient.s8_id.s8_id
        return context


class InvLabsDeleteView(LoginRequiredMixin, DeleteView):
    model = InvestigationsLabs

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = InvestigationsLabs.objects.get(pk=pk)
        return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_id.s8_id})


# LATE TOXICITY DETAILS
class LateToxCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LateToxicity
    form_class = modelform_factory(LateToxicity, LateToxicityForm)
    template_name = "patient_data/latetoxdetails.html"
    success_message = "Late Toxicity Created Successfully!"
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        if "to_fup" in self.request.POST:
            return reverse_lazy("radonc-fup-update", kwargs={"pk": pk})
        if "to_cp" in self.request.POST:
            return reverse_lazy("radonc-careplan-list", kwargs={"pk": crn})

        return reverse_lazy("radonc-fup-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(LateToxCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class LateToxForm(LateToxicityForm):
            def __init__(self, *args, **kwargs):
                super(LateToxForm, self).__init__(*args, **kwargs)

        form = LateToxForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context[s8_id] = s8_id
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class LateToxUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LateToxicity
    form_class = modelform_factory(LateToxicity, LateToxicityForm)
    template_name = "patient_data/latetoxdetails.html"
    success_message = "Late Toxicity Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = LateToxicity.objects.get(pk=pk)
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = LateToxicity.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-fup-update", kwargs={"pk": self.request.POST['s8_id']})

    def get_context_data(self, **kwargs):
        context = super(LateToxUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = LateToxicity.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient
        context['s8_id'] = patient.s8_id.s8_id
        return context


class LateToxDeleteView(LoginRequiredMixin, DeleteView):
    model = LateToxicity

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = LateToxicity.objects.get(pk=pk)
        return reverse_lazy("radonc-fup-update", kwargs={"pk": patient.s8_id.s8_id})


# PFT Details
class PFTDetailsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PFTDetails
    form_class = modelform_factory(PFTDetails, PFTDetailsForm)
    template_name = "patient_data/pftdetails.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['s8_id']
        fu_details = S8FUP.objects.get(s8_id=pk)
        crn = fu_details.parent_id.crnumber
        return reverse_lazy("radonc-pftdetails-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(PFTDetailsCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        patient = S1ParentMain.objects.get(crnumber=crnumber)

        class PFTForm(PFTDetailsForm):
            def __init__(self, *args, **kwargs):
                super(PFTForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = PFTForm()
        context['form'] = form
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class PFTDetailsListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = PFTDetails
    template_name = 'patient_data/pftdetails_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return PFTDetails.objects.filter(parent_id=self.kwargs['crnumber'])


class PFTDetailsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PFTDetails
    form_class = modelform_factory(PFTDetails, PFTDetailsForm)
    template_name = "patient_data/pftdetails.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = PFTDetails.objects.get(pk=pk)
        current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = PFTDetails.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-pftdetails-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(PFTDetailsUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = PFTDetails.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        patient_pft_p = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient_pft_p

        return context


class PFTDetailsDeleteView(LoginRequiredMixin, DeleteView):
    model = PFTDetails

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = PFTDetails.objects.get(pk=pk)
        return reverse_lazy("radonc-pftdetails-list", kwargs={"crnumber": patient.parent_id.crnumber})


# Cardiac Markers

class CardiacMarkersCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CardiacMarkers
    form_class = modelform_factory(CardiacMarkers, CardiacMarkersForm)
    template_name = "patient_data/cardiacmarkers.html"
    success_message = "Data Created Successfully!"
    # success_url = reverse_lazy('radonc-database-home')
    context_object_name = 'data'

    def form_valid(self, form):
        current_user = User.objects.get(id=self.request.user.id)
        # crnumber = self.kwargs['crnumber']

        form.instance.user_id = current_user
        return super().form_valid(form)

    def get_success_url(self):
        crnumber = self.kwargs['crnumber']
        patient = S1ParentMain.objects.get(crnumber=crnumber)
        return reverse_lazy("radonc-cardiacmarkers-list", kwargs={"crnumber": crnumber})

    def get_context_data(self, **kwargs):
        context = super(CardiacMarkersCreateView, self).get_context_data(**kwargs)
        crnumber = self.kwargs['crnumber']
        s8_id = self.kwargs['s8_id']

        class CardiacForm(CardiacMarkersForm):
            def __init__(self, *args, **kwargs):
                super(CardiacMarkersForm, self).__init__(*args, **kwargs)
                # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)

        form = CardiacForm()

        context['form'] = form

        patient = S1ParentMain.objects.get(crnumber=crnumber)
        context['crnumber'] = crnumber
        context['patient'] = patient
        context['form'].initial['parent_id'] = crnumber
        context['form'].initial['s8_id'] = s8_id

        return context

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return form.errors


class CardiacMarkersListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = CardiacMarkers
    template_name = 'patient_data/cardiacmarkers_display.html'  # <app>/<model>_<view type>.html
    context_object_name = 'data'

    def get_queryset(self):
        return CardiacMarkers.objects.filter(parent_id=self.kwargs['crnumber'])


class CardiacMarkersUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CardiacMarkers
    form_class = modelform_factory(CardiacMarkers, CardiacMarkersForm)
    template_name = "patient_data/cardiacmarkers.html"
    context_object_name = 'data'
    success_message = "Data Updated Successfully!"

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        patient = CardiacMarkers.objects.get(pk=pk)
        # current_user = User.objects.get(id=self.request.user.id)
        # form.instance.updated_by = current_user.username
        form.instance.user_id = patient.user_id
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = CardiacMarkers.objects.get(pk=pk)
        crn = patient.parent_id.crnumber
        # patient = PatientDiagnosis.objects.get(pk=pk)
        patient.updated_by = self.request.user.username
        patient.save()
        return reverse_lazy("radonc-cardiacmarkers-list", kwargs={"crnumber": crn})

    def get_context_data(self, **kwargs):
        context = super(CardiacMarkersUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        patient = CardiacMarkers.objects.get(pk=pk)
        updatecrn = patient.parent_id.crnumber

        patient_cm_p = S1ParentMain.objects.get(crnumber=updatecrn)

        context['updatecrn'] = updatecrn
        context['update'] = True
        context['patient'] = patient_cm_p

        return context


class CardiacMarkersDeleteView(LoginRequiredMixin, DeleteView):
    model = CardiacMarkers

    def get_success_url(self):
        pk = self.kwargs["pk"]
        patient = CardiacMarkers.objects.get(pk=pk)
        return reverse_lazy("radonc-cardiacmarkers-list", kwargs={"crnumber": patient.parent_id.crnumber})


@login_required
def simflow(request):
    return render(request, 'patient_data/simulation_flow.html')


@login_required
def simflowzoom(request):
    return render(request, 'patient_data/simulation_flow_zoom.html')


@login_required
def rtstatus(request):
    return render(request, 'patient_data/rt_status.html')


@login_required
def rtstatuszoom(request):
    return render(request, 'patient_data/rt_status_zoom.html')


@login_required
def overview(request):
    return render(request, 'patient_data/operations_overview.html')


@login_required
def summary(request, crnumber):
    name = ""
    fixed_text = ""
    hpe_text = ""
    chemo_text = ""
    patient = S1ParentMain.objects.get(crnumber=crnumber)
    p = patient
    sx = patient.s6surgery_set.all()
    if sx:
        sxtype = [sx.surgery for sx in sx[0].sxtype.all()]
        try:
            sxdate = sx[0].sxdate.strftime('%d/%m/%Y')
        except:
            sxdate = ""
    else:
        sxtype = ""
        sxdate = ""
    hp = patient.s6hpe_set.all()
    rt_details = patient.s4rt_set.all()
    if len(rt_details) > 0:
        rt_tech = f"{rt_details[0].tech1_id}"
        modality = f"{rt_details[0].modality1}"
        if rt_details[0].rtdose1:
            dose1 = f"{rt_details[0].rtdose1}"
            fx1 = f"{rt_details[0].rtdosefr1}"
        else:
            dose1 = 0
            fx1 = 0
        if rt_details[0].rtdose2:
            dose2 = f"{rt_details[0].rtdose2}"
            fx2 = f"{rt_details[0].rtdosefr2}"
        else:
            dose2 = 0
            fx2 = 0
        if rt_details[0].rtdose3:
            dose3 = f"{rt_details[0].rtdose3}"
            fx3 = f"{rt_details[0].rtdosefr3}"
        else:
            dose3 = 0
            fx3 = 0
        if (dose2 == 0) & (dose3 == 0):
            dose_text = f"{dose1}Gy/{fx1} given 5 days a week"
        elif (dose2 != 0) and (dose3 == 0):
            dose_text = f"{dose1}Gy/{fx1}# followed by " \
                        f"{dose2}Gy/{fx2}# boost, given 5 days a week"
        else:
            dose_text = f"Phase 1: {dose1}Gy/{fx1}#, " \
                        f"Phase2: {dose2}Gy/{fx2}#, " \
                        f"Phase3: {dose3}Gy/{fx3}#, given 5 days a week"
        rt_status_code = rt_details[0].rtstatus.code
        if rt_status_code:
            status = rt_status_code
            if status == "Completed":
                try:
                    duration_text = f"{rt_details[0].rtstartdate.strftime('%d/%m/%Y')} to {rt_details[0].rtfinishdate.strftime('%d/%m/%Y')}"
                except AttributeError as e:
                    duration_text = "Incorrect Data: PLEASE CHECK RT Finish and Completion Date"
                    Log.summary_rt.error(f"Error: {e}, Deatils: {duration_text}")

            elif status == "Ongoing":
                duration_text = "On Radiotherapy"
            else:
                duration_text = status
        else:
            duration_text = "Details Not Available"
    else:
        rt_tech = ""
        modality = ""
        dose_text = ""
        duration_text = ""
    try:
        ref_to = patient.s5chemo_set.all().first().unit_id
    except:
        ref_to = None
    if ref_to:
        if ref_to == "DCD":
            ref_to_text = "Dr. D.C. Doval"
        elif ref_to == "UB":
            ref_to_text = "Dr. Ullas Batra"
        elif ref_to == "SG":
            ref_to_text = "Dr. Sumit Goyal"
        elif ref_to == "VT":
            ref_to_text = "Dr. Vineet Talwar"
        else:
            ref_to_text = "Primary treating doctor"
    else:
        ref_to_text = "Primary treating doctor"
    if modality == "P":
        modality = "Photons"
    try:
        simid = patient.s4rt_set.all()[0].simid.simid
        target = f"{Simulation.objects.get(pk=simid).volumes.volume}"
    except:
        target = ""

    chemotherapy = patient.s5chemo_set.all().order_by('-chemodate')
    if chemotherapy:
        cycleno = chemotherapy[0].cycleno
        protocolcode = chemotherapy[0].chemo_protocol.code
        chemodate = chemotherapy[0].chemodate.strftime('%d/%m/%Y')
    else:
        cycleno = ""
        protocolcode = ""
        chemodate = ""
    if p.gender and p.age:
        if p.gender == 'Male' and p.age > 17:
            name = f"Mr {p.first_name.upper()} {p.last_name.upper()}"
        if p.gender == 'Male' and p.age < 17:
            name = f"Master {p.first_name.upper()} {p.last_name.upper()}"
        if p.gender == 'Female' and p.age > 12:
            name = f"Ms {p.first_name.upper()} {p.last_name.upper()}"
        if p.gender == 'Female' and p.age < 12:
            name = f"Baby {p.first_name.upper()} {p.last_name.upper()}"
    elif p.gender == 'Male':
        name = f"Mr {p.first_name.upper()} {p.last_name.upper()}"
    else:
        if p.last_name:
            name = f"Ms {p.first_name.upper()} {p.last_name.upper()}"
        else:
            name = f"Ms {p.first_name.upper()}"
    gender = p.gender
    reg_date = p.reg_date

    length1 = len(patient.s2diagnosis_set.all())
    if length1 > 0:
        d = patient.s2diagnosis_set.all()
        path = d[0].icd_path_code.hpe
        path = path.split(sep=',')[0]
        lat = d[0].laterality
        topo = d[0].icd_topo_code.site
        try:
            main_topo = d[0].icd_main_topo.site
        except AttributeError:
            main_topo = None
        topo = topo.split(sep=',')[0]
        t = d[0].c_t_id
        n = d[0].c_n_id
        m = d[0].c_m_id
        stage = d[0].c_stage_group_id
        if d[0].er == 'Yes':
            er = 'Positive'
        else:
            er = 'Negative'
        if d[0].pr == 'Yes':
            pr = 'Positive'
        else:
            pr = 'Negative'
        if d[0].her2neu == 'Yes':
            her2neu = 'Positive'
        else:
            her2neu = 'Negative'
        if len(hp) > 0:
            try:
                hptype = f"{hp[0].icd_path_code.hpe.split(',')[0]}"
            except:
                hptype = None
            try:
                grade = f"{hp[0].hpegrade.code}"
            except:
                grade = None
            nodes_p = f"{hp[0].nodesp}"
            nodes_r = f"{hp[0].nodesr}"
            pt = f"{hp[0].pt_id}"
            pn = f"{hp[0].pn_id}"
            if hp[0].lvi_vi == "Yes":
                lvi = "positive"
            elif hp[0].lvi_vi == "No":
                lvi = "negative"
            else:
                lvi = "unknown"

            if hp[0].er == 'Yes':
                er_h = 'Positive'
            else:
                er_h = 'Negative'
            if hp[0].pr == 'Yes':
                pr_h = 'Positive'
            else:
                pr_h = 'Negative'
            if hp[0].her2neu == 'Yes':
                her2neu_h = 'Positive'
            else:
                her2neu_h = 'Negative'
        else:
            lvi = "Unknown"
            er_h = 'Unknown'
            pr_h = 'Unknown'
            her2neu_h = 'Unknown'
            hptype = "Unknown"
            grade = "Unknown"
            nodes_p = "Unknown"
            nodes_r = "Unknown"
            pt = "x"
            pn = "x"
        try:
            temp_main = main_topo.upper()
        except AttributeError:
            main_topo = "NO DETAILS"
        if main_topo.upper() == 'BREAST':
            dx_clinical = f"{path} of {lat} {topo}, T{t}N{n}M{m} {stage}, ER:{er} PR:{pr} HER2Neu:{her2neu}"
            fixed_text = f"After {'his' if p.gender == 'Male' else 'her'} initial workup {'his' if p.gender == 'Male' else 'her'} was diagnosed with Breast Carcinoma " \
                         f"and underwent {sxtype} on " \
                         f"{sxdate}"
            hpe_text = f"Histopathology: {hptype}, {grade}, LVI {lvi} " \
                       f"with {nodes_p} out of {nodes_r} nodes positive " \
                       f"Final Stage: pT{pt}N{pn}. Hormonal Status: ER: {er_h} " \
                       f"PR: {pr_h} HER2neu: {her2neu_h}"
            chemo_text = f"{'his' if p.gender == 'Male' else 'her'} received {cycleno} cycles of {protocolcode} based" \
                         f" chemotherapy last on {chemodate}"
        elif 'sarcoma' in path.split(sep=" "):
            dx_clinical = f"{path} of {lat} {topo}, T{t}N{n}M{m} {stage}"
            fixed_text = f"No Details"
            hpe_text = f"No Details"
            chemo_text = f"No Details"
        else:
            dx_clinical = f"{path} of {lat} {topo}"
    else:
        dx_clinical = "No Details"
        fixed_text = "No Details"
        hpe_text = f"No Details"
        chemo_text = f"No Details"

    time = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)

    data = {'name': name, 'reg_date': reg_date, 'gender': gender,
            'pt': p, 'dx_clin': dx_clinical, 'fixed_text': fixed_text,
            'hpe_text': hpe_text, 'chemo_text': chemo_text, 'rt_tech': rt_tech,
            'modality': modality, 'target': target, 'dose_text': dose_text,
            'duration_text': duration_text, 'ref_to_text': ref_to_text, 'time': time}
    pre_url = request.GET.get('next')
    # prev_url = pre_url.split('/')[2]
    return render(request, 'patient_data/summary.html', {'data': data})


@login_required
def dbstats(request):
    return render(request, 'patient_data/dbstats.html')


@login_required
def download_file(request):
    # get the file path
    file_path = 'download.csv'

    # open the file in binary mode
    file = open(file_path, 'rb')

    # create an HttpResponse object with the FileWrapper as the content
    response = HttpResponse(FileWrapper(file), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_path}"'

    return response


def get_second_field_options(request):
    first_field_value = request.POST.get('main_site', '')
    if first_field_value:
        icdmain_code_values = first_field_value.split(',')[0][:3]
        codes = first_field_value.split(',')
        second_field_options = Site.objects.filter(code__in=codes).values_list()
    else:
        second_field_options = []

    # if first_field_value == 1:
    #     second_field_options = ["A", "B", "C"]
    # else:
    #     second_field_options = ["AA", "BB", "CC"]
    return render(request, 'patient_data/partials/partial_select_sites.html',
                  {'options': second_field_options})


@login_required
def filter_rt_started(request):
    all_options = ICDMainSites.objects.all().values_list()
    options1 = [(instance[2], instance[1]) for instance in all_options]
    if request.method == 'POST':
        form = FilterRTStarted(request.POST)
        main_site = form.data.get('main_site', "")
        subsite = form.data.get('subsite', "")

        main_site_option = []
        for i, vals in enumerate(options1):
            if vals[0] == main_site:
                main_site_option = options1[i]

        # s_date = form.data['s_date']
        # f_date = form.data['f_date']
        # intent = form.data['intent']
        # technique = form.data['technique']
        # studygp = form.data['studygp']
        # print(f"MainSIte:{main_site} SubSite:{subsite}")
        # if s_date:
        #     s_date = pd.to_datetime(form.data.get('s_date'), utc=True, unit='ns')
        # else:
        #     s_date = None
        # if f_date:
        #     f_date = pd.to_datetime(form.data.get('f_date'), utc=True, unit='ns')
        # else:
        #     f_date = None
        if subsite:
            site_id = subsite
            site = Site.objects.get(pk=site_id)
        else:
            site_id = None
            site = None
        # print(site_id)
        if main_site:
            main_site_id = ICDMainSites.objects.filter(icd_code=main_site).first().pk
            # main_site_icd_code = ICDMainSites.objects.filter(site=main_site).first().icd_code
            # codes = main_site_icd_code.split(",")
            # final_site_code = codes[0][:3]
            # print(codes)
            # print(final_site_code)
            # subsites = Site.objects.filter(code__contains=final_site_code).values()
            # print(subsites)
        else:
            main_site_id = None

        if site_id and main_site_id:
            data = {}
            query = mainsite_subsite_query
            params = [main_site_option[1], site_id]
            query_res = raw_query01(query, params)
            data = {}

        elif site_id:
            data = S1ParentMain.objects.filter(s2diagnosis__isnull=False).prefetch_related(
                's2diagnosis_set__icd_topo_code'
            ).filter(s2diagnosis__icd_topo_code=site_id)
        elif main_site_id:
            query = mainsite_query
            params = [main_site_option[1]]
            query_res = raw_query01(query, params)
            data = {}
        else:
            # print("No Data to print")
            data = {}

        df = pd.DataFrame.from_records(data.values())
        df.to_csv('download.csv')
        return render(request, 'patient_data/filter_rt_started.html',
                      {'form': form, 'data': query_res, 'options1': options1,
                       'main_site_option': main_site_option, 'site': site})

    form = FilterRTStarted()
    return render(request, 'patient_data/filter_rt_started.html', {'form': form, 'options1': options1})


@login_required
def checkdata(request):
    return render(request, 'patient_data/check_data.html')


# FUNCTIONS FOR HTMX

@login_required
def showdvh(request, s4_id):
    rt = S4RT.objects.get(pk=s4_id)
    if request.method == "POST":
        form = PrimaryDVHForm(request.POST)
        if form.is_valid():
            post = form.save()
            dvhdata = PrimaryDVH.objects.filter(s4_id=s4_id).all()
            return render(request, 'patient_data/partials/partial_primarydvh.html', {'dvhdata': dvhdata,
                                                                                     'rtdata': rt})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_primarydvh.html', {'errors': form_errors,
                                                                                     'rtdata': rt})
    else:
        dvhdata = PrimaryDVH.objects.filter(s4_id=s4_id).all()
        data = "Data Exists"
        if not dvhdata:
            data = f"No DVH Data to Display. Please enter DVH data for Patient{rt.parent_id.first_name} {rt.parent_id.last_name} ({rt.parent_id.crnumber})"
        return render(request, 'patient_data/partials/partial_primarydvh.html', {'dvhdata': dvhdata,
                                                                                 'rtdata': rt,
                                                                                 'data': data})


@login_required
def deletedvh(request, pk):
    dvh = PrimaryDVH.objects.get(pk=pk)
    rtid = dvh.s4_id.s4_id

    dvh.delete()

    rt = S4RT.objects.get(pk=rtid)
    dvhdata = PrimaryDVH.objects.filter(s4_id=rtid).all()

    return render(request, 'patient_data/partials/partial_primarydvh.html', {'dvhdata': dvhdata,
                                                                             'rtdata': rt})


@login_required
def updatedvh(request, pk):
    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(PrimaryDVH, pk=pk)
        # pass the object as instance in form
        form = PrimaryDVHForm(request.POST or None, instance=obj)
        s4_id = request.POST.get('s4_id')
        rt = S4RT.objects.get(s4_id=s4_id)

        if form.is_valid():
            form.save()
            dvhdata = PrimaryDVH.objects.filter(s4_id=s4_id).all()
            return render(request, 'patient_data/partials/partial_primarydvh.html', {'dvhdata': dvhdata,
                                                                                     'rtdata': rt})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_primarydvh.html', {'errors': form_errors,
                                                                                     'rtdata': rt})

    dvh = PrimaryDVH.objects.get(pk=pk)
    form = PrimaryDVHForm(instance=dvh)
    updatecrn = dvh.s4_id.parent_id.crnumber
    dvhid = dvh.s4_dvh_id
    update = True
    context = {
        'form': form,
        'updatecrn': updatecrn,
        'update': update,
        'dvhid': dvhid
    }

    return render(request, 'patient_data/partials/partial_updatedvh.html', context)


@login_required
def showprescription(request, s8_id):
    fu = S8FUP.objects.get(pk=s8_id)
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            post = form.save()
            prescriptiondata = Prescription.objects.filter(s8_id=s8_id).all()
            return render(request, 'patient_data/partials/partial_prescription.html',
                          {'prescriptiondata': prescriptiondata,
                           'fudata': fu,
                           's8_id': s8_id})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_prescription.html', {'errors': form_errors,
                                                                                       'fudata': fu,
                                                                                       's8_id': s8_id})
    else:
        prescriptiondata = Prescription.objects.filter(s8_id=s8_id).all()
        data = "Data Exists"
        if not prescriptiondata:
            data = f"No Prescription Data to Display. Please enter Prescription data for Patient{fu.parent_id.first_name} {fu.parent_id.last_name} ({fu.parent_id.crnumber})"
        return render(request, 'patient_data/partials/partial_prescription.html', {'prescriptiondata': prescriptiondata,
                                                                                   'fudata': fu,
                                                                                   'data': data,
                                                                                   's8_id': s8_id})


@login_required
def rtshowprescription(request, s7_id):
    ass = S7Assessment.objects.get(pk=s7_id)
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            post = form.save()
            prescriptiondata = Prescription.objects.filter(s7_id=s7_id).all()
            return render(request, 'patient_data/partials/partial_prescription.html',
                          {'prescriptiondata': prescriptiondata,
                           'assdata': ass,
                           's7_id': s7_id})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_prescription.html', {'errors': form_errors,
                                                                                       'assdata': ass,
                                                                                       's7_id': s7_id})
    else:
        prescriptiondata = Prescription.objects.filter(s7_id=s7_id).all()
        data = "Data Exists"
        if not prescriptiondata:
            data = f"No RT Prescription Data to Display. Please enter Prescription data for Patient{ass.parent_id.first_name} {ass.parent_id.last_name} ({ass.parent_id.crnumber})"
        return render(request, 'patient_data/partials/partial_prescription.html', {'prescriptiondata': prescriptiondata,
                                                                                   'assdata': ass,
                                                                                   'data': data,
                                                                                   's7_id': s7_id})


@login_required
def updateprescription(request, pk):
    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Prescription, pk=pk)
        # pass the object as instance in form
        form = PrescriptionForm(request.POST or None, instance=obj)
        s8_id = request.POST.get('s8_id')
        fu = S8FUP.objects.get(s8_id=s8_id)

        if form.is_valid():
            form.save()
            prescriptiondata = Prescription.objects.filter(s8_id=s8_id).all()
            return render(request, 'patient_data/partials/partial_prescription.html',
                          {'prescriptiondata': prescriptiondata,
                           'fudata': fu,
                           's8_id': s8_id})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_prescription.html', {'errors': form_errors,
                                                                                       'fudata': fu,
                                                                                       's8_id': s8_id})

    prescription = Prescription.objects.get(pk=pk)
    form = PrescriptionForm(instance=prescription)
    updatecrn = prescription.s8_id.parent_id.crnumber
    prescription_id = prescription.pk
    s8_id = prescription.s8_id.s8_id
    update = True
    context = {
        'form': form,
        'updatecrn': updatecrn,
        'update': update,
        'prescription_id': prescription_id,
        's8_id': s8_id
    }

    return render(request, 'patient_data/partials/partial_updateprescription.html', context)


def rtupdateprescription(request, pk):
    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Prescription, pk=pk)
        # pass the object as instance in form
        form = PrescriptionForm(request.POST or None, instance=obj)
        s7_id = request.POST.get('s7_id')
        ass = S7Assessment.objects.get(s7_id=s7_id)

        if form.is_valid():
            form.save()
            prescriptiondata = Prescription.objects.filter(s7_id=s7_id).all()
            return render(request, 'patient_data/partials/partial_prescription.html',
                          {'prescriptiondata': prescriptiondata,
                           'assdata': ass,
                           's7_id': s7_id})
        else:
            form_errors = form.errors
            return render(request, 'patient_data/partials/partial_prescription.html', {'errors': form_errors,
                                                                                       'fudata': ass,
                                                                                       's7_id': s7_id})
    prescription = Prescription.objects.get(pk=pk)

    form = PrescriptionForm(instance=prescription)
    drug = prescription.drug_name.split(" ")[0]
    drug_name = GenDrugs.objects.filter(drug=drug).first()

    form.initial['drug_name'] = drug_name
    updatecrn = prescription.s7_id.parent_id.crnumber
    s7_id = prescription.s7_id.s7_id
    prescription_id = prescription.pk
    update = True
    context = {
        'form': form,
        'updatecrn': updatecrn,
        'update': update,
        'prescription_id': prescription_id,
        's7_id': s7_id
    }
    return render(request, 'patient_data/partials/partial_updateprescription.html', context)


@login_required
def deleteprescription(request, pk):
    prescription = Prescription.objects.get(pk=pk)
    s8_id = prescription.s8_id.s8_id

    prescription.delete()

    fu = S8FUP.objects.get(pk=s8_id)
    prescriptiondata = Prescription.objects.filter(s8_id=s8_id).all()

    return render(request, 'patient_data/partials/partial_prescription.html', {'prescriptiondata': prescriptiondata,
                                                                               'fudata': fu,
                                                                               's8_id': s8_id})


@login_required
def rtdeleteprescription(request, pk):
    prescription = Prescription.objects.get(pk=pk)
    s7_id = prescription.s7_id.s7_id

    prescription.delete()

    ass = S7Assessment.objects.get(pk=s7_id)
    prescriptiondata = Prescription.objects.filter(s7_id=s7_id).all()

    return render(request, 'patient_data/partials/partial_prescription.html', {'prescriptiondata': prescriptiondata,
                                                                               'fudata': ass,
                                                                               's7_id': s7_id})


# NEW CHEMOTHERAPY FORMSET BASED VIEW
@login_required
def create_chemodrug(request, crnumber, pk):
    protocol = S5ChemoProtocol.objects.get(pk=pk)
    patient = S1ParentMain.objects.get(crnumber=crnumber)
    drugs = S5ChemoDrugs.objects.filter(s5_protocol_id=protocol).order_by('cycleno')
    form = S5ChemoDrugsForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            drug = form.save(commit=False)
            drug.s5_protocol_id = protocol
            drug.parent_id = patient
            drug.save()
            return redirect("drug-detail", pk=drug.pk)
        else:
            return render(request, "patient_data/partials/partial_chemo_drug_form.html", {
                "form": form
            })
    context = {
        "form": form,
        "protocol": protocol,
        "drugs": drugs,
        "crnumber": crnumber,
        "s5_protocol_id": pk
    }

    return render(request, "patient_data/chemo_entry_module.html", context)


@login_required
def create_chemodrug_form(request, crnumber, s5_protocol_id):
    patient = S1ParentMain.objects.get(crnumber=crnumber)
    last_patient_chemo = S5ChemoDrugs.objects.filter(parent_id=crnumber).last()
    if last_patient_chemo:
        form = S5ChemoDrugsForm(instance=last_patient_chemo)
        form.initial['s5_protocol_id'] = s5_protocol_id
        form.initial['user_id'] = request.user
    else:
        form = S5ChemoDrugsForm()
        form.initial['parent_id'] = crnumber
        form.initial['s5_protocol_id'] = s5_protocol_id
        form.initial['user_id'] = request.user

    context = {
        "form": form
    }

    return render(request, "patient_data/partials/partial_chemo_drug_form.html", context)


@login_required
def drug_detail(request, pk):
    drug = S5ChemoDrugs.objects.get(pk=pk)
    context = {
        "drug": drug
    }

    return render(request, "patient_data/partials/partial_chemo_drug_detail.html", context)


@login_required
def update_chemodrug(request, pk):
    drug = S5ChemoDrugs.objects.get(pk=pk)
    form = S5ChemoDrugsForm(request.POST or None, instance=drug)

    if request.method == "POST":
        if form.is_valid():
            drug = form.save()
            drug = S5ChemoDrugs.objects.get(pk=pk)
            drug.updated_by = request.user.username
            drug.save()
            return redirect("drug-detail", pk=drug.pk)

    context = {
        "form": form,
        "drug": drug
    }

    return render(request, "patient_data/partials/partial_chemo_drug_form.html", context)


@login_required
def drug_delete(request, pk):
    drug = S5ChemoDrugs.objects.get(pk=pk)
    drug.delete()

    return HttpResponse('')


@login_required
def acute_tox_second_field_options(request):
    first_field_value = request.POST.get('tox_system', '')
    if first_field_value:
        second_field_options = CTCV5.objects.filter(system=first_field_value).values_list()
    else:
        second_field_options = []
    # print(update)
    # if first_field_value == 1:
    #     second_field_options = ["A", "B", "C"]
    # else:
    #     second_field_options = ["AA", "BB", "CC"]
    return render(request, 'patient_data/partials/partial_select_toxicities.html',
                  {'options': second_field_options})


@login_required
def display_tox(request):
    first_field_value = request.POST.get('tox_term', '')
    tox = CTCV5.objects.get(pk=first_field_value)
    options = [tox.grade0, tox.grade1, tox.grade2, tox.grade3, tox.grade4, tox.grade5]

    return render(request, 'patient_data/partials/partial_display_grades.html',
                  {'options': options})


@login_required
def get_presim(request, crnumber, s3_id):
    field_dibh = request.POST.get('dibh', '')
    if field_dibh == '0':
        form = NewPreSimulationForm()
        form.fields['presimparent'].initial = crnumber
        form.fields['s3_id'].initial = s3_id
        return render(request, 'patient_data/partials/partial_new_presim.html', {'form': form,
                                                                                 'crnumber': crnumber,
                                                                                 's3_id': s3_id})
    else:
        if NewPreSimulation.objects.filter(s3_id=s3_id).exists():
            presim = NewPreSimulation.objects.filter(s3_id=s3_id)
            return render(request, 'patient_data/partials/partial_presim_display.html', {'presim': presim,
                                                                                         'crnumber': crnumber,
                                                                                         's3_id': s3_id})
        else:
            return redirect('radonc-simulation', crnumber, s3_id)


@login_required
def get_final_status(request):
    training_day = request.POST.get('day', '')
    form = NewPreSimulationForm()
    rttech = RTTech.objects.all().values_list()
    if training_day:
        training_day = int(training_day)
        if training_day >= 3:
            rttech_option = request.POST.get('final_status', '')
            if rttech_option:
                selected = rttech_option
                return render(request, 'patient_data/partials/partial_field_presim_final_status.html', {'form': form,
                                                                                                        'options': rttech,
                                                                                                        'selected': selected})
            else:
                return render(request, 'patient_data/partials/partial_field_presim_final_status.html', {'form': form,
                                                                                                        'options': rttech})
    return HttpResponse("")


@login_required
def create_presim(request):
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        data = request.POST.copy()
        form = NewPreSimulationForm(data=data)
        # print(request.POST)
        form.data['user'] = current_user.pk
        crn = form.data.get('presimparent')
        s3_id = form.data.get('s3_id')
        day = form.data.get('day')
        if form.is_valid():
            form.save()
            # messages.success(request,
            #                  f'DIBH assessment details has been saved for CRNumber: {crn} for DAY-{day}')
            presim = NewPreSimulation.objects.filter(s3_id=s3_id)
            presim_last = presim.last()
            # presim_last.user = request.GET
            return render(request, 'patient_data/partials/partial_presim_display.html',
                          {'presim': presim,
                           'crnumber': crn,
                           's3_id': s3_id})
        else:
            # print(form.errors)
            error = form.errors
            return render(request, 'patient_data/partials/partial_new_presim.html',
                          {'crnumber': crn,
                           's3_id': s3_id,
                           'error': error,
                           'form': form})


# Duplicating creating new presimulation as above function (create_presim) for direct access from mobiles
@login_required
def presim_create(request, crnumber):
    if request.method == "POST":
        pass

    else:
        form = NewPreSimulationForm()
        context = {'crnumber': crnumber, 'form': form}
        return render(request, 'patient_data/presim_create.html', context)


@login_required
def create_presim_new(request, crnumber):
    """
    Creating presimulation without dignosis or careplan.
    Later on we can attach to with s3_id
    """
    if request.method == "POST":
        form = NewPreSimulationWithoutCareForm(request.POST)
        if form.is_valid():
            form.save()
            form = NewPreSimulationWithoutCareForm()
            form.fields['presimparent'].initial = crnumber
            message = "Pre-Simulation added successfully!!!"
            # Need to decide where to pass
            return render(request, 'patient_data/new_presim_without_careplan.html',
                          {'form': form, 'crnumber': crnumber, 'message': message})
        else:
            message = form.errors
            form = NewPreSimulationWithoutCareForm(request.POST)
            return render(request, 'patient_data/new_presim_without_careplan.html',
                          {'form': form, 'crnumber': crnumber, 'message': message})
    else:
        form = NewPreSimulationWithoutCareForm()
        form.fields['presimparent'].initial = crnumber
        return render(request, 'patient_data/new_presim_without_careplan.html',
                      {'form': form, 'crnumber': crnumber, 'message': None})


@login_required
def create_simulation(request, crnumber):
    """
    Creating simulation without dignosis or careplan.
    Later on we can attach to with s3_id
    """
    if request.method == "POST":
        form = SimulationWithoutCarePlanForm(request.POST)
        if form.is_valid():
            form.save()
            form = SimulationWithoutCarePlanForm()
            form.fields['simparent'].initial = crnumber
            message = "Simulation added successfully!!!"
            # Need to decide where to pass
            return render(request, 'patient_data/create_simulation_without_careplan.html',
                          {'form': form, 'crnumber': crnumber, 'message': message})
        else:
            message = form.errors
            form = SimulationWithoutCarePlanForm(request.POST)
            return render(request, 'patient_data/create_simulation_without_careplan.html',
                          {'form': form, 'crnumber': crnumber, 'message': message})
    else:
        form = SimulationWithoutCarePlanForm()
        patient = S1ParentMain.objects.filter(crnumber=crnumber).first()
        form.fields['simparent'].initial = crnumber
        if patient.last_name:
            form.fields['name'].initial = patient.first_name + " " + patient.last_name
        else:
            form.fields['name'].initial = patient.first_name
        return render(request, 'patient_data/create_simulation_without_careplan.html',
                      {'form': form, 'crnumber': crnumber, 'message': None})


@login_required
def link_presim_with_careplan(request, presimid, s3_id):
    """
    Pre-Simulation link with careplan.
    """
    pre_sim = NewPreSimulation.objects.get(presimid=presimid)
    care_plan = S3CarePlan.objects.get(s3_id=s3_id)
    pre_sim.s3_id = care_plan
    pre_sim.save()
    return HttpResponse("Simulation linked --- PLEASE REFRESH THE PAGE TO SEE UPDATED STATUS")


@login_required
def link_simulation_with_careplan(request, simid, s3_id):
    """
    Simulation link with careplan.
    """
    sim = Simulation.objects.get(simid=simid)
    care_plan = S3CarePlan.objects.get(s3_id=s3_id)
    sim.s3_id = care_plan
    sim.s2_id = care_plan.s2_id
    # print(sim)
    sim.save()
    return HttpResponse("Simulation linked --- PLEASE REFRESH THE PAGE TO SEE UPDATED STATUS")


@login_required
def get_presim_buttons(request):
    finalstatus = request.POST.get('final_status', '')
    if finalstatus == '0':
        return HttpResponse('')
    else:
        return render(request, 'patient_data/partials/partial_presim_buttons.html')


@login_required
def edit_presim(request, pk):
    presim = NewPreSimulation.objects.get(pk=pk)
    all_presim = NewPreSimulation.objects.filter(s3_id=presim.s3_id.s3_id).all()
    form = NewPreSimulationForm(request.POST or None, instance=presim)
    # print(request.POST)
    if request.method == "POST":
        if form.is_valid():
            presim = form.save()
            messages.success(request, f'DIBH assessment details has been updated')
            return render(request, 'patient_data/partials/partial_presim_display.html', {'presim': all_presim,
                                                                                         'crnumber': presim.presimparent.crnumber,
                                                                                         's3_id': presim.s3_id.s3_id})
    context = {
        "form": form,
        "presim": presim
    }

    return render(request, "patient_data/partials/partial_new_presim.html", context)


@login_required
def delete_presim(request, pk):
    presim = NewPreSimulation.objects.get(pk=pk)
    all_presim = NewPreSimulation.objects.filter(s3_id=presim.s3_id.s3_id).all
    try:
        presim.delete()
    except IntegrityError as e:
        return render(request, 'patient_data/partials/partial_presim_display.html', {'presim': all_presim,
                                                                                     'crnumber': presim.presimparent.crnumber,
                                                                                     's3_id': presim.s3_id.s3_id,
                                                                                     'error': e})

    return render(request, 'patient_data/partials/partial_presim_display.html', {'presim': all_presim,
                                                                                 'crnumber': presim.presimparent.crnumber,
                                                                                 's3_id': presim.s3_id.s3_id})


@login_required
def patient_search(request):
    res = S1ParentMain.objects.all()
    page = request.GET.get('page')
    page_no = int(request.GET.get('page', 1))
    result = 10
    serial_num = ((int(request.GET.get('page', 1)) - 1) * result + 1) - 1

    paginator = Paginator(res, result)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        res = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        res = paginator.page(page)

    context = {'result': res, 'paginator': paginator, 'serial_num': serial_num, 'page_no': page_no}

    return render(request, 'patient_data/patient_search_form.html', context)


@login_required
def search(request):
    try:
        search_word = int(request.POST.get('search', ""))
        res = S1ParentMain.objects.filter(crnumber__startswith=search_word)
    except ValueError:
        search_word = request.POST.get('search', "")
        res = S1ParentMain.objects.filter(first_name__startswith=search_word)

    page = request.GET.get('page')
    page_no = int(request.GET.get('page', 1))
    result = 10
    serial_num = ((int(request.GET.get('page', 1)) - 1) * result + 1) - 1

    paginator = Paginator(res, result)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        res = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        res = paginator.page(page)

    context = {'result': res, 'paginator': paginator, 'serial_num': serial_num, 'page_no': page_no}
    return render(request, 'patient_data/partials/partial_patientlist.html', context)


@login_required
def mobile_view(request):
    if mobile(request):
        context = {'mobile': True}
    else:
        context = {'mobile': False}
    return render(request, 'patient_data/test.html', context)


@login_required
def confirmed_by(request, dx_id=None):
    crnumber = request.POST['parent_id']
    first_dx = False
    primary_dx = False
    if dx_id:
        new_dx = False
    else:
        new_dx = True
    try:
        if S2Diagnosis.objects.filter(parent_id=crnumber).exists():
            primary_dx = True
            # primary_dx_no = S2Diagnosis.objects.filter(parent_id=crnumber).count()
            first_dx = S2Diagnosis.objects.filter(parent_id=crnumber).first()
            if first_dx.pk == dx_id:
                first_dx = True
            else:
                first_dx = False
    except:
        first_dx = False
    if (request.POST['confirmed_by'] == "Imaging") or (request.POST['confirmed_by'] == "NA"):
        return HttpResponse("")
    else:
        try:
            diagnosis = S2Diagnosis.objects.get(pk=dx_id)
            form = S2DiagnosisForm(instance=diagnosis)
        except:
            form = S2DiagnosisForm()
        context = {'form': form, 'first_dx': first_dx, 'primary_dx': primary_dx, 'new_dx': new_dx, 'dx_id': dx_id}
        return render(request, 'patient_data/partials/partial_confirmed_by.html', context)


@login_required
def custom_tnm(request, new_primary=False):
    T, N, M, Stage = [("", "")], [("", "")], [("", "")], [("", "")]
    pT, pN, pM, pStage = [("", "")], [("", "")], [("", "")], [("", "")]

    for value in ClinT.objects.all().values():
        T.append((value["code"], value["code"]))
        pT.append((value["code"], value["code"]))
    for value in ClinN.objects.all().values():
        N.append((value["code"], value["code"]))
        pN.append((value["code"], value["code"]))
    for value in ClinM.objects.all().values():
        M.append((value["code"], value["code"]))
        pM.append((value["code"], value["code"]))
    for value in StageGroup.objects.all().values():
        Stage.append((value["code"], value["code"]))
        pStage.append((value["code"], value["code"]))
    if request.POST:
        if new_primary:
            primary_diagnosis = int(request.POST['diagnosis'])
            if primary_diagnosis == 10:
                T, N, M, pT, pN, pM = get_tnm(site="Lung")
            if primary_diagnosis == 12:
                T, N, M, pT, pN, pM = get_tnm()
            if primary_diagnosis == 13:
                T, N, M, pT, pN, pM = get_tnm(site="Esophagus")

            class DiagnosisForm(S2DiagnosisForm):
                def __init__(self, *args, **kwargs):
                    super(DiagnosisForm, self).__init__(*args, **kwargs)
                    # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)
                    self.fields['t_new'] = forms.ChoiceField(choices=[], required=False,
                                                             widget=forms.Select(
                                                                 attrs={'class': 'myselect form-control'}))
                    self.fields['n_new'] = forms.ChoiceField(choices=[], required=False,
                                                             widget=forms.Select(
                                                                 attrs={'class': 'myselect form-control'}))
                    self.fields['m_new'] = forms.ChoiceField(choices=[], required=False,
                                                             widget=forms.Select(
                                                                 attrs={'class': 'myselect form-control'}))
                    self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'myselect form-control'}))
                    self.fields['p_t_new'] = forms.ChoiceField(choices=[], required=False,
                                                               widget=forms.Select(
                                                                   attrs={'class': 'myselect form-control'}))
                    self.fields['p_n_new'] = forms.ChoiceField(choices=[], required=False,
                                                               widget=forms.Select(
                                                                   attrs={'class': 'myselect form-control'}))
                    self.fields['p_m_new'] = forms.ChoiceField(choices=[], required=False,
                                                               widget=forms.Select(
                                                                   attrs={'class': 'myselect form-control'}))
                    self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                                   widget=forms.Select(
                                                                       attrs={'class': 'myselect form-control'}))

            form = DiagnosisForm()
            form.fields["t_new"].choices = T
            form.fields["n_new"].choices = N
            form.fields["m_new"].choices = M
            form.fields["stage_new"].choices = Stage
            form.fields["p_t_new"].choices = pT
            form.fields["p_n_new"].choices = pN
            form.fields["p_m_new"].choices = pM
            form.fields["p_stage_new"].choices = pStage
            form.fields['diagnosis'].initial = request.POST['diagnosis']
            context = {'form': form, 'new_primary': new_primary}
            return render(request, 'patient_data/partials/partial_tnm.html', context)


        else:
            dx_type = request.POST['dx_type']
            if dx_type:
                if dx_type == "Second Malignancy":
                    new_primary = True
                primary_diagnosis = int(request.POST['diagnosis'])
                if primary_diagnosis == 10:
                    T, N, M, pT, pN, pM = get_tnm(site="Lung")
                if primary_diagnosis == 12:
                    T, N, M, pT, pN, pM = get_tnm()
                if primary_diagnosis == 13:
                    T, N, M, pT, pN, pM = get_tnm(site="Esophagus")

                class DiagnosisForm(S2DiagnosisForm):
                    def __init__(self, *args, **kwargs):
                        super(DiagnosisForm, self).__init__(*args, **kwargs)
                        # self.fields['s3_dx_id'].queryset = S2Diagnosis.objects.filter(parent_id=111111)
                        self.fields['t_new'] = forms.ChoiceField(choices=[], required=False,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'myselect form-control'}))
                        self.fields['n_new'] = forms.ChoiceField(choices=[], required=False,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'myselect form-control'}))
                        self.fields['m_new'] = forms.ChoiceField(choices=[], required=False,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'myselect form-control'}))
                        self.fields['stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                                     widget=forms.Select(
                                                                         attrs={'class': 'myselect form-control'}))
                        self.fields['p_t_new'] = forms.ChoiceField(choices=[], required=False,
                                                                   widget=forms.Select(
                                                                       attrs={'class': 'myselect form-control'}))
                        self.fields['p_n_new'] = forms.ChoiceField(choices=[], required=False,
                                                                   widget=forms.Select(
                                                                       attrs={'class': 'myselect form-control'}))
                        self.fields['p_m_new'] = forms.ChoiceField(choices=[], required=False,
                                                                   widget=forms.Select(
                                                                       attrs={'class': 'myselect form-control'}))
                        self.fields['p_stage_new'] = forms.ChoiceField(choices=[], required=False,
                                                                       widget=forms.Select(
                                                                           attrs={'class': 'myselect form-control'}))

                form = DiagnosisForm()
                form.fields["t_new"].choices = T
                form.fields["n_new"].choices = N
                form.fields["m_new"].choices = M
                form.fields["stage_new"].choices = Stage
                form.fields["p_t_new"].choices = pT
                form.fields["p_n_new"].choices = pN
                form.fields["p_m_new"].choices = pM
                form.fields["p_stage_new"].choices = pStage
            else:
                form = None
            context = {'form': form, 'new_primary': new_primary}
        return render(request, 'patient_data/partials/partial_tnm.html', context)


@login_required
def get_mets(request):
    context = get_stagegroup(request=request)
    return render(request, 'patient_data/partials/partial_mets.html', context)


@login_required
def get_p_mets(request):
    context = get_stagegroup(request=request, pathologic=True)
    return render(request, 'patient_data/partials/partial_p_mets.html', context)


@login_required
def test(request):
    T, N, M = get_tnm()
    # print(M)
    return HttpResponse("Test")
