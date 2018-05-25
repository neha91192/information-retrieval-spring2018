'''
Created on Apr 7, 2018

@author: nehashukla
'''
import math
from RetrievalModel import RetrievalModel
'''
Inherits Retrieval Model class. It extends computeScore() function to perform document score generation using BM25 Scoring Model
'''
class BM25Model(RetrievalModel):
    '''
    Constants to compute BM25 score
    '''
    k1=1.2
    k2=100
    b=0.75
    ri = 0;
    R = 0;

    '''
        Constructor
    '''
    def __init__(self):
        
        super().__init__()
        
    '''
    Loads queries from the text file.  
    '''    
    def loadIndex(self):
        super().loadIndex()
        
    '''
    Processes queries from the text file.  
    '''    
    def processQueries(self):
        super().processQueries()
        
    '''
    Processes queries from the text file.  
    '''    
    def expandQuery(self):
        super().expandQuery()
        
    '''
    Processes queries from the text file.  
    '''    
    def readRelevantDocs(self):
        super().readRelevantDocs()
    
    '''
    Reads inverted list entry [term : (doc_id, frequency_of_occurence_in_that_doc) ] for each query term. 
    Stores the same in a dictionary (index_entries), where key is query term and value is the (doc_id, frequency) pairs.
    '''        
    def fetchInvertedList(self):
        super().fetchInvertedList()
    
    '''
    Finds number of terms in all the relevant documents. It also calculates the average document length of the corpus
    '''    
    def calculateDocumentLength(self):
        super().calculateDocumentLength()
    '''
    This is a Probabilistic document scoring model which takes into account information such as term occurence in the document, document length, average document length,
    relevance information, and query frequency.
    '''               
    def computeScore(self,query_list):
        self.document_scores = {}
        
        for query_word in query_list:
            
            doc_tf_dictionary = {}
            doc_list= []
            
            #processes index entries to find term frequency for each document.
            if(query_word in self.index_entries.keys()):
                entry_list = self.index_entries[query_word]
                for entry in entry_list:
                    doc_entry = entry.rsplit(',', 1)
                    term_frequency_entry = doc_entry[1].strip(')')
                    doc_entry =doc_entry[0].strip()
                    doc_id = doc_entry[1:]
                    doc_list.append(doc_id)
                    doc_tf_dictionary[doc_id] = int(term_frequency_entry)
                
                #no of documents with the given query term
                ni = len(doc_list)
                #frequency of query term in the query
                qfi = query_list.count(query_word)
                
                #for each document in the set of documents that this query term has been appeared in 
                for doc_id in doc_list:
                    K = self.k1 * ((1-self.b) + self.b*float(self.doc_length[doc_id])/float(self.average_doc_length))
                    #frequency of the query term in the document
                    fi = doc_tf_dictionary[doc_id]
                    scoring_function =math.log(((self.ri+0.5)/(self.R-self.ri+0.5))/((ni-self.ri+0.5)/(self.N-ni-self.R+self.ri+0.5)))
                    doc_term_weight = (((self.k1+1)*fi)/(K+fi))
                    query_term_weight =(((self.k2+1)*qfi)/(self.k2+qfi))
                    score =scoring_function*doc_term_weight*query_term_weight
                   
                    if(doc_id in self.document_scores):
                        self.document_scores[doc_id] = self.document_scores[doc_id] + score
                    else:
                        self.document_scores[doc_id] = score
    '''
    Saves top result in the following order:
    query_id Q0 doc_id rank BM25_score system_name
    '''
    def saveResults(self,query_id, system_name):
        super().saveResults(query_id,system_name)
    
        
if __name__ == '__main__':
    pass
        