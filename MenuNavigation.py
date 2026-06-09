import DBOperations

class MenuNavigation:

    # The MenuNavigation will parse arguments.
    # These argument will be definded by the users on the console.
    # The user will select a choice from the menu to interact with the database.

    def __init__(self):
        self.db_ops = DBOperations.DBOperations()

    def main_menu(self):
        while True:
            print("\n Menu:")
            print("**********")
            print(" 1. View all Flights")
            print(" 2. View Flights by specific criteria")
            print(" 3. Add a new Flight")
            print(" 4. Search a flight")
            print(" 5. Update data some records")
            print(" 6. Delete data some records")
            print(" 7. Exit\n")

            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                self.db_ops.show_flights()
            elif choice == 2:
                self.flights_by_criteria_menu()
            elif choice == 3:
                self.db_ops.add_new_flight()
            elif choice == 4:
                self.db_ops.search_data()
            elif choice == 5:
                self.db_ops.update_data()
            elif choice == 6:
                self.db_ops.delete_data()
            elif choice == 7:
                exit(0)
            else:
                print("Invalid Choice")

    def next_menu(self):
        while True:
            print("\n What would you like to do next?")
            print("**********")
            print(" 1. Return to Main Menu")
            print(" 2. Exit\n")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.main_menu()
            elif choice == 2:
                exit(0)
            else:
                print("Invalid Choice")

    def flights_by_criteria_menu(self):
        while True:
            print("\n View Flights by specific criteria:")
            print("**********")
            print(" 1. View Flights by Destination")
            print(" 2. View Flights by Date")
            print(" 3. View Flights by Status")
            print(" 4. Return to Main Menu\n")

            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                self.db_ops.show_flights_by_destination()
            elif choice == 2:
                self.db_ops.show_flights_by_date()
            elif choice == 3:
                self.db_ops.show_flights_by_status()
            elif choice == 4:
                break
            else:
                print("Invalid Choice")
