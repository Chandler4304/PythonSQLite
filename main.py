import DBOperations
import SampleData

# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

DBOperations.DBOperations().__init__()
SampleData.SampleData().seed_sample_data()

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. View all flights")
  print(" 2. Insert data into FlightInfo")
  print(" 3. Select all data from FlightInfo")
  print(" 4. Search a flight")
  print(" 5. Update data some records")
  print(" 6. Delete data some records")
  print(" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations.DBOperations()
  if __choose_menu == 1:
    db_ops.show_flights()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print("Invalid Choice")
