import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image

a = Tk()
a.geometry("700x550")
class store:
    def __init__(self):
        self.obj = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'fellowes', database = 'store')
        
        img = ImageTk.PhotoImage(Image.open("bg_store.jpg"))
        imglabel = Label(a, image=img, width = 700, height =600)
        imglabel.image = img
        imglabel.place(x=0, y = 0)

        title1 = Label(a, text = 'LifeStyle Store', font = ('Times',20,'bold')).place(x = 250, y = 25)

        b1 = Button(a, text  = 'Veiw Item', font = ('',14,'bold'), command = self.veiw_item)
        b2 = Button(a, text  = 'Purchase Item', font = ('',14,'bold'), command = self.Purchase_Item)
        b1.place(x = 150, y = 222)
        b2.place(x = 400, y = 222)

    def veiw_item(self):
        cur = self.obj.cursor()
        Window = Tk()
        Window.geometry("600x200")
        l1 = Label(Window, text = 'item_name', width = 20, borderwidth = 2, relief = 'ridge').grid(row = 0, column = 0)
        l1 = Label(Window, text = 'item_des', width = 20, borderwidth = 2, relief = 'ridge').grid(row = 0, column = 1)
        l1 = Label(Window, text = 'Qty', width = 20, borderwidth = 2, relief = 'ridge').grid(row = 0, column = 2)
        l1 = Label(Window, text = 'price', width = 20, borderwidth = 2, relief = 'ridge').grid(row = 0, column = 3)

        sql1 = 'select * from stock_table'
        count = 1

        try:
            cur.execute(sql1)
            for v1 in cur:
                for v2 in range(len(v1)):
                    b = Label(Window, text = v1[v2], width = 20, borderwidth = 2, relief = 'ridge')
                    b.grid( row = count, column = v2)
                count = count + 1
        except:
            messagebox.showinfo('veiw item', 'Table not printed')

    def Purchase_Item(self):
        global Window1, c_id
        Window1 = Tk()
        Window1.geometry("600x500")
        title1 = Label(Window1, text = 'Purchase Item', font = ('Times',20,'bold')).place(x = 200, y = 20)
        title1 = Label(Window1, text = 'Enter Customer ID :-', font = ('',15,'')).place(x = 25, y = 130)
        global cust_id
        cust_id = Entry(Window1)
        cust_id.place(x = 240, y = 135)
        b1 = Button(Window1, text = 'Purchase', font = ('Times',12,'bold'), command = self.purchasin)
        b1. place(x = 230, y = 200)
        

    def purchasin(self):
        global d, d2, a1
        d = simpledialog.askstring("Purchasing", "Enter the Item name u want to buy",
                                parent=Window1)
        d1 = simpledialog.askstring("Purchasing", "Enter Quantity of item",
                                parent=Window1)
        a = self.qty("'"+d+"'")
        a1 = int(a)
        d2 = int(d1)
        if a1 >= 100:
            self.reducing_quantity()

    def reducing_quantity(self):
        order_no = 0
        cur = self.obj.cursor()
        sql1 = "Update stock_table set Qty = %s where item_name = %s"
        x = a1 - d2
        print(x)
        rec = (x, d)
        
        try:
            cur.execute(sql1,rec)
            messagebox.showinfo('Purchased','Item Purchased Succesfully')
            order_no = order_no + 1
            self.order()
        except mysql.connector.Error as err:
            messagebox.showinfo("Purchased","Your purchase can not be done")
        cur.close()
        
    def qty(self, xyz):
        print(xyz)
        cur = self.obj.cursor()
        sql1 = "SELECT Qty FROM stock_table WHERE item_name = %s" % (xyz)
    
        try:
            cur.execute(sql1)
            record = cur.fetchone()
            r1 = (record[0])
            return r1
        except mysql.connector.Error as err:
            messagebox.showinfo("Quantity","Your Quantity can not be shown becouse Error {}".format(err))
        cur.close()

    def order(self):
        cur = self.obj.cursor()
        c_id = cust_id.get()
        sql1 = "Insert into order_table values (%s,%s,%s,%s)"
        rec = (order_no,d,d2,c_id)
        try:
            cur.execute(sql1,rec)
            self.obj.commit()
            messagebox.showinfo('Order','Item Order Saved')
        except mysql.connector.Error as err:
            messagebox.showinfo("Order",'Item not ordered')
        cur.close()
        self.close()

    def close(self):
        Window1.destroy()
                     
s = store()
