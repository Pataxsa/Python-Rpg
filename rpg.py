import os
from functions.functions import createplayer, getplayer, removeplayer, removeallplayers, getautoconnexion, setautoconnexion, checkfiles, initdata
from basemenu import basemenu

clear = lambda: os.system('cls')
data = []

checkfiles()
data = initdata()

while True:
    clear()
    print("RPG - by 0BL1V10N (Pataxsa)")
    print()
    print("1- Create new player.\n2- Choose a player.\n3- Delete a player.\n4- Delete all players.\n5- Auto Connexion.\n6- Quit the game.")
    print()
    
    choice = input("Please choice: ")

    clear()

    if choice == "1":
        print(" - Create a player - ")
        print()
        name = input("Choose your player name: ")
        if getplayer(name, data) == False:
            password = input("Choose your player password: ")
            createplayer(name, password, data)
            clear()
            print("The player " + name + " was created !")
            input()
            clear()
        else:
            clear()
            print("The player with the name " + name + " already exist !")
            input()
            clear()
    elif choice == "2":
        print("Connect your player !")
        print()
        name = input("Enter player name: ")

        if getplayer(name, data) == False:
            clear()
            print("The player " + name + " doesnt exist !")
            input()
            clear()
        else:
            password = input("Enter password: ")
        
            if password == getplayer(name, data)["password"]:
                clear()
                if getautoconnexion(data) != False:
                    if getautoconnexion(data)["name"] != name:
                        toautoconnect = input("Do you want to set this player in the autoconnect ? (Type Yes/No)")
                        if toautoconnect == "Yes":
                            clear()
                            setautoconnexion(name, data)
                            print("The player " + name + " is now in autoconnexion !")
                            input()
                            clear()
                        else:
                            clear()
                else:
                    toautoconnect = input("Do you want to set this player in the autoconnect ? (Type Yes/No)")
                    if toautoconnect == "Yes":
                        clear()
                        setautoconnexion(name, data)
                        print("The player " + name + " is now in autoconnexion !")
                        input()
                        clear()
                    else:
                        clear()
                basemenu(data, getplayer(name, data))
                break
            else:
                clear()
                print("Bad password !")
                input()
                clear()
    elif choice == "3":
        print("Delete a player !")
        print()

        name = input("Enter player name: ")
        if getplayer(name, data) == False:
            clear()
            print("The player " + name + " doesn't exist.")
            input()
            clear()
        else:
            password = input("Enter player password: ")
            if password == getplayer(name, data)["password"]:
                removeplayer(name, data)
                clear()
                print("The player " + name + " was deleted !")
                input()
                clear()
            else:
                clear()
                print("Bad password !")
                input()
                clear()
    elif choice == "4":
        print("Delete all players !")
        print()

        confirmation = input("Do you realy want to delete all players saves ? (Type Yes/No)")
        if confirmation == "Yes":
            removeallplayers()
            data = [{"players": []}, {"autoconnect": {}}]
            clear()
            print("All players was deleted !")
            input()
            clear()
        else:
            clear()
    elif choice == "5":
        if getautoconnexion(data) == False:
            clear()
            print("You don't have set the auto connect player !")
            input()
            clear()
        else:
            basemenu(data, getplayer(getautoconnexion(data)["name"], data))
            break
    elif choice == "6":
        print("I have leaved the game !")
        break
