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
            print(" 3. Search a Flight")
            print(" 4. Manage Flights")
            print(" 5. Manage Pilots")
            print(" 6. Manage Aircraft")
            print(" 7. Manage Stations")
            print(" 8. Manage Routes")
            print(" 9. Exit\n")

            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.db_ops.show_flights()
            elif choice == "2":
                self.flights_by_criteria_menu()
            elif choice == "3":
                self.db_ops.search_flight()
            elif choice == "4":
                self.manage_flights_menu()
            elif choice == "5":
                self.manage_pilots_menu()
            elif choice == "6":
                self.manage_aircraft_menu()
            elif choice == "7":
                self.manage_stations_menu()
            elif choice == "8":
                self.manage_routes_menu()
            elif choice == "9":
                exit(0)
            else:
                print("Invalid Choice")

    def next_menu(self):
        while True:
            print("\n What would you like to do next?")
            print("**********")
            print(" 1. Return to Main Menu")
            print(" 2. Exit\n")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.main_menu()
            elif choice == "2":
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

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.show_flights_by_destination()
            elif choice == "2":
                self.db_ops.show_flights_by_date()
            elif choice == "3":
                self.db_ops.show_flights_by_status()
            elif choice == "4":
                self.main_menu()
            else:
                print("Invalid Choice")

    def manage_flights_menu(self):
        while True:
            print("\n Manage Flights:")
            print("**********")
            print(" 1. Add a new Flight")
            print(" 2. Update a Flight")
            print(" 3. Delete a Flight")
            print(" 4. Return to Main Menu\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.add_new_flight()
            elif choice == "2":
                self.db_ops.update_flight()
            elif choice == "3":
                self.db_ops.delete_flight()
            elif choice == "4":
                self.main_menu()
            else:
                print("Invalid Choice")

    def manage_pilots_menu(self):
        while True:
            print("\n Manage Pilots:")
            print("**********")
            print(" 1. View all Pilots")
            print(" 2. Add a new Pilot")
            print(" 3. Update a Pilot")
            print(" 4. Delete a Pilot")
            print(" 5. View pilot schedule")
            print(" 6. Return to Main Menu\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.show_pilots()
            elif choice == "2":
                self.db_ops.add_new_pilot()
            elif choice == "3":
                self.db_ops.update_pilot()
            elif choice == "4":
                self.db_ops.delete_pilot()
            elif choice == "5":
                self.db_ops.view_pilot_schedule()
            elif choice == "6":
                self.main_menu()
            else:
                print("Invalid Choice")

    def manage_aircraft_menu(self):
        while True:
            print("\n Manage Aircraft:")
            print("**********")
            print(" 1. View all Aircraft")
            print(" 2. Add a new Aircraft")
            print(" 3. Update an Aircraft")
            print(" 4. Delete an Aircraft")
            print(" 5. Return to Main Menu\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.show_aircraft()
            elif choice == "2":
                self.db_ops.add_new_aircraft()
            elif choice == "3":
                self.db_ops.update_aircraft()
            elif choice == "4":
                self.db_ops.delete_aircraft()
            elif choice == "5":
                self.main_menu()
            else:
                print("Invalid Choice")

    def manage_stations_menu(self):
        while True:
            print("\n Manage Stations:")
            print("**********")
            print(" 1. View all Stations")
            print(" 2. Add a new Station")
            print(" 3. Update a Station")
            print(" 4. Delete a Station")
            print(" 5. Return to Main Menu\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.show_stations()
            elif choice == "2":
                self.db_ops.add_new_station()
            elif choice == "3":
                self.db_ops.update_station()
            elif choice == "4":
                self.db_ops.delete_station()
            elif choice == "5":
                self.main_menu()
            else:
                print("Invalid Choice")

    def manage_routes_menu(self):
        while True:
            print("\n Manage Routes:")
            print("**********")
            print(" 1. View all Routes")
            print(" 2. Add a new Route")
            print(" 3. Update a Route")
            print(" 4. Delete a Route")
            print(" 5. Return to Main Menu\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.db_ops.show_routes()
            elif choice == "2":
                self.db_ops.add_new_route()
            elif choice == "3":
                self.db_ops.update_route()
            elif choice == "4":
                self.db_ops.delete_route()
            elif choice == "5":
                self.main_menu()
            else:
                print("Invalid Choice")