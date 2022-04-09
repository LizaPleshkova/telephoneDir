from django.urls import path, include
from rest_framework import routers
from directory.views import get_person, DepartmentView

from .views import EmployeeView, PersonView, get_department

router = routers.SimpleRouter()

router.register(r'department', DepartmentView, basename='department')
router.register(r'employee', EmployeeView, basename='employee')
router.register(r'person', PersonView, basename='person')

urlpatterns = [
   path('person/', get_person),
   path('depart/', get_department),
]

urlpatterns += router.urls