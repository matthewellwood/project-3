import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from extras import apology, login_required, GBP

# Configure application
app = Flask(__name__, static_folder='static')

# Custom filter
app.jinja_env.filters["GBP"] = GBP

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///aepricelist.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    """Show Home Page"""
    if request.method == "GET":
        return render_template ("index.html")
    else:
        return render_template("customer_order.html")



@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    """Show Order Form"""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address_1 = request.form.get("Address_1")
        address_2 = request.form.get("Address_2")
        address_3 = request.form.get("Address_3")
        postcode = request.form.get("Postcode")
        telephone_1 = request.form.get("Telephone_1")
        telephone_2 = request.form.get("Telephone_2")
        db.execute("INSERT INTO customers(first_name, last_name, address_1, address_2, address_3, postcode, telephone_1, telephone_2) VALUES (?,?,?,?,?,?,?,?);", first_name, last_name, address_1, address_2, address_3, postcode, telephone_1, telephone_2 ) 
        detail = db.execute("select * from customers;")
        return render_template("list_of_customers.html",detail = detail)
    if request.method == "GET":
        return render_template("new_customer.html")
    
@app.route("/list_of_customers", methods=["GET"])
def list_of_customers():
    if request.method == "GET":
        detail = db.execute("select * from customers;")
        return render_template("list_of_customers.html",detail = detail)
        

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        staff_member = request.form.get("staff_member")
        order_date = request.form.get("order_date")
        customer_id = request.form.get("customer_id")
        customer_last_name = request.form.get("customer_last_name")
        postcode = request.form.get("postcode")
        item_id = request.form.get("item_id")
        info = db.execute("select * from customers JOIN orders ON customers.id = orders.cust_id GROUP BY last_name;")
        return render_template("search.html", info = info)
    else:
        #search_items = staff_member, order_date, customer_id, customer_last_name, postcode, item_id
        return render_template("search.html")
    


@app.route("/customer_order", methods=["GET", "POST"])
def customer_order():
    """Show Order Form"""
    if request.method == "POST":
        staff_member = request.form.get("staff_member")
        order_date = request.form.get("order_date")
        customer_last_name = request.form.get("customer_last_name")
        db.execute("INSERT INTO orders(staff_member, order_date, customer_last_name) VALUES (?, ?, ?);", staff_member, order_date, customer_last_name)
        return render_template("order_details.html")
    if request.method == "GET":
        return render_template("customer_order.html")
    
    
@app.route("/order_details", methods=["GET", "POST"])
def order_details():
    """Show Order Form"""
    if request.method == "POST":
        # do this
        completion_date = request.form.get("completion_date")
        delivery_date = request.form.get("delivery_date")
        item_name = request.form.get("item_name")
        item_description = request.form.get("item_description")
        colour_finish = request.form.get("colour_finish")
        width = request.form.get("width")
        depth = request.form.get("depth")
        height = request.form.get("height")
        extra_details = request.form.get("extra_details")
        selling_price = request.form.get("selling_price")
        del_col_take = request.form.get("del_col_take")
        db.execute("INSERT INTO orders(completion, delivery_date, item_name, item_description, colour_finish, width, depth, height, extra_details, selling_price, del_col_take) VALUES (?,?,?,?,?,?,?,?,?);", completion_date, delivery_date, item_name, item_description, colour_finish, width, depth, height, extra_details, selling_price, del_col_take)
        ord_detail = db.execute("SELECT * FROM orders;")
        return render_template("list_of__orders.html",ord_detail = ord_detail)

    if request.method == "GET":
        return render_template("order_details.html")
    

@app.route("/list_of_orders", methods=["GET", "POST"])
def list_of_orders():
    # do this
    if request.method == "POST":
        # do this
        return render_template("list_of_orders.html")

    if request.method == "GET":
        ord_detail = db.execute("SELECT * FROM orders;")
        return render_template("list_of_orders.html", ord_detail = ord_detail)