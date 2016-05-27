# -*- coding: utf-8 -*-


#=============================================================IMPORTS-&-PICKLES
import os, pickle, random, pageMake
from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
from models import db, User, DEXmon
#from config import DevelopmentConfig
from miscFunctions import (giveIndexNum, giveFullName, makeChecklist,
                           makeFilters, filterMons, calcDamage, biomeCheck,
                           prepareListIndex)

filepath=os.path.realpath("app.py")
os.chdir(os.path.dirname(filepath))
index=pickle.load(open("index.p", "rb"))
abilIndex=pickle.load(open("abilIndex.p", "rb"))
allMoves=pickle.load(open("allMoves.p", "rb"))
allAbils=pickle.load(open("allAbils.p", "rb"))
biomeList=pickle.load(open("biomeList.p", "rb"))
biomeList.remove("N/A")
BACKDOOR=["fake", "backdoor"]

#Done each time, in order to allow mid-game changes to mons
indexKeys=sorted(index.keys())
allMonNames=[]
allMonLowerNames=[]
for mon in indexKeys:
    allMonNames+=[index[mon]["FullName"]]
    allMonLowerNames+=[index[mon]["FullName"].lower()]

allLowerMoves, allLowerAbils=[], []
for i in range(len(allMoves)):
    allLowerMoves+=[allMoves[i].lower()]
for i in range(len(allAbils)):
    allLowerAbils+=[allAbils[i].lower()]

#skipMons=[]
#unfinishedMons=[]
#for i in range(len(unfinishedMons)):
#    skipMons+=[giveIndexNum(unfinishedMons[i])]
#skipMons.sort()



app=Flask(__name__)

app.secret_key="fake secret key"

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]

db.init_app(app)
#=====================================================================FUNCTIONS

"""
NOTE: Only functions relating to browsing and the datebase are kept here.
The rest are imported from miscFunctions.py
"""

#Convenience function for development
#def shutdown_server():
#    func=request.environ.get('werkzeug.server.shutdown')
#    if func is None:
#        raise RuntimeError('Not running with the Werkzeug Server')
#    func()
#    return "Server shutting down..."

#Ensures that users are logged in while browsing
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return wrap

#checks to see if [username] is registered
def userExists(username):
    users=db.session.query(User).all()
    for user in users:
        if user.username==username:
            return True
    
    return False

#Users' progress with each mons is saved as a "status-string", updated here
def updateMon(mon, newLetters):
    
    def arrangeLetters(status, newLetters):
        if status=="None":
            status=""
        if "A" in newLetters or "B" in newLetters or "C" in newLetters:
            newLetters+="S"
        letterList=sorted(list(set(list(status + newLetters))))
        if "S" in letterList:
            tempList=[]
            tempList+=["S"] + letterList[:-1]
            newStatus="".join(tempList)
        else:
            newStatus="".join(letterList)
        return newStatus
    
    status=db.session.query(DEXmon).filter_by(fullName=mon).first().status
    status[session["username"]]=arrangeLetters(status[session["username"]], newLetters)
    db.session.query(DEXmon).filter_by(fullName=mon).update({ "status" : status })
    db.session.commit()
    
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    
    if mon not in monNames:
        monNames+=[mon]
        monNames.sort()
        db.session.query(User).filter_by(username=session["username"]).update({ "monNames" : monNames })
        db.session.commit()

def clearStatus(mon):
    status=db.session.query(DEXmon).filter_by(fullName=mon).first().status
    status[session["username"]]="None"
    db.session.query(DEXmon).filter_by(fullName=mon).update({ "status" : status })
    db.session.commit()
    
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
        
    while mon in monNames:
        monNames.remove(mon)
        db.session.query(User).filter_by(username=session["username"]).update({ "monNames" : monNames }) #is this line necessary with mutation tracking?
        db.session.commit()
#================================================================PAGE-FUNCTIONS

@app.route("/login", methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("home"))
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":   
        existingUser=userExists(request.form["username"])
        error="Invalid credentials. Please try again."
        if existingUser==True:
            if request.form["password"]!=User.query.filter_by(username=request.form["username"]).first().password:
                return render_template("login.html", error=error)
            else:
                session["logged_in"]=True
                session["username"]=request.form["username"]
                return redirect(url_for("home"))
        elif existingUser==False:
            return render_template("login.html")
        else:
            return "Error: Uncaught POST request, login()"

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))
    
