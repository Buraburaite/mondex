# -*- coding: utf-8 -*-

import pickle

index=pickle.load(open("index.p", "rb"))
abilIndex=pickle.load(open("abilIndex.p", "rb"))
allMoves=pickle.load(open("allMoves.p", "rb"))
allAbils=pickle.load(open("allAbils.p", "rb"))
biomeList=pickle.load(open("biomeList.p", "rb"))
biomeList.remove("N/A")
BACKDOOR=["admin", "jigglypuff"]
    
indexKeys=sorted(index.keys())
allMonNames=[]
allMonLowerNames=[]
for mon in indexKeys:
    allMonNames+=[index[mon]["FullName"]]
    allMonLowerNames+=[index[mon]["FullName"].lower()]

def giveIndexNum(name):
    for mon in index:
        if name.lower()==index[mon]["FullName"].lower():
            indexNum=index[mon]["IndexNumber"]
            break
    return indexNum

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









def giveFullName(name):
    
    for mon in allMonNames:
        if name.lower()==mon.lower():
            name=mon
            break
    return name
    
def makeChecklist(request):
    
    checklist=[]
    if "checkboxS" in str(request.form):
        checklist+=["S"]
    if "checkboxA" in str(request.form):
        checklist+=["A"]
    if "checkboxB" in str(request.form):
        checklist+=["B"]
    if "checkboxC" in str(request.form):
        checklist+=["C"]
    checklist="".join(checklist)
    
    return checklist

def prepareListIndex(username, allUserMons, monNames=allMonNames):
    
    statusDict=dict()
    for mon in allUserMons:
        statusDict.update({ mon.fullName : mon.status[username] })
    
    dexIndex=dict()
    (seenCount, caughtCount, PCount, DCount)=0, 0, 0, 0
    
    for mon in monNames:
        monNum=giveIndexNum(mon)
        
        if "P-" in monNum:
            PCount+=1
        elif "D-" in monNum:
            DCount+=1            
        if statusDict[mon]!="None":
            seenCount+=1
        if "C" in statusDict[mon]:
            caughtCount+=1
        
        monDict={}
        monDict.update({ "FullName" : mon })
        monDict.update({ "Rank" : index[monNum]["Rank"] })
        monDict.update({ "Type" : index[monNum]["Type"] })
        monDict.update({ "Biome" : index[monNum]["Biome"] })
        monDict.update({ "Obtainability" : index[monNum]["Obtainability"] })
        monDict.update({ "Status" : statusDict[mon] })
        dexIndex.update({ monNum : monDict })
    
    dexIndex.update({ "Difference" : PCount - DCount })
    dexIndex.update({ "seenActual" : seenCount })
    dexIndex.update({ "caughtActual" : caughtCount })
    if monNames!=allMonNames:
        dexIndex.update({ "seenTotal" : len(monNames) })
        dexIndex.update({ "caughtTotal" : dexIndex["seenTotal"] })
    else:
        dexIndex.update({ "seenTotal" : len(monNames) })
        dexIndex.update({ "caughtTotal" : dexIndex["seenTotal"] })
    
    keys=list(dexIndex.keys())
    keys.remove("Difference")
    keys.remove("seenActual")
    keys.remove("caughtActual")
    keys.remove("seenTotal")
    keys.remove("caughtTotal")
    keys.sort()
    return [dexIndex, keys]

def makeFilters(request):
    
    filters=dict()
    if request.form["searchLvl"]!="":
        levelRange=request.form["searchLvl"]
    else:
        levelRange="None"
    
    if request.form["searchMove"]!="" and request.form["searchMove"].lower() in allLowerMoves:
        hasMove=request.form["searchMove"].lower()
    elif request.form["searchMove"]!="":
        return "Move not found."
    else:
        hasMove="None"
    
    if request.form["searchAbil"]!="" and request.form["searchAbil"].lower() in allLowerAbils:
        hasAbil=request.form["searchAbil"].lower()
    elif request.form["searchAbil"]!="":
        return "Ability not found."
    else:
        hasAbil="None"
    
    filters.update({ "Level" : levelRange })
    filters.update({ "Rank" : request.form.getlist("rank") })
    filters.update({ "Type" : request.form.getlist("type") })
    filters.update({ "Biome" : request.form.getlist("biome") })
    filters.update({ "BadgeCrest" : request.form.getlist("badgeCrest") })
    filters.update({ "Move" : hasMove })
    filters.update({ "Abil" : hasAbil })
    return filters

