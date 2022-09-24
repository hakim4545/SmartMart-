import sqlite3
def create_db():
    con=sqlite3.connect(database=r'1.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text , email text , gender text, contact text, dob text, doj text, pass text, utype text, adress text, salary text)" ,)
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text , contact text , desc text)" ,)
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text , Category text , name text, price text, qty text, status text)" )
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS customer(invoice INTEGER PRIMARY KEY AUTOINCREMENT,cname text , cemail text , billamt text, tax text, netpay text , date text)")
    con.commit()

[]
create_db()   


        # CREATE TABLE database_name.table_name(
        # column1 datatype PRIMARY KEY(one or more columns),
        # column2 datatype,
        # column3 datatype,
        # .....
        # columnN datatype
        # );