from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_view
from django.conf import settings
from django.conf.urls.static import static
from .dash_apps.finished_apps import (simulation_flow, rt_status, check_data,
                                      simulation_flow_zoom, rt_status_zoom, simstats)
from . import views
from .views import S1RegUpdateView, S1ListView, PreSimulationUpdateView, PreSimulationListView, PreSimulationDeleteView, \
    DiagnosisCreateView, DiagnosisListView, DiagnosisUpdateView, CareplanCreateView, CareplanListView, \
    CarePlanUpdateView, SimulationListView, SimulationUpdateView, RadiotherapyCreateView, RadiotherapyListView, \
    RadiotherapyUpdateView, AssCreateView, AssListView, AssUpdateView, SurgeryCreateView, SurgeryListView, \
    SurgeryUpdateView, HPECreateView, HPEListView, HPEUpdateView, ChemotherapyCreateView, ChemotherapyListView, \
    ChemotherapyUpdateView, FUPCreateView, FUPListView, FUPUpdateView, PrimaryDVHCreateView, PFTDetailsCreateView, \
    PFTDetailsListView, PFTDetailsUpdateView, PFTDetailsDeleteView, CardiacMarkersCreateView, CardiacMarkersListView, \
    CardiacMarkersUpdateView, CardiacMarkersDeleteView, ChemotherapyDeleteView, InvImgCreateView, InvImgUpdateView, \
    InvImgDeleteView, PrescriptionCreateView, PrescriptionUpdateView, PrescriptionDeleteView, InvPathlabCreateView, \
    InvPathlabUpdateView, InvPathlabDeleteView, InvMolPathlabCreateView, InvMolPathlabUpdateView, \
    InvMolPathlabDeleteView, InvLabsCreateView, InvLabsUpdateView, InvLabsDeleteView, LateToxCreateView, \
    LateToxUpdateView, LateToxDeleteView

