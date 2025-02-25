from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

mail = Mail(app) # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dev.samworks@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db.init_app(app)

@app.route("/")
def _index():
    return render_template("index.html", TITLE="Homepage")

@app.route("/dashboard")
def _dashboard():
    if 'user_id' not in session:
        return redirect(url_for('_auth'))
    return render_template("dashboard.html", TITLE="Dashboard")

@app.route("/auth")
def _auth():
    return render_template("auth.html", TITLE="Authentication")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Send welcome email
    msg = Message('Welcome to CyberDeep', sender='dev.samworks@gmail.com', recipients=[email])
    msg.body = f"Hello {name},\n\nThank you for signing up for CyberDeep. We are excited to have you on board!"
    mail.send(msg)

    session['user_id'] = new_user.id
    flash('Account created successfully!', 'success')
    return redirect(url_for('_dashboard'))

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        flash('Logged in successfully!', 'success')
        return redirect(url_for('_dashboard'))
    else:
        flash('Login failed. Check your email and password.', 'danger')
        return redirect(url_for('_auth'))

@app.route("/forgot", methods=["POST"])
def forgot():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Password reset link has been sent to your email.', 'info')
    else:
        flash('Email not found.', 'danger')
    return redirect(url_for('_auth'))

@app.route("/err")
def __error():
    args = request.args.to_dict()
    return render_template("error.html", TEXT=args['text'], CODE=args['code'], TITLE="Oops!")

@app.route("/<else_>")
def __Trigger(else_: str):
    text = f"'{else_}', Page Not Found!"
    return redirect(f"/err?text={text}&code=404")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()