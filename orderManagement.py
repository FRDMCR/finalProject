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
2019-06-12
'''

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from orderMngDb import *

func = Function()

def funcAbout() :
    messagebox.showinfo("About", 
    """
    개발자 : 정성진
    학과 : 컴퓨터공학과
    학번 : 2014040013
    메일주소 : tjdwls01007@naver.com
    마지막 수정 날짜 : 2019-06-12""")

def funcExit() :
    window.quit()
    window.destroy()

if __name__ == "__main__":

    window = Tk()

    window.title("Order Management Program")
    window.geometry("750x400")
    window.resizable(width = FALSE, height = FALSE)

    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    #-------------파일 메뉴----------------#
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu = fileMenu)
    fileMenu.add_command(label = "조회")
    fileMenu.add_separator()
    fileMenu.add_command(label = "추가")
    fileMenu.add_separator()
    fileMenu.add_command(label = "수정")
    fileMenu.add_separator()
    fileMenu.add_command(label = "삭제")
    fileMenu.add_separator()
    fileMenu.add_command(label = "종료", command = funcExit)
    fileMenu.add_separator()

    #--------------About------------------#
    aboutMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "About", menu = aboutMenu)
    aboutMenu.add_cascade(label = "프로그램 정보", command = funcAbout)
    
    #------------거래처 현황---------------#
    labelCustomer = Label(window, text = "거래처 현황", width = 80, fg = "white", bg = "black")
    labelCustomer.pack(side = TOP, anchor = W)

    comboboxCustomer = ttk.Combobox(window, width = 78, textvariable = StringVar())
    comboboxCustomer['values'] = func.readCustomerStat('name')
    comboboxCustomer.pack(side = TOP, anchor = W)
    comboboxCustomer.config(state='readonly')
    
    frameCViews = Frame(window)
    frameCViews.pack(side = TOP, anchor = W)
    views = len(comboboxCustomer['values'])         # 조회건수
    labelCViews = Label(frameCViews, text = "조회건수", width = 20, bg = "white", relief=SOLID, borderwidth = 1)
    labelCViews.pack(side = LEFT)
    labelCVData = Label(frameCViews, text = views, width = 20, bg = "white", relief=SOLID, borderwidth = 1)
    labelCVData.pack(side = LEFT)

    #---------------주문 현황---------------#
    #참조 : https://076923.github.io/posts/Python-tkinter-30/
    labelOrder = Label(window, text = "주문 현황", width = 80, fg = "white", bg = "black")
    labelOrder.pack(side = TOP, anchor = W)

    frameTree = Frame(window)
    frameTree.pack(side = TOP, anchor = W)
    treeOrder = ttk.Treeview(frameTree)
    treeYscrollbar = Scrollbar(frameTree, orient="vertical", command=treeOrder.yview)
    treeOrder.configure(yscroll=treeYscrollbar.set)
    treeOrder["columns"] = ("OrderID", "OrderDate", "ProductID", "ProductName", "Quantity", "UnitPrice", "TotalPrice")
    treeOrder.heading('#0', text="", anchor=W)
    treeOrder.heading('#1', text="주문번호", anchor=W)
    treeOrder.heading('#2', text="주문일자", anchor=W)
    treeOrder.heading('#3', text="품목코드", anchor=W)
    treeOrder.heading('#4', text="품목명", anchor=W)
    treeOrder.heading('#5', text="수량", anchor=W)
    treeOrder.heading('#6', text="단가", anchor=W)
    treeOrder.heading('#7', text="금액", anchor=W)
    treeOrder.column("#0", width=0, stretch=0, minwidth=0)
    treeOrder.column("#1", width=80)
    treeOrder.column("#2", width=80)
    treeOrder.column("#3", width=80)
    treeOrder.column("#4", width=80)
    treeOrder.column("#5", width=80)
    treeOrder.column("#6", width=80)
    treeOrder.column("#7", width=80)

    
    orderStatList = func.readOrderStat()
    for i in range(len(treelist)):
    
        treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i)+"번")
    treeYscrollbar.pack(side=RIGHT, fill=Y)
    treeOrder.pack(fill=X, side = LEFT)

    window.mainloop() 