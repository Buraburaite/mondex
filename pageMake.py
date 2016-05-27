# -*- coding: utf-8 -*-

"""
This contains functions relating to generating a dictionary containing all
information available to a user concerning any particular mon. The function
that actually returns the dictionary is createPokepage(mon, monNames,
                                                       username, status)
"""


from miscFunctions import giveIndexNum
import pickle

index=pickle.load(open("index.p", "rb"))
abilIndex=pickle.load(open("abilIndex.p", "rb"))
BACKDOOR=["fake", "backdoor"]
    
indexKeys=sorted(index.keys())
allMonNames=[]
allMonLowerNames=[]
for mon in indexKeys:
    allMonNames+=[index[mon]["FullName"]]
    allMonLowerNames+=[index[mon]["FullName"].lower()]

skipMons=[]
unfinishedMons=["BlackElecmon", "Betsumon", "Akatorimon", "WaruSeadramon", "Kogamon", "Tinkermon",
                "KoEnimon", "Petermon", "Ganemon", "Splashmon"]
for i in range(len(unfinishedMons)):
    skipMons+=[giveIndexNum(unfinishedMons[i])]
skipMons.sort()




def fixName(oldName):
    newName=oldName.replace("-","").replace(" ","").replace(".","").replace("'","")

    return newName

def createPreList(mon, monNames, table):
    
    preList=[]
    for i in range(1, 4):
        if table!="Master":
            if (mon["PreEv" + str(i)]!="P-000" and mon["PreEv" + str(i)]!="D-000"
                and ("P-" in mon["PreEv" + str(i)] or "D-" in mon["PreEv" + str(i)]) 
                and mon["PreEv" + str(i)] not in skipMons
                and index[mon["PreEv" + str(i)]]["FullName"] in monNames):
                
                preList+=[index[(mon["PreEv" + str(i)])]["FullName"]]
                    
        else:
            if (mon["PreEv" + str(i)]!="P-000" and mon["PreEv" + str(i)]!="D-000"
                and ("P-" in mon["PreEv" + str(i)] or "D-" in mon["PreEv" + str(i)])
                and (mon["PreEv" + str(i)] not in skipMons)):
                preList+=[index[(mon["PreEv" + str(i)])]["FullName"]]
    
    return preList

def createEvoList(mon, monNames, table):
    
    evoList=[]
    for i in range(1, 9):
        if table!="Master":
            if (mon["Ev" + str(i)]!="P-000" and mon["Ev" + str(i)]!="D-000"
                and ("P-" in mon["Ev" + str(i)] or "D-" in mon["Ev" + str(i)]) 
                and mon["Ev" + str(i)] not in skipMons
                and index[mon["Ev" + str(i)]]["FullName"] in monNames):
                
                evoList+=[index[(mon["Ev" + str(i)])]["FullName"]]
                    
        else:
            if (mon["Ev" + str(i)]!="P-000" and mon["Ev" + str(i)]!="D-000"
                and ("P-" in mon["Ev" + str(i)] or "D-" in mon["Ev" + str(i)])
                and (mon["Ev" + str(i)] not in skipMons)):
                evoList+=[index[(mon["Ev" + str(i)])]["FullName"]]
    
    return evoList

def arrangeAbil(mon):

    monName=fixName(mon["FullName"])
    abilList=[]
    noneCount=0
    for i in range(1, 5):
        if abilIndex[(monName+"Abils")][str(i)]!="None":
            abilList+=[abilIndex[(monName+"Abils")][str(i)]]
        elif abilIndex[(monName+"Abils")][str(i)]=="None":
            noneCount+=1
    abilList.sort()
    for i in range(noneCount):
        abilList+=["None"]

    return abilList


