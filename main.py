"""-----Hoan Nguyen - ID: 011310417-----"""
from CSVLoading import Distance_matrix, load_package_data, number_of_packages
from datetime import time
from DeliveryAlgorithm import calculate_route, status_at_time
from HashTable import Hash_table
from Trucks import Trucks, preroute_loading

# Create a hash table to hold package objects.
hash_table = Hash_table(number_of_packages('WGUPS Package File - Cleaned up.csv'))  # Time: O(N) Space: O(N)

# Read CSV files, populate the hash table, and create a distance table.
load_package_data('WGUPS Package File - Cleaned up.csv', hash_table)  # Time: O(N) Space: O(N)
dist_matrix = Distance_matrix()
dist_matrix.populate_distances('WGUPS Distance Table - Cleaned up.csv')  # Time: O(1) Space: O(N)

# Create truck objects.
truck_1 = Trucks()
truck_2 = Trucks(start_time=time(hour=9))  # Truck 2 holds DELAYED packages, so it needs to start at 9AM.
truck_3 = Trucks()

# Packages loading function. This function logically loads packages onto trucks to help improve the delivery routes.
# More details are in the function's module.
preroute_loading(truck_1, truck_2, truck_3, hash_table)  # Time: O(NlogN) Space: O(N)

# Use nearest neighbor algorithm to create truck 1 & 2 routes.
# Time: O(N^2) Space: O(1)
first_route = calculate_route(truck_1, dist_matrix.distance_values, dist_matrix.all_addresses, truck_1.start_time)
second_route = calculate_route(truck_2, dist_matrix.distance_values, dist_matrix.all_addresses, truck_2.start_time)

# Truck 3 starts at 11AM, after wrong addresses are updated.
truck_3.start_time = time(hour=11)

# Create truck 3 route.
# Time: O(N^2) Space: O(1)
third_route = calculate_route(truck_3, dist_matrix.distance_values, dist_matrix.all_addresses, truck_3.start_time)

'''-------------------------------------------------------------------------------------------------
                                        User Interface
-------------------------------------------------------------------------------------------------'''


def main_menu():  # Time: O(1) Space: O(1)
    # Prompt user to pick one of the options.
    main_input = input('What do you want to do?\n'
                       '1. Look up packages\n'
                       '2. Check statuses at a specific time\n'
                       '3. Exit\n')
    # Repeatedly ask user to input valid option. Recursive menu method.
    while main_input not in ['1', '2', '3']:
        print('Invalid option!')
        main_menu()

    match main_input:
        case '1':  # Sub-option for looking up packages. By ID or by address.
            user_input = input('Look up packages:\n'
                               '1. By package\'s ID\n'
                               '2. By address\n'
                               '3. Go back\n')
            match user_input:
                case '1':  # Use hash table's search function to look up package by its ID.
                    user_input = input('Please enter package\'s id: ')
                    print(hash_table.look_up(int(user_input)))
                case '2':  # Look up and print all packages delivered at a specific address.
                    user_input = input('Please enter address (i.e. 1060 Dalton Ave S): ')
                    if user_input in first_route:
                        for item in first_route[user_input]['Packages']:
                            print(item)
                    elif user_input in second_route:
                        for item in second_route[user_input]['Packages']:
                            print(item)
                    elif user_input in third_route:
                        for item in third_route[user_input]['Packages']:
                            print(item)
                case '3':  # Go back to main menu.
                    main_menu()
                case _:  # Go back to main menu if user inputs invalid option.
                    print('Invalid option!')
                    main_menu()
        case '2':  # Prompt user to input a specific time.
            user_input = input('Check statuses at a specific time:\n'
                               'Please enter a time between 08:00 and 15:00: ')

            print_dict = {}  # A dictionary that holds package's ID and status only

            # status_at_time function determines and adds the DELIVERED packages ONLY at the requested time,
            # and return the total distance traveled up until said time.
            total_distance = status_at_time(user_input, first_route, print_dict)
            total_distance += status_at_time(user_input, second_route, print_dict)
            total_distance += status_at_time(user_input, third_route, print_dict)

            # Add the remaining packages (En route) into print_dict.
            for item in hash_table.table:
                if item[0].id not in print_dict.keys():
                    print_dict[item[0].id] = item[0].status

            # Print all packages' status order by ID.
            for id in sorted(print_dict):
                print(f'ID: {id} \t\t Status: {print_dict[id]}')
            print(f'\nTotal distance traveled: {total_distance}\n')
        case '3':  # Exit the program option.
            print('Exiting . . .')

main_menu()  # Call main_menu.
