import psycopg2
connection = psycopg2.connect('dbname=ray2')

id = int(input("id= "))
name = input("name= ")

data = {}
data["id"] = id
data["name"] = name

cursor = connection.cursor()
cursor.execute('''
    INSERT INTO student (id,name) VALUES(%(id)s,%(name)s);
'''
,data )

connection.commit()

connection.close()
cursor.close()

