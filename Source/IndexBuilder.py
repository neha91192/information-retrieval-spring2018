'''
Created on Mar 16, 2018

@author: nehashukla
'''

import os
import collections
import io
import sys



'''
Builds Inverted Index from the downloaded html files
'''

class IndexBuilder:
    
    encoding = 'utf-8'
    corpus_location = '/cacm_corpus/'
    stemmed_corpus_location= '/cacm_stemmed_corpus/'
    html_content_filespath = '/downloaded_files/bfs_content_files/'
    
    corpus_files_path = ""
    rel_path=""
    index_file_name = ""
    tf_table_file_name = ""
    df_table_file_name = ""
    stopwordsfile = '/common_words'
    stopwords_list = []
    
    
    '''
    Constructor
    '''
    def __init__(self,position, is_stopping, is_stemmed_corpus):
        self.doc_terms_table = {}
        self.inverted_index = {}
        self.store_position = position
        self.tf_table = {}
        self.df_table = {}
        self.doc_keys = {}
        self.stopping_required = is_stopping
        self.is_stemmed= is_stemmed_corpus
        self.output_files_location = ""

    def intializeStoplist(self):
        #if stopwords are to be excluded from the inverted index
        rel_path = os.path.dirname(os.path.abspath(__file__))
        with open(rel_path +self.stopwordsfile, 'r', encoding="utf-8") as stopwordsfile:
            self.stopwords_list = stopwordsfile.read().splitlines()

        
    '''
    Generates n-gram inverted index. 
    '''
    def build_inverted_index(self, n):
        print("Building inverted index..")
        self.inverted_index = collections.defaultdict(list)
        rel_path = os.path.dirname(os.path.abspath(__file__))
        if(self.is_stemmed):
            self.corpus_files_path = rel_path+self.stemmed_corpus_location
        else:
            self.corpus_files_path = rel_path+self.corpus_location
        self.index_file_name = rel_path+self.output_files_location+'indexer_'+str(n)
        self.df_table_file_name = rel_path+self.output_files_location+'df_table_'+str(n)
        self.tf_table_file_name = rel_path+self.output_files_location+'tf_table_'+str(n)
        doc_terms_table_file = rel_path+self.output_files_location+'doc_terms_table_'+str(n)
        
        if not os.path.exists(rel_path+self.output_files_location):
            os.makedirs(rel_path+self.output_files_location, 0o777)
        
        if(self.store_position):
            self.index_file_name = self.index_file_name+'_position'
        if(self.stopping_required):
            self.intializeStoplist() 
        
        for doc_id in os.listdir(self.corpus_files_path):
            with open(self.corpus_files_path+doc_id, 'r', encoding=self.encoding) as file:
                data=file.read().replace('\n', ' ')
    
            tokens = data.split(' ')
            
            if(self.stopping_required):    
                tokens = self.remove_stopWords(self.stopwords_list,tokens)
                
            term_set = set()
            i=0
            terms=[]
            while(i<len(tokens)):
                if((i+n)>len(tokens)):
                    term=tokens[i:]
                else:
                    term = tokens[i:(i+n)]
                if('' not in term):
                    terms.append(term)
                    unique_term = ""
                    for item in term:
                        unique_term = unique_term + str(item) + " "
                    unique_term = unique_term[:-1]
                    term_set.add(unique_term)
                i=i+1
                
            if(n==1 and self.store_position):
                self.update_terms_with_positions(terms, doc_id) 
            else: 
                self.update_terms(terms,doc_id)
            self.doc_terms_table[doc_id] = len(term_set)
                
        sorted_inverted_index = sorted(self.inverted_index.keys())
        with io.open(self.index_file_name, 'w+', encoding=self.encoding) as file:
            for k in sorted_inverted_index:
                postings = self.inverted_index[k]
                new_posting = k+": "
                for posting in postings:
                    if(self.store_position):
                        new_posting = new_posting+'('+posting[0].strip()+','+str(posting[1])+','+str(posting[2])+'), '
                    else:
                        new_posting = new_posting+'('+posting[0].strip()+','+str(posting[1])+'), '
                new_posting = new_posting[:-2]+'\n'
                file.write(new_posting)
            
        sorted_doc_terms_table = sorted(self.doc_terms_table, key=lambda x:self.doc_terms_table.get(x) ,reverse=True)
        with io.open(doc_terms_table_file, 'w+', encoding = self.encoding) as file:
            for doc_id in sorted_doc_terms_table:
                count =self.doc_terms_table[doc_id]
                entry = doc_id+': '+str(count)+'\n'
                file.write(entry)
                
        print("Indexer is now created successfully. Please check the indexer file at the location: "+rel_path+self.output_files_location)
  
    '''
    Updates inverted index for all the terms (n-gram words) in the format:  TERM : [[doc_id1, tf], [doc_id2, tf]...,[doc_idn,tf]]
    '''   
    def update_terms(self,terms,doc_id):
        
        for term in terms:
            term_as_key = ' '.join(term)
            posting = self.inverted_index.get(term_as_key)
            if(posting is None):
                posting = [doc_id,1]
                self.inverted_index[term_as_key].append(posting)
            else:
                for item in posting:
                    is_updated=False
                    if(item[0]==doc_id):
                        item[1] = item[1]+1
                        is_updated =True
                if(not(is_updated)):
                    posting.append([doc_id, 1])
    
    '''
    Updates inverted index for all the terms (unigram only) with positions in the format: TERM: [[doc_id1, tf,[positions]], [doc_id2, tf, [positions]...,[doc_idn, tf, [positions]]
    '''
    def update_terms_with_positions(self,terms,doc_id):
        
        for i,term in enumerate(terms):
            posting = self.inverted_index.get(term[0])
            if(posting is None):
                posting = [doc_id,1,[i]]
                self.inverted_index[term[0]].append(posting)
            else:
                for item in posting:
                    is_updated=False
                    if(item[0]==doc_id):
                        item[1] = item[1]+1
                        item[2].append(i)
                        is_updated =True
                if(not(is_updated)):
                    posting.append([doc_id, 1, [i]])
    '''
    Generates Term frequency table. The entries in this table are sorted in the descending order of the count of occurrences of each terms.
    '''                
    def generate_tf_table(self):
        print("Creating term frequency table..")
        
        for term in self.inverted_index.keys():
            postings = self.inverted_index[term]
            count=0 
            for posting in postings:
                count = count + posting[1]
            self.tf_table[term] = count
            
        sorted_tf_table = sorted(self.tf_table, key=lambda x:self.tf_table.get(x) ,reverse=True)
        
        with io.open(self.tf_table_file_name, 'w+', encoding=self.encoding) as file:
            for key in sorted_tf_table:
                row = key+": "+str(self.tf_table[key])+'\n'
                file.write(row)
                
        print("Term frequency table is now created successfully. To see this table, please check the path: "+self.output_files_location)
                
    def generate_df_table(self):
        print("Creating document frequency table..")
        for term in self.inverted_index.keys():
            postings = self.inverted_index[term]
            
            doc_id_entry = ""
            for posting in postings:
                doc_id_entry = doc_id_entry + posting[0]+' '
            doc_id_entry = doc_id_entry.strip()
            doc_frequency_entry = len(postings)
            self.df_table[term] = [doc_id_entry, doc_frequency_entry]
            
        sorted_df_table = sorted(self.df_table.keys())
            
        with io.open(self.df_table_file_name, 'w+', encoding=self.encoding) as file:
            for key in sorted_df_table:
                entry = self.df_table[key]
                row = key+': '+'['+entry[0]+']'+' '+str(entry[1])+' \n'
                file.write(row)
        print("Document frequency table is now created successfully. To see this table, please check the path: "+self.output_files_location)
        
        
    def remove_stopWords(self,stopwords_list, tokens):
        terms = tokens
        stopwords_in_doc = set(tokens).intersection(set(stopwords_list))
        index_terms = [term for term in terms if term not in stopwords_in_doc]
        return index_terms       
 
    
# def main(n, position):
 
def main(is_stopping,is_stemmed_corpus): 
    n=1
    builder = IndexBuilder(is_stopping, is_stemmed_corpus)
    if(is_stemmed_corpus):
        builder.output_files_location = '/indexer_output_stem_cacm/'
    else:
        builder.output_files_location = '/indexer_output_cacm/'
    builder.build_inverted_index(n)
    builder.generate_tf_table()
    builder.generate_df_table()

        
# if __name__ == '__main__':
#         
#     if(len(sys.argv)==1):
#         raise Exception("Please pass the argument: n = (1, 2, 3) and position as True or False")
#     else:
#         n =int(sys.argv[1])
#         position = sys.argv[2]
#         if(position == 'False'):
#            position = False
#         elif(position == 'True'):
#            position = True
#            
#         
#     main(n,position)
        
if __name__ == '__main__':

    main()
        
                
                    
