# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:46:28 2021

@author: Jennifer
"""


from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
import pymongo
import datetime
import re
 
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

app=Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'survey',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

ques=[]
ans=[]
typeofqn=[]
lnk=""
xyz=""
username=""
password=""

class Form(db.Document):
    question=db.ListField()
    answer=db.ListField()
    qntype=db.ListField()
    link=db.StringField()
    response=db.ListField()
    def to_json(self):
        return {"question": self.question,
                "answer": self.answer,
                "qntype":self.qntype,
                "link": self.link,
                "response": self.response}
    
class User(db.Document):
    mailid=db.StringField()
    pwd=db.StringField()
    surveylink=db.ListField()
    def to_json(self):
        return {"mailid": self.mailid,
                "pwd": self.pwd,
                "surveylink":self.surveylink}
    
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["survey"]
mycol1 = mydb["form"]
mycol2 = mydb["user"]

@app.route("/")
def login():
    global username, password 
    username=""
    password=""
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/account",methods=["POST"])
def account():
    global username, password
    username=request.form["mailid"]
    password=request.form["pwd"]
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    
    if(re.search(regex, username)):
        f=0
        for obj in User.objects(mailid=username):
            f=1
        if f==1:
            username=""
            password=""
            return render_template("login.html")
        else:
            mycol2.insert_one({"mailid":username,"pwd":password,"surveylink":[]})
            return render_template("home.html")
    else:
        username=""
        password=""
        return render_template("login.html")

@app.route("/check",methods=["POST"])
def check():
    global username, password
    username=request.form["mailid"]
    password=request.form["pwd"]
    temp=""
    for obj in User.objects(mailid=username):
        temp=obj.pwd
    if temp==password:
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/create")
def create():
    global ques,ans,typeofqn,lnk,xyz
    ques=[]
    ans=[]
    typeofqn=[]
    lnk=""
    xyz=""
    return render_template("create.html")

@app.route("/history")
def history():
    global username
    l=[]
    no=[]
    surveylnk=[]
    for obj in User.objects(mailid=username):
        surveylnk=obj.surveylink
    for obj in Form.objects():
        if obj.link in surveylnk:
            l.append([obj.link,obj.question,obj.qntype,obj.answer,obj.response])
            no.append(len(obj.question))
    print(l)
    return render_template("history.html",l=l,no=no,length=len(l))

@app.route("/attend")
def attend():
    return render_template("attend.html")


@app.route("/qntype",methods=["POST"])
def qntype():
    if request.form["type"]=="mcq":
        return render_template("mcq.html")
    else:
        return render_template("text.html")

@app.route("/addtxt",methods=["POST","GET"])
def addtxt(): 
    ques.append(request.form["question"])
    ans.append(request.form["answer"])
    typeofqn.append("text")
    return render_template("create.html")

@app.route("/addmcq",methods=["POST","GET"])
def addmcq(): 
    ques.append(request.form["question"])
    ans.append([request.form["option1"],request.form["option2"],request.form["option3"],request.form["option4"]])
    typeofqn.append("mcq")
    return render_template("create.html")

@app.route("/submit",methods=["POST"])
def submit():
    global lnk
    time = str(datetime.datetime.now())
    time = time[:13]+"-"+time[14:16]+"-"+time[17:]
    link1 = 'templates/survey '+time+'.html'
    #form(question,answer,link)
    mycol1.insert_one({"question":ques,"answer":ans,"qntype":typeofqn,"link":link1,"response":[]})
    try:
        l=[]
        user = User.objects(mailid=username).get_or_404()
        l=user.surveylink
        l.append(link1)
        user.surveylink=l
        user.save()
    except:
        return render_template("home.html")
    print(ques,ans)
    lnk=link1[10:]
    return render_template("link.html",link=link1[10:])

@app.route("/fillform",methods=["POST","GET"])
def fillform():
    global xyz,ques,ans,typeofqn
    xyz=request.form["link"]
    ques=[]
    ans=[]
    typeofqn=[] 
    
    for obj in Form.objects(link=xyz):
        ques=obj.question
        ans=obj.answer
        typeofqn=obj.qntype
    return render_template("form.html",ques=ques,ans=ans,typeofqn=typeofqn,length=len(ques))
    
@app.route("/response",methods=["POST","GET"])
def response():
    global xyz
    try:
        l=[]
        form = Form.objects(link=xyz).get_or_404()
        l=form.response
        m=[username]
        for i in range(0,len(ques)):
            m.append(request.form[ques[i]])
            print(request.form[ques[i]])
        print(m)
        l.append(m)
        form.response=l
        form.save()
        return render_template("response.html")
    except:
        return render_template("home.html")

if __name__ == '__main__':
    app.run()