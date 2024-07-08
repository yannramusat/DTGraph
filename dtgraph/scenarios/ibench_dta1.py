from dtgraph.scenarios.scenario import Scenario

class iBenchDBLPToAmalgam1(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_dinproceedings_cmd = """MERGE (n:DInProceedings {
            pid: row[1], 
            title: row[2],
            pages: row[3],
            booktitle: row[4],
            url: row[5],
            cdrom: row[6],
            month: row[7],
            year: row[8]
        })"""
        dinproceedings_filepath = "file:///dta1/dinproceedings"+str(size)+"-5.csv"
        graph.populate_with_csv(dinproceedings_filepath, rel_dinproceedings_cmd, stats=True)
        # csv#2
        rel_darticle_cmd = """MERGE (n:DArticle {
            pid: row[1], 
            title: row[2], 
            pages: row[3], 
            cdrom: row[4], 
            month: row[5], 
            year: row[6], 
            volume: row[7], 
            journal: row[8], 
            number: row[9], 
            url: row[10]
        })"""
        darticle_filepath = "file:///dta1/darticle"+str(size)+"-5.csv"
        graph.populate_with_csv(darticle_filepath, rel_darticle_cmd, stats=True)
        # csv#3
        rel_pubauthors_cmd = """MERGE (n:PubAuthors {
            pid: row[1],
            author: row[2]
        })"""
        pubauthors_filepath = "file:///dta1/pubauthors"+str(size)+"-5.csv"
        graph.populate_with_csv(pubauthors_filepath, rel_pubauthors_cmd, stats=True)
        # csv#4
        rel_dbook_cmd = """MERGE (n:DBook {
            pid: row[1],
            editor: row[2],
            title: row[3],
            publisher: row[4],
            year: row[5],
            isbn: row[6],
            cdrom: row[7],
            citel: row[8],
            url: row[9]
        })"""
        dbook_filepath = "file:///dta1/dbook"+str(size)+"-5.csv"
        graph.populate_with_csv(dbook_filepath, rel_dbook_cmd, stats=True)
        # csv#5
        rel_masterthesis_cmd = """MERGE (n:MasterThesis {
            author: row[1],
            title: row[2],
            year: row[3],
            school: row[4]
        })"""
        masterthesis_filepath = "file:///dta1/masterthesis"+str(size)+"-5.csv"
        graph.populate_with_csv(masterthesis_filepath, rel_masterthesis_cmd, stats=True)
        # csv#6
        rel_phdthesis_cmd = """MERGE (n:PhDThesis {
            author: row[1],
            title: row[2],
            year: row[3],
            series: row[4],
            number: row[5],
            month: row[6],
            school: row[7],
            publisher: row[8],
            isbn: row[9]
        })"""
        phdthesis_filepath = "file:///dta1/phdthesis"+str(size)+"-5.csv"
        graph.populate_with_csv(phdthesis_filepath, rel_phdthesis_cmd, stats=True)
        # csv#7
        rel_www_cmd = """MERGE (n:WWW {
            pid: row[1],
            title: row[2],
            year: row[3],
            url: row[4]
        })"""
        www_filepath = "file:///dta1/www"+str(size)+"-5.csv"
        graph.populate_with_csv(www_filepath, rel_www_cmd, stats=True)