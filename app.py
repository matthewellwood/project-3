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
        choice = request.form.get("choice")
        #details = request.form.get("details")
        #postcode = request.form.get("postcode")
        #if choice == "customer_id" or choice == "customer_last_name" or choice == "postcode" :
        custom = db.execute("select * from customers GROUP BY last_name;")
        #else:
        orders = db.execute("select * from orders;")
        #order_date = request.form.get("order_date")
        #customer_id = request.form.get("customer_id")
        #customer_last_name = request.form.get("customer_last_name")
        #postcode = request.form.get("postcode")
        #item_id = request.form.get("item_id")
        #info = db.execute("select * from customers JOIN orders ON customers.id = orders.cust_id GROUP BY last_name;")
        return render_template("search_results.html", custom = custom, orders = orders)
    else:
        #search_items = staff_member, order_date, customer_id, customer_last_name, postcode, item_id
        return render_template("search.html")
    


@app.route("/customer_order", methods=["GET", "POST"])
def customer_order():
    """Show Order Form"""
    if request.method == "POST":
        staff_member = request.form.get("staff_member")
        order_date = request.form.get("order_date")
        customer_id = request.form.get("customer_id")
        customer_last_name = request.form.get("customer_last_name")
        db.execute("INSERT INTO orders(cust_id, staff_member, order_date, customer_last_name) VALUES (?, ?, ?, ?);", customer_id,  staff_member, order_date, customer_last_name)
        order_info = db.execute("SELECT * FROM orders;")
        last_elem =order_info[len(order_info)-1]
        return render_template("order_details.html", order_info = order_info, last_elem = last_elem)
    if request.method == "GET":
        return render_template("customer_order.html")
    
    
@app.route("/order_details", methods=["GET", "POST"])
def order_details():
    """Show Order Form"""
    if request.method == "POST":
        # do this
        order_number = db.execute("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1;")
        for row in order_number:
            current = row["order_id"]
            current_order = int(current)
        completion = request.form.get("completion")
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
        #change here
        #db.execute("INSERT INTO stock (item_name, item_description, colour_finish, width, depth, height, selling_price) VALUES (?, ?, ?, ?, ?, ?, ?);",item_name, item_description, colour_finish, width, depth, height, selling_price)
        item_check = db.execute("SELECT item_id,item_name FROM stock WHERE item_name = (?);", item_name)
        for row in item_check:
            item_id = row["item_id"]
            if not item_id:
                db.execute("INSERT INTO stock (item_name, item_description, colour_finish, width, depth, height, selling_price) VALUES (?, ?, ?, ?, ?, ?, ?);",item_name, item_description, colour_finish, width, depth, height, selling_price)
            else:
                db.execute("INSERT INTO stock (item_name, item_description, colour_finish, width, depth, height, selling_price) VALUES (?, ?, ?, ?, ?, ?, ?) WHERE item_id = (?);",item_name, item_description, colour_finish, width, depth, height, selling_price, item_id)
        db.execute("UPDATE orders SET completion = (?), delivery_date = (?), item_name = (?) , item_description = (?), colour_finish = (?), width = (?), depth = (?), height = (?), extra_details = (?), selling_price = (?), del_col_take = (?)  WHERE order_id = (?);", completion, delivery_date, item_name, item_description, colour_finish, width, depth, height, extra_details, selling_price, del_col_take, current_order)
        ord_detail = db.execute("SELECT * FROM orders;")
        return render_template("list_of_orders.html",ord_detail = ord_detail)
    else:
        ord_detail = db.execute("select staff_member, order_id, order_date, completion, orders.selling_price, delivery_date, stock.item_id, orders.item_name, address_3, postcode from orders join customers on orders.cust_id = customers.id join stock on orders.item_name = stock.item_name;")
        return render_template("list_of_orders.html", ord_detail = ord_detail)
    

@app.route("/list_of_orders", methods=["GET", "POST"])
def list_of_orders():
    # do this
    if request.method == "POST":
        # do this
        return render_template("list_of_orders.html")

    if request.method == "GET":
        ord_detail = db.execute("select * from orders join customers on orders.cust_id = customers.id;")
        return render_template("list_of_orders.html", ord_detail = ord_detail)
    
@app.route("/stock_list", methods=["GET", "POST"])
def stock_list():
        if request.method == "POST":
        # do this
            return render_template("stock_list.html")

        if request.method == "GET":
            stock = db.execute("SELECT * FROM stock;")
            return render_template("stock_list.html", stock = stock)
        

@app.route("/lounge.html", methods=["GET", "POST"])
def lounge():
        if request.method == "POST":
        # do this
            return render_template("stock_list.html")

        if request.method == "GET":
            lounge = db.execute("SELECT * FROM stock WHERE Type = 'lounge' ;")
            return render_template("lounge.html", lounge = lounge)


@app.route("/bedroom.html", methods=["GET", "POST"])
def bedroom():
        if request.method == "POST":
        # do this
            return render_template("stock_list.html")

        if request.method == "GET":
            bedroom = db.execute("SELECT * FROM stock WHERE Type = 'bedroom' ;")
            return render_template("bedroom.html", bedroom = bedroom)