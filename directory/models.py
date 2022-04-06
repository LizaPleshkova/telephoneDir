from django.db import models


class Department(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id}  - {self.parent} - {self.name}'


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone_number = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name}  - {self.middle_name} - {self.last_name} - {self.telephone_number}'


class Employee(models.Model):
    '''
    должность?position вынести в отдельную таблицу??
    '''
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_employee')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='empl_department')
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id}  - [{self.person.first_name}- {self.person.last_name}] - {self.department.name} - {self.position}'
