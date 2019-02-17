from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os
#import central_interface
#--------------------------------------------------------------------------
def quitsparqlsearch():
    global sparqlchooseframe
    global menuframe
    sparqlchooseframe.pack_forget()
    menuframe.pack()
def quitsparqlbuilder():
    global sparqlbuildframe
    global sparqlenterframe
    global sparqlchooseframe
    sparqlbuildframe.pack_forget()
    sparqlenterframe.pack_forget()
    sparqlchooseframe.pack()
def sparqladdargument():
    global sparqlbuildframe
    global sparqlarguments
    #Make boxes
    optionalbox = IntVar()
    optionalboxt = Checkbutton(sparqlbuildframe, variable = optionalbox)
    subjectbox = Entry(sparqlbuildframe)
    verbbox = Entry(sparqlbuildframe)
    objectbox = Entry(sparqlbuildframe)
    #Place boxes
    rowat = len(sparqlarguments)+2
    optionalboxt.grid(row = rowat, column = 0)
    subjectbox.grid(row = rowat, column = 1)
    verbbox.grid(row = rowat, column = 2)
    objectbox.grid(row = rowat, column = 3)
    #Add to array
    temparr = [optionalbox,subjectbox,verbbox,objectbox]
    sparqlarguments.append(temparr)
def quitsparqloutput():
    global sparqloutframe
    global sparqloutputframe
    global sparqlchooseframe
    sparqloutframe.pack_forget()
    sparqloutputframe.pack_forget()
    sparqlchooseframe.pack()
def sparqladdoutput():
    global sparqloutframe
    global sparqloutputs
    #Make boxes
    outputbox = Entry(sparqloutframe)
    #Place boxes
    rowat = len(sparqloutputs)+3
    outputbox.grid(row = rowat, column = 0)
    #Add to array
    sparqloutputs.append(outputbox)
def sparqloutGUI():
    #stop sparql search arguments frame
    global sparqlenterframe
    global sparqlchooseframe
    sparqlbuildframe.pack_forget()
    sparqlenterframe.pack_forget()
    #Make frame for output frame
    global sparqloutframe
    sparqloutframe = Frame()
    #Place frame for output frame
    sparqloutframe.pack()
    #Make frame for enter frame
    global sparqloutputframe
    sparqloutputframe = Frame()
    #Place frame for sparql enter frame
    sparqloutputframe.pack()
    #Set enter and back button
    enterKey = Button(sparqloutputframe, text = "Enter", command = sparqlpostchooser)
    backKey = Button(sparqloutputframe, text = "Back", command = quitsparqloutput)
    enterKey.grid(row = 0, column = 1)
    backKey.grid(row = 0, column = 0)
    #Make Headings
    sparqloutheading = Label(sparqloutframe, text = "SPARQL Builder")
    sparqloutinstructions = Label(sparqloutframe, text = "Input the variables you want to return.")
    morebutton = Button(sparqloutframe, text = "+", command = sparqladdoutput)
    #Place Headings
    sparqloutheading.grid(row = 0)
    sparqloutinstructions.grid(row = 1)
    morebutton.grid(row = 2)
    #Make outputs array
    global sparqloutputs
    sparqloutputs = []
    #Loop through arguments
    sparqladdoutput()
def quitpostchooser():
    global postchooserframe
    global sparqlchooseframe
    postchooserframe.pack_forget()
    sparqlchooseframe.pack()
