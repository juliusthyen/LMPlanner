
# Classes

class Stint:
    def __init__(self, driver):
        self.driver = driver

class Driver:
    def __init__(self, name, lap_time):
        self.name = name
        self.lap_time = lap_time

# User class

class User:
    def __init__(self):
        self.races = []

    # Define Methods

    def create_race(self):
        while True:
            user_input = input("What do you want to name the race?: (c to cancel) ")
            if user_input == "c":
                return
            name = user_input
            user_input = input("How long is the race in hours?: (c to cancel, b to go back) ")
            if user_input == "c":
                return
            if user_input == "b":
                continue
            duration = float(user_input) * 3600
            race = RaceManager(name, duration)
            race.users.append(self)
            self.races.append(race)

    def select_race(self):
        while True:
            found = False
            self.display_races()
            user_input = input("Which race do you want to select?: (c to go cancel) ")
            if user_input == "c":
                print("Canceled choosing race.")
                return
            target_race = user_input
            for race in self.races:
                if race.name == target_race:
                    found = True
                    in_race_menu(race)
            if not found:
                print("Race not found.")

    def remove_race(self):
        while True:
            self.display_races()
            user_input = input("Which race do you want to remove?: (c to cancel) ")
            if user_input == "c":
                return
            target_race = user_input
            for race in self.races:
                if race.name == target_race:
                    if input(f"Are you sure you want to remove {race.name}?: (Y to confirm) ") == "Y":
                        self.races.remove(race)
                        print(f"Successfully removed {race.name}.")
                        return
                    else:
                        print("Canceled Removing Race.")
                        return
            print("Race not found.")

    def display_races(self):
        for race in self.races:
            print(f"- {race.name}")


# Manager class

class RaceManager:
    def __init__(self, name, duration):
        self.drivers = []
        self.stints = []
        self.users = []
        self.name = name
        self.duration = duration

    # Define Methods

    def add_driver(self):
        while True:
            user_input = input("What is the drivers name?: (c to cancel) ")
            if user_input == "c":
                print("Canceled adding driver.")
                return
            driver = user_input
            while True:
                user_input = input(f"What is {driver}'s lap time in seconds?: (c to cancel, b to go back) ")
                if user_input == "c":
                    print("Canceled adding driver.")
                    return
                if user_input == "b":
                    break
                lap_time = get_valid_float(user_input)
                if lap_time is None:
                    continue
                self.drivers.append(Driver(driver, lap_time))
                m, s, ms = convert_seconds_to_time(lap_time)
                print(f"Successfully added {driver} with a lap time of {m:.0f}.{s:02.0f}.{ms*10:.0f}")
                break

    def edit_driver(self):
        while True:
            self.display_drivers()
            found = False
            user_input = input("Which driver do you want to edit?: (c to go cancel) ")
            if user_input == "c":
                print("Canceled editing driver.")
                return
            target_name = user_input
            for driver in self.drivers:
                if driver.name == target_name:
                    found = True
                    while True:
                        user_input = input("What do you want to set their lap time to in seconds?: (c to cancel, b to go back) ")
                        if user_input == "c":
                            print("Canceled editing driver.")
                            return
                        if user_input == "b":
                            break
                        lap_time = get_valid_float(user_input)
                        if lap_time is None:
                            continue
                        m, s, ms = convert_seconds_to_time(lap_time)
                        driver.lap_time = lap_time
                        print(f"Set {driver.name}'s laptime to {m:.0f}.{s:02.0f}.{ms*10:.0f}.")
                        break
            if not found:
                print("Driver not found.")

    def remove_driver(self):
        while True:
            self.display_drivers()
            user_input = input("Which driver do you want to remove?: (c to cancel) ")
            if user_input == "c":
                print("Canceled removing driver.")
                return
            target_name = user_input
            for driver in self.drivers:
                if driver.name == target_name:
                    if input(f"Are you sure you want to remove {driver.name}?: (Y to confirm) ") == "Y":
                        self.drivers.remove(driver)
                        print(f"Successfully removed {driver.name}.")
                        return
                    else:
                        print("Canceled Removing Driver.")
                        return
            print("Driver not found.")

    def display_drivers(self):
        for driver in self.drivers:
            m, s, ms = convert_seconds_to_time(driver.lap_time)
            print(f"{driver.name:15} - {m:.0f}.{s:02.0f}.{ms*10:.0f}")

    def assign_driver(self):
        pass
        # for stint in self.stints:
        #     driver_assigned = input(f"Which driver do you want to assign to stint {self.stints.index(stint) + 1}?: ")
        #     for driver in self.drivers:
        #         if driver.name == driver_assigned:
        #             stint.driver = driver
        #             break
        #     else:
        #         print("Driver not found.")

# Helper Functions:

def convert_seconds_to_time(lap_time):
    minutes, minutes_remainder = divmod(lap_time, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return minutes, seconds, seconds_remainder

    # Convert using:
    # m, s, ms = convert_seconds_to_time(SECONDS)
    # Format as follows for m.ss.ms:
    # {m:.0f}.{s:02.0f}.{ms*10:.0f}

def get_valid_float(inp):
    try:
        inp = float(inp)
    except ValueError:
        print("Invalid Input.")
        return None
    return inp

def get_user_confirmation():
    pass

# Global Functions

# Menu Functions

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
        print("5. Continue to Stint Assignments")
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
                race.assign_driver()
            case "Exit":
                return
            case _:
                print("Invalid Input.")

# Main Loop

def main():

    # Setup

    user = User()

    # CLI

    out_race_menu(user)

    #
    # print("--- Welcome to LMPlanner ---")
    # print("")
    # print("Step 1: Set Up Driver Lineup")
    # print("")

# Run the Program

if __name__ == "__main__":
    main()