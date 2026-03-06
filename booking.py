from general_imports import *
from rates import *
from driver_report import driver_stats
from datetime import *
from tabulate import tabulate
from itertools import islice
import re

# Initialize the details of the rider
rider_details = {
    "Name": "",
    "Surname": "",
    "Email": "",
}

# Initialize the booking details
booking_details = {
    "Where From": "",
    "Where To": "",
    "Distance in km": "",
    "Ride Option": "",
    "Payment Choice": ""
}

# Initialize the booking fee
booking_fee = 15


# Store the ride options and their fees
ride_fees = {
    "Cheap": 10,
    "Comfort": 15,
    "Luxury": 20
}

# Initialize the ride's total fee and the driver's tip
driver_tip = 0
total_fee = 0


# Function to reset the rider details and booking details
def reset_details() -> None:
    for rd in rider_details:
        rider_details[rd] = ""
    for bd in booking_details:
        booking_details[bd] = ""


# Function to get the rider's details
def register_rider():
    clear()
    rr()

    email_pattern = '[a-zA-Z0-9]+@[a-zA-z]+\.(com)'
    for i, det in enumerate(rider_details):
        while not rider_details[det]:
            if i == 2:
                print('Email format: example@gmail.com')
                user_email = input(f'Enter your {det}: ').strip()
                if re.match(email_pattern, user_email):
                    rider_details["Email"] = user_email
                else:
                    clear()
                    print('Please enter a valid email following the format.\n')
            else:
                rider_details[det] = input(f'Enter your {det}: ').strip()
    clear()


# Function to book a ride
def book_ride():
    clear()
    br()

    ride_types = ("Cheap", "Comfort", "Luxury")
    payment_options = ("Cash", "Card")

    if rr.not_called:
        input('''Please register your details before booking a ride.
    Press ENTER to return to menu''')
        clear()
    else:
        reset_details()
        # Function to convert input to input and check for error

        def convert_to_int(k, bkdet, num_input):
            if k == 2:
                try:
                    booking_details[bkdet] = float(num_input)
                except ValueError:
                    print('Please enter a valid distance in km.\n')
                return None
            else:
                try:
                    converted = int(num_input)
                except ValueError:
                    clear()
                    print('Please enter a valid digit.\n')
                    return None
                else:
                    if k == 3:
                        try:
                            booking_details[bkdet] = ride_types[converted - 1]
                        except IndexError:
                            clear()
                            print(
                                'Invalid. Choose from the available ride options.\n')
                    else:
                        try:
                            booking_details[bkdet] = payment_options[converted - 1]
                        except IndexError:
                            clear()
                            print('Invalid. Choose between cash or card.\n')

        # Get the booking time
        global ct, eta
        strfct = datetime.today().strftime("%H:%M:%S")
        h, m, s = [int(t) for t in strfct.split(":")]
        ct = timedelta(hours=h, minutes=m, seconds=s)

        for k, bkdet in enumerate(booking_details):
            clear()
            while not booking_details[bkdet]:
                if k == 2:
                    num_input = input(f'{bkdet}: ').strip()
                    convert_to_int(k, bkdet, num_input)
                elif k == 3:
                    for num, ride in enumerate(ride_types):
                        print(f'{num + 1}: {ride}')
                    num_input = input(f'{bkdet}: ').strip()
                    convert_to_int(k, bkdet, num_input)
                elif k == 4:
                    for nbr, payment in enumerate(payment_options):
                        print(f'{nbr + 1}: {payment}')
                    num_input = input(f'{bkdet}: ').strip()
                    convert_to_int(k, bkdet, num_input)
                else:
                    booking_details[bkdet] = input(f'{bkdet}: ').strip()
        # Get the estimated time of arrival (assuming driver is traveling 55km/h)
        ride_duration = booking_details["Distance in km"] / 55
        arrival = ct + timedelta(hours=ride_duration)
        # In case ride duration is longer than 24 hours
        eta = timedelta(seconds=arrival.seconds)

        # Update the driver stats
        driver_stats["Rides"][0] += 1
        driver_stats["Total km"][0] += booking_details["Distance in km"]

        # Display the ride details
        clear()
        show_ride_details()


# Funciton to check if the booking time or ct are in peak hours
def is_in_peak(delta_t):
    peak_hrs1 = (timedelta(hours=7, minutes=30), timedelta(hours=9))
    peak_hrs2 = (timedelta(hours=16, minutes=30), timedelta(hours=18))
    if (peak_hrs1[0] < delta_t < peak_hrs1[1]) or (peak_hrs2[0] < delta_t < peak_hrs2[1]):
        return True
    else:
        return False