def sparqlpostchooser():
    #Close frames
    global sparqloutframe
    global sparqloutputframe
    sparqloutframe.pack_forget()
    sparqloutputframe.pack_forget()
    #Open post-condition frame
    global postchooserframe
    postchooserframe=Frame()
    #Place post-condition frame
    postchooserframe.pack()
    #Make 
    global limitEntry
    global distinctCheck
    postconditionHeading = Label(postchooserframe, text = "Post-Condition Entry")
    limitLabel = Label(postchooserframe, text = "Set limit to number of result triples: ")
    distinctLabel = Label(postchooserframe, text = "Toggle distinct setting")
    limitEntry = Entry(postchooserframe)
    global distinctLabelv
    distinctLabelv = IntVar()
    distinctCheck = Checkbutton(postchooserframe, variable = distinctLabelv)
    #Place labels
    postconditionHeading.grid(row = 0, columnspan=2)
    limitLabel.grid(row = 1, column = 0)
    distinctLabel.grid(row = 2, column = 0)
    limitEntry.grid(row = 1, column = 1)
    distinctCheck.grid(row = 2, column = 1)
    #Set enter and back button
    enterKey = Button(postchooserframe, text = "Enter", command = sparqlbuilder)
    backKey = Button(postchooserframe, text = "Back", command = quitpostchooser)
    enterKey.grid(row = 3, column = 1)
    backKey.grid(row = 3, column = 0)
def sparqlbuilder():
    #Get post conditions
    global distinctLabelv
    numofLimit = limitEntry.get()
    if not numofLimit == "":
        numofLimit = int(numofLimit)
    else:
        numofLimit = -100
    isdistinct = False
    if distinctLabelv.get() == 1:
        isdistinct = True
    tripcondarr = []
    #Get argument conditions
    for argument in sparqlarguments:
        isoptional = False
        if argument[0].get() == 1:
            isoptional = True
        subject = argument[1].get()
        verb = argument[2].get()
        object = argument[3].get()
        if isoptional:
            tripcondarr.append("OPTIONAL{ ?" + subject + " " + verb + " ?" + object + " }")
        else:
            tripcondarr.append("?" + subject + " " + verb + " ?" + object)
        #print(isoptional,subject,verb,object)
    #Get output conditions
    repcondarr = []
    for outvar in sparqloutputs:
        repcondarr.append(outvar.get())
    #Make query
    query = ""
    if isdistinct:
        query += " DISTINCT"
    for rep in repcondarr:
        query += " ?" + rep
    query += " \n WHERE { \n"
    for cond in tripcondarr:
        query += cond + " .\n"
    query += "}\n"
    if numofLimit != -100:
        query += "LIMIT "+ numofLimit
    #Make Loading Screen
    sparqlLoading = Label(sparqlenterframe, text = "Processing...")
    #Place Loading Screen
    sparqlLoading.grid(row=1, columnspan=2)
    global res
    res = []
    #res = sparqlexecuter(query)
    #Remove stuff
    global postchooserframe
    postchooserframe.pack_forget()
    #Display SPARQL Query
    global sparqloutputqueryframe
    global sparqloutputcontrolframe
    sparqloutputqueryframe = Frame()
    sparqloutputqueryframe.pack()
    sparqloutputheading = Label(sparqloutputqueryframe, text = "Output")
    sparqloutputheading.grid(row = 0, columnspan=2)
    aty = 0
    for row in res:
       atx = 0
       for col in row:
           outputpiece = Label(sparqloutputqueryframe, text = col)
           outputpiece.grid(row = aty+1, column = atx)
           atx+=1
       aty+=1
    #Make back button
    sparqloutputcontrolframe = Frame()
    sparqloutputcontrolframe.pack()
    outputbackbutton = Button(sparqloutputcontrolframe, text = "Menu", command = quitsparqlqueryoutput)
    outputbackbutton.grid(row = 0, columnspan = 2)
