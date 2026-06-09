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
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime.format("Aircraft", "aircraftID INTEGER PRIMARY KEY AUTOINCREMENT, aircraftModel VARCHAR(30), capacity INTEGER"))
      self.cur.execute(self.sql_create_table_firsttime.format("Stations", "stationID INTEGER PRIMARY KEY AUTOINCREMENT, stationName VARCHAR(50), timeZone VARCHAR(30)"))
      self.cur.execute(self.sql_create_table_firsttime.format("Pilots", "pilotID INTEGER PRIMARY KEY AUTOINCREMENT, firstName VARCHAR(30), lastName VARCHAR(30)"))
      self.cur.execute(self.sql_create_table_firsttime.format("Routes", "routeID INTEGER PRIMARY KEY AUTOINCREMENT, routeBase INTEGER REFERENCES Stations(stationID), " \
      "                                                 routeDestination INTEGER REFERENCES Stations(stationID), flightTime HOURS"))
      self.cur.execute(self.sql_create_table_firsttime.format("Flights", "flightID INTEGER PRIMARY KEY AUTOINCREMENT, route INTEGER REFERENCES Routes(routeID), " \
      "                                                 aircraft INTEGER REFERENCES Aircraft(aircraftID), pilot INTEGER REFERENCES Pilots(pilotID), " \
      "                                                 coPilot INTEGER REFERENCES Pilots(pilotID), outboundDate DATE, outboundTime TIME, inboundDate DATE, inboundTime TIME, status VARCHAR(30)"))

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
    try:
      self.get_connection()
      self.cur.execute("SELECT * FROM Stations")
      stations = self.cur.fetchall()
      if not stations:
        print("\nNo stations found.")
        return
      for station in stations:
        print(f"Station ID: {station['stationID']}, Name: {station['stationName']}")
    except Exception as e:
      print(e)
    finally:
      self.conn.row_factory = None      
      self.conn.close()

  def show_flights(self):
    try:
      self.get_connection()
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
      self.conn.row_factory = None      
      self.conn.close()
      MenuNavigation.MenuNavigation().next_menu()


  def show_flights_by_destination(self, destination=None):
    try:
      self.show_stations()
      self.get_connection()
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
      self.conn.row_factory = None     
      self.conn.close()
      MenuNavigation.MenuNavigation().next_menu()

  def show_flights_by_date(self):
    try:
      self.get_connection()
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
      self.conn.row_factory = None     
      self.conn.close()
      MenuNavigation.MenuNavigation().next_menu()

  def show_flights_by_status(self):
    try:
      self.get_connection()
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
      self.conn.row_factory = None     
      self.conn.close()
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
    valid_input = False
    while valid_input == False:
      try:
        self.show_stations()
        self.get_connection()
        dest_station_id = int(input("\nEnter Destination Station ID or 0 to cancel: "))
        if dest_station_id == 0:
          print("Operation cancelled.")
          return
        self.cur.execute("""SELECT Routes.routeID, Routes.flightTime, base.timeZone AS baseTimezone, dest.timeZone AS destTimezone
                            FROM Routes
                            JOIN Stations AS base ON Routes.routeBase = base.stationID
                            JOIN Stations AS dest ON Routes.routeDestination = dest.stationID
                            WHERE routeDestination = ?""", (dest_station_id,))
        route_row = self.cur.fetchone()
        if not route_row:
          print("Invalid Station ID.")
          continue

        route_id = route_row['routeID'] if isinstance(route_row, sqlite3.Row) else route_row[0]
        flight_time = route_row['flightTime'] if isinstance(route_row, sqlite3.Row) else route_row[1]
        base_tz = zoneinfo.ZoneInfo(route_row['baseTimezone']) if isinstance(route_row, sqlite3.Row) else zoneinfo.ZoneInfo(route_row[2])
        dest_tz = zoneinfo.ZoneInfo(route_row['destTimezone']) if isinstance(route_row, sqlite3.Row) else zoneinfo.ZoneInfo(route_row[3])

        self.cur.execute("SELECT * FROM Aircraft")
        aircraft_ids = [row[0] for row in self.cur.fetchall()]
        print("\nAvailable Aircraft: \n")
        for row in self.cur.fetchall():
          print(f"  {row[0]}: {row[1]}")
        aircraft_id = int(input("Enter Aircraft ID or 0 to cancel: "))
        if aircraft_id == 0:
          print("Operation cancelled.")
          return
        if aircraft_id not in aircraft_ids:
          print("Invalid Aircraft ID.")
          continue
        self.cur.execute("SELECT * FROM Pilots")
        pilot_ids = [row[0] for row in self.cur.fetchall()]
        print("\nAvailable Pilots: \n")
        for row in self.cur.fetchall():
          print(f"  {row[0]}: {row[1]}")
        pilot_id = int(input("Enter Pilot ID or 0 to cancel: "))
        if pilot_id == 0:
          print("Operation cancelled.")
          return
        if pilot_id not in pilot_ids:
          print("Invalid Pilot ID.")
          continue
        co_pilot_id = int(input("Enter Co-Pilot ID or 0 to cancel: "))
        if co_pilot_id == 0:
          print("Operation cancelled.")
          return
        if co_pilot_id not in pilot_ids:
          print("Invalid Co-Pilot ID.")
          continue
        if co_pilot_id == pilot_id:
          print("Pilot and Co-Pilot cannot be the same person.")
          continue
        outbound_date = input("Enter Outbound Date (Local Time) (YYYY-MM-DD) or 0 to cancel: ")
        if outbound_date == "0":
          print("Operation cancelled.")
          return
        outbound_time = input("Enter Outbound Time (Local Time) (HH:MM) or 0 to cancel: ")
        if outbound_time == "0":
          print("Operation cancelled.")
          return
        inbound_date = input("Enter Inbound Date (Local Time) (YYYY-MM-DD) or 0 to cancel: ")
        if inbound_date == "0":
          print("Operation cancelled.")
          return
        inbound_time = input("Enter Inbound Time (Local Time) (HH:MM) or 0 to cancel: ")
        if inbound_time == "0":
          print("Operation cancelled.")
          return
        outbound_dt = datetime.datetime.strptime(outbound_date + " " + outbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=base_tz)
        outbound_arrival = (outbound_dt + datetime.timedelta(hours=flight_time)).astimezone(dest_tz)
        inbound_dt = datetime.datetime.strptime(inbound_date + " " + inbound_time, '%Y-%m-%d %H:%M').replace(tzinfo=dest_tz)

        if inbound_dt < outbound_arrival + datetime.timedelta(hours=1):
          print("\nInbound departure must be at least 1 hour after outbound arrival at the destination.")
          continue
        
        status = input("Enter Flight Status or 0 to cancel: ")
        if status == "0":
          print("Operation cancelled.")
          return

        self.cur.execute("""INSERT INTO Flights (route, aircraft, pilot, coPilot, outboundDate, outboundTime, inboundDate, inboundTime, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (route_id, aircraft_id, pilot_id, co_pilot_id, outbound_date, outbound_time, inbound_date, inbound_time, status))
        self.conn.commit()
        print("\nNew flight added successfully.")
      except Exception as e:
        print(e)
      finally:
        self.conn.row_factory = None      
        self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert)
      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.row_factory = None
      self.conn.close()
      

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      result = self.cur.fetchall()

      # think how you could develop this method to show the records

    except Exception as e:
      print(e)
    finally:
      self.conn.row_factory = None
      self.conn.close()
      

  def search_data(self):
    try:
      self.get_connection()
      flightID = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple(str(flightID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Origin: " + detail)
          elif index == 2:
            print("Flight Destination: " + detail)
          else:
            print("Status: " + str(detail))
      else:
        print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
      self.conn.row_factory = None

  def update_data(self):
    try:
      self.get_connection()

      # Update statement
      flightID = int(input("Enter FlightID: "))
      new_status = input("Enter new status: ")
      self.cur.execute(self.sql_update_data, tuple(str(new_status) + " WHERE flightID = " + str(flightID)))
      self.conn.commit()
      result = self.cur.fetchall()

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.row_factory = None
      self.conn.close()
      


# Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corresponding record.

  def delete_data(self):
    try:
      self.get_connection()

      flightID = int(input("Enter FlightID to delete: "))
      self.cur.execute(self.sql_delete_data, (flightID,))
      result = self.cur.fetchall()

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.row_factory = None
      self.conn.close()
      
