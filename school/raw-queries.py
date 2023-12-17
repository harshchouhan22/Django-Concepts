from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
def get_schools(request):
    raw_query =  'SELECT id, name, location FROM yourapp_school;'
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        schools_data = cursor.fetchall()

    #Convert Raw data into list of dictionaries
    schools = [{'id': school[0]} for school in schools_data]

    return JsonResponse({'data': schools, 'status':200})


# Cursor Execute (sql, params= None)
def fetch_list_with_filter(request):
    raw_query = 'SELECT * FROM your_table WHERE id = %s;'
    with connection.cursor() as cursor:
        cursor.execute(raw_query, [1])
    
    #Fetches the next row from the result set as a tuple.
    row = cursor.fetchone()

    #Fetches all rows from the result set as a list of tuples
    rows = cursor.fetchall()

    #Fetch Many, you can set the size = 10 as
    rows = cursor.fetchmany(10)

    #Moves the cursor to a new position in the result set. you can set value and mode
    cursor.scroll(2)

    # Fetches  a column
    desc  = cursor.description

    #Row.Count
    count = cursor.rowcount
    



