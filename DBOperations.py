import sqlite3

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
      self.cur.execute(self.sql_create_table_firsttime.format("Stations", "stationID INTEGER PRIMARY KEY AUTOINCREMENT, stationName VARCHAR(50), timeZone VARCHAR(10)"))
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
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("FlightManager.db")
    self.conn.row_factory = sqlite3.Row # Use row factory to access columns by name
    self.cur = self.conn.cursor()
    

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
        print("No flights found.")
        return
      for flight in flights:
        print(f"Flight ID: {flight['flightID']}")
        print(f"  From: {flight['baseStation']}")
        print(f"  To: {flight['destStation']}")
        print(f"  Aircraft: {flight['aircraftModel']}")
        print(f"  Pilot: {flight['pilotFirstName']} {flight['pilotLastName']}")
        print(f"  Co-Pilot: {flight['coPilotFirstName']} {flight['coPilotLastName']}")
        print(f"  Outbound: {flight['outboundDate']} {flight['outboundTime']} ({flight['baseTimezone']})")
        print(f"  Arrival: ")
        print(f"  Inbound: {flight['inboundDate']} {flight['inboundTime']} ({flight['destTimezone']})")
        print(f"  Status: {flight['status']}")
        print("-" * 50)
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
      
