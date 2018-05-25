'''
@author: Meesam Syed
The relevance class contains various relevance methods
evaluatePrecision()    :  calculates precision for every result
evaluateRecall()       :  calculates precision for every result
evaluateAP()           :  calculates average precision for each query
evaluateMAP()          :  calculates mean average precision for all queries
evaluateRR()           :  calculates reciprocal rank for each query
evaluateMRR()          :  calculate mean reciprocal rank across queries
evaluatePat5andPat20() :  calculates precision at rank 5 and rank 20 for each query
'''
import os


class Relevance():
    def __init__(self, result, relevance):
        self.result_file = os.getcwd() + '\\' + result
        self.relevance_file = os.getcwd() + '\\' + relevance
        self.relevance = []
        self.new_relevance = []
        resultn = result[:-4]
        self.evaluation_folder = os.getcwd() + '\\EvaluationResults' + '_' + resultn

    def loadrelevance(self):
        print('Loading relevance...')
        with open(self.relevance_file, 'r', encoding='utf-8') as file:
            previous = '0'
            list = []
            for line in file:
                splitted = line.split(' ')
                list =[]
                list.append(splitted[0])
                list.append(splitted[2])
                self.relevance.append(list)
        list = []
        previous = '0'
        for items in self.relevance:
            if items[0] == previous:
                list.append(items[1])
                previous = items[0]
            else:
                previous = items[0]
                self.new_relevance.append(list)
                list = []
                list.append(items[0])
                list.append(items[1])
        self.new_relevance.append(list)
        self.new_relevance.pop(0)
        if not os.path.exists(self.evaluation_folder):
            os.makedirs(self.evaluation_folder)
        print('Loading relevance done :)')





    def evaluatePrecision(self):
        print('Evaluating precision...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevancePrecision.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        with open(self.result_file, 'r', encoding='utf-8') as file:
            previous = '0'
            linenumber = 1
            relevant_count = 0
            i = 0
            for line in file:
                if line[0].isdigit():

                    splitted = line.split(' ')
                    query_id = splitted[0]
                    index = int(query_id) - 1
                    doc = splitted[2]
                    f = 0
                    for lists in self.new_relevance:
                        if lists[0] == query_id:
                            mylist = lists
                            f = 1
                            break
                    if f == 0:
                        continue

                    if previous != query_id:
                        linenumber = 1
                        relevant_count = 0
                    flag = 0
                    for items in mylist:
                        if doc == items:
                            flag  = 1
                            break
                    if flag == 1:
                        relevant_count = relevant_count + 1
                        outputLine = query_id + " " + doc + " R " + str(relevant_count/linenumber) + '\n'
                    elif flag == 0:
                        outputLine = query_id + " " + doc + " NR " + str(relevant_count/linenumber) + "\n"



                    linenumber = linenumber + 1
                    previous = query_id
                    fileresult = result[:-4]
                    relevance_filePrecision = self.evaluation_folder + '\\' + fileresult + '-relevancePrecision.txt'
                    with open(relevance_filePrecision, 'a', encoding='utf-8') as o:
                        o.write(outputLine)
        print('Evaluating precision done :)')

    def evaluateRecall(self):
        print('Evaluating Recall...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceRecall.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')

        mylist = []
        outputline = ''
        relevant_docs = 0
        previous = '0'
        with open(self.result_file, 'r' , encoding='utf-8') as file:
            for line in file:
                if line[0].isdigit():
                    splitted = line.split(' ')
                    query_id = splitted[0]
                    doc = splitted[2]

                    if previous!= query_id:
                        relevant_docs = 0

                    for items in self.new_relevance:
                        if items[0] == query_id:
                            mylist = items
                            break
                    total_relevant_docs = len(mylist) - 1
                    flag = 0
                    for item in mylist:
                        if doc == item:
                            relevant_docs = relevant_docs + 1
                            flag = 1
                            break
                    if flag == 1:
                        outputline = query_id + " " + doc + " R " + str(relevant_docs/total_relevant_docs) + "\n"
                    else:
                        outputline = query_id + " " + doc + " NR " + str(relevant_docs/total_relevant_docs) + "\n"
                    fileresult = result[:-4]
                    relevanceRecall = self.evaluation_folder + '\\' + fileresult + '-relevanceRecall.txt'
                    previous = query_id

                    with open(relevanceRecall, 'a' , encoding='utf-8') as output:
                        output.write(outputline)
        print('Evaluating Recall done :)')

    def evaluateRR(self):
        print('Evaluating Reciprcal Rank...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceRR.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        with open(self.result_file, 'r', encoding='utf-8') as file:
            previous = '0'
            mylist = []
            linenumber = 1
            flag  = 0
            for line in file:
                if line[0].isdigit():
                    splitted = line.split(' ')
                    query_id = splitted[0]
                    doc = splitted[2]

                    for items in self.new_relevance:
                        if items[0] == query_id:
                            mylist = items

                    if query_id !=previous:
                        linenumber = 1
                        flag = 0
                    if flag == 1:
                        continue
                    for item in mylist:
                        if item == doc:
                            flag = 1
                            outputline = query_id + " " + str(1/linenumber) + "\n"
                            fileresult = result[:-4]
                            outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceRR.txt'
                            with open(outputfile, 'a', encoding='utf-8') as output:
                                output.write(outputline)

                    previous = query_id
                    linenumber = linenumber + 1
        print('Evaluating Reciprocal Rank done :)')



    def evaluateAP(self):
        print('Evaluating Average precision...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceAP.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        fileresult = result[:-4]
        resultfile = self.evaluation_folder + '\\' + fileresult + '-relevancePrecision.txt'
        with open(resultfile, 'r' ,encoding='utf-8') as file:
            p = 0
            previous = '0'
            linenumber = 1
            i = 0
            ap = 0
            mylist = []
            for line in file:
                if line[0].isdigit():
                    splitted = line.split(' ')
                    queryid = splitted[0]
                    RorNR = splitted[2]
                    precision = splitted[3]
                    if previous != queryid:
                        ap = float(p/linenumber)
                        if previous != '0':
                            outputline = previous + " AP " + str(ap) + "\n"
                            fileresult = result[:-4]
                            outputfile = self.evaluation_folder + "\\" + fileresult + "-relevanceAP.txt"
                            with open(outputfile, 'a', encoding='utf-8') as output:
                                output.write(outputline)
                        p = 0
                        linenumber = 1

                    if RorNR == 'R':
                        p = p + float(precision)
                        linenumber = linenumber + 1
                    previous=queryid
            ap = float(p / linenumber)
            outputline = previous + " AP " + str(ap) + "\n"
            fileresult = result[:-4]
            outputfile = self.evaluation_folder + "\\" + fileresult + "-relevanceAP.txt"
            with open(outputfile, 'a', encoding='utf-8') as output:
                output.write(outputline)

        print('Evaluating Average Precision done :)')


    def evaluateMAP(self):

        print('Evaluating Mean Average precision...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceMAP.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')

        fileresult = result[:-4]
        resultfile = self.evaluation_folder + "\\" + fileresult + "-relevanceAP.txt"
        linenumber = 1
        ap = 0
        with open(resultfile, 'r', encoding='utf-8') as file:
            for line in file:
                splitted = line.split(' ')
                p = float(splitted[2])
                ap = ap + p
                linenumber += 1
            map = ap/linenumber
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + "\\" + fileresult + "-relevanceMAP.txt"
        with open(outputfile, 'w',encoding='utf-8') as o:
            o.write('')
        with open(outputfile, 'a' , encoding='utf-8')as o:
            line = 'The Mean Average Precision of ' + fileresult + ' is ' + str(map) + '\n'
            o.write(line)
        print('Evaluating Mean Average Precision done :)')

    def evaluateMRR(self):
        print('Evaluating MRR...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevanceMRR.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        resultfile = self.evaluation_folder + '\\' + fileresult + '-relevanceRR.txt'
        arr = 0
        linenumber = 0
        with open(resultfile, 'r', encoding='utf-8') as file:
            for line in file:
                splitted = line.split(' ')
                arr = arr + float(splitted[1])
                linenumber += 1
        mrr = float(arr/linenumber)
        with open(outputfile, 'a', encoding='utf-8') as o:
            line = 'The Mean Reciprocal Rank for ' + fileresult + ' is ' + str(mrr) + '\n'
            o.write(line)
        print('Evaluating MRR done :)')




    def evaluatePat5andPat20(self):
        print('Evaluating precision at rank 5 and 20...')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relevancePat5andPat20.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        fileresult = result[:-4]
        outputfile = self.evaluation_folder + '\\' + fileresult + '-relelvancePat5andPat20.txt'
        with open(outputfile, 'w', encoding='utf-8') as o:
            o.write('')
        result_file = self.evaluation_folder + "\\" + fileresult + "-relevancePrecision.txt"
        linenumber = 1
        with open(result_file, 'r', encoding='utf-8') as file:
            previous = '1'
            for line in file:
                splitted = line.split(' ')

                if previous!=splitted[0]:
                    linenumber = 1

                if linenumber == 5:
                    precision = float(splitted[3])
                    outputfile = self.evaluation_folder + '\\' + fileresult + '-relelvancePat5andPat20.txt'
                    query_id = splitted[0]
                    rank = linenumber
                    RorNR = splitted[2]
                    doc = splitted[1]
                    with open(outputfile, 'a+', encoding='utf-8') as out:
                        line = str(query_id) + ' ' + str(doc) + ' ' + str(rank) + ' ' + str(RorNR) + ' ' + str(precision) + '\n'
                        out.write(line)



                if linenumber == 20:
                    precision = float(splitted[3])
                    outputfile = self.evaluation_folder + '\\' + fileresult + '-relelvancePat5andPat20.txt'
                    query_id = splitted[0]
                    rank = linenumber
                    RorNR = splitted[2]
                    doc = splitted[1]
                    with open(outputfile, 'a+', encoding='utf-8') as out:
                        line = str(query_id) + ' ' + str(doc) + ' ' + str(rank) + ' ' + str(RorNR) + ' ' + str(precision) + '\n'
                        out.write(line)

                previous = splitted[0]
                linenumber += 1
        print('Done evaluating...')


result = input('Enter result file...')
result += '.txt'
relevance = input('Enter relevance file...')
relevance += '.txt'
print(relevance)
rl = Relevance(result,relevance)

rl.loadrelevance()
rl.evaluatePrecision()
rl.evaluateRecall()
rl.evaluateRR()
rl.evaluateAP()
rl.evaluateMAP()
rl.evaluateMRR()
rl.evaluatePat5andPat20()