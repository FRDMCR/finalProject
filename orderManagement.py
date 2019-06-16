'''
//작성자--------------------------//
충북대학교 컴퓨터공학과
2014040013 정성진
tjdwls01007@naver.com
//프로그램 명---------------------//
order management program
//프로그램 구성-------------------//
query.py
orderMngDb.py
orderManagement.py
//마지막 수정 날짜----------------//
2019-06-16
'''

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from orderMngDb import *
from datetime import datetime

func = Function()       # 조회, 추가, 수정, 삭제를 담은 모듈

## 프로그램 종료 함수 ##
def funcExit() :
    window.quit()
    window.destroy()

## 추가 입력 창 생성 콜백 ##
def createInsertWin(*args):
    InsertWin(window)
 
## 추가 입력 창 생성 콜백 ##
def createUpdateWin(*args):
    UpdateWin(window)

## 삭제 기능 콜백 ##
def funcDelete(*args):
    response = messagebox.askquestion("삭제 확인", "정말로 삭제하시겠습니까?")
    if response == 'yes' : # '예'를 누르면 삭제
        func.delete(orderStat.orderID)
        printOrderStat() # 주문 현황과 조회 수 바로 업데이트
    else :
        return

## 거래처 현황 업데이트 ##
def updateCustomerStat() :
    customerStat.comboboxCustomer['values'] = func.readCustomerStat('name')

## 거래처 선택 시 해당 주문 현황 출력, 조회 수 업데이트 콜백 ##
def printOrderStat(*args) :
    orderStat.treeOrder.delete(*orderStat.treeOrder.get_children())
    orderStatList = func.readOrderStat(customerStat.getSelected())
    for i in range(len(orderStatList)): 
        # idd = 해당 열 id 값 = PK(orderID, productID)
        orderStat.treeOrder.insert('', 'end', text=orderStatList[i][0], values=orderStatList[i], iid=(orderStatList[i][0],orderStatList[i][2]))
    orderViews.labelVData.configure(text = len(func.readOrderStat(customerStat.getSelected()))) # 주문 현황 조회 수 업데이트

class FileMenu :
    """
       파일 메뉴 위젯
       조회, 추가, 수정, 삭제, 종료 기능
    """
    def __init__(self, mainMenu) :
        self.fileMenu = Menu(mainMenu)
        mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "추가", command = createInsertWin)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "수정", command = createUpdateWin)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "삭제", command = funcDelete)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "종료", command = funcExit)
        self.fileMenu.add_separator()

class AboutMenu :
    """
        About 메뉴 위젯
        프로그램 정보
    """
    def __init__(self, mainMenu):
        self.aboutMenu = Menu(mainMenu)
        mainMenu.add_cascade(label = "About", menu =    self.aboutMenu)
        self.aboutMenu.add_cascade(label = "프로그램 정보", command = self.funcAbout)

    ## about 메뉴 함수 ##
    def funcAbout(self) :
        messagebox.showinfo("About", 
        """
        개발자 : 정성진
        학과 : 컴퓨터공학과
        학번 : 2014040013
        메일주소 : tjdwls01007@naver.com
        마지막 수정 날짜 : 2019-06-16""")

    
class CustomerStat :
    """
        거래처 현황 위젯
    """
    def __init__(self, window):
        self.labelCustomer = Label(window, text = "거래처 현황", width = 89, fg = "white", bg = "black")
        self.labelCustomer.pack(side = TOP, anchor = W)

        self.comboboxCustomer = ttk.Combobox(window, width = 87, textvariable = StringVar())
        self.comboboxCustomer['values'] = func.readCustomerStat('name')
        self.comboboxCustomer.pack(side = TOP, anchor = W)
        self.comboboxCustomer.config(state='readonly')
        self.comboboxCustomer.current(0)
        self.comboboxCustomer.bind("<<ComboboxSelected>>",printOrderStat) # printOrderStat call back
        
    ## 선택한 CompanyName 반환 ##
    def getSelected(self):
        return self.comboboxCustomer.get()

class Views :
    """
        조회 건수 위젯
    """
    def __init__(self, window, entry):
        self.frameViews = Frame(window)
        self.frameViews.pack(side = TOP, anchor = W)
        self.views = len(entry)
        self.labelViews = Label(self.frameViews, text = "조회건수", width = 30, bg = "white", relief=SOLID, borderwidth = 1)
        self.labelViews.pack(side = LEFT)
        self.labelVData = Label(self.frameViews, text = self.views, width = 59, bg = "white", relief=SOLID, borderwidth = 1)
        self.labelVData.pack(side = LEFT)

