import web_crawler
import graph_interface
import time
import os
def sparqlbuilder():
    print("s")
def sparqlexecuter(sparqlQuery):
    global root
    start_time = time.time()
    res=graph_interface.sparql_query(sparqlQuery,root)  
    return res
def sparqlqueryoutput(res):
    at = 1
    for row in res:
        str2 = "| "
        for col in row:
            str2 += col.toPython() + " | "
        print("----------------------------------------------------------------------------")
        print("Response #"+str(at))
        print(str2)
        at+=1
    print("--- %s seconds for search query---" % (time.time() - start_time))
def webCrawler(seachQuery, number):
    start_time = time.time()
    articles = web_crawler.crawl(number,searchQuery)
    print("--- %s seconds for document retrieval---" % (time.time() - start_time))
    if len(articles) > number:
        articles = articles[0:number]
    start_time = time.time()
    graph_interface.graph_creator(articles,root,coreNLPfull, javaHome)
    print("--- %s seconds for graph creation---" % (time.time() - start_time))
def sparqlenter():
    print("What is the SPARQL search query you are searching for? ")
    print(r"Enter (Exit) when you want to stop writing the query")
    sparqlQuery = ""
    temp = ""
    temp = input()
    while not temp == "(Exit)":
        sparqlQuery += temp + "\n"
        temp = input()
    return sparqlQuery

def sparqlcomposer():
    print("SPARQL Builder:")
    print("Do you want instructions? (Y/N)")
    numcond = (input())
    if numcond == "Y":
        print("1) First enter a series of conditions")
        print("2) The type of condition can either be NECESSARY or CONDITIONAL")
        print("3) One thing to note is that the last 3 conditions each correspond to a particular part of a condition in SPARQL")
        print("4) Finally, the user decides if they want want only distinct results and if they want to limit the amount of results")
        print("5) Each condition has four parts: type of condition, variable being searched, thing being searched for, and variable to which the result is assigned")
        print("6) Then the user decides which variables they want to return")
        print("\n")
    tripcondarr = []
    while 1>0:
        tripletyp = (input("What type of condition. Type \"(Exit)\" to end condition input."))
        if tripletyp == "(Exit)":
            break
        triplesubj = (input("What is the target variable (subject)?"))
        triplepred = (input("What is the condition (predicate)?"))
        tripleobj = (input("What do you want the output variable (object) to be named?"))
        if tripletyp == "NECESSARY":
            tripcondarr.append("?" + triplesubj + " " + triplepred + " ?" + tripleobj)
        elif tripletyp == "OPTIONAL":
            tripcondarr.append("OPTIONAL{ ?" + triplesubj + " " + triplepred + " ?" + tripleobj + " }")
    print("Which variables do you want to report. Enter \"(Exit)\" to leave.")
    repcondarr = []
    while 1>0:
        repcond = (input())
        if repcond == "(Exit)":
            break
        repcondarr.append(repcond)
    print("Which post conditions do you want to set?")
    print("1-Set limit to number of result triples")
    print("2-Toggle distinct setting")
    print("3-Exit")
    postcondarr = [-1,"N"]
    while 1>0 :
        postcond = int(input())
        if postcond == 1:
            tempcond1 = int(input("What limit do you want to set to? Enter -1 to have no limit."))
            postcondarr[0] = tempcond1
        elif postcond == 2:
            tempcond2 = (input("Do you want the distinct setting to be on (Y/N)?"))
            postcondarr[1] = tempcond2
        elif postcond == 3:
            break
    query = "SELECT"
    if postcondarr[1] == "Y":
        query += " DISTINCT"
    for rep in repcondarr:
        query += " ?" + rep
    query += " \n WHERE { \n"
    for cond in tripcondarr:
        query += cond + " .\n"
    query += "}\n"
    if postcondarr[0] != -1:
        query += "LIMIT "+ postcondarr[0]
    print(query)
    return query


