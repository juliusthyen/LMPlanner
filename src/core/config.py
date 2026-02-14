
from . import classes
from . import menus

# region Main Loop
def main():

    # Setup
    user = classes.User()
    race = classes.RaceManager("Bahrain Outer", 4, 44, classes.Car("GT3_Lexus", "LMGT3"), None)
    user.races = [race]
    driver1 = classes.Driver("Julius", 66.6)
    driver2 = classes.Driver("Aleks", 67.2)
    race.drivers.append(driver1)
    race.drivers.append(driver2)
    menus.in_race_menu(race)

    # CLI
    # out_race_menu(user)
# endregion

