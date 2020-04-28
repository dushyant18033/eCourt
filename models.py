from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column('ID', db.Integer, primary_key = True)
    Username = db.Column('Username', db.String(40), unique = True, nullable = False)
    Password = db.Column('Password', db.String(100), nullable = False)
    ClientID = db.Column('ClientID', db.Integer, db.ForeignKey('Clients.ID'))
    LawyerID = db.Column('LawyerID', db.Integer, db.ForeignKey('Lawyers.ID'))
    JudgeID = db.Column('JudgeID', db.Integer, db.ForeignKey('Judges.ID'))
    FirmID = db.Column('FirmID', db.Integer, db.ForeignKey('Firms.ID'))

class Client (db.Model):
    __tablename__ = 'Clients'

    ID = db.Column('ID', db.Integer, primary_key = True)
    Name = db.Column('Name', db.String(30), nullable = False)
    DOB = db.Column('DOB', db.Date, nullable = False)

class Lawyer (db.Model):
    __tablename__ = 'Lawyers'

    ID = db.Column('ID', db.Integer, primary_key = True)
    Name = db.Column('Name', db.String(30), nullable = False)
    AIBE = db.Column('AIBE', db.Integer, nullable = False)
    License_status = db.Column('License_status', db.String(10), nullable = False)
    Spec_Area = db.Column('Spec_Area', db.String(30), nullable = False)
    FirmID = db.Column('FirmID', db.Integer,db.ForeignKey('Firms.ID'))
    ED_Profile = db.Column('Ed_Profile', db.String(30), nullable = False)
    Rating = db.Column('Rating', db.Integer)
    Fees_Range = db.Column('Fees_Range', db.Integer)
    

class Firms (db.Model):
    __tablename__ = 'Firms'

    ID = db.Column('ID', db.Integer, primary_key = True)
    Name = db.Column('Name', db.String(30), nullable = False)
    License_status = db.Column('License_status', db.String(10), nullable = False)
    Spec_Area = db.Column('Spec_Area', db.String(30), nullable = False)
    Rating = db.Column('Rating', db.Integer)
    Fees_Range = db.Column('Fees_Range', db.Integer)
    Est = db.Column('Est', db.Integer)


    


class Judge (db.Model):
    __tablename__ = 'Judges'

    ID = db.Column('ID', db.Integer, primary_key = True)
    Name = db.Column('Name', db.String(30), nullable = False)
    Recruit_Src = db.Column('Recruit_Src', db.String(30), nullable = False)
    Apptmnt_Date = db.Column('Apptmnt_Date', db.Date, nullable = False)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
