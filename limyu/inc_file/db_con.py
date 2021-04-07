import pymysql

class db_con :
    def __init__(self):
        self.dburl = '192.168.19.234'
        self.dbuser = 'root'
        self.dbpw = 'cic_study!@'
        self.dbname = 'cic_study'
        self.dbport = 40022

    def dbconnection(self):
        try :
            dbcon = pymysql.connect(user=self.dbuser, passwd=self.dbpw, db=self.dbname, port=self.dbport, host=self.dburl, charset='utf8')
            return dbcon
        except Exception as e:
            print(str(e))
            return None