from server.model import Data
from server.app import db

def add_data(username, password,template,isVerified):
    data = Data(username= username,
                password=password,
                template=template,
                isVerified=isVerified)
    db.session.add(data)
    db.session.commit()
    print("User added successfully!")

def read_data():
    users = db.session.query(Data).all()
    return users

def update_isVerified(id, new):
    user = db.session.get(Data, id)
    if user:
        user.isVerified = new
        db.session.commit()
        print("User updated successfully")
    else:
        print("User not found")

def delete_data(username):
    row = db.session.query(Data).filter_by(username=username).first()
    if row:
        db.session.delete(row)
        db.session.commit()
        print("User deleted successfully!")
    else:
        print("User not found")

