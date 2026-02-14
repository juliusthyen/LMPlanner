
# region Classes
class Stint:
    def __init__(self, driver, actual_laps, race):
        self.driver = driver
        self.race = race
        self.actual_laps = actual_laps

    @property
    def pitstop_time(self):
        return 0

    @property
    def is_last_stint(self):
        index = self.race.stints.index(self)
        try:
            if self.race.stints[index + 1].start_time > self.race.duration:
                return True
            else:
                return False
        except IndexError:
            return True

    @property
    def duration(self):
        return self.lap_time * self.laps + self.pitstop_time
    @property
    def lap_time(self):
        if self.driver is None:
            return sum(driver.lap_time for driver in self.race.drivers) / len(self.race.drivers)
        else:
            return self.driver.lap_time
    @property
    def laps(self):
        if self.actual_laps is None:
            return self.race.expected_laps_per_stint
        else:
            return self.actual_laps
    @property
    def driver_name(self):
        if self.driver is None:
            return "Unassigned"
        else:
            return self.driver.name

    @property
    def out_lap(self):
        index = self.race.stints.index(self)
        return round(sum(stint.laps for stint in self.race.stints[:index]) + 1, 1)

    @property
    def in_lap(self):
        index = self.race.stints.index(self)
        return sum(stint.laps for stint in self.race.stints[:index + 1])

    @property
    def start_time(self):
        index = self.race.stints.index(self)
        return sum(stint.duration for stint in self.race.stints[:index])

class Driver:
    def __init__(self, name, lap_time):
        self.name = name
        self.lap_time = lap_time

class User:
    def __init__(self):
        self.races = []

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
            duration = get_valid_float(user_input * 3600)
            user_input = input("How many laps per stint do you expect?: (c to cancel, b to go back) ")
            if user_input == "c":
                return
            if user_input == "b":
                continue
            laps_per_stint = get_valid_int(user_input)
            race = RaceManager(name, duration, laps_per_stint, None, None)
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

class RaceManager:
    def __init__(self, name, duration, expected_laps_per_stint, car, track):
        self.drivers = []
        self.stints = []
        self.users = []
        self.name = name
        self.duration = duration * 3600
        self.expected_laps_per_stint = expected_laps_per_stint
        self.car = car
        self.track = track

    # region Methods
    # region Drivers
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
                m, s, ms = convert_seconds_to_minutes_time(lap_time)
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
                        m, s, ms = convert_seconds_to_minutes_time(lap_time)
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
            m, s, ms = convert_seconds_to_minutes_time(driver.lap_time)
            print(f"{driver.name:15} - {m:.0f}.{s:02.0f}.{ms*10:.0f}")
    # endregion

    # region Stints
    def display_stints(self):
        if not self.drivers:
            print("Add at least one driver.")
            return
        self.update_stints()
        for stint in self.stints:
            h, m, s, ms = convert_seconds_to_hours_time(stint.start_time)
            print(f"{self.stints.index(stint) + 1:4} - Out: {stint.out_lap:3}, In: {stint.in_lap:3} - {stint.driver_name:15} - {h:02.0f}:{m:02.0f} - laps: {stint.laps} - duration: {stint.duration} - {stint.lap_time} - {stint.is_last_stint}")

    def update_stints(self):
        while sum(stint.duration for stint in self.stints) < self.duration:
            new_stint = Stint(None, None, self)
            self.stints.append(new_stint)

    def adjust_stints(self):
        pass

    def assign_drivers(self):
        self.update_stints()
        for stint in self.stints:
            if not stint.driver:
                status = ""
            else:
                status = f"(Current driver: ({stint.driver}))"
            while True:
                found = False
                user_input = input(f"{status} Which driver do you want to assign to stint {self.stints.index(stint) + 1}?: (c to cancel, s to skip, leave empty to unassign) ")
                if user_input == "c":
                    self.display_stints()
                    return
                if user_input == "s":
                    break
                if user_input == "":
                    stint.driver = None
                    continue
                assigned_driver = user_input
                for driver in self.drivers:
                    if driver.name == assigned_driver:
                        found = True
                        stint.driver = driver
                        print(f"Successfully assigned {driver.name}")
                if not found:
                    print("Driver not found.")
                break
        self.display_stints()
    # endregion
    # endregion
# endregion

# region Helper Functions:

def convert_seconds_to_minutes_time(lap_time):
    minutes, minutes_remainder = divmod(lap_time, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return minutes, seconds, seconds_remainder
    # Convert using:
    # m, s, ms = convert_seconds_to_minutes_time(SECONDS)
    # Format as follows for m.ss.ms:
    # {m:.0f}.{s:02.0f}.{ms*10:.0f}

def convert_seconds_to_hours_time(lap_time):
    hours, hours_remainder = divmod(lap_time, 3600)
    minutes, minutes_remainder = divmod(hours_remainder, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return hours, minutes, seconds, seconds_remainder
    # Convert using:
    # m, s, ms = convert_seconds_to_minutes_time(SECONDS)
    # Format as follows for m.ss.ms:
    # {h:02.0f}:{m:02.0f}.{s:02.0f},{ms*10:.0f}

def get_valid_float(inp):
    try:
        inp = float(inp)
    except ValueError:
        print("Invalid Input.")
        return None
    return inp

def get_valid_int(inp):
    try:
        inp = int(inp)
    except ValueError:
        print("Invalid Input.")
        return None
    return inp

def get_user_confirmation():
    pass
# endregion

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

# region Main Loop
def main():

    # Setup
    user = User()
    race = RaceManager("Bahrain Outer", 4, 44, None, None)
    user.races = [race]
    driver1 = Driver("Julius", 66.6)
    driver2 = Driver("Aleks", 67.2)
    race.drivers.append(driver1)
    race.drivers.append(driver2)
    in_race_menu(race)

    # CLI
    # out_race_menu(user)
# endregion

# region Run the Program
if __name__ == "__main__":
    main()
# endregion