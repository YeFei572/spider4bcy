import pymysql

conn = pymysql.Connect(host='localhost', port=3306, user="root", password="keppel2016", database="estate")
course = conn.cursor()
sql01 = 'select * from user'
course.execute(sql01)
result = course.fetchall()
for item in result[0] :
    print(item)
conn.commit()
print(result)
course.close()
conn.close()