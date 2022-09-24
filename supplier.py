from ast import Delete
from multiprocessing import parent_process
from textwrap import fill
from tkinter import*
from PIL import Image,ImageTk #pip install pillow 
from tkinter import ttk ,messagebox
import sqlite3

class supplierClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.title("Inventory Mangment System")
		self.root.config(bg="white")
		self.root.focus_force()
		######========================= variable=======================================

		self.var_searchby=StringVar()
		self.var_searchtxt=StringVar()

		self.var_sup_invoice=StringVar()
		self.var_contact=StringVar()
		self.var_name=StringVar()


		####==================serach frame===============================================

		searchFrame=LabelFrame(self.root,text="Search employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
		searchFrame.place(x=250,y=20,width=600,height=70)

		####=======================options =============================================
		#lbl_search=Label(searchFrame,text="Search By Invoice No.",bg="white" , font=("times new roman",15))
		#lbl_search.place(x=10,y=10)
		#lbl_search.current(0)

		#txt_search=Entry(searchFrame,textvariable=self.var_searchtxt,font=("goudy old  style",15),bg="lightyellow").place(x=200,y=10)

		#btn_search=Button(searchFrame,text="Search",command=self.search, font=("goudy old  style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=10,width=150,height=30)


		######================================title==================
		title=Label(self.root,text="Supplier Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

		#####===============================content==========================

		###=====================row1================
		lbl_supplier_invoice=Label(self.root,text="Invoice NO.",font=("goudy old style",15),bg="white").place(x=50,y=150)
		txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
		
		
		###=================row2===============================================
		lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
		txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
		
		####========================row3=======================================
		lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=230)
		txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
		
		#####====================row4 ===================================================
		lbl_discription=Label(self.root,text="Discription",font=("goudy old style",15),bg="white").place(x=50,y=270)
		self.txt_discription=Text(self.root,font=("goudy old style",15),bg="lightyellow")
		self.txt_discription.place(x=150,y=270,width=300,height=60)
		
		####========================buttons=============================
		btn_add=Button(self.root,text="Save",command=self.add, font=("goudy old  style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
		btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old  style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
		btn_delete=Button(self.root,text="Delete",command=self.delete, font=("goudy old  style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
		
		####=================employee details==================

		emp_frame=Frame(self.root,bd=3,relief=RIDGE)
		emp_frame.place(x=0,y=350,relwidth=1,height=150)

		scrolly=Scrollbar(emp_frame,orient=HORIZONTAL)
		scrolly=Scrollbar(emp_frame,orient=VERTICAL)
		self.supplierTable=ttk.Treeview(emp_frame,columns=("Invoice","name","Contact","Disc"),yscrollcommand=scrolly.set)
		self.supplierTable.heading("Invoice",text="Invoice id")
		self.supplierTable.heading("name",text="Name")
		self.supplierTable.heading("Contact",text="Contact")
		self.supplierTable.heading("Disc",text="Discription")
		self.supplierTable["show"]="headings"

		self.supplierTable.column("Invoice",width=90)
		self.supplierTable.column("name",width=100)
		self.supplierTable.column("Contact",width=100)
		self.supplierTable.column("Disc",width=100)
		self.supplierTable.pack(fill=BOTH,expand=1)
		self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

		self.show()



#====================================================add===========================================================================

	def add(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			if self.var_sup_invoice.get()=="": 
				messagebox.showerror("Error","Invoice must be required",parent=self.root)
			else:
				cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
				row=cur.fetchone()
				if row!=None:
					messagebox.showerror("Error","This Invoice no. already assigned, try different",parent=self.root)
				else:
					cur.execute("Insert into supplier(invoice,name,contact,desc)values(?,?,?,?)",(
												self.var_sup_invoice.get(),
												self.var_name.get(),
												self.var_contact.get(),
												self.txt_discription.get('1.0' ,END),
																	
					))
					con.commit()
					messagebox.showinfo("Success" ,"Supplier Addedd Successfully",parent=self.root)
					self.show()

		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		

	#==================================show=================	
	def show(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			cur.execute("select * from supplier")
			rows=cur.fetchall()
			self.supplierTable.delete(*self.supplierTable.get_children())
			for row in rows:
				self.supplierTable.insert('',END,values=row)
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		
	#======================================
	def get_data(self,ev):
		f=self.supplierTable.focus()
		content=(self.supplierTable.item(f))
		row=content['values']
		#print(row)
		self.var_sup_invoice.set(row[0]) 
		self.var_name.set(row[1]) 
		self.var_contact.set(row[2]) 
		self.txt_discription.delete('1.0' , END) 
		self.txt_discription.insert( END ,row[4]) 
		
	#======================update=======================================================
	def update(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			if self.var_sup_invoice.get()=="": 
				messagebox.showerror("Error","Invoice no. must be required",parent=self.root)
			else:
				cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid invoice no",parent=self.root)
				else:
					cur.execute("Update supplier set name =?,contact=?,Desc=? where invoice=?",(
												self.var_name.get(),
												self.var_contact.get(),
												self.txt_discription.get('1.0' ,END),
												self.var_sup_invoice.get(),				
					))
					con.commit()
					messagebox.showinfo("Success" ,"Supplier Updated Successfully",parent=self.root)
					self.show()

		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		
	#================================delete=================================
	def delete(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			if self.var_sup_invoice.get()=="": 
				messagebox.showerror("Error","Invoice no must be required",parent=self.root)
			else:
				
				
				cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid Invoice no",parent=self.root)
				else:
					op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
					if op==True:
						cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
						con.commit()
						messagebox.showinfo("Delete","Supplier Deleted Succcesfully",parent=self.root)
						self.show()
		
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
		

#================================Clear===================================================================



#-8:39 #3 video part

#===========================Search =========================================================================

if __name__=="__main__" :
        root=Tk()
        obj=supplierClass(root)
        root.mainloop()
		 