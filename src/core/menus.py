# region Menu Functions
def out_race_menu(user):
    while True:
        print("1. Create New Race")
        print("2. Choose Existing Race")
        print("3. Remove Race")
        print("4. Show Races")
        print("5. Type 'Exit' to exit program.")
        user_input = input("What would you like to do?: ")
        match user_input:
            case "1":
                user.create_race()
            case "2":
                user.select_race()
            case "3":
                user.remove_race()
            case "4":
                user.display_races()
            case "Exit":
                return
            case _:
                print("Invalid Input.")

def in_race_menu(race):
    while True:
        print("Options:")
        print("1. Add Driver")
        print("2. Edit Driver")
        print("3. Remove Driver")
        print("4. View Driver Lineup")
        print("5. Assign Drivers")
        print("6. Edit Stints")
        print("7. Display Stints")
        print("Type 'Exit' to exit race.")
        menu_choice = input("What do you want to do?: ")
        match menu_choice:
            case "1":
                race.add_driver()
            case "2":
                race.edit_driver()
            case "3":
                race.remove_driver()
            case "4":
                race.display_drivers()
            case "5":
                race.assign_drivers()
            case "6":
                race.adjust_stints(race)
            case "7":
                race.display_stints()
            case "Exit":
                return
            case _:
                print("Invalid Input.")
# endregion