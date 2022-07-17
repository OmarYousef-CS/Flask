from flask import Flask, flash, redirect, render_template, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, null, true

app = Flask(__name__)
app.secret_key = "super secret key"
#=====DB=Configrations================================================
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#=====LoginManger==================================
login_manger = LoginManager()
login_manger.login_view = 'home'
login_manger.init_app(app)

@login_manger.user_loader
def load_user(id):
	return accounts.query.get(int(id))

#=====Clasees======================================
class accounts(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column("name", db.String(50))
	email = db.Column("email", db.String(50))
	password = db.Column("password", db.String(50))
	story = db.Column("story", db.String(999))

def __init__(self, name, email, password):
	self.name = name
	self.email = email
	self.password = password
	self.story = "no story"

#=====HomePage================================
@app.route("/")
def home():
	return render_template('homePage.html', accounts = accounts.query.filter().all())

#=====SignupPage===============================
@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method == "POST":
		name = request.form.get("usrName")
		email = request.form.get("email")
		pass1 = request.form.get("pass1")
		pass2 = request.form.get("pass2")
		#check if inputs are valid
		if(accounts.query.filter_by(email = email).first()):
			return render_template('signupPage.html', alert="email is Used")
		elif len(pass1) < 8:
			return render_template('signupPage.html', alert="password must be at least 8 charcters")
		elif pass1 != pass2:
			return render_template('signupPage.html', alert="password1 not equal to password2, please try again")
		db.session.add(accounts(name=name, email=email, password=pass1, story="no story"))
		db.session.commit()
		print(accounts.query.filter_by(email = email, password=pass1).first())
		user = accounts.query.filter_by(email = email, password=pass1).first()
		print(user)
		login_user(user, remember=True)
		return redirect(url_for('userZone'))
	if request.method == "GET":
		return render_template('signupPage.html')
	
#=====LoginPage================================
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		email = request.form.get("email")
		passwordForm = request.form.get("password")
		ifAccountInDB = accounts.query.filter_by(email = email, password = passwordForm).first()
		print(ifAccountInDB)
		if not ifAccountInDB:
			return render_template('loginPage.html', alert='Email or Password Wrong, try again')
		login_user(ifAccountInDB, remember=True)
		return redirect(url_for('userZone'))
	if request.method == "GET":
		return render_template('loginPage.html')

#=====LogOut================================
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

#=====User-Zone-After-Login================================
@app.route('/userZone')
@login_required
def userZone():
	return render_template('userPage.html', user=current_user)

#=====Save-the-new-story===================================
@app.route('/saveStory', methods=["POST"])
@login_required
def saveStory():
	current_user.story = request.form.get("newStory")
	db.session.commit()
	return redirect(url_for('userZone'))

#===================================
if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)