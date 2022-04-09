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
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, first_name, middle_name, last_name, telephone_number FROM directory_person")
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_person(person_id: int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT id, first_name, middle_name, last_name, telephone_number
            FROM directory_person as pers
            WHERE pers.id = %s::integer
            ''', [person_id])
            data = dictfetchall_list(cursor)
        return data[0]

    @staticmethod
    def update_person(person_id: int, new_data):
        person = PersonService.get_person(person_id)
        print(person)
        with connection.cursor() as cursor:
            print('herre')
            cursor.execute(''' 
            update directory_person 
            set  first_name=%s, middle_name=%s, last_name=%s, telephone_number=%s
            where id =  %s::integer
            ''', [new_data['first_name'], new_data['middle_name'], new_data['last_name'], new_data['telephone_number'], new_data['id']])


class DepartmentService:

    @staticmethod
    def get_queryset_department():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, parent_id as parent FROM directory_department")
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_department(department_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT id, name, parent_id as parent FROM directory_department department
                where department.id = %s::integer''', [department_id])
            data = dictfetchall_list(cursor)
        return data[0]

    @staticmethod
    def list_employes(department_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                '''select first_name, position, telephone_number, department.name
                    from directory_employee as employee
                    inner join directory_person as person on person.id = employee.person_id
                    inner join directory_department as department on department.id = employee.department_id
                    where department.id = %s::integer''', [department_id]
            )
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_child_department(department_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                '''WITH  RECURSIVE included_department(id, parent_id, name) as (
                    SELECT t1.id, t1.parent_id, t1.name
                    FROM directory_department as t1
                    WHERE t1.id = %s::integer
                    UNION all
                    SELECT t2.id, t2.parent_id, t2.name
                    FROM directory_department as t2
                    INNER JOIN included_department as i_d ON i_d.id = t2.parent_id
                )
                SELECT id, parent_id as parent, name FROM included_department
            ''', [department_id]
            )
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_child_department_employees(departments):
        print(departments, type(departments[0]))

        # dep_list = (print(i) for i in departments['id'])
        print(dep_list)
        with connection.cursor() as cursor:
            cursor.execute(
                '''
            '''
            )
            data = dictfetchall_list(cursor)
        return data


class EmployeeService:

    @staticmethod
    def get_queryset_employees():
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT id, person_id as person, position, department_id as department
            FROM directory_employee
            ''')
            data = dictfetchall_list(cursor)
            print(data)

        return data

    @staticmethod
    def get_employee(employee_id: int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT id, person_id as person, position, department_id as department
            FROM directory_employee as empl
            WHERE empl.id = %s::integer
            ''', [employee_id])
            data = dictfetchall_list(cursor)
            # print(data)
        return data[0]
