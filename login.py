from cProfile import label
from cgitb import text
from itertools import product
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import os
import email_password
import time
import smtplib
class login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("login system | Developed by Star Group")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
        
        # self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        # self.lbl_phoneimage=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)


        ###login frame========================
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        self.employeeid=StringVar()
        self.password=StringVar() 
        txt_user=Entry(login_frame,textvariable=self.employeeid,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)


        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,text="Log in",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",fg="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgrey").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgrey",font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_fp=Button(login_frame,text="Forget Password?",command=self.forget_pass,font=("times new roman",13),bg="white",fg="#00759E",bd=0,cursor="hand2").place(x=100,y=390)

        ########frame2==================
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        register_lbl=Label(register_frame,text="STAR GROUP",font=("times new roman",13),bg="white").place(x=0,y=20,relwidth=1)

        ############animation====================
        # self.im2=ImageTk.PhotoImage(file="images/im2.png")
        # self.im3=ImageTk.PhotoImage(file="images/im3.png")
        # self.lbl_change_image=Label(self.root)
        # self.lbl_change_image.place(x=367,y=153,width=240,height=428)
        
        
        # self.animate()
        
    
    # def animate(self):
    #     self.im=self.im1
    #     self.im1=self.im2
    #     self.im2=self.im3
    #     self.im3=self.im
    #     self.lbl_change_image.config(image=self.im)
    #     self.lbl_change_image.after(2000,self.animate)


     

    def login(self):
        con=sqlite3.connect(database=r'1.db')
        cur=con.cursor()
        try:
            if self.employeeid.get()==""or self.password.get()=="":
                messagebox.showerror("Error","All field are Required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employeeid.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid ID/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
    
    
    
    def forget_pass(self):
        con=sqlite3.connect(database=r'1.db')
        cur=con.cursor()
        try:
            if self.employeeid.get()=="":
               messagebox.showerror("Error","ID mustbe Required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employeeid.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid ID",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_nwepass=StringVar()
                    self.var_confpass=StringVar()


                    chk=self.sentemail(email[0])
                    if chk =='f':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('Reset Password')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()
                    
                        title=Label(self.forget_win,text="Forget Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_newpass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_newpass=Entry(self.forget_win,textvariable=self.var_nwepass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_confpass=Label(self.forget_win,text="Confirmed Password",font=("times new roman",15)).place(x=20,y=225) 
                        txt_confpass=Entry(self.forget_win,textvariable=self.var_confpass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_pass,state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

                    
                   


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    def update_pass(self):
        if self.var_nwepass.get()=="" or self.var_confpass.get()=="":
            messagebox.showerror("Error","password is required",parent=self.forget_win)
        elif self.var_nwepass.get() != self.var_confpass.get():
            messagebox.showerror("Error","password must be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database="1.db")
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_nwepass.get(),self.employeeid.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated succesfully",parent=self.forget_win)

                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)





    def validate(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP",parent=self.forget_win)



    def sentemail(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_password.email_
        pass_=email_password.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj='Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\n STAR Group'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'





    


          





    


root=Tk()
obj=login_system(root)
root.mainloop()