@app.route("/create-account", methods=["GET", "POST"])
def createAccount():
    if request.method=="GET":
        return render_template("createAccount.html")
    elif request.method=="POST":
        existingUser=userExists(request.form["username"])
        if existingUser==False:
            newUser=User(request.form["username"], request.form["password"])
            db.session.add(newUser)
            for mon in allMonNames:
                status=db.session.query(DEXmon).filter_by(fullName=mon).first().status
                status.update({ request.form["username"] : "None" })
                db.session.query(DEXmon).filter_by(fullName=mon).update({ "status" : status })
            db.session.commit()
            return redirect(url_for("login", error="Account created, please login."))
        elif existingUser==True:
            error="Username taken, please try another."
            return render_template("createAccount.html", error=error)
        else:
            return "Error: Uncaught POST request, createAccount()"

#@app.route("/shutdown")
#def shutdown():
#    shutdown_server()
#    return "Server shutting down..."


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        return render_template("home.html", monNames=monNames)
    elif request.method=="POST":
        if request.form["submit"]=="Go":
            monName=giveFullName(request.form["search"])
            if monName in monNames:
                return redirect(url_for("result", monName=monName))
            else:
                return render_template("home.html", monNames=monNames, errorGo="Not found.")
        elif request.form["submit"]=="Update":
            monName=giveFullName(request.form["searchUpdate"])
            checklist=makeChecklist(request)
            if monName in allMonNames and checklist!="":
                updateMon(monName, checklist)
                return redirect(url_for("result", monName=monName))
            elif monName in allMonNames:
                return render_template("home.html", monNames=monNames, errorUpdate="Select changes.")
            else:
                return render_template("home.html", monNames=monNames, errorUpdate="Not found.")
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Biomes":
            return redirect(url_for("biomePage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, home()"

#The page which displays each mon
@app.route("/result/<monName>", methods=["GET", "POST"])
@login_required
def result(monName): #If redirect here, monName must be in monNames and a FullName
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        monName=giveFullName(monName)
        if monName in monNames:
            session["lastResult"]=monName #session["lastResult"] would make more sense as pageIndex, possible?
            status=db.session.query(DEXmon).filter_by(fullName=monName).first().status[session["username"]]
            pageIndex=pageMake.createPokepage(index[giveIndexNum(monName)], monNames, session["username"], status)
            return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex)
        else:
            return redirect(url_for("home"))
    if request.method=="POST":
        monName=giveFullName(request.form["search"])
        if request.form["submit"]=="Go":
            if monName in monNames:
                session["lastResult"]=monName
                status=db.session.query(DEXmon).filter_by(fullName=monName).first().status[session["username"]]
                pageIndex=pageMake.createPokepage(index[giveIndexNum(monName)], monNames, session["username"], status)
                return redirect(url_for("result", monName=monName))
            else:
                status=db.session.query(DEXmon).filter_by(fullName=monName).first().status[session["username"]]
                pageIndex=pageMake.createPokepage(index[giveIndexNum(session["lastResult"])], monNames, session["username"], status)
                return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex, error="Not found.")
        elif request.form["submit"]=="Update":
            if session["username"]==BACKDOOR[0]:
                pageIndex=pageMake.createPokepage(index[giveIndexNum(session["lastResult"])], monNames, session["username"], "SABC")
                return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex)
            else:
                checklist=makeChecklist(request)
                if checklist!="" and monName in allMonNames:
                    updateMon(monName, checklist)
                    status=db.session.query(DEXmon).filter_by(fullName=monName).first().status[session["username"]]
                    pageIndex=pageMake.createPokepage(index[giveIndexNum(monName)], monNames, session["username"], status)
                    return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex)
                elif checklist!="" and request.form["search"]=="":
                    updateMon(session["lastResult"], checklist)
                    status=db.session.query(DEXmon).filter_by(fullName=session["lastResult"]).first().status[session["username"]]
                    pageIndex=pageMake.createPokepage(index[giveIndexNum(session["lastResult"])], monNames, session["username"], status)
                    return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex)
                elif checklist!="" or (checklist=="" and monName not in allMonNames):
                    status=db.session.query(DEXmon).filter_by(fullName=session["lastResult"]).first().status[session["username"]]
                    pageIndex=pageMake.createPokepage(index[giveIndexNum(session["lastResult"])], monNames, session["username"], status)
                    return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex, error="Not found.")
                elif monName in allMonNames:
                    status=db.session.query(DEXmon).filter_by(fullName=session["lastResult"]).first().status[session["username"]]
                    pageIndex=pageMake.createPokepage(index[giveIndexNum(session["lastResult"])], monNames, session["username"], status)
                    return render_template("monTemplate.html", monNames=monNames, pageIndex=pageIndex, error="Select changes.")
                else:
                    return 'Error: Uncaught POST request, result(), request.form["submit"]="Update"'
        elif request.form["submit"]=="Home":
            return redirect(url_for("home")) 
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))       
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))  #create a switchboard method in order to get rid of this madness?
        else:
            return "Error: Uncaught POST request, result()"

