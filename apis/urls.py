from django.urls import path
from .views import SimulationsList, PreSimulationList, UpdateExpoToken, GetStats, GetTodaysSimulations, user_details, get_simulation_status,update_simulation_status

urlpatterns = [
    path('get-simulations/<str:username>/<str:days>/', SimulationsList.as_view(), name='get-simulations'),
    path('get-todays-simulations/', GetTodaysSimulations.as_view(), name='get-todays-simulations'),
    path('get-presimulations/<str:username>/<str:days>/', PreSimulationList.as_view(), name='get-presimulations'),
    path('get-stats/', GetStats.as_view(), name='get-stats'),
    path('get-simulation-status/', get_simulation_status, name='get_simulation_status'),
    path('update-simulation-status/<str:sim_id>/', update_simulation_status, name='update_simulation_status'),
    path('updateexpotoken/<str:username>/', UpdateExpoToken.as_view(), name='update-expo-token'),
    path('get-user/<str:user_id>', user_details, name="get-user")
]
