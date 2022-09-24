
from textwrap import fill
from tkinter import *
#from typing_extensions import self
from PIL import Image,ImageTk #pip install pillow 
from tkinter import ttk ,messagebox
import sqlite3

class categoryclass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+130")
		self.root.title("Inventory Mangment System")
		self.root.config(bg="white")
		self.root.focus_force()
        #####variables=======
		self.var_cat_id=StringVar()
		self.var_name=StringVar()


        ##########title
		lbl_title=Label(self.root,text="Management category",font=("goudy old style",30),bg="#184a45",fg="white").pack(side=TOP,fill=X)
		lbl_name=Label(self.root,text="Enter category name",font=("goudy old style",30),bg="white").place(x=50,y=100)
		txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",25),bg="lightyellow").place(x=50,y=170,width=300)
		
		btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
		btn_del=Button(self.root,text="DELETE",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        ########category Details==========
		cat_frame=Frame(self.root,bd=3,relief=RIDGE)
		cat_frame.place(x=700,y=100,width=380,height=380)

		scrolly=Scrollbar(cat_frame,orient=HORIZONTAL)
		scrolly=Scrollbar(cat_frame,orient=VERTICAL)
		self.categoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set)
		self.categoryTable.heading("cid",text="Category id")
		self.categoryTable.heading("name",text="Name")
		self.categoryTable["show"]="headings"

		self.categoryTable.column("cid",width=90)
		self.categoryTable.column("name",width=100)
		self.categoryTable.pack(fill=BOTH,expand=1)
		self.categoryTable.bind("<ButtonRelease-1>",self.get_data)
		self.show()


        #====================Images================
    

        ######===============fuctions=================================
	def add(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()
		try:
			if self.var_name.get()=="": 
				messagebox.showerror("Error","Category name should be required",parent=self.root)
			else:
				cur.execute("Select * from category where name=?",(self.var_name.get(),))
				row=cur.fetchone()
				if row!=None:
					messagebox.showerror("Error","Category already present, try different",parent=self.root)
				else:
					cur.execute("Insert into category(name)values(?)",(self.var_name.get(),))
					con.commit()
					messagebox.showinfo("Success" ,"Category Addedd Successfully",parent=self.root)
					self.show()

		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

        #==================================show=================	
	def show(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			cur.execute("select * from category")
			rows=cur.fetchall()
			self.categoryTable.delete(*self.categoryTable.get_children())
			for row in rows:
				self.categoryTable.insert('',END,values=row)
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


        #======================================
	def get_data(self,ev):
		f=self.categoryTable.focus()
		content=(self.categoryTable.item(f))
		row=content['values']
		#print(row)
		self.var_cat_id.set(row[0]) 
		self.var_name.set(row[1]) 
		


        #########delete====================
	def delete(self):
		con=sqlite3.connect(database=r'1.db')
		cur=con.cursor()

		try:
			if self.var_cat_id.get()=="": 
				messagebox.showerror("Error","Please select or enter category name",parent=self.root)
			else:
				
				
				cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Error,please try again",parent=self.root)
				else:
					op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
					if op==True:
						cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
						con.commit()
						messagebox.showinfo("Delete","category Deleted Succcesfully",parent=self.root)
						self.show()
						self.var_cat_id.set("")
						self.var_name.set("")
		
		except Exception as ex:
			messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
	




if __name__=="__main__" :
        root=Tk()
        obj=categoryclass(root)
        root.mainloop()
