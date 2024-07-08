from dtgraph.scenarios.scenario import Scenario

class iBenchAmalgam1ToAmalgam3(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_inproceedings_cmd = """MERGE (n:InProceedings {
            inprocid: row[1], 
            title: row[2],
            bktitle: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        inproceedings_filepath = "file:///a1ta3/inproceedings"+str(size)+"-5.csv"
        graph.populate_with_csv(inproceedings_filepath, rel_inproceedings_cmd, stats=True)
        # csv#2
        rel_article_cmd = """MERGE (n:Article {
            articleid: row[1], 
            title: row[2],
            journal: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        article_filepath = "file:///a1ta3/article"+str(size)+"-5.csv"
        graph.populate_with_csv(article_filepath, rel_article_cmd, stats=True)
        # csv#3
        rel_techreport_cmd = """MERGE (n:TechReport {
            techid: row[1],
            title: row[2],
            inst: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        techreport_filepath = "file:///a1ta3/techreport"+str(size)+"-5.csv"
        graph.populate_with_csv(techreport_filepath, rel_techreport_cmd, stats=True)
        # csv#4
        rel_book_cmd = """MERGE (n:Book {
            bookid: row[1],
            title: row[2],
            publisher: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        book_filepath = "file:///a1ta3/book"+str(size)+"-5.csv"
        graph.populate_with_csv(book_filepath, rel_book_cmd, stats=True)
        # csv#5
        rel_incollection_cmd = """MERGE (n:InCollection {
            colid: row[1],
            title: row[2],
            bktitle: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        incollection_filepath = "file:///a1ta3/incollection"+str(size)+"-5.csv"
        graph.populate_with_csv(incollection_filepath, rel_incollection_cmd, stats=True)
        # csv#6
        rel_misc_cmd = """MERGE (n:Misc {
            miscid: row[1],
            title: row[2],
            howpub: row[3],
            confloc: row[4],
            year: row[5],
            month: row[6],
            pages: row[7],
            vol: row[8],
            num: row[9],
            loc: row[10],
            class: row[11],
            note: row[12],
            annote: row[13]
        })"""
        misc_filepath = "file:///a1ta3/misc"+str(size)+"-5.csv"
        graph.populate_with_csv(misc_filepath, rel_misc_cmd, stats=True)
        # csv#7
        rel_manual_cmd = """MERGE (n:Manual {
            manid: row[1],
            title: row[2],
            org: row[3],
            year: row[4],
            month: row[5],
            pages: row[6],
            vol: row[7],
            num: row[8],
            loc: row[9],
            class: row[10],
            note: row[11],
            annote: row[12]
        })"""
        manual_filepath = "file:///a1ta3/manual"+str(size)+"-5.csv"
        graph.populate_with_csv(manual_filepath, rel_manual_cmd, stats=True)
        # csv#8
        rel_author_cmd = """MERGE (n:Author {
            authid: row[1],
            name: row[2]
        })"""
        author_filepath = "file:///a1ta3/author"+str(size)+"-5.csv"
        graph.populate_with_csv(author_filepath, rel_author_cmd, stats=True)
        # csv#9
        rel_inprocpublished_cmd = """MERGE (n:InProcPublished {
            inproc: row[1],
            auth: row[2]
        })"""
        inprocpublished_filepath = "file:///a1ta3/inprocpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(inprocpublished_filepath, rel_inprocpublished_cmd, stats=True)
        # csv#10
        rel_articlepublished_cmd = """MERGE (n:ArticlePublished {
            article: row[1],
            auth: row[2]
        })"""
        articlepublished_filepath = "file:///a1ta3/articlepublished"+str(size)+"-5.csv"
        graph.populate_with_csv(articlepublished_filepath, rel_articlepublished_cmd, stats=True)
        # csv#11
        rel_techpublished_cmd = """MERGE (n:TechPublished {
            tech: row[1],
            auth: row[2]
        })"""
        techpublished_filepath = "file:///a1ta3/techpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(techpublished_filepath, rel_techpublished_cmd, stats=True)
        # csv#12
        rel_bookpublished_cmd = """MERGE (n:BookPublished {
            book: row[1],
            auth: row[2]
        })"""
        bookpublished_filepath = "file:///a1ta3/bookpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(bookpublished_filepath, rel_bookpublished_cmd, stats=True)
        # csv#13
        rel_incollpublished_cmd = """MERGE (n:InCollPublished {
            col: row[1],
            auth: row[2]
        })"""
        incollpublished_filepath = "file:///a1ta3/incollpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(incollpublished_filepath, rel_incollpublished_cmd, stats=True)
        # csv#14
        rel_miscpublished_cmd = """MERGE (n:MiscPublished {
            misc: row[1],
            auth: row[2]
        })"""
        miscpublished_filepath = "file:///a1ta3/miscpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(miscpublished_filepath, rel_miscpublished_cmd, stats=True)
        # csv#15
        rel_manualpublished_cmd = """MERGE (n:ManualPublished {
            manual: row[1],
            auth: row[2]
        })"""
        manualpublished_filepath = "file:///a1ta3/manualpublished"+str(size)+"-5.csv"
        graph.populate_with_csv(manualpublished_filepath, rel_manualpublished_cmd, stats=True)
