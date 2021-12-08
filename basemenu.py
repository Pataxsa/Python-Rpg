import os
import socket
import json
from functions.functions import payitem, givemoney, levelup, damage
from random import randint

def basemenu(data):
    Active = True
    clear = lambda: os.system('cls')

    while Active:
        print("RPG - by 0BL1V10N (Pataxsa)")
        print()
        print("1- Solo.\n2- Multiplayer.\n3- Inventory.\n4- Shop.\n5- My stats.\n6- Quit the game.")

        choice = input("Please choice: ")

        clear()

        if choice == "1":
            if data["life"] <= 0:
                print("You can't play because you are dead !")
                input()
                clear()
            else:
                monsters = [{"name": "Basic Monster", "baselife": 4, "basedamage": 2}, {"name": "Monster", "baselife": 10, "basedamage": 3}]
                randm = randint(0, len(monsters)-1)
                monster = monsters[randm]
                monsterlife = monster["baselife"] * data["level"]
                monsterdamage = monster["basedamage"] * data["level"]

                while True:
                    clear()

                    print("Level - " + str(data["level"]))
                    print()
                    print(data["name"] + " - life: " + str(data["life"]))
                    print(monster["name"] + " - " + "life: " + str(monsterlife) + ", damage: " + str(monsterdamage))
                    print()

                    itemscount = 0
                    for i in [d for d in data["items"] if d['type'] in ["weapon"]]:
                        itemscount += 1
                        print(str(itemscount) + " - " + i["name"] + ", " + " damage: " + str(i["damage"]))

                    choice = input("Choice your item to fight the monster : ")
                    print(monster["name"] + " has done " + str(monsterdamage) + " damage to you")
                    damage(data, monsterdamage)
                    if data["life"] <= 0:
                        print("You are dead !")
                        input()
                        clear()
                        break
                    print(data["name"] + " used the " + data["items"][int(choice)-1]["name"] + " weapon wich caused " + str(data["items"][int(choice)-1]["damage"]) + " damage")
                    monsterlife -= data["items"][int(choice)-1]["damage"]
                    if monsterlife <= 0:
                        levelup(data)
                        givemoney(data)
                        print()
                        print(monster["name"] + " is dead !")
                        print("You win 100 money (you have now " + str(data["money"]) + " money)")
                        print("You level up ! (you are now level " + str(data["level"]) + ")")
                        input()
                        clear()
                        break
                    input()
        elif choice == "2": 
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

            try:
                print("Connecting to the server...")

                clientSocket.connect(("127.0.0.1",9090));
                print("Good !")

                data = "Hello Server!";

                clientSocket.send(data.encode());

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
            print("Weapons - " + str(len([d for d in data["items"] if d['type'] in ["weapon"]])) + ": ")
            for i in [d for d in data["items"] if d['type'] in ["weapon"]]:
                print(i["name"] + ", " + " damage: " + str(i["damage"]))
            print()
            print("Armors - "+ str(len([d for d in data["items"] if d['type'] in ["armor"]])) + ": ")
            for i in [d for d in data["items"] if d['type'] in ["armor"]]:
                print(i["name"] + ", " + " damagereduction: " + str(i["damagereduction"]*100).replace(".0", "") + "%")
            input()
            clear()
        elif choice == "4":
            clear()
            print("1- Weapons")
            print("2- Armors")
            category = input("Choice a category: ")
            clear()

            if category == "1":
                item = [{"name": "Wooden Sword", "type": "weapon", "price": 100, "damage": 4 }, {"name": "Iron Sword", "type": "weapon", "price": 1000, "damage": 10 }, {"name": "Diamond Sword", "type": "weapon", "price": 10000, "damage": 30 }]

                for i in item:
                    print("name: " + i["name"] + ", price: " + str(i["price"]) + ", damage: " + str(i["damage"]))
                
                choiceitem = input("Choice your weapon: ")

                try:
                    if data["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(data, item[int(choiceitem)-1])
                        print("You have buy " + item[int(choiceitem)-1]["name"] + " for " + str(item[int(choiceitem)-1]["price"]))
                        input()
                        clear()
                    elif data["money"] < item[int(choiceitem)-1]["price"]:
                        clear()
                        print("You can't buy " + item[int(choiceitem)-1]["name"] + " (you have just " + str(data["money"]) + " money)")
                        input()
                        clear()
                except:
                    clear()
            elif category == "2":
                item = [{"name": "Wooden Armor", "type": "armor", "price": 1000, "damagereduction": 0.5 }, {"name": "Iron Armor", "type": "armor", "price": 4000, "damagereduction": 0.6 }, {"name": "Diamond Armor", "type": "armor", "price": 15000, "damagereduction": 0.7 }]

                for i in item:
                    print("name: " + i["name"] + ", price: " + str(i["price"]) + ", damagereduction: " + str(i["damagereduction"]))
                
                choiceitem = input("Choice your armor: ")

                try:
                    if data["money"] >= item[int(choiceitem)-1]["price"]:
                        clear()
                        payitem(data, item[int(choiceitem)-1])
                        print("You have buy " + item[int(choiceitem)-1]["name"] + " for " + str(item[int(choiceitem)-1]["price"]))
                        input()
                        clear()
                    elif data["money"] < item[int(choiceitem)-1]["price"]:
                        clear()
                        print("You can't buy " + item[int(choiceitem)-1]["name"] + " (you have just " + str(data["money"]) + " money)")
                        input()
                        clear()
                except:
                    clear()

        elif choice == "5":
            clear()
            print("Name: " + str(data["name"]) + "\nPassword: " + str(data["password"]) + "\nMoney: " + str(data["money"]) +"\nLife: " + str(data["life"]) + "\nItems: " + str(data["items"]))
            input()
            clear()
        elif choice == "6":
            print("I have leaved the game !")
            Active = False