def sparqlbuilderGUI():
    #stop sparql search choose frame
    global sparqlchooseframe
    sparqlchooseframe.pack_forget()
    #Make frame for arguments frame
    global sparqlbuildframe
    sparqlbuildframe = Frame()
    #Place frame for arguments frame
    sparqlbuildframe.pack()
    #Make frame for enter frame
    global sparqlenterframe
    sparqlenterframe = Frame()
    #Place frame for sparql enter frame
    sparqlenterframe.pack()
    #Set enter and back button
    enterKey = Button(sparqlenterframe, text = "Enter", command = sparqloutGUI)
    backKey = Button(sparqlenterframe, text = "Back", command = quitsparqlbuilder)
    enterKey.grid(row = 0, column = 1)
    backKey.grid(row = 0, column = 0)
    #Make Headings
    sparqlbuilderheading = Label(sparqlbuildframe, text = "SPARQL Builder")
    sparqlmandatoryheading = Label(sparqlbuildframe, text = "Optional?")
    sparqlsubjectheading = Label(sparqlbuildframe, text = "Subject")
    sparqlverbheading = Label(sparqlbuildframe, text = "Verb")
    sparqlobjectheading = Label(sparqlbuildframe, text = "Object")
    morebutton = Button(sparqlbuildframe, text = "+", command = sparqladdargument)
    #Place Headings
    sparqlbuilderheading.grid(row = 0, columnspan = 4)
    sparqlmandatoryheading.grid(row = 1, column = 0)
    sparqlsubjectheading.grid(row = 1, column = 1)
    sparqlverbheading.grid(row = 1, column = 2)
    sparqlobjectheading.grid(row = 1, column = 3)
    morebutton.grid(row = 1, column = 4)
    #Make arguments array
    global sparqlarguments
    sparqlarguments = []
    #Loop through arguments
    sparqladdargument()
def sparqlinput():
    global sparqlinputframe
    global sparqltext
    sparqlquery = sparqltext.get("1.0",END)
    #Make Loading Screen
    sparqlLoading = Label(sparqlinputframe, text = "Processing...")
    #Place Loading Screen
    sparqlLoading.grid(row=4, columnspan=2)
    #Make the query
    global res
    res = []
    res = sparqlexecuter(sparqlquery)
    #Remove stuff
    sparqlinputframe.pack_forget()
    #Display SPARQL Query
    global sparqloutputqueryframe
    global sparqloutputcontrolframe
    sparqlinputframe.pack_forget()
    sparqloutputqueryframe = Frame()
    sparqloutputqueryframe.pack()
    sparqloutputheading = Label(sparqloutputqueryframe, text = "Output")
    sparqloutputheading.grid(row = 0, columnspan=2)
    aty = 0
    for row in res:
       atx = 0
       for col in row:
           outputpiece = Label(sparqloutputqueryframe, text = col)
           outputpiece.grid(row = aty+1, column = atx)
           atx+=1
       aty+=1
    #Make back button
    sparqloutputcontrolframe = Frame()
    sparqloutputcontrolframe.pack()
    outputbackbutton = Button(sparqloutputcontrolframe, text = "Menu", command = quitsparqlqueryoutput)
    outputbackbutton.grid(row = 0, columnspan = 2)
def quitsparqlqueryoutput():
    #Go back to Menu
    global menuframe
    global sparqloutputqueryframe
    global sparqloutputcontrolframe 
    sparqloutputqueryframe.pack_forget()
    sparqloutputcontrolframe.pack_forget()
    menuframe.pack()
def quitsparqlinput():
    global sparqlinputframe
    global sparqlchooseframe
    sparqlinputframe.pack_forget()
    sparqlchooseframe.pack()
def sparqlinputGUI():
    #stop sparql search choose frame
    global sparqlchooseframe
    sparqlchooseframe.pack_forget()
    #Make frame for SPARQL input
    global sparqlinputframe
    sparqlinputframe = Frame()
    #Place frame for arguments frame
    sparqlinputframe.pack()
    #Make Labels
    global sparqltext
    sparqlinputLabel = Label(sparqlinputframe, text = "SPARQL Input")
    sparqlinputInstructions = Label(sparqlinputframe, text = "Enter the SPARQL Query:")
    sparqltext = ScrolledText(sparqlinputframe)
    #Place Labels
    sparqlinputLabel.grid(row = 0,columnspan=2)
    sparqlinputInstructions.grid(row = 1,columnspan=2)
    sparqltext.grid(row = 2,columnspan=2)
    #Set enter and back button
    enterKey = Button(sparqlinputframe, text = "Enter", command = sparqlinput)
    backKey = Button(sparqlinputframe, text = "Back", command = quitsparqlinput)
    enterKey.grid(row = 3, column = 1)
    backKey.grid(row = 3, column = 0)
