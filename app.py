from flask import Flask,redirect,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:gajanan@localhost:3306/flask_curd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
class User(db.Model):
    Uid=db.Column(db.Integer,primary_key=True)
    Uname = db.Column(db.String(10))
    Pword = db.Column(db.String(10))
    Fname = db.Column(db.String(10))
    Lname = db.Column(db.String(10))
    Gender=db.Column(db.String(10))
    Eid = db.Column(db.String(100))
    PhoneNo = db.Column(db.String(20))
db.create_all()
@app.route('/')
def Login():
    return render_template("login.html")
@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        un=request.form.get('uname')
        pw=request.form.get('pword')
        fn=request.form.get('fname')
        ln=request.form.get('lname')
        pn=request.form.get('phon')
        eid=request.form.get("eid")
        g=request.form.get("Gender")
        l=db.session.query(User.Uname).all()
        list=[i for n in l for i in n]
        msg="Username is allready there plze enter again"
        if un not in list:
            u = User(Uname=un, Pword=pw, Fname=fn, Lname=ln, PhoneNo=pn, Gender=g, Eid=eid)
            db.session.add(u)
            db.session.commit()
        else:
            return render_template("ragister.html", msg=msg)
        return render_template("login.html")
    return render_template("ragister.html")
@app.route("/log",methods=["POST","GET"])
def login():
    un = request.form.get('uname')
    pw = request.form.get('pword')
    if request.method=="POST":
        l = db.session.query(User.Uname).all()
        ulist = [i for n in l for i in n]
        l1 = db.session.query(User.Pword).all()
        plist = [i for n in l1 for i in n]
        if un in ulist:
            i=ulist.index(un)
            if pw==plist[i]:
                return redirect(url_for('view',un=un))
            else:
                msg="invalid password plze try again"
                return render_template("login.html",msg=msg)
        else:
            msg="invalid USER Plze insert again "
            return render_template("login.html", msg=msg)
@app.route("/showdata")
def view():
    u=request.args.get("un")
    list=User.query.filter(User.Uname==u)
    return render_template("display.html",list=list)
@app.route("/delete/<int:uid>")
def delete(uid):
    u=User.query.get(uid)
    db.session.delete(u)
    db.session.commit()
    return redirect('/showdata')
@app.route("/update/<int:uid>",methods=["post","GET"])
def update(uid):
    u =User.query.get(uid)
    if request.method == "POST":
        u.Uname=request.form.get("uname")
        u.Pword=request.form.get("pword")
        u.Fname=request.form.get("fname")
        u.Lname=request.form.get("lname")
        u.Eid=request.form.get("eid")
        u.Gender=request.form.get("Gender")
        u.PhoneNo=request.form.get("phon")
        db.session.commit()
        #return redirect("/showdata")
        return redirect(url_for('view',un=u))
    return render_template("update.html",u=u)
if __name__=='__main__':
    app.run(debug=True)