def arrangeEvo(preList, evoList):

    for i in range(0, len(preList)):
        preList[i]=preList[i] + ".png"

    for i in range(0, len(evoList)):
        evoList[i]=evoList[i] + ".png"
        
    imageList=[]

    ##In this function, images are added to imageList based
    ##on the Template markers: vertically, moving left to right.
    ##(ex. 3A, 2A, 3B, 2B, 3C for pre-evolutions)

    if len(preList)==0:
        for i in range(5):
            imageList+=["Markers/noPic.png"]
    elif len(preList)==1:
        imageList+=["Markers/noPic.png"]   #3A
        imageList+=["Markers/noPic.png"]   #2A
        imageList+=["Icons/" + preList[0]] #3B
        imageList+=["Markers/noPic.png"]   #2B
        imageList+=["Markers/noPic.png"]   #3C
    elif len(preList)==2:
        imageList+=["Markers/noPic.png"]   #3A
        imageList+=["Icons/" + preList[0]] #2A
        imageList+=["Markers/noPic.png"]   #3B
        imageList+=["Icons/" + preList[1]] #2B
        imageList+=["Markers/noPic.png"]   #3C
    elif len(preList)==3:
        imageList+=["Icons/" + preList[0]] #3A
        imageList+=["Markers/noPic.png"]   #2A
        imageList+=["Icons/" + preList[1]] #3B
        imageList+=["Markers/noPic.png"]   #2B
        imageList+=["Icons/" + preList[2]] #3C


    if len(evoList)==0:
        for i in range(18):
            imageList+=["Markers/noPic.png"]
    elif len(evoList)==1:
        imageList+=["Markers/noPic.png"]   #N
        imageList+=["Markers/noPic.png"]   #O
        imageList+=["Markers/noPic.png"]   #P
        imageList+=["Markers/noPic.png"]   #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Icons/" + evoList[0]] #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==2:
        imageList+=["Markers/noPic.png"]   #N
        imageList+=["Markers/noPic.png"]   #O
        imageList+=["Markers/noPic.png"]   #P
        imageList+=["Markers/noPic.png"]   #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Icons/" + evoList[0]] #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Icons/" + evoList[1]] #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==3:
        imageList+=["Markers/noPic.png"]   #N
        imageList+=["Markers/noPic.png"]   #O
        imageList+=["Markers/noPic.png"]   #P
        imageList+=["Markers/noPic.png"]   #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Icons/" + evoList[0]] #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Icons/" + evoList[1]] #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Icons/" + evoList[2]] #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==4:
        imageList+=["Markers/noPic.png"]   #N
        imageList+=["Markers/noPic.png"]   #O
        imageList+=["Markers/noPic.png"]   #P
        imageList+=["Markers/noPic.png"]   #Q
        imageList+=["Icons/" + evoList[0]] #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Icons/" + evoList[1]] #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Icons/" + evoList[2]] #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Icons/" + evoList[3]] #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==5:
        imageList+=["Markers/noPic.png"]   #N
        imageList+=["Icons/" + evoList[0]] #O
        imageList+=["Icons/" + evoList[1]] #P
        imageList+=["Markers/noPic.png"]   #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Icons/" + evoList[2]] #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Icons/" + evoList[3]] #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Icons/" + evoList[4]] #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==6:
        imageList+=["Icons/" + evoList[0]] #N
        imageList+=["Icons/" + evoList[1]] #O
        imageList+=["Icons/" + evoList[2]] #P
        imageList+=["Icons/" + evoList[3]] #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Icons/" + evoList[4]] #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Icons/" + evoList[5]] #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==7:
        imageList+=["Icons/" + evoList[0]] #N
        imageList+=["Icons/" + evoList[1]] #O
        imageList+=["Icons/" + evoList[2]] #P
        imageList+=["Icons/" + evoList[3]] #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Markers/noPic.png"]   #R
        imageList+=["Icons/" + evoList[4]] #K
        imageList+=["Markers/noPic.png"]   #S
        imageList+=["Icons/" + evoList[5]] #L
        imageList+=["Markers/noPic.png"]   #T
        imageList+=["Icons/" + evoList[6]] #M
        imageList+=["Markers/noPic.png"]   #U
    elif len(evoList)==8:
        imageList+=["Icons/" + evoList[0]] #N
        imageList+=["Icons/" + evoList[1]] #O
        imageList+=["Icons/" + evoList[2]] #P
        imageList+=["Icons/" + evoList[3]] #Q
        imageList+=["Markers/noPic.png"]   #D
        imageList+=["Markers/noPic.png"]   #A
        imageList+=["Markers/noPic.png"]   #E
        imageList+=["Markers/noPic.png"]   #B
        imageList+=["Markers/noPic.png"]   #F
        imageList+=["Markers/noPic.png"]   #C
        imageList+=["Markers/noPic.png"]   #G
        imageList+=["Icons/" + evoList[4]] #R
        imageList+=["Markers/noPic.png"]   #K
        imageList+=["Icons/" + evoList[5]] #S
        imageList+=["Markers/noPic.png"]   #L
        imageList+=["Icons/" + evoList[6]] #T
        imageList+=["Markers/noPic.png"]   #M
        imageList+=["Icons/" + evoList[7]] #U

    return imageList


