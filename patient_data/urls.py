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
    LateToxUpdateView, LateToxDeleteView, ChemoProtocolCreateView, ChemoProtocolUpdateView, ChemoProtocolDeleteView, \
    AcuteToxicityCreateView, RTPrescriptionCreateView, RTPrescriptionUpdateView, RTPrescriptionDeleteView, \
    RTInvImgCreateView, RTInvImgUpdateView, RTInvImgDeleteView, RTInvPathlabCreateView, RTInvPathlabUpdateView, \
    RTInvPathlabDeleteView, RTInvLabsCreateView, RTInvLabsUpdateView, RTInvLabsDeleteView, AcuteToxicityUpdateView, \
    AcuteToxicityDeleteView, SimulationDeleteView, NewPreSimulationListView, link_presim_with_careplan, create_simulation, \
    link_simulation_with_careplan

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
    # PRESIMULATION PATHS
    path('radonc-presimulation/<str:crnumber>/<int:s3_id>/', views.presimulation, name="radonc-presimulation"),
    path('radonc-presimulation/<int:pk>/update/', PreSimulationUpdateView.as_view(),
         name="radonc-presimulation-update"),
    path('radonc-presimulation/<str:crnumber>/list/', PreSimulationListView.as_view(),
         name="radonc-presimulation-list"),
    path('radonc-presimulation/<int:pk>/delete/', PreSimulationDeleteView.as_view(),
         name="radonc-presimulation-delete"),

    path('radonc-newpresimulation/<str:crnumber>/list/', NewPreSimulationListView.as_view(),
         name="radonc-newpresimulation-list"),


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

    # SIMULATION
    path('radonc-simulation/<str:crnumber>/<int:s3_id>/', views.simulation, name="radonc-simulation"),
    path('radonc-simulation2/<str:crnumber>/<int:s3_id>/', views.simulation2, name="radonc-simulation2"),
    path('radonc-simulation/<str:crnumber>/<int:s3_id>/<int:presimid>/', views.simulation, name="radonc-simulation"),
    path('radonc-simulation2/<str:crnumber>/<int:s3_id>/<int:presimid>/', views.simulation2, name="radonc-simulation2"),
    path('radonc-simulation/<str:crnumber>/list/', SimulationListView.as_view(), name="radonc-simulation-list"),
    path('radonc-simulation/<int:pk>/update/', SimulationUpdateView.as_view(), name="radonc-simulation-update"),
    path('radonc-simulation/<int:pk>/delete/', SimulationDeleteView.as_view(),
         name="radonc-simulation-delete"),

    # NEWSIMULATION
    path('new-simulation/<str:crnumber>/<int:s3_id>/', views.new_simulation, name="new-simulation"),

    # RADIOTHERAPY
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

    # NEW CHEMOTHERAPY PROTOCOL PATHS
    path('radonc-chemoprotocol/<str:crnumber>/<int:s3_id>/', ChemoProtocolCreateView.as_view(),
         name="radonc-chemoprotocol"),
    path('radonc-chemoprotocol/<int:pk>/update', ChemoProtocolUpdateView.as_view(),
         name="radonc-chemoprotocol-update"),
    path('radonc-chemoprotocol/<int:pk>/delete', ChemoProtocolDeleteView.as_view(),
         name="radonc-chemoprotocol-delete"),


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

    # RT INVESTIGATION IMAGING
    path('rtinv-imaging/<str:crnumber>/<int:s7_id>/', RTInvImgCreateView.as_view(), name="rtinv-imaging"),
    path('rtinv-imaging/<int:pk>/update/', RTInvImgUpdateView.as_view(), name="rtinv-imaging-update"),
    path('rtinv-imaging/<int:pk>/delete/', RTInvImgDeleteView.as_view(), name="rtinv-imaging-delete"),

    # INVESTIGATION LAB TEST
    path('inv-lab/<str:crnumber>/', InvLabsCreateView.as_view(), name="inv-lab1"),
    path('inv-lab/<str:crnumber>/<int:s8_id>/', InvLabsCreateView.as_view(), name="inv-lab2"),
    path('inv-lab/<int:pk>/update/', InvLabsUpdateView.as_view(), name="inv-lab-update"),
    path('inv-lab/<int:pk>/delete/', InvLabsDeleteView.as_view(), name="inv-lab-delete"),

    # INVESTIGATION LAB TEST
    path('rtinv-lab/<str:crnumber>/<int:s7_id>/', RTInvLabsCreateView.as_view(), name="rtinv-lab"),
    path('rtinv-lab/<int:pk>/update/', RTInvLabsUpdateView.as_view(), name="rtinv-lab-update"),
    path('rtinv-lab/<int:pk>/delete/', RTInvLabsDeleteView.as_view(), name="rtinv-lab-delete"),

    # INVESTIGATION PATH LABS
    path('inv-pathlab/<str:crnumber>/', InvPathlabCreateView.as_view(), name="inv-pathlab1"),
    path('inv-pathlab/<str:crnumber>/<int:s8_id>/', InvPathlabCreateView.as_view(), name="inv-pathlab2"),
    path('inv-pathlab/<int:pk>/update/', InvPathlabUpdateView.as_view(), name="inv-pathlab-update"),
    path('inv-pathlab/<int:pk>/delete/', InvPathlabDeleteView.as_view(), name="inv-pathlab-delete"),

    # RT INVESTIGATION PATH LABS
    path('rtinv-pathlab/<str:crnumber>/<int:s7_id>/', RTInvPathlabCreateView.as_view(), name="rtinv-pathlab"),
    path('rtinv-pathlab/<int:pk>/update/', RTInvPathlabUpdateView.as_view(), name="rtinv-pathlab-update"),
    path('rtinv-pathlab/<int:pk>/delete/', RTInvPathlabDeleteView.as_view(), name="rtinv-pathlab-delete"),

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

    # RT PRESCRIPTION
    path('rtprescription/<str:crnumber>/<int:s7_id>/', RTPrescriptionCreateView.as_view(), name="rtprescription"),
    path('rtprescription/<int:pk>/update/', RTPrescriptionUpdateView.as_view(), name="rtprescription-update"),
    path('rtprescription/<int:pk>/delete/', RTPrescriptionDeleteView.as_view(), name="rtprescription-delete"),

    # RT ACUTE TOXICITY
    path('acute-toxicity/<str:crnumber>/<int:s7_id>/', AcuteToxicityCreateView.as_view(), name='acute-toxicity'),
    path('acute-toxicity-update/<int:pk>/', AcuteToxicityUpdateView.as_view(), name='acute-toxicity-update'),
    path('acute-toxicity-delete/<int:pk>/', AcuteToxicityDeleteView.as_view(), name='acute-toxicity-delete'),


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
    path('presim-create/<str:crnumber>/', views.presim_create, name="presim-create"),
    path('create-presim/<str:crnumber>/', views.create_presim_new, name='add-presim'),
    path('create-simulation/<str:crnumber>/', views.create_simulation, name='add-simulation'),

    # TEST URL


]