def sparqlsearchGUI():
    #stop menuframe
    global menuframe
    menuframe.pack_forget()
    #Make frame for sparql search choose frame
    global sparqlchooseframe
    sparqlchooseframe = Frame(root)
    #Place frame for sparql search choose frame
    sparqlchooseframe.pack()
    #Make buttons
    sparqlchooserHeading = Label(sparqlchooseframe, text = "SPARQL Search")
    choosequeryLabel = Label(sparqlchooseframe, text = "Would you like to use the SPARQL Query builder?")
    yesbuilderLabel = Button(sparqlchooseframe, text = "Yes", command = sparqlbuilderGUI)
    nobuilderLabel = Button(sparqlchooseframe, text = "No", command = sparqlinputGUI)
    backKey = Button(sparqlchooseframe, text = "Back", command = quitsparqlsearch)
    #Place buttons
    sparqlchooserHeading.grid(row = 0, columnspan=2)
    choosequeryLabel.grid(row = 1, columnspan=2)
    yesbuilderLabel.grid(row = 2, column = 0)
    nobuilderLabel.grid(row = 2, column = 1)
    backKey.grid(row = 3, columnspan=2)
#--------------------------------------------------------------------------
def quitwebcrawler():
    global webcrawlerframe
    global menuframe
    webcrawlerframe.pack_forget()
    menuframe.pack()
def webcrawler():
    #Get output
    global generalSearch
    global numOfArticles
    querySearch = generalSearch.get()
    numOfA = numOfArticles.get()
    #Make Loading Screen
    webcrawlerLoading = Label(webcrawlerframe, text = "Processing...")
    #Place Loading Screen
    webcrawlerLoading.grid(row=4, columnspan=2)
    #webCrawler(querySearch,int(numOfA))
    quitwebcrawler()
def webcrawlerGUI():
    #stop menuframe
    global menuframe
    menuframe.pack_forget()
    #Make frame for webcrawler
    global webcrawlerframe
    webcrawlerframe = Frame(root)
    #Place frame for webcrawler
    webcrawlerframe.pack()
    #Make variables for webcrawler
    global generalSearch
    global numOfArticles
    #Make entry boxes for the webcrawler
    webcrawlerHeading = Label(webcrawlerframe, text = "External Search")
    generalSearchLabel = Label(webcrawlerframe, text = "General Search Query:")
    numOfArticlesLabel = Label(webcrawlerframe, text = "Number of Articles:")
    generalSearch = Entry(webcrawlerframe)
    numOfArticles = Entry(webcrawlerframe)
    #Place boxes
    webcrawlerHeading.grid(row = 0, columnspan=2)
    generalSearchLabel.grid(row = 1, column = 0)
    numOfArticlesLabel.grid(row = 2, column = 0)
    generalSearch.grid(row = 1, column = 1)
    numOfArticles.grid(row = 2, column = 1)
    #Set enter and back button
    enterKey = Button(webcrawlerframe, text = "Enter", command = webcrawler)
    backKey = Button(webcrawlerframe, text = "Back", command = quitwebcrawler)
    enterKey.grid(row = 3, column = 1)
    backKey.grid(row = 3, column = 0)
#--------------------------------------------------------------------------
#Settings Methods
def quitsettings():
    global settingframe
    global menuframe
    settingframe.pack_forget()
    menuframe.pack()
def settings():
    #Get output
    global stanfordEntry
    global javaEntry
    coreNLPfull = stanfordEntry.get()
    javaHome = javaEntry.get()
    quitsettings()
