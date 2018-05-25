________________________________________________________
Phase 1: (All files are present in Source Folder)

--Information Retrieval System is built on python 3.5+ version.
  * uses BeautifulSoup 4 for parsing HTML pages

-- To install BeautifulSoup 4, run pip install beautifulsoup4 or python setup.py install 



--Now To use this retrieval system, please run Driver.py class.  

--Steps to run Driver.py class:
	python Driver.py

--Output files can be categorized as follows. (They are present at the location Source/Output/Phase1_Output), but when you run, they will be created in the source folder:
1. Search results (10 runs): (3 baseline (Task 1), 1 query enrichment run (Task 2), 3 stopped and 3 stemmed   (Task 3) = Total 10 files) can be found in the 
2.Intermediate result: corpus(2) and indexes(3): (cacm_corpus and cacm_stemmed_corpus)  

The format of the search results output file is--> Search_Results_cacm_<system_name>

---------------------
 
--Lucene Retrieval System is built on Java 4.7.2 version.
--Lucene.java is the source program for Lucene Retrieval System.

--To run this program, import the source package 'Lucene' present in the assignment folder. You can use Java Eclipse IDE (Juno or above)

--Steps to run Lucene.java on Eclipse:

1. Import project:
Go to File --> Import --> General --> Existing projects into workspace --> Browse source directory and select 'Lucene'
folder of the assignment folder

2. Add classpath variable:
Go to Project --> Properties --> Java Build Path --> Libraries --> choose Add Variable --> click on Configure variable button
--> click 'New' button and enter following details --> Name: LUCENE Folder Path as: <source>/Lucene/lucene_jars
Click on 'Ok', 'Apply and Close' and when it asks for Apply full build, choose 'yes'. 

3. Now using eclipse console, select 'Run' option and select 'Lucene' class to run. It will ask for the following details:
 a. Full path for index location:
 Enter 'Index' to create Index folder. You can find this folder created inside the Lucene folder
 b. Path to Corpus location:
 Enter '../cacm'. It will index all the documents present in the corpus folder outside the Lucene folder
 c. The program will automatically load queries from the cacm_query.txt file present in the assignment folder. The output for this program can be found in 'Lucene-results.txt' file at the location /Source/Output/Phase1_Output(but when you run, they will be created in the current folder).

________________________________________________________
Phase 2:
Place all the files from Phase 2 folder in one directory

Use a fancy editor like PyCharm to complile and run this code
The source code is present in the file SnippetGenerationv5.py
External libraries used in this file are as follows:
os           :for directory operations
operator     :for sorting dictionaries
math         :to take floor
re & string  :for punctuation handling

Make Sure you have the above libraries installed, Once you have all the required libraries installed you are good to go.
This program asks for the result like of the retrieval model as input which are present in the folder.

Snippets for all the 8 runs have been included.The results for all the runs are also provided in the /Source/Output/Phase2_Output folder (but when you run, they will be created in the current folder).
for eg: snippets for BM25 model are placed in Snippets-Search_Results_cacm_BM25Model


Each folder contains an html file of snippets name after queryid
for eg. snippets for query id 9 are placed in 9.html
_________________________________________________________
Phase 3:
Place all the files from Phase 3 folder in one directory
Use a fancy editor like PyCharm to complile and run this code
The source code is present in the file Evaluation.py

External libraries used in this file are as follows:
os  :  for directory operations

The class relevance in Evaluation.py contains the following methods
evaluatePrecision()    :  calculates precision for every result
evaluateRecall()       :  calculates precision for every result
evaluateAP()           :  calculates average precision for each query
evaluateMAP()          :  calculates mean average precision for all queries
evaluateRR()           :  calculates reciprocal rank for each query
evaluateMRR()          :  calculate mean reciprocal rank across queries
evaluatePat5andPat20() :  calculates precision at rank 5 and rank 20 for each query

Evaluation.py requires 2 files as input:
1st : Result file, which contains results from the run of retrieval model 
For eg: Search_Results_cacm_BM25Model which result file of BM25 model
Result file for each retrival Model is provided in the folder

2nd : Relevance file, this file contains relevance information provided to us as part of project.
This file is cacm.rel which is also present in the the folder

Results:
Result for each of the baseline run is present in the /Source/Output/Phase3_Output folder (but when you run, they will be created in the current folder)

This Folder contains file for each retrieval model
The files included in this folder are described as follows

Eg: Evaluation_Results_Search_Results_cacm_Lucene includes the following files

Lucene-results-cacm-relevancePrecison: Files of this type have a format of entries 

->query_id doc_id relevant_nonrelevant score

Lucene-results-cacm-relevanceRecall: Files of this type have a format of entries same as above

Lucene-results-cacm-relevancePat5andPat20: Files of this type have a format of entries same as above

Lucene-results-cacm-relevanceMAP: files of this type contains MAP for that particular retrieval model

Lucene-results-cacm-relevanceMRR: files of this type contains MRR for that particular retrieval model

Referenced Links:

https://www.crummy.com/software/BeautifulSoup/
https://nlp.stanford.edu/IR-book/html/htmledition/relevance-feedback-and-query-expansion-1.html


