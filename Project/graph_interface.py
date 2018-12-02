#From triple_extraction
import triple_extraction
from rdflib import Namespace
from stanfordcorenlp import StanfordCoreNLP
import rdflib
from rdflib import Graph
from rdflib.namespace import RDF, DC
from rdflib import Namespace
from rdflib.plugins.sparql import prepareQuery
from rdflib import URIRef, BNode, Literal
#From web_crawler
from rdflib.plugins.sleepycat import Sleepycat
import xml.etree.ElementTree as ET
import os
#NPDS Interface Imports
import requests
import json
import re
import math
#XML Parser Modules
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import fromstring
#XML to JSON
import xmljson
from xmljson import badgerfish as bf
import warnings
#Format of Output file
form = "xml"
def graph_creator(articles, root, coreNLPfull, javaHome):
    warnings.filterwarnings("ignore", category=ResourceWarning)
    totalTriplesRetrieved = 0
    totalArticlesRetrieved = 0
    temporaryURI = "http://temporary.org/"
    #Initialize CoreNLP Object
    nlp = StanfordCoreNLP(coreNLPfull,memory='3g')
    for article in articles:
        #try:
            #Open the index file
            #Read the file
            reader = open(root+r'\Number_Of_Documents.txt', "r")
            at = int(reader.read())
            reader.close()
            #Make title literal and clean it to ensure single spacing
            title = Literal(' '.join(article["title"].split()))
            #Make DOI literal
            if article["doi"][0:4] == "DOI:":
                doi = Literal(article["doi"][4:])
            else: 
                doi = Literal(article["doi"])
            #Make Authors list
            authors = article["author(s)"]
            #Make date literal
            #Try normal parse
            try:
                #List of months
                months = ['Jan','Feb','Mar',"Apr", "May", 'Jun', "Jul", 'Aug', 'Sept', "Nov", "Oct", "Dec"]
                #Seperate the date
                date_parts = article["date"].split("-")
                #Check if the date has month in number format
                if not date_parts[1] in months:
                    #If it is in number format then convert to abbreviated month format
                    date_parts[1] = months[int(date_parts[1])-1]
                #Remerge date sections and make date Literal
                date = Literal("-".join(date_parts))
            #If parse not in format
            except:
                date = Literal(article["date"])
            #Make publisher/database Literal
            publisher = Literal(article["database"])
            #Make an abstract literal
            if article["abstract"][0:8] == "Abstract":
                abstract = Literal(article["abstract"][8:])
            else:
                abstract = Literal(article["abstract"])
            #Initialize a graph
            graph = Graph()
            #identifier= "doc"+str(at)
            #graph = Graph('Sleepycat', identifier)
            #graph.open(root,True)
            document = URIRef(temporaryURI + str(at))
            #Add the title triple
            graph.add((document, DC.title, title))
            #If the doi literal is filled then add a DOI literal
            if not doi == "":
                graph.add((document, DC.identifier, doi))
            #Add the first author as a creator triple
            try:
                graph.add((document, DC.creator, Literal(authors[0])))
            except:
                x=1
            #Add other authors as contributors
            for i in range(1,len(authors)):
                graph.add((document, DC.contributor, Literal(authors[i])))
            #Add date as publishing date
            graph.add((document, DC.dateSubmitted, date))
            #Add the database triple
            graph.add((document, DC.publisher, publisher))
            #Add the database abstract
            graph.add((document, DC.abstract, abstract))
            #Add the semantic metadata
            vn = Namespace('https://verbs.colorado.edu/vn3.2.4-test-uvi/themroles/')
            
            triples = triple_extraction.triple_extraction(abstract, javaHome, coreNLPfull, nlp)
            #print(len(triples))
            for triple in triples:
                #print(triple)
                graph.add((triple[0], vn.Predicate, triple[1]))
                graph.add((triple[1], vn.Recipient, triple[2]))
            
            #print("fail")
            #Export process
            #Overwrite the file with a incremented number
            writer = open(root+r'\Number_Of_Documents.txt', "w") 
            writer.write(str(at+1))
            writer.close()
            #Set destination file
            destination=root+"\\doc"+str(at)+".txt"
            #Serialize
            graph.serialize(destination, form)
            totalTriplesRetrieved += len(triples)
            totalArticlesRetrieved += 1
        #except:
        #    print("Error in graph creation due to missing data.")
        #--------------------------------------------------------------------------------------------
        #Testing
        #print(str(graph.serialize(format='turtle')).replace("\\n", "\n"))
        #graph.close()
    nlp.close()
    del nlp
    print("Num Triples: " + str(totalTriplesRetrieved))
    print("Num Articles: " + str(totalArticlesRetrieved))
def sparql_query(query, root):
    g = Graph()
    #Read the file
    reader = open(root+r'\Number_Of_Documents.txt', "r") 
    #Number of .ttl files
    numFiles = int(reader.read())
    reader.close()
    #Go through files
    for i in range(1,numFiles):
        #Add to graph
        g.parse(str(root+"\\doc"+str(i)+".txt"), format = form)
    #Retrieve from the BHAVI records
    serverPrincipalTag = "nexus"
    entityPrincipalTag = "davinci"
    requestPage = r"http://npds.portaldoors.net/" + serverPrincipalTag + "/" + entityPrincipalTag
    r = requests.get(requestPage)
    #If the request work
    #if r.status_code == 200:
    #    print(r.text[3:])
    #    tree = ET.fromstring(r.text)
    #    data = raw_data[0][0][0][0]
    #    for entry in data:
    #        hasRDF = False
    #        entityMetadata = entry[0]
    #        try:
    #            supportingTags = entityMetadata.find('SupportingTags')
    #            for supportingTag in supportingTags:
    #                if supportingTag == 'HasRDFTest':
    #                    hasRDF = True
    #        except:
    #            x = -1
    #        if hasRDF:
    #           descriptions = entityMetadata.find("Descriptions")
    #           rdf = descriptions[0][0]
    #           rdf.write(root+"\\doc_temp.txt")
    #           g.parse(str(root+"\\doc_temp.txt"), format = form)
    #           os.remove(root+"\\doc_temp.txt")
    #    raw_data = r.json()
    #    data = raw_data["NPDS xmlns=\"http://npds.portaldoors.org/nsvo/npdsystem#\" Version=\"1.1.0 (2018-10-14)\""]["Message"]["ServerResponse"]["Answer"]["NexusService"]
    #    for entry in data:
    #        hasRDF = False
    #        try:
    #            tags=entry["EntityMetadata"]["SupportingTags"]
    #            for tag in tags:
    #                if tag == "HasRDFTest":
    #                    hasRDF = True
    #        if hasRDF:
    #            articleRDF = entry["EntityMetadata"]["Descriptions"]["Description"]
    #
    #else:
    #    print("RDF data retrieval failed from " + serverPrincipalTag + " type " + entityPrincipalTag + " server. Status Code: " + str(r.status_code))
    
    #SPARQL Test Query
    #Create the query
    query = prepareQuery(query, initNs = { "dc": DC})
    #Query the graph
    res = g.query(query)
    #Print results
    #for row in res:
    #    print(row)
    return res
#import web_crawler
#root = r"D:\Documents\BHAVI Documents\Code\Python Code\Project\Metadata_Records"
#articles = web_crawler.crawl(50,"Micro organisms")
#graph_creator(articles,root)
#query = """SELECT DISTINCT ?author ?title
#        WHERE {
#            ?a dc:contributor ?author .
#            ?a dc:title ?title
#        }"""




