import os
import socket
import json
from functions.functions import payitem, givemoney, levelup, damage, changeequipeditem, checkequipeditem, heal
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
                    if playerdata["equipeditems"]["armor"] != {}:
                        monsterlife = monster["baselife"] * playerdata["level"]
                        monsterdamagerl = monster["basedamage"] * playerdata["level"]
                        monsterdamage = int(monsterdamagerl * playerdata["equipeditems"]["armor"]["damagereduction"])
                    else:
                        monsterlife = monster["baselife"] * playerdata["level"]
                        monsterdamage = monster["basedamage"] * playerdata["level"]

                    while True:
                        clear()

                        print("Level - " + str(playerdata["level"]))
                        print()
                        print(playerdata["name"] + " - life: " + str(playerdata["life"]))
                        if playerdata["equipeditems"]["armor"] != {}:
                            print(monster["name"] + " - " + "life: " + str(monsterlife) + ", damage: " + str(monsterdamagerl) + "-" + str(monsterdamagerl - monsterdamage) + " (" + str(monsterdamage) + ")")
                        else:
                            print(monster["name"] + " - " + "life: " + str(monsterlife) + ", damage: " + str(monsterdamage))
                        print()

                        choice = input("Press Enter to combat !")
                        print(monster["name"] + " has done " + str(monsterdamage) + " damage to you")
                        damage(playerdata, monsterdamage, data)
                        if playerdata["life"] <= 0:
                            print("You are dead !")
                            input()
                            clear()
                            break
                        print(playerdata["name"] + " used the " + playerdata["equipeditems"]["weapon"]["name"] + " weapon wich caused " + str(playerdata["equipeditems"]["weapon"]["damage"]) + " damage")
                        monsterlife -= playerdata["equipeditems"]["weapon"]["damage"]
                        if monsterlife <= 0:
                            levelup(playerdata, data)
                            givemoney(playerdata, data)
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
            items = []
            clear()
            print(" - Inventory - ")
            print()
            if len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) > 0:
                print("Weapons - " + str(len([d for d in playerdata["items"] if d['type'] in ["weapon"]])) + ": ")
                count = 0
                for i in [d for d in playerdata["items"] if d['type'] in ["weapon"]]:
                    count += 1
                    items.append(i)
                    print(str(count) + "- " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", damage: " + str(i["damage"]))
                print()

            if len([d for d in playerdata["items"] if d['type'] in ["armor"]]) > 0:
                print("Armors - "+ str(len([d for d in playerdata["items"] if d['type'] in ["armor"]])) + ": ")
                count = len([d for d in playerdata["items"] if d['type'] in ["weapon"]])
                for i in [d for d in playerdata["items"] if d['type'] in ["armor"]]:
                    count += 1
                    items.append(i)
                    print(str(count) + "- " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
                print()

            if len([d for d in playerdata["items"] if d['type'] in ["consumable"]]) > 0:
                print("Consumables - "+ str(len([d for d in playerdata["items"] if d['type'] in ["consumable"]])) + ": ")
                count = len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) + len([d for d in playerdata["items"] if d['type'] in ["armor"]])
                for i in [d for d in playerdata["items"] if d['type'] in ["consumable"]]:
                    count += 1
                    items.append(i)
                    print(str(count) + "- " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", heal: " + str(i["heal"]))
                print()

            try:
                choice1 = int(input("Please choice: "))
                clear()
                print("Item - " + items[choice1-1]["name"])
                print()
                if items[choice1-1]["type"] == "weapon":
                    print("1- Equip Weapon\n2- Weapon Stats")
                    print()
                    choice2 = int(input("Please choice: "))
                    if choice2 == 1:
                        if checkequipeditem(playerdata, items[choice1-1]) == False:
                            clear()
                            changeequipeditem(playerdata, items[choice1-1], data)
                            print("Your have equiped a new weapon ! (" + items[choice1-1]["name"] + ")")
                            input()
                            clear()
                        else:
                            clear()
                            print("You have already this equiped item !")
                            input()
                            clear()
                    elif choice2 == 2:
                        clear()
                        print("Name: " + items[choice1-1]["name"] + "\nPrice: " + str(items[choice1-1]["price"]) + "\nRarity: " + items[choice1-1]["rarity"] + "\nDamage: " + str(items[choice1-1]["damage"]))
                        input()
                        clear()
                elif items[choice1-1]["type"] == "armor":
                    print("1- Equip Armor\n2- Armor Stats")
                    print()
                    choice2 = int(input("Please choice: "))
                    if choice2 == 1:
                        if checkequipeditem(playerdata, items[choice1-1]) == False:
                            clear()
                            changeequipeditem(playerdata, items[choice1-1], data)
                            print("Your have equiped a new armor ! (" + items[choice1-1]["name"] + ")")
                            input()
                            clear()
                        else:
                            clear()
                            print("You have already this equiped item !")
                            input()
                            clear()
                    if choice2 == 2:
                        clear()
                        print("Name: " + items[choice1-1]["name"] + "\nPrice: " + str(items[choice1-1]["price"]) + "\nRarity: " + items[choice1-1]["rarity"] + "\nDamagereduction: " + str(items[choice1-1]["damagereduction"]*100).replace("0.", "") + "%")
                        input()
                        clear()
                elif items[choice1-1]["type"] == "consumable":
                    print("1- Consume\n2- Consumable Stats")
                    print()
                    choice2 = int(input("Please choice: "))
                    if choice2 == 1:
                        if playerdata["life"] < 100:
                            clear()
                            heal(playerdata, items[choice1-1], data)
                            print("You are healed by " + str(items[choice1-1]["heal"])  + " ! (you have now " + str(playerdata["life"]) + ")")
                            input()
                            clear()
                        else:
                            clear()
                            print("You have the maximum life !")
                            input()
                            clear()
                    if choice2 == 2:
                        clear()
                        print("Name: " + items[choice1-1]["name"] + "\nPrice: " + str(items[choice1-1]["price"]) + "\nRarity: " + items[choice1-1]["rarity"] + "\nHeal: " + str(items[choice1-1]["heal"]))
                        input()
                        clear()
            except:
                clear()
        elif choice == "4":
            clear()
            print(" - Shop - ")
            print()
            print("1- Weapons\n2- Armors\n3- Consumables")
            print()
            category = input("Choose a category: ")
            clear()

            if category == "1":
                item = [{"name": "Wooden Sword", "type": "weapon", "price": 100, "rarity": "Common", "damage": 4 }, {"name": "Iron Sword", "type": "weapon", "price": 1000, "rarity": "Uncommon", "damage": 10 }, {"name": "Diamond Sword", "type": "weapon", "price": 10000, "rarity": "Rare", "damage": 30 }]

                print(" - Weapons - ")
                print()
                for i in item:
                    print("name: " + i["name"] + ", price: " + str(i["price"]) + ", rarity: " + i["rarity"] + ", damage: " + str(i["damage"]))
                print()
                choiceitem = input("Choice your weapon: ")

                try:
                    if playerdata["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(playerdata, item[int(choiceitem)-1], data)
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
                item = [{"name": "Wooden Armor", "type": "armor", "price": 1000, "rarity": "Common", "damagereduction": 0.5 }, {"name": "Iron Armor", "type": "armor", "price": 4000, "rarity": "Uncommon", "damagereduction": 0.6 }, {"name": "Diamond Armor", "type": "armor", "price": 15000, "rarity": "Rare", "damagereduction": 0.7 }]

                print(" - Armors - ")
                print()
                for i in item:
                    print(i["name"] + ", price: " + str(i["price"]) + ", rarity: " + i["rarity"] + ", damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
                print()
                choiceitem = input("Choose your armor: ")

                try:
                    if playerdata["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(playerdata, item[int(choiceitem)-1], data)
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
            elif category == "3":
                item = [{"name": "Apple", "type": "consumable", "price": 50, "rarity": "Common", "heal": 30}, {"name": "Healing Potion", "type": "consumable", "price": 100, "rarity": "Common", "heal": 60}, {"name": "Big Healing Potion", "type": "consumable", "price": 300, "rarity": "Uncommon", "heal": 100}]

                print(" - Consumables - ")
                print()
                for i in item:
                    print(i["name"] + ", price: " + str(i["price"]) + ", rarity: " + i["rarity"] + ", heal: " + str(i["heal"]))
                print()
                choiceitem = input("Choice a consumable: ")

                try:
                    if playerdata["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(playerdata, item[int(choiceitem)-1], data)
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
            print("Name: " + str(playerdata["name"]) + "\nPassword: " + str(playerdata["password"]) + "\nLevel: " + str(playerdata["level"]) + "\nMoney: " + str(playerdata["money"]) +"\nLife: " + str(playerdata["life"]))
            print("EquipedItems: ")
            print()
            if playerdata["equipeditems"]["weapon"] != {}:
                print("Weapon: " + playerdata["equipeditems"]["weapon"]["name"] + ", price: " + str(playerdata["equipeditems"]["weapon"]["price"]) + ", Rarity: " + playerdata["equipeditems"]["weapon"]["rarity"] + ", damage: " + str(playerdata["equipeditems"]["weapon"]["damage"]))
            else:
                print("Weapon: You don't equiped an weapon !")
            print()
            if playerdata["equipeditems"]["armor"] != {}:
                print("Armor: " + playerdata["equipeditems"]["armor"]["name"] + ", price: " + str(playerdata["equipeditems"]["armor"]["price"]) + ", Rarity: " + playerdata["equipeditems"]["armor"]["rarity"] + ", damagereduction: " + str(playerdata["equipeditems"]["armor"]["damagereduction"]*100).replace(".0", "") + "%")
            else:
                print("Armor: You don't equiped an armor !")
            print("Items: ")
            if len([d for d in playerdata["items"] if d['type'] in ["weapon"]]) > 0:
                print("Weapons - " + str(len([d for d in playerdata["items"] if d['type'] in ["weapon"]])) + ":")
                for i in [d for d in playerdata["items"] if d['type'] in ["weapon"]]:
                    print("Name: " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", Damage: " + str(i["damage"]))
                print()
            if len([d for d in playerdata["items"] if d['type'] in ["armor"]]) > 0:
                print("Armors - " + str(len([d for d in playerdata["items"] if d['type'] in ["armor"]])) + ": ")
                for i in [d for d in playerdata["items"] if d['type'] in ["armor"]]:
                    print("Name: " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", Damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
                print()
            if len([d for d in playerdata["items"] if d['type'] in ["consumable"]]) > 0:
                print("Consumables - " + str(len([d for d in playerdata["items"] if d['type'] in ["consumable"]])) + ": ")
                for i in [d for d in playerdata["items"] if d['type'] in ["consumable"]]:
                    print("Name: " + i["name"] + ", Price: " + str(i["price"]) + ", Rarity: " + i["rarity"] + ", Heal: " + str(i["heal"]))
            input()
            clear()
        elif choice == "6":
            print("I have leaved the game !")
            break

