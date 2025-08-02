import razorpay
import os
from flask import Flask, render_template,request, session, flash,redirect,url_for,send_file
import secrets
import random
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import psycopg2

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, text


# if os.environ.get("FLASK_ENV") != "production":
# from dotenv import load_dotenv
# load_dotenv()



app=Flask(__name__)
app.secret_key='123123123123'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
# print(f"first motha fuka issue  {RAZORPAY_KEY_SECRET}")

# @app.route('/download-db')
def download_db():
    return send_file('database.db', as_attachment=True)
import psycopg2.extras

def get_conn():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=psycopg2.extras.RealDictCursor
    )
# def drop():
#     db=get_conn()    
#     cursor=db.cursor()
#     cursor.execute("drop table if exists items")
#     db.commit()


# @app.route("/create-db")
# def create_db():
    flash("Data migration in progress")
    db=get_conn()
    cursor=db.cursor()
    cursor.execute('''
    drop table if exists users_new cascade''')
    cursor.execute('''drop table if exists items_new''')
    db.commit()
    cursor.execute('''
    create table if not exists users_new(
     id  serial  primary key ,
        username varchar(30) not null unique,
        email varchar(100) not null unique,
        password_hash varchar(600) not null,
        budget int not null default 50,
        phone varchar(10) default null,
        ip_address varchar(50000) default null
    )
    
    ''')

    cursor.execute('''
    
    create table if not exists items_new(
    id  serial  primary key ,
    name varchar(100) not null,
    barcode varchar(12) not null,
    price varchar(2000) not null,
    description varchar(1000) not null,
    owner_id integer,
    foreign key (owner_id) references users_new(id)
    )
    
    ''')
    db.commit()
    
    db_sqlite=sqlite3.connect("database.db")
    db_sqlite.row_factory=sqlite3.Row
    cursor_sqlite=db_sqlite.cursor()
    db_pgsql=get_conn()
    cursor_pgsql=db_pgsql.cursor()




    cursor_sqlite.execute('''
    select * from users
    ''')
    rows=cursor_sqlite.fetchall()
    for row in rows:
        cursor_pgsql.execute('''
        insert into users_new (id,username,email,password_hash,budget,phone,ip_address)
        values(%s,%s,%s,%s,%s,%s,%s)
        ''',(
            row["id"],
            row["username"],
            row["email"],
            row["password_hash"],
            row["budget"],
            row["phone"],
            row["ipaddress"]
        ))
    db_pgsql.commit()
    cursor_sqlite.execute(''' 
    select * from items_new
    ''')
    rows=cursor_sqlite.fetchall()
    for row in rows:
        cursor_pgsql.execute('''
        insert into items_new(id,name, barcode,price,description,owner_id)
        values(%s,%s,%s,%s,%s,%s)
        
        ''',(
            row["id"],
            row["name"],
            row["barcode"],
            row["price"],
            row["description"],
            row["owner_id"]
        ))
    db_pgsql.commit()
    cursor_pgsql.close()
    cursor_sqlite.close()
    db_pgsql.close()
    db_sqlite.close()
    flash("The Data migration is successfull")
    return redirect(url_for("main"))

# def create_db():
#     db=get_conn()
#     cursor=db.cursor()
    # cursor.execute('''
    #     alter table users rename to user_old2
    # ''')       
    # cursor.execute('''
    # create table if not exists users(
    #     id integer primary key autoincrement,
    #     username varchar(30) not null unique,
    #     email varchar(100) not null unique,
    #     password_hash varchar(60) not null,
    #     budget int not null default 50,
    #     phone varchar(10) default null,
    #     ipaddress varchar(50000) default null
    #     )

    # ''') 
    # db.commit()
    # cursor.execute(''' 
    #     insert into users(id,username,email,password_hash,budget,phone)
    #     select id ,username,email,password_hash,budget,phone from user_old2
    # ''')
    # cursor.execute('''
    #     drop table user_old2
    #     ''')
    # db.commit()
    # db.close()

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
# def insert():

#     db=get_conn()
#     cursor=db.cursor()
#     cursor.execute('''insert into items (name,barcode,price,description)
#     values(?,?,?,?) ''',("BMW","1asd23123123",1700000,"M3","",1))
    # cursor.execute('''insert into users(username,email,password_hash) 
    # values(?,?,?)''',("sameasderydv","sam@1g.com","123455"))
    # db.commit()
    # db.close()

# def get_items():
#     db=get_conn()
#     cursor=db.cursor()
#     cursor.execute("select * from items")
#     data1=cursor.fetchall()
#     return data1
# def get_users():
#     db=get_conn()
#     cursor=db.cursor()
#     cursor.execute("select * from users")
#     data1=cursor.fetchall()
#     return data1


@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def main():
    # flash("No working cuzz I need to change the database system!! Everything's broke ")
    # create_db()
    # print(f"{os.environ.get('FLASK_ENV')} falsk asdlfalsdjfaksd")
    # print(request.form.get('form_type'))
    if request.method=="POST" and request.form.get('form_type'):
        if "user" in session:
            return redirect(url_for('market'))
        else:
            flash("Please login first")
            return redirect(url_for('register'))
    # drop()
    # create_db()
    # db=get_conn()
    # cursor=db.cursor()
    # cursor.execute("select * from users")
    # data=cursor.fetchall()
    
    # data1=get_users()
    # db.close()
    # alter_items_table()
    return render_template("home.html")
