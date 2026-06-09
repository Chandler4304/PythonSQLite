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
                ("London Heathrow", "Europe/London"),
                ("New York John F. Kennedy International Airport", "America/New_York"),
                ("Dubai International Airport", "Asia/Dubai"),
                ("Tokyo Narita International Airport", "Asia/Tokyo"),
                ("Sydney Kingsford Smith Airport", "Australia/Sydney"),
                ("Paris Charles de Gaulle Airport", "Europe/Paris")
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
                (station_map["London Heathrow"], station_map["New York John F. Kennedy International Airport"], 8),
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

            flight_schedule = [
                (route_map["New York John F. Kennedy International Airport"], aircraft_ids[0], pilot_ids[0], pilot_ids[1], datetime.datetime(2026, 8, 1, 6, 0), datetime.datetime(2026, 8, 1, 10, 0), "Scheduled"),
                (route_map["Dubai International Airport"], aircraft_ids[1], pilot_ids[2], pilot_ids[3], datetime.datetime(2026, 8, 1, 7, 0), datetime.datetime(2026, 8, 1, 18, 0), "Scheduled"),
                (route_map["Tokyo Narita International Airport"], aircraft_ids[2], pilot_ids[4], pilot_ids[5], datetime.datetime(2026, 8, 1, 8, 0), datetime.datetime(2026, 8, 2, 9, 0), "Scheduled"),
                (route_map["Sydney Kingsford Smith Airport"], aircraft_ids[3], pilot_ids[6], pilot_ids[7], datetime.datetime(2026, 8, 1, 9, 0), datetime.datetime(2026, 8, 3, 7, 0), "Scheduled"),
                (route_map["Paris Charles de Gaulle Airport"], aircraft_ids[4], pilot_ids[8], pilot_ids[9], datetime.datetime(2026, 8, 1, 10, 0), datetime.datetime(2026, 8, 1, 13, 0), "Scheduled"),
                (route_map["New York John F. Kennedy International Airport"], aircraft_ids[5], pilot_ids[10], pilot_ids[11], datetime.datetime(2026, 8, 2, 6, 0), datetime.datetime(2026, 8, 2, 10, 0), "Scheduled"),
                (route_map["Dubai International Airport"], aircraft_ids[6], pilot_ids[12], pilot_ids[13], datetime.datetime(2026, 8, 2, 7, 0), datetime.datetime(2026, 8, 2, 18, 0), "Scheduled"),
                (route_map["Tokyo Narita International Airport"], aircraft_ids[7], pilot_ids[14], pilot_ids[15], datetime.datetime(2026, 8, 2, 8, 0), datetime.datetime(2026, 8, 3, 9, 0), "Scheduled"),
                (route_map["Sydney Kingsford Smith Airport"], aircraft_ids[0], pilot_ids[0], pilot_ids[1], datetime.datetime(2026, 8, 3, 10, 0), datetime.datetime(2026, 8, 5, 7, 0), "Scheduled"),
                (route_map["Paris Charles de Gaulle Airport"], aircraft_ids[1], pilot_ids[2], pilot_ids[3], datetime.datetime(2026, 8, 2, 13, 0), datetime.datetime(2026, 8, 2, 16, 0), "Scheduled")
            ]

            flights = [
                (
                    route,
                    aircraft,
                    pilot,
                    coPilot,
                    outbound_dt.strftime("%Y-%m-%d"),
                    outbound_dt.strftime("%H:%M"),
                    inbound_dt.strftime("%Y-%m-%d"),
                    inbound_dt.strftime("%H:%M"),
                    status
                )
                for route, aircraft, pilot, coPilot, outbound_dt, inbound_dt, status in flight_schedule
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
            