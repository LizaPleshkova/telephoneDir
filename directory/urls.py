from django.urls import path, include
from rest_framework import routers
from directory.views import DepartmentView,EmployeeView, PersonView

router = routers.SimpleRouter()

router.register(r'department', DepartmentView, basename='department')
router.register(r'employee', EmployeeView, basename='employee')
router.register(r'person', PersonView, basename='person')


urlpatterns = router.urls