def settingsGUI():
    #stop menuframe
    global menuframe
    menuframe.pack_forget()
    #Make frame for settings
    global settingframe
    settingframe = Frame(root)
    #Place frame for settings
    settingframe.pack()
    #Make variables for settings
    global stanfordEntry
    global javaEntry
    #Make entry boxes for the settings
    settingsHeading = Label(settingframe, text = "Settings")
    stanfordLabel = Label(settingframe, text = "Change StanfordNLP Location:")
    javaLabel = Label(settingframe, text = "Change Java JDK Location:")
    stanfordEntry = Entry(settingframe)
    javaEntry = Entry(settingframe)
    #Place boxes
    settingsHeading.grid(row = 0, columnspan=2)
    stanfordLabel.grid(row = 1, column = 0)
    javaLabel.grid(row = 2, column = 0)
    stanfordEntry.grid(row = 1, column = 1)
    javaEntry.grid(row = 2, column = 1)
    #Set enter and back button
    enterKey = Button(settingframe, text = "Enter", command = settings)
    backKey = Button(settingframe, text = "Back", command = quitsettings)
    enterKey.grid(row = 3, column = 1)
    backKey.grid(row = 3, column = 0)
#--------------------------------------------------------------------------
def quitwebcrawler2():
    global webcrawlerframe
    webcrawlerframe.pack_forget()
def webcrawler2():
    #Get output
    global generalSearch
    global numOfArticles
    querySearch = generalSearch.get()
    numOfA = numOfArticles.get()
    #Make Loading Screen
    webcrawlerLoading = Label(webcrawlerframe, text = "Processing...")
    #Place Loading Screen
    webcrawlerLoading.grid(row=4, columnspan=2)
    #webCrawler(querySearch,int(numOfA))
    quitwebcrawler2()
    sparqlsearchGUI()
def completesearchGUI():
    #stop menuframe
    global menuframe
    menuframe.pack_forget()
    #Make frame for webcrawler
    global webcrawlerframe
    webcrawlerframe = Frame(root)
    #Place frame for webcrawler
    webcrawlerframe.pack()
    #Make variables for webcrawler
    global generalSearch
    global numOfArticles
    #Make entry boxes for the webcrawler
    webcrawlerHeading = Label(webcrawlerframe, text = "External Search")
    generalSearchLabel = Label(webcrawlerframe, text = "General Search Query:")
    numOfArticlesLabel = Label(webcrawlerframe, text = "Number of Articles:")
    generalSearch = Entry(webcrawlerframe)
    numOfArticles = Entry(webcrawlerframe)
    #Place boxes
    webcrawlerHeading.grid(row = 0, columnspan=2)
    generalSearchLabel.grid(row = 1, column = 0)
    numOfArticlesLabel.grid(row = 2, column = 0)
    generalSearch.grid(row = 1, column = 1)
    numOfArticles.grid(row = 2, column = 1)
    #Set enter and back button
    enterKey = Button(webcrawlerframe, text = "Enter", command = webcrawler2)
    backKey = Button(webcrawlerframe, text = "Back", command = quitwebcrawler)
    enterKey.grid(row = 3, column = 1)
    backKey.grid(row = 3, column = 0)
#--------------------------------------------------------------------------
def exit():
    os._exit(0)
#--------------------------------------------------------------------------
#Main Frame
init = Tk()
root = Frame(init)
root.pack()
#Make Heading
heading = Label(root, text = "CoVaSEA", font='Helvetica 14 bold')
heading.pack()
#Make menuframe
menuframe = Frame(root)
menuframe.pack()
#Make menu heading
menuheading = Label(menuframe, text = "Main Menu")
menuheading.pack()
#Make buttons
completebutton = Button(menuframe, text = "Complete Search", fg = "blue", command = completesearchGUI)
externalbutton = Button(menuframe, text = "External Search", fg = "violet", command = webcrawlerGUI)
internalbutton = Button(menuframe, text = "Internal Search", fg = "purple", command = sparqlsearchGUI)
settingsbutton = Button(menuframe, text = "Settings", fg = "green", command = settingsGUI)
exitbutton = Button(menuframe, text = "Exit", fg = "red", command = exit)
#Place Buttons
completebutton.pack()
externalbutton.pack()
internalbutton.pack()
settingsbutton.pack()
exitbutton.pack()
#Loop
root.mainloop()
