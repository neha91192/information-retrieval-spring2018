'''
Created on Mar 23, 2018

@author: nehashukla
'''
import os  
from bs4 import BeautifulSoup 
import re
import io
import string
import collections

class CorpusBuilder:  
    
    html_content_filespath = '/cacm/'
    corpus_location = '/cacm_corpus/'
    stemmed_corpus_location= '/cacm_stemmed_corpus/'
    encoding = 'utf-8'
    file_extension = '.html'
    stemmed_file='/cacm_stem.txt'
    f_id = 1
    
    '''
    Constructor
    '''
    def __init__(self):
        self.doc_keys = {}
        
    def initialize_doc_keys(self):
        self.doc_keys= collections.OrderedDict()
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = self.rel_path + self.html_content_filespath
        for i,file in enumerate(os.listdir(folder_path)):
            self.doc_keys[i] = file.split('.')[0]
        
    '''
    Generates corpus from the downloaded html files. 
    '''
    
    def create_corpus(self):
        print("Initializing Corpus Creation process..")
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = self.rel_path + self.html_content_filespath
        self.corpus_files_path = self.rel_path+self.corpus_location
        
        if not os.path.exists(self.corpus_files_path):
            os.makedirs(self.corpus_files_path, 0o777)

        for filename in os.listdir(folder_path):
            
            with open(folder_path+filename, 'r', encoding=self.encoding) as file:
                data=file.read()
            
            soup = BeautifulSoup(data, "html.parser")
            content = soup.find("html")

            body_content = self.retrieve_body_content(content)
            soup_title= BeautifulSoup(data, "html.parser").find(re.compile('title')) 
            file_content = "" 
            if(soup_title!=None):
                title = re.sub('\s+', ' ', soup_title.getText()).strip()
                file_content = self.punctuation_handler(file_content, title)
            plain_text = re.sub('\s+', ' ', body_content.getText()).strip()
            file_content = self.punctuation_handler(file_content, plain_text)
            filename= filename.split('.')[0]

            with io.open(self.corpus_files_path+filename, 'w+', encoding=self.encoding) as file:
                file.write(file_content)
        print("Corpus creation has finished successfully. Please check the files on the path: "+self.corpus_files_path)
        
    
    '''
    Retrieves punctuation characters from the text obtained from html pages
    '''
    def punctuation_handler(self, file_content,plain_text):
        punctuation_list_for_text = string.punctuation.replace('-', '')
        punctuation_list_for_text = punctuation_list_for_text+'”'+'“'+'’'+'‘'+'…'+'‚'
        text_pattern = r"[{}]".format(punctuation_list_for_text)
        
        regex_alpha = re.compile('[a-zA-z]+')
        regex_numbers = re.compile('[0-9]+')
        number_pattern = r'[^0-9\.\,\%]'
        plain_text = plain_text.replace('\n',' ')
        plain_text = plain_text.replace('\t',' ')
        words_list = plain_text.split(' ')
        for word in words_list:
            if(word.startswith("http")):
                final_word = word
            else:
                if(regex_alpha.search(word)):
                    if(word.find("'")!=-1):
                        word = word.replace("'",'')  
                    final_word = re.sub(text_pattern, " ", word)
                else:
                    if(regex_numbers.search(word)):
                        final_word = re.sub(number_pattern, " ", word)
                        if(('.' in final_word) or ('%' in final_word) or (',' in final_word)):
                            final_word = "".join(final_word.split())
                        if(final_word.endswith('.') or final_word.endswith(',')):
                            final_word = final_word.replace('.','')
                            final_word = final_word.replace(',','')
                        if(not(final_word.endswith('%'))):
                            final_word = final_word.replace('%','')
                        
                    else:
                        final_word=''
            text = final_word.lower().strip()
            if('—' in text):
                text = "".join(text.split('-'))
            if(text != ""):
                file_content = file_content+ text+' '      
        return file_content
    
    
    '''
    Extracts the html objects that are not relevant to the corpus
    '''
    def retrieve_body_content(self,content):
        suplist= content.findAll(re.compile("sup"))
        for sup_tag in suplist:
            sup_tag.extract()
            
        toc = content.find("div", id="toc")
        if(toc!=None):
            toc.extract()
        
        tablelist = content.findAll(re.compile('table'))
        for table_tag in tablelist:
            table_tag.extract()
            
        imglist = content.findAll(re.compile('img'))
        for img_tag in imglist:
            img_tag.extract()
            
        math_elements = content.findAll(re.compile('math'))
        for math in math_elements:
            math.extract()
        
        see_also = content.find('span', id='See_also')
        if(see_also!=None):
            h_parent= see_also.parent
            for sibling in h_parent.find_all_next():
                sibling.extract()
              
        references = content.find('span', id='References')
        if(references!=None):
            h_parent = references.parent
            
            for sibling in h_parent.find_all_next():
                sibling.extract()
                
        external_links = content.find('span', id='External_links')
        if(external_links!=None):
            h_parent=external_links.parent
            for sibling in h_parent.find_all_next():
                sibling.extract()
                
        notes = content.find('span', id='Notes')
        if(notes!=None):
            h_parent=notes.parent
            for sibling in h_parent.find_all_next():
                sibling.extract()
        
        biblography = content.find('span', id='Bibliography')
        if(biblography!=None):
            h_parent=biblography.parent
            for sibling in h_parent.find_all_next():
                sibling.extract()
        
        further_reading = content.find('span', id='Further_reading')
        if(further_reading!=None):
            h_parent=further_reading.parent
            for sibling in h_parent.find_all_next():
                sibling.extract()
                
        
                
        return content
    
    def create_stemmed_corpus_files(self):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        
        file=open(self.rel_path+self.stemmed_file,'r+', encoding= 'utf-8')
        data =  file.read()
        content_list = data.split('#')
        content_list = list(filter(None, content_list))
        for file_content in content_list:
            file_content=file_content[3:]
            f = self.createFile(self.f_id)
            self.f_id += 1
            for word in file_content:
                word = word.replace("\n", " ")
                f.write(str(word))
                    
    def createFile(self, f_id):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        f_id=str(f_id)
        m=f_id.zfill(4)
        if(not(os.path.isdir(self.rel_path+self.stemmed_corpus_location))):
            os.makedirs(self.rel_path+self.stemmed_corpus_location)
        fileHandle =open(self.rel_path+self.stemmed_corpus_location+'CACM-' + str(m), 'w+', encoding = 'utf-8')
        return fileHandle
                    
        

def main(is_stemmed_corpus):
    corpusBuilder = CorpusBuilder()
    if(not(is_stemmed_corpus)):    
        corpusBuilder.initialize_doc_keys()
        corpusBuilder.create_corpus()
    else:
        corpusBuilder.create_stemmed_corpus_files()

        
if __name__ == '__main__':
        
    main() 