urlpatterns = [
    path('', views.index, name='database-index'),
    # path('', views.index1, name='database-index'),
    path('db_operations/', views.radonc_home, name='db_operations'),
    path('db_operations/<str:crnumber>/', views.radonc_home, name='db_operations'),
    path('registration/', views.s1registration, name="registration"),
    path('registration/<str:crnumber>/', views.s1registration, name="registration"),
    path('radonc-registration/<int:pk>/update/', S1RegUpdateView.as_view(), name="registration-update"),
    path('radonc-patientlist/', S1ListView.as_view(), name='radonc-patientlist'),
    path('summary/<str:crnumber>/', views.summary, name="summary"),
    # path('radonc-presimulation/', views.presimulation, name="radonc-presimulation"),
    path('radonc-presimulation/<str:crnumber>/<int:s3_id>/', views.presimulation, name="radonc-presimulation"),
    path('radonc-presimulation/<int:pk>/update/', PreSimulationUpdateView.as_view(),
         name="radonc-presimulation-update"),
    path('radonc-presimulation/<str:crnumber>/list/', PreSimulationListView.as_view(),
         name="radonc-presimulation-list"),
    path('radonc-presimulation/<int:pk>/delete/', PreSimulationDeleteView.as_view(),
         name="radonc-presimulation-delete"),
    # path('presim2sim/<int:crnumber>/', views.proceed2sim, name="proceed2sim"),
    path('radonc-diagnosis/', DiagnosisCreateView.as_view(), name="radonc-diagnosis"),
    path('radonc-diagnosis/<str:crnumber>/', DiagnosisCreateView.as_view(), name="radonc-diagnosis"),
    path('radonc-diagnosis/<str:crnumber>/list/', DiagnosisListView.as_view(), name="radonc-diagnosis-list"),
    path('radonc-diagnosis/<int:pk>/update/', DiagnosisUpdateView.as_view(), name="radonc-diagnosis-update"),
    path('radonc-careplan/', CareplanCreateView.as_view(), name="radonc-careplan"),
    path('radonc-careplan/<str:crnumber>/<int:s2_id>', CareplanCreateView.as_view(), name="radonc-careplan"),
    path('radonc-careplan/<str:crnumber>/list/', CareplanListView.as_view(), name="radonc-careplan-list"),
    path('radonc-careplan/<int:pk>/update/', CarePlanUpdateView.as_view(), name="radonc-careplan-update"),
    # path('radonc-simulation/', views.simulation, name="radonc-simulation"),
    path('radonc-simulation/<str:crnumber>/<int:s3_id>/', views.simulation, name="radonc-simulation"),
    path('radonc-simulation/<str:crnumber>/<int:s3_id>/<int:presimid>/', views.simulation, name="radonc-simulation"),
    path('radonc-simulation/<str:crnumber>/list/', SimulationListView.as_view(), name="radonc-simulation-list"),
    path('radonc-simulation/<int:pk>/update/', SimulationUpdateView.as_view(), name="radonc-simulation-update"),
    path('radonc-radiotherapy/', RadiotherapyCreateView.as_view(), name="radonc-radiotherapy"),
    path('radonc-radiotherapy/<str:crnumber>/<int:simid>/', RadiotherapyCreateView.as_view(),
         name="radonc-radiotherapy"),
    path('radonc-radiotherapy/<str:crnumber>/list/', RadiotherapyListView.as_view(), name="radonc-radiotherapy-list"),
    path('radonc-radiotherapy/<int:pk>/update/', RadiotherapyUpdateView.as_view(), name="radonc-radiotherapy-update"),

    # SURGERY
    path('radonc-surgery/', SurgeryCreateView.as_view(), name="radonc-surgery"),
    path('radonc-surgery/<str:crnumber>/<int:s3_id>/', SurgeryCreateView.as_view(),
         name="radonc-surgery"),
    path('radonc-surgery/<str:crnumber>/list/', SurgeryListView.as_view(), name="radonc-surgery-list"),
    path('radonc-surgery/<int:pk>/update/', SurgeryUpdateView.as_view(), name="radonc-surgery-update"),

    # HISTOPATHOLOGY
    path('radonc-hpe/', HPECreateView.as_view(), name="radonc-hpe"),
    path('radonc-hpe/<str:crnumber>/<int:s6_id>/', HPECreateView.as_view(), name="radonc-hpe"),
    path('radonc-hpe/<str:crnumber>/list/', HPEListView.as_view(), name="radonc-hpe-list"),
    path('radonc-hpe/<int:pk>/update/', HPEUpdateView.as_view(), name="radonc-hpe-update"),

    # CHEMOTHERAPY
    path('radonc-chemotherapy/<int:pk>/update/', ChemotherapyUpdateView.as_view(), name="radonc-chemotherapy-update"),
    path('radonc-chemotherapy/<str:crnumber>/list/', ChemotherapyListView.as_view(), name="radonc-chemotherapy-list"),
    path('radonc-chemotherapy/', ChemotherapyCreateView.as_view(), name="radonc-chemotherapy"),
    path('radonc-chemotherapy/<str:crnumber>/<int:s3_id>/', ChemotherapyCreateView.as_view(),
         name="radonc-chemotherapy"),
    path('radonc-chemotherapy/<int:pk>/delete/', ChemotherapyDeleteView.as_view(),
         name="radonc-chemotherapy-delete"),

    # ASSESSMENT
    path('radonc-ass/<int:s4_id>/', AssCreateView.as_view(), name="radonc-ass"),
    path('radonc-ass/<int:s4_id>/list/', AssListView.as_view(), name="radonc-ass-list"),
    path('radonc-ass/<int:pk>/update/', AssUpdateView.as_view(), name="radonc-ass-update"),

    # FOLLOWUP
    path('radonc-fup/<str:crnumber>/<int:s2_id>/<int:s3_id>/', FUPCreateView.as_view(), name="radonc-fup1"),
    path('radonc-fup/<str:crnumber>/', FUPCreateView.as_view(), name="radonc-fup2"),
    path('radonc-fup/<str:crnumber>/list/', FUPListView.as_view(), name="radonc-fup-list"),
    path('radonc-fup/<int:pk>/update/', FUPUpdateView.as_view(), name="radonc-fup-update"),

    # INVESTIGATION IMAGING
    path('inv-imaging/<str:crnumber>/', InvImgCreateView.as_view(), name="inv-imaging1"),
    path('inv-imaging/<str:crnumber>/<int:s8_id>/', InvImgCreateView.as_view(), name="inv-imaging2"),
    path('inv-imaging/<int:pk>/update/', InvImgUpdateView.as_view(), name="inv-imaging-update"),
    path('inv-imaging/<int:pk>/delete/', InvImgDeleteView.as_view(), name="inv-imaging-delete"),

    # INVESTIGATION LAB TEST
    path('inv-lab/<str:crnumber>/', InvLabsCreateView.as_view(), name="inv-lab1"),
    path('inv-lab/<str:crnumber>/<int:s8_id>/', InvLabsCreateView.as_view(), name="inv-lab2"),
    path('inv-lab/<int:pk>/update/', InvLabsUpdateView.as_view(), name="inv-lab-update"),
    path('inv-lab/<int:pk>/delete/', InvLabsDeleteView.as_view(), name="inv-lab-delete"),

    # INVESTIGATION PATH LABS
    path('inv-pathlab/<str:crnumber>/', InvPathlabCreateView.as_view(), name="inv-pathlab1"),
    path('inv-pathlab/<str:crnumber>/<int:s8_id>/', InvPathlabCreateView.as_view(), name="inv-pathlab2"),
    path('inv-pathlab/<int:pk>/update/', InvPathlabUpdateView.as_view(), name="inv-pathlab-update"),
    path('inv-pathlab/<int:pk>/delete/', InvPathlabDeleteView.as_view(), name="inv-pathlab-delete"),

    # INVESTIGATIONS MOL PATH LABS inv-molpathlab1
    path('inv-molpathlab/<str:crnumber>/', InvMolPathlabCreateView.as_view(), name="inv-molpathlab1"),
    path('inv-molpathlab/<str:crnumber>/<int:s8_path_id>/', InvMolPathlabCreateView.as_view(), name="inv-molpathlab2"),
    path('inv-molpathlab/<int:pk>/update/', InvMolPathlabUpdateView.as_view(), name="inv-molpathlab-update"),
    path('inv-molpathlab/<int:pk>/delete/', InvMolPathlabDeleteView.as_view(), name="inv-molpathlab-delete"),

    # LATE TOXICITY LABS
    path('latetox/<str:crnumber>/', LateToxCreateView.as_view(), name="latetox1"),
    path('latetox/<str:crnumber>/<int:s8_id>/', LateToxCreateView.as_view(), name="latetox2"),
    path('latetox/<int:pk>/update/', LateToxUpdateView.as_view(), name="latetox-update"),
    path('latetox/<int:pk>/delete/', LateToxDeleteView.as_view(), name="latetox-delete"),


    # PRESCRIPTION
    path('prescription/<str:crnumber>/', PrescriptionCreateView.as_view(), name="prescription1"),
    path('prescription/<str:crnumber>/<int:s8_id>/', PrescriptionCreateView.as_view(), name="prescription2"),
    path('prescription/<int:pk>/update/', PrescriptionUpdateView.as_view(), name="prescription-update"),
    path('prescription/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name="prescription-delete"),

    # PRIMARY-DVH
    path('radonc-primarydvh/<int:s4_id>/', PrimaryDVHCreateView.as_view(), name="radonc-primarydvh"),
    # path('radonc-primarydvh/<int:s4_id>/list/', PrimaryDVHListView1.as_view(), name="radonc-primarydvh-list"),
    # path('radonc-primarydvh/<int:pk>/update/', PrimaryDVHUpdateView1.as_view(), name="radonc-primarydvh-update"),

    #PFT
    path('radonc-pftdetails/<str:crnumber>/<int:s8_id>/', PFTDetailsCreateView.as_view(), name="radonc-pftdetails"),
    path('radonc-pftdetails/<str:crnumber>/list/', PFTDetailsListView.as_view(), name="radonc-pftdetails-list"),
    path('radonc-pftdetails/<int:pk>/update/', PFTDetailsUpdateView.as_view(), name="radonc-pftdetails-update"),
    path('radonc-pftdetails/<int:pk>/delete/', PFTDetailsDeleteView.as_view(), name="radonc-pftdetails-delete"),

    # CARDIAC MARKER DETAILS
    path('radonc-cardiacmarkers/<str:crnumber>/<int:s8_id>/', CardiacMarkersCreateView.as_view(),
         name="radonc-cardiacmarkers"),
    path('radonc-cardiacmarkers/<str:crnumber>/list/', CardiacMarkersListView.as_view(),
         name="radonc-cardiacmarkers-list"),
    path('radonc-cardiacmarkers/<int:pk>/update/', CardiacMarkersUpdateView.as_view(),
         name="radonc-cardiacmarkers-update"),
    path('radonc-cardiacmarkers/<int:pk>/delete/', CardiacMarkersDeleteView.as_view(),
         name="radonc-cardiacmarkers-delete"),
    path('overview/', views.overview, name="overview"),

    path('simflow/', views.simflow, name="simflow"),
    path('simflowzoom/', views.simflowzoom, name="simflowzoom"),
    path('rtstatus/', views.rtstatus, name="rtstatus"),
    path('rtstatuszoom/', views.rtstatuszoom, name="rtstatuszoom"),
    path('dbstats/', views.dbstats, name="dbstats"),
    path('filter-rt-started/', views.filter_rt_started, name="filter-rt-started"),
    path('filter-rt-started/download', views.download_file, name="filtered-download"),
    path('checkdata/', views.checkdata, name="checkdata"),

]

htmx_urlpatterns = [
    path('showdvh/<int:s4_id>', views.showdvh, name="showdvh"),
    path('deletedvh/<int:pk>', views.deletedvh, name="deletedvh"),
    path('updatedvh/<int:pk>', views.updatedvh, name="updatedvh"),
    path('get_second_field_options/', views.get_second_field_options, name='get_second_field_options'),

    path('showprescription/<int:s8_id>', views.showprescription, name="showprescription"),
    path('updateprescription/<int:pk>', views.updateprescription, name="updateprescription"),
    path('deleteprescription/<int:pk>', views.deleteprescription, name="deleteprescription"),
]

urlpatterns += htmx_urlpatterns