class CurrentTime :
    """
        현재 일시 위젯
    """
    def __init__(self, window):
        self.frameTime = Frame(window)
        self.frameTime.pack(side = TOP, anchor = W)
        self.now = datetime.now()
        self.labelTime = Label(self.frameTime, text = "현재 일시", width = 30, bg = "white", relief=SOLID, borderwidth = 1)
        self.labelTime.pack(side = LEFT)
        self.labelTData = Label(self.frameTime, text = "%04d-%02d-%02d %02d:%02d:%02d" % 
            (self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second), width = 59, bg = "white", relief=SOLID, borderwidth = 1)
        self.labelTData.pack(side = LEFT)

        self.updateTime()
        
    ## 현재 일시 실시간 업데이트 ##
    def updateTime(self):
        self.now = datetime.now()
        self.labelTData.configure(text = "%04d-%02d-%02d %02d:%02d:%02d" % 
            (self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second))
        self.labelTData.after(1000, self.updateTime)

class OrderStat :
    """
        주문 현황 위젯
    """
    def __init__(self, window):
        self.labelOrder = Label(window, text = "주문 현황", width = 89, fg = "white", bg = "black")
        self.labelOrder.pack(side = TOP, anchor = W)
        
        self.frameTree = Frame(window)
        self.frameTree.pack(side = TOP, anchor = W)
        self.treeOrder = ttk.Treeview(self.frameTree)
        self.treeYscrollbar = Scrollbar(self.frameTree, orient="vertical", command=self.treeOrder.yview)
        self.treeOrder.configure(yscroll=self.treeYscrollbar.set)
        self.treeOrder["columns"] = ("OrderID", "OrderDate", "ProductID", "ProductName", "Quantity", "UnitPrice", "TotalPrice")
        self.treeOrder.heading('#0', text="", anchor=W)
        self.treeOrder.heading('#1', text="주문번호", anchor=W)
        self.treeOrder.heading('#2', text="주문일자", anchor=W)
        self.treeOrder.heading('#3', text="품목코드", anchor=W)
        self.treeOrder.heading('#4', text="품목명", anchor=W)
        self.treeOrder.heading('#5', text="수량", anchor=W)
        self.treeOrder.heading('#6', text="단가", anchor=W)
        self.treeOrder.heading('#7', text="금액", anchor=W)
        self.treeOrder.column("#0", width=0, stretch=0, minwidth=0)
        self.treeOrder.column("#1", width=80)
        self.treeOrder.column("#2", width=75)
        self.treeOrder.column("#3", width=70)
        self.treeOrder.column("#4", width=150)
        self.treeOrder.column("#5", width=80)
        self.treeOrder.column("#6", width=80)
        self.treeOrder.column("#7", width=80)
        
        self.orderStatList = func.readOrderStat(customerStat.getSelected())      # 초기 값
        for i in range(len(self.orderStatList)):
        
            # idd = 해당 열 id 값 = PK(orderID, productID)
            self.treeOrder.insert('', 'end', text=self.orderStatList[i][0], values=self.orderStatList[i], iid=(self.orderStatList[i][0], self.orderStatList[i][2]))

        self.treeYscrollbar.pack(side=RIGHT, fill=Y)
        self.treeOrder.pack(fill=X, side = LEFT)
   
        self.treeOrder.bind("<<TreeviewSelect>>", self.selected) # 표의 열 선택 이벤트

    ## 표에서 선택한 열의 orderID와 productID 저장 ##
    def selected(self, *args):
        self.orderID = list(self.treeOrder.selection()[0].split())[0]
        self.productID = list(self.treeOrder.selection()[0].split())[1]
        

class FuncButton:
    """
        기능 버튼
    """
    def __init__(self, window, text):
        self.text = text
        self.button = Button(window, text = self.text, overrelief="solid", width=10, height = 10, bg = 'Yellow')
        self.button.pack(side = LEFT, padx = 40)

    def setExit(self):
        self.button.configure(command = funcExit)

    def setDelete(self):
        self.button.configure(command = funcDelete)

    def setInsertWin(self, window):
        self.button.configure(command = createInsertWin)

    def setUpdateWin(self, window):
        self.button.configure(command = createUpdateWin)

