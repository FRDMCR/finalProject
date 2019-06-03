'''

'''
class Query() :

    def __init__(self):
        pass

    def selectCustomer(self) :
        return """SELECT DISTINCT a.CustomerID, a.CompanyName
                FROM Customers a INNER JOIN Orders b ON a.CustomerID = b.CustomerID 
                INNER JOIN OrderDetails c ON b.OrderID = c.OrderID
                INNER JOIN Products d ON c.ProductID = d.ProductID 
                WHERE c.Quantity*c.UnitPrice >= 1000
                AND NOT (d.ProductID / 10) = 0"""

    def selectOrder(self, customerID) :
        return f"""SELECT b.OrderID, b.OrderDate, 
                    d.ProductID, d.ProductName, 
                    c.Quantity, c.UnitPrice, c.Quantity*c.UnitPrice AS TotalPrice
                FROM Customers a INNER JOIN Orders b ON a.CustomerID = b.CustomerID 
                INNER JOIN OrderDetails c ON b.OrderID = c.OrderID
                INNER JOIN Products d ON c.ProductID = d.ProductID
                WHERE a.CustomerID = {customerID}
                AND c.Quantity*c.UnitPrice >= 1000
                AND NOT (d.ProductID / 10) = 0
                ORDER BY b.OrderDate DESC, d.ProductID ASC
                """

    def insertCustomers(self, customerID, companyName) :
        return f"""INSERT INTO Customers (CustomerID, CompanyName)
                VALUES ({customerID}, {companyName})"""

    def insertProducts(self, productID, productName) :
        return f"""INSERT INTO Products (ProductID, ProductName)
                VALUES ({productID}, {productName})"""

    def insertOrders(self, orderID, customerID, orderDate) :
        return f"""INSERT INTO Orders (OrderID, CustomerID, OrderDate)
                VALUES ({orderID}, {customerID}, {orderDate})"""

    def insertOrderDetails(self, orderID, productID, unitPrice, quantity) :
        return f"""INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity)
                VALUES ({orderID}, {productID}, {unitPrice}, {quantity})"""

    def updateCustomers(self, customerID, companyName) :
        return f"""UPDATE Customers SET CompanyName = {companyName}
                WHERE CustomerID = {customerID}"""

    def updateProducts(self, productID, productName) :
        return f"""UPDATE Products SET ProductName = {productName}
                WHERE ProductID = {productID}"""
            
    def updateOrders(self, orderID, customerID, orderDate) :
        return f"""UPDATE Orders SET CustomerID = {customerID}, OrderDate = {orderDate}
                WHERE OrderID = {orderID}"""

    def updateOrderDetails(self, orderID, productID, unitPrice, quantity) :
        return f"""UPDATE Orders SET ProductID = {productID}, UnitPrice = {unitPrice}, Quantity = {quantity}
                WHERE OrderID = {orderID}"""

    def deletePorducts(self, productID) :
        return f"""DELETE FROM Products
                WHERE ProductID = {productID}"""

    def deleteOrders(self, orderID) :
        return f"""DELETE FROM Orders
                WHERE OrderID = {orderID}"""
    
    def deleteOrderDetails(self, productID, orderID) :
        return f"""DELETE FROM OrderDetails
                WHERE ProductID = {productID}, OrderID = {orderID}"""