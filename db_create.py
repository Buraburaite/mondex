# -*- coding: utf-8 -*-

"""
This code is from a database migration to PostgresSQL. Not needed for app.
"""

from models import db, User, DEXmon, MutableList
from app import app, giveIndexNum
from app import allMonNames
recordedMons=["Pinamon", "Wurmple", "Pikachu", "Raichu", "Voltorb", "Electrode", "Electabuzz",
              "Jolteon", "Zapdos", "Pichu", "Mareep", "Flaafy", "Ampharos", "Elekid", "Raikou",
              "Stingmon", "Wormmon", "Flymon", "FlyBeemon", "Minomon", "Dokunemon", "Snimon",
              "TigerVespamon", "DinoBeemon", "Kuwagamon", "Roachmon", "Trailmon- BG", "SandYanmamon",
              "Guilmon", "Galgomon", "Rapidmon", "Terriermon", "Jigglypuff", "BlackRapidmon"]

db.init_app(app)

#create database

with app.app_context(): #Needed for the sqlalchemy extension to know which app
    db.create_all()


#insert

    import pickle
    oldUsers=pickle.load(open("currentUsers.p", "rb"))
    oldMons=pickle.load(open("currentMons.p", "rb"))
    
    for user in oldUsers:
        monNames=MutableList()
        for mon in oldMons[user]:
            if oldMons[user][mon]!="None":
                monNames+=[mon]
        monNames.sort()
        db.session.add(User(user, oldUsers[user], monNames))


    for mon in allMonNames:
        newMon=DEXmon(mon, giveIndexNum(mon))
        for user in oldUsers:
            if user=="fake":
                newMon.status.update({ user : "SABC" })
            elif user=="john":
                if mon not in recordedMons:
                    newMon.status.update({ user : "None" })
                else:
                  newMon.status.update({ user : "SABC" })
            else:
                newMon.status.update({ user : oldMons[user][mon] })
        db.session.add(newMon)

#commit
    
    db.session.commit()




#Dex=DEXmon.query.all()
#print(Dex)