def filterMons(username, filters, monNames, allUserMons):
    
    fIndex=index
    results=[]
    keys=list(filters.keys())
    filterStatuses=["None", "S", "SC"]
    
    for mon in allUserMons:
        fIndex[mon.indexNumber].update({ "Status" : mon.status[username] })
    
    for mon in index:
        if (index[mon]["FullName"] in monNames
            and fIndex[mon]["Status"] not in filterStatuses):
            fCount=0
            
            if "Rank" in keys and filters["Rank"]!=[]:
                for rank in filters["Rank"]:
                    if index[mon]["Rank"]==rank:
                        fCount+=1
                        break
                    else:
                        pass
            else:
                fCount+=1
            
            if "Type" in keys and filters["Type"]!=[]:
                for Type in filters["Type"]:
                    if (index[mon]["Type"][0:2]==Type or index[mon]["Type"][3:5]==Type):
                        fCount+=1
                        break
                    else:
                        pass
            else:
                fCount+=1
            
            if "Biome" in keys and filters["Biome"]!=[]:
                for biome in filters["Biome"]:
                    if index[mon]["Biome"]==biome:
                        fCount+=1
                        break
                    else:
                        pass
            else:
                fCount+=1
            
            if "BadgeCrest" in keys and filters["BadgeCrest"]!=[]:
                for bc in filters["BadgeCrest"]:
                    if index[mon]["BadgeCrest"][:2]==bc:
                        fCount+=1
                        break
                    else:
                        pass
            else:
                fCount+=1
            
            if "Level" in keys:
                if "-" in filters["Level"]:
                    levelList=filters["Level"].split("-")
                    minimum=int(levelList[0])
                    maximum=int(levelList[1])
                    if ((index[mon]["LvlA"]>=minimum and index[mon]["LvlA"]<=maximum and "A" in fIndex[mon]["Status"])
                    or (index[mon]["LvlB"]>=minimum and index[mon]["LvlB"]<=maximum and "B" in fIndex[mon]["Status"])):
                        fCount+=1
                    else:
                        pass
                elif filters["Level"]=="None":
                    fCount+=1
                else:
                    if ((index[mon]["LvlA"]==int(filters["Level"]) and "A" in fIndex[mon]["Status"])
                    or (index[mon]["LvlB"]==int(filters["Level"]) and "B" in fIndex[mon]["Status"])):
                        fCount+=1
                    else:
                        pass
                    
            if "Move" in keys:
                if filters["Move"]=="None":
                    fCount+=1
                else:
                    if ("A" in fIndex[mon]["Status"]
                    and (filters["Move"]==index[mon]["MoveAA"].lower() or
                    filters["Move"]==index[mon]["MoveAB"].lower())):
                        fCount+=1
                    elif ("B" in fIndex[mon]["Status"]
                    and (filters["Move"]==index[mon]["MoveBA"].lower() or
                    filters["Move"]==index[mon]["MoveBB"].lower())):
                        fCount+=1
                    else:
                        pass
            
            if "Abil" in keys:
                if filters["Abil"]=="None":
                    fCount+=1
                else:
                    if ("A" in fIndex[mon]["Status"]
                    and (filters["Abil"]==index[mon]["AbilityA"].lower())):
                        fCount+=1
                    elif ("B" in fIndex[mon]["Status"]
                    and (filters["Abil"]==index[mon]["AbilityB"].lower())):
                        fCount+=1
                    else:
                        pass
            
            if fCount==len(keys):
                results+=[index[mon]["FullName"]]
        
    return results


def calcDamage(request):

    if request.form["crit"]=="Manual":
        Crit=float(request.form["Crit"])
    else:
        Crit=float(request.form["crit"])
        
    Atk=float(request.form["Atk"])*float(request.form["atk"])
    Def=float(request.form["Def"])*float(request.form["def"])
    
    if Crit!=1:
        if float(request.form["atk"])<1:
            Atk=float(request.form["Atk"])
        if float(request.form["def"])>1:
            Def=float(request.form["Def"])
            
    Pwr=float(request.form["Pwr"])
    
    if request.form["lvl"]=="Manual":
        Lvl=float(request.form["Lvl"])
    else:
        Lvl=float(request.form["lvl"])
    
    if request.form["dvv"]=="Manual":
        DVV=float(request.form["DVV"])
    else:
        DVV=float(request.form["dvv"])
    
    if request.form["stab"]=="Manual":
        STAB=float(request.form["STAB"])
    else:
        STAB=float(request.form["stab"])
    
    if request.form["effval"]=="Manual":
        EffVal=float(request.form["EffVal"])
    else:
        EffVal=float(request.form["effval"])
    
    if request.form["othera"]=="Manual":
        OtherA=float(request.form["OtherA"])
    else:
        OtherA=float(request.form["othera"])
    
    if request.form["otherb"]=="Manual":
        OtherB=float(request.form["OtherB"])
    else:
        OtherB=float(request.form["otherb"])
    
    if request.form["otherc"]=="Manual":
        OtherC=float(request.form["OtherC"])
    else:
        OtherC=float(request.form["otherc"])
        
    base=(2+(2*Lvl+10)/250.0000*(Atk/Def)*Pwr*10)
    modifier=(STAB+DVV-1)*EffVal*Crit*OtherA*OtherB*OtherC
    damage=(base*modifier)/10
    damage=str(round(damage, 3))
    
    return damage
  
def biomeCheck(username, allUserMons):
    biomeIndex={}
    for biome in biomeList:
        biomeIndex.update({ biome : [0, 0, 0] }) #i.e., [monCount, speciesCount, versionCount]
    
    skipStatuses=["None", "S", "SC"]
    for mon in allUserMons:
        if index[mon.indexNumber]["Biome"]!="N/A":
            biomeIndex[index[mon.indexNumber]["Biome"]][0]+=1
            if mon.status[username] not in skipStatuses:
                biomeIndex[index[mon.indexNumber]["Biome"]][1]+=1
                if "AB" in mon.status[username]:
                    biomeIndex[index[mon.indexNumber]["Biome"]][2]+=2
                else:
                    biomeIndex[index[mon.indexNumber]["Biome"]][2]+=1
    
    for biome in biomeIndex: #first number is percentage species, second is percentage versions
        biomeIndex[biome]=[float(biomeIndex[biome][1])/float(biomeIndex[biome][0]),
                            float(biomeIndex[biome][2])/(float(biomeIndex[biome][0])*2.0), 6-len(biome)]
        biomeIndex[biome]+=[bool(int(biomeIndex[biome][0]*100) < 10)]
        biomeIndex[biome]+=[bool(int(biomeIndex[biome][1]*100) < 10)]
        for i in range(2):
            biomeIndex[biome][i]=str(int(biomeIndex[biome][i]*100))
    
    return biomeIndex
    
if __name__=="__main__":
    x=0