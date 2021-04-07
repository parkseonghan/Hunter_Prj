import pymysql


class Db_conn:

    def __init__(self):
        self.host = '192.168.19.234'
        self.port = 40022
        self.user = 'root'
        self.pwd = 'cic_study!@'
        self.db = 'cic_study'

    def connection(self):
        try:
            conn = pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.pwd,
                                   db=self.db,
                                   charset='utf8')
            return conn
        except Exception as e:
            print(str(e))
            return None

    def db_insert(self, sql):
        print("++++++++ " + sql + " ++++++++")
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()



# ==== DB CONNECTION ==== #
# http://pythonstudy.xyz/python/article/202-MySQL-%EC%BF%BC%EB%A6%AC
# db_cls = db_con.Db_conn()
# dbcon = db_cls.connection()
# cursor = dbcon.cursor()  # cursor 객체 생성 : db에 sql문 수행하고 조회된 결과 가지고 오는 역할
# cursor.execute("SELECT name, pNum, pwd, DATE_FORMAT(date, '%Y%m%d'), time, writeDate FROM serena")
# rows = cursor.fetchall()  # fetchall : 조회된 결과 모두 리스트로 반환
# dbcon.close()
# print(rows)





# if conn.open:
#     with conn.cursor() as curs:
#         print("db connected")
#
#
# conn.close()
