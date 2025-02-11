# Imports
import os
from flask import *

# Imports from Local Directory
import app
# Import's Keys functions
from app.keys import generate_server_key, double_sha256
# Import's Database functions
from app.models import User, SessionLocal, hash_password
# Import's Authentication functions
from app.auth import *

# Intialization
app = Flask(__name__, "/static", static_folder=".\\Static", template_folder=".\\Templates")
# Generate a server key
server_key = generate_server_key()
# Set a secret key for Flask sessions
app.secret_key = server_key

# Before every Request
@app.before_request
def before_request():
    # List of routes that do not require login
    allowed_routes = ['_index', '_auth', '_listing', 'static', 'login', 'signup', "_err"]
    if 'logged_in' not in session and request.endpoint not in allowed_routes:
        # Check for login cookies
        username = request.cookies.get('username')
        dashboard_key = request.cookies.get('dashboard_key')
        is_admin = request.cookies.get('is_admin')
        if username and dashboard_key:
            session['logged_in'] = True
            session['dashboard_key'] = dashboard_key
            session['is_admin'] = is_admin == 'true'
        else:
            return redirect(url_for('_auth'))
    
    # Admin check for admin routes
    admin_routes = ['admin', 'add_user', 'edit_user', 'delete_user']
    if request.endpoint in admin_routes and not session.get('is_admin'):
        return redirect(url_for('_auth'))

# Index Homepage
@app.route("/")
def _index():
    return render_template("index.html", TITLE="Database Homepage")

# Error Page
@app.route("/err/<code>:<text>")
def _err(code: int, text: str):
    return render_template("err.html", CODE=code, TEXT=text)

# Database Page
@app.route("/listing")
def _listing():
    ldir = os.listdir(".\\db\\")

    for i in ldir:
        if i.endswith(".json") or i.startswith("."):
            ldir.remove(i)
    
    return render_template("listing.html", TITLE="Database Listing", LIST=ldir)

# Sign-in Sign-up Page
@app.route("/auth")
def _auth():
    return render_template("auth.html", TITLE="Authentication")

# Backend Login
@app.route("/login", methods=["POST"])
def login():
    # Example login logic
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = hash_password(password)
    
    # Check user in the database
    db = SessionLocal()
    user = db.query(User).filter(User.username == username, User.password == hashed_password).first()
    db.close()
    
    if user:
        session['logged_in'] = True
        session['is_admin'] = user.is_admin
        # Generate a unique dashboard key using double_sha256
        auth_info = {"username": username}
        dashboard_key = double_sha256(server_key, auth_info)
        session['dashboard_key'] = dashboard_key
        # Set cookies
        resp = make_response(redirect(f'/dashboard'))
        resp.set_cookie('username', username, max_age=60*60*24*30)  # 30 days
        resp.set_cookie('dashboard_key', dashboard_key, max_age=60*60*24*30)  # 30 days
        resp.set_cookie('is_admin', str(user.is_admin).lower(), max_age=60*60*24*30)  # 30 days
        return resp
    else:
        return redirect("/err/401:Invalid%20Credentials")

# Backend Sign-up
@app.route("/signup", methods=["POST"])
def signup():
    # Example signup logic
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = hash_password(password)
    
    # Add user to the database
    db = SessionLocal()
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()
    
    session['logged_in'] = True
    # Generate a unique dashboard key using double_sha256
    auth_info = {"username": username}
    dashboard_key = double_sha256(generate_server_key(), auth_info)
    session['dashboard_key'] = dashboard_key
    # Set cookies
    resp = make_response(redirect(url_for('_dashboard')))
    resp.set_cookie('username', username, max_age=60*60*24*30)  # 30 days
    resp.set_cookie('dashboard_key', dashboard_key, max_age=60*60*24*30)  # 30 days
    return resp

# Backend Logout
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('dashboard_key', None)
    session.pop('is_admin', None)
    # Clear cookies
    resp = make_response(redirect(url_for('_auth')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('dashboard_key', '', expires=0)
    resp.set_cookie('is_admin', '', expires=0)
    return resp

# Rest API for each db
@app.route("/db/<db>")
def _ret_db(db: str):
    return open(f"{db}.json", "r").read()

# Dashboard Page
@app.route("/dashboard")
def _dashboard():
    key = session.get("dashboard_key")
    if key:
        return render_template("dashboard.html", TITLE="Dashboard")
    else:
        return redirect(url_for("_auth"))

# Admin Dashboard
@app.route("/admin")
def _admin():
    if admin(request):
        return render_template("admin/dashboard.html", TITLE="Admin Dashboard")
    else:
        return redirect("/err/401:Unauthorized")

# Admin Users Listing
@app.route("/admin/users")
def _users():
    if admin(request):
        db = SessionLocal()
        users = db.query(User).all()
        db.close()

        list_ = []

        for i in users:
            username = i.username
            email = i.email
            usid = i.id
            list_.append(f"{username},{email},{usid}")

        return render_template("admin/user.html", TITLE="Users Listing", LIST=list_)
    else:
        return redirect("/err/401:Unauthorized")
    
# API for each Database
@app.route("/dashboard/database")
def __():
    return request.args

# 404 Trigger Mechanism
@app.route("/<any>")
def _any(any: str):
    return redirect(f"/err/404:'{any}', Not Found")