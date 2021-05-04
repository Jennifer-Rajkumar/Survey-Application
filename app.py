# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:46:28 2021

@author: Jennifer
"""


from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
import pymongo
import datetime

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
    
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["survey"]
mycol = mydb["form"]

@app.route("/")
def home():
    return render_template("home.html")

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
    l={}
    for obj in Form.objects():
        l[obj.link]=[obj.question,obj.answer,obj.response]
    return render_template("history.html",l=l)

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
    f = open(link1, 'w')
    html_template = """<html>
    <head>
    <title>Form</title>
    <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trinity School|Private School</title>
        <link rel="stylesheet" href="{{url_for('static',filename='css/style.css')}}" type="text/css">
        <!--<link rel="stylesheet" href="file:///F:/fontawesome-free-5.15.3-web/css/all.css"> -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
            integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
            crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
            integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN"
            crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js"
            integrity="sha384-+YQ4JLhjyBLPDQt//I+STsc9iw4uQqACwlvpslubQzn4u2UU2UFM80nGisd026JF"
            crossorigin="anonymous"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css"
            integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
            integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
    </head>
    <body>
        <nav>
            <div class="logo"><span class="highlight">Survey </span>Application</div>
        </nav>
        <div class="wrapper">
        <div class="title">
            Create Survey
        </div>	
		<form action="/response" method="POST">
			<div class="form">
			    {%for i in range(0,length)%}
				    <div class="input_field">
					    <label for=""><b>{{ques[i]}}</b></label>
				    </div>
                    <label for="">Answer</label>
                    {% if typeofqn[i]=="mcq" %}
                            {% for x in ans[i] %}
                                <div class="input_field">
                                    <input type="radio" name="{{ques[i]}}" id="{{x}}" value="{{x}}" class="input">
                                    <label for="{{x}}">{{x}}</label><br>
                                </div>
                            {% endfor %}
                    {% else %}
                        <div class="input_field">
                            <input type="text" name="{{ques[i]}}" id="{{ques[i]}}" value="{{ques[i]}}" class="input">
				        </div>
                    {% endif %}
                {% endfor %}
				<div class="input_field">
					<input type="submit" value="Submit" class="button">
				</div>
			</div>
		</form>
        </div>

        <footer>
        <div class="footer">
            <div class="inner-footer">
                <div class="footer-items"> 
                    <h1 class="about">About Us</h1>
                </div>
                
                <div class="footer-items"> 
                    <h1 class="about">Quick Links</h1>
                </div>
                
                <div class="footer-items"> 
                    <h2>Contact Us</h2>
                    <div class="borde"></div>
                </div>

            </div>
            <div class="footer-bottom">
                Copyright &copy; Survey Application 2021.All rights reserved.
            </div>
        </div>
    </footer>
    </body>
    </html>
    """
    
    f.write(html_template)
    f.close()
    mycol.insert_one({"question":ques,"answer":ans,"qntype":typeofqn,"link":link1,"response":[]})
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
    return render_template(xyz[10:],ques=ques,ans=ans,typeofqn=typeofqn,length=len(ques))

@app.route("/opensurvey/<link>")
def opensurvey(link):
    global lnk
    lnk=request.view_args['link']
    return render_template(lnk,ques=ques,ans=ans,typeofqn=typeofqn,length=len(ques))
    
@app.route("/response",methods=["POST","GET"])
def response():
    global xyz
    try:
        l=[]
        form = Form.objects(link=xyz).get_or_404()
        l=form.response
        m=[]
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