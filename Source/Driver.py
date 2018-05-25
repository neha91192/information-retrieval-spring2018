'''
Created on Apr 24, 2018

@author: nehashukla
'''
import os
from CorpusBuilder import CorpusBuilder
from IndexBuilder import IndexBuilder
from BM25Model import BM25Model
from SmoothedQLM import SmoothedQLM
from TfIdf import TfIdf

class Driver:
    stemmed_index_folder='/indexer_output_stem_cacm/'
    stopped_index_folder='/indexer_output_stop_cacm/'
    index_folder='/indexer_output_cacm/'
    rel_path=os.path.dirname(os.path.abspath(__file__))
    corpus_path='/cacm_corpus'
    
    def runCorpusBuilder(self,is_stemmed_corpus):
        corpusBuilder = CorpusBuilder()
        if(is_stemmed_corpus): 
            corpusBuilder.create_stemmed_corpus_files()    
        else:
            corpusBuilder.initialize_doc_keys()
            corpusBuilder.create_corpus() 
            
    def runIndexBuilder(self, is_stopping,is_stemmed_corpus):
        n=1
        builder = IndexBuilder(False,is_stopping, is_stemmed_corpus)
        if(is_stemmed_corpus):
            builder.output_files_location = self.stemmed_index_folder
        if(is_stopping):
            builder.output_files_location = self.stopped_index_folder
        if(not(is_stemmed_corpus) and not(is_stopping)):
            builder.output_files_location = self.index_folder
        builder.build_inverted_index(n)
        builder.generate_tf_table()
        builder.generate_df_table()
        
    def bm25(self):
        print("Starting Baseline run...")
        bm25 = BM25Model();
        bm25.index_folder_location = self.index_folder
        bm25.loadIndex()
        bm25.processQueries()
        bm25.fetchInvertedList()
        bm25.calculateDocumentLength()
        
        for query_id, query in bm25.queries.items():
            querylist= query.split()
            bm25.computeScore(querylist)
            bm25.saveResults(query_id, 'BM25Model')
        
        print("Baseline run completed successfully!")
        
        print("Starting run for stemmed corpus...")
        bm25 = BM25Model();
        bm25.index_folder_location = self.stemmed_index_folder
        bm25.loadIndex()
        bm25.processStemmedQueries()
        bm25.fetchInvertedList()
        bm25.calculateDocumentLength()
        
        for query_id, query in bm25.queries.items():
            querylist= query.split()
            bm25.computeScore(querylist)
            bm25.saveResults(query_id, 'BM25Model_Stemmed')
            
        print("Run for stemmed corpus completed successfully!")
         
        print("Starting run for stopping with no stemming...")   
        bm25 = BM25Model();
        bm25.stopping_required = True
        bm25.index_folder_location = self.stopped_index_folder
        bm25.loadIndex()
        bm25.processQueries()
        bm25.fetchInvertedList()
        bm25.calculateDocumentLength()
        
        
        for query_id, query in bm25.queries.items():
            querylist= query.split()
            bm25.computeScore(querylist)
            bm25.saveResults(query_id, 'BM25Model_Stopped')
        print("Run for stopping with no stemming completed successfully!")
            
            
    def sqlm(self):
        print("Starting Baseline run...")
        sqlm = SmoothedQLM();
        sqlm.index_folder_location = self.index_folder
        sqlm.loadIndex()
        sqlm.processQueries()
        sqlm.fetchInvertedList()
        sqlm.calculateDocumentLength()
           
        for query_id, query in sqlm.queries.items():
            querylist= query.split()
            sqlm.computeScore(querylist)
            sqlm.saveResults(query_id, 'SQLModel')
          
        print("Baseline run completed successfully!")
        
        print("Starting run for stemmed corpus...")
        sqlm = SmoothedQLM();
        sqlm.index_folder_location = self.stemmed_index_folder
        sqlm.loadIndex()
        sqlm.processStemmedQueries()
        sqlm.fetchInvertedList()
        sqlm.calculateDocumentLength()
        
        for query_id, query in sqlm.queries.items():
            querylist= query.split()
            sqlm.computeScore(querylist)
            sqlm.saveResults(query_id, 'SQLModel_Stemmed')
        print("Run for stemmed corpus completed successfully!")
        
        print("Starting run for stopping with no stemming...")     
        sqlm = SmoothedQLM();
        sqlm.stopping_required = True
        sqlm.index_folder_location = self.stopped_index_folder
        sqlm.loadIndex()
        sqlm.processQueries()
        sqlm.fetchInvertedList()
        sqlm.calculateDocumentLength()
        
        for query_id, query in sqlm.queries.items():
            querylist= query.split()
            sqlm.computeScore(querylist)
            sqlm.saveResults(query_id, 'SQLModel_Stopped')
        
        print("Run for stopping with no stemming completed successfully!")
        
        print("Starting run with query enrichment..")
        sqlm = SmoothedQLM()
        sqlm.index_folder_location = self.index_folder
        sqlm.loadIndex()
        sqlm.processQueries()
        sqlm.readRelevantDocs()
        sqlm.expandQuery()
        sqlm.fetchInvertedList()
        sqlm.calculateDocumentLength()
        
        for query_id, query in sqlm.queries.items():
            list_q =sqlm.query_terms_for_expansion[query_id]
            querylist= query.split() + sqlm.query_terms_for_expansion[query_id]
            sqlm.computeScore(querylist)
            sqlm.saveResults(query_id, 'SQLModel_QE')
            
        print("Run with query enrichment ended successfully!")
            
    def tfidf(self):
        print("Starting Baseline run...")
        tfidf = TfIdf();
        tfidf.index_folder_location = self.index_folder
        tfidf.loadIndex()
        tfidf.processQueries()
        tfidf.fetchInvertedList()
        tfidf.calculateDocumentLength()
        
        for query_id, query in tfidf.queries.items():
            querylist= query.split()
            tfidf.computeScore(querylist)
            tfidf.saveResults(query_id, 'TfIdfModel')
        print("Baseline run completed successfully!")
        
        print("Starting run for stemmed corpus...")
        tfidf = TfIdf();
        tfidf.index_folder_location = self.stemmed_index_folder
        tfidf.loadIndex()
        tfidf.processStemmedQueries()
        tfidf.fetchInvertedList()
        tfidf.calculateDocumentLength()
        
        for query_id, query in tfidf.queries.items():
            querylist= query.split()
            tfidf.computeScore(querylist)
            tfidf.saveResults(query_id, 'TfIdfModel_Stemmed')
            
        print("Run for stemmed corpus completed successfully!")
         
        print("Starting run for stopping with no stemming...")    
        tfidf = TfIdf();
        tfidf.stopping_required = True
        tfidf.index_folder_location = self.stopped_index_folder
        tfidf.loadIndex()
        tfidf.processQueries()
        tfidf.fetchInvertedList()
        tfidf.calculateDocumentLength()
        
        for query_id, query in tfidf.queries.items():
            querylist= query.split()
            tfidf.computeScore(querylist)
            tfidf.saveResults(query_id, 'TfIdfModel_Stopped')
        print("Run for stopping with no stemming completed successfully!")
            
            

def main():  
    driver = Driver()
    print("Building corpus for baseline runs..")
    driver.runCorpusBuilder(False)
    print()
    driver.runCorpusBuilder(True)
    print("Building Index for baseline runs..")
    driver.runIndexBuilder(False, False)
    print("Index for baseline runs has been created successfully at location: "+driver.rel_path+driver.index_folder)
    print()
    print("Building Index for stopping with no stemming..")
    driver.runIndexBuilder(True, False)
    print("Index (without stopwords) has been created successfully at location: "+driver.rel_path+driver.stopped_index_folder)
    print()
    print("Building Index for stemmed corpus..")
    driver.runIndexBuilder(False,True)
    print("Index for stemmed corpus has been created successfully at location: "+driver.rel_path+driver.stemmed_index_folder)
    print()
    print("Running BM25 Retrieval Model for the following runs:")
    driver.bm25() 
    print()
    print("Running Smoothed Query Likelihood Retrieval Model for the following runs:")
    driver.sqlm()
    print()
    print("Running TfIdf Retrieval Model for the following runs:")
    driver.tfidf()
    
    
    

    
    
    
        

if __name__ == '__main__':
    main()
