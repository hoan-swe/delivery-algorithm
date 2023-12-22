# Define a hash table class.
class Hash_table:  # Time: O(N) Space: O(N)
    # Constructor with optional initial capacity parameter, default to 40.
    def __init__(self, initial_capacity=40):

        # Initialize the hash table with an empty bucket list.
        self.table = []

        # Assigns an empty list to each bucket.
        for i in range(initial_capacity):
            self.table.append([])

    # Insert function to insert package OBJECTS into the hash table.
    def insert(self, ID, package):  # Time: O(1) Space: O(1)
        # Modulo as hash function using packages' ID.
        bucket_number = ID % len(self.table)
        bucket = self.table[bucket_number]
        # Insert the package to the end of the bucket.
        bucket.append(package)

    # Search function using package's ID.
    def look_up(self, ID):  # Time: O(1) Space: O(1)
        # Check if package ID is in table.
        if len(self.table) >= ID > 0:
            # The bucket where this package would be.
            bucket_number = ID % len(self.table)
            # Return the package object.
            return self.table[bucket_number][0]
        else:
            return None