import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=ResourceWarning)
#Environment Variable
global root
reader = open(r'Environment_Variables.txt', "r") 
root = reader.readline()[0:-2]
root = r"Metadata_Records"
javaHome = reader.readline()[0:-2]
coreNLPfull = reader.readline()[0:-1]
reader.close()
#root = r"D:\Documents\BHAVI Documents\Code\Python Code\Project\Metadata_Records"
#javaHome = r"C:\Program Files\Java\jdk1.8.0_181\bin\java.exe"
#coreNLPfull = r'D:\Documents\BHAVI Documents\Code\Python Code\Python Libraries\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27'
#Output Menu
print("Welcome to the COVASEA Semantic Graph Expander and SPARQL Searcher")
print("Functions:") 
print("1 - Perform a full External SPARQL search")
print("2 - Expand the Graph via External Search")
print("3 - Search the Local Store via SPARQL")
print("4 - Change Environment Variables")
print("5 - Reprint these commands")
print("6 - Exit")
inp = int(input("Choose a command: "))
while(not inp == 6):
    if inp == 1:
        searchQuery = (input("What is the natural language search query you are searching for? "))
        queryChoice = (input("Do you want to enter a SPARQL query manually? (Y/N)"))
        if queryChoice == "Y":
            sparqlQuery = sparqlenter()
        else:
            sparqlQuery = sparqlcomposer()
        number = int(input("How many articles do you want to search through? "))
        webCrawler(searchquery, number)
        res = sparqlexecuter(sparqlQuery)
        sparqlqueryoutput(res)
        break
    elif inp == 2:
        searchQuery = (input("What is the natural language search query you are searching for? "))
        number = int(input("How many articles do you want to search through? "))
        webCrawler(searchQuery, number)
        break
    elif inp == 3:
        queryChoice = (input("Do you want to enter a query manually? (Y/N)"))
        if queryChoice == "Y":
            sparqlQuery = sparqlenter()
        else:
            sparqlQuery = sparqlcomposer()
        #print(sparqlQuery)`
        #Test Query
        #sparqlQuery = """SELECT DISTINCT ?author ?title
        #           WHERE {
        #              ?a dc:contributor ?author .
        #              ?a dc:title ?title
        #          """
        res=sparqlexecuter(sparqlQuery)
        sparqlqueryoutput(res)
    elif inp == 4:
        #print("1 - Change Metadata Storage Location")
        print("1 - Change Location of Stanford CoreNLP Full Installation")
        print("2 - Change Location of Java JDK Installation")
        print("3 - Exit")
        inp2 = int(input("Choose a command: "))
        while not inp2 == 3:
            if inp2 == 202020333302:
                root = (input("Input the file where you want the local metadata to be stored. "))
                writer = open(root+r'\Number_Of_Documents.txt', "w") 
                writer.write(str(1))
                writer.close()
                print("Store file set to: " + root)
            if inp2 == 1:
                coreNLPfull = (input("Input the location of the Stanford CoreNLP full installation. "))
                print("Installation file set to: " + coreNLPfull)
            if inp2 == 2:
                javaHome = (input("Input the location of Java JDK installation. "))
                print("Installation file set to: " + javaHome)
            inp2 = int(input("Choose a command: "))
        os.remove(r'Environment_Variables.txt')
        writer = open(r'Environment_Variables.txt', "w") 
        variables = [root, javaHome, coreNLPfull, "EOF"]
        writer.write(root)
        writer.write("\n")
        writer.write(javaHome)
        writer.write("\n")
        writer.write(coreNLPfull)
        writer.write("\n")
        writer.write("EOF")
        writer.write("\n")
        writer.close()
    elif inp == 5:
        print("1 - Expand the Graph via External Search")
        print("2 - Search the Local Store via SPARQL")
        print("3 - Change Environment Variables")
        print("4 - Reprint these commands")
        print("5 - Exit")
    inp = int(input("Choose a command: "))
        

