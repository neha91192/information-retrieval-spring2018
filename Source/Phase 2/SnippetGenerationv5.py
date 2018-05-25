'''
Used os for directory operations
Used operator for sorting dictionaries
Used math to take floor
Used re and string for punctuation handling
'''

'''
@author: Meesam Syed
This file takes as argument the result file(for eg. Search_results_BM25Model) which contains method generateSnippets() which  
and generates snippet by scoring each sentence based on frequency of query words it contains. The sentences with higher score will be selected 
for snippet. Title of the document is also included in the snippet
'''
import os
import string
import re
import operator
class snippets:
    def __init__(self):
        pass

    def punctuation_handler(self, file_content, plain_text):
        punctuation_list_for_text = string.punctuation.replace('-', '')
        punctuation_list_for_text = punctuation_list_for_text + '”' + '“' + '’' + '‘' + '…' + '‚'
        text_pattern = r"[{}]".format(punctuation_list_for_text)

        regex_alpha = re.compile('[a-zA-z]+')
        regex_numbers = re.compile('[0-9]+')
        number_pattern = r'[^0-9\.\,\%]'
        plain_text = plain_text.replace('\n', ' ')
        plain_text = plain_text.replace('\t', ' ')
        words_list = plain_text.split(' ')
        for word in words_list:
            if (word.startswith("http")):
                final_word = word
            else:
                if (regex_alpha.search(word)):
                    if (word.find("'") != -1):
                        word = word.replace("'", '')
                    final_word = re.sub(text_pattern, " ", word)
                else:
                    if (regex_numbers.search(word)):
                        final_word = re.sub(number_pattern, " ", word)
                        if (('.' in final_word) or ('%' in final_word) or (',' in final_word)):
                            final_word = "".join(final_word.split())
                        if (final_word.endswith('.') or final_word.endswith(',')):
                            final_word = final_word.replace('.', '')
                            final_word = final_word.replace(',', '')
                        if (not (final_word.endswith('%'))):
                            final_word = final_word.replace('%', '')

                    else:
                        final_word = ''
            text = final_word.lower().strip()
            if ('—' in text):
                text = "".join(text.split('-'))
            if (text != ""):
                file_content = file_content + text + ' '
        return file_content

    def refine_query(self, query):
        common_words = os.getcwd() + '\\common_words.txt'
        common_words_list = []
        with open(common_words, 'r', encoding='utf-8') as file:
            for line in file:
                if '\n' in line:
                    line = line.replace('\n', '')
                common_words_list.append(line)
        common_words_set = set(common_words_list)

        splitted_query = query.split(' ')
        splitted_query_set = set(splitted_query)

        intersection_set = common_words_set.intersection(splitted_query_set)

        newquery = ''
        for words in splitted_query:
            if words in intersection_set:
                continue
            newquery += words + " "
        newquery = newquery[:-1]
        return newquery

    def generate_snippets(self, original_query, query, query_id, results_file, result):
        print('Generating snippets for query ' + str(query_id))
        final_snippet = '<html>'
        final_snippet +='<font style="font-family:calibri;" size="5"><p> Search results for <a href=""><i>' + original_query + '</i></a></a></p></font>'
        with open(results_file, 'r', encoding='utf-8') as file:
            i = 0
            for line in file:
                i = i + 1
                '''
                here snippets from each document for a given query is created
                '''
                if line.startswith(query_id):
                    line = line.split(' ')

                    document = line[2]

                    document_address = os.getcwd() + "\\cacm\\" + document + '.html'

                    doc_string = ''
                    with open(document_address, 'r', encoding='utf-8') as doc_file:
                        k = 1
                        title = ''
                        for doc_line in doc_file:
                            if 'html' in doc_line:
                                continue
                            if 'pre' in doc_line:
                                continue
                            if '\n' in doc_line:
                                doc_line =doc_line.replace('\n',' ')
                            if doc_line[0].isdigit():
                                continue
                            if doc_line[0] == 'C' and doc_line[1] == 'A':
                                continue
                            if k == 1:
                                if doc_line[0].isupper():
                                    title = doc_line
                                    k = 2
                            else:
                                doc_string += doc_line

                    address = '../cacm/' + document + '.html'
                    # final_snippet += '<font style="font-family:calibri;" size="4"><a href="' + '/cacm/' + document + '.html' +'">' + title + '</a></font></br>'
                    final_snippet += '<font style="font-family:calibri;" size="4"><a href="' + address +'">' + title + '</a></font></br>'
                    final_snippet += '<font style="font-family:calibri;" size="3"><b>' + document + '</b></font><br/>\n'
                    doc_string = re.sub(' +', ' ', doc_string)

                    doc_string_list = doc_string.split('.')

                    doc_line_score = {}
                    query_list = query.split(' ')
                    for item in doc_string_list:
                        count = 0
                        for query_word in query_list:
                            if query_word in item:
                                count += 1
                        doc_line_score[item] = count

                    sorted_doc_line_score = sorted(doc_line_score.items(), key=operator.itemgetter(1), reverse=True)
                    line1 = sorted_doc_line_score[0][0]
                    f = 0
                    try:
                        line2 = sorted_doc_line_score[1][0]
                    except:
                        f = 1


                    line1_snippet = '<font style="font-family:calibri;">'
                    line1_splitted = line1.split(' ')

                    for words in line1_splitted:
                        flag = 0
                        for query_word in query_list:
                            if query_word == words:
                                line1_snippet += "<b>" + words + "</b>" + " "
                                flag = 1
                                break
                        if flag == 0:
                            line1_snippet += words + " "
                    line1_snippet += '</font>'
                    line1_snippet = line1_snippet.replace(line1_snippet[0],line1_snippet[0].upper())

                    line2_snippet = '<font style="font-family:calibri;">'
                    if f == 0:

                        line2_splitted = line2.split(' ')
                        for words in line2_splitted:
                            flag = 0
                            for query_word in query_list:
                                if query_word == words:
                                    line2_snippet += "<b>" + words + "</b>" + " "
                                    flag = 1
                                    break
                            if flag == 0:
                                line2_snippet += words + " "
                    line2_snippet += '</font>'
                    line2_snippet = line2_snippet.replace(line2_snippet[0], line2_snippet[0].upper())
                    line2_snippet += '.......'

                    final_snippet += line1_snippet + ".\n" + line2_snippet + '<br/><br/>\n\n\n'

        result = result[:-4]
        addr = os.getcwd() + '\Snippets-' + result
        if not os.path.exists(addr):
            os.makedirs(addr)
        final_snippet += '</html>'
        query_id = addr + '\\' + query_id + '.html'

        with open(query_id, 'w' ,encoding='utf-8') as writer:
            writer.write(final_snippet)

snippets = snippets()
result = input('Enter the result file...')
result += '.txt'
results_file = os.getcwd() + "\\" + result
with open(results_file, 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith('Query'):
            splitted = line.split(' ', 2)
            query_id = splitted[1]
            query = splitted[2]
            intermediate_query = ''
            intermediate_query = snippets.punctuation_handler(intermediate_query,query)
            new_query = snippets.refine_query(intermediate_query)
            snippets.generate_snippets(query, new_query,query_id,results_file,result)