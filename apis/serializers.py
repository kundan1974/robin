from rest_framework import serializers
from patient_data.models import Simulation, NewPreSimulation, User, SimStatus
from users.models import Profile

class UserSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_superuser']


class SimulationSerializer(serializers.ModelSerializer):
    """
    
    """
    user = UserSerializer()

    class Meta: 
        model = Simulation
        fields = '__all__'
        # fields = ['name', 'simdate', 'simparent', 'assignedto', ]



class PreSimulationSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta: 
        model = NewPreSimulation
        fields = '__all__'


class SimulationStatusSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta:
        model = SimStatus
        fields = "__all__"