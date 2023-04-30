from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from patient_data.models import Simulation, NewPreSimulation
from .serializers import SimulationSerializer, PreSimulationSerializer
from django.contrib.auth.models import User
from users.models import Profile

class SimulationsList(APIView):
    """
    Get Simulation List for specified user
    Input: user_id
    """
    permission_classes = [IsAuthenticated]
    # Add auth class
    def get(self, request,username, days):
        delta_days = timezone.now() - timezone.timedelta(int(days))
        simulations = Simulation.objects.filter(assignedto=username).filter(simdate__gt=delta_days)      
        if simulations:
            simulationsserializer = SimulationSerializer(simulations, many=True)
            return Response(simulationsserializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No data found", status=status.HTTP_204_NO_CONTENT)
        
class PreSimulationList(APIView):
    """
    Get Presimulation list for specified user
    Input: user_id, and future days
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username, days):
        # presimulations = NewPreSimulation.objects.filter(assignedto=username)
        # presimdata = NewPreSimulation.objects.prefetch_related().filter(date__gt=delta_date_5).order_by('-date').all()
        presimulations = NewPreSimulation.objects.prefetch_related().filter(assessedby=username).order_by('-date')
        if presimulations:
            presimulationserializer = PreSimulationSerializer(presimulations, many=True)
            return Response(presimulationserializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No data found", status=status.HTTP_204_NO_CONTENT)


class PatientsList(APIView):
    """
    Fetch all on going patients list
    Input: user_id
    """
    def get(self, request, username):
        """
        Pass
        """
        pass


class GetUser(APIView):
    """
    Get user details
    Input: username
    """
    def get(self, request, username):
        user_details = User.objects.filter(username=username)
        if user_details:
            pass
        else:
            return Response("No data found", status=status.HTTP_204_NO_CONTENT)



class UpdateExpoToken(APIView):
    def put(self, request, username):
        user_id = username
        print(user_id)
        print(request.data)
        profile = Profile.objects.get(user_id=user_id)
        if not profile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile.expotoken = request.data.get('expotoken')
        profile.save()
        return Response(status=status.HTTP_200_OK)