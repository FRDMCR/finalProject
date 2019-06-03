#insert나 update 할 떄 key 예외처리
#PK는 수정 x
#orderDetail 수정할 때 unitPrice는 productID에서 
#orderDetail 수정할 때 productID 중보 예외처리
#delete 질문 

import sqlite3
from query import *

PATH = "C:/sqlite/ReportDB"
query = Query()

class Function() :

    def __init__(self) :
        pass

    def readCustomer(self) :
        rows = None,  # 조회한 열들의 튜플
        sql = query.selectCustomer()

        with sqlite3.connect(PATH) as con :
            cur = con.cursor()
            
            cur.execute(sql)
            for

    def readOrder(self, customerID) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

        

    def insert(self) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            con.commit()

    def update(self) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            con.commit()

    def delete(self) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            con.commit()
