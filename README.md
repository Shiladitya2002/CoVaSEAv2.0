 Here is how to install and use the CoVaSEA system
# You first have to download the project file onto your computer. Then you must download the Stanford Parser files that are included and # unzip them. You will need to download 5 packages via pip: 
# 1) stanfordcorenlp
# 2) nltk
# 3) rdflib
# 4) requests
# 5) xmljson 
# Then run the central_interface.py class. This will start the program. As soon as CoVaSEA starts, enter 4 to change the environment variables. Change the location of the Stanford CoreNLP installation to wherever you have downloaded the included Stanford CoreNLP files. More specifically to the folder of the stanford-corenlp-full-2018-02-27 files. Finally change Java JDK installation location to the location of the Java JDK java.exe file on your computer. This is necessary for Stanford CoreNLP which is a Java based program. Then you are able to run the system. You have 3 main functionalities. 
# 1)Complete Search
# The first is to perform a combination search. First you input a natural language search query which is used to search for potentially pertinent articles on the 4 databases. Then you can decide whether or not to enter a SPARQL Search query manually. You can manually enter a SPARQL search manually by simply entering it into the command line and then inputting "(Exit)" when complete. You can also use the SPARQL Builder form to help build a query. Finally it will ask you how many articles your want to search through. Do not ask for more than 30 articles at a time since it may overload the API key for CORE. Then the system will search for articles, translate them, and apply the SPARQL query. The system will then return to you the answer for your SPARQL query. 
# 2)Expansion
# The second option is to expand the store of semantic metadata. For this you will need to just enter the natural language search query and how many articles you want to search. Do not ask for more than 30 articles at a time since it may overload the API key for CORE. The system will then expand the semantic stores
# 3)SPARQL Search
# The last option is to search the store of semantic metadata. For this you can enter a SPARQL query or use a SPARQL builder form and it will search through the semantic stores. You can manually enter a SPARQL search manually by simply entering it into the command line and then entering "(Exit)" when complete. You can also use the SPARQL Builder form to help build a query.
