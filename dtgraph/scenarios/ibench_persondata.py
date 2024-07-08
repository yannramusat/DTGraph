from dtgraph.scenarios.scenario import Scenario

class iBenchPersonData(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_person_cmd = "MERGE (n:Person {name: row[1], address: row[2]})"
        person_filepath = "file:///persondata/person"+str(size)+"-5.csv"
        graph.populate_with_csv(person_filepath, rel_person_cmd, stats=True)
        # csv#2
        rel_address_cmd = "MERGE (n:Address {occ: row[1], city: row[2]})"
        address_filepath = "file:///persondata/address"+str(size)+"-5.csv"
        graph.populate_with_csv(address_filepath, rel_address_cmd, stats=True)
        # csv#3
        rel_place_cmd = "MERGE (n:Place {occ: row[1], zip: row[2]})"
        place_filepath = "file:///persondata/place"+str(size)+"-5.csv"
        graph.populate_with_csv(place_filepath, rel_place_cmd, stats=True)