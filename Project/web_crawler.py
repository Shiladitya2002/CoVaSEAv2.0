
#Crawlers
#-----------------------------------------------------------------------------------------------------------------------
#Core Crawler
def core_crawler(numarticles, searchKey, metadatas):
    #Import Modules
    #Python Modules
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
    #Initiate list of abstracts
    abstracts = []
    #Clean search key to ensure validity
    searchKey = searchKey.replace(" ", "%20")
    #Determine the number of pages
    numPages = 1
    if numarticles > 50:
        numPages = numarticles/50
    numPages = math.ceil(numPages)
    remainingArticles = numarticles
    #Initialize number of abstracts taken
    numAccepted = 0
    #Loop through pages
    for i in range(1,numPages+1):
        #Make request for a page of results
        requestPage = "https://core.ac.uk:443/api-v2/articles/search/"+searchKey+"?page="+str(i)+"&pageSize=50&metadata=true&fulltext=false&citations=false&similar=false&duplicate=false&urls=false&faithfulMetadata=false&apiKey=eYjDGVdhsRTy2f5iQ8xqBauKFLJSUP4c"
        r = requests.get(requestPage)
        #Check if request successful
        if r.status_code == 200:
            req = r.json()
            #Ensure that don't return abstracts over the specified number
            temp1 = min(remainingArticles,50)
            remainingArticles -= 50
            #Loop though all entries in a page
            for i in range(0,temp1):
                #Some variations in standard json format occur in this database
                try:
                    abstract = req['data'][i]['description'] 
                    #Check if abstract is present
                    if abstract is None:
                        print("Exception - Core Document ID:" + str(req['data'][i]['id']) + " does not have an abstract")
                        continue
                    #Remove excessive whitespaces 
                    abstract = ' '.join(abstract.split())
                    #Take out relevant entity metadata
                    #Title
                    title = req['data'][i]["title"]
                    #doi = req['data'][i]["identifiers"]
                    doi = ""
                    #Authors
                    authors = []
                    auth = req['data'][i]["authors"]
                    for author in auth:
                        authors.append(author)
                    #Date
                    date = req['data'][i]["datePublished"]
                    #Database
                    database = "Core"
                    #Abstract
                    abstractcpy = abstract
                    #Initiate Metadata Storage Array
                    metadata = {"title": title, "doi": doi, "author(s)": authors, "date": date, "database": database, "abstract": abstractcpy}
                    metadatas.append(metadata)
                    #Append to list of abstracts
                    abstracts.append(abstract)
                    #Increment number of accepted abstracts
                    numAccepted += 1
                    #Check if the number required is met
                    if numAccepted >= numarticles:
                        return abstracts
                #If it doesn't work continue
                except:
                    continue
        #If not return error
        else:
            temp20=-1
            #print("Error- Webcrawler Query Failure Code: Position: Initial Search String Query - Springer, Status Code: " + str(r.status_code))
        return abstracts
#Springer Crawler
def springer_crawler(numarticles, searchKey):
    #Import Modules
    #Python Modules
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
    abstracts = []
    searchKey = searchKey.replace(" ", "%20")
    numPages = 1
    if numarticles > 10:
        numPages = numarticles/10
    start = 1
    numPages = math.ceil(numPages)
    for i in range(1,numPages+1):
        requestPage = 'https://api.springer.com/metadata/json?q='+searchKey+'&p=2&s='+str(start)+'&api_key=b24edb7711f9b47c95673a12e592793a'
        start+=10
        r = requests.get(requestPage)
        if r.status_code==200:
            req = r.json()
            for i in range(0,2):
                secondaryReq = req['records'][i]['doi']
                #print(secondaryReq)
                requestPage2 = 'https://api.springer.com/metadata/pam?q='+secondaryReq+'&api_key=b24edb7711f9b47c95673a12e592793a'
                r2 = requests.get(requestPage2)
                if r2.status_code==200:
                    req2 = r2.content
                    translation = bf.data(fromstring(req2))
                    #print(translation)
                else:
                    temp20=-1
                    #print("Error- Webcrawler Query Failure Code: Position: Abstract Search String Query - Springer, Status Code: " + str(r.status_code) + ", Article DOI: " + requestPage2)
        else:
            temp20=-1
    #print("Error- Webcrawler Query Failure Code: Position: Initial Search String Query - Springer, Status Code: " + str(r.status_code))
    return abstracts
