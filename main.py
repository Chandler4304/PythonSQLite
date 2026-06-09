import DBOperations
import SampleData
import MenuNavigation

# The main function will initialize the database connection, seed it with sample data if there is none, and launch the menu.

DBOperations.DBOperations().__init__()
SampleData.SampleData().seed_sample_data()

MenuNavigation.MenuNavigation().main_menu()