htmx_urlpatterns = [
    path('showdvh/<int:s4_id>', views.showdvh, name="showdvh"),
    path('deletedvh/<int:pk>', views.deletedvh, name="deletedvh"),
    path('updatedvh/<int:pk>', views.updatedvh, name="updatedvh"),
    path('get_second_field_options/', views.get_second_field_options, name='get_second_field_options'),
    path('acute_tox_second_field_options/', views.acute_tox_second_field_options, name='acute_tox_second_field_options'),

    path('showprescription/<int:s8_id>', views.showprescription, name="showprescription"),
    path('rtshowprescription/<int:s7_id>', views.rtshowprescription, name="rtshowprescription"),
    path('updateprescription/<int:pk>', views.updateprescription, name="updateprescription"),
    path('rtupdateprescription/<int:pk>', views.rtupdateprescription, name="rtupdateprescription"),
    path('deleteprescription/<int:pk>', views.deleteprescription, name="deleteprescription"),
    path('rtdeleteprescription/<int:pk>', views.rtdeleteprescription, name="rtdeleteprescription"),

    path("htmx/chemodrug-form/<str:crnumber>/<int:s5_protocol_id>", views.create_chemodrug_form, name="chemodrug-form"),
    path("htmx/drug-detail/<int:pk>/", views.drug_detail, name="drug-detail"),
    path("htmx/drug-delete/<int:pk>/delete", views.drug_delete, name="drug-delete"),
    path("htmx/drug-update/<int:pk>/update", views.update_chemodrug, name="drug-update"),
    path("chemo/<str:crnumber>/<int:pk>/", views.create_chemodrug, name="create-chemodrug"),
    path('display-tox/', views.display_tox, name='display-tox'),

    path('get-presim/<crnumber>/<s3_id>', views.get_presim, name='get-presim'),
    path('get-final-status/', views.get_final_status, name='get-final-status'),
    path('get-presim-buttons/', views.get_presim_buttons, name='get-presim-buttons'),
    path('link-presim-with-careplan/<str:presimid>/<str:s3_id>', views.link_presim_with_careplan, name="link-presim-with-careplan"),
    path('link-simulation-with-careplan/<str:simid>/<str:s3_id>', views.link_simulation_with_careplan, name="link-simulation-with-careplan"),
    path('radonc-new-presimulation/create/', views.create_presim,
         name="radonc-new-presimulation-create"),
    path('radonc-new-presimulation/<int:pk>/update/', views.edit_presim,
         name="radonc-new-presimulation-update"),
    path('radonc-new-presimulation/<int:pk>/delete/', views.delete_presim,
         name="radonc-new-presimulation-delete"),
    path('patient-search/', views.patient_search, name="patient_search"),
    path('patient-search/search/', views.search, name="search"),
]

urlpatterns += htmx_urlpatterns