#Science Direct Crawler
def scidir_crawler(numarticles, searchKey, metadatas):
    #Import Modules
    #Python Modules
    import requests
    import json
    import re
    import math
    import time
    #XML Parser Modules
    from xml.dom import minidom
    from xml.etree import ElementTree
    from xml.etree.ElementTree import fromstring
    #XML to JSON
    import xmljson
    from xmljson import badgerfish as bf
    #Initiate abstracts array
    abstracts = []
    #Ensure search statement is valid
    searchKey = searchKey.replace(" ", "%20")
    returnType = "application/json"
    #Create request
    requestPage = 'https://api.elsevier.com/content/search/scidir?query='+searchKey+'&count='+str(numarticles)+'&httpAccept=' + returnType + '&apiKey=7f59af901d2d86f78a1fd60c1bf9426a'
    r = requests.get(requestPage)
    #Initialize number of accepted abstract
    numAccepted = 0
    #Check to see if request got returned
    if r.status_code == 200:
        #Convert to dictionary data structure
        req = r.json()
        #Loop through results
        for articles in req["search-results"]["entry"]:
            time.sleep(0.7)
            #Take out DOI
            secondaryReq = articles["prism:url"]
            returnType2 = "application/json"
            #Formulate request for DOI to get individual article
            requestPage2 = secondaryReq + "}?httpAccept="+returnType2+"&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
            r2 = requests.get(requestPage2)
            #Check to see if request got returned
            if r2.status_code == 200:
                try:
                    #Convery to dictionary data structure
                    req2 = r2.json()
                    #Retrieve abstract
                    abstract = req2["full-text-retrieval-response"]["coredata"]["dc:description"]
                    #Format abstract properly
                    abstract = ' '.join(abstract.split())
                    #Take out relevant entity metadata
                    #Title
                    title = articles["dc:title"]
                    doi = articles["dc:identifier"]
                    #Authors
                    authors = []
                    auth = articles["authors"]["author"]
                    for author in auth:
                        authors.append(author["given-name"] + ", " + author["surname"])
                    #Date
                    #print("a")
                    date = articles["prism:coverDate"][0]["$"]
                    #Database
                    database = "Elsevier Science Direct"
                    #Abstract
                    abstractcpy = abstract
                    #Initiate Metadata Storage Array
                    metadata = {"title": title, "doi": doi, "author(s)": authors, "date": date, "database": database, "abstract": abstractcpy}
                    metadatas.append(metadata)
                    #Add abstract to arraylist
                    abstracts.append(abstract)
                    #Increment number of accepted abstracts
                    numAccepted += 1
                    #Check if the number required is met
                    if numAccepted >= numarticles:
                        return abstracts
                #If data missing continue
                except:
                    continue
            #Return error if not request returned
            else:
                temp20=-1
                #print("Error- Webcrawler Query Failure Code: Position: Abstract Search String Query - SciDir, Status Code: " + str(r2.status_code))
    #Return error if not request returned
    else:
        temp20 = -1
        #print("Error- Webcrawler Query Failure Code: Position: Initial Search String Query - SciDir, Status Code: " + str(r.status_code))
    return abstracts
