from django.contrib import admin
from .models import Department, Employee, Person


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'parent', 'name'
    )
    search_fields = ['parent', 'name']
    list_filter = ['parent']


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'middle_name', 'last_name', 'telephone_number'
    )
    search_fields = ['last_name']
    list_filter = ['last_name']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'person', 'department', 'position'
    )
    search_fields = ['name']
    list_filter = ['person', 'department']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Employee, EmployeeAdmin)
