from server.app import db
from flask_login import UserMixin
class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable = False)
    template = db.Column(db.String(100), nullable = False)
    isVerified = db.Column(db.Boolean , nullable = False)

    



#Config Models
class Admin(UserMixin,db.Model):
    username = db.Column(db.String(100),nullable=False,primary_key=True)
    password = db.Column(db.String(100),nullable=False)

    def get_id(self):
        return (self.username)

class Messengers(db.Model):
    service = db.Column(db.String(100),nullable=False,primary_key=True)
    token = db.Column(db.String(100),nullable=False)
    chat_id = db.Column(db.String(100))
    use_it = db.Column(db.Boolean,nullable=False)


    

    

