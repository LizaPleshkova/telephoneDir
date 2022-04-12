from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, action
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView, Response
from .serializers import DepartmanetListSerializer, EmployeeListSerializer, PersonSerializer, DepartmentSerializer
from .services import DepartmentService, EmployeeService, PersonService



class DepartmentView(mixins.ListModelMixin, RetrieveModelMixin,CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return DepartmanetListSerializer
        return DepartmanetListSerializer

    def retrieve(self, request, pk=None):
        instance = DepartmentService.get_department(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = DepartmentService.create_department(serializer.validated_data)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def patch(self, request, pk):
        try:
            new_dep_data = DepartmentService.get_department(pk)
            for field in request.data:
                if field in new_dep_data:
                    new_dep_data[field] = request.data[field]
                else:
                    raise AttributeError(f"that attr {field} doesn't exists")
            serializer = DepartmanetListSerializer(data=new_dep_data)
            if serializer.is_valid(raise_exception=True):
                DepartmentService.update_department(serializer.validated_data)
            return Response(content_type="application/json", status=status.HTTP_200_OK)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='employees', url_name='employees')
    def list_employes(self, request, pk=None):
        employess = DepartmentService.list_employes(pk)
        return Response(employess, content_type="application/json", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='child-department', url_name='child_department')
    def get_child_departments(self, request, pk=None):
        child_dep = DepartmentService.get_child_department(pk)
        return Response(child_dep, content_type="application/json", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='child-department-employees', url_name='child_department_employees')
    def get_child_departments_employees(self, request, pk=None):
        child_dep = DepartmentService.get_child_department(pk)
        child_dep_employees = DepartmentService.get_child_department_employees(child_dep)
        return Response(child_dep_employees, content_type="application/json", status=status.HTTP_200_OK)


class PersonView(mixins.ListModelMixin, RetrieveModelMixin,CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = PersonService.get_queryset_person()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return PersonSerializer
        return PersonSerializer

    def retrieve(self, request, pk=None):
        instance = PersonService.get_person(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = PersonService.create_person(serializer.validated_data)
            headers = self.get_success_headers(data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            new_pers_data = PersonService.get_person(pk)
            for field in request.data:
                if field in new_pers_data:
                    new_pers_data[field] = request.data[field]
                else:
                    raise AttributeError(f"that attr {field} doesn't exists")
            serializer = PersonSerializer(data=new_pers_data)
            if serializer.is_valid(raise_exception=True):
                PersonService.update_person(pk, serializer.validated_data)
            return Response(content_type="application/json", status=status.HTTP_200_OK)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)


class EmployeeView( mixins.ListModelMixin, RetrieveModelMixin, CreateModelMixin,  viewsets.GenericViewSet, APIView):
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        search_value = request.query_params.get('search')
        if search_value:
            return EmployeeService.search_employee(search_value)
        else:
            return EmployeeService.get_queryset_employees()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return EmployeeListSerializer
        return EmployeeListSerializer

    def retrieve(self, request, pk=None):
        try:
            instance = EmployeeService.get_employee(pk)
            if instance !=[]:
                serializer = self.get_serializer(instance)
                return Response(serializer.data,  content_type="application/json", status=status.HTTP_200_OK)
            else:
                return Response(content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = EmployeeService.create_employee(serializer.validated_data)
            headers = self.get_success_headers(data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            new_empl_data = EmployeeService.get_employee(pk)

            for field in request.data:
                if field in new_empl_data:
                    new_empl_data[field] = request.data[field]   
                else:
                    raise AttributeError(f"that attr {field} doesn't exists")
            serializer = EmployeeListSerializer(data=new_empl_data)
            if serializer.is_valid(raise_exception=True):
                EmployeeService.update_employee(serializer.validated_data)
            return Response(content_type="application/json", status=status.HTTP_200_OK)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            return Response(format(error), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk:
            EmployeeService.delete_employee(pk)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)