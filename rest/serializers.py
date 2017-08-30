from rest_framework import serializers
from app.models import *

# Serializers define the API representation.
class ProjectsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'created_at')


class JobTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobTypes
        fields = ('id', 'name')


class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        fields = ('name', 'phone', 'email')

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Users
        fields = ('user', 'phone', 'avatar', 'color_hoe_header', 'color_hoe_right_header', 'color_hoeapp_container')


class WorksSerializer(serializers.HyperlinkedModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')
    leader = serializers.ReadOnlyField(source='leader.id')
    support1 = serializers.ReadOnlyField(source='support1.id')
    support2 = serializers.ReadOnlyField(source='support2.id')
    support3 = serializers.ReadOnlyField(source='support3.id')
    support4 = serializers.ReadOnlyField(source='support4.id')
    support5 = serializers.ReadOnlyField(source='support5.id')
    customer = serializers.ReadOnlyField(source='customer.id')

    class Meta:
        model = Works
        fields = ('project', 'address', 'date', 'initial_time',
        'leader', 'support1','support2','support3','support4','support5',
        'register_time', 'latitude_register', 'longitude_register', 'end_time',
        'report', 'photo1', 'photo2', 'photo3', 'photo4', 'is_completed', 'notes',
        'customer', 'evaluation', 'sign')


class WorksTypesSerializer(serializers.HyperlinkedModelSerializer):
    work = serializers.ReadOnlyField(source='work.id')
    type = serializers.ReadOnlyField(source='type.id')
    work_name = serializers.ReadOnlyField(source='work.name')
    type_name = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = WorksTypes
        fields = ('work', 'type', 'work_name', 'type_name')
