from flask import Flask, render_template, request, redirect, url_for, session,flash

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY_SESSION")
app.config['UPLOAD_FOLDER'] =  os.getenv('UPLOAD_FOLDER')
socketio = SocketIO(app, cors_allowed_origins='*')

# Connecting to database 
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
database = os.getenv('DATABASE')

mydb = mysql.connector.connect(user=user,password=password,host=host,database=database,port=3306)



@socketio.on('message')
def handleMessage(msg,id):
    sql = "INSERT INTO history(msg,rID,uID,uname) VALUES (%s,%s,%s,%s)"
    val = (msg,id,getUserId(),session['username'])
 
    mycursor=mydb.cursor()  
    mycursor.execute(sql,val)
    mydb.commit()
    send(msg,broadcast=True)


# custom methods
def auth():
    if not session.get("loggedin"):
        return False
    return True

def isadmin():
    email = session.get("email")
    sql = "SELECT isadmin FROM user WHERE email=%s"
    val = email
    mycursor=mydb.cursor()  
    mycursor.execute(sql,(val,))
    isadmin = mycursor.fetchone()
    if isadmin[0]==1:
        return True
    else:
        return False

def getAdminId():
    mycursor=mydb.cursor()  
    mycursor.execute("SELECT uID FROM user WHERE isadmin=1")
    uID = mycursor.fetchone()
    return uID


def getUserId():
    email = session.get("email")
    sql = "SELECT uID FROM user WHERE email=%s"
    val = email
    mycursor=mydb.cursor()  
    mycursor.execute(sql,(val,))
    user_id = mycursor.fetchone()
    print(user_id)
    return user_id[0]

def getUserName(user_id): 
    sql = "SELECT * FROM user WHERE uID=%s"
    val = user_id
    mycursor=mydb.cursor()  
    mycursor.execute(sql,(val,))
    data = mycursor.fetchone()
    return data[1]+' '+data[2]

def update_idea_status(id,user_id,status):
    sql = "UPDATE idea SET status=%s  WHERE uID=%s AND iID=%s"
    val = (status,user_id,id)
    mycursor=mydb.cursor()  
    mycursor.execute(sql,val)
    mydb.commit()
    pass


def getIdea(id):
    sql = "SELECT user.fname, user.email,user.department, idea.iID, idea.title, idea.idea_desc,idea.status, category.cateogry_name , idea.uID FROM idea INNER JOIN user ON idea.uID = user.uID INNER JOIN category ON idea.cID = category.cID WHERE  iID=%s"
    val = id
    mycursor=mydb.cursor()  
    mycursor.execute(sql,(val,))
    data = mycursor.fetchone() 
    return data

def getSubscribers(id):
    sql = "SELECT COUNT(*) FROM subscription WHERE iID=%s"
    val =id
    mycursor=mydb.cursor()  
    mycursor.execute(sql,(val,))
    data = mycursor.fetchone() 
    return data[0]
# routers

@app.route('/')
def index():
    return redirect('landing_page')

