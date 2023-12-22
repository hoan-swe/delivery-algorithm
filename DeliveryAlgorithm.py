from datetime import time


def calculate_route(truck, distance_values, all_addresses, start_time):  # Time: O(N^2) Space: O(1)
    # Create a dictionary that holds the delivery addresses in order of delivery and the information related to that
    # location.
    route_dict = {}

    # add_list is a copy of the truck's delivery address list.
    add_list = truck.address_list.copy()
    min_dist = 140
    start = 0  # Start at HUB
    destination = 0  # Index of the destination address
    traveled_dist = 0  # TOTAL distance traveled

    '''-----------------------------------------------------------------------------------------------------
                                *** MAIN DELIVERY ALGORITHM BLOCK ***
                                    NEAREST NEIGHBOR - BIG O (N^2)
    -----------------------------------------------------------------------------------------------------'''
    # While there are still un-visited address in the delivery list, repeat the algorithm
    while len(add_list) != 0:
        current_row = distance_values[start]  # The row of distances from the current address

        # For each (index of)address from the delivery address list
        for i in range(1, len(all_addresses)):
            # Skip to next address if the address is the current position (current_row[i] == 0)
            # or already visited (all_addresses[i] not in add_list)
            if float(current_row[i]) == 0 or all_addresses[i] not in add_list:
                continue
            # Else, record the smaller distance
            elif min_dist > float(current_row[i]):
                min_dist = float(current_row[i])
                # Put the current address as destination (using index)
                destination = i
        # After the above for-loop, the algorithm found the destination's address with the
        # smallest distance from the current position.
        '''--------------------------------------------------------------------------------------------------'''
        traveled_dist += min_dist  # Calculate the distance the truck has traveled up to this location.
        delivered_packages = []  # This list holds packages that were delivered at current location.

        # Any package on the truck that has current location as its delivery address is delivered.
        for item in truck.packages:
            if item.address == all_addresses[destination]:
                delivered_packages.append(item)

        # Calculate the time to get from previous location to current location (project's assumption: 18 MPH)
        # Distance / speed = time (unit: hours, type float)
        hour_traveled, minute_traveled = divmod(traveled_dist / 18, 1)
        hour_traveled = int(hour_traveled)  # Integer part = hour
        minute_traveled = int(minute_traveled * 60)  # Fractional part * 60 = minute
        # Add hour and minute to truck's start time, and create a time object.
        time_traveled = time(hour=start_time.hour + hour_traveled, minute=start_time.minute + minute_traveled)

        # Add all information (packages, distance traveled up to current location, and arrival time) as values to
        # current location address (as key)
        record = {'Distance traveled': traveled_dist,
                  'Packages': delivered_packages,
                  'Time arrived': time_traveled}
        route_dict[all_addresses[destination]] = record  # Add delivery addresses in order of delivery

        min_dist = 140  # Reset minimal distance.

        # Remove the destination's address from the delivery address list (visited).
        add_list.remove(all_addresses[destination])

        # Set current position as starting position.
        start = destination - 1

        # NOTE: all_address has an empty column in the beginning, so its index needs to be off-set
        #       by 1 to be used in distance_values (start = destination - 1).

    # After all deliveries are done, add the distance of going back to the HUB.
    traveled_dist += float(distance_values[start][1])
    # Calculate time needed to get back to the HUB, and populate the HUB's values
    hour_traveled, minute_traveled = divmod(traveled_dist / 18, 1)
    hour_traveled = int(hour_traveled)
    minute_traveled = int(minute_traveled * 60)
    time_traveled = time(hour=start_time.hour + hour_traveled, minute=start_time.minute + minute_traveled)

    record = {'Distance traveled': traveled_dist,
              'Packages': [],
              'Time arrived': time_traveled}
    route_dict[all_addresses[1]] = record

    return route_dict  # Return the truck's deliver route dictionary.


# This function fetch packages' ID and delivery status as a key-value pair, put them in the dictionary
# argument, and return the total distance traveled up to a specific time.
def status_at_time(user_input, route, dict):  # Time: O(N) Space: O(1)
    distance = 0
    request_time = time()  # Create a time object.
    request_time = request_time.fromisoformat(user_input)  # Convert user's input string to time object.

    # Compare arrival time of each address to user's input.
    for address in route:
        if route[address]['Time arrived'] < request_time:
            # Put all packages that were delivered to the current address into the dictionary to be printed at main.
            for item in route[address]['Packages']:
                item.status = 'Delivered at '
                dict[item.id] = item.status + str(route[address]['Time arrived'])
            distance = route[address]['Distance traveled']
    return distance
