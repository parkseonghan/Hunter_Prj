import cx_Oracle

#한글 지원 방법
import os
os.putenv('NLS_LANG', '.UTF8')

ora_id = ''
ora_pw = ''
ora_url = ''

#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)
connection = cx_Oracle.connect(ora_id,ora_pw,ora_url)

cursor = connection.cursor()

cursor.execute("""
   SELECT SYSDATE as date1  FROM DUAL
   """
)

for date1 in cursor:
   print("날짜 : ", date1)