# Set up global variables, iterables etc.

stints = []
drivers = []



# Define Classes

class Stint:
    def __init__(self, driver):
        self.driver = driver

class Driver:
    def __init__(self, name, lap_time):
        self.name = name
        self.lap_time = lap_time



# Define Functions

def time_seconds_convert(lap_time):
    minutes, minutes_remainder = divmod(lap_time, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return minutes, seconds, seconds_remainder
    
    # Convert using:
    # m, s, ms = time_seconds_convert(SECONDS)
    # Format as follows for m.ss.ms:
    # {m:.0f}.{s:02.0f}.{ms*10:.0f}


def driver_add():
    while True:
        driver = input("What is the drivers name?: (c to go back) ")
        if driver.lower() == "c":
            return
        while True:
            lap_time = input(f"What is {driver}'s lap time in seconds?: (c to go back) ")
            if lap_time.lower() == "c":
                break
            try:
                lap_time = float(lap_time)
            except ValueError:
                print("Invalid Input.")
                continue
            drivers.append(Driver(driver, lap_time))
            m, s, ms = time_seconds_convert(lap_time)
            print(f"Successfully added {driver} with a lap time of {m:.0f}.{s:02.0f}.{ms*10:.0f}")
            break



def driver_edit():
    while True:
        driver_lineup()
        found = False
        driver_edited = input("Which driver do you want to edit?: (c to go back) ")
        if driver_edited.lower() == "c":
            break
        for driver in drivers:
            if driver.name == driver_edited:
                found = True
                while True:
                    lap_time = input("What do you want to set their lap time to in seconds?: (c to go back) ")
                    if lap_time.lower() == "c":
                        break
                    try:
                        lap_time = float(lap_time)
                    except ValueError:
                        print("Invalid Input.")
                        continue
                    while True:
                        m, s, ms = time_seconds_convert(lap_time)
                        match input(f"Are you sure you want to set {driver.name}'s lap time to {m:.0f}.{s:02.0f}.{ms*10:.0f}?: (Y/n) "):
                            case "Y":
                                driver.lap_time = lap_time
                                print(f"Set {driver.name}'s laptime to {m:.0f}.{s:02.0f}.{ms*10:.0f}.")
                                break
                            case "n" | "N":
                                break
                            case _:
                                print("Invalid Input.")
                                continue
                    break
            if not found:
                print("Driver not found.")



def driver_remove():
    driver_lineup()
    while True:
        driver_removed = input("Which driver do you want to remove?: ")
        for driver in drivers:
            if driver.name == driver_removed:
                if input(f"Are you sure you want to remove {driver.name}?: (Y to confirm) ") == "Y":
                    drivers.remove(driver)
                    print(f"Successfully removed {driver.name}.")
                    return
                else:
                    print("Canceled Removing Driver.")
                    return
        else:
            print("Driver not found.")



def driver_lineup():
    for driver in drivers:
        m, s, ms = time_seconds_convert(driver.lap_time)
        print(f"{driver.name:15} - {m:.0f}.{s:02.0f}.{ms*10:.0f}")



def drivers_assign():
    for stint in stints:
        driver_assigned = input(f"Which driver do you want to assign to stint {stints.index(stint) + 1}?: ")
        for driver in drivers:
            if driver.name == driver_assigned:
                stint.driver = driver
                break
        else:
            print("Driver not found.")



def main():

    # CLI

    print("--- Welcome to LMPlanner ---")
    print("")
    print("Step 1: Set Up Driver Lineup")
    print("")
    while True:
        print("Options:")
        print("1. Add Driver")
        print("2. Edit Driver")
        print("3. Remove Driver")
        print("4. View Driver Lineup")
        print("5. Continue to Stint Assignments")
        print("Type 'Exit' to exit.")
        menu_choice = input("What do you want to do?: ")
        match menu_choice:
            case "1":
                driver_add()
            case "2":
                driver_edit()
            case "3":
                driver_remove()
            case "4":
                driver_lineup()
            case "5":
                drivers_assign()
            case "Exit":
                return
            case _:
                print("Invalid Input.")



# Run the Program

if __name__ == "__main__":
    main()