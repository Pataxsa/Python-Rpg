import os
import json
import uuid

path = os.getenv('APPDATA') + '/PythonRpg/data/players.json'
clear = lambda: os.system('cls')

def checkfiles():
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write('[{"players": []}, {"autoconnect": {}}]')

def initdata():
    try:
        file = open(path, "r")
        jsondata = json.load(file)

        return jsondata
    except:
        with open(path, "w") as f:
            f.write('[{"players": []}, {"autoconnect": {}}]')
        
        return [{"players": []}, {"autoconnect": {}}]

def getautoconnexion(data):
    if data[1]["autoconnect"] == {}:
        return False
    else:
        return data[1]["autoconnect"]

def setautoconnexion(name, data):
    data[1]["autoconnect"] = { "name": name }
    jsondata = json.dumps(data)

    with open(path, 'w+') as f:
        f.write(jsondata)
        f.close()

def createplayer(name, password, data):
    data1 = {
        "name": name,
        "password": password,
        "uuid": str(uuid.uuid4()),
        "life": 100,
        "money": 0,
        "level": 1,
        "equipeditems": {"armor": {}, "weapon": {}}, 
        "items": [{ "name": "Hands", "type": "weapon", "price": 0, "damage": 1 }]
    }

    data[0]["players"].append(data1)

    jsondata = json.dumps(data)

    with open(path, 'w+') as f:
        f.write(jsondata)
        f.close()

def getplayer(name, data):
    if [d for d in data[0]["players"] if d['name'] in [name]] == []:
        return False
    else:
        return [d for d in data[0]["players"] if d['name'] in [name]][0]

def removeplayer(name, data):
    data[0]["players"].remove([d for d in data[0]["players"] if d['name'] in [name]][0])

    jsondata = json.dumps(data)

    with open(path, 'w+') as f:
        f.write(jsondata)
        f.close()

def removeallplayers():
    dat = [{"players": []}, {"autoconnect": {}}]
    jsondata = json.dumps(dat)

    with open(path, 'w+') as f:
        f.write(jsondata)
        f.close()

def payitem(playerdata, itemdata):
    file = open(path, "r")
    jsondata = json.load(file)
    name = playerdata["name"]
    player = [d for d in jsondata[0]["players"] if d['name'] in [name]][0]

    player["money"] -= itemdata["price"]
    player["items"].append(itemdata)
    playerdata["money"] -= itemdata["price"]
    playerdata["items"].append(itemdata)

    jsondat = json.dumps(jsondata)

    with open(path, "w+") as f:
        f.write(jsondat)
        f.close()

def givemoney(playerdata):
    file = open(path, "r")
    jsondata = json.load(file)
    name = playerdata["name"]
    player = [d for d in jsondata[0]["players"] if d['name'] in [name]][0]

    player["money"] += 100
    playerdata["money"] += 100
    jsondat = json.dumps(jsondata)

    with open(path, "w+") as f:
        f.write(jsondat)
        f.close()

def levelup(playerdata):
    file = open(path, "r")
    jsondata = json.load(file)
    name = playerdata["name"]
    player = [d for d in jsondata[0]["players"] if d['name'] in [name]][0]

    player["level"] += 1
    playerdata["level"] += 1
    jsondat = json.dumps(jsondata)

    with open(path, "w+") as f:
        f.write(jsondat)
        f.close()

def damage(playerdata, damage):
    file = open(path, "r")
    jsondata = json.load(file)
    name = playerdata["name"]
    player = [d for d in jsondata[0]["players"] if d['name'] in [name]][0]

    player["life"] -= damage
    playerdata["life"] -= damage

    if player["life"] <= 0 and playerdata["life"] <= 0:
        player["life"] = 0
        playerdata["life"] = 0

    jsondat = json.dumps(jsondata)

    with open(path, "w+") as f:
        f.write(jsondat)
        f.close()

def changeequipeditem(playerdata, itemdata, data):
    playerdata["equipeditems"][itemdata["type"]] = itemdata

    jsondat = json.dumps(data)

    with open(path, "w+") as f:
        f.write(jsondat)
        f.close()

def checkequipeditem(playerdata, itemdata):
    if playerdata["equipeditems"][itemdata["type"]] == itemdata:
        return True
    else:
        return False