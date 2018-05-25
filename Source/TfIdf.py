'''
Created on Apr 21, 2018

@author: nehashukla
'''
import math
from RetrievalModel import RetrievalModel
'''
Inherits Retrieval Model class. It extends computeScore() function to perform document score generation using BM25 Scoring Model
'''
class TfIdf(RetrievalModel):
    '''
    Constants 
    '''
   

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
    Firstly, it computes tf values for all the query word. Then it computes term frequency weight for each query words using tf/sum(all tf values for each query words) 
    formula. Now it finds document frequency weight using similar approach and the formula for the same is log(N/ni). The total score is tf.idf
    '''               
    def computeScore(self,query_list):
        self.document_scores = {}
        
        for query_word in query_list:
            
            doc_tf_dictionary = {}
            doc_list= []
        
            tf_component = 0
            #processes index entries to find term frequencies for q1, q2, q3 for each document.
            if(query_word in self.index_entries.keys()):
                entry_list = self.index_entries[query_word]
                for entry in entry_list:
                    doc_entry = entry.rsplit(',', 1)
                    term_frequency_entry = doc_entry[1].strip(')')
                    doc_entry =doc_entry[0].strip()
                    doc_id = doc_entry[1:]
                    doc_list.append(doc_id)
                    tf_value =int(term_frequency_entry)
                    doc_tf_dictionary[doc_id] = tf_value

                #no of documents with the given query term
                ni = len(doc_list)
                
                idf_component = math.log(self.N/ni) 
                
                for doc_id in doc_list:
                    tf_component = doc_tf_dictionary[doc_id]/self.doc_length[doc_id]
                    score = tf_component*idf_component
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
        