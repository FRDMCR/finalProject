#inset 4 cases
#수정 주문번호 제외 모두
'''
//작성자--------------------------//
충북대학교 컴퓨터공학과
2014040013 정성진
tjdwls0607@naver.com
//프로그램 명---------------------//
order management program
//프로그램 구성-------------------//
query.py
orderMngDb.py
orderManagement.py
//마지막 수정 날짜----------------//
2019-06-12
'''

import sqlite3
from query import *

PATH = "C:/sqlite/ReportDB.db"     # 사용할 DB의 경로
query = Query()     # 쿼리문을 만들기 위해 query.py의 Query 클래스 객체를 전역 변수로 사용

class Function() :
    '''
    orderManagement 프로그램에서 사용될 기능들 중
    Database를 연동해야 하는 부분들
    '''

    def __init__(self) :
        pass

    ## 거래처 현황 조회해서 열 리스트로 반환 ##
    def readCustomerStat(self, var) :
        rowsList = []       # 조회한 열들의 리스트
        sql = query.selectCustomerStat()    

        with sqlite3.connect(PATH) as con :
            cur = con.cursor()
            
            cur.execute(sql)
            for i, row in enumerate(cur.fetchall()):
                if var == 'id' :            
                        rowsList.insert(i, row[0])   # 조회한 열(튜플)의 인스턴스를 요청한 값(var)에 따라 한 행씩 리스트에 삽입
                elif var == 'name' :                 # row[0] = CustomerID, row[1] = CompanyName
                    rowsList.insert(i, row[1])
                else :
                    print("잘못된 값을 요청했습니다.")
                    return "error"          
            
        return rowsList

    ## 거래처 별 주문 현황 조회해서 열 리스트로 반환 ##
    def readOrderStat(self, customerID) :
        rowsList = []       
        sql = query.selectOrderStat(customerID)

        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            cur.execute(sql)
            for i, row in enumerate(cur.fetchall()):    # row[0] = OrderID, row[1] = OrderDate, row[2] = ProductID
                rowsList.insert(i, row)                 # row[3] = ProductName, row[4] = Quantity, row[5] = UnitPrice 
                                                        # row[6] = TotalPrice
        return rowsList

    ## 추가 & 수정 ##
    def insert(self, customerID, companyName, orderID, orderDate,
                productID, productName, unitPrice, quantity) :
        sql = ""  
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            sql = query.insertCustomers(customerID, companyName)
            con.commit()

    def update(self) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            con.commit()

    def delete(self, orderID, productID) :
        sql = ""
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            sql = query.deleteOrderDetails(orderID, productID)
            cur.execute(sql)
            sql = query.deleteOrders(orderID)
            cur.execute(sql)
            sql = query.deletePorducts(productID)
            cur.execute(sql)
            
            
            con.commit()
