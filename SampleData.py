import sqlite3
import datetime

class SampleData:

    def get_connection(self):
        self.conn = sqlite3.connect("FlightManager.db")
        self.cur = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row # Use row factory to access columns by name

    def seed_sample_data(self):
        # Populate sample data
        try:
            self.get_connection()
            self.cur.execute("SELECT COUNT(*) FROM Stations")
            if self.cur.fetchone()[0] > 0:
                return

            stations = [
                ("London Heathrow", "BST"),
                ("John F. Kennedy International Airport", "EDT"),
                ("Dubai International Airport", "GST"),
                ("Tokyo Narita International Airport", "JST"),
                ("Sydney Kingsford Smith Airport", "AEST"),
                ("Paris Charles de Gaulle Airport", "CEST")
            ]
            self.cur.executemany(
                "INSERT INTO Stations (stationName, timeZone) VALUES (?, ?)",
                stations
            )

            aircraft = [
                ("Boeing 737-700", 138),
                ("Boeing 737-800", 162),
                ("Boeing 737-900", 180),
                ("Boeing 737 MAX 8", 178),
                ("Boeing 737 MAX 9", 193),
                ("Boeing 737-700", 138),
                ("Boeing 737-800", 162),
                ("Boeing 737-900", 180)
            ]
            self.cur.executemany(
                "INSERT INTO Aircraft (aircraftModel, capacity) VALUES (?, ?)",
                aircraft
            )

            pilots = [
                ("Amelia", "Earhart"),
                ("Charles", "Lindbergh"),
                ("Bessie", "Coleman"),
                ("Howard", "Hughes"),
                ("Jacqueline", "Cochran"),
                ("Chuck", "Yeager"),
                ("Sally", "Ride"),
                ("Neil", "Armstrong"),
                ("Valentina", "Tereshkova"),
                ("Yuri", "Gagarin"),
                ("Wally", "Funk"),
                ("John", "Glenn"),
                ("James", "Doolittle"),
                ("Hanna", "Reitsch"),
                ("Jean", "Batten"),
                ("Robert", "Taylor")
            ]
            self.cur.executemany(
                "INSERT INTO Pilots (firstName, lastName) VALUES (?, ?)",
                pilots
            )

            self.conn.commit()

            self.cur.execute("SELECT stationID, stationName FROM Stations")
            station_map = {name: station_id for station_id, name in self.cur.fetchall()}

            routes = [
                (station_map["London Heathrow"], station_map["John F. Kennedy International Airport"], 8),
                (station_map["London Heathrow"], station_map["Dubai International Airport"], 7),
                (station_map["London Heathrow"], station_map["Tokyo Narita International Airport"], 11),
                (station_map["London Heathrow"], station_map["Sydney Kingsford Smith Airport"], 22),
                (station_map["London Heathrow"], station_map["Paris Charles de Gaulle Airport"], 1)
            ]
            self.cur.executemany(
                "INSERT INTO Routes (routeBase, routeDestination, flightTime) VALUES (?, ?, ?)",
                routes
            )
            self.conn.commit()

            self.cur.execute("SELECT routeID, stationName FROM Routes JOIN Stations ON routeDestination = stationID")
            route_map = {station_name: route_id for route_id, station_name in self.cur.fetchall()}

            self.cur.execute("SELECT aircraftID FROM Aircraft")
            aircraft_ids = [row[0] for row in self.cur.fetchall()]
            self.cur.execute("SELECT pilotID FROM Pilots")
            pilot_ids = [row[0] for row in self.cur.fetchall()]

            flights = [
                (route_map["John F. Kennedy International Airport"], aircraft_ids[0], pilot_ids[0], pilot_ids[1], "2026-08-01", "06:00", "2026-08-01", "09:00", "Scheduled"),
                (route_map["Dubai International Airport"], aircraft_ids[1], pilot_ids[2], pilot_ids[3], "2026-08-01", "07:00", "2026-08-01", "17:00", "Scheduled"),
                (route_map["Tokyo Narita International Airport"], aircraft_ids[2], pilot_ids[4], pilot_ids[5], "2026-08-01", "08:00", "2026-08-02", "09:00", "Scheduled"),
                (route_map["Sydney Kingsford Smith Airport"], aircraft_ids[3], pilot_ids[6], pilot_ids[7], "2026-08-01", "09:00", "2026-08-03", "07:00", "Scheduled"),
                (route_map["Paris Charles de Gaulle Airport"], aircraft_ids[4], pilot_ids[8], pilot_ids[9], "2026-08-01", "10:00", "2026-08-01", "12:00", "Scheduled"),
                (route_map["John F. Kennedy International Airport"], aircraft_ids[5], pilot_ids[10], pilot_ids[11], "2026-08-02", "06:00", "2026-08-02", "09:00", "Scheduled"),
                (route_map["Dubai International Airport"], aircraft_ids[6], pilot_ids[12], pilot_ids[13], "2026-08-02", "07:00", "2026-08-02", "17:00", "Scheduled"),
                (route_map["Tokyo Narita International Airport"], aircraft_ids[7], pilot_ids[14], pilot_ids[15], "2026-08-02", "08:00", "2026-08-03", "09:00", "Scheduled"),
                (route_map["Sydney Kingsford Smith Airport"], aircraft_ids[0], pilot_ids[0], pilot_ids[1], "2026-08-03", "10:00", "2026-08-05", "07:00", "Scheduled"),
                (route_map["Paris Charles de Gaulle Airport"], aircraft_ids[1], pilot_ids[2], pilot_ids[3], "2026-08-02", "13:00", "2026-08-02", "15:00", "Scheduled")
            ]
            self.cur.executemany(
                "INSERT INTO Flights (route, aircraft, pilot, coPilot, outboundDate, outboundTime, inboundDate, inboundTime, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                flights
            )
            self.conn.commit()
            print ("Sample data inserted successfully.")
        except Exception as e:
            print("Error seeding sample data: " + str(e))
            self.conn.rollback()
            import traceback
            traceback.print_exc()  
        finally:
            self.conn.row_factory = None
            self.conn.close()
            