#Import Libraries
#From Stanford NLP
from stanfordcorenlp import StanfordCoreNLP
#From NLTK
from nltk.util import breadth_first
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.tokenize import word_tokenize
from nltk.tree import *
import nltk
#From RDFLib
from rdflib import Graph
from rdflib import URIRef
from rdflib import BNode, Literal
#From Python
import json
import warnings
#Preprocessing
#-----------------------------------------------------------------------------------------------------------------------
#Named Entity Recognition
def unique_entity_labeling(phrase,nlp):
    props={'annotators': 'dcoref, relation','pipelineLanguage':'en','outputFormat':'text'}
    output = nlp.annotate(phrase, properties=props)
    print(output)
    #Coreference resolution
    sents = []
    sentences = sent_tokenize(phrase)
    for i in sentences:
        sents.append(word_tokenize(i))
    coreferences = []
    #for chains in range(1,len(coreferences.keys())+1):
    for chains in range(1,1):
        lengthofrep = 0
        rep = []
        for info in coreferences[str(chains)]:
            if info["isRepresentativeMention"] == True:
                sentat = info["sentNum"]-1
                lengthofrep = info["endIndex"]-info["startIndex"]
                for i in range(info["startIndex"]-1, info["endIndex"]-1):
                    rep.append(sents[sentat][i])
                break
        print(rep)
        for info in coreferences[str(chains)]:
            if not info["isRepresentativeMention"] == True:
                sentat = info["sentNum"]-1
                #print(info["startIndex"]," ",info["endIndex"])
                #print(sents[sentat])
                del sents[sentat][info["startIndex"]-1: info["endIndex"]-1]
                #print(sents[sentat])
                for i in range(0,lengthofrep):
                    sents[sentat].insert(info["startIndex"]+i-1,rep[i])
    phrase = ""
    for sent in sents:
        for sen in sent:
            phrase += sen+" "
#Define Triplet Extraction Algorithms
#-----------------------------------------------------------------------------------------------------------------------
#Define central Tree method
def getTrees(ti,triples, sentNum):
    #Converts the parse tree to a parented tree for easier handling
    t = ParentedTree.convert(ti)
    #Defines if the getTree has to go deeper to parse out the sub sentences
    godeep = True
    #Checks if sub sentences are present 
    for phrases in t:
        if phrases.label() == "S":
            #Recursively goes deeper
            #pylint: disable-msg=too-many-arguments
            getTrees(phrases,triples, sentNum)
            godeep = False
    #If it hits a sub sentence it will initiate triple extraction
    if godeep == True:
        #Define temporary triple array
        ttriples = []
        #Define the various the svo arrays
        subj = []
        verb = []
        obj = []
        #Defines a temporary tree
        tempnountrees = [t]
        #Calls noun tree method
        getNountrees(tempnountrees,subj,ttriples)
        #Calls the verb tree method
        #Verb tree method also handles objects and adjective since those reside in the Verb Phrase
        getVerbtrees(t,verb,obj,ttriples)
        #Defines the transformed versions of the object
        nounTransform = []
        verbPhraseTransform = []
        adjPhraseTransform = []
        for adjtriple in ttriples:
            adjparts = adjtriple.split(";")
            adj_subject = noun_Phrase_Transformer(adjparts[0], sentNum)
            adj_object = noun_Phrase_Transformer(adjparts[2], sentNum)
            hasQuality_Composition = {"word":"HasQuality", "start_position":-1, "end_position":-1, "sentence_position":sentNum}
            triples.append([adj_subject,hasQuality_Composition,adj_object])
        #Places all the nouns and verbs into a triple
        # Assign position numbers to all noun phrases
        for noun in subj:
            word_composition = noun_Phrase_Transformer(noun,sentNum)
            nounTransform.append(word_composition)
        for pairs in obj:
            verbPhrase = verb_Phrase_Transformer(pairs, sentNum)
            verbPhraseTransform.append(verbPhrase)
        for nn in nounTransform:
            for vp in verbPhraseTransform:
                triples.append([nn,vp[0],vp[1]])
def noun_Phrase_Transformer(noun, sentNum):
    #Split the noun phrase into words
    parts = noun.split(",")
    word = ""
    #Assign noun phrase beginning an ending variables
    start_word = 1000000000
    end_word = -100000000
    for part in parts:
        if part == "":
            continue
        sections = part.split("@$/$@")
        #print(sections)
        word += sections[0]+" "
        wposition = int(sections[1])
        start_word = min(start_word,wposition)
        end_word = max(end_word,wposition)
    word_composition = {"word":word, "start_position":start_word, "end_position":end_word, "sentence_position":sentNum}
    return word_composition
