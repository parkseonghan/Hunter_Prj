import inc_file.db_con as dbcon


dbcls = dbcon.db_con()
dbcon = dbcls.dbconnection()
cursor = dbcon.cursor()
cursor.execute("SELECT no, name, birthday, tel, DATE_FORMAT(create_date, '%Y%m%d') FROM yulim_test")
rows = cursor.fetchall()

print(rows)