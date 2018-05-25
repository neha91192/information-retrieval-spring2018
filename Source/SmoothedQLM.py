'''
Created on Apr 21, 2018

@author: nehashukla
'''
import math
from RetrievalModel import RetrievalModel

'''
Inherits Retrieval Model class. It extends computeScore() function to perform document score generation using Query likelihood Model
'''

class SmoothedQLM(RetrievalModel):
    '''
    Constants 
    '''
    lamda_val = 0.35 
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
    Computes values for all the query words.
    '''

    def computeScore(self, query_list):
        self.document_scores = {}
        tf_for_each_queries = {}
        doc_set = set()
        collection_length = len(self.tf_dict)

        for query_word in query_list:

            doc_tf_dictionary = {}
        
            # processes index entries to find term frequency for each document.
            if(query_word in self.index_entries.keys()):
                entry_list = self.index_entries[query_word]
    
                for entry in entry_list:
                    doc_entry = entry.rsplit(',', 1)
                    term_frequency_entry = doc_entry[1].strip(')')
                    doc_entry = doc_entry[0].strip()
                    doc_id = doc_entry[1:]
                    doc_set.add(doc_id)
                    doc_tf_dictionary[doc_id] = int(term_frequency_entry)
                    tf_for_each_queries[query_word] = doc_tf_dictionary
        
        
        for query in tf_for_each_queries.keys():
            doc_tf_dictionary_entry = tf_for_each_queries[query]
        
            for doc_id in doc_set:
                if(doc_id not in doc_tf_dictionary_entry.keys()):
                    tf = 0
                else:
                    tf = (doc_tf_dictionary_entry[doc_id])
                doc_weight = ((1 - self.lamda_val) * (tf/self.doc_length[doc_id]))
                collection_weight = self.lamda_val * (int(self.tf_dict[query])/collection_length)
                qscore = math.log(doc_weight + collection_weight)
                if (doc_id in self.document_scores):
                    self.document_scores[doc_id] = self.document_scores[doc_id] + qscore
                else:
                    self.document_scores[doc_id] = qscore
        
        
            
            

    '''
    Saves top result in the following order:
    query_id Q0 doc_id rank Querylikelihood_score system_name
    '''

    def saveResults(self, query_id, system_name):
        super().saveResults(query_id, system_name)


if __name__ == '__main__':
    pass