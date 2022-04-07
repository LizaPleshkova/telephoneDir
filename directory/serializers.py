from rest_framework import serializers
from rest_framework.utils import json
from directory.services import DepartmentService, PersonService, EmployeeService
from .models import Employee, Department, Person


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    telephone_number = serializers.CharField()


class DepartmanetListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.IntegerField(allow_null=True)
    name = serializers.CharField()


class EmployeeListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    person = serializers.IntegerField()
    position = serializers.CharField()
    department = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        pers_id = representation['person']
        dep_id = representation['department']

        dep = DepartmentService.get_department(dep_id)
        serializer_dep = DepartmanetListSerializer(dep)

        pers = PersonService.get_person(pers_id)
        serializer_pers = PersonSerializer(pers)

        representation['department'] = serializer_dep.data
        representation['person'] = serializer_pers.data
        return representation


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