@app.route("/landing_page")
def landing_page():
    return render_template('landing.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE email= %s"
        val = email
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        data = mycursor.fetchone()
        if password==data[6]:
            session['loggedin'] = True
            session['email'] = email
            session['username'] = data[1]
            if data[8] == 1:
                session['admin'] = True
            else:
                session['admin'] = False

            return redirect('home')
        else:
            flash(u'Incorrect usesrname or password', 'info')
            return render_template("error.html")
    else:
        return render_template('login.html')
    
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('admin', None)
    return redirect('landing_page')
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        password1 = request.form['password']
        department = request.form['department']

        sql = "SELECT * FROM user WHERE email=%s"
        val=email
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        data = mycursor.fetchone()

    
        if data:
            flash(u'User already exists', 'warning')
            return render_template("error.html")
        else:
            sql = "INSERT INTO user(fname,lname,gender,phone,email,passwrd,department) values(%s,%s,%s,%s,%s,%s,%s)"
            val = (fname,lname,gender,phone,email,password1,department) 
            mycursor.execute(sql,val)
            mydb.commit()
            session['loggedin'] = True
            session['email'] = email
            session['username'] = fname
            session['admin'] = False

            return redirect('mycategories')
    else:
        return render_template('register.html')

@app.route('/home')
def home():
    if not auth():
        flash(u'Login To continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        sql ="select user.fname, user.lname, user.department, idea.title, LEFT(idea.idea_desc, 50), idea.iID,category.cateogry_name FROM idea INNER JOIN user ON idea.uID=user.uID INNER JOIN favcategory ON idea.cID = favcategory.cID INNER JOIN category ON idea.cID=category.cID WHERE favcategory.uID = %s AND idea.uID <>%s"
        val = (user_id,user_id)
        mycursor=mydb.cursor()  
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        return render_template('home.html',data=result,isadmin=session['admin'])


@app.route('/my_profile', methods =['GET', 'POST'])
def my_profile():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        sql = "SELECT * FROM user WHERE uID=%s"
        val = user_id
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        data = mycursor.fetchone()

        sql = "SELECT COUNT(*) FROM idea WHERE uID=%s"
        mycursor.execute(sql,(val,))
        ideas = mycursor.fetchone()

        sql = "SELECT COUNT(*) FROM subscription WHERE uID=%s"
        mycursor.execute(sql,(val,))
        subscriptions = mycursor.fetchone()

        sql = "Select count(distinct subscription.uID) from subscription  INNER JOIN idea ON subscription.iID=idea.iID WHERE idea.uID=%s"
        val = user_id
        mycursor.execute(sql,(val,))
        subscribers = mycursor.fetchone()

        sql = "SELECT COUNT(*) FROM favcategory WHERE uID=%s"
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        favcat = mycursor.fetchone()
        
        return render_template('profile.html',data=data,ideas=ideas,subscriptions=subscriptions,subscribers=subscribers,favcat=favcat,isadmin=session['admin'])


@app.route('/recent')
def recent():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        sql ="select user.fname, user.lname, user.department, idea.title, LEFT(idea.idea_desc, 50), idea.iID,idea.created,category.cateogry_name FROM idea INNER JOIN user ON idea.uID=user.uID INNER JOIN category ON idea.cID=category.cID  WHERE idea.uID <>%s ORDER BY idea.created DESC"
        val = user_id
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        result = mycursor.fetchall()
        print(result)
        return render_template('recent.html',data=result,isadmin=session['admin'])



@app.route('/mycategories', methods =['GET', 'POST'])
def mycategories():
    if not auth():
        return 'login to continue'
    else:
        user_id = getUserId()
        mycursor=mydb.cursor()  
        if request.method == "POST":
            v1 = request.form.get('cat1')
            v2 = request.form.get('cat2')
            v3 = request.form.get('cat3')
            v4 = request.form.get('cat4')
            v5 = request.form.get('cat5')
            v6 = request.form.get('cat6')
            sql = "INSERT INTO favcategory(uID,cID) VALUES(%s,%s)"
            for x in [v1,v2,v3,v4,v5,v6]:
                if x :
                    val = user_id,x
                    mycursor.execute(sql,val)

                else:
                    pass           
            mydb.commit()
            return redirect('home')
        else:
            return render_template('favcat.html',isadmin=session['admin'])


@app.route('/createidea', methods =['GET', 'POST'])
def createidea():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        if request.method == "POST":
            description = request.form['description'] 
            title = request.form['title'] 
            cid = request.form['cid'] 
            print(description,cid,title)

            mycursor=mydb.cursor()  
            sql = "INSERT INTO idea(uID,idea_desc,cID,title) values(%s,%s,%s,%s)"
            val = (user_id,description,cid,title)
            mycursor.execute(sql,val)
            mydb.commit()

            sql = "SELECT iID from idea WHERE uID=%s AND title=%s"
            val=(user_id,title)
            mycursor.execute(sql,val)
            data = mycursor.fetchone()

            sql = "INSERT INTO room(uID,iID,name) VALUES (%s,%s,%s)"
            val = (user_id,data[0],title)
            mycursor.execute(sql,val)
            mydb.commit()
            
            sql = "SELECT * from room WHERE uID=%s AND name=%s"
            val=(user_id,title)
            mycursor.execute(sql,val)
            rID = mycursor.fetchone()

            sql = "INSERT INTO room_members(rID,uID,iID) VALUES (%s,%s,%s)"
            val = (rID[0],user_id,data[0])
            mycursor.execute(sql,val)
            mydb.commit()

            admin_id = getAdminId()
            val = (rID[0],admin_id[0],data[0])
            mycursor.execute(sql,val)
            mydb.commit()


            return redirect(url_for('idea',id=data[0]))
        else:
            return render_template('createidea.html',isadmin=session['admin'])
   
@app.route('/idea/<id>', methods =['GET', 'POST'])
def idea(id):
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        data = getIdea(id)
        if data[8]== user_id:
            is_owner = True
        else:
            is_owner = False
        subscribers = getSubscribers(id)


        if request.method == 'POST':
            if request.form['form-name'] == "subscribe":
                sql = "INSERT INTO subscription(uID,iID) VALUES (%s,%s)"
                val=(user_id,id)
                mycursor=mydb.cursor()  
                mycursor.execute(sql,val)
                mydb.commit()     
                
                sql = "SELECT rID from room WHERE iID=%s"
                val=(id)
                mycursor.execute(sql,(val,))
                rID = mycursor.fetchone()
                
                sql = "INSERT INTO room_members(rID,uID,iID) VALUES (%s,%s,%s)"
                val = (rID[0],user_id,id)
                mycursor.execute(sql,val)
                mydb.commit()
                return redirect(url_for('chatroom',id=id))
                
            elif request.form['form-name'] == "update":
                status = request.form['progress']
                update_idea_status(id,user_id,status)
                subscribers = getSubscribers(id)
                data = getIdea(id)
                return render_template('idea.html',is_owner=is_owner,data= data,subscribers=subscribers,isadmin=session['admin'])
            else:
                flash(u'Something went wrong', 'warning')
                return render_template("error.html")
        else:
            return render_template('idea.html',is_owner=is_owner,data=data,subscribers=subscribers,isadmin=session['admin'])

@app.route('/my_ideas')
def my_ideas():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        sql ="select  idea.title, LEFT(idea.idea_desc, 50), idea.iID, category.cateogry_name FROM idea INNER JOIN category ON idea.cID=category.cID WHERE  idea.uID =%s"
        val = user_id
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        result = mycursor.fetchall()
        return render_template('myideas.html',data=result,isadmin=session['admin'])

@app.route('/my_subscriptions')
def my_subscriptions():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        sql ="select user.fname, user.lname,user.department, idea.title, LEFT(idea.idea_desc, 50),idea.iID FROM idea INNER JOIN user ON idea.uID=user.uID INNER JOIN subscription ON idea.iID = subscription.iID WHERE subscription.uID =%s"
        val = user_id
        mycursor=mydb.cursor()  
        mycursor.execute(sql,(val,))
        result = mycursor.fetchall()
        return render_template('mysubscriptions.html',data=result,isadmin=session['admin'])



@app.route('/chatroom/<id>')
def chatroom(id):
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    else:
        user_id = getUserId()
        idea_id = id
        sql = "SELECT * FROM room_members WHERE uID =%s AND iID=%s"
        val = user_id,idea_id

        mycursor=mydb.cursor(buffered=True)  
        mycursor.execute(sql,val)
        data = mycursor.fetchone()
        if data:
            sql= "SELECT * FROM history WHERE rID=%s"
            val= data[1]
            mycursor3=mydb.cursor(buffered=True)  
            mycursor3.execute(sql,(val,))
            messages = mycursor3.fetchall()
            sql = "SELECT * FROM room WHERE rID =%s"
            val = data[1]
            mycursor2=mydb.cursor()  
            mycursor2.execute(sql,(val,))
            room_detail = mycursor2.fetchone()
            name=room_detail[3]
            owner=getUserName(room_detail[2])
            sql = "SELECT  user.fname, user.lname FROM room_members INNER JOIN user ON room_members.uID=user.uID WHERE rID =%s group by room_members.uID "
            val = data[1]
            mycursor.execute(sql,(val,))
            usersList =mycursor.fetchall()
             
            return render_template('chatroom.html',messages=messages,uID=user_id,name=name,owner=owner,usersList=usersList,isadmin=session['admin'],rID=data[1])
        else:
            flash(u'Subscribe to continue', 'warning')
            return render_template("error.html")
 
@app.route('/dashboard', methods =['GET', 'POST'])
def dashboard():
    if not auth():
        flash(u'login to continue', 'warning')
        return render_template("error.html")
    elif not isadmin():
        flash(u'You are not an Admin', 'warning')
        return render_template("error.html")
    else:
        sql = "SELECT count(*) FROM user"

        mycursor=mydb.cursor()  
        mycursor.execute(sql)
        user_count = mycursor.fetchone()
        mycursor.execute("SELECT count(*) FROM idea")
        idea_count = mycursor.fetchone()
        sql = "SELECT idea.title, user.fname,user.lname,category.cateogry_name,idea.status, count(*)-1 FROM idea INNER JOIN user ON idea.uID = user.uID INNER JOIN  category ON idea.cID = category.cID INNER JOIN  room_members ON idea.iID = room_members.iID GROUP BY idea.title"       
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mycursor.execute("SELECT COUNT(*), status FROM idea GROUP BY status")
        result = mycursor.fetchall()
        status = {'initiated':0,'in-progress':0,'completed':0,'blocked':0}
        print(result)
        for r in result:
            if r[1] in status:
                status[r[1]] =r[0]
        title = {'Task':'Idea Status'}
        ct = {**title, **status}
        print(ct)
        
        mycursor.execute("SELECT COUNT(*),cateogry_name FROM category,idea WHERE idea.cID=category.cID GROUP BY idea.cID ")
        cat = mycursor.fetchall()
        mycursor.execute("SELECT cateogry_name FROM category")
        result1 = mycursor.fetchall()
        categories = {k[0]:0 for k in result1}
        for c in cat:
            if c[1] in categories:
                categories[c[1]] = c[0]
        title2 = {'Task':'Idea per Category'}
        cat_idea = {**title2, **categories}

        return render_template('dashboard.html',user_count=user_count,idea_count=idea_count,data=data,piedata=ct,piedata2=cat_idea,isadmin=session['admin'])
    

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')


@app.route('/about')
def about():
    return render_template('about.html',isadmin=session['admin'])

@app.errorhandler(404)
def not_found(e):
  return render_template("error.html")

if __name__=='__main__':
    socketio.run(app,debug=True)
