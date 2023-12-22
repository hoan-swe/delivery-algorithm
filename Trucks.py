from datetime import time


# Create a trucks class to hold packages for delivery.
class Trucks:
    def __init__(self, capacity=16, start_time=time(hour=8, minute=00)):
        self.cap = capacity
        self.packages = []  # Holds LISTS (bucket) of package OBJECTS        
        self.address_list = []  # Holds packages' delivery addresses
        self.start_time = start_time  # Time the truck leave the HUB at, default 0800

    # Load function adds package OBJECTS onto truck's packages list.
    def load(self, item):  # Time: O(1) Space: O(1)
        self.packages.append(item)
        item.status = 'En route'

    # Update address function populate the truck's delivery address list.
    def update_address_list(self):  # Time: O(N) Space: O(1)
        for package in self.packages:
            # No duplicate addresses to make delivery algorithm easier.
            if package.address not in self.address_list:
                self.address_list.append(package.address)


# This function's purpose is to logically load packages onto truck prioritizing SPECIAL NOTES and DEADLINES first,
# then group packages that have the same delivery address together.
def preroute_loading(truck_1, truck_2, truck_3, hash_table):  # Time: O(NlogN) Space: O(N)
    # A dictionary to hold ID (key) and its corresponding address. This is needed because this dictionary will be
    # modified to act as counter and tracker (delivered package is removed) leaving hash table data untouched.
    delivery_dict = {}

    # Load packages onto trucks prioritizing special notes and delivery time
    for bucket in hash_table.table:
        # Put packages that say 'Truck 2 only' on truck_2
        if (bucket[0].notes == '2' or bucket[0].notes == 'Delayed') and len(truck_2.packages) < truck_2.cap and bucket[0].status != 'En route':
            truck_2.load(bucket[0])
        # Put packages that need to go together (Combined) and packages that have a deadline before EOD on Truck 1
        elif (bucket[0].notes == 'Combined' or bucket[0].deadline != 'EOD') and len(truck_1.packages) < truck_1.cap and \
                bucket[0].status != 'En route':
            truck_1.load(bucket[0])
        # Put packages that have the wrong address on truck_3.
        elif bucket[0].notes == 'Wrong address' and len(truck_3.packages) < truck_3.cap and bucket[0].status != 'En route':
            truck_1.load(bucket[0])
        # Store unloaded packages.
        else:
            delivery_dict[bucket[0].id] = bucket[0].address

    truck_1.update_address_list()
    truck_2.update_address_list()

    # Group packages with the same addresses as loaded packages onto the same trucks until full.
    remaining_delivery = delivery_dict.copy()
    for id, address in remaining_delivery.items():
        if address in truck_1.address_list and len(truck_1.packages) < truck_1.cap:
            truck_1.load(hash_table.look_up(id))
            delivery_dict.pop(id)
        elif address in truck_2.address_list and len(truck_2.packages) < truck_2.cap:
            truck_2.load(hash_table.look_up(id))
            delivery_dict.pop(id)
    # Load remaining packages that have no similar delivery address
    remaining_delivery = delivery_dict.copy()
    for id in remaining_delivery:
        if len(truck_1.packages) < truck_1.cap:
            truck_1.load(hash_table.look_up(id))
            delivery_dict.pop(id)
        elif len(truck_2.packages) < truck_2.cap:
            truck_2.load(hash_table.look_up(id))
            delivery_dict.pop(id)
        else:
            truck_3.load(hash_table.look_up(id))

    truck_1.update_address_list()
    truck_2.update_address_list()
    truck_3.update_address_list()
