from server.model import Admin
from server.app import db

def addUser(username="admin",password="root"):
    user = Admin(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print("User Added Successfully")

def get_user():
    user = db.session.query(Admin).all()
    if not user:
        addUser()
    return user

def update_user_pass(oldusername,username,newpassword):
    user=db.session.get(Admin,oldusername)
    if user:
        user.username = username
        user.password = newpassword
        db.session.commit()
        print("User Password Updated Sucessfully")
    else:
        addUser()

# def change_user(username,nusername,npassword):
#     row = db.session.query(Admin).filter_by(username=username).first()
#     if row:
#         db.session.delete(row)
#         db.session.commit()
#         print("User Deleted Successfully")
#         addUser(username=nusername,password=npassword)