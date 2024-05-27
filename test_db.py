import dbconnect as db
from datetime import datetime


def add_employee():
# We use the function modifydatabase() -- it has 2 arguments
# The first argument is the sql code, where we use a placeholder %s
# The second argument is ALWAYS a list of values to replace the %s in the sql code
   sqlcode = """ INSERT INTO employees (
   employee_id,
   employee_name,
   role_id,
   start_role_date
   )
   VALUES (%s, %s, %s, %s)"""

   db.modifydatabase(sqlcode, ['65','LaiaV','45', datetime.now()])
   db.modifydatabase(sqlcode, ['51','MonicaP','36', datetime.now()])
   # Just some feedback that the code succeeded
   print('done!')


sql_query = """ SELECT * FROM employees"""
values = []
# number of column names must match the attributes for table genres
columns = ['employee_id', 'employee_name', 'role_id', 'start_role_date','end_role_date','manager_id']
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)


sql_add_employee = """
TRUNCATE TABLE employees """

db.modifydatabase(sql_add_employee, [])
add_employee()
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)





### 



def add_roles():
# We use the function modifydatabase() -- it has 2 arguments
# The first argument is the sql code, where we use a placeholder %s
# The second argument is ALWAYS a list of values to replace the %s in the sql code
   sqlcode = """ INSERT INTO roles (
   role_id,
   role_name,
   division,
   create_date
   )
   VALUES (%s, %s,%s,%s)"""

   db.modifydatabase(sqlcode, ['1','Data Analyst','Business Intelligence Team', datetime.now()])
   db.modifydatabase(sqlcode, ['2','Machine Learning Engineer','Modeling Team', datetime.now()])
   db.modifydatabase(sqlcode, ['3','Data Engineer','Data Engineering Team', datetime.now()])
   db.modifydatabase(sqlcode, ['4','Business Intelligence Analyst','Business Intelligence Team', datetime.now()])

   # Just some feedback that the code succeeded
   print('done!')


sql_query = """ SELECT * FROM roles"""
values = []
# number of column names must match the attributes for table genres
columns = ['role_id', 'role_name', 'division', 'create_date','delete_date']
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)

sql_add_roles = """
TRUNCATE TABLE roles """

db.modifydatabase(sql_add_roles, [])
add_roles()
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)
