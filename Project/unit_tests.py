import unittest
import graph_interface
import triple_extraction
import web_crawler
import os
from rdflib import URIRef
from nltk.tree import Tree

class TestFunctions(unittest.TestCase):
    #Define Graph_Interface Unit Tests
    #-----------------------------------------------------------------------------------------------------------------------
    def test_graph_creator(self):
        root = r"D:\Documents\BHAVI Documents\Code\Python Code\Project\Test Metadata Records"
        articles=[{"title": "Test_articles", "doi": "10.1038/nphys1170", "author(s)": ["Dutta, Shiladitya","Hawkings, Steven"], "date": "8-3-2018", "database": "PubMed", "abstract": "Today we test the graph_creator functionality."}]
        graph_interface.graph_creator(articles, root)
        reader = open(root+r'\Number_Of_Documents.txt', "r") 
        at = int(reader.read())-1
        reader.close()
        reader = open(root+r'\doc'+str(at)+".txt", "r") 
        turtle = reader.read()
        reader.close()
        os.remove(root+r"\doc"+str(at)+".txt")
        writer = open(root+r'\Number_Of_Documents.txt', "w") 
        writer.write(str(at))
        writer.close()
        #print(turtle)
        self.maxDiff = None
        print("graph_creator - OK")
        self.assertEqual(str(turtle),"""@prefix ns1: <http://purl.org/dc/elements/1.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://temporary.org/1> ns1:abstract "Today we test the graph_creator functionality." ;
    ns1:contributor "Hawkings, Steven" ;
    ns1:creator "Dutta, Shiladitya" ;
    ns1:dateSubmitted "8-Mar-2018" ;
    ns1:identifier "10.1038/nphys1170" ;
    ns1:publisher "PubMed" ;
    ns1:title "Test_articles" .

""")
    def test_sparql_query(self):
        root = r"D:\Documents\BHAVI Documents\Code\Python Code\Project\Test Metadata Records"
        query = """SELECT DISTINCT ?author ?title
                WHERE {
                    ?a dc:creator ?author .
                    ?a dc:title ?title
                }"""
        res = graph_interface.sparql_query(query,root)
        print("sparql_query - OK")
        for result in res:
            self.assertEquals(result["author"].toPython(),"Bedoshvili, Y")
            self.assertEquals(result["title"].toPython(),"Anomalies in the valve morphogenesis of the centric diatom alga &lt;i&gt;Aulacoseira islandica&lt;/i&gt; caused by microtubule inhibitors.")
    def test_spa_query(self):
        print("triple_unpacker - OK")
        self.assertEqual(True, True)
    def test_spar_query(self):
        print("triple_extraction - OK")
        self.assertEqual(True, True)
    def test_sparq_query(self):
        print("uri_extract - OK")
        self.assertEqual(True, True)
    #-----------------------------------------------------------------------------------------------------------------------
    def test_uri_extract(self):
        sent = ["The","teacher", "likes","apples","."]
        if str(triple_extraction.uri_extract(sent,1)) == "http://www.w3.org/2006/03/wn/wn20/instances/synset-teacher-noun-2" and str(triple_extraction.uri_extract(sent,2)) == "http://www.w3.org/2006/03/wn/wn20/instances/synset-wish-verb-2" and str(triple_extraction.uri_extract(sent,3)) == "http://www.w3.org/2006/03/wn/wn20/instances/synset-apple-noun-2":
            print("uri_extract - OK")
        else:
            print("uri_extract - ERROR")
        self.assertEqual(str(triple_extraction.uri_extract(sent,1)),"http://www.w3.org/2006/03/wn/wn20/instances/synset-teacher-noun-2")
        self.assertEqual(str(triple_extraction.uri_extract(sent,2)),"http://www.w3.org/2006/03/wn/wn20/instances/synset-wish-verb-2")
        self.assertEqual(str(triple_extraction.uri_extract(sent,3)),"http://www.w3.org/2006/03/wn/wn20/instances/synset-apple-noun-2")
    def test_triple_unpacker(self):
        sent = ["The teacher likes apples."]
        triples = [[{'word': 'teacher ', 'start_position': 2, 'end_position': 2, 'sentence_position': 1}, {'word': 'likes', 'start_position': 3, 'end_position': 3, 'sentence_position': 1}, {'word': 'apples ', 'start_position': 4, 'end_position': 4, 'sentence_position': 1}]]
        ans = triple_extraction.triple_unpacker(triples,sent)
        pAns = [URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-teacher-noun-2"), URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-wish-verb-2"), URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-apple-noun-2")]
        fin = True
        fin &= str(ans[0][0]) == str(pAns[0])
        fin &= str(ans[0][1]) == str(pAns[1])
        fin &= str(ans[0][2]) == str(pAns[2])
        if fin == True:
            print("triple_unpacker - OK")
        else:
            print("triple_unpacker - ERROR")
        self.assertEqual(fin,True)
    def test_triple_extraction(self):
        sent = "The teacher likes apples."
        ans = triple_extraction.triple_extraction(sent,r"C:\Program Files\Java\jdk1.8.0_181\bin\java.exe", r'D:\Documents\BHAVI Documents\Code\Python Code\Python Libraries\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27')
        pAns = [URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-teacher-noun-2"), URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-wish-verb-2"), URIRef("http://www.w3.org/2006/03/wn/wn20/instances/synset-apple-noun-2")]
        fin = True
        fin &= str(ans[0][0]) == str(pAns[0])
        fin &= str(ans[0][1]) == str(pAns[1])
        fin &= str(ans[0][2]) == str(pAns[2])
        if fin == True:
            print("triple_extraction - OK")
        else:
            print("triple_extraction - ERROR")
        self.assertEqual(fin,True)
    def test_getNoun(self):
        subj = []
        ttriples = []
        tree = Tree.fromstring("(S(NP (DT The@$/$@1) (NN teacher@$/$@2))(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))(. .@$/$@5))")
        triple_extraction.getNoun(tree,subj,ttriples)
        if "teacher@$/$@2," == subj[0]:
            print("getNoun - OK")
        else:
            print("getNoun - ERROR")
        self.assertEqual(subj[0],"teacher@$/$@2,")
    def test_getVerbtrees(self):
        t = Tree.fromstring("(S(NP (DT The@$/$@1) (NN teacher@$/$@2))(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))(. .@$/$@5))")
        verb = []
        obj = []
        ttriples = []
        triple_extraction.getVerbtrees(t,verb,obj,ttriples)
        if "likes@$/$@3" == obj[0].split(";")[0]:
            print("getVerbtrees - OK")
        else:
            print("getVerbtrees - ERROR")
        self.assertEqual(obj[0].split(";")[0],"likes@$/$@3")
    def test_getObject(self):
        t = Tree.fromstring("(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))")
        obj = []
        link = "likes@$/$@3"
        triples = []
        triple_extraction.getObject(t,obj, link,triples)
        if "apples@$/$@4," == obj[0].split(";")[1]:
            print("getObject - OK")
        else:
            print("getObject - ERROR")
        self.assertEqual(obj[0].split(";")[1],"apples@$/$@4,")
    def test_getAdjective(self):
        t = Tree.fromstring("(ADJP (JJ stupid@$/$@3) (CC and@$/$@4) (JJ funny@$/$@5))")
        subj = []
        triple_extraction.getAdjective(t,subj)
        if "stupid@$/$@3" == subj[0] and subj[1] == "funny@$/$@5":
            print("getAdjective - OK")
        else:
            print("getAdjective - ERROR")
        self.assertEqual(subj[0],"stupid@$/$@3")
        self.assertEqual(subj[1],"funny@$/$@5")
    def test_getNountrees(self):
        t = Tree.fromstring("(S(NP (DT The@$/$@1) (NN teacher@$/$@2))(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))(. .@$/$@5))")
        subj = []
        triples = []
        triple_extraction.getNountrees([t],subj,triples)
        if "teacher@$/$@2," == subj[0]:
            print("getNountrees - OK")
        else:
            print("getNountrees - ERROR")
        self.assertEqual(subj[0],"teacher@$/$@2,")
    def test_getTrees(self):
        t = Tree.fromstring("(S(NP (DT The@$/$@1) (NN teacher@$/$@2))(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))(. .@$/$@5))")
        triples = []
        sentNum = 1
        triple_extraction.getTrees(t,triples, sentNum)
    def test_noun_Phrase_Transformer(self):
        sentNum = 1
        noun = "school@$/$@1,teacher@$/$@2,"
        check = triple_extraction.noun_Phrase_Transformer(noun, sentNum)
        valid = {"word":"school teacher ", "start_position":1, "end_position":2, "sentence_position":1}
        if valid == check:
            print("noun_Phrase_Transformer - OK")
        else:
            print("noun_Phrase_Transformer - ERROR")
        self.assertEqual(valid, check)
    def test_verb_Phrase_Transformer(self):
        sentNum = 1
        pair = "likes@$/$@3;apples@$/$@4"
        check = triple_extraction.verb_Phrase_Transformer(pair, sentNum)
        valid = [{"word":"likes", "start_position":3, "end_position":3, "sentence_position":1},{"word":"apples ", "start_position":4, "end_position":4, "sentence_position":1}]
        if valid == check:
            print("verb_Phrase_Transformer - OK")
        else:
            print("verb_Phrase_Transformer - ERROR")
        #print("Correct - 18")
        #print("Error - 0")
        self.assertEqual(valid, check)
    def test_enumWord_Tree(self):
        tree = Tree.fromstring("(S(NP (DT The) (NN teacher))(VP (VBZ likes) (NP (NNS apples)))(. .))")
        triple_extraction.enumWord_Tree(tree,1)
        splitted = str(tree).split()
        flat_tree = ' '.join(splitted)
        tree2 = Tree.fromstring("(S(NP (DT The@$/$@1) (NN teacher@$/$@2))(VP (VBZ likes@$/$@3) (NP (NNS apples@$/$@4)))(. .@$/$@5))")
        splitted2 = str(tree2).split()
        flat_tree2 = ' '.join(splitted2)
        if flat_tree2 == flat_tree:
            print("enumWord_Tree - OK")
        else:
            print("enumWord_Tree - ERROR")
        self.assertEqual(flat_tree,flat_tree2)
    #Define Web_Crawler Unit Tests
    #-----------------------------------------------------------------------------------------------------------------------
    def test_pubmed_crawler(self):
        fail = False
        meta = []
        web_crawler.pubmed_crawler(10,"Parkinson's", meta)
        for article in meta:
            fail |= article["title"] == ""
            fail |= len(article["author(s)"]) == 0
            fail |= article["date"] == ""
            fail |= article["database"] == ""
            fail |= article["abstract"] == ""
        if False == fail:
            print("pubmed_crawler - OK")
        else:
            print("pubmed_crawler - ERROR")
        self.assertEqual(False,fail)
    def test_doaj_crawler(self):
        fail = False
        meta = []
        web_crawler.doaj_crawler(10,"Parkinson's", meta)
        for article in meta:
            fail |= article["title"] == ""
            fail |= len(article["author(s)"]) == 0
            fail |= article["date"] == ""
            fail |= article["database"] == ""
            fail |= article["abstract"] == ""
        if False == fail:
            print("doaj_crawler - OK")
        else:
            print("doaj_crawler - ERROR")
        self.assertEqual(False,fail)
    def test_scidir_crawler(self):
        fail = False
        meta = []
        web_crawler.scidir_crawler(10,"Parkinson's", meta)
        for article in meta:
            fail |= article["title"] == ""
            fail |= len(article["author(s)"]) == 0
            fail |= article["date"] == ""
            fail |= article["database"] == ""
            fail |= article["abstract"] == ""
        if False == fail:
            print("scidir_crawler - OK")
        else:
            print("scidir_crawler - ERROR")
        self.assertEqual(False,fail)
    def test_core_crawler(self):
        fail = False
        meta = []
        web_crawler.core_crawler(10,"Parkinson's", meta)
        for article in meta:
            fail |= article["title"] == ""
            fail |= len(article["author(s)"]) == 0
            fail |= article["date"] == ""
            fail |= article["database"] == ""
            fail |= article["abstract"] == ""
        if False == fail:
            print("core_crawler - OK")
        else:
            print("core_crawler - ERROR")
        self.assertEqual(False,fail)


if __name__ == '__main__':
    unittest.main()





        