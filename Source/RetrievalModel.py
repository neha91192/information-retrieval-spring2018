'''
Created on Apr 3, 2018

@author: nehashukla
'''
import os
import collections
from bs4 import BeautifulSoup 
from CorpusBuilder import CorpusBuilder
import os.path

'''
Loads user queries from the text file, find index entries specific to those queries , computes document score and save results in a text file
'''
class RetrievalModel:
    '''
    Variables specific to location of corpus and indexer location, 
    
    '''
    
    index_file_name = '/indexer_1'
    doc_terms_file = '/doc_terms_table_1'
    corpus_location = '/cacm_corpus'
    search_results_file = '/Search_Results_cacm'
    query_file_name = '/cacm_query.txt'
    stemmed_query_file= '/cacm_stem_query.txt'
    doc_length = {}
    average_doc_length=  0
    resultfile = '/Search_Results_cacm_SQLModel'
    tf_file = '/tf_table_1'
    df_file = '/df_table_1'
    stopwordsfile = '/common_words'
    
    hits = 100
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.index_entries = {}
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        self.document_scores = {}
        self.N = len(os.listdir(self.rel_path+self.corpus_location))
        self.queries = {}
        self.rawQueries ={}
        self.relevant_docs_for_query = {}
        self.index_list = []
        self.tf_dict = {}
        self.df_table = {}
        self.query_terms_for_expansion= {}
        self.stopwords_list = []
        self.stopping_required = False
        self.index_folder_location = ""
    
    '''
    Loads queries from the text file.  
    '''    
    def loadIndex(self):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        with open(self.rel_path+self.index_folder_location+self.index_file_name, 'r', encoding="utf-8") as file:
            self.index_list = file.read().splitlines()
            
        with open(self.rel_path+self.index_folder_location+self.tf_file, 'r', encoding="utf-8") as tffile:
            lines= tffile.read().splitlines()
            for line in lines:
                entry = line.split(": ")
                self.tf_dict[entry[0]] = entry[1]
         
        with open(self.rel_path+self.index_folder_location+self.df_file, 'r', encoding="utf-8") as dffile:
            lines= dffile.read().splitlines()
            for line in lines:
                entry = line.split(": ")
                self.df_table[entry[0]] = entry
        
        with open(self.rel_path+self.stopwordsfile, 'r', encoding="utf-8") as stopwordsfile:
            self.stopwords_list =stopwordsfile.read().splitlines()
            
                        
    '''
    Reads query from query file and applies punctuation handler.
    '''
    def processQueries(self):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        filename = self.rel_path+self.query_file_name
        self.rawQueries = collections.OrderedDict()
        with open(filename, 'r', encoding="utf-8") as file:
            data=file.read()
            
            soup = BeautifulSoup(data, "html.parser")
            content = soup.findAll("doc")
            for entry in content:
                query_id_tag = entry.find("docno")
                queryid= query_id_tag.getText().strip()
                query_id_tag.extract()
                query = entry.getText().strip()
                self.rawQueries[queryid] = query
                
        self.queries = collections.OrderedDict()   
        corpusbuilder = CorpusBuilder()
        for query_id in self.rawQueries.keys():
            query_text = self.rawQueries[query_id]
            if(self.stopping_required):
                query_text_list = query_text.split()
                s_query= self.remove_stopWords(self.stopwords_list, query_text_list)
                query_text = ''.join(s_query[0:len(s_query)-1])
            content =""
            content = corpusbuilder.punctuation_handler(content, self.rawQueries[query_id])
            self.queries[query_id]=content
            
          
    def processStemmedQueries(self):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        filename = self.rel_path+self.stemmed_query_file
        self.rawQueries = collections.OrderedDict()
        with open(filename, 'r', encoding="utf-8") as file:
            lines=file.read().splitlines()

            for query_id,query in enumerate(lines):
                self.rawQueries[str(query_id+1)] = query
                 
        self.queries = collections.OrderedDict()   
        corpusbuilder = CorpusBuilder()
        for query_id in self.rawQueries.keys():
            content =""
            content = corpusbuilder.punctuation_handler(content, self.rawQueries[query_id])
            self.queries[query_id]=content
            
    '''
    Top 5 less frequent terms in query (Luhn's law)
    Top 10 less frequent terms in top 2 relevant documents
    Calculate Dice's coefficient for all 5 chosen terms of the query with the chosen terms in the document. 
    Select top result for each terms in query. This ensures adding terms relevant to the query
    '''
    def expandQuery(self): 
        
        for query_id in self.queries.keys():
            query_expansion_list = []
            #term_association_matrix = {}
            score_dict_for_terms = {}
            sorted_tf_dict_query = collections.OrderedDict()
            
            query = self.queries[query_id]
            query_terms = query.split()
            #remove stopwords
            terms = query_terms
            stopwords_in_query_terms = set(terms).intersection(set(self.stopwords_list))
            query_terms = [term for term in query_terms if term not in stopwords_in_query_terms]
            
            for term in query_terms:
                if(term in self.tf_dict.keys()):
                    sorted_tf_dict_query[term] = self.tf_dict[term]
                
            
            sortedOrderbytf = sorted(sorted_tf_dict_query, key=lambda x:int(sorted_tf_dict_query.get(x)))
            
      
            if(query_id in self.relevant_docs_for_query.keys()):
                relevantdocs = self.relevant_docs_for_query[query_id]
                for doc_count in range(0,len(relevantdocs)):
                    if(doc_count<2):
                        term_freq = collections.OrderedDict()
                        relevant_file =self.rel_path+self.corpus_location+'/'+relevantdocs[doc_count]
                        if(os.path.isfile(relevant_file)):
                            with open(self.rel_path+self.corpus_location+'/'+relevantdocs[doc_count], 'r', encoding="utf-8") as file:
                                words = file.read().split() 
                                for word in words:
                                    if(word in term_freq.keys()):
                                        term_freq[word] = term_freq[word] +1
                                    else:
                                        term_freq[word] = 1
                                        
                                list_keys = term_freq.keys()
                                stopwords_in_doc_terms = set(list_keys).intersection(set(self.stopwords_list))
                             
                                for key in stopwords_in_doc_terms:
                                    if key in term_freq:
                                        del term_freq[key]
                                
                                for word in sortedOrderbytf:
                                    if word in term_freq:
                                        del term_freq[word]
                                
                                sortedOrderbytf_rel = sorted(term_freq, key=lambda x:term_freq.get(x))
                                
                                for i in range(0,len(sortedOrderbytf)):
                                    if(i<5):
                                        query_term = sortedOrderbytf[i]
                                        score_dict = self.calculateDicesCoefficient(query_term, sortedOrderbytf_rel[:10])
                                        
                                        for key in score_dict.keys():
                                            if(key in score_dict_for_terms.keys()):
                                                score_dict_for_terms[key] = score_dict_for_terms[key]+score_dict[key]
                                            else:
                                                score_dict_for_terms[key] = score_dict[key]
                                    else:
                                        break
                    else:
                        break
            
    
            sortedOrderByScore = sorted(score_dict_for_terms, key=lambda x:score_dict_for_terms.get(x), reverse =True)
            query_expansion_list = sortedOrderByScore[:10]
            exp_list = list(set(query_expansion_list))
            
            self.query_terms_for_expansion[query_id] = exp_list
                                
            
    
    def calculateDicesCoefficient(self, query_term, document_term_list):
        dices_score = {}
        df_entry_na= self.df_table[query_term]
        doc_frequency_pair = df_entry_na[1].strip().rsplit(" ", 1)
        doc_list_na = doc_frequency_pair[0]
        na = int(doc_frequency_pair[1])
        
        for term in document_term_list:
            df_entry_nb = self.df_table[term]
            doc_frequency_pair = df_entry_nb[1].strip().rsplit(" ", 1)
            doc_list_nb = doc_frequency_pair[0]
            nb = int(doc_frequency_pair[1])
            nab = len(set(doc_list_na).intersection(set(doc_list_nb)))
            
            score = (2*nab)/(na+nb)
            dices_score[term] = score
        
        return dices_score
         
        
    
    def readRelevantDocs(self):
        with open(self.rel_path+self.resultfile, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
            for line in lines:
                if(line[0].isdigit()):
                    rel_doc_entry = line.split()
                    queryid = rel_doc_entry[0]
                    if(queryid in self.relevant_docs_for_query.keys()):
                        value = self.relevant_docs_for_query[queryid]
                        value.append(rel_doc_entry[2])
                    else:
                        value=[]
                        value.append(rel_doc_entry[2])
                        self.relevant_docs_for_query[queryid] = value
        
        
    '''
    Reads inverted list entry [term : (doc_id, frequency_of_occurence_in_that_doc) ] for each query term. 
    Stores the same in a dictionary (index_entries), where key is query term and value is the (doc_id, frequency) pairs.
    '''        
    def fetchInvertedList(self):
        #read indexer file
        entries = []
        query_words = []
        for query in self.queries.values():
            query_words = query_words + query.split()
        
        query_words = set(query_words)
        
        for line in self.index_list:
            entries = line.split(':')

            if entries[0] in query_words: 
                doc_list_text = entries[1]
                doc_list = doc_list_text.split(', ')
                self.index_entries[entries[0]] = doc_list
                    
    '''
    Uses Retrieval model to compute document score. Implementation of this function can be either done using BM25 scoring model, tfidf, or Query likelihood model 
    '''
                     
    def computeScore(self, query_list): 
        pass
        
        
    '''
    Finds number of terms in all the relevant documents. It also calculates the average document length of the corpus
    '''    
    def calculateDocumentLength(self):
        with open(self.rel_path+self.index_folder_location+self.doc_terms_file, 'r', encoding="utf-8") as file:
            for line in file:
                entries = line.split(':')
                self.doc_length[entries[0]] = int(entries[1].strip())
            self.average_doc_length  = sum(self.doc_length.values())/self.N
            
        
    '''
    Saves top result in the following order:
    query_id Q0 doc_id rank <doc_score> system_name
    '''
    def saveResults(self,query_id,system_name):
        
        sorted_scores = sorted(self.document_scores, key=lambda x:self.document_scores.get(x) ,reverse=True)
        
        result_size = len(self.document_scores.keys())
        if(result_size>self.hits):
            result_size = self.hits
            
        with open(self.rel_path+self.search_results_file+'_'+system_name, 'a', encoding='utf-8') as file:
            
            heading = "Query "+query_id+" "+self.queries[query_id]+'\n'
            file.write(heading)
            for index,key in enumerate(sorted_scores):
                if(index<self.hits): 
                    line = str(query_id)+' Q0 '+key+' '+str(index+1)+' '+str(self.document_scores[key])+' '+system_name+' '+'\n'
                    file.write(line)
                else:
                    break
    
                
    def remove_stopWords(self,stopwords_list, tokens):
        terms = tokens
        stopwords_in_doc = set(tokens).intersection(set(stopwords_list))
        index_terms = [term for term in terms if term not in stopwords_in_doc]
        return index_terms 

    def levenshteinDistance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]
    

if __name__ == '__main__':
    pass