def verb_Phrase_Transformer(pairs, sentNum):
    pair = pairs.split(";")
    objec = pair[1]
    parts = objec.split(",")
    word = ""
    start_word = 1000000000
    end_word = -100000000
    for part in parts:
        if part == "":
            continue
        sections = part.split("@$/$@")
        word += sections[0]+" "
        wposition = int(sections[1])
        start_word = min(start_word,wposition)
        end_word = max(end_word,wposition)
    object_composition = {"word":word, "start_position":start_word, "end_position":end_word, "sentence_position":sentNum}
    verb2 = pair[0]
    parts2 = verb2.split(",")
    word2 = ""
    start_word2 = 1000000000
    end_word2 = -100000000
    for part in parts2:
        sections = part.split("@$/$@")
        word2 += sections[0]
        #print(sections)
        wposition = int(sections[1])
        start_word2 = min(start_word2,wposition)
        end_word2 = max(end_word2,wposition)
    verb_composition = {"word":word2, "start_position":start_word2, "end_position":end_word2, "sentence_position":sentNum}
    verbPhrase = [verb_composition,object_composition]
    return verbPhrase
#Define Noun Parser
#Uses a breadth first search to get to the first Noun Tree
def getNountrees(t,subj,triples):
    #Defines a queue
    subtrees = []
    #Goes through the children of the tree
    for subt in t:
        #Goes through the children of the children
        for child in subt:
            #Checks if a noun phrase is present
            if isinstance(child, Tree) and child.label()=="NP":
                #Calls phrase extractor
                getNoun(child,subj,triples)
                #Then breaks
                break    
            #Else puts into queue
            if isinstance(child, Tree):
                subtrees.append(child)
    #Checks if another level of breadth first search needs to be done 
    if(len(subtrees)>1):
        getNountrees(subtrees,subj,triples)
#Define Attribute Subparser
def getNoun(t,subj,triple):
    #Defines variable to check if the tree has a sub noun phrase
    down = False
    #If another noun phrase is under then go down to that noun phrase                                          
    for child in t:
        if child.label() == "NP":
            down = True
            getNoun(child,subj,triple)
    #If there isn't a sub noun phrase tree continue start to extract sections
    if not down:
        ret = ""
        adjectives = []
        for child in t:
            #If it has a noun parse it out and add to description list
            if (child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "NNPS" or child.label() == "PRP"):
                ret += child[0] + ","
            #If it has a description word then add to adjective list
            elif (child.label() == "JJ" or child.label() == "JJR" or child.label() == "NNP" or child.label() == "JJS" or child.label() == "CD"):
                adjectives.append(child[0])
        #Add to subject list
        subj.append(ret)
        #Adds triples for the adjectives 
        for adj in adjectives:
            triple.append(ret + ";hasQuality;" + adj)
hit = False
#Define Verb Parser
#Finds the deepest Verb Phrase via depth-first search
def getVerbtrees(t,verb,obj,triples):
    #Defines if a verb phrase has been hit upon
    stop = False
    #Loops through all of the children
    for child in t:
        if isinstance(child,Tree) and (child.label()=="VP" or child.label()=="S"):
            #Goes deeper into the tree
            ret = getVerbtrees(child,verb,obj,triples)
            #Checks about the first thing to tab a object to
            if not (ret==True) and child.label()=="VP":
                #The first word phrase hit upon and the tagging will discontinue
                #The objects that the verb refers to will be taken out
                getObject(child,obj, ret,triples)
                stop = True
        #If a verb is found take out relevant section
        elif isinstance(child,Tree) and (child.label()=="VB" or child.label()=="VBD" or child.label()=="VBG" or child.label()=="VBN" or child.label()=="VBP" or child.label()=="VBZ"):
            return child[0]
    return stop
#Define Object Parser
#Link is placed to directly link object to verb phrase
def getObject(t,obj,link,triples):
    #Loops though the children of the verb phrase
    for objects1 in t:
        #If a preposition or verb phrase is hit upon it calls noun extractor
        if objects1.label() == "PP" or objects1.label() == "NP":
            temparr = []
            getNoun(objects1,temparr,triples)
            for objects2 in temparr:
                obj.append(link + ";" + objects2)
        #If it hits upon an adjective phrase it calls an adjective extractor
        elif objects1.label() == "ADJP":
            temparr = []
            getAdjective(objects1,temparr)
            for objects2 in temparr:
                obj.append(link + ";" + objects2)
#Define Adjective Subparser
def getAdjective(t,subj):
    for child in t:
        if (child.label() == "JJ" or child.label() == "JJR" or child.label() == "NNP" or child.label() == "JJS" or child.label() == "CD"):
            subj.append(child[0])
        elif child.label() == "ADJP":
            getAdjective(child,subj) 
#Define Word Enumerator
def enumWord_Tree(t,numberT):
    number = numberT
    for i in range(0,len(t)):
        if not isinstance(t[i],Tree):
            t[i] += "@$/$@" + str(number)
            number+=1
            return number
        else:
            number = enumWord_Tree(t[i],number)
    return number