#DOAJ Crawler
def doaj_crawler(numarticles, searchKey, metadatas):
    #Import Modules
    #Python Modules
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
    warnings.filterwarnings("ignore")
    #Initialize abstract list
    abstracts = []
    #Clean search key to ensure it is correct
    searchKey = searchKey.replace(" ","%20")
    #Create API query
    requestPage = "https://doaj.org/api/v1/search/articles/" + searchKey + "?page=1&pageSize=" + str(numarticles)
    r = requests.get(requestPage)
    #Initialize number of abstracts that are accepted
    numAccepted = 0
    #Check to see if query was successful
    if r.status_code == 200:
        #Convert to json format
        res = r.json()
        #Loop through returned articles
        for articles in res["results"]:
            #Check if json formatted directly
            try:
                #Access articles
                abstract = articles["bibjson"]["abstract"]
                #Clean articles to ensure format
                abstract = ' '.join(abstract.split())
                #Take out relevant entity metadata
                #Title
                title = articles["bibjson"]["title"]
                #DOI
                doi = ""
                identifiers = articles["bibjson"]["identifier"]
                #Loop through identifiers
                for ids in identifiers:
                    if ids["type"] == "doi":
                        doi = ids["id"]
                        break
                #Authors
                authors = []
                auth = articles["bibjson"]["author"]
                for author in auth:
                    authors.append(author["name"].replace(" ", ", "))
                #Date
                date = articles["last_updated"].split("T")[0]
                #Database
                database = "DOAJ"
                #Abstract
                abstractcpy = abstract
                #Initiate Metadata Storage Array
                metadata = {"title": title, "doi": doi, "author(s)": authors, "date": date, "database": database, "abstract": abstractcpy}
                metadatas.append(metadata)
                #Add to list of abstracts
                abstracts.append(abstract)
                #Increment number of accepted abstracts
                numAccepted += 1
                #Check if the number required is met
                if numAccepted >= numarticles:
                    return abstracts
            #If JSON not formatted standardly continue
            except:
                continue
    #Else return error if query unsuccessful
    else:
        temp20 = -1
        #print("Error- Webcrawler Query Failure Code: Position: Initial Search String Query - DOAJ, Status Code: " + str(r.status_code))
    return abstracts
