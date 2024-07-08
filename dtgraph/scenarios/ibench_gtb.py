from dtgraph.scenarios.scenario import Scenario

class iBenchGUSToBIOSQL(Scenario):
    @staticmethod
    def load(graph, size = 1_000):
        graph.flush_database()
        # csv#1
        rel_gusgene_cmd = """MERGE (n:GUSGene {
            geneID: row[1], 
            name: row[2],
            geneSymbol: row[3],
            geneCategoryID: row[4],
            reviewStatusID: row[5],
            description: row[6],
            reviewerSummary: row[7],
            sequenceOntologyID: row[8]
        })"""
        gusgene_filepath = "file:///gtb/gusgene"+str(size)+"-5.csv"
        graph.populate_with_csv(gusgene_filepath, rel_gusgene_cmd, stats=True)
        # csv#2
        rel_gusgenesynonym_cmd = """MERGE (n:GUSGeneSynonym {
            geneSynonymID: row[1], 
            geneID: row[2],
            synonymName: row[3],
            reviewStatusID: row[4],
            isObsolete: row[5]
        })"""
        gusgenesynonym_filepath = "file:///gtb/gusgenesynonym"+str(size)+"-5.csv"
        graph.populate_with_csv(gusgenesynonym_filepath, rel_gusgenesynonym_cmd, stats=True)
        # csv#3
        rel_gusgorelationship_cmd = """MERGE (n:GUSGoRelationship {
            goRelationshipID: row[1], 
            parentTermID: row[2],
            childTermID: row[3],
            goRelationshipTypeID: row[4]
        })"""
        gusgorelationship_filepath = "file:///gtb/gusgorelationship"+str(size)+"-5.csv"
        graph.populate_with_csv(gusgorelationship_filepath, rel_gusgorelationship_cmd, stats=True)
        # csv#4
        rel_gusgosynonym_cmd = """MERGE (n:GUSGoSynonym {
            goSynonymID: row[1], 
            externalDatabaseReleaseID: row[2],
            sourceID: row[3],
            goTermID: row[4],
            text: row[5]
        })"""
        gusgosynonym_filepath = "file:///gtb/gusgosynonym"+str(size)+"-5.csv"
        graph.populate_with_csv(gusgosynonym_filepath, rel_gusgosynonym_cmd, stats=True)
        # csv#5
        rel_gusgoterm_cmd = """MERGE (n:GUSGoTerm {
            goTermID: row[1], 
            goID: row[2],
            externalDatabaseReleaseID: row[3],
            sourceID: row[4],
            name: row[5],
            definition: row[6],
            commentString: row[7],
            minimumLevel: row[8],
            maximumLevel: row[9],
            numberOfLevels: row[10],
            ancestorGoTermID: row[11],
            isObsolete: row[12]
        })"""
        gusgoterm_filepath = "file:///gtb/gusgoterm"+str(size)+"-5.csv"
        graph.populate_with_csv(gusgoterm_filepath, rel_gusgoterm_cmd, stats=True)
        # csv#6
        rel_gustaxon_cmd = """MERGE (n:GUSTaxon {
            taxonID: row[1],
            ncbiTaxID: row[2],
            parentID: row[3],
            rank: row[4],
            geneticCodeID: row[5],
            mitochondrialGeneticCodeID: row[6]
        })"""
        gustaxon_filepath = "file:///gtb/gustaxon"+str(size)+"-5.csv"
        graph.populate_with_csv(gustaxon_filepath, rel_gustaxon_cmd, stats=True)
        # csv#7
        rel_gustaxonname_cmd = """MERGE (n:GUSTaxonName {
            taxonNameID: row[1],
            taxonID: row[2],
            name: row[3],
            uniqueNameVariant: row[4],
            nameClass: row[5]
        })"""
        gustaxonname_filepath = "file:///gtb/gustaxonname"+str(size)+"-5.csv"
        graph.populate_with_csv(gustaxonname_filepath, rel_gustaxonname_cmd, stats=True)
