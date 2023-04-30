from rest_framework import serializers
from patient_data.models import Simulation, NewPreSimulation
from users.models import Profile

class SimulationSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta: 
        model = Simulation
        fields = '__all__'



class PreSimulationSerializer(serializers.ModelSerializer):
    """
    
    """
    class Meta: 
        model = NewPreSimulation
        fields = '__all__'


