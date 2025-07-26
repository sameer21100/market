from flask import Flask, render_template,request, session, flash,redirect,url_for
import secrets
import random
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app=Flask(__name__)
app.secret_key='123123123123'
def get_conn():
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    return conn
# def drop():
#     db=get_conn()    
#     cursor=db.cursor()
#     cursor.execute("drop table if exists items")
#     db.commit()
# def create_db():
#     db=get_conn()
#     cursor=db.cursor()
    
#     cursor.execute('''
#     create table if not exists users(
#     id INTEGER primary key autoincrement,
#     username varchar(30) not null unique ,
#     email varchar(50) not null unique,
#     password_hash varchar(60) not null,
#     budget int  not null default 1000
    
#     )''')
#     db.close()
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

# def alter_items_table():
#     db=get_conn()
#     cursor=db.cursor()
#     cursor.execute(''' alter table  items rename to items_old''')
#     cursor.execute('''
#     create table if not exists items(
#     id INTEGER primary key autoincrement,
#     name varchar(100) not null,
#     barcode varchar(12) not null,
#     price int not null,
#     description varchar(1000) not null,
#     owner_id integer ,
#     foreign key (owner_id) references users(id)
#     )
#     ''')
#     cursor.execute('''
#     insert into items(id,name,barcode,price,description,owner_id)
#     select id,name,barcode,price,description,owner_id from items_old
    
#     ''')
#     cursor.execute('''drop table if exists users_old''')
#     db.commit()
#     db.close()
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


@app.route("/")
@app.route("/home")
def main():
    # drop()
    # create_db()
    db=get_conn()
    cursor=db.cursor()
    cursor.execute("select * from users")
    data=cursor.fetchall()
    
    data1=get_users()
    db.close()
    # alter_items_table()
    return render_template("home.html",users=data1)
@app.route("/login",methods=["GET","POST"])
def login():
    if "user" in session:
        flash("You are already logged in")
        return redirect(url_for("main"))
    if request.method== "POST":
        username=request.form["username"]
        password=request.form["password"]
        db=get_conn()
        cursor=db.cursor()
        cursor.execute('''
            select * from users where username = ?''',(username,))
        user=cursor.fetchone()
        if user and check_password_hash(user["password_hash"],password):
            session["user"]=username
            session["budget"]=user["budget"]
            # db=get_conn()
            # cursor=db.cursor()
            # cursor.execute('''
            # Select * from user
            # ''')
            # session["description"]=
            flash("login successfull")
            return redirect(url_for("main"))
        else:
            flash("Wrong credentials")
            return redirect(url_for("login"))
    else:
        
        return render_template("login.html")

@app.route("/logout")
def logout():
    username=session["user"]
    session.clear()
    flash(f"{username} have been logged out")
    return redirect(url_for('login'))
    

@app.route("/register" , methods=["POST","GET"])
def register():
    if request.method=="GET":
        token=secrets.token_hex(16)
        session["csrf_token"]=token
        return render_template("register.html",csrf_token=token)
    else:
        session_token=session["csrf_token"]
        form_token=request.form["csrf_token"]
        if not form_token or session_token!=form_token:
            return "Invalid csrf token",400
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        confirm_pass=request.form["confirm_password"]
        if password !=confirm_pass:
            flash("Password not equal",category='danger')
            return redirect(url_for("register"))
        
        db=get_conn()
        cursor=db.cursor()
        cursor.execute("select * from users where email=? or username=?",(email,username))
        lis=cursor.fetchone()
        if lis:
            flash("User already exists")
            return redirect(url_for("register"))
        hashed_pass=generate_password_hash(password)
        cursor.execute('''
        insert into users(username,email,password_hash)
        values(?,?,?)
        ''',(username,email,hashed_pass))
        db.commit()
        db.close()
        return redirect(url_for("login"))
@app.route("/market")
def market():
    if "user" in session:
        db=get_conn()
        cursor=db.cursor()
        cursor.execute("select * from items")
        data=cursor.fetchall()
        db.close()
        return render_template("market.html",objects=data)
    else:
        flash(f"Please login first {random.randint(0,9)}","error")
        return redirect(url_for("login"))
# if __name__=="__main__":
#     app.run(host="0.0.0.0",port=5050)