class InsertWin :
    """
        입력 창 위젯
    """
    def __init__(self, window):
        self.insertWin = Toplevel(window)
        self.insertWin.title("Insert Data")
        self.insertWin.geometry("850x120")
        self.insertWin.resizable(width = FALSE, height = FALSE)

        Label(self.insertWin, text = "customerID", width=10, relief = SOLID, fg = 'red').grid(column = 0)
        Label(self.insertWin, text = "companyName", width=20, relief = SOLID, fg = 'red').grid(row = 0, column = 1)
        Label(self.insertWin, text = "orderID", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 2)
        Label(self.insertWin, text = "orderDate", width=20, relief = SOLID, fg = 'red').grid(row = 0, column = 3)
        Label(self.insertWin, text = "productID", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 4)
        Label(self.insertWin, text = "productName",  width=25, relief = SOLID, fg = 'red').grid(row = 0, column = 5)
        Label(self.insertWin, text = "quantity", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 6)
        Label(self.insertWin, text = "unitPrice", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 7)

        self.eCustomerID = Entry(self.insertWin, width=10)
        self.eCompanyName = Entry(self.insertWin, width=20)      
        self.eOrderID = Entry(self.insertWin, width=10)
        self.eOrderDate = Entry(self.insertWin, width=20)
        self.eProductID = Entry(self.insertWin, width=10)
        self.eProductName = Entry(self.insertWin,  width=25)
        self.eQuantity = Entry(self.insertWin, width=10)
        self.eUnitPrice = Entry(self.insertWin, width=10)

        self.eCustomerID.grid(row = 1, column = 0)
        self.eCompanyName.grid(row = 1, column = 1)
        self.eOrderID.grid(row = 1, column = 2)
        self.eOrderDate.grid(row = 1, column = 3)
        self.eProductID.grid(row = 1, column = 4)
        self.eProductName.grid(row = 1, column = 5)
        self.eQuantity.grid(row = 1, column = 6)
        self.eUnitPrice.grid(row = 1, column = 7)

        Label(self.insertWin).grid(row = 2)
        button = Button(self.insertWin, text = 'Insert', width = 4, height = 1)
        button.grid(row = 4, column = 7, pady = 5, padx = 3)
        button.bind("<Button-1>", self.clickInsert)

        ## Insert 버튼 클릭 시 추가 이벤트 ##
    def clickInsert(self, *args):
        self.customerID = self.eCustomerID.get()
        self.companyName =  self.eCompanyName.get()
        self.orderID = self.eOrderID.get()
        self.orderDate = self.eOrderDate.get()
        self.productID = self.eProductID.get()
        self.productName = self.eProductName.get()
        self.quantity = self.eQuantity.get()
        self.unitPrice =  self.eUnitPrice.get()

        try :
            result = func.insert(self.customerID, int(self.orderID), int(self.productID), self.companyName, self.orderDate, self.productName, int(self.unitPrice), int(self.quantity))
            if result == "clear" :
                self.response = messagebox.askquestion("추가 요청", "정말로 추가하시겠습니까?")
                if self.response == 'yes' : # '예'를 누르면 추가하고 창 종료
                    self.insertWin.destroy()
                    updateCustomerStat()
                    printOrderStat()
            elif result == "duplication" :
                messagebox.showinfo("중복", "추가를 실패했습니다.\n모두 이미 존재하는 ID입니다.")
            elif result == "impossible" :
                messagebox.showinfo("추가 불가", "추가를 실패했습니다.\n추가할 수 없는 유형입니다.")
        except ValueError :
            messagebox.showinfo("추가 실패", "추가를 실패했습니다.\n입력 값을 확인하세요.")