def createPokepage(mon, monNames, username, status):

    pageIndex={}
    
    if username==BACKDOOR[0]:
        table="Master"
        status="SABC"
    else:
        table=username + "DEX"
    
    
    pageIndex.update({"Status": status})

    preList=createPreList(mon, monNames, table)
    evoList=createEvoList(mon, monNames, table)
    evolutions=arrangeEvo(preList, evoList)

    nameName=r"Names/" + mon["Name"] + ".png"
    pageIndex.update({"nameName": nameName})

    picName=r"Pics/" + mon["FullName"] + ".png"
    DVVName=r"DVV/" + mon["DVV"] + ".png"
    typeName=r"Types/" + mon["Type"] + ".png"
    pageIndex.update({"picName": picName})
    pageIndex.update({"DVVName": DVVName})
    pageIndex.update({"typeName": typeName})

    indexName=mon["IndexNumber"]
    rankName=mon["Rank"]
    biomeName=mon["Biome"]
    catchDownloadName=r"Symbols/" + mon["Obtainability"] + ".png"
    badgeCrestName=r"Symbols/" + mon["BadgeCrest"] + ".png"
    pageIndex.update({"indexName": indexName})
    pageIndex.update({"rankName": rankName})
    pageIndex.update({"biomeName": biomeName})
    pageIndex.update({"catchDownloadName": catchDownloadName})
    pageIndex.update({"badgeCrestName": badgeCrestName})

    abilityXName=r"Abilities/" + mon["AbilityA"] + ".png"
    move1Name=r"Moves/" + mon["MoveAA"] + ".png"
    move2Name=r"Moves/" + mon["MoveAB"] + ".png"
    abilityYName=r"Abilities/" + mon["AbilityB"] + ".png"
    move3Name=r"Moves/" + mon["MoveBA"] + ".png"
    move4Name=r"Moves/" + mon["MoveBB"] + ".png"
    pageIndex.update({"abilityXName": abilityXName})
    pageIndex.update({"move1Name": move1Name})
    pageIndex.update({"move2Name": move2Name})
    pageIndex.update({"abilityYName": abilityYName})
    pageIndex.update({"move3Name": move3Name})
    pageIndex.update({"move4Name": move4Name})

    leftArrowName=r"Symbols/" + mon["PreEvArrow"] + ".png"
    if len(createEvoList(mon, monNames, table))==0:
        rightArrowName=r"Symbols/" + "0way.png"
    else:
        rightArrowName=r"Symbols/" + index[mon["Ev1"]]["PreEvArrow"] + ".png"
    pageIndex.update({"leftArrowName": leftArrowName})
    pageIndex.update({"rightArrowName": rightArrowName})

    leftEvoName=r"EvoTemplates/" + str(len(createPreList(mon, monNames, table))) + ".png"
    rightEvoName=r"EvoTemplates/" + str(len(createEvoList(mon, monNames, table))) + ".png"
    pageIndex.update({"leftEvoName": leftEvoName})
    pageIndex.update({"rightEvoName": rightEvoName})



    A2Name=evolutions[1]
    B2Name=evolutions[3]
    A3Name=evolutions[0]
    B3Name=evolutions[2]
    C3Name=evolutions[4]
    AName=evolutions[10]
    BName=evolutions[12]
    CName=evolutions[14]
    DName=evolutions[9]
    EName=evolutions[11]
    FName=evolutions[13]
    GName=evolutions[15]
    KName=evolutions[17]
    LName=evolutions[19]
    MName=evolutions[21]
    NName=evolutions[5]
    OName=evolutions[6]
    PName=evolutions[7]
    QName=evolutions[8]
    RName=evolutions[16]
    SName=evolutions[18]
    TName=evolutions[20]
    UName=evolutions[22]
    pageIndex.update({"A2Name": A2Name})
    pageIndex.update({"B2Name": B2Name})
    pageIndex.update({"A3Name": A3Name})
    pageIndex.update({"B3Name": B3Name})
    pageIndex.update({"C3Name": C3Name})
    pageIndex.update({"AName": AName})
    pageIndex.update({"BName": BName})
    pageIndex.update({"CName": CName})
    pageIndex.update({"DName": DName})
    pageIndex.update({"EName": EName})
    pageIndex.update({"FName": FName})
    pageIndex.update({"GName": GName})
    pageIndex.update({"KName": KName})
    pageIndex.update({"LName": LName})
    pageIndex.update({"MName": MName})
    pageIndex.update({"NName": NName})
    pageIndex.update({"OName": OName})
    pageIndex.update({"PName": PName})
    pageIndex.update({"QName": QName})
    pageIndex.update({"RName": RName})
    pageIndex.update({"SName": SName})
    pageIndex.update({"TName": TName})
    pageIndex.update({"UName": UName})

    linkIndex={}    #This if for the hyperlinked images.
    linkIndex.update({"A2Name6-4": A2Name[6:-4]})
    linkIndex.update({"B2Name6-4": B2Name[6:-4]})
    linkIndex.update({"A3Name6-4": A3Name[6:-4]})
    linkIndex.update({"B3Name6-4": B3Name[6:-4]})
    linkIndex.update({"C3Name6-4": C3Name[6:-4]})
    linkIndex.update({"AName6-4": AName[6:-4]})
    linkIndex.update({"BName6-4": BName[6:-4]})
    linkIndex.update({"CName6-4": CName[6:-4]})
    linkIndex.update({"DName6-4": DName[6:-4]})
    linkIndex.update({"EName6-4": EName[6:-4]})
    linkIndex.update({"FName6-4": FName[6:-4]})
    linkIndex.update({"GName6-4": GName[6:-4]})
    linkIndex.update({"KName6-4": KName[6:-4]})
    linkIndex.update({"LName6-4": LName[6:-4]})
    linkIndex.update({"MName6-4": MName[6:-4]})
    linkIndex.update({"NName6-4": NName[6:-4]})
    linkIndex.update({"OName6-4": OName[6:-4]})
    linkIndex.update({"PName6-4": PName[6:-4]})
    linkIndex.update({"QName6-4": QName[6:-4]})
    linkIndex.update({"RName6-4": RName[6:-4]})
    linkIndex.update({"SName6-4": SName[6:-4]})
    linkIndex.update({"TName6-4": TName[6:-4]})
    linkIndex.update({"UName6-4": UName[6:-4]})

    for link in linkIndex:
        if linkIndex[link]=="s/noPic":
            linkIndex[link]=""
        pageIndex.update({link: linkIndex[link]})



    levelXName=str(mon["LvlA"])
    levelYName=str(mon["LvlB"])
    HPName=str(mon["HP"])
    atkName=str(mon["Atk"])
    satkName=str(mon["SAtk"])
    spdName=str(mon["Spd"])
    sdefName=str(mon["SDef"])
    defName=str(mon["Def"])
    pageIndex.update({"levelXName": levelXName})
    pageIndex.update({"levelYName": levelYName})
    pageIndex.update({"HPName": HPName})
    pageIndex.update({"atkName": atkName})
    pageIndex.update({"satkName": satkName})
    pageIndex.update({"spdName": spdName})
    pageIndex.update({"sdefName": sdefName})
    pageIndex.update({"defName": defName})


    abilList=arrangeAbil(mon)
    ability1Name=r"TotalAbilities/" + abilList[0] + ".png"
    ability2Name=r"TotalAbilities/" + abilList[1] + ".png"
    ability3Name=r"TotalAbilities/" + abilList[2] + ".png"
    ability4Name=r"TotalAbilities/" + abilList[3] + ".png"
    pageIndex.update({"ability1Name": ability1Name})
    pageIndex.update({"ability2Name": ability2Name})
    pageIndex.update({"ability3Name": ability3Name})
    pageIndex.update({"ability4Name": ability4Name})

    leftListName=r"MoveLists/" + mon["FullName"] + ".png"
    pageIndex.update({"leftListName": leftListName})

    with open("TMList.txt", "r") as f:
        TMlists=[]
        for line in f:
            TMlists+=[line]
        tempvar=0
        for i in range(len(TMlists)):
            if mon["FullName"]==TMlists[i]:
                tempvar=1
        if tempvar==1:
            rightListName=r"TMLists/" + mon["FullName"] + ".png"
        else:
            rightListName=r"TMLists/" + "None.png"
    pageIndex.update({"rightListName": rightListName})

    abilityBorderName=r"Symbols/Ability Base.png"
    versionXName=r"Symbols/version border.png"
    versionYName=r"Symbols/version border.png"
    pageIndex.update({"abilityBorderName": abilityBorderName})
    pageIndex.update({"versionXName": versionXName})
    pageIndex.update({"versionYName": versionYName})


    pageIndex.update({"FullName": mon["FullName"]})

    return pageIndex
    




if __name__=="__main__":
    for mon in index:
        if mon not in skipMons and (index[mon]["AbilityA"]=="Thermal Mane" or index[mon]["AbilityB"]=="Thermal Mane"):
            print(index[mon]["FullName"])
