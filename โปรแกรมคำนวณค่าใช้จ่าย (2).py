from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

#สร้างwindow,tab,frame
GUI =Tk()
GUI.geometry('1000x600')
GUI.title('โปรแกรมคำนวณรายรับรายจ่าย')

FONT1 = ('Angsana New',20)   #กำหนดฟอนต์และขนาด
Tab = ttk.Notebook(GUI)
tab1 = Frame(Tab)
money_bag = PhotoImage(file = 'Money_Suitcase.png').subsample(12) #รูปTab1
Tab.add(tab1, text=f'{"เพิ่มรายการ": ^{30}}', image = money_bag, compound = 'top') #ชื่อTab1
Frame01 = Frame(tab1)
Frame01.pack() #เพิ่มFrame01ลงTab1
tab2 = Frame(Tab)
notesheet = PhotoImage(file = 'notesheet.png').subsample(4)#รูปTab2
Tab.add(tab2, text=f'{"รายการทั้งหมด": ^{30}}', image = notesheet, compound = 'top') #ชื่อTab2
Frame02 = Frame(tab2)
Frame02.pack() #เพิ่มFrame02ลงTab2
Tab.pack(fill=BOTH)
wallet_pic = PhotoImage(file='wallet.png').subsample(10)
pic01 = ttk.Label(Frame01, image = wallet_pic)
pic01.pack(pady = 20)

#ฟังก์ชั่นและตัวแปร
dt = datetime.now()     #วันวันที่เดือนปีเวลา
day = dt.strftime('%A')
def Save(event=None):   #ระบบบันทึก
    expense = V_expense.get()
    price = V_price.get()
    quantity = V_quantity.get()
    if expense == '' :
        print('no data กรุณากรอกชื่อรายการ')
        messagebox.showwarning('no data','กรุณากรอกชื่อรายการ')
        return
    elif price == '' :
        print('no data กรุณากรอกราคา')
        messagebox.showwarning('no data','กรุณากรอกราคา')
        return
    elif quantity == '' :
        print('no data กรุณากรอกจำนวน')
        messagebox.showwarning('no data','กรุณากรอกจำนวน')
        return
    try:
            totalprice = int(price) * int(quantity)
            result_text = '{} {} ราการรายจ่าย:{} ราคาต่อหน่วย:{}บาท จำนวน{}หน่วย ราคารวม{}บาท'.format(day,dt,expense,price,quantity,totalprice)
            V_result.set(result_text)
            print(result_text)
            with open('savedata.csv','a',encoding='utf-8',newline='') as f:
                fw = csv.writer(f)
                data = [dt,str(f'รายการรายจ่าย:{expense}'),str(f'ราคาต่อหน่วย:{price}บาท'),str('จำนวน{}หน่วย'.format(quantity)),str(f'ราคารวม{totalprice}บาท)')]
                fw.writerow(data)
            Enter01.focus()
            updatetable()
    except Exception as e:
        print('ERROR',e)
        messagebox.showerror('ERROR','ตัวเลขไม่ถูกต้อง กรุณากรอกข้อมูลใหม่')
    V_expense.set('')
    V_price.set('')
    V_quantity.set('')
GUI.bind('<Return>',Save)   #Enterเพื่อเซฟ

#ช่องกรอกรายการ
Label01 =ttk.Label(Frame01,text='ชื่อรายการค่าใช้จ่าย',font=FONT1).pack()
V_expense = StringVar()
Enter01 = ttk.Entry(Frame01,textvariable = V_expense,font=FONT1)
Enter01.pack()

#ช่องกรอกราคา
Label02 =ttk.Label(Frame01,text='ราคาหน่วยละ(บาท)',font=FONT1).pack()
V_price = StringVar()
Enter02 = ttk.Entry(Frame01,textvariable = V_price,font=FONT1)
Enter02.pack()

#ช่องกรอกจำนวน
Label03 =ttk.Label(Frame01,text='จำนวน(หน่วย)',font=FONT1).pack()

V_quantity = StringVar()
Enter03 = ttk.Entry(Frame01,textvariable = V_quantity,font=FONT1)
Enter03.pack()

#ปุ่มเซฟ
LabelSave =ttk.Label(Frame01,text="บันทึก",font=FONT1).pack()
Button01 = ttk.Button(Frame01,text=f'{"Save": >{20}}',command=Save)
Button01.pack(ipadx=50,ipady=30)
save_icon = PhotoImage(file='save_icon.png').subsample(5)
pic02 = ttk.Label(Button01, image = save_icon)
pic02.place(x = 40,y = 15)

V_result = StringVar()
V_result.set('-----result-----')
result = ttk.Label(Frame01, textvariable=V_result ,font=FONT1,foreground = 'black')
result.pack(pady=20)

#แสดงค่าในหน้ารายการ

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
        '''
        rs = read_csv()
        global rs
        print(data)
        print(data[0])
        print(data[0][0])
        for a,b,c,d,e in data:
            print(a + b + c +d + e)
        '''
    return data

rs = read_csv()
for d in rs:
    print (d)

#ทำตาราง
LabelTable = ttk.Label(tab2,text="ตารางรวมรายการทั้งหมด",font=FONT1).pack()
header =['วัน-เวลา','รายการ','ราคาต่อหน่วย','จำนวน','รวมราคา']
resulttable = ttk.Treeview(tab2,columns=header,show='headings',height=20
                        )
resulttable.pack()

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,240,120,120,120]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

def updatetable():
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

updatetable()

GUI.mainloop()
