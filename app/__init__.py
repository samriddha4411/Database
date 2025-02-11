# Imports
import os
from flask import *

# Imports from Local Directory
import app
# Import's Keys functions
from app.keys import generate_server_key

# Initialization
app = Flask(__name__, "/static", static_folder=".\\Static", template_folder=".\\Templates")
# Generate a server key
server_key = generate_server_key()
# Set a secret key for Flask sessions
app.secret_key = server_key

# Before every Request
@app.before_request
def before_request():
    # List of routes that do not require login
    allowed_routes = ['_index', '_listing', 'static', "_err"]
    if request.endpoint not in allowed_routes:
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

# Rest API for each db
@app.route("/db/<db>")
def _ret_db(db: str):
    return open(f"{db}.json", "r").read()

# Dashboard Page
@app.route("/dashboard")
def _dashboard():
    return render_template("dashboard.html", TITLE="Dashboard")

# API for each Database
@app.route("/dashboard/database")
def __():
    return request.args

# 404 Trigger Mechanism
@app.route("/<any>")
def _any(any: str):
    return redirect(f"/err/404:'{any}', Not Found")

if __name__ == "__main__":
    app.run(debug=True)