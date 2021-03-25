import pandas as pd

import cx_Oracle

import os

os.putenv('NLS_LANG', 'KOREAN_KOREA.KO16MSWIN949')

con1 = cx_Oracle.connect("dreamer/dsdvp@djh")

professor = pd.read_sql("select * from dual",con=con1)

professor.head()

