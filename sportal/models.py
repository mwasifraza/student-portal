from sportal import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    fname    = db.Column(db.String(length=255), nullable=False)
    lname    = db.Column(db.String(length=255), nullable=False)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    email    = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    gender   = db.Column(db.String(length=255), nullable=False)
    course   = db.Column(db.Integer(), db.ForeignKey('course.id'))

    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

class Course(db.Model):
    id             = db.Column(db.Integer(), primary_key=True)
    course_name    = db.Column(db.String(length=255), nullable=False, unique=True)
    course_teacher = db.Column(db.String(length=255), nullable=False)
    course_day     = db.Column(db.String(length=255), nullable=False)
    users          = db.relationship('User', backref='student', lazy=True)

    