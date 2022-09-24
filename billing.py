from cProfile import label
from datetime import date
from tkinter import*
from tkinter.font import BOLD
from tkinter import ttk,messagebox
import sqlite3
import time
import os 
import tempfile
import smtplib
import email_password
from PIL import Image,ImageTk #pip install pillow 

class billclass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1350x700+0+0")
		self.root.title("Inventory Mangment System")
		self.root.config(bg="white")
		self.cart_list=[]
		self.chk_print=0

		#=============title===================================
		self.icon_title=PhotoImage(file="images\logo1.png")
		title=Label(self.root,text="Inventory Mangment System",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
		
		#=============btn_logout===================================
		btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
		#=============clock===================================
		self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangment System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman",15),bg="#4d636d",fg="white")
		self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

		self.date_=time.strftime("%d-%m-%Y")
		
		
        #================product frame 1 =======
		self.var_search=StringVar()
		
		ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
		ProductFrame1.place(x=6,y=110,width=410,height=550)
		
		ptitle=Label(ProductFrame1,text="Product's in Stock",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
		#===============Product Search Frame 2===========
		
		ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
		ProductFrame2.place(x=2,y=42,width=398,height=90)
        
		lbl_search=Label(ProductFrame2,text="Search Product | by name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

		lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
		txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
		btn_search=Button(ProductFrame2,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=284,y=45,width=100,height=25)

		btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=284,y=10,width=100,height=25)


		#===============Product Deatails Frame 3===========

		ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
		ProductFrame3.place(x=2,y=140,width=398,height=375)

		scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
		scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
		
		self.ProductTable=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set)
		scrollx.pack(side=BOTTOM , fill=X)
		scrolly.pack(side=RIGHT , fill=Y)
		scrollx.config(command=self.ProductTable.xview)
		scrolly.config(command=self.ProductTable.yview)

		self.ProductTable.heading("pid",text="P.Id")
		self.ProductTable.heading("name",text="Name")
		self.ProductTable.heading("price",text="Price")
		self.ProductTable.heading("qty",text="Quantity")
		self.ProductTable.heading("status",text="Status")
		self.ProductTable["show"]="headings"

		self.ProductTable.column("pid",width=90)
		self.ProductTable.column("name",width=100)
		self.ProductTable.column("price",width=100)
		self.ProductTable.column("qty",width=100)
		self.ProductTable.column("status",width=100)
		self.ProductTable.pack(fill=BOTH,expand=1)
		self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
		lbl_note=Label(ProductFrame1,text="Note:Enter 0 Quantity to remove product from cart",font=("goudy old style",12),bg="white",fg="red").pack(side=BOTTOM,fill=X)

		#=============Customer frame================
		self.var_cname=StringVar()
		self.var_contact=StringVar()

		CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
		CustomerFrame.place(x=420,y=110,width=530,height=70)

		ctitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

		lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
		txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)
		
		lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
		txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
		
		#=========Cal cart Frame===================

		Cal_cartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
		Cal_cartFrame.place(x=420,y=190,width=530,height=360)

		#=========Calculator Frame===================
		#Cal_Frame=Frame(Cal_cartFrame,bd=2,bg="yellow")
		#Cal_Frame.place(x=5,y=10,width=268,height=340)                #calculator frame
			
		#cal_name=Label(Cal_Frame,text="STAR GROUP",font=("goudy old style",15,"bold"),fg="Black",bg="yellow").place(x=250,y=10) 
		#cal_name2=Label(Cal_Frame,text="*************************** ",font=("goudy old style",22,"bold"),fg="Black",bg="yellow").pack(side=TOP,fill=X)
		#cal_name3=Label(Cal_Frame,text="*************************** ",font=("goudy old style",22,"bold"),fg="Black",bg="yellow").pack(side=BOTTOM,fill=X)

		
		#==========Cart Frame===================
		CartFrame=Frame(Cal_cartFrame,bd=3,relief=RIDGE)
		CartFrame.place(x=5,y=10,width=520,height=342)

		self.carttitle=Label(CartFrame,text="Cart \t Total Product: [0]",font=("goudy old style",15,"bold"),bg="lightblue")
		self.carttitle.pack(side=TOP,fill=X)

		#scrolly=Scrollbar(CartFrame,orient=HORIZONTAL)
		#scrolly=Scrollbar(CartFrame,orient=VERTICAL)
		self.CartTable=ttk.Treeview(CartFrame,columns=("pid","name","price","qty"))#,yscrollcommand=scrolly.set)
		self.CartTable.heading("pid",text="P Id")
		self.CartTable.heading("name",text="Name")
		self.CartTable.heading("price",text="Price")
		self.CartTable.heading("qty",text="Quantity")
		
		self.CartTable["show"]="headings"

		self.CartTable.column("pid",width=40)
		self.CartTable.column("name",width=100)
		self.CartTable.column("price",width=90)
		self.CartTable.column("qty",width=40)
		
		self.CartTable.pack(fill=BOTH,expand=1)
		self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
		
		#=====ADD cart frame=======
		self.var_pid=StringVar()
		self.var_pname=StringVar()
		self.var_price=StringVar()
		self.var_qty=StringVar()
		self.var_stock=StringVar()

		Addcart_widgetFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
		Addcart_widgetFrame.place(x=420,y=550,width=530,height=110)

		lbl_p_name=Label(Addcart_widgetFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
		txt_p_name=Entry(Addcart_widgetFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)
		
		lbl_p_price=Label(Addcart_widgetFrame,text="Price",font=("times new roman",15),bg="white").place(x=230,y=5)
		txt_p_price=Entry(Addcart_widgetFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

		lbl_p_qty=Label(Addcart_widgetFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
		txt_p_qty=Entry(Addcart_widgetFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

		self.lbl_instock=Label(Addcart_widgetFrame,text="In Stock",font=("times new roman",15,"bold"),bg="lightgray",fg="green")
		self.lbl_instock.place(x=5,y=70)

		btn_clear_cart=Button(Addcart_widgetFrame,text="Clear",command=self.clear_cart,font=("times new roman",18,"bold"),bg="lightgrey",cursor="hand2").place(x=280,y=70,width=100,height=30)
		btn_add_cart=Button(Addcart_widgetFrame,text="UPDATE",command=self.add_update_cart, font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=410,y=70,width=100,height=30)
		btn_save=Button(Addcart_widgetFrame,text="Save",command=self.customer, font=("times new roman",15,"bold"),bg="blue",cursor="hand2").place(x=150,y=70,width=100,height=30)
		
		
		#**********************Billing Area *******************************************
		billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='lightblue')
		billFrame.place(x=953,y=110,width=390,height=410)

		Btitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

		scrolly=Scrollbar(billFrame,orient=VERTICAL)
		scrolly.pack(side=RIGHT,fill=Y)

		self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
		self.txt_bill_area.pack(fill=BOTH,expand=1)
		scrolly.config(command=self.txt_bill_area.yview)


	
		billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
		billMenuFrame.place(x=953,y=520,width=410,height=140)

		#**********************Billing Label *******************************************
		self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",15,"bold"),bg="lightblue",fg="black")
		self.lbl_amnt.place(x=2,y=5,width=120,height=70)

		self.lbl_discount=Label(billMenuFrame,text='GST \n[18%]',font=("goudy old style",15,"bold"),bg="lightyellow",fg="black")
		self.lbl_discount.place(x=124,y=5,width=120,height=70)
		
		self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",15,"bold"),bg="lightblue",fg="black")
		self.lbl_net_pay.place(x=246,y=5,width=160,height=70)


		#***#**********************Billing Button *******************************************
		btn_print=Button(billMenuFrame,text='Print',cursor='hand2',command=self.print_bill, font=("goudy old style",15,"bold"),bg="#010c48",fg="white")
		btn_print.place(x=2,y=80,width=120,height=50)

		btn_clear_all=Button(billMenuFrame,text='Clear All',cursor='hand2',command=self.clear_all, font=("goudy old style",15,"bold"),bg="yellow",fg="black")
		btn_clear_all.place(x=124,y=80,width=120,height=50)

		btn_generate=Button(billMenuFrame,text='Generate Bill',cursor='hand2',command=self.generate_bill, font=("goudy old style",15,"bold"),bg="#010c48",fg="white")
		btn_generate.place(x=246,y=80,width=160,height=50)

		
       #$$$$$$$$$$$$$$$$$$$ Footer $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

		footer=Label(self.root, text="Inventory Managment System | Developed By STAR GROUP\nfor any Technical issue contact: 987654321",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM, fill=X)
		self.show()
		#self.bill_top()
		self.update_date_time()
		#=+++++++++++++++++++++++++++++++ ALL Functions ++++++++++++++++++++++++++++++++++++++++++++++++++





		#==================customer details======================================
	def customer(self):
		self.customer_win=Toplevel(self.root)
		self.customer_win.title('Customer details')
		self.customer_win.geometry('1000x350+500+100')
		self.customer_win.focus_force()
		cust_frame=Frame(self.customer_win,bd=3,relief=RIDGE)
		cust_frame.place(x=5,y=10,width=955,height=290)

		btn_mail=Button(self.customer_win,text="Send Mail",command=self.mail_check,font=("times new roman",18,"bold"),bg="orange",cursor="hand2").place(x=800,y=310,width=150,height=30)

		scrolly=Scrollbar(cust_frame,orient=HORIZONTAL)
		scrollx=Scrollbar(cust_frame,orient=VERTICAL)
		self.CustomerTable=ttk.Treeview(cust_frame,columns=("invoice","cname","cemail","billamt","tax","netpay","date"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM , fill=X)
		scrolly.pack(side=RIGHT , fill=Y)
		scrollx.config(command=self.CustomerTable.xview)
		scrolly.config(command=self.CustomerTable.yview)

		self.CustomerTable.heading("invoice",text="Invoice id")
		self.CustomerTable.heading("cname",text="Name")
		self.CustomerTable.heading("cemail",text="Email")
		self.CustomerTable.heading("billamt",text="Bill Amt")
		self.CustomerTable.heading("tax",text="GST")
		self.CustomerTable.heading("netpay",text="Net Pay")
		self.CustomerTable.heading("date",text="Date")
		self.CustomerTable["show"]="headings"

		self.CustomerTable.column("invoice",width=90)
		self.CustomerTable.column("cname",width=100)
		self.CustomerTable.column("cemail",width=100)
		self.CustomerTable.column("billamt",width=100)
		self.CustomerTable.column("tax",width=100)
		self.CustomerTable.column("netpay",width=100)
		self.CustomerTable.column("date",width=100)
		self.CustomerTable.pack(fill=BOTH,expand=1)
		#self.CustomerTable.bind("<ButtonRelease-1>",self.get_custdata)

		self.get_custdata
		self.cust_add()
		self.cust_show() 

		#-----------------------------------Pop Up window----------------------------
	def cust_add(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			if self.invoice == 0: 
				messagebox.showerror("Error","Invoice must be required",parent=self.root)
			else:
				cur.execute("Select * from customer where invoice=?",(self.invoice,))
				row=cur.fetchone()
				if row!=None:
					messagebox.showerror("Error","This Invoice already assigned, try different",parent=self.root)
				else:
					cur.execute("Insert into customer(invoice,cname,cemail,billamt,tax,netpay,date)values(?,?,?,?,?,?,?)",(
												self.invoice,
												self.var_cname.get(),
												self.var_contact.get(),
												self.bill_amnt,
												self.discount,
												self.net_pay,
												self.date_,
					))
					con.commit()
					messagebox.showinfo("Success" ,"customer Addedd Successfully",parent=self.root)
					self.show()

		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		




	def cust_show(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			cur.execute("select * from customer")
			rows=cur.fetchall()
			self.CustomerTable.delete(*self.CustomerTable.get_children())
			for row in rows:
				self.CustomerTable.insert('',END,values=row)
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		

		
	def get_custdata(self,ev):
		f=self.CustomerTable.focus()
		content=(self.CustomerTable.item(f))
		row=content['values']
		print(row)
		self.invoice=row[0] 
		self.var_cname.set(row[1]) 
		self.var_contact.set(row[2])
		self.bill_amnt.set(row[3]) 
		self.discount.set(row[4]) 
		self.net_pay.set(row[5])
		self.date_=row[6] 
	




	
	def show(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			#self.ProductTable=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set)
			cur.execute("select pid , name , price , qty , status from product ")
			rows=cur.fetchall()
			self.ProductTable.delete(*self.ProductTable.get_children())
			for row in rows:
				self.ProductTable.insert('',END,values=row)
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
	

	



		#==============Search =========

										#Time :-9:13 video 11 


		#==========Get data===========
	def get_data(self,ev):
		f=self.ProductTable.focus()
		content=(self.ProductTable.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])
		self.lbl_instock.config(text=f"In Stock[{str(row[3])}]")
		self.var_stock.set(row[3])
		self.var_qty.set('1')

	def get_data_cart(self,ev):
		f=self.CartTable.focus()
		content=(self.CartTable.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])
		self.var_qty.set(row[3])

		self.lbl_instock.config(text=f"In Stock[{str(row[4])}]")
		self.var_stock.set(row[4])


			#==========add update=========
	def add_update_cart(self):
		if self.var_pid.get()=='':
			messagebox.showerror('Error',"Please select product from the list",parent=self.root)

		elif self.var_qty.get()=='':
			messagebox.showerror('Error',"Quantity is Required",parent=self.root)

		elif int(self.var_qty.get())>int(self.var_stock.get()):
			messagebox.showerror('Error',"Invalid Quantity ",parent=self.root)
		else:
			#price_cal=int(self.var_qty.get())*float(self.var_price.get())
			#price_cal=float(price_cal)
			price_cal=self.var_price.get()
			cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
			#print(self.cart_list)

			#==============Update_cart=================
			present='no'
			index_=0
			for row in self.cart_list:
				if self.var_pid.get()==row[0]:
					present='yes'
					break
				index_+=1	
			if present=='yes':
				op=messagebox.askyesno('Confirm',"Product alredy present!\nDo you want to Update|Remove from the Cart List",parent=self.root)
				if op==True:
					if self.var_qty.get=="0":
						self.cart_list.pop(index_)
					else:
						#self.cart_list[index_][2]=price_cal
						self.cart_list[index_][3]=self.var_qty.get()
			else:
				self.cart_list.append(cart_data)	
			
			self.show_cart()
			self.bill_update()

	#=================
	def bill_update(self):
		self.bill_amnt=0
		self.net_pay=0
		self.discount=0
		for row in self.cart_list:
			self.bill_amnt=self.bill_amnt+float(row[2])*int(row[3])
		self.discount=(self.bill_amnt*18/100)
	
		self.net_pay=self.bill_amnt+self.discount
		self.lbl_amnt.config(text=f'Bill Amnt.(Rs.)\n{str(self.bill_amnt)}')
		self.lbl_net_pay.config(text=f'Net Amount(Rs.)\n{str(self.net_pay)}')
		self.carttitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")


	def show_cart(self):
		
		try:
			self.CartTable.delete(*self.CartTable.get_children())
			for row in self.cart_list:
				self.CartTable.insert('',END,values=row)
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


	
	def generate_bill(self):
		if self.var_cname.get()=='' or self.var_contact.get()=='':
			messagebox.showerror("Error",f"Customer Details are required",parent=self.root)

		elif len(self.cart_list)==0:
			messagebox.showerror("Error",f"Please Add Product to the Cart!!!",parent=self.root)
		else:
			#========Bill Top =====
			self.bill_top()
			#========Bill Middle =====
			self.bill_middle()
			#========Bill Bottom =====
			self.bill_bottom()

			fp=open(f'bill/{str(self.invoice)}.txt','w')
			fp.write(self.txt_bill_area.get('1.0',END))
			fp.close()
			messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
			self.chk_print=1

	#--------------------Bill Top -------------------
	def bill_top(self):
		self.invoice=int(time.strftime('%H%M%S'))+int(time.strftime("%d%m%Y"))
		bill_top_temp=f''''
\t\t Apple-Inventory
\t Phone NO. 987654321 , Delhi-125001
{str("="*45)}
Customer Name: {self.var_cname.get()}
Ph No. : {self.var_contact.get()}
Bill No.:{str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
Product Name\t\t\tQTY\tPrice
{str("="*45)}
		'''
		self.txt_bill_area.delete('1.0',END)
		self.txt_bill_area.insert('1.0',bill_top_temp)



	#--------------------Bill Bottom -------------------
	def bill_bottom(self):
		bill_bottom_temp=f''''
{str("="*45)}
Bill Amount \t\t\t\tRs.{self.bill_amnt}
GST\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str(""*47)}\n
		'''
		self.txt_bill_area.insert(END,bill_bottom_temp)


	#--------------------Bill Bottom -------------------
	def bill_middle(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			for row in self.cart_list:
				pid=row[0]
				name=row[1]
				qty=int(row[4])-int(row[3])
				if int(row[3])==int(row[4]):
					status='Inactive'
				if int(row[3])!=int(row[4]):
					status='Active'

				price=float(row[2])*int(row[3])
				price=str(price)
				self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
				
				# ------------Update qty in product table------------
				cur.execute('Update product set qty=?,status=? where pid=?',(
					qty,
					status,
					pid
				
				))
				con.commit()
			con.close()
			self.show()
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

	def clear_cart(self):
		self.var_pid.set('')
		self.var_pname.set('')
		self.var_price.set('')
		self.var_qty.set('')

		self.lbl_instock.config(text=f"In Stock")
		self.var_stock.set('')


	def clear_all(self):
		del self.cart_list[:]
		self.var_cname.set('')
		self.var_contact.set('')
		self.txt_bill_area.delete('1.0',END)
		self.carttitle.config(text=f"Cart \t Total Product: [0]")
		self.clear_cart()
		self.show()
		self.show_cart()
		self.chk_print=0

	def update_date_time(self):
		time_=time.strftime("%I:%M:%S")
		date_=time.strftime("%d-%m-%Y")
		self.lbl_clock.config(text=f"Welcome to Inventory Mangment System\t\t Date:{str(date_)}\t\t Time:{str(time_)}", font=("times new roman",15),bg="#4d636d",fg="white")
		self.lbl_clock.after(200,self.update_date_time)

	def print_bill(self):
		if self.chk_print==1:
			messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
			new_file=tempfile.mktemp('.txt')
			open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
			os.startfile(new_file,'print')

		else:
			messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)

	def logout(self):
		self.root.destroy()
		os.system("python login.py")

	###################===send mail=========================

	def mail_check(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			if self.var_contact.get()=="":
				messagebox.showerror("Error","Mail ID mustbe Required",parent=self.root)
			else:
				cur.execute("select cemail from customer where invoice=?",(self.invoice,))
				email=cur.fetchone()
				if email==None:
					messagebox.showerror("Error","Invalid mail ID",parent=self.root)
				else:
					chk=self.sentemail(email[0])
					if chk =='f':
						messagebox.showerror("Error","Connection Error,try again",parent=self.root)
					else:
						messagebox.showinfo("Success" ,"Mail sent Successfully",parent=self.root)
					
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		
       





	def sentemail(self,to_):
		s=smtplib.SMTP('smtp.gmail.com',587)
		s.starttls()
		email_=email_password.email_
		pass_=email_password.pass_
																																			
		s.login(email_,pass_)
		subj='Invoice Details'
		msg=f'''Dear Customer,
		\nOrder placed successfully.
		Bill No.:{str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
		\nYour Bill Amount Rs.{self.bill_amnt}
		\nYou Have Paid Rs.{self.net_pay} with (18%)GST.
		\nYour Invoice Number is {self.invoice}.
		\nThank You,Visit Again.
		\nWith Regards,\nSTAR Group'
		
		'''
		msg="Subject:{}\n\n{}".format(subj,msg)
		s.sendmail(email_,to_,msg)
		chk=s.ehlo()
		if chk[0]==250:
			return 's'
		else:
			return 'f'


	
	


	   


        

		


	    


			
if __name__=="__main__":
        root=Tk()
        obj=billclass(root)
        root.mainloop()
