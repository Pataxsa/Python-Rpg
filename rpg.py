import os
from functions.functions import createplayer, getplayer, removeplayer, removeallplayers, getautoconnexion, setautoconnexion, checkfiles
from basemenu import basemenu

Active = True
clear = lambda: os.system('cls')

checkfiles()

while Active:
    print("RPG - by 0BL1V10N (Pataxsa)")
    print()
    print("1- Create new player.\n2- Choose a player.\n3- Delete a player.\n4- Delete all players.\n5- Auto Connexion.\n6- Quit the game.")

    choice = input("Please choice: ")

    clear()

    if choice == "1":
        print("Create your player !")
        print()
        name = input("Choose your name: ")
        password = input("Choose your password: ")
        createplayer(name, password)
    elif choice == "2":
        print("Connect your player !")
        print()
        name = input("Enter player name: ")

        if getplayer(name) == False:
            clear()
            print("The player " + name + " doesnt exist !")
            input()
            clear()
        else:
            password = input("Enter password: ")
        
            if password == getplayer(name)["password"]:
                clear()
                toautoconnect = input("Do you want to set this player in the autoconnect ? (Type Yes/No)")
                if toautoconnect == "Yes":
                    clear()
                    setautoconnexion(name)
                else:
                    clear()
                basemenu(getplayer(name))
                Active = False
            else:
                clear()
                print("Bad password !")
                input()
                clear()
    elif choice == "3":
        print("Delete a player !")
        print()

        name = input("Enter player name: ")
        password = input("Enter player password: ")
        if getplayer(name) == False:
            clear()
            print("The player " + name + " doesn't exist.")
            input()
            clear()
        elif password == getplayer(name)["password"]:
            removeplayer(name)
        else:
            print("Invalid password !")
    elif choice == "4":
        print("Delete all players !")
        print()

        confirmation = input("Do you realy want to delete all players saves ? (Type Yes/No)")
        if confirmation == "Yes":
            removeallplayers()
        else:
            clear()
    elif choice == "5":
        if getautoconnexion() == False:
            print("You don't have set the auto connect player !")
        else:
            basemenu(getplayer(getautoconnexion()["name"]))
            Active = False
    elif choice == "6":
        print("I have leaved the game !")
        Active = False