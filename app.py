from flask import Flask, render_template,request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
app=Flask(__name__)
def get_conn():
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    return conn
def drop():
    db=get_conn()    
    cursor=db.cursor()
    cursor.execute("drop table if exists items")
    db.commit()
def create_db():
    db=get_conn()
    cursor=db.cursor()
    
    cursor.execute('''
    create table if not exists users(
    id INTEGER primary key autoincrement,
    username varchar(30) not null unique ,
    email varchar(50) not null unique,
    password_hash varchar(60) not null,
    budget int  not null default 1000
    
    )''')
    db.close()
    # cursor.execute('''
    # create table if not exists items(
    # id INTEGER primary key autoincrement,
    # name varchar(100) not null,
    # barcode varchar(12) not null,
    # price int not null,
    # description varchar(1000) not null,
    # owner_id integer ,
    # foreign key (owner_id) references users(id)
    # )
    # ''')

def alter_items_table():
    db=get_conn()
    cursor=db.cursor()
    cursor.execute(''' alter table  items rename to items_old''')
    cursor.execute('''
    create table if not exists items(
    id INTEGER primary key autoincrement,
    name varchar(100) not null,
    barcode varchar(12) not null,
    price int not null,
    description varchar(1000) not null,
    owner_id integer ,
    foreign key (owner_id) references users(id)
    )
    ''')
    cursor.execute('''
    insert into items(id,name,barcode,price,description,owner_id)
    select id,name,barcode,price,description,owner_id from items_old
    
    ''')
    cursor.execute('''drop table if exists users_old''')
    db.commit()
    db.close()
def insert():

    db=get_conn()
    cursor=db.cursor()
    cursor.execute('''insert into items (name,barcode,price,description)
    values(?,?,?,?) ''',("BMW","1asd23123123",1700000,"M3","",1))
    # cursor.execute('''insert into users(username,email,password_hash) 
    # values(?,?,?)''',("sameasderydv","sam@1g.com","123455"))
    db.commit()
    db.close()

def get_items():
    db=get_conn()
    cursor=db.cursor()
    cursor.execute("select * from items")
    data1=cursor.fetchall()
    return data1
def get_users():
    db=get_conn()
    cursor=db.cursor()
    cursor.execute("select * from users")
    data1=cursor.fetchall()
    return data1


app=Flask(__name__)
@app.route("/")
def main():
    # drop()
    # create_db()
    db=get_conn()
    cursor=db.cursor()
    cursor.execute("select * from users")
    data=cursor.fetchall()
    # if len(data)<=2:
    #     print("dickhead")
    #     insert()
    data1=get_users()
    db.close()
    # alter_items_table()
    return render_template("home.html",users=data1)
@app.route("/register" , methods=["POST","GET"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        confirm_pass=request.form["confirm_password"]

        if password !=confirm_pass:
            return "Password not equal"
        
        db=get_conn()
        cursor=db.cursor()
        cursor.execute("select * from users where email=?",(email,))
        lis=cursor.fetchone()
        if lis:
            return "User already exists"
        hashed_pass=generate_password_hash(password)
        cursor.execute('''
        insert into users(username,email,password_hash)
        values(?,?,?)
        ''',(username,email,hashed_pass))
        db.commit()
        db.close()
        return "Registration Successfull"
@app.route("/market")
def market():

    db=get_conn()
    cursor=db.cursor()
    cursor.execute("select * from items")
    data=cursor.fetchall()
    db.close()
    return render_template("market.html",objects=data)
if __name__=="__main__":
    app.run()