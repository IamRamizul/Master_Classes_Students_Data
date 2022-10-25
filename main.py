from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, URL



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.String(250), nullable=False)
    parents = db.Column(db.String(250), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    stream = db.Column(db.Text, nullable=True)
    college = db.Column(db.String(250), nullable=True)

    course = db.Column(db.String(250), unique=False, nullable=True)
    mothers_name = db.Column(db.String(250), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=True)
    address = db.Column(db.String(250), nullable=False)
    admitted_by = db.Column(db.String(250), nullable=False)
    date_of_registration = db.Column(db.String(250), nullable=False)
    total_fees = db.Column(db.Integer, nullable = True)
db.create_all()
##WTForm
class CreateStudentForm(FlaskForm):
    name = StringField("Student's Full name: (Surname + Name + Father's name)", validators=[DataRequired()])
    mothers_name = StringField("Mother's Name", validators=[DataRequired()])
    course = StringField("Enrolled in Course: ", validators=[DataRequired()])
    photo = FileField("Upload Photo:")
    # college = CKEditorField("Blog Content", validators=[DataRequired()])
    college = StringField("College Name: ")
    stream = SelectField("Stream:", choices = ["IX","SSC","Science" ,"Commerce"])
    contact = IntegerField("Student's mobile number:", validators=[DataRequired()] )
    parents = StringField("Parent/Guardian's mobile number:", validators=[DataRequired()] )
    dob = StringField("Date of Birth: ", validators=[DataRequired()])
    address = StringField("Address: ", validators=[DataRequired()])
    admitted_by = StringField("Admission Taken by :", validators = [DataRequired()])
    date_of_admission = StringField("Date of Registration: ", validators=[DataRequired()])
    total_fees = IntegerField("Total Fees of the coures:")
    submit = SubmitField("Add")



##RENDER HOME PAGE USING DB
@app.route('/')
def get_all_posts():
    students = Student.query.all()
    return render_template("index.html", students=students)


##RENDER POST USING DB
@app.route("/post/<int:student_id>")
def show_student(student_id):
    requested_post = Student.query.get(student_id)

    return render_template("post.html", student=requested_post)
@app.route("/search", methods = ["GET", "POST"])
def search_for():
    entered = request.args.get("search_bar").title()
    student = Student.query.filter_by(name = entered).first()
    if student:
        return redirect(url_for("show_student", student_id = student.id))
    else:
        return "Sorry no such student found! Go to the previous page."

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit/<int:student_id>",methods = ["POST","GET"])
def edit_student(student_id):
    form = CreateStudentForm()
    student= Student.query.get(student_id)
    edit_form = CreateStudentForm(
        name = student.name,
        mothers_name = student.mothers_name,
        course = student.course,
        college = student.college,
        stream = student.stream,
        contact=student.contact,
        parents=student.parents,
        dob=student.dob,
        address=student.address,
        admitted_by=student.admitted_by,
        total_fees=student.total_fees
    )
    if edit_form.validate_on_submit():
        student.name = edit_form.name.data
        student.mothers_name = edit_form.mothers_name.data
        student.course = edit_form.course.data
        student.college = edit_form.college.data
        student.stream = edit_form.stream.data
        student.parents = edit_form.parents.data
        student.dob = edit_form.dob.data
        student.address = edit_form.address.data
        student.admitted_by = edit_form.admitted_by.data
        student.total_fees = edit_form.total_fees.data
        student.contact = edit_form.contact.data


        db.session.commit()

        return redirect(url_for("show_student", student_id = student.id))
    return render_template("make-post.html",form=edit_form,is_edit=True)


@app.route("/new_post", methods=["POST", "GET"])
def add_new_student():
    form = CreateStudentForm()

    if form.validate_on_submit():
        new_student = Student(
            date_of_registration=form.date_of_admission.data,
            admitted_by=form.admitted_by.data,
            address=form.address.data,
            name=form.name.data.title(),
            mothers_name=form.mothers_name.data.title(),
            course=form.course.data,
            college=form.college.data,
            stream=form.stream.data,
            contact = form.contact.data,
            parents = form.parents.data,
            dob = form.dob.data,
            total_fees = form.total_fees.data
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect("/")

    return render_template("make-post.html", form=form)

@app.route("/delete_post/<int:student_id>")
def delete_student(student_id):
    student_to_delete = Student.query.get(student_id)
    db.session.delete(student_to_delete)
    db.session.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