class UpdateWin :
    """
        수정 창 위젯
    """
    def __init__(self, window):
        self.updateWin = Toplevel(window)
        self.updateWin.title("Update Data")
        self.updateWin.geometry("900x120")
        self.updateWin.resizable(width = FALSE, height = FALSE)

        Label(self.updateWin, text = "customerID", width=10, relief = SOLID, fg = 'red').grid(column = 0)
        Label(self.updateWin, text = "companyName", width=20, relief = SOLID, fg = 'red').grid(row = 0, column = 1)
        Label(self.updateWin, text = "orderID", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 2)
        Label(self.updateWin, text = "orderDate", width=20, relief = SOLID, fg = 'red').grid(row = 0, column = 3)
        Label(self.updateWin, text = "productID", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 4)
        Label(self.updateWin, text = "productName",  width=25, relief = SOLID, fg = 'red').grid(row = 0, column = 5)
        Label(self.updateWin, text = "quantity", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 6)
        Label(self.updateWin, text = "unitPrice", width=10, relief = SOLID, fg = 'red').grid(row = 0, column = 7)
      
        self.eCompanyName = Entry(self.updateWin, width=20)
        self.eOrderDate = Entry(self.updateWin, width=20)
        self.eProductName = Entry(self.updateWin,  width=25)
        self.eQuantity = Entry(self.updateWin, width=10)
        self.eUnitPrice = Entry(self.updateWin, width=10)

        self.eCompanyName.grid(row = 1, column = 1)
        self.eOrderDate.grid(row = 1, column = 3)
        self.eProductName.grid(row = 1, column = 5)
        self.eQuantity.grid(row = 1, column = 6)
        self.eUnitPrice.grid(row = 1, column = 7)

        self.cCustomerID = ttk.Combobox(self.updateWin, width=10, textvariable = StringVar(), state='readonly')
        self.cCustomerID['values'] = func.getIDList('Customers')
        self.cCustomerID.grid(row = 1, column = 0)
        self.cOrderID = ttk.Combobox(self.updateWin, width=10, textvariable = StringVar(), state='readonly')
        self.cOrderID['values'] = func.getIDList('Orders')
        self.cOrderID.grid(row = 1, column = 2)
        self.cProductID = ttk.Combobox(self.updateWin, width=10, textvariable = StringVar(), state='readonly')
        self.cProductID['values'] = func.getIDList('Products')
        self.cProductID.grid(row = 1, column = 4)

        Label(self.updateWin).grid(row = 2)
        button = Button(self.updateWin, text = 'Update', width = 5, height = 1)
        button.grid(row = 4, column = 7, pady = 5, padx = 3)
        button.bind("<Button-1>", self.clickUpdate)


    ## Update 버튼 클릭 시 수정 이벤트 ##
    def clickUpdate(self, *args):
        self.customerID = self.cCustomerID.get()
        self.companyName =  self.eCompanyName.get()
        self.orderID = self.cOrderID.get()
        self.orderDate = self.eOrderDate.get()
        self.productID = self.cProductID.get()
        self.productName = self.eProductName.get()
        self.quantity = self.eQuantity.get()
        self.unitPrice =  self.eUnitPrice.get()

        try :
            func.update(self.customerID, self.companyName, self.orderID, self.orderDate, self.productID, self.productName, int(self.quantity), int(self.unitPrice))
            self.response = messagebox.askquestion("수정 요청", "정말로 수정하시겠습니까?")
           
        except ValueError :
            messagebox.showinfo("수정 실패", "수정을 실패했습니다.\n입력 값을 확인하세요.")

        if self.response == 'yes' : # '예'를 누르면 수정하고 창 종료
            self.updateWin.destroy()
            updateCustomerStat()
            printOrderStat()

## main 함수 ##
if __name__ == "__main__":

    window = Tk()

    window.title("Order Management Program")
    window.geometry("630x400")
    window.resizable(width = FALSE, height = FALSE)

    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    FileMenu(mainMenu)  # 파일메뉴 위젯 생성
    AboutMenu(mainMenu) # About 메뉴 위젯 생성

    customerStat = CustomerStat(window) # 거래처 현황 위젯 생성
    customerViews = Views(window, func.readCustomerStat('name')) # 거래처 조회건수 위젯 생성

    orderStat = OrderStat(window) # 주문 현황 위젯 생성
    orderViews = Views(window, func.readOrderStat(customerStat.getSelected())) # 주문 조회건수 위젯 생성
    CurrentTime(window) # 현재일시 위젯 생성

    insertButton = FuncButton(window, "추가") # 추가 버튼 위젯 생성
    insertButton.setInsertWin(window) # 추가 입력 창 위젯 생성

    updateButton = FuncButton(window, "수정") # 수정 버튼 위젯 생성
    updateButton.setUpdateWin(window) # 수정 창 위젯 생성

    deleteButton = FuncButton(window, "삭제") # 삭제 버튼 위젯 생성
    deleteButton.setDelete() # 삭제 기능 이벤트 설정

    exitButton = FuncButton(window, "종료") # 종료 버튼 위젯 생성
    exitButton.setExit() # 종료 기능 이벤트 설정

    window.mainloop()                                  