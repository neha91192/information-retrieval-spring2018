'''
Used os for directory operations
Used operator for sorting dictionaries
Used math to take floor
Used re and string for punctuation handling
Used enchant to access dictionary
'''
'''
@author: Meesam Syed
This file contains methods genError() which shuffles characters in larger words(1st and last character are not shuffled) for 40% of query words
'''
import os
import operator
import math
import random
import string
import re
import enchant

class ErrorGenerator:
    def __init__(self):
        self.word_length = {}
        self.word_position = {}
        self.final_word = {}

    def shuffle(self,word):
        output = list(word[1:-1])
        random.shuffle(output)
        output.append(word[-1])
        return word[0] + "".join(output)

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

    def swap(self, s, i, j):
        lst = list(s)
        lst[i], lst[j] = lst[j], lst[i]
        return ''.join(lst)


    def error(self, query):
        self.word_length.clear()
        self.word_position.clear()
        self.final_word.clear()
        splitted = query.split(' ')
        length_of_query = len(splitted)
        output = ''
        position = 1
        for item in splitted:
            self.word_position[item] = position
            length = len(item)
            self.word_length[item] = length
            position += 1
        sorted_word_length = sorted(self.word_length.items(), key=operator.itemgetter(1), reverse=True)
        number_words_to_shuffle = math.floor(length_of_query * 0.2)
        i = 0
        while i < len(sorted_word_length):
            if i < number_words_to_shuffle:
                word = sorted_word_length[i][0]
                position = self.word_position[word]
                # new_word = self.shuffle(word)
                new_word = word
                if len(word) >= 3:
                    new_word = self.swap(word,1,2)
                if len(word) >= 5:
                    new_word = self.swap(word,3,4)
                self.final_word[new_word] = position
                pass
            else:
                word = sorted_word_length[i][0]
                position = self.word_position[word]
                self.final_word[word] = position

            i = i + 1
        sorted_final_word = sorted(self.final_word.items(), key=operator.itemgetter(1))

        k = 0
        output = ''
        while k < len(sorted_final_word):
            word = sorted_final_word[k][0]
            output += str(word) + " "
            k = k + 1
        output = output[:-1]
        return output

    def genError(self):
        ifile = os.getcwd() +'//queries.txt'
        ofile = os.getcwd() + '//error_queries.txt'
        with open(ofile, 'w', encoding='utf-8') as f:
            f.write('')
        with open(ifile, 'r', encoding='utf-8') as file:
            linenumber = 0
            for line in file:
                linenumber += 1
                output = ''
                line = str(line)
                newline = ''
                newline = self.punctuation_handler(newline,line)
                print('Original:' + str(newline))
                output = self.error(newline)
                output = output + '\n'
                print('Output ' + str(linenumber) + ":"+str(output))
                print('\n\n')
                with open(ofile, 'a', encoding='utf=8') as o:
                    o.write(output)

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

eg =ErrorGenerator()
eg.genError()
eg.correctQuery()

