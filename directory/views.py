from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.utils import json

from rest_framework.views import APIView, Response
from .serializers import PersonSerializer, DepartmentSerializer
from .models import Department
from .services import DepartmentService, PersonService


class DepartmentView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = DepartmentSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        # queryset = Department.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = DepartmentService.get_queryset_department()
        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
