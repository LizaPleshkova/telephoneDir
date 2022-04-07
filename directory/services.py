import json
from django.db import connection


def dictfetchall_list(cursor):
    ''' Return all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchall_item(cursor):
    ''' Return all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchone()
    ]


class PersonService:

    @staticmethod
    def get_queryset_person():
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, middle_name, last_name, telephone_number FROM directory_person")
        data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_person(person_id: int):
        cursor = connection.cursor()
        cursor.execute(''' 
        SELECT id, first_name, middle_name, last_name, telephone_number
        FROM directory_person as pers
        WHERE pers.id = %s::integer
        ''', [person_id])
        data = dictfetchall_list(cursor)
        return data[0]


class DepartmentService:

    @staticmethod
    def get_queryset_department():
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, parent_id as parent FROM directory_department")
        data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_department(department_id: int):
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT id, name, parent_id as parent FROM directory_department department
            where department.id = %s::integer''', [department_id])
        data = dictfetchall_list(cursor)
        return data[0]

    @staticmethod
    def list_employes(department_id: int):
        cursor = connection.cursor()
        cursor.execute(
            '''select first_name, position, telephone_number, department.name
                from directory_employee as employee
                inner join directory_person as person on person.id = employee.person_id
                inner join directory_department as department on department.id = employee.department_id
                where department.id = %s::integer''', [department_id]
        )
        data = dictfetchall_list(cursor)
        return data


class EmployeeService:

    @staticmethod
    def get_queryset_employees():
        cursor = connection.cursor()
        cursor.execute(''' 
        SELECT id, person_id as person, position, department_id as department
        FROM directory_employee
        ''')
        data = dictfetchall_list(cursor)
        print(data)

        return data

    @staticmethod
    def get_employee(employee_id: int):
        cursor = connection.cursor()
        cursor.execute(''' 
        SELECT id, person_id as person, position, department_id as department
        FROM directory_employee as empl
        WHERE empl.id = %s::integer
        ''', [employee_id])
        data = dictfetchall_list(cursor)
        # print(data)

        return data[0]
