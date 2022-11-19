from flask  import Flask,request, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" +os.path.join(basedir,'job.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    dob =db.Column(db.Integer,nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    email =db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.Integer, nullable = False, unique = True)
    date_joined = db.Column(db.Date,default = datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.email}>"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.Integer, nullable = False, unique = True)

    def __repr__(self):
        return f"<User : {self.name}>"
class jobs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.String(50), nullable = False)
    place =db.Column(db.String,nullable = False)
    position = db.Column(db.String, nullable = False)
    skills =db.Column(db.String(50), nullable = False)
    salary = db.Column(db.String, nullable = False)
    application = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<User : {self.application}>"

class appy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    skills = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f"<User : {self.email}>"
with app.app_context():

    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")
@app.route('/new.html')
def new():
    return render_template("new.html")
@app.route('/home.html')
def home():
    data = jobs.query.order_by(jobs.id).all()
    return render_template("home.html", jobs = data)
@app.route('/Candidates.html')
def candidates():
    data = appy.query.order_by(appy.id).all()
    return render_template("candidates.html", appy = data)
@app.route('/apply.html')
def applyjob():
    return render_template("apply.html")
@app.route('/about.html')
def abou():
    return render_template("about.html")
@app.route('/about2.html')
def about():
    return render_template("about2.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")
@app.route('/sign_in.html')
def sign_page():
    return render_template("sign_in.html")
@app.route('/reg_page.html')
def reg_page():
    return render_template("reg_page.html")
@app.route('/Add_jobs.html')
def add_jobs():
    return render_template("Add_jobs.html")
@app.route('/admin.html')
def admin():
    return render_template("admin.html")
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('date')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        avail = bool(Register.query.filter_by(email = email).first())
        avail1 = bool(Register.query.filter_by(password=password).first())
        if avail:
            return render_template('reg_page.html', result = "email already exist")
        elif avail1:
            return render_template('reg_page.html', result = "password already exist")
        else:

            query = Register(name = name, dob = dob, phone = phone, email = email, password = password)
            db.session.add(query)
            db.session.commit()
            return redirect("/sign_in.html")
    else:
        return redirect("/")
@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        name_v = request.form.get('name')
        password_v = request.form.get('password')
        login = Register.query.filter_by(name = name_v, password = password_v).first()
        # query = Admin(name='ESHWIN',password= "Jeffick")
        # db.session.add(query)
        # db.session.commit()
        admin = Admin.query.filter_by(name = name_v, password = password_v).first()
        if login  is not None:
            return render_template('home.html', login_data= name_v)
        elif admin is not None:
            return redirect('Add_jobs.html')
            #pass
        else:
            return render_template('index.html', login_data="make sure  entered the correct password")
@app.route('/addjob',methods=['GET','POST'])
def addjob():
    if request.method == 'POST':
        if request.method == 'POST':
            company = request.form.get('company')
            place = request.form.get('place')
            position = request.form.get('position')
            skills = request.form.get('skills')
            salary = request.form.get('salary')
            application = request.form.get('application')
            query =  jobs(company=company, place=place, position=position, skills=skills, salary=salary,application=application)
            db.session.add(query)
            db.session.commit()
            return redirect("/Add_jobs.html")

@app.route('/apply',methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        if request.method == 'POST':
            application = request.form.get('application')
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            skills = request.form.get('skills')
            experience = request.form.get('experience')
            query = appy(application=application, name=name, phone=phone, email=email, skills=skills,experience=experience)
            db.session.add(query)
            db.session.commit()
            return redirect("/home.html")

if __name__ == '__main__':
    app.run(debug = True)