@app.route("/record", methods=["GET", "POST"])
@login_required
def recordChanges():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        return render_template("recordChanges.html", monNames=monNames)
    elif request.method=="POST":
        monName=request.form["searchUpdate"]
        if monName[-3:]=="mom":
            monName=monName[:-1] + "n"
        monName=giveFullName(monName)
        if request.form["submit"]=="Go":
            monName=giveFullName(request.form["search"])
            if monName in monNames:
                return redirect(url_for("result", monName=monName))
            else:
                return render_template("recordChanges.html", errorGo="Not found.")
        elif request.form["submit"]=="Update":
            if session["username"]==BACKDOOR[0]:
                return render_template("recordChanges.html", monNames=monNames)
            else:
                checklist=makeChecklist(request)
                if monName in allMonNames and checklist!="":
                    updateMon(monName, checklist)
                    return render_template("recordChanges.html", monNames=monNames)
                elif monName in allMonNames:
                    return render_template("recordChanges.html", monNames=monNames, errorUpdate="Select changes.")
                else:
                    return render_template("recordChanges.html", monNames=monNames, errorUpdate="Not found.")
        elif request.form["submit"]=="Clear":
            if session["username"]==BACKDOOR[0]:
                return render_template("recordChanges.html", monNames=monNames, errorUpdate="What are you doing?")
            else:
                if monName in allMonNames:
                    clearStatus(monName)
                    return render_template("recordChanges.html", monNames=monNames)
                else:
                    return render_template("recordChanges.html", monNames=monNames, errorUpdate="Not found.")
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, recordChanges()"

@app.route("/list", methods=["GET", "POST"])
@login_required
def dexList():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        if session["username"]==BACKDOOR[0]:
            return render_template("list.html", monNames=monNames, index=pickle.load(open("listIndex.p", "rb")), monList=pickle.load(open("listIndexKeys.p", "rb")))
        else:
            dexIndex=prepareListIndex(session["username"], db.session.query(DEXmon).all())
            return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1])
    elif request.method=="POST":
        if request.form["submit"]=="Go" or request.form["submit"]=="Update":
            monName=giveFullName(request.form["search"])
            if request.form["submit"]=="Go":
                if monName in monNames:
                    return redirect(url_for("result", monName=monName))
                else:
                    if session["username"]==BACKDOOR[0]:
                        return render_template("list.html", monNames=monNames, index=pickle.load(open("listIndex.p", "rb")), monList=pickle.load(open("listIndexKeys.p", "rb")), error="Logged in as admin")
                    else:
                        dexIndex=prepareListIndex(session["username"], db.session.query(DEXmon).all())
                        return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1], error="Not found.")
            elif request.form["submit"]=="Update":
                if session["username"]==BACKDOOR[0]:
                    return render_template("list.html", monNames=monNames, index=pickle.load(open("listIndex.p", "rb")), monList=pickle.load(open("listIndexKeys.p", "rb")), error="Logged in as admin")
                else:
                    checklist=makeChecklist(request)
                    if checklist!="" and monName in allMonNames:
                        updateMon(giveFullName(request.form["search"]), checklist)
                        return redirect(url_for("result", monName=monName))
                    elif monName in allMonNames:
                        dexIndex=prepareListIndex(session["username"], db.session.query(DEXmon).all())
                        return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1], error="Select changes.")
                    else:
                        dexIndex=prepareListIndex(session["username"], db.session.query(DEXmon).all())
                        return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1], error="Not found.")
        elif request.form["submit"]=="Filter":
            filters=makeFilters(request)
            if type(filters)==str:
                dexIndex=prepareListIndex(session["username"], db.session.query(DEXmon).all())
                if "Move" in filters:
                    return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1], errorFilter="Move not found.")
                elif "Ability" in filters:
                    return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1], errorFilter="Ability not found.")
                else:
                    return 'Error: Uncaught POST request, dexList(), request.form["submit"]=="Filter"'            
            else:
                allUserMons=db.session.query(DEXmon).all()
                dexIndex=prepareListIndex(session["username"], allUserMons, filterMons(session["username"], filters, monNames, allUserMons))
            return render_template("list.html", monNames=monNames, index=dexIndex[0], monList=dexIndex[1])
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, dexList()"

