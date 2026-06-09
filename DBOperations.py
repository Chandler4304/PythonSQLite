import sqlite3
import datetime
import zoneinfo
import MenuNavigation

class DBOperations:

  sql_create_table_firsttime = "CREATE TABLE IF NOT EXISTS {} ({})"
  sql_create_table = "CREATE TABLE {} ({})"
  sql_insert = "INSERT INTO {} ({}) VALUES ({})"
  sql_select_all = "SELECT * FROM {}"
  sql_search = "SELECT * FROM {} WHERE {} = ?"
  sql_alter_data = "ALTER TABLE {} ADD COLUMN {} {}"
  sql_update_data = "UPDATE {} SET {} WHERE {} = ?"
  sql_delete_data = "DELETE FROM {} WHERE {} = ?"
  sql_drop_table = "DROP TABLE IF EXISTS {}"


  def __init__(self):
    try:
      # Create a connection to the database and create tables if they do not exist.
      self.conn = sqlite3.connect("FlightManager.db")
      self.conn.row_factory = sqlite3.Row # Use row factory to access columns by name
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime.format("Aircraft", "aircraftID INTEGER PRIMARY KEY AUTOINCREMENT, aircraftModel VARCHAR(30), capacity INTEGER"))
      self.cur.execute(self.sql_create_table_firsttime.format("Stations", "stationID INTEGER PRIMARY KEY AUTOINCREMENT, stationName VARCHAR(50), timeZone VARCHAR(30)"))
      self.cur.execute(self.sql_create_table_firsttime.format("Pilots", "pilotID INTEGER PRIMARY KEY AUTOINCREMENT, firstName VARCHAR(30), lastName VARCHAR(30)"))
      self.cur.execute(self.sql_create_table_firsttime.format("Routes", """routeID INTEGER PRIMARY KEY AUTOINCREMENT, routeBase INTEGER DEFAULT '1' REFERENCES Stations(stationID),
                                                              routeDestination INTEGER REFERENCES Stations(stationID), flightTime HOURS"""))
      self.cur.execute(self.sql_create_table_firsttime.format("Flights", """flightID INTEGER PRIMARY KEY AUTOINCREMENT, route INTEGER REFERENCES Routes(routeID),
                                                              aircraft INTEGER REFERENCES Aircraft(aircraftID), pilot INTEGER REFERENCES Pilots(pilotID),
                                                              coPilot INTEGER REFERENCES Pilots(pilotID), outboundDate DATE, outboundTime TIME, inboundDate DATE, inboundTime TIME, status VARCHAR(30)"""))
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      return

  def get_connection(self):
    self.conn = sqlite3.connect("FlightManager.db")
    self.conn.row_factory = sqlite3.Row # Use row factory to access columns by name
    self.cur = self.conn.cursor()
  
  def show_stations(self):
    self.cur.execute("SELECT * FROM Stations")
    stations = self.cur.fetchall()
    if not stations:
      print("\nNo stations found.")
      return
    for station in stations:
      print(f"Station ID: {station['stationID']}, Name: {station['stationName']}")

  def show_aircraft(self):
    self.cur.execute("SELECT * FROM Aircraft")
    aircrafts = self.cur.fetchall()
    if not aircrafts:
      print("\nNo aircraft found.")
      return
    for aircraft in aircrafts:
      print(f"Aircraft ID: {aircraft['aircraftID']}, Model: {aircraft['aircraftModel']}, Capacity: {aircraft['capacity']}")

  def show_pilots(self):
    self.cur.execute("SELECT * FROM Pilots")
    pilots = self.cur.fetchall()
    if not pilots:
      print("\nNo pilots found.")
      return
    for pilot in pilots:
      print(f"Pilot ID: {pilot['pilotID']}, Name: {pilot['firstName']} {pilot['lastName']}")

  def show_flights(self):
    try:
      self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                          dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                          p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                          p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                          FROM Flights
                          JOIN Routes ON Flights.route = Routes.routeID
                          JOIN Stations AS base ON Routes.routeBase = base.stationID
                          JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                          JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                          JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                          JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID""")  
      flights = self.cur.fetchall()
      if not flights:
        print("\nNo flights found.")
        return
      for flight in flights:
        self.print_flight_details(flight)
    except Exception as e:
      print(e)
    finally:   
      MenuNavigation.MenuNavigation().next_menu()


  def show_flights_by_destination(self, destination=None):
    try:
      self.show_stations()
      if destination is None:
        destination = input("\nEnter Destination Station ID: ")
      self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                          dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                          p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                          p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                          FROM Flights
                          JOIN Routes ON Flights.route = Routes.routeID
                          JOIN Stations AS base ON Routes.routeBase = base.stationID
                          JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                          JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                          JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                          JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                          WHERE dest.stationID = ?""", (destination,))
      flights = self.cur.fetchall()
      if not flights:
        print("\nNo flights found for the specified destination.")
        return
      for flight in flights:
        self.print_flight_details(flight)
    except Exception as e:
      print(e)
    finally:   
      MenuNavigation.MenuNavigation().next_menu()

  def show_flights_by_date(self):
    try:
      date = input("\nEnter Date (YYYY-MM-DD): ")
      self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                          dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                          p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                          p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                          FROM Flights
                          JOIN Routes ON Flights.route = Routes.routeID
                          JOIN Stations AS base ON Routes.routeBase = base.stationID
                          JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                          JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                          JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                          JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                          WHERE outboundDate = ? OR inboundDate = ?""", (date, date))
      flights = self.cur.fetchall()
      if not flights:
        print("\nNo flights found for the specified date.")
        return
      for flight in flights:
        self.print_flight_details(flight)
    except Exception as e:
      print(e)
    finally:
      MenuNavigation.MenuNavigation().next_menu()

  def show_flights_by_status(self):
    try:
      status = input("\nEnter Flight Status: ")
      self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                          dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                          p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                          p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                          FROM Flights
                          JOIN Routes ON Flights.route = Routes.routeID
                          JOIN Stations AS base ON Routes.routeBase = base.stationID
                          JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                          JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                          JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                          JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                          WHERE status = ?""", (status,))
      flights = self.cur.fetchall()
      if not flights:
        print("\nNo flights found for the specified status.")
        return
      for flight in flights:
        self.print_flight_details(flight)
    except Exception as e:
      print(e)
    finally:
      MenuNavigation.MenuNavigation().next_menu()

  def print_flight_details(self, flight):
    base_tz = zoneinfo.ZoneInfo(flight['baseTimezone'])
    dest_tz = zoneinfo.ZoneInfo(flight['destTimezone'])
    outbound_dt = datetime.datetime.strptime(flight['outboundDate'] + " " + flight['outboundTime'], '%Y-%m-%d %H:%M').replace(tzinfo=base_tz)
    outbound_arrival = (outbound_dt + datetime.timedelta(hours=flight['flightTime'])).astimezone(dest_tz)
    inbound_dt = datetime.datetime.strptime(flight['inboundDate'] + " " + flight['inboundTime'], '%Y-%m-%d %H:%M').replace(tzinfo=dest_tz)
    inbound_arrival = (inbound_dt + datetime.timedelta(hours=flight['flightTime'])).astimezone(base_tz)

    print(f"Flight ID: {flight['flightID']}")
    print(f"  From: {flight['baseStation']}")
    print(f"  To: {flight['destStation']}")
    print(f"  Aircraft: {flight['aircraftModel']}")
    print(f"  Pilot: {flight['pilotFirstName']} {flight['pilotLastName']}")
    print(f"  Co-Pilot: {flight['coPilotFirstName']} {flight['coPilotLastName']}")
    print(f"  Outbound: {flight['outboundDate']} {flight['outboundTime']} ({base_tz.tzname(outbound_dt)})")
    print(f"  Outbound Arrival Time: {outbound_arrival.strftime('%Y-%m-%d %H:%M')} ({dest_tz.tzname(outbound_arrival)})")
    print(f"  Inbound: {flight['inboundDate']} {flight['inboundTime']} ({dest_tz.tzname(inbound_dt)})")
    print(f"  Inbound Arrival Time: {inbound_arrival.strftime('%Y-%m-%d %H:%M')} ({base_tz.tzname(inbound_arrival)})")
    print(f"  Status: {flight['status']}")
    print("-" * 50)

  def add_new_flight(self):
    # Input validation for each step. Not required for 'Status'
    valid_station = False
    valid_aircraft = False
    valid_pilots = False
    valid_timings = False

    try:
      while valid_station == False:
        self.show_stations()
        try:
          dest_station_id = int(input("\nEnter Destination Station ID or 0 to cancel: "))
          if dest_station_id == 0:
            print("\nOperation cancelled.\n")
            return
          self.cur.execute("""SELECT Routes.routeID, Routes.flightTime, base.timeZone AS baseTimezone, dest.timeZone AS destTimezone
                              FROM Routes
                              JOIN Stations AS base ON Routes.routeBase = base.stationID
                              JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                              WHERE routeDestination = ?""", (dest_station_id,))
          route_row = self.cur.fetchone()
          if not route_row:
            print("\nInvalid Station ID.\n")
            return
        except ValueError:
          print("\nInvalid input. Please enter a valid Station ID.\n")
          return

        route_id = route_row['routeID'] if isinstance(route_row, sqlite3.Row) else route_row[0]
        flight_time = route_row['flightTime'] if isinstance(route_row, sqlite3.Row) else route_row[1]
        base_tz = zoneinfo.ZoneInfo(route_row['baseTimezone']) if isinstance(route_row, sqlite3.Row) else zoneinfo.ZoneInfo(route_row[2])
        dest_tz = zoneinfo.ZoneInfo(route_row['destTimezone']) if isinstance(route_row, sqlite3.Row) else zoneinfo.ZoneInfo(route_row[3])
        valid_station = True

      while valid_aircraft == False:
        print("\nAvailable Aircraft: \n")
        self.show_aircraft()
        try:
          aircraft_id = int(input("\nEnter Aircraft ID or 0 to cancel: "))
          if aircraft_id == 0:
            print("\nOperation cancelled.\n")
            return
          self.cur.execute("SELECT * FROM Aircraft")
          aircraft_ids = [row[0] for row in self.cur.fetchall()]
          if aircraft_id not in aircraft_ids:
            print("\nInvalid Aircraft ID.\n")
            continue
        except ValueError:
          print("\nInvalid input. Please enter a valid Aircraft ID.\n")
          return
        valid_aircraft = True
        
      while valid_pilots == False:
        print("\nAvailable Pilots: \n")
        self.show_pilots()
        try:
          pilot_id = int(input("\nEnter Pilot ID or 0 to cancel: "))
          if pilot_id == 0:
            print("\nOperation cancelled.\n")
            return
          self.cur.execute("SELECT * FROM Pilots")
          pilot_ids = [row[0] for row in self.cur.fetchall()]
          if pilot_id not in pilot_ids:
            print("\nInvalid Pilot ID.\n")
            continue
          co_pilot_id = int(input("\nEnter Co-Pilot ID or 0 to cancel: "))
          if co_pilot_id == 0:
            print("\nOperation cancelled.\n")
            return
          if co_pilot_id not in pilot_ids:
            print("\nInvalid Co-Pilot ID.\n")
            continue
          if co_pilot_id == pilot_id:
            print("\nPilot and Co-Pilot cannot be the same person.\n")
            continue
        except ValueError:
          print("\nInvalid input. Please enter a valid Pilot ID.\n")
          return
        valid_pilots = True
      
      while valid_timings == False:
        outbound_date = input("Enter Outbound Date (Local Time) (YYYY-MM-DD) or 0 to cancel: ")
        if outbound_date == "0":
          print("\nOperation cancelled.\n")
          return
        outbound_time = input("\nEnter Outbound Time (Local Time) (HH:MM) or 0 to cancel: ")
        if outbound_time == "0":
          print("\nOperation cancelled.\n")
          return
        inbound_date = input("\nEnter Inbound Date (Local Time) (YYYY-MM-DD) or 0 to cancel: ")
        if inbound_date == "0":
          print("\nOperation cancelled.\n")
          return
        inbound_time = input("\nEnter Inbound Time (Local Time) (HH:MM) or 0 to cancel: ")
        if inbound_time == "0":
          print("\nOperation cancelled.\n")
          return
        try:
          outbound_dt = datetime.datetime.strptime(outbound_date + " " + outbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=base_tz)
          outbound_arrival = (outbound_dt + datetime.timedelta(hours=flight_time)).astimezone(dest_tz)
          inbound_dt = datetime.datetime.strptime(inbound_date + " " + inbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=dest_tz)
        except ValueError:
          print("\nInvalid date or time format.\n")
          continue
        if inbound_dt < outbound_arrival + datetime.timedelta(hours=1):
          print("\nInbound departure must be at least 1 hour after outbound arrival at the destination.")
          continue
        valid_timings = True
        
        status = input("\nEnter Flight Status or 0 to cancel: ")
        if status == "0":
          print("\nOperation cancelled.\n")
          return

        self.cur.execute("""INSERT INTO Flights (route, aircraft, pilot, coPilot, outboundDate, outboundTime, inboundDate, inboundTime, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (route_id, aircraft_id, pilot_id, co_pilot_id, outbound_date, outbound_time, inbound_date, inbound_time, status))
        self.conn.commit()
        print("\nNew flight added successfully.")
    except Exception as e:
      print(e)
    finally:
      MenuNavigation.MenuNavigation().next_menu()

  def search_flight(self):
    valid_input = False
    while valid_input == False:
      try: 
        self.get_connection()
        flight_id = int(input("\nEnter Flight ID to search: "))
        self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                            dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                            p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                            p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                            FROM Flights
                            JOIN Routes ON Flights.route = Routes.routeID
                            JOIN Stations AS base ON Routes.routeBase = base.stationID
                            JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                            JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                            JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                            JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                            WHERE flightID = ?""", (flight_id,))
        flight = self.cur.fetchone()
        if not flight:
          print("\nNo flight found with the specified ID.")
          return
        self.print_flight_details(flight)
        valid_input = True
      except ValueError:
        print("\nInvalid Flight ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def update_flight(self):
    valid_input = False
    while valid_input == False:
      try:
        flight_id = int(input("\nEnter Flight ID to update or 0 to cancel: "))
        if flight_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                            dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                            p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                            p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                            FROM Flights
                            JOIN Routes ON Flights.route = Routes.routeID
                            JOIN Stations AS base ON Routes.routeBase = base.stationID
                            JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                            JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                            JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                            JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                            WHERE flightID = ?""", (flight_id,))
        flight = self.cur.fetchone()
        if not flight:
          print("\nNo flight found with the specified ID.")
          continue
        print("\nCurrent Flight Details:")
        self.print_flight_details(flight)
        print("\nSpecify which details to update or 0 to cancel:")
        print("1. Destination Station")
        print("2. Aircraft")
        print("3. Pilot")
        print("4. Co-Pilot")
        print("5. Date and Time")
        print("6. Status")
        choice = input("Enter your choice: ")
        if choice == "0":
          print("\nOperation cancelled.")
          return
        elif choice == "1":
          self.show_stations()
          dest_station_id = int(input("\nEnter new Destination Station ID: "))
          self.cur.execute("""SELECT routeID FROM Routes WHERE routeDestination = ?""", (dest_station_id,))
          route_row = self.cur.fetchone()
          if not route_row:
            print("\nInvalid Station ID.")
            return
          print("\nDate and time must be reconfirmed after changing the destination. Please enter the new date and time details:\n")
          outbound_date = input("\nEnter new Outbound Date (Local Time) (YYYY-MM-DD): ")
          outbound_time = input("\nEnter new Outbound Time (Local Time) (HH:MM): ")
          inbound_date = input("\nEnter new Inbound Date (Local Time) (YYYY-MM-DD): ")
          inbound_time = input("\nEnter new Inbound Time (Local Time) (HH:MM): ")
          try:
            flight_time = flight['flightTime'] if isinstance(flight, sqlite3.Row) else flight[1]
            base_tz = zoneinfo.ZoneInfo(flight['baseTimezone']) if isinstance(flight, sqlite3.Row) else zoneinfo.ZoneInfo(flight[2])
            dest_tz = zoneinfo.ZoneInfo(flight['destTimezone']) if isinstance(flight, sqlite3.Row) else zoneinfo.ZoneInfo(flight[3])
            outbound_dt = datetime.datetime.strptime(outbound_date + " " + outbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=base_tz)
            outbound_arrival = (outbound_dt + datetime.timedelta(hours=flight_time)).astimezone(dest_tz)
            inbound_dt = datetime.datetime.strptime(inbound_date + " " + inbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=dest_tz)
          except ValueError:
            print("\nInvalid date or time format.\n")
            return
          if inbound_dt < outbound_arrival + datetime.timedelta(hours=1):
            print("\nInbound departure must be at least 1 hour after outbound arrival at the destination. (" + outbound_arrival.strftime('%Y-%m-%d %H:%M') + " " + dest_tz.tzname(outbound_arrival) + ")")
            continue
          new_route_id = route_row['routeID'] if isinstance(route_row, sqlite3.Row) else route_row[0]
          self.cur.execute("UPDATE Flights SET route = ? WHERE flightID = ?", (new_route_id, flight_id))
          self.cur.execute("UPDATE Flights SET outboundDate = ?, outboundTime = ? WHERE flightID = ?", (outbound_date, outbound_time, flight_id))
          self.cur.execute("UPDATE Flights SET inboundDate = ?, inboundTime = ? WHERE flightID = ?", (inbound_date, inbound_time, flight_id))
        elif choice == "2":
          self.show_aircraft()
          aircraft_id = int(input("\nEnter new Aircraft ID: "))
          self.cur.execute("SELECT * FROM Aircraft")
          aircraft_ids = [row[0] for row in self.cur.fetchall()]
          if aircraft_id not in aircraft_ids:
            print("\nInvalid Aircraft ID.")
            continue
          self.cur.execute("UPDATE Flights SET aircraft = ? WHERE flightID = ?", (aircraft_id, flight_id))
        elif choice == "3":
          self.show_pilots()
          pilot_id = int(input("\nEnter new Pilot ID: "))
          self.cur.execute("SELECT * FROM Pilots")
          pilot_ids = [row[0] for row in self.cur.fetchall()]
          if pilot_id not in pilot_ids:
            print("\nInvalid Pilot ID.")
            continue
          self.cur.execute("UPDATE Flights SET pilot = ? WHERE flightID = ?", (pilot_id, flight_id))
        elif choice == "4":
          self.show_pilots()
          co_pilot_id = int(input("\nEnter new Co-Pilot ID: "))
          self.cur.execute("SELECT * FROM Pilots")
          pilot_ids = [row[0] for row in self.cur.fetchall()]
          if co_pilot_id not in pilot_ids:
            print("\nInvalid Co-Pilot ID.")
            continue
          self.cur.execute("UPDATE Flights SET coPilot = ? WHERE flightID = ?", (co_pilot_id, flight_id))
        elif choice == "5":
          outbound_date = input("\nEnter new Outbound Date (Local Time) (YYYY-MM-DD): ")
          outbound_time = input("\nEnter new Outbound Time (Local Time) (HH:MM): ")
          inbound_date = input("\nEnter new Inbound Date (Local Time) (YYYY-MM-DD): ")
          inbound_time = input("\nEnter new Inbound Time (Local Time) (HH:MM): ")
          try:
            flight_time = flight['flightTime'] if isinstance(flight, sqlite3.Row) else flight[1]
            base_tz = zoneinfo.ZoneInfo(flight['baseTimezone']) if isinstance(flight, sqlite3.Row) else zoneinfo.ZoneInfo(flight[2])
            dest_tz = zoneinfo.ZoneInfo(flight['destTimezone']) if isinstance(flight, sqlite3.Row) else zoneinfo.ZoneInfo(flight[3])
            outbound_dt = datetime.datetime.strptime(outbound_date + " " + outbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=base_tz)
            outbound_arrival = (outbound_dt + datetime.timedelta(hours=flight_time)).astimezone(dest_tz)
            inbound_dt = datetime.datetime.strptime(inbound_date + " " + inbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=dest_tz)
          except ValueError:
            print("\nInvalid date or time format.\n")
            return
          if inbound_dt < outbound_arrival + datetime.timedelta(hours=1):
            print("\nInbound departure must be at least 1 hour after outbound arrival at the destination. (" + outbound_arrival.strftime('%Y-%m-%d %H:%M') + " " + dest_tz.tzname(outbound_arrival) + ")")
            continue
          self.cur.execute("UPDATE Flights SET outboundDate = ?, outboundTime = ? WHERE flightID = ?", (outbound_date, outbound_time, flight_id))
          self.cur.execute("UPDATE Flights SET inboundDate = ?, inboundTime = ? WHERE flightID = ?", (inbound_date, inbound_time, flight_id))
        elif choice == "6":
          status = input("\nEnter new Flight Status: ")
          self.cur.execute("UPDATE Flights SET status = ? WHERE flightID = ?", (status, flight_id))
        else:
          print("\nInvalid choice.")
          continue
        self.conn.commit()
        print("\nFlight details updated successfully. Please review the updated details in case further changes are needed:")
        valid_input = True
      except ValueError:
        print("\nInvalid input. Please use the correct format.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def delete_flight(self):
    valid_input = False
    while valid_input == False:
      try:
        flight_id = int(input("\nEnter Flight ID to delete or 0 to cancel: "))
        if flight_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Flights WHERE flightID = ?", (flight_id,))
        flight = self.cur.fetchone()
        if not flight:
          print("\nNo flight found with the specified ID.")
          return
        confirm = input("\nAre you sure you want to delete this flight? (y/n): ")
        if confirm.lower() == 'y':
          self.cur.execute("DELETE FROM Flights WHERE flightID = ?", (flight_id,))
          self.conn.commit()
          print("\nFlight deleted successfully.")
          valid_input = True
        else:
          print("\nOperation cancelled.")
          MenuNavigation.MenuNavigation().next_menu()
      except ValueError:
        print("\nInvalid Flight ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def add_new_pilot(self):
    first_name = input("\nEnter Pilot's First Name or 0 to cancel: ")
    if first_name == "0":
      print("\nOperation cancelled.")
      return
    last_name = input("\nEnter Pilot's Last Name or 0 to cancel: ")
    if last_name == "0":
      print("\nOperation cancelled.")
      return
    self.cur.execute("INSERT INTO Pilots (firstName, lastName) VALUES (?, ?)", (first_name, last_name))
    self.conn.commit()
    print("\nNew pilot added successfully.")
    MenuNavigation.MenuNavigation().next_menu()

  def update_pilot(self):
    valid_input = False
    while valid_input == False: 
      try:     
        self.show_pilots()
        pilot_id = int(input("\nEnter Pilot ID to update or 0 to cancel: "))
        if pilot_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Pilots WHERE pilotID = ?", (pilot_id,))
        pilot = self.cur.fetchone()
        if not pilot:
          print("\nNo pilot found with the specified ID.")
          return
        print("\nCurrent Pilot Details:")
        print(f"Pilot ID: {pilot['pilotID']}, Name: {pilot['firstName']} {pilot['lastName']}")
        first_name = input("\nEnter new First Name or press Enter to keep current: ")
        last_name = input("\nEnter new Last Name or press Enter to keep current: ")
        if first_name.strip() == "":
          first_name = pilot['firstName']
        if last_name.strip() == "":
          last_name = pilot['lastName']
        self.cur.execute("UPDATE Pilots SET firstName = ?, lastName = ? WHERE pilotID = ?", (first_name, last_name, pilot_id))
        self.conn.commit()
        print("\nPilot details updated successfully.")
        valid_input = True
      except ValueError:
        print("\nInvalid input. Please enter a valid Pilot ID.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def delete_pilot(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_pilots()
        pilot_id = int(input("\nEnter Pilot ID to delete or 0 to cancel: "))
        if pilot_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Pilots WHERE pilotID = ?", (pilot_id,))
        pilot = self.cur.fetchone()
        if not pilot:
          print("\nNo pilot found with the specified ID.")
          return
        self.cur.execute("SELECT * FROM Flights WHERE pilot = ? OR coPilot = ?", (pilot_id, pilot_id))
        flights = self.cur.fetchall()
        if flights:
          print("\nCannot delete pilot. The pilot is assigned to the following flights:")
          for flight in flights:
            print(f"Flight ID: {flight['flightID']}")
          print("\nPlease reassign or delete these flights before deleting the pilot.")
          return
        confirm = input("\nAre you sure you want to delete this pilot? (y/n): ")
        if confirm.lower() == 'y':
          self.cur.execute("DELETE FROM Pilots WHERE pilotID = ?", (pilot_id,))
          self.conn.commit()
          print("\nPilot deleted successfully.")
          valid_input = True
        else:
          print("\nOperation cancelled.")
          MenuNavigation.MenuNavigation().next_menu()
      except ValueError:
        print("\nInvalid Pilot ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def view_pilot_schedule(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_pilots()
        pilot_id = int(input("\nEnter Pilot ID to view schedule or 0 to cancel: "))
        if pilot_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("""SELECT flightID, base.stationName AS baseStation, base.timeZone AS baseTimezone,
                            dest.stationName AS destStation, dest.timeZone AS destTimezone, aircraftModel,
                            p1.firstName AS pilotFirstName, p1.lastName AS pilotLastName, p2.firstName AS coPilotFirstName,
                            p2.lastName AS coPilotLastName, outboundDate, outboundTime, inboundDate, inboundTime, flightTime, status
                            FROM Flights
                            JOIN Routes ON Flights.route = Routes.routeID
                            JOIN Stations AS base ON Routes.routeBase = base.stationID
                            JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                            JOIN Aircraft ON Flights.aircraft = Aircraft.aircraftID
                            JOIN Pilots AS p1 ON Flights.pilot = p1.pilotID
                            JOIN Pilots AS p2 ON Flights.coPilot = p2.pilotID
                            WHERE pilot = ? OR coPilot = ?""", (pilot_id, pilot_id))
        flights = self.cur.fetchall()
        if not flights:
          print("\nNo flights found for the specified pilot.")
          return
        for flight in flights:
          self.print_flight_details(flight)
      except ValueError:
        print("\nInvalid Pilot ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def add_new_aircraft(self):
    model = input("\nEnter Aircraft Model or 0 to cancel: ")
    if model == "0":
      print("\nOperation cancelled.")
      return
    while True:
      try:
        capacity = int(input("\nEnter Aircraft Capacity or 0 to cancel: "))
        if capacity == 0:
          print("\nOperation cancelled.")
          return
        break
      except ValueError:
        print("\nInvalid input. Please enter a valid integer for capacity.")
    self.cur.execute("INSERT INTO Aircraft (aircraftModel, capacity) VALUES (?, ?)", (model, capacity))
    self.conn.commit()
    print("\nNew aircraft added successfully.")
    MenuNavigation.MenuNavigation().next_menu() 

  def update_aircraft(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_aircraft()
        aircraft_id = int(input("\nEnter Aircraft ID to update or 0 to cancel: "))
        if aircraft_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Aircraft WHERE aircraftID = ?", (aircraft_id,))
        aircraft = self.cur.fetchone()
        if not aircraft:
          print("\nNo aircraft found with the specified ID.")
          return
        print("\nCurrent Aircraft Details:")
        print(f"Aircraft ID: {aircraft['aircraftID']}, Model: {aircraft['aircraftModel']}, Capacity: {aircraft['capacity']}")
        model = input("\nEnter new Model or press Enter to keep current: ")
        capacity_input = input("\nEnter new Capacity or press Enter to keep current: ")
        if model.strip() == "":
          model = aircraft['aircraftModel']
        if capacity_input.strip() == "":
          capacity = aircraft['capacity']
        else:
          try:
            capacity = int(capacity_input)
          except ValueError:
            print("\nInvalid input. Please enter a valid integer for capacity.")
            return
        self.cur.execute("UPDATE Aircraft SET aircraftModel = ?, capacity = ? WHERE aircraftID = ?", (model, capacity, aircraft_id))
        self.conn.commit()
        print("\nAircraft details updated successfully.")
        valid_input = True
      except ValueError:
        print("\nInvalid input. Please enter a valid Aircraft ID.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def delete_aircraft(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_aircraft()
        aircraft_id = int(input("\nEnter Aircraft ID to delete or 0 to cancel: "))
        if aircraft_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Aircraft WHERE aircraftID = ?", (aircraft_id,))
        aircraft = self.cur.fetchone()
        if not aircraft:
          print("\nNo aircraft found with the specified ID.")
          return
        self.cur.execute("SELECT * FROM Flights WHERE aircraft = ?", (aircraft_id,))
        flights = self.cur.fetchall()
        if flights:
          print("\nCannot delete aircraft. The aircraft is assigned to the following flights:")
          for flight in flights:
            print(f"Flight ID: {flight['flightID']}")
          print("\nPlease reassign or delete these flights before deleting the aircraft.")
          return
        confirm = input("\nAre you sure you want to delete this aircraft? (y/n): ")
        if confirm.lower() == 'y':
          self.cur.execute("DELETE FROM Aircraft WHERE aircraftID = ?", (aircraft_id,))
          self.conn.commit()
          print("\nAircraft deleted successfully.")
          valid_input = True
        else:
          print("\nOperation cancelled.")
          MenuNavigation.MenuNavigation().next_menu()
      except ValueError:
        print("\nInvalid Aircraft ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def add_new_station(self):
    station_name = input("\nEnter Station Name or 0 to cancel: ")
    if station_name == "0":
      print("\nOperation cancelled.")
      return
    self.cur.execute("SELECT stationName FROM Stations")
    existing_stations = [row[0] for row in self.cur.fetchall()]
    if station_name in existing_stations:
      print("\nStation name already exists. Please enter a unique station name.")
      return
    time_zone = input("\nEnter Time Zone (e.g., America/New_York) or 0 to cancel: ")
    if time_zone == "0":
      print("\nOperation cancelled.")
      return
    try:
      zoneinfo.ZoneInfo(time_zone)
    except Exception:
      print("\nInvalid time zone format. Please enter a valid time zone.")
      return
    self.cur.execute("INSERT INTO Stations (stationName, timeZone) VALUES (?, ?)", (station_name, time_zone))
    self.conn.commit()
    print("\nNew station added successfully.")
    MenuNavigation.MenuNavigation().next_menu()

  def update_station(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_stations()
        station_id = int(input("\nEnter Station ID to update or 0 to cancel: "))
        if station_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Stations WHERE stationID = ?", (station_id,))
        station = self.cur.fetchone()
        if not station:
          print("\nNo station found with the specified ID.")
          return
        print("\nCurrent Station Details:")
        print(f"Station ID: {station['stationID']}, Name: {station['stationName']}, Time Zone: {station['timeZone']}")
        station_name = input("\nEnter new Station Name or press Enter to keep current: ")
        time_zone = input("\nEnter new Time Zone (e.g., America/New_York) or press Enter to keep current: ")
        if station_name.strip() == "":
          station_name = station['stationName']
        else:
          self.cur.execute("SELECT stationName FROM Stations")
          existing_stations = [row[0] for row in self.cur.fetchall()]
          if station_name in existing_stations:
            print("\nStation name already exists. Please enter a unique station name.")
            return
        if time_zone.strip() == "":
          time_zone = station['timeZone']
        else:
          try:
            zoneinfo.ZoneInfo(time_zone)
          except Exception:
            print("\nInvalid time zone format. Please enter a valid time zone.")
            return
        self.cur.execute("UPDATE Stations SET stationName = ?, timeZone = ? WHERE stationID = ?", (station_name, time_zone, station_id))
        self.conn.commit()
        print("\nStation details updated successfully.")
        valid_input = True
      except ValueError:
        print("\nInvalid input. Please enter a valid Station ID.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()

  def delete_station(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_stations()
        station_id = int(input("\nEnter Station ID to delete or 0 to cancel: "))
        if station_id == 0:
          print("\nOperation cancelled.")
          return
        self.cur.execute("SELECT * FROM Stations WHERE stationID = ?", (station_id,))
        station = self.cur.fetchone()
        if not station:
          print("\nNo station found with the specified ID.")
          return
        self.cur.execute("""SELECT Flights.flightID FROM Flights
                            JOIN Routes ON Flights.route = Routes.routeID
                            WHERE Routes.routeBase = ? OR Routes.routeDestination = ?""", (station_id, station_id))
        flights = self.cur.fetchall()
        if flights:
          print("\nCannot delete station. The station is associated with the following flights:")
          for flight in flights:
            print(f"Flight ID: {flight['flightID']}")
          print("\nPlease reassign or delete these flights before deleting the station.")
          return
        confirm = input("\nAre you sure you want to delete this station? (y/n): ")
        if confirm.lower() == 'y':
          self.cur.execute("DELETE FROM Stations WHERE stationID = ?", (station_id,))
          self.conn.commit()
          print("\nStation deleted successfully.")
          valid_input = True
        else:
          print("\nOperation cancelled.")
          MenuNavigation.MenuNavigation().next_menu()
      except ValueError:
        print("\nInvalid Station ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()
      
  def show_routes(self):
    self.cur.execute("""SELECT Routes.routeID, base.stationName AS baseStation, dest.stationName AS destStation, flightTime
                        FROM Routes
                        JOIN Stations AS base ON Routes.routeBase = base.stationID
                        JOIN Stations AS dest ON Routes.routeDestination = dest.stationID""")
    routes = self.cur.fetchall()
    print("\nAvailable Routes:\n")
    for route in routes:
      print(f"Route ID: {route['routeID']}, From: {route['baseStation']} To: {route['destStation']}, Flight Time: {route['flightTime']} hours")

  def add_new_route(self):
    try:
      self.show_stations()
      route_dest_id = int(input("\nEnter Destination Station ID or 0 to cancel: "))
      if route_dest_id == 0:
        print("\nOperation cancelled.\n")
        return
      if route_dest_id == 1:
        print("\nBase and destination stations cannot be the same.")
        return
      self.cur.execute("SELECT stationID FROM Stations")
      station_ids = [row[0] for row in self.cur.fetchall()]
      if route_dest_id not in station_ids:
        print("\nInvalid Station ID.\n")
        return
      self.cur.execute("SELECT routeDestination FROM Routes WHERE routeDestination = ?", (route_dest_id,))
      existing_route = self.cur.fetchone()
      if existing_route:
        print("\nA route to this destination already exists.")
        return
      flight_time = float(input("\nEnter Flight Time in hours (e.g., 2.5) or 0 to cancel: "))
      if flight_time == 0:
        print("\nOperation cancelled.\n")
        return
    except ValueError:
      print("\nInvalid input. Please enter valid integers for station IDs and a valid number for flight time.")
      return
    self.cur.execute("INSERT INTO Routes (routeDestination, flightTime) VALUES (?, ?)", (route_dest_id, flight_time))
    self.conn.commit()
    print("\nNew route added successfully.")
    MenuNavigation.MenuNavigation().next_menu()

  def update_route(self):
    valid_input = False
    try:
      while valid_input == False:
        self.show_routes()
        route_id = int(input("\nEnter Route ID to update or 0 to cancel: "))
        if route_id == 0:
          print("\nOperation cancelled.\n")
          return
        self.cur.execute("SELECT * FROM Routes WHERE routeID = ?", (route_id,))
        route_row = self.cur.fetchone()
        if not route_row:
          print("\nNo route found with the specified ID.\n")
          return
        self.cur.execute("SELECT * FROM Flights WHERE route = ?", (route_id,))
        flights = self.cur.fetchall()
        if flights:
          print("\nCannot amend route. The route is associated with the following flights:")
          for flight in flights:
            print(f"Flight ID: {flight['flightID']}")
          print("\nPlease reassign or delete these flights before amending the route.")
          return
        self.show_stations()
        route_dest_id = int(input("\nEnter new Destination Station ID or 0 to cancel: "))
        if route_dest_id == 0:
          print("\nOperation cancelled.\n")
          return
        if route_dest_id == 1:
          print("\nBase and destination stations cannot be the same.")
          return
        self.cur.execute("SELECT stationID FROM Stations")
        station_ids = [row[0] for row in self.cur.fetchall()]
        if route_dest_id not in station_ids:
          print("\nInvalid Station ID.\n")
          return
        self.cur.execute("SELECT routeDestination FROM Routes WHERE routeDestination = ? AND routeID != ?", (route_dest_id, route_id))
        existing_route = self.cur.fetchone()
        if existing_route:
          print("\nA route to this destination already exists.")
          return
        flight_time = float(input("\nEnter new Flight Time in hours (e.g., 2.5) or 0 to cancel: "))
        if flight_time == 0:
          print("\nOperation cancelled.\n")
          return
        self.cur.execute("UPDATE Routes SET routeDestination = ?, flightTime = ? WHERE routeID = ?", (route_dest_id, flight_time, route_id))
        self.conn.commit()
        print("\nRoute details updated successfully.")
        valid_input = True
    except ValueError:
      print("\nInvalid input. Please enter valid integers for station IDs and a valid number for flight time.")
      return
    except Exception as e:
      print(e)
    finally:
      MenuNavigation.MenuNavigation().next_menu()

  def delete_route(self):
    valid_input = False
    while valid_input == False:
      try:
        self.show_routes()
        route_id = int(input("\nEnter Route ID to delete or 0 to cancel: "))
        if route_id == 0:
          print("\nOperation cancelled.\n")
          return
        self.cur.execute("SELECT * FROM Routes WHERE routeID = ?", (route_id,))
        route_row = self.cur.fetchone()
        if not route_row:
          print("\nNo route found with the specified ID.\n")
          return
        self.cur.execute("SELECT * FROM Flights WHERE route = ?", (route_id,))
        flights = self.cur.fetchall()
        if flights:
          print("\nCannot delete route. The route is associated with the following flights:")
          for flight in flights:
            print(f"Flight ID: {flight['flightID']}")
          print("\nPlease reassign or delete these flights before deleting the route.")
          return
        confirm = input("\nAre you sure you want to delete this route? (y/n): ")
        if confirm.lower() == 'y':
          self.cur.execute("DELETE FROM Routes WHERE routeID = ?", (route_id,))
          self.conn.commit()
          print("\nRoute deleted successfully.")
          valid_input = True
        else:
          print("\nOperation cancelled.")
          MenuNavigation.MenuNavigation().next_menu()
      except ValueError:
        print("\nInvalid Route ID. Please enter a valid integer.")
        return
      except Exception as e:
        print(e)
      finally:
        MenuNavigation.MenuNavigation().next_menu()