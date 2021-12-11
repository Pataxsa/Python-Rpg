import os
import socket
import json
from functions.functions import payitem, givemoney, levelup, damage, changeequipeditem, checkequipeditem
from random import randint

def basemenu(data, playerdata):
    clear = lambda: os.system('cls')

    while True:
        print("RPG - by 0BL1V10N (Pataxsa)")
        print()
        print("1- Solo.\n2- Multiplayer.\n3- Inventory.\n4- Shop.\n5- My stats.\n6- Quit the game.")
        print()
        choice = input("Please choice: ")

        clear()

        if choice == "1":
            if playerdata["life"] <= 0:
                print("You can't play because you are dead !")
                input()
                clear()
            else:
                if playerdata["equipeditems"]["weapon"] != {}:
                    monsters = [{"name": "Basic Monster", "baselife": 4, "basedamage": 2}, {"name": "Monster", "baselife": 10, "basedamage": 3}]
                    randm = randint(0, len(monsters)-1)
                    monster = monsters[randm]
                    monsterlife = monster["baselife"] * playerdata["level"]
                    monsterdamage = monster["basedamage"] * playerdata["level"]

                    while True:
                        clear()

                        print("Level - " + str(playerdata["level"]))
                        print()
                        print(playerdata["name"] + " - life: " + str(playerdata["life"]))
                        print(monster["name"] + " - " + "life: " + str(monsterlife) + ", damage: " + str(monsterdamage))
                        print()

                        choice = input("Press Enter to combat !")
                        print(monster["name"] + " has done " + str(monsterdamage) + " damage to you")
                        damage(playerdata, monsterdamage)
                        if playerdata["life"] <= 0:
                            print("You are dead !")
                            input()
                            clear()
                            break
                        print(playerdata["name"] + " used the " + playerdata["equipeditems"]["weapon"]["name"] + " weapon wich caused " + str(playerdata["equipeditems"]["weapon"]["damage"]) + " damage")
                        monsterlife -= playerdata["equipeditems"]["weapon"]["damage"]
                        if monsterlife <= 0:
                            levelup(playerdata)
                            givemoney(playerdata)
                            print()
                            print(monster["name"] + " is dead !")
                            print("You win 100 money (you have now " + str(playerdata["money"]) + " money)")
                            print("You level up ! (you are now level " + str(playerdata["level"]) + ")")
                            input()
                            clear()
                            break
                        input()
                else:
                    print("You can't play because you don't have equiped a weapon !")
                    input()
                    clear()
                    
        elif choice == "2": 
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

            try:
                print("Connecting to the server...")

                clientSocket.connect(("127.0.0.1",9090));
                print("Good !")

                clientSocket.send("Hello Server!".encode());

                dataFromServer = clientSocket.recv(1024);

                my_dict_again = json.loads(dataFromServer.decode())
                print("name: " + my_dict_again["name"] + " price: " + str(my_dict_again["price"]))
                input()
                clear()
            except ConnectionRefusedError:
                print("You have no connexion !")
                input()
                clear()
        elif choice == "3":
            clear()
            print(" - Inventory - ")
            print()
            if len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) > 0:
                print("Weapons - " + str(len([d for d in playerdata["items"] if d['type'] in ["weapon"]])) + ": ")
                for i in [d for d in playerdata["items"] if d['type'] in ["weapon"]]:
                    print(i["name"] + ", " + " damage: " + str(i["damage"]))

            if len([d for d in playerdata["items"] if d['type'] in ["armor"]]) > 0:
                print()
                print("Armors - "+ str(len([d for d in playerdata["items"] if d['type'] in ["armor"]])) + ": ")
                for i in [d for d in playerdata["items"] if d['type'] in ["armor"]]:
                    print(i["name"] + ", " + " damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
            print()
            print("1- Change equiped weapon\n2- Change equiped armor")
            print()
            choice = input("Please choice: ")

            try:
                int(choice)
                if choice == "1":
                    clear()
                    if len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) > 0:
                        for i in [d for d in playerdata["items"] if d['type'] in ["weapon"]]:
                            print(i["name"] + ", " + " damage: " + str(i["damage"]))
                        print()
                        weapon = input("Equip a weapon: ")
                        if checkequipeditem(playerdata, [d for d in playerdata["items"] if d['type'] in ["weapon"]][int(weapon)-1]) == False:
                            clear()
                            changeequipeditem(playerdata, [d for d in playerdata["items"] if d['type'] in ["weapon"]][int(weapon)-1], data)
                            print("Your have equiped a new weapon ! (" + [d for d in playerdata["items"] if d['type'] in ["weapon"]][int(weapon)-1]["name"] + ")")
                            input()
                            clear()
                        else:
                            clear()
                            print("You have already this equiped item !")
                            input()
                            clear()
                    else:
                        clear()
                        print("You don't have any weapons :/")
                        input()
                        clear()
                elif choice == "2":
                    clear()
                    if len([d for d in playerdata["items"] if d['type'] in ["armor"]]) > 0:
                        for i in [d for d in playerdata["items"] if d['type'] in ["armor"]]:
                            print(i["name"] + ", " + " damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
                        print()
                        armor = input("Equip a armor: ")
                        if checkequipeditem(playerdata, [d for d in playerdata["items"] if d['type'] in ["armor"]][int(armor)-1]) == False:
                            clear()
                            changeequipeditem(playerdata, [d for d in playerdata["items"] if d['type'] in ["armor"]][int(armor)-1], data)
                            print("Your have equiped a new armor ! (" + [d for d in playerdata["items"] if d['type'] in ["armor"]][int(armor)-1]["name"] + ")")
                            input()
                            clear()
                        else:
                            clear()
                            print("You have already this equiped item !")
                            input()
                            clear()
                    else:
                        clear()
                        print("You don't have any armors :/")
                        input()
                        clear()
            except:
                clear()
        elif choice == "4":
            clear()
            print(" - Shop - ")
            print()
            print("1- Weapons")
            print("2- Armors")
            print()
            category = input("Choose a category: ")
            clear()

            if category == "1":
                item = [{"name": "Wooden Sword", "type": "weapon", "price": 100, "damage": 4 }, {"name": "Iron Sword", "type": "weapon", "price": 1000, "damage": 10 }, {"name": "Diamond Sword", "type": "weapon", "price": 10000, "damage": 30 }]

                print(" - Weapons - ")
                print()
                for i in item:
                    print("name: " + i["name"] + ", price: " + str(i["price"]) + ", damage: " + str(i["damage"]))
                print()
                choiceitem = input("Choice your weapon: ")

                try:
                    if playerdata["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(playerdata, item[int(choiceitem)-1])
                        print("You have buy " + item[int(choiceitem)-1]["name"] + " for " + str(item[int(choiceitem)-1]["price"]))
                        input()
                        clear()
                    elif playerdata["money"] < item[int(choiceitem)-1]["price"]:
                        clear()
                        print("You can't buy " + item[int(choiceitem)-1]["name"] + " (you have just " + str(playerdata["money"]) + " money)")
                        input()
                        clear()
                except:
                    clear()
            elif category == "2":
                item = [{"name": "Wooden Armor", "type": "armor", "price": 1000, "damagereduction": 0.5 }, {"name": "Iron Armor", "type": "armor", "price": 4000, "damagereduction": 0.6 }, {"name": "Diamond Armor", "type": "armor", "price": 15000, "damagereduction": 0.7 }]

                print(" - Armors - ")
                print()
                for i in item:
                    print(i["name"] + ", price: " + str(i["price"]) + ", damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
                print()
                choiceitem = input("Choose your armor: ")

                try:
                    if playerdata["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(playerdata, item[int(choiceitem)-1])
                        print("You have buy " + item[int(choiceitem)-1]["name"] + " for " + str(item[int(choiceitem)-1]["price"]))
                        input()
                        clear()
                    elif playerdata["money"] < item[int(choiceitem)-1]["price"]:
                        clear()
                        print("You can't buy " + item[int(choiceitem)-1]["name"] + " (you have just " + str(playerdata["money"]) + " money)")
                        input()
                        clear()
                except:
                    clear()

        elif choice == "5":
            clear()
            print(" - Player Stats - ")
            print()
            print("Name: " + str(playerdata["name"]) + "\nPassword: " + str(playerdata["password"]) + "\nMoney: " + str(playerdata["money"]) +"\nLife: " + str(playerdata["life"]))
            print("EquipedItems: ")
            print()
            if playerdata["equipeditems"]["weapon"] != {}:
                print("Weapon: " + playerdata["equipeditems"]["weapon"]["name"] + ", price: " + str(playerdata["equipeditems"]["weapon"]["price"]) + ", damage: " + str(playerdata["equipeditems"]["weapon"]["damage"]))
            else:
                print("Weapon: You don't equiped an weapon !")
            print()
            if playerdata["equipeditems"]["armor"] != {}:
                print("Armor: " + playerdata["equipeditems"]["armor"]["name"] + ", price: " + str(playerdata["equipeditems"]["armor"]["price"]) + ", damagereduction: " + str(playerdata["equipeditems"]["armor"]["damagereduction"]*100).replace(".0", "") + "%")
            else:
                print("Armor: You don't equiped an armor !")
            print("Items: ")
            print()
            print("Weapons - " + str(len([d for d in playerdata["items"] if d['type'] in ["weapon"]])) + ":")
            if len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) > 0:
                for i in [d for d in playerdata["items"] if d['type'] in ["weapon"]]:
                    print(i["name"] + ", price: " + str(i["price"]) + ", damage: " + str(i["damage"]))
            else:
                print("You don't have any weapons :/")
            print()
            print("Armors - " + str(len([d for d in playerdata["items"] if d['type'] in ["armor"]])) + ": ")
            if len([d for d in playerdata["items"] if d['type'] in ["armor"]]) > 0:
                for i in [d for d in playerdata["items"] if d['type'] in ["armor"]]:
                    print(i["name"] + ", price: " + str(i["price"]) + ", damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
            else:
                print("You don't have any armors :/")
            input()
            clear()
        elif choice == "6":
            print("I have leaved the game !")
            break