@app.route("/type-chart", methods=["GET", "POST"])
@login_required
def typeChart():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        return render_template("typeChart.html", monNames=monNames)
    elif request.method=="POST":
        if request.form["submit"]=="Go":
            if giveFullName(request.form["search"]) in monNames:
                return redirect(url_for("result", monName=giveFullName(request.form["search"])))
            else:
                return render_template("typeChart.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Update":
            monName=giveFullName(request.form["search"])
            if session["username"]==BACKDOOR[0]:
                return redirect(url_for("result", monName=monName))
            else:
                checklist=makeChecklist(request)
                if checklist!="" and monName in allMonNames:
                    updateMon(monName, checklist)
                    return redirect(url_for("result", monName=monName))
                elif monName in allMonNames:
                    return render_template("typeChart.html", monNames=monNames, error="Select changes.")
                else:
                    return render_template("typeChart.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, typeChart()"

@app.route("/map", methods=["GET", "POST"])
@login_required
def mapPage():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        return render_template("map.html", monNames=monNames)
    elif request.method=="POST":
        if request.form["submit"]=="Go":
            if giveFullName(request.form["search"]) in monNames:
                return redirect(url_for("result", monName=giveFullName(request.form["search"])))
            else:
                return render_template("map.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Update":
            monName=giveFullName(request.form["search"])
            if session["username"]==BACKDOOR[0]:
                return redirect(url_for("result", monName=monName))
            else:
                checklist=makeChecklist(request)
                if checklist!="" and monName in allMonNames:
                    updateMon(monName, checklist)
                    return redirect(url_for("result", monName=monName))
                elif monName in allMonNames:
                    return render_template("map.html", monNames=monNames, error="Select changes.")
                else:
                    return render_template("map.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, mapPage()"
            
@app.route("/calc", methods=["GET", "POST"])
@login_required
def calcPage():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        return render_template("calc.html", monNames=monNames, damage="0", draw="0")
    elif request.method=="POST":
        monName=giveFullName(request.form["search"])
        if request.form["submit"]=="Go":
            if monName in monNames:
                return redirect(url_for("result", monName=monName))
            else:
                return render_template("calc.html", monNames=monNames, damage="0", draw="0", error="Not found.")
        elif request.form["submit"]=="Update":
            checklist=makeChecklist(request)
            if monName in allMonNames and checklist!="":
                updateMon(monName, checklist)
                return redirect(url_for("result", monName=monName))
            elif monName in allMonNames:
                return render_template("calc.html", monNames=monNames, damage="0", draw="0", error="Select changes.")
            else:
                return render_template("calc.html", monNames=monNames, damage="0", draw="0", error="Not found.")
        elif request.form["submit"]=="Calculate":
            if request.form["Atk"]=="" or request.form["Def"]=="" or request.form["Pwr"]=="" or (request.form["Lvl"]=="" and request.form["lvl"]=="Manual"):
                return render_template("calc.html", monNames=monNames, damage="0", draw="0", error="Must enter Atk, Def, Pwr, and Lvl")
            else:
                damage=calcDamage(request)
                draw=str(random.randint(1, 100))
                return render_template("calc.html", monNames=monNames, damage=damage, draw=draw)
        elif request.form["submit"]=="Draw":
            draw=str(random.randint(1, 100))
            return render_template("calc.html", monNames=monNames, damage="0", draw=draw)
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request calcPage()"

@app.route("/biome", methods=["GET", "POST"])
@login_required
def biomePage():
    monNames=db.session.query(User).filter_by(username=session["username"]).first().monNames
    if request.method=="GET":
        biomeIndex=biomeCheck(session["username"], db.session.query(DEXmon).all())
        
        return render_template("biomes.html", biomeList=biomeList, biomeIndex=biomeIndex, monNames=monNames)
    elif request.method=="POST":
        if request.form["submit"]=="Go":
            if giveFullName(request.form["search"]) in monNames:
                return redirect(url_for("result", monName=giveFullName(request.form["search"])))
            else:
                return render_template("biomes.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Update":
            monName=giveFullName(request.form["search"])
            if session["username"]==BACKDOOR[0]:
                return redirect(url_for("result", monName=monName))
            else:
                checklist=makeChecklist(request)
                if checklist!="" and monName in allMonNames:
                    updateMon(monName, checklist)
                    return redirect(url_for("result", monName=monName))
                elif monName in allMonNames:
                    return render_template("biomes.html", monNames=monNames, error="Select changes.")
                else:
                    return render_template("biomes.html", monNames=monNames, error="Not found.")
        elif request.form["submit"]=="Home":
            return redirect(url_for("home"))
        elif request.form["submit"]=="Record":
            return redirect(url_for("recordChanges"))
        elif request.form["submit"]=="List":
            return redirect(url_for("dexList"))
        elif request.form["submit"]=="Map":
            return redirect(url_for("mapPage"))
        elif request.form["submit"]=="Type Chart":
            return redirect(url_for("typeChart"))
        elif request.form["submit"]=="Calculate":
            return redirect(url_for("calcPage"))
        elif request.form["submit"]=="Logout":
            return redirect(url_for("logout"))
        else:
            return "Error: Uncaught POST request, biomePage()"


if __name__=="__main__":
    app.run(debug=True)
    #Left as True since that made it easier to debug, considering there were
    #few users and they could send pictures of the errors they received.