# Function to tabulate the booking fees and rates
def tabulate_fees_and_rates(rate_fees: dict):
    fees_and_rates = [
        ["Booking Fee", booking_fee],
        [f"Ride Option Fee ({booking_details['Ride Option']})",
         ride_fees[booking_details["Ride Option"]]],
    ]

    for rate_fee in islice(list(rate_fees.items()), 4):
        fee = list(rate_fee)
        if fee[1] == "":
            continue
        if fee[0] == "Base Fee":
            fees_and_rates.insert(0, fee)
        else:
            fees_and_rates.append(fee)

    # Initialize the headers for the table
    headings = ["Fees & Rates", "Amount (R)"]

    print(f'''\tYour Booking Details:
{tabulate(fees_and_rates, headings, tablefmt="orgtbl")}
Total Before Tip: R{total_fee}''')

# Function to calculate the fare price


def calc_fare():
    clear()
    if br.not_called:
        input('''Cannot calculate a fare if no ride is booked.\n
    Press ENTER to retun to menu...''')
        clear()
    else:
        cf()

        # Get the rates
        file_path = "C:/Users/hloni/Ride Hailing (Group 8)/rates.json"
        with open(file_path, "r") as file:
            opened_rates = json.load(file)

        # Get the distance fee (charged per kilometer)
        distance_fee = (
            booking_details["Distance in km"]) * opened_rates["2"][1]

        # Get the fees before adding the rates
        base_fee = opened_rates["1"][1] + \
            ride_fees[booking_details["Ride Option"]] + \
            booking_fee

        # To get amounts paid on rates
        rate_fees = {
            "Base Fee": opened_rates["1"][1],
            "Distance Fee": distance_fee,
            "Peak Rate Fee": "",
            "Vat Amount": "",
            "Total Fee": ""
        }

        # Calculate the total fee
        global peak_rate_fee, vat_amount, total_fee
        if (is_in_peak(ct)) or is_in_peak(eta):
            peak_rate_fee = (base_fee * opened_rates["3"][1])
            vat_amount = round((base_fee + peak_rate_fee)
                               * opened_rates["4"][1], 2)
            total_fee = round(
                distance_fee + base_fee + peak_rate_fee + vat_amount, 2)
            rate_fees["Peak Rate Fee"] = peak_rate_fee
            driver_stats["Peak Income"][0] += total_fee
        else:
            vat_amount = round(base_fee * opened_rates["4"][1], 2)
            total_fee = round(distance_fee + base_fee + vat_amount, 2)
            driver_stats["Income Non-Peak"][0] += total_fee
        rate_fees["Vat Amount"] = vat_amount
        rate_fees["Total Fee"] = total_fee

        # Update the driver stats
        driver_stats["Total Income"][0] += total_fee
        if booking_details["Ride Option"] == "Cash":
            driver_stats["Cash Income"][0] += total_fee
        else:
            driver_stats["Card Income"][0] += total_fee

        # Display the booking bill
        input(f'''{tabulate_fees_and_rates(rate_fees)}\n
    Press ENTER to return to menu...''')
        clear()

# Function to get the driver's tip


def get_driver_tip():
    clear()
    if (br.not_called) or (cf.not_called):
        input('''Cannot tip driver unless ride is booked and fare is calculated.
    Press ENTER to return to menu...''')
        clear()
    else:
        while True:
            try:
                global driver_tip, total_fee
                driver_tip = int(input('Tip Driver: R'))
            except ValueError:
                clear()
                print("Please enter a valid number to tip driver.\n")
            else:
                total_fee += driver_tip
                clear()
                break

        # Update the driver stats
        driver_stats["Total Income"][0] += driver_tip
        driver_stats["Tips"][0] += driver_tip
        if booking_details["Ride Option"] == "Cash":
            driver_stats["Cash Income"][0] += driver_tip
        else:
            driver_stats["Card Income"][0] += driver_tip


# Function to display the details of the ride booked
def show_ride_details():
    clear()
    if br.not_called:
        input('''Cannot view ride details if ride has not been booked.
    Press ENTER to return to menu...''')
        clear()
    else:
        print(f'''\tRide Details:\n
Booking Time: {ct}
ETA: {eta}\n''')

        for booking in booking_details:
            print(f'{booking}: {booking_details[booking]}')
        if not total_fee:
            print(f'''Total Fee: TBD
Driver Tip: {driver_tip}''')
        else:
            print(f'''Total Fee: {total_fee}
Driver Tip: {driver_tip}''')

        input('\nPress ENTER to return to menu...')
        clear()


rr, br, cf = [TrackFuncCall(register_rider), TrackFuncCall(
    book_ride), TrackFuncCall(calc_fare)]
