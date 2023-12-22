import csv


# Packages' delivery data CSV.
# Define a Package class to hold package's delivery data.
class Package:
    def __init__(self, ID, address, deadline, city, weight, zip, status, notes):
        self.id = ID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.weight = weight
        self.zip = zip
        self.status = status
        self.notes = notes

    # Overload str() function to return a string instead of an object reference.
    # The string is formatted for search result printing.
    def __str__(self):
        return ('Package ID: %s\n'
                'Address: %s\n'
                'Deadline: %s\n'
                'City: %s\n'
                'Weight: %s\n'
                'Zip code: %s\n'
                'Status: %s\n') % (self.id, self.address, self.deadline, self.city, self.weight, self.zip, self.status)


# Load function to read CSV file and populate hash table.
def load_package_data(file_name, hash_table):  # Time: O(N) Space: O(N)
    # Open CSV file.
    with open(file_name) as packages:
        # Read CSV file, remove commas and put data into package_data.
        package_data = csv.reader(packages, delimiter=',')
        next(package_data)  # Skip headers.
        # Iterate through package_data, and assign values to corresponding variables.
        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_deadline = package[5]
            p_city = package[2]
            p_weight = package[6]
            p_zip = package[4]
            p_status = "At the HUB"
            p_notes = package[7]

            # Create a package object with above values.
            package = Package(p_id, p_address, p_deadline, p_city, p_weight, p_zip, p_status, p_notes)

            # Insert into hash table using insert function.
            hash_table.insert(p_id, package)


# -------------------------------------------------------------------------------------------------------------
# Define a class to create an object that holds the distance table values.
class Distance_matrix:
    def __init__(self):
        # A list of ALL delivery addresses (including the 'HUB').
        self.all_addresses = []
        # A list of distances from each delivery address (address at index 0, distance values start at index 1)
        self.distance_values = []

    # Open CSV file, read, and populate the lists above.
    def populate_distances(self, file_name):  # Time: O(1) Space: O(N)
        with open(file_name) as distances:
            row_data = csv.reader(distances, delimiter=',')
            self.all_addresses = next(row_data)
            self.distance_values = list(row_data)


# Count the number of packages, return the total. This makes the program self-adjusts to different numbers of packages.
def number_of_packages(filename) -> int:  # Time: O(N) Space: O(1)
    total = -1  # Off set header row.
    # Iterate through CSV file, count, and add up all rows.
    for row in open(filename):
        total += 1
    return total
