# coding=gbk
import jieba
class Cutter(object):
    def __init__(self, posfile, negfile):
        self.posFile = posfile
        self.negFile = negfile

    def __readLine(self, fileName):
        lines = []
        with open(fileName,encoding='utf-8') as fileSteam:
            line = fileSteam.readline()
            while line:
                lines.append(line.strip())
                line = fileSteam.readline()
        return lines

    def getStopList(self, fileName):
        stop_words = list()
        for line in self.__readLine(fileName):
            stop_words.append(line.strip())
        return stop_words

    def __split_cell(self, fileName, stopList):
        if not stopList or not fileName:
            return
        resultList = list()
        dic = list()
        for line in self.__readLine(fileName):
            wordList = jieba.cut(line, cut_all=False)
            washedList = list()
            for word in wordList:
                if word not in stopList and word!=' ':
                    washedList.append(word)
                    dic.append(word)
            resultList.append(washedList)
        return dic, resultList

    def split(self, stopFile, testFile, trainFile, dictFile):
        stopList = self.getStopList(stopFile)
        dic_pos, result_pos = self.__split_cell(self.posFile, stopList)
        dic_neg, result_neg = self.__split_cell(self.negFile, stopList)
        # 处理词典dict
        oldDic = dic_pos+dic_neg
        dic =[]
        for i in oldDic:
            if i not in dic:
                dic.append(i)
        print(len(dic))
        listNum = [i for i in range(len(dic))]
        dic = dict(zip(dic, listNum))
        with open(dictFile, 'w',encoding='utf-8') as Stream:
            Stream.write('{')
            for key, value in dic.items():
                Stream.write("'"+key+"': "+str(value)+',')
            Stream.write('}')


        with open(trainFile, 'w',encoding='utf-8') as Stream:
            Stream.write('[')
            # 转换向量并写入
            for i in range(len(result_neg)):
                Stream.write('([')
                for j in range(len(result_neg[i])):
                    result_neg[i][j] = dic[result_neg[i][j]]
                    Stream.write(str(result_neg[i][j]))
                    if j < len(result_neg[i])-1:
                        Stream.write(', ')
                Stream.write('], 0), ')
            for i in range(len(result_pos)):
                Stream.write('([')
                for j in range(len(result_pos[i])):
                    result_pos[i][j] = dic[result_pos[i][j]]
                    Stream.write(str(result_pos[i][j]))
                    if j < len(result_pos[i]) - 1:
                        Stream.write(', ')
                if i < (len(result_pos) -1):
                    Stream.write('], 1), ')
                else:Stream.write('], 1)')
            Stream.write(']')

        with open(testFile, 'w',encoding='utf-8') as Stream:
            Stream.write('[')
            # 转换向量并写入
            for i in range(len(result_neg)):
                if i%4 !=0:
                    continue
                Stream.write('([')
                for j in range(len(result_neg[i])):
                    Stream.write(str(result_neg[i][j]))
                    if j < len(result_neg[i]) - 1:
                        Stream.write(', ')
                Stream.write('], 0), ')
            for i in range(len(result_pos)):
                if i % 4 != 0:
                    continue
                Stream.write('([')
                for j in range(len(result_pos[i])):
                    Stream.write(str(result_pos[i][j]))
                    if j < len(result_pos[i]) - 1:
                        Stream.write(', ')
                if i < (len(result_pos) - 1):
                    Stream.write('], 1), ')
                else:
                    Stream.write('], 1)')
            Stream.write(']')




if __name__ == '__main__':
    cutter = Cutter('positive.txt', 'critical.txt')
    cutter.split('stop.txt', 'test_data.txt','train_data.txt', 'word_dict.txt')
    with open('word_dict.txt','r',encoding='utf-8') as st:
        a = st.read()
    dic = eval(a)
    print(dic)