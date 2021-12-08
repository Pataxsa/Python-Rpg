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
            f.write('[{"players": []}, {"autoconnect": []}]')

def getautoconnexion():
    file = open(path, "r")
    jsondat = json.load(file)

    if jsondat[1]["autoconnect"] == []:
        return False
    else:
        return jsondat[1]["autoconnect"][0]

def setautoconnexion(name):
    file = open(path, "r")
    jsondat = json.load(file)
    dat = jsondat

    if dat[1]["autoconnect"] == []:
        dat[1]["autoconnect"].append({"name": name})
        jsondata = json.dumps(dat)

        with open(path, 'w+') as f:
            f.write(jsondata)
            f.close()
            print("The player " + name + " is now in autoconnexion !")
            input()
            clear()
    else:
        dat[1]["autoconnect"].remove(dat[1]["autoconnect"][0])
        dat[1]["autoconnect"].append({"name": name})
        jsondata = json.dumps(dat)

        with open(path, 'w+') as f:
            f.write(jsondata)
            f.close()
            print("The player " + name + " is now in autoconnexion !")
            input()
            clear()

def createplayer(name, password):
    file = open(path, "r")
    jsondat = json.load(file)
    dat = jsondat

    if [d for d in dat[0]["players"] if d['name'] in [name]] == []:
        try:
            file1 = open(path, "r")
            jsondat = json.load(file1)
            dat = jsondat

            data = {
                "name": name,
                "password": password,
                "uuid": str(uuid.uuid4()),
                "life": 100,
                "money": 0,
                "level": 1,
                "items": [{ "name": "Hands", "type": "weapon", "price": 0, "damage": 1 }]
            }

            dat[0]["players"].append(data)

            jsondata = json.dumps(dat)

            with open(path, 'w+') as f:
                f.write(jsondata)
                f.close()
                clear()
                print("The player " + name + " was created !")
                input()
                clear()
        except:
            dat = [{"players": []}, {"autoconnect": []}]

            data = {
                "name": name,
                "password": password,
                "uuid": str(uuid.uuid4()),
                "life": 100,
                "level": 1,
                "items": [{ "name": "Hands", "price": 0, "damage": 1 }]
            }

            dat[0]["players"].append(data)

            jsondata = json.dumps(dat)

            with open(path, 'w+') as f:
                f.write(jsondata)
                f.close()
                clear()
                print("The player " + name + " was created !")
                input()
                clear()
    else:
        clear()
        print("The player with the name " + name + " already exist !")
        input()
        clear()

def getplayer(name):
    file = open(path, 'r')
    jsondata = json.load(file)

    if [d for d in jsondata[0]["players"] if d['name'] in [name]] == []:
        return False
    else:
        return [d for d in jsondata[0]["players"] if d['name'] in [name]][0]

def removeplayer(name):
    file = open(path, "r")
    jsondat = json.load(file)
    dat = jsondat

    if [d for d in dat[0]["players"] if d['name'] in [name]] == []:
        clear()
        print("This player can't be deleted because it doesnt exist !")
        input()
        clear()
    else:
        dat[0]["players"].remove([d for d in dat[0]["players"] if d['name'] in [name]][0])

        jsondata = json.dumps(dat)

        with open(path, 'w+') as f:
            f.write(jsondata)
            f.close()
            clear()
            print("The player " + name + " was deleted !")
            input()
            clear()

def removeallplayers():
    dat = [{"players": []}, {"autoconnect": []}]
    jsondata = json.dumps(dat)

    with open(path, 'w+') as f:
        f.write(jsondata)
        f.close()
        clear()
        print("All players was deleted !")
        input()
        clear()

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