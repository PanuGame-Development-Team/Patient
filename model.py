from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Unicode(64),unique=True,nullable=False,index=True)
    password = db.Column(db.String(162),nullable=False)#hashed password
    access = db.Column(db.Integer,nullable=False,default=0)
    created_time = db.Column(db.DateTime,default=datetime.now)
    latest_login_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
class Data(db.Model):
    def __todict__(self):
        return {
            'id':self.id,
            'uid':self.uid,
            'machine_type':self.machine_type,
            'garage_id':self.garage_id,
            'error_id':self.error_id,
            'detail':self.detail,
            'errdate':self.errdate.strftime("%Y/%m/%d %H:%M"),
            'created_time':self.created_time.strftime("%Y/%m/%d %H:%M"),
        }
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,index=True)
    machine_type = db.Column(db.String(128),nullable=False,index=True)
    garage_id = db.Column(db.String(128),nullable=False,index=True)
    error_id = db.Column(db.String(32),nullable=False,index=True)
    detail = db.Column(db.UnicodeText,nullable=False)
    errdate = db.Column(db.DateTime,nullable=False)
    created_time = db.Column(db.DateTime,default=datetime.now,index=True)
class Logging(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,index=True)
    data_id = db.Column(db.Integer,db.ForeignKey('data.id'),index=True)
    type = db.Column(db.Integer,nullable=False)
    category = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,nullable=False)
class Session(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,index=True)
    session_id = db.Column(db.String(32),nullable=False,index=True)
    content = db.Column(db.Text)