
from itertools import product
from textwrap import fill
from tkinter import*
from tkinter.font import BOLD 
from PIL import Image,ImageTk 
import os 
import sqlite3
import time
from tkinter import messagebox
from employee import employeeClass
from product import productClass
from supplier import supplierClass
from category import categoryclass
from product import productClass
from sales import salesClass
class IMS:
	def __init__(self,root): #Default Constructor for this class
		self.root=root
		self.root.geometry("1350x700+0+0")		#(width x ht+x+y)
		self.root.title("Inventory Mangment System")
		self.root.config(bg="white") #


		#=============title===================================
		self.icon_title=PhotoImage(file="images\logo1.png")
		title=Label(self.root,text="Smart Mart",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
		

		#=============btn_logout===================================
		btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
		#=============clock===================================
		self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangment System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman",15),bg="#4d636d",fg="white")
		self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
		
		#=============Left Menu ==================================
		self.MenuLogo=Image.open("images/menu_im.png")
		self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
		self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

		LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
		LeftMenu.place(x=0,y=102,width=200,height=565)
		
		lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
		lbl_menuLogo.pack(side=TOP,fill=X)

		self.icon_side=PhotoImage(file="images/side.png") # side image >>

		lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X) #left side menu 

		btn_employee=Button(LeftMenu,text="Employee",command=self.employee, image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
		btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier, image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
		btn_category=Button(LeftMenu,text="Category",command=self.category, image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
		btn_product=Button(LeftMenu,text="Product",command=self.product, image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
		btn_sales=Button(LeftMenu,text="Sales",command=self.sales, image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
		btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w", font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)


        #==============Content================================
		self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE, bg="#33bbf9",fg="black",font=("goudy old style",24,"bold"))
		self.lbl_employee.place(x=300,y=120,height=150,width=300)

		self.lbl_supplier=Label(self.root,text="Total Supplier\n[ 0 ]",bd=5,relief=RIDGE, bg="#009688",fg="black",font=("goudy old style",24,"bold"))
		self.lbl_supplier.place(x=650,y=120,height=150,width=300)

		self.lbl_category=Label(self.root,text="Total Category\n[ 0 ]",bd=5,relief=RIDGE, bg="#ff5722",fg="black",font=("goudy old style",24,"bold"))
		self.lbl_category.place(x=1000,y=120,height=150,width=300)

		self.lbl_product=Label(self.root,text="Total Product\n[ 0 ]",bd=5,relief=RIDGE, bg="#607d8b",fg="black",font=("goudy old style",24,"bold"))
		self.lbl_product.place(x=300,y=300,height=150,width=300)

		self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE, bg="#ffc107",fg="black",font=("goudy old style",24,"bold"))
		self.lbl_sales.place(x=650,y=300,height=150,width=300)

        #=============footer===================================
		self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangment System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman",15),bg="#4d636d",fg="white")
		self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

		self.update_content()
#=============================================================================================================================

	def employee(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=employeeClass(self.new_win)                #==============employee

	def product(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=productClass(self.new_win)				#==========product 
		
	def supplier(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=supplierClass(self.new_win)			#==========supplier

	def category(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=categoryclass(self.new_win)			#==========product
	
	def product(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=productClass(self.new_win)			#==========product

	def sales(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=salesClass(self.new_win)			#==========product

	def update_content(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			cur.execute("select * from product")
			product=cur.fetchall()
			self.lbl_product.config(text=f'Total Product\n\n[{str(len(product))}]')

			cur.execute("select * from supplier")
			supplier=cur.fetchall()
			self.lbl_supplier.config(text=f'Total Supplier\n\n[{str(len(supplier))}]')

			cur.execute("select * from category")
			category=cur.fetchall()
			self.lbl_category.config(text=f'Total Category\n\n[{str(len(category))}]')

			cur.execute("select * from employee")
			employee=cur.fetchall()
			self.lbl_employee.config(text=f'Total Employee\n\n[{str(len(employee))}]')

			bill=len(os.listdir('bill'))
			self.lbl_sales.config(text=f'Total Sales\n\n[{str(bill)}]')

		
			time_=time.strftime("%I:%M:%S")
			date_=time.strftime("%d-%m-%Y")
			self.lbl_clock.config(text=f"Welcome to Inventory Mangment System\t\t Date:{str(date_)}\t\t Time:{str(time_)}", font=("times new roman",15),bg="#4d636d",fg="white")
			self.lbl_clock.after(200,self.update_content)

		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

if __name__=="__main__":
        root=Tk()			 #object to tkinter class
        obj=IMS(root)  #object of IMS class (addting root to attach tk to IMS class)
        root.mainloop() # to make window stay for long time until close 
		 