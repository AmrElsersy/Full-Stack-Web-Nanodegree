import psycopg2
connection = psycopg2.connect('dbname=ray2')

cursor = connection.cursor()


# this instructions has no effect on fetch functions as this is not the last instruction
cursor.execute('''
    SELECT * FROM student WHERE id >= 30;
'''
)

# last executed instructions >> its output >> fetch
cursor.execute('''
    SELECT * FROM student WHERE id < 30;
'''
)


# fetch 1 output of the last instruction executed (the first one)
result2 = cursor.fetchone()
print(result2)

# fetch x output from buffer starting from the begining of the output array
result_x = cursor.fetchmany(2)
print(result_x)

# fetch all output remain from buffer
result = cursor.fetchall()
print(result)


# save changes to database
connection.commit()
# close
cursor.close()
connection.close()

