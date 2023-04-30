from django.urls import path
from .views import SimulationsList, PreSimulationList, UpdateExpoToken

urlpatterns = [
    path('get-simulations/<str:username>/<str:days>/', SimulationsList.as_view(), name='get-simulations'),
    path('get-presimulations/<str:username>/<str:days>/', PreSimulationList.as_view(), name='get-presimulations'),
    path('updateexpotoken/<str:username>/', UpdateExpoToken.as_view(), name='update-expo-token'),
]