#PubMed Crawler
def pubmed_crawler(numarticles, searchKey, metadatas):
    #Import Modules
    #Python Modules
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
    #Initialize abstract list
    abstracts = []
    #Return type of query
    returnType = "json"
    #Clean search key to ensure validity
    searchKey = searchKey.replace(" ","+")
    #Formulate API request
    requestPage = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + searchKey + '&retmode=' + returnType + '&retmax='+ str(numarticles)
    r = requests.get(requestPage)
    #Initialize number of accepted abstracts
    numAccepted = 0
    #Check if REST API call functioned properly
    if r.status_code == 200:
        #Translate to dictionary
        req = r.json()
        #Access list of ids for articles that match search parameter
        arrid = req['esearchresult']['idlist']
        #Loop through articles
        for id in arrid:
            #Formulate secondary REST API request
            requestPage2 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=' + id + '&retmode=' + returnType 
            r2 = requests.get(requestPage2)
            #Check if the REST API request worked as intended
            if r2.status_code == 200:
                #Translate to JSON
                req2 = r2.json()
                #Check if article has an english abstract attached to it
                if 'Has Abstract' in req2['result'][str(id)]['attributes'] and ('eng' in req2['result'][str(id)]['lang']):
                    #Formulate request for the abstract
                    returnType3 = "xml"
                    requestPage3 = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode="+returnType3+"&rettype=abstract&id=" + str(id)
                    r3 = requests.get(requestPage3)
                    #Check if the API call worked as intended
                    if r3.status_code == 200:
                        #Try standard parsing
                        try:
                            #Convert returned object to a Ordered Dictionary
                            translation = bf.data(fromstring(r3.content))
                            #Clean the abstract by removing redundant newlines
                            raw_String = translation['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']['$']
                            #Clean the abstract by removing any spaces
                            abstract = ' '.join(raw_String.split())
                            #Take out relevant entity metadata
                            #Title
                            title = req2["result"][str(id)]["title"]
                            #DOI
                            doi = ""
                            identifiers = req2["result"][str(id)]["articleids"]
                            #Loop through identifiers
                            for ids in identifiers:
                                if ids["idtype"] == "doi":
                                    doi = ids["value"]
                                    break
                            #Authors
                            authors = []
                            auth = req2["result"][str(id)]["authors"]
                            for author in auth:
                                authors.append(author["name"].replace(" ", ", "))
                            #Date
                            date = req2["result"][str(id)]["pubdate"].replace(" ","-")
                            #Database
                            database = "NCBI PubMed"
                            #Abstract
                            abstractcpy = abstract
                            #Initiate Metadata Storage Array
                            metadata = {"title": title, "doi": doi, "author(s)": authors, "date": date, "database": database, "abstract": abstractcpy}
                            metadatas.append(metadata)
                            #Add to abstract list
                            abstracts.append(abstract)
                            #Increment number of accepted abstracts
                            numAccepted += 1
                            #Check if the number required is met
                            if numAccepted >= numarticles:
                                return abstracts
                        #If XML not standard format continue
                        except:
                            continue
                    #If article doesn't have an abstract throw an exception
                    else:
                        temp20 = -1
                        print("Error- Webcrawler Query Failure Code: Position: Abstract ID Search - PubMed , Status Code: " + str(r2.status_code))
                else:
                    temp20 = -1
                    print("Exception - Pubmed Document ID:" + str(id) + " does not have an abstract or is in another language")
            #If API call doesn't work throw an error
            else:
                temp20 = -1
                #print("Error- Webcrawler Query Failure Code: Position: Summary ID Search - Pubmed, Status Code: " + str(r2.status_code))
    #If API call not functioning throw error
    else:
        temp20 = -1
        #print("Error- Webcrawler Query Failure Code: Position: Initial Search String Query - Pubmed, Status Code: " + str(r.status_code))
    return abstracts
#Initialization
#-----------------------------------------------------------------------------------------------------------------------
#@staticmethod
def crawl(num_Return_Articles, searchKey):
    import math
    #Set number of articles from each repository
    #Due to the inevitability that the initial search query will have some invalid entries, the initial search query asks for double the requested amount
    #Then the crawler return once they've went through all the entries or retrieved the number of valid abstracts requested
    numArticles = math.ceil(num_Return_Articles/2)
    #PubMed Crawler Method Call
    pm_meta = []
    pm = pubmed_crawler(numArticles,searchKey, pm_meta)
    #Science Direct Crawler Method Call
    sd_meta = []
    sd = scidir_crawler(numArticles,searchKey, sd_meta)
    #DOAJ Crawler Method Call
    dj_meta = []
    dj = doaj_crawler(numArticles,searchKey, dj_meta)
    #CORE Crawler Method Call
    cr_meta = []
    cr = core_crawler(numArticles,searchKey, cr_meta)
    #print("Number of Returned PubMed Articles: " + str(len(pm)))
    #print("Number of Returned ScienceDirect Articles: " + str(len(sd)))
    #print("Number of Returned DOAJ Articles: " + str(len(dj)))
    #print("Number of Returned CORE Articles: " + str(len(cr)))
    #for abst in pm_meta:
    #   print(abst["title"])
    #for abst in sd_meta:
    #    print(abst["title"])
    #for abst in dj_meta:
    #    print(abst["title"])
    #for abst in cr_meta:
    #    print(abst["title"])
    #print(len(pm)+len(sd)+len(dj)+len(cr))
    #Make final return list
    final_List = pm_meta + sd_meta + dj_meta + cr_meta
    return final_List
    #arr5 = springer_crawler(numArticles,searchKey)
#import web_crawler
#print("a")
#Web_crawler.crawl(50,"Gene Expression")
#quit()