#Define Utility Functions
#-----------------------------------------------------------------------------------------------------------------------
#Define URI Extractor
def uri_extract(words, position):
    from rdflib import URIRef
    from nltk.corpus import wordnet as wn
    from nltk.stem import WordNetLemmatizer
    from nltk.wsd import lesk
    try:
        sent = words
        poss = nltk.pos_tag(sent)
        #print(words, position)
        pos = ""
        if poss[position][1]=="VB" or poss[position][1]=="VBD" or poss[position][1]=="VBG" or poss[position][1]=="VBN" or poss[position][1]=="VBP" or poss[position][1]=="VBZ":
            pos = "v"
        elif poss[position][1] == "NN" or poss[position][1] == "NNS" or poss[position][1] == "NNP" or poss[position][1] == "NNPS" or poss[position][1] == "PRP" or poss[position][1] == "PRP$":
            pos = "n"
        elif poss[position][1] == "JJ" or poss[position][1] == "JJR" or poss[position][1] == "JJS" or poss[position][1] == "CD":
            pos = "a"
        synset = lesk(sent, sent[position], pos)
        if str(synset) == "None":
           uri = Literal(sent[position] + "." + pos)
           return uri
        str_synset = str(synset)[8:-2]
        parts = str_synset.split(".")
        #print(sent[position] + " " + str(synset))
        #print(parts)
        lexform = parts[0]
        part_of_speech = ""
        if parts[1] == 'a':
            part_of_speech = "adjective"
        elif parts[1] == 'n':
            part_of_speech = "noun"
        elif parts[1] == 'v':
            part_of_speech = "verb"
        sensenr = str(int(parts[2]))
        uri = "http://www.w3.org/2006/03/wn/wn20/instances/synset-" + lexform + "-" + part_of_speech + "-" + sensenr
        return URIRef(uri)
    except:
        return False
def triple_unpacker(triples, sentences):
    s=0
    #If only SVO triples to be extracted
    onlyVital = True
    rdf = []
    for triple in triples:
        #Check if descriptor triples
        if triple[1]['word'] == "HasQuality" and not onlyVital:
            try:
                #For descriptor triples
                #Extract subject synset
                subj_sentpos = triple[0]['sentence_position']-1
                subj_position = triple[0]['end_position']-1
                subj =  uri_extract(word_tokenize(sentences[subj_sentpos]), subj_position)
                if subj == False: continue
                #Descriptor predicate
                pred =  URIRef("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#hasQuality")
                #Extract Adjective synset
                adj_sentpos = triple[2]['sentence_position']-1
                adj_position = triple[2]['end_position']-1
                adj = uri_extract(word_tokenize(sentences[adj_sentpos]), adj_position)
                if adj == False: continue
                rdf.append([subj, pred ,adj])
                #numMade+=1
                #print("s")
            except:
                s+=1
        elif not triple[1]['word'] == "HasQuality":  
                #For SVO triples
                #Extract subject synset
                subj_sentpos = triple[0]['sentence_position']-1
                subj_position = triple[0]['end_position']-1
                subj =  uri_extract(word_tokenize(sentences[subj_sentpos]), subj_position)
                if subj == False: continue
                #Extract predicate sysnet
                pred_sentpos = triple[1]['sentence_position']-1
                pred_position = triple[1]['end_position']-1
                pred =  uri_extract(word_tokenize(sentences[pred_sentpos]), pred_position)
                if pred == False: continue
                #Extract object synset
                obj_sentpos = triple[2]['sentence_position']-1
                obj_position = triple[2]['end_position']-1
                obj = uri_extract(word_tokenize(sentences[obj_sentpos]), obj_position)
                if obj == False: continue
                rdf.append([subj, pred , obj])
                s+=1
                #numMade+=1
                #print("s")
    return rdf
#Parse Tree Extraction
#-----------------------------------------------------------------------------------------------------------------------
#Post-Process Logical Form Triples
def triple_extraction(phrase, javaHome, coreNLP, nlp):
    #Test Setup 
    #javaHome = r"C:\Program Files\Java\jdk1.8.0_181\bin\java.exe"
    #coreNLP = r'D:\Documents\BHAVI Documents\Code\Python Code\Python Libraries\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27'
    #Set OS
    import os
    import warnings
    warnings.filterwarnings("ignore")
    java_path = javaHome
    os.environ['JAVAHOME'] = java_path
    #Logical Form Triple
    triples = []
    sentences = sent_tokenize(phrase)
    sentAt = 1
    warnings.filterwarnings('error', category=ResourceWarning)
    for sentence in sentences:
        try:
            s = nlp.parse(sentence)
            tree = Tree.fromstring(s)
            enumWord_Tree(tree,1)
            getTrees(tree,triples, sentAt)
            sentAt+=1
        except:
            pass
    #print(len(triples))
    rdf =triple_unpacker(triples, sentences)
    return rdf
import time
#phrase = r'''Parkinson's is a serious brain disorder. It takes multiple years to develop. The cause of Parkinson's is a lack of dopamine receptors in the brain. Research has been done to cure and diagnose Parkinson's.''' 
#start_time = time.time()
#print(triple_extraction(phrase,r"C:\Program Files\Java\jdk1.8.0_181\bin\java.exe", r'D:\Documents\BHAVI Documents\Code\Python Code\Python Libraries\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27'))
#print("--- %s seconds for graph creation---" % (time.time() - start_time))