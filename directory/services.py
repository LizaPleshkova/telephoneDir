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
    def create_person(new_person):
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO directory_person (first_name, middle_name,last_name,telephone_number)
                   VALUES(%s, %s, %s, %s) RETURNING *;''', [new_person['first_name'], new_person['middle_name'], new_person['last_name'], new_person['telephone_number']]
            )
            data = dictfetchall_list(cursor)
        return data

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

    @staticmethod
    def is_exists(pers_id: int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            select exists(
                select 1 
                from directory_person
                where id=%s
            )
            ''', [pers_id])
            data = cursor.fetchone()
        return data[0]

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
    def create_department(new_deaprtment):
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO directory_department as dep (name, parent_id)
                   VALUES(%s, %s::integer) RETURNING *;''', [new_deaprtment['name'], new_deaprtment['parent']]
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
        department_ids = [dep['id'] for dep in departments]
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM directory_employee
                WHERE department_id = ANY(%s)
            ''', [department_ids]
            )
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def is_exists(dep_id: int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            select exists(
                select 1 
                from directory_department
                where id=%s
            )
            ''', [dep_id])
            data = cursor.fetchone()
        return data[0]
    
    @staticmethod
    def update_department(new_data):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            update directory_department
            set name=%s, parent_id=%s
            where id =  %s::integer
            ''', [new_data['name'], new_data['parent'], new_data['id']])


class EmployeeService:

    @staticmethod
    def get_queryset_employees():
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT id, person_id as person, position, department_id as department
            FROM directory_employee
            ''')
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def get_employee(employee_id: int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT id, person_id as person, position, department_id as department
            FROM directory_employee as empl
            WHERE empl.id = %s
            ''', [employee_id])
            data = dictfetchall_list(cursor)
            print(data)
        return data[0]

    @staticmethod
    def search_employee(search_str: str):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            SELECT empl.id, person_id as person, position, department_id as department
            FROM directory_employee as empl
            INNER JOIN directory_person as person ON person.id = empl.person_id
            WHERE first_name || middle_name || last_name ILIKE '%%' || %s || '%%' or position ILIKE '%%' || %s || '%%'
            ''', [search_str, search_str])
            data = dictfetchall_list(cursor)
        return data

    @staticmethod
    def create_employee(new_empl):
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO directory_employee (person_id, department_id, position)
                   VALUES(%s, %s, %s) RETURNING *;''', [new_empl['person'], new_empl['department'], new_empl['position']]
            )
            data = dictfetchall_list(cursor)
        return data


    @staticmethod
    def update_employee(new_data):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            update directory_employee
            set person_id=%s, position=%s, department_id=%s
            where id =  %s::integer
            ''', [new_data['person'], new_data['position'], new_data['department'], new_data['id']])

    @staticmethod
    def delete_employee(employee_id:int):
        with connection.cursor() as cursor:
            cursor.execute(''' 
            DELETE FROM directory_employee
            WHERE id = %s::integer
            ''', [employee_id])
            # data = cursor.fetchone()
            # print(data)
