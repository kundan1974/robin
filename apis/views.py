from django.utils import timezone
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from patient_data.models import Simulation, NewPreSimulation, SimStatus
from .serializers import SimulationSerializer, PreSimulationSerializer, UserSerializer, SimulationStatusSerializer
from django.contrib.auth.models import User
from users.models import Profile
from .utils import send_push_notifications_to_all

class SimulationsList(APIView):
    """
    Get Simulation List for specified user
    Input: user_id
    """
    permission_classes = [IsAuthenticated]
    # Add auth class
    # TODO: Current day
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



@api_view(['GET'])
def user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_simulation_status(request):
    """
    Fetching simulation status from SimStatus table
    """
    try:
        sim_status = SimStatus.objects.all()
        sim_status_serializer = SimulationStatusSerializer(sim_status, many=True)
        if sim_status_serializer:
            return Response(sim_status_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Statues not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({'error': 'Statues not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def update_simulation_status(request, sim_id):
    """
    update_simulation_status
    """
    try:
        code = request.data['code']
        print(sim_id)
        s_code = SimStatus.objects.get(code=code)
        sim = Simulation.objects.get(simid=sim_id)
        sim.initialstatus = s_code
        print(sim)
        sim.save()
        msg = f"Simulation process is updated for {sim.simparent}"
        send_push_notifications_to_all(msg)
        return Response({'success': True})
    except Simulation.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)
    except SimStatus.DoesNotExist:
        return Response({'error': 'Task status not found'}, status=404)


#TODO: Remove this
def update_status(request, task_id):
    status_code = request.data['status_code']
    s_code = TaskStatus.objects.get(id=status_code)
    task = Task.object.get(id=task_id)
    task.status= s_code
    task.save()
    return Response({'success': True})


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
    

class GetStats(APIView):
    """
    1. Today's Implementations count
    2. Completing Today Count
    3. Near Comletion  Count
    """
    def get(self, request):
        todays_implementations_count = Simulation.objects.filter(impdate=timezone.now().date()).count()
        completing_today_count = Simulation.objects.filter(tentativecompletiondate=timezone.now().date()).count()
        delta_date_3 = timezone.now() + timezone.timedelta(3)
        near_completion_count = Simulation.objects.filter(
        tentativecompletiondate__gt=timezone.now().date()).filter(tentativecompletiondate__lte=delta_date_3).count()
        data = {
            'todays_implementations': todays_implementations_count,
            'completing_today': completing_today_count,
            'near_completion': near_completion_count
        }
        return JsonResponse(data)


class GetTodaysSimulations(APIView):
    """
    Get Todays Simulations
    """
    def get(self, request):
        # delta_days = timezone.now() - timezone.timedelta(int(days))
        # delta_days = timezone.now() - timezone.timedelta(3)
        # todays_simulations = Simulation.objects.filter(simdate__gt=delta_days).prefetch_related(
        # 'assignedto'
        # )

        todays_simulations = Simulation.objects.filter(simdate=timezone.now().date()).prefetch_related(
        'assignedto'
        )

        if todays_simulations:
            simulationsserializer = SimulationSerializer(todays_simulations, many=True)
            return Response(simulationsserializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No data found", status=status.HTTP_204_NO_CONTENT)     
        