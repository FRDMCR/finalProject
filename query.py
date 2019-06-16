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

class Query :
    '''
    orderMngDb에서 cursor를 이용해 실행할 
    database sqlite3의 단순 쿼리문들을 string으로 반환해주는 클래스
    '''
    def __init__(self):
        pass

    ## 각 테이블 별 PK 가져오기 ##
    def selectCustomersPK(self) :
        return """SELECT CustomerID FROM Customers"""

    def selectProductsPK(self) :
        return """SELECT ProductID FROM Products ORDER BY ProductID ASC"""

    def selectOrdersPK(self) :
        return """SELECT OrderID FROM Orders ORDER BY OrderID ASC"""

    def selectOrderDetailsPK(self) :
        return """SELECT OrderID, ProductID FROM OrderDetails"""

    ## Orders, Products 테이블 마지막 ID 값 선택 ##
    def selectOrdLastPK(self) :
        return """SELECT MAX(OrderID) FROM Orders"""

    def selectProLastPK(self) :
        return """SELECT MAX(ProductID) FROM Products"""

    ## 거래처 현황 조회 쿼리문 ##
    def selectCustomerStat(self) :
        return """SELECT DISTINCT a.CustomerID, a.CompanyName
                FROM Customers a INNER JOIN Orders b ON a.CustomerID = b.CustomerID 
                INNER JOIN OrderDetails c ON b.OrderID = c.OrderID
                INNER JOIN Products d ON c.ProductID = d.ProductID 
                WHERE c.Quantity*c.UnitPrice >= 1000
                AND NOT (d.ProductID / 10) = 0"""

    ## 주문 현황 조회 쿼리문 ##
    def selectOrderStat(self, companyName) :
        return f"""SELECT b.OrderID, b.OrderDate, 
                    d.ProductID, d.ProductName, 
                    c.Quantity, c.UnitPrice, c.Quantity*c.UnitPrice AS TotalPrice
                FROM Customers a INNER JOIN Orders b ON a.CustomerID = b.CustomerID 
                INNER JOIN OrderDetails c ON b.OrderID = c.OrderID
                INNER JOIN Products d ON c.ProductID = d.ProductID
                WHERE a.companyName = '{companyName}'
                AND c.Quantity*c.UnitPrice >= 1000
                AND NOT (d.ProductID / 10) = 0
                ORDER BY b.OrderDate DESC, d.ProductID ASC
                """

    ## 각 테이블 별 추가 쿼리문 ##
    def insertCustomers(self, customerID, companyName) :
        return f"""INSERT INTO Customers (CustomerID, CompanyName)
                VALUES ('{customerID}', '{companyName}')"""

    def insertProducts(self, productID, productName) :
        return f"""INSERT INTO Products (ProductID, ProductName)
                VALUES ({productID}, '{productName}')"""

    def insertOrders(self, orderID, customerID, orderDate) :
        return f"""INSERT INTO Orders (OrderID, CustomerID, OrderDate)
                VALUES ({orderID}, '{customerID}', '{orderDate}')"""

    def insertOrderDetails(self, orderID, productID, unitPrice, quantity) :
        return f"""INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity)
                VALUES ({orderID}, {productID}, {unitPrice}, {quantity})"""

    ## 각 테이블 별 수정 쿼리문 ##
    def updateCustomers(self, customerID, companyName) :
        return f"""UPDATE Customers SET CompanyName = '{companyName}'
                WHERE CustomerID = '{customerID}'"""

    def updateProducts(self, productID, productName) :
        return f"""UPDATE Products SET ProductName = '{productName}'
                WHERE ProductID = {productID}"""
            
    def updateOrders(self, orderID, customerID, orderDate) :
        return f"""UPDATE Orders SET CustomerID = '{customerID}', OrderDate = '{orderDate}'
                WHERE OrderID = {orderID}"""

    def updateOrderDetails(self, orderID, productID, unitPrice, quantity) :
        return f"""UPDATE OrderDetails SET UnitPrice = {unitPrice}, Quantity = {quantity}
                WHERE OrderID = {orderID} AND ProductID = {productID}"""

    ## 각 테이블 별 삭제 쿼리문 ##
    def deletePorducts(self, productID) :
        return f"""DELETE FROM Products
                WHERE ProductID = {productID}"""

    def deleteOrders(self, orderID) :
        return f"""DELETE FROM Orders
                WHERE OrderID = {orderID}"""
    
    def deleteOrderDetails(self, orderID) :
        return f"""DELETE FROM OrderDetails
                WHERE OrderID = {orderID}"""
                