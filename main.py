from general_imports import *
from booking import *
from driver_report import *

menu_opts = {
    "1": ("Rider Details", register_rider),
    "2": ("Book Ride", book_ride),
    "3": ("Calculate Fare", calc_fare),
    "4": ("Calculate Driver's Tip", get_driver_tip),
    "5": ("View Ride Details", show_ride_details),
    "6": ("Change Rates", change_rates),
    "7": ("Driver Report", show_driver_report)
}

if __name__ == "__main__":

    while True:
        print('''\t\t\033[1mByte Ride\033[0m
The Only Transport Service You Can Trust\n''')

        for opt in menu_opts:
            print(f'{opt}: {menu_opts[opt][0]}')
        user_choice = input('Select an option 1 to 7: ')
        try:
            run_opt = menu_opts[user_choice][1]
        except KeyError:
            clear()
            input('''Can only select options 1 to 7
    Press ENTER to try again...''')
            clear()
        else:
            run_opt()
