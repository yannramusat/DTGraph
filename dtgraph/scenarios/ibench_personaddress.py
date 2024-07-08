from dtgraph.scenarios.scenario import Scenario

class iBenchPersonAddress(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_address_cmd = "MERGE (n:Address {zip: row[1], city: row[2]})"
        address_filepath = "file:///personaddress/address"+str(size)+"-5.csv"
        graph.populate_with_csv(address_filepath, rel_address_cmd, stats=True)
        # csv#2
        rel_person_cmd = "MERGE (n:Person {name: row[1], address: row[2]})"
        person_filepath = "file:///personaddress/person"+str(size)+"-5.csv"
        graph.populate_with_csv(person_filepath, rel_person_cmd, stats=True)