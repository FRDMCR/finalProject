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
2019-06-16
'''

import sqlite3
from query import *

PATH = "C:/sqlite/ReportDB.db"     # 사용할 DB의 경로
query = Query()     # 쿼리문을 만들기 위해 query.py의 Query 클래스 객체를 전역 변수로 사용

## PK 중복 검사 함수 ##
def dupliCheck(cursor, pk, tableName) :
    if tableName == 'Customers' :
        cursor.execute(query.selectCustomersPK())
        for row in cursor.fetchall():
            if pk == row[0] :
                return "duplCstomer"
            else :
                return "clear"
    elif tableName == 'Products' :
        cursor.execute(query.selectProductsPK())
        for row in cursor.fetchall():
            if pk == row[0] :
                return "duplProduct"
            else :
                return "clear"
    elif tableName == 'Orders' :
        cursor.execute(query.selectOrdersPK())
        for row in cursor.fetchall():
            if pk == row[0] :
                return "duplOrder"
            else :
                return "clear"
    elif tableName == 'OrderDetails' :
        cursor.execute(query.selectOrderDetailsPK())
        for row in cursor.fetchall():
            if pk == row :
                return "duplOrderDetail"
            else :
                return "clear"

class Function :
    '''
    orderManagement 프로그램에서 사용될 기능들 중
    Database를 연동해야 하는 부분들
    '''

    def __init__(self) :
        pass

    ## 테이블의 ID 리스트 반환 ##
    def getIDList(self, table) :
        idList = []       # 조회한 ID 리스트
        if table == 'Customers' :
            sql = query.selectCustomersPK()
        elif table == 'Products' :
            sql = query.selectProductsPK()
        elif table == 'Orders' :
            sql = query.selectOrdersPK()

        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            cur.execute(sql)
            for i, row in enumerate(cur.fetchall()):
                idList.insert(i, row) 

        return idList

    ## 거래처 현황 조회해서 열 리스트로 반환 ##
    def readCustomerStat(self, column) :
        rowsList = []       # 조회한 열들의 리스트
        sql = query.selectCustomerStat()    

        with sqlite3.connect(PATH) as con :
            cur = con.cursor()
            
            cur.execute(sql)
            for i, row in enumerate(cur.fetchall()):
                if column == 'id' :            
                        rowsList.insert(i, row[0])   # 조회한 열(튜플)의 인스턴스를 요청한 값(column)에 따라 한 행씩 리스트에 삽입
                elif column == 'name' :                 # row[0] = CustomerID, row[1] = CompanyName
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

    ## choice 별 추가, 주문 번호는 항상 추가되도록 ##
    # 아에 다 받고 하던지 -> 선택 시에 새로 추가하는 거 선택하면 자동으로 +1된 ID값
    # 그럼 인자값에 디폴트로 넣어주기?
    # 중복검사는 자동 증가로 ?
    # commit
    # 트랜잭션 문제
    # ID 값을 가져와야해 -> 아에 화면에 값을 넣어 놓고 그걸 가져올거냐 어차피 화면에는 표시할거임, 여기서 넣을거냐
    # 중복검사만 하자 반복문 try
    def insert(self, customerID, orderID, productID,
                companyName, orderDate, productName, unitPrice, quantity) :
        sqlCus = query.insertCustomers(customerID, companyName)             # 각 테이블 별 삽입 sql
        sqlOrd = query.insertOrders(orderID, customerID, orderDate)
        sqlPro = query.insertProducts(productID, productName)
        sqlOrdd = query.insertOrderDetails(orderID, productID, unitPrice, quantity)
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()
    
            cusCheck = dupliCheck(cur, customerID, 'Customers')
            ordCheck = dupliCheck(cur, int(orderID), 'Orders')
            proCheck = dupliCheck(cur, int(productID), 'Products')
            orddCheck = dupliCheck(cur, (int(orderID),int(productID)) ,'OrderDetails')

            try :   # sql에 올바른 값 입력되는 지 검사
                if cusCheck == "clear" and ordCheck == "clear" and proCheck == "clear" : 
                    # 모든 정보 추가
                    
                    cur.execute(sqlCus)
                    con.commit()
                    print(sqlOrd)
                    cur.execute(sqlOrd)
                    con.commit()
                    print("2")
                    print(sqlPro)
                    cur.execute(sqlPro)
                    con.commit()
                    
                    print("3")
                    print(sqlOrdd)
                    cur.execute(sqlOrdd)
                    con.commit()
                    print("4")

                elif cusCheck == "duplCustomer" and ordCheck == "clear" and proCheck == "clear" : 
                    # 거래처는 기존, 품목, 주문, 주문 세부 정보 추가

                    cur.execute(sqlOrd)
                    con.commit()
                    cur.execute(sqlPro)
                    con.commit()
                    cur.execute(sqlOrdd)
                    con.commit()

                elif cusCheck == "duplCustomer" and ordCheck == "duplOrder" and proCheck == "clear" : 
                    # 거래처 & 주문 기존, 품목, 주문 세부 정보 추가

                    cur.execute(sqlPro)
                    con.commit()
                    cur.execute(sqlOrdd)
                    con.commit()

                elif cusCheck == "duplCustomer" and ordCheck == "clear" and proCheck == "duplProduct" :   
                    # 거래처 & 품목 기존, 주문, 주문 세부 정보 추가

                    cur.execute(sqlOrdd)
                    con.commit()

                elif cusCheck == "duplCustomer" and ordCheck == "duplOrder" and proCheck == "duplProduct" and orddCheck == "clear" :  
                    # 주문 세부 정보만 추가

                    cur.execute(sqlOrdd)
                    con.commit()

                elif cusCheck == "duplCustomer" and ordCheck == "duplOrder" and proCheck == "duplProduct" and orddCheck == "duplOrderDetail": 
                    # 중복 = 추가 불가

                    return "duplication"

                else :  # 위의 경우들을 제외한 별도 추가 요청 금지
                    return "impossible"
            except :
                raise ValueError
            
            return "clear"
            
    ## 주문번호를 기준으로 수정 ##
    def update(self, customerID, companyName, orderID, orderDate,
                productID, productName, unitPrice, quantity) :
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            try :
                sql = query.updateCustomers(customerID, companyName)
                cur.execute(sql)
                sql = query.updateOrders(orderID, customerID, orderDate)
                cur.execute(sql)  
                sql = query.updateProducts(productID, productName)
                cur.execute(sql)
                sql = query.updateOrderDetails(orderID, productID, unitPrice, quantity)
                cur.execute(sql)

                con.commit()
            except :
                raise ValueError

    ## 주문현황 선택 삭제 ##
    def delete(self, orderID) :
        sql = ""
        with sqlite3.connect(PATH) as con :
            cur = con.cursor()

            sql = query.deleteOrderDetails(orderID)
            cur.execute(sql)
            con.commit()
            sql = query.deleteOrders(orderID)
            cur.execute(sql)
            
            con.commit()
'''
test = Function()
print(test.getIDList('OrderDetails'))'''