orderID = '1'
productID = '2'
unitPrice = '3'
quantity = '4'
productName = '123'
print("INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity) VALUES ("+ orderID +","+ productID +","+ unitPrice +","+ quantity+")")
print("SELECT ProductID FROM Products WHERE ProductName =" + "'" + productName + "'")

'''
ile "c:\python\final.py", line 99, in insertData
    cur.execute("INSERT INTO Customers (CustomerID, CompanyName) VALUES ('"+ customerID +"','"+ companyName +"')")
sqlite3.OperationalError: database is locked
'''