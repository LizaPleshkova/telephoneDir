from rest_framework import serializers
from rest_framework.utils import json

from .models import Employee, Department, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class DepartmanetParentSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        print('DP', attrs)
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print('DP', representation)
        return json.dumps(representation)


class DepartmentSerializer(serializers.ModelSerializer):
    parent = DepartmanetParentSerializer(allow_null=True)

    class Meta:
        model = Department
        fields = '__all__'

    def to_internal_value(self, data):
        print('IV', data)
        parent_id = data['parent']
        print(parent_id)
        return data