@app.route("/add_user_phone/", methods=["GET","POST"])
def add_user_phone():
    if session["phone"] is not None :
        flash("Phone number already added")
        return redirect(url_for("main"))
    if request.method=="POST":
        phone=request.form["phone"]
        session["phone"]=phone
        db=get_conn()
        cursor=db.cursor()
        cursor.execute('''
        update users_new set phone=%s where id=%s
        ''',(phone,session["id"]))
        db.commit()
        db.close()
        flash("Number added successfull")
        return redirect(url_for("add"))
    else:
        return render_template("add_user_phone.html")
@app.route("/add",methods=["GET","POST"])
def add():

    if "user" in session:
        print(f"{session['phone']} is the phone number")
        if session["phone"] is None:
            flash("Please enter your phone number first")
            return redirect(url_for("add_user_phone"))
        if request.method=="POST":
            name=request.form["name"]
            barcode=request.form["barcode"]
            price=request.form["price"]
            description=request.form["description"]
            owner_id=session["id"]

            db=get_conn()
            cursor=db.cursor()
            cursor.execute('''
            insert into items_new (name,barcode,price,description,owner_id)
            values(%s,%s,%s,%s,%s)''',
            (name,barcode,price,description,owner_id))
            db.commit()
            flash("Item added successfully")
            return redirect(url_for('market'))

        elif request.method=="GET":
           
            return render_template("add.html")
    else:
        flash("Please login to view this page")
        return redirect(url_for("login"))
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
            select * from users_new where username = %s''',(username,))
        user=cursor.fetchone()
        if user and check_password_hash(user["password_hash"],password):
            session["user"]=username
            session["budget"]=user["budget"]
            print(user["budget"])
            # print(user["id"])
            session["phone"]=user["phone"]
            session["id"]=user["id"]
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
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')  
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
        cursor.execute("select * from users_new where email=%s or username=%s",(email,username))
        lis=cursor.fetchone()
        if lis:
            flash("User already exists")
            return redirect(url_for("register"))
        hashed_pass=generate_password_hash(password)
        cursor.execute('''
        insert into users_new(username,email,password_hash,ip_address)
        values(%s,%s,%s,%s)
        ''',(username,email,hashed_pass,ip_address))
        db.commit()
        db.close()
        return redirect(url_for("login"))
@app.route("/delete/<id>",methods=["POST"])
def delete(id):
    db=get_conn()
    cursor=db.cursor()
    cursor.execute(''' 
    delete from items_new where id=%s and owner_id=%s
    ''',(id,session['id']))
    db.commit()
    return redirect(url_for("market"))

@app.route("/create_payment/<int:val>", methods=["GET"])
def create_payment(val):
    

    if "user" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    if val < 50:
        flash("Minimum amount should be ₹500")
        return redirect(url_for("market"))

    client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET ))
    # print(f"here is the issue mothaforka{RAZORPAY_KEY_ID}")
    # client = razorpay.Client(auth=("rzp_live_PrDxVO5r3nbrTB", "60sCmL6zRZOO91f4Yv2VzzCM"))
    order_data = {
        "amount": val * 100,  # amount in paise
        "currency": "INR",
        "payment_capture": 1
    }
    payment = client.order.create(order_data)
    return render_template("payment.html", payment=payment, val=val,key_id=RAZORPAY_KEY_ID)

@app.route("/payment_success", methods=["POST"])
def payment_success():
    import razorpay
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
    data = request.form
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })
    except:
        flash("Payment verification failed")
        return redirect(url_for("market"))

    val = int(request.form['val'])
    session['budget'] += val
    db = get_conn()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE users_new
        SET budget = %s
        WHERE id = %s
    ''', (session['budget'], session['id']))
    db.commit()
    db.close()
    flash(f"₹{val} added to your budget")
    return redirect(url_for("market"))

@app.route("/reduce/<int:val>/<int:owner_id>", methods=["POST"])
def reduce(val,owner_id):
    if session['budget'] < int(val):
        flash("Not enough balance. Please add funds.")
        return redirect(url_for("create_payment", val=val))
    else:
        session['budget'] =session['budget']- int(val)
        db = get_conn()
        cursor = db.cursor()
        cursor.execute('''
            update users_new
            set budget=%s
            where id=%s
        ''', (session['budget'], session['id']))
        owner_id=int(owner_id)
        cursor.execute('''
            select * from users_new where id=%s
        ''',(owner_id,))
        seller=cursor.fetchone()
        phone_of_owner=seller["phone"]
        user_name=seller["username"]
        # print(phone_no_of_owner)
        flash(f"The phone number of the seller({user_name})  is: {phone_of_owner}")
        db.commit()
        db.close()
        # session["phone_no_of_user"]=phone_no_of_owner["phone"]
        return redirect(url_for('market'))
@app.route("/users")
def user():
    db=get_conn()
    cursor=db.cursor()
    cursor.execute('''
    select * from users_new
    ''')
    users=cursor.fetchall()
    return render_template("list_users.html",users=users)
def fix_postgres_sequence():
    db = get_conn()
    cursor = db.cursor()
    cursor.execute("SELECT setval('items_new_id_seq', (SELECT MAX(id) FROM items_new));")
    db.commit()
    cursor.close()
    db.close()
@app.route("/market")
def market():
    # fix_postgres_sequence()
    # flash("the sequence has been fixed")

    if "user" in session:
        db=get_conn()
        cursor=db.cursor()
        cursor.execute("select * from items_new order by id desc")
        data=cursor.fetchall()
        db.close()
        return render_template("market.html",objects=data)
    else:
        flash(f"Please login first {random.randint(0,9)}","error")
        return redirect(url_for("login"))
# if __name__=="__main__":
#     app.run(host="0.0.0.0",port=5050,debug="true")
