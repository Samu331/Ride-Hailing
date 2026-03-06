from general_imports import *
import json

# Initialize the different rates
rates = {
    "1": ["Base Fare", 10],
    "2": ["Distance Rate", 1],
    "3": ["Peak Rate", 0.1],
    "4": ["Vat Rate", 0.15]
}

file_path = "rates.json"

# Save the rates to a JSON file
with open(file_path, "w") as file:
    json.dump(rates, file)

# Function to change the rates


def change_rates():
    clear()

    def check_changed_rate(to_change):
        while True:
            clear()
            print(
                f'Current {loaded_data[to_change][0].capitalize()}: {loaded_data[to_change][1]}')
            new_rate = input(f'New {loaded_data[to_change][0].capitalize()}: ')
            try:
                new_rate = float(new_rate)
            except ValueError:
                clear()
                input('''Enter a valid digit to change the rate.
    Press ENTER to try again.''')
            else:
                break
        return new_rate

    # Open the rates.json and write to it as well
    with open(file_path, "r+") as file:
        loaded_data = json.load(file)

        while True:
            for letter in loaded_data:
                print(f'{letter}: {loaded_data[letter][0].capitalize()}')
            to_change = input("Choose what to change: ")
            try:
                loaded_data[to_change][1] = check_changed_rate(to_change)
            except KeyError:
                clear()
                print("Select options 1 to 4.\n")
                clear()
            else:
                break

        # Move pointer to start of file and clear its content
        file.seek(0)
        file.truncate()

        # Write the changed rate back to the file
        json.dump(loaded_data, file)
        clear()
