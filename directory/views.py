from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView, Response
from .serializers import DepartmanetListSerializer, EmployeeListSerializer, PersonSerializer, DepartmentSerializer
from .models import Department
from .services import DepartmentService, EmployeeService, PersonService


class DepartmentView(mixins.ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    # serializer_class = DepartmentSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        # queryset = Department.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return DepartmanetListSerializer
        return DepartmanetListSerializer

    def retrieve(self, request, pk=None):
        ''' взять первый эелемент списка '''
        instance = DepartmentService.get_department(pk)
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='employees', url_name='employees')
    def list_employes(self, request, pk=None):
        employess = DepartmentService.list_employes(pk)

        return Response(employess, content_type="application/json", status=status.HTTP_200_OK)



class PersonView(mixins.ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    
    def get_queryset(self, *args, **kwargs):
        queryset = PersonService.get_queryset_person()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return PersonSerializer
        return PersonSerializer

    def retrieve(self, request, pk=None):
        ''' something wrong. CHECK! '''
        instance = PersonService.get_person(pk)
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)




class EmployeeView(mixins.ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    # serializer_class = DepartmentSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = EmployeeService.get_queryset_employees()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return EmployeeListSerializer
        return EmployeeListSerializer

    def retrieve(self, request, pk=None):
        ''' взять первый эелемент списка '''
        instance = EmployeeService.get_employee(pk)
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)


    # def list(self, request, *args, **kwargs):
    #     queryset = DepartmentService.get_queryset_department()
    #     # queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='employees', url_name='employees')
    def list_employes(self, request, pk=None):
        employess = DepartmentService.list_employes(pk)

        return Response(employess, content_type="application/json", status=status.HTTP_200_OK)



@api_view(['GET'])
def get_person(request):
    person = PersonService.get_queryset_person()
    ser = PersonSerializer(person, many=True)
    return Response(ser.data, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department(request):
    person = DepartmentService.get_queryset_department()
    ser = DepartmentSerializer(data=person, many=True)
    ser.is_valid(raise_exception=True)
    return Response(ser.validated_data, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department(request):
    person = DepartmentService.get_queryset_department()
    ser = DepartmentSerializer(data=person, many=True)
    ser.is_valid(raise_exception=True)
    return Response(ser.validated_data, content_type='application/json', status=status.HTTP_200_OK)
