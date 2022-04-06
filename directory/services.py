from django.db import connection


def dictfetchall(cursor):
    ''' Return all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class PersonService:

    @staticmethod
    def get_queryset_person():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM directory_person")
        data = dictfetchall(cursor)
        return data


class DepartmentService:

    @staticmethod
    def get_queryset_department():
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, parent_id as parent FROM directory_department")
        data = dictfetchall(cursor)
        print(data)
        return data


class EmployeeService:

    @staticmethod
    def get_queryset_employee():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM directory_employee")
        data = dictfetchall(cursor)
        return data




