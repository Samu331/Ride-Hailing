from general_imports import clear
import pandas as pd

# Collect data for the drivers report
driver_stats = {
    "Rides": [0],
    "Total km": [0],
    "Total Income": [0],
    "Tips": [0],
    "Cash Income": [0],
    "Card Income": [0],
    "Income Non-Peak": [0],
    "Peak Income": [0]
}


# Function to display the driver report
def show_driver_report():

    # Create a dataframe and do average and total calculations
    df = pd.DataFrame(driver_stats)

    average_km = df['Total km'].mean()
    try:
        average_income_per_km = round(
            driver_stats["Total Income"][0] / driver_stats["Total km"][0], 2)
    except ZeroDivisionError:
        average_income_per_km = 0
    try:
        percentage_cash = round(
            (driver_stats["Cash Income"][0] / driver_stats["Total Income"][0]) * 100, 2)
    except ZeroDivisionError:
        percentage_cash = 0
    try:
        percentage_card = round(
            (driver_stats["Card Income"][0] / driver_stats["Total Income"][0]) * 100, 2)
    except ZeroDivisionError:
        percentage_card = 0

    clear()
    # Print the summary
    print(f'''{df}\n
Average Kilometers: {average_km}km
Average Income per Kilometer: R{average_income_per_km}
Percentage Cash: {percentage_cash}%
Percentage Card: {percentage_card}%''')
    input('Press ENTER to return to menu...')
    clear()
