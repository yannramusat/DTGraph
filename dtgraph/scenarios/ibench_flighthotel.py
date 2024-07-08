from dtgraph.scenarios.scenario import Scenario

class iBenchFlightHotel(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_flight_cmd = "MERGE (n:Flight {fid: row[1], src: row[2], dest: row[3]})"
        flight_filepath = "file:///flighthotel/flight"+str(size)+"-5.csv"
        graph.populate_with_csv(flight_filepath, rel_flight_cmd, stats=True)
        # csv#2
        rel_hotel_cmd = "MERGE (n:Hotel {flid: row[1], hid: row[2]})"
        hotel_filepath = "file:///flighthotel/hotel"+str(size)+"-5.csv"
        graph.populate_with_csv(hotel_filepath, rel_hotel_cmd, stats=True)