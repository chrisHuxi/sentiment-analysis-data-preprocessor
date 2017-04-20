# -*- coding: UTF-8 -*-

#===========================加载要用到的各类模块=========================#
#引入文件读写模块
import text_read_wirte as Textrw
reload(Textrw)

#引入个性化处理文本模块
import personalize.corpus_pre_process as Cprepro
reload(Cprepro)

#引入个性化处理标签模块
import personalize.label_read as Labelr
reload(Labelr)

#引入加载个性化词向量模块
import personalize.load_embedding as Loadwv
reload(Loadwv)

#加载shffle用的random模块
import random
#存储array时用的numpy模块
import numpy
#获取当前脚本目录时使用
import os  

#=================================================================#



####用来对数据进行预处理的类####
class DataPreparer:
    #======================基本属性定义区=========================#
    #1.需要处理的文件名称
    rawDataFileName = ''#路径+文件名 语料文件
    rawLabelFileName = ''#路径+文件名 标签文件
    goalDataFileName = ''#路径+文件名 处理后的data放入的文件
    goalLabelFileName = ''#路径+文件名 处理后的labels放入的文件
    embeddingsFileName = ''#路径+文件名 词向量文件
    vocabularyFileName = '' #路径+文件名 词典文件
    #======================基本属性定义区=========================#
    
    
    #初始化函数定义
    def __init__(self,rawFileName,rawLabelFileName,goalDataFileName ,goalLabelFileName ,embeddingsFileName):
        self.rawDataFileName = rawDataFileName
        self.rawLabelFileName = rawLabelFileName
        self.goalDataFileName = goalDataFileName
        self.goalLabelFileName = goalLabelFileName
        self.embeddingsFileName = embeddingsFileName
        self.vocabularyFileName = vocabularyFileName
    
        
    #======================成员函数定义区.start======================#
    ####读入文件，进行文本清理####
    #输入：self->原始语料的文件名
    #输出：原始语料的清理结果
    def SeparateWord(self):
        if rawDataFileName == '':
            print "file name is empty!"
            return
        else:
            separateWordResult = Cprepro.preprocess(self.rawDataFileName)
            return separateWordResult   #1d list


    ####读入label文件####
    #输入：self->原始label的文件名
    #输出：labellist
    def readLabels(self):
        #pass
        return Labelr.readLabel(self.rawLabelFileName)
            
    ####加载训练好的词向量####
    #输入：无
    #输出：词向量model，通过model['good']访问            
    def LoadWordVector(self):
        wordVecModel = Loadwv.loadEmbedding()
        return wordVecModel
    
    ####将分词结果列表与词向量列表中的词作比较####
    #输入：分词结果列表（list），词向量模型（W2Vmodel）
    #输出：比较后结果列表（list）
    def IntersectSepResult_Embedding(self,sepResultList,model):
        print "IntersectSepResult_Embedding start!"
        intersectedResult = []
        wordSet = set(model.keys())
        for sentence in sepResultList:
            intersectedSentence = []
            for word in sentence:
                #if word in model.keys():   #这里不能用这个，效率太低
                if word in wordSet:            #这速度！牛逼！
                    intersectedSentence.append(word)
            intersectedResult.append(intersectedSentence)
        print "IntersectSepResult_Embedding over!"
        return intersectedResult    #2d word list
        
        
    ####建立词典####
    #输入：（相交后）分词后的结果二维list(list) 
    #输出：可以由索引读出词的字典(dict)，可以由词读出索引的字典(dict)
    def BulidDictionary(self,resultList):
        wholeWord = []
        for sentence in resultList:
            wholeWord.extend(sentence)        
        wordSet = set(wholeWord)
        word2IdDict = dict()
        id2WordDict = dict()
        i = 0
        for everyWord in wordSet:
            word2IdDict[everyWord] = i
            id2WordDict[i] = everyWord
            i = i + 1
        return id2WordDict,word2IdDict
        
        
    ####建立词向量词典embeddings####
    #输入：id2WordDict,word2IdDict,model
    #输出：词向量词典embeddings（按照词在词典中的顺序进行存放,np.array类型）
    #         词典vocabulary(一维lsit)
    def buildEmbeddings(self,id2WordDict,word2IdDict,wordVecModel):
        embeddings = []
        vocabulary = []
        for i in range(0,len(id2WordDict)):
            embeddings.append(wordVecModel[id2WordDict[i]])
            vocabulary.append(id2WordDict[i])
        embeddings = numpy.array(embeddings)
        return embeddings,vocabulary
        
     
    ####将句子表示为index的格式#### 例：125 302 52 0 127 。。。。。
    #输入：读入的句子（二维list），将单词转化为index的字典（dict）
    #输入：句子的词用index表示（二维list）
    def Sentence2Index(self,resultList,word2IdDict):
        idList = []
        for sentence in resultList:
            sentenceList_T = []
            for word in sentence:
                sentenceList_T.append(word2IdDict[word])
            idList.append(sentenceList_T)
        return idList
        
    ####将数据随机打乱####
    #输入：dataList（2维），labelList（1维）
    #输出：打乱顺序后的datalist（2维），以及按照同样顺序排列的labelist（1维）
    def ShuffleAllData(self,dataList,labelList):
        #pass
        indexList = range(0,len(dataList))
        random.shuffle(indexList)
        shuffledIndexList = indexList
        shuffledData = []
        shuffledLabel = []
        for i in range(0,len(dataList)):
            shuffledData.append(dataList[shuffledIndexList[i]])
            shuffledLabel.append(labelList[shuffledIndexList[i]])
        #print len(shuffledData)
        #print len(shuffledLabel)
        assert len(shuffledData) == len(shuffledLabel)    
        return shuffledData,shuffledLabel

    #======================成员函数定义区.end======================#
    
    
    ####主运行程序####
    #输入：self->rawDataFileName
    #输出：
    def Run(self):
        separateWordResult = self.SeparateWord()#分词结果
        labels = self.readLabels()#读入标签
        wordVecModel = self.LoadWordVector()#词向量模型
        intersectedResult = self.IntersectSepResult_Embedding(sepResultList = separateWordResult,model = wordVecModel)#与词向量词典相交后的分词结果
        id2WordDict,word2IdDict = self.BulidDictionary(resultList = intersectedResult)#以相交后的分词结果建立需要的词典
        embeddings,vocabulary = self.buildEmbeddings(id2WordDict = id2WordDict,word2IdDict = id2WordDict,wordVecModel = wordVecModel)#建立词向量词典embeddings
        wordIdSentences = self.Sentence2Index(resultList = intersectedResult,word2IdDict = word2IdDict)#将句子表达成一个词索引的形式
        shuffledData,shuffledLabel = self.ShuffleAllData(dataList = wordIdSentences,labelList = labels)#将数据进行shuffle
        
        Textrw.output2File1DList(toFileName = self.vocabularyFileName,list1D = vocabulary)#vocabulary输出到txt文件
        
        Textrw.output2File2DList(toFileName = self.goalDataFileName,list2D = shuffledData)#shuffledData输出到txt文件
        Textrw.output2File1DList(toFileName = self.goalLabelFileName,list1D = shuffledLabel)#shuffledLabel输出到txt文件
        
        numpy.save(self.embeddingsFileName,embeddings)#embedding以array的形式保存
        
        
        
if __name__ == '__main__':
    #测试代码
    
    '''
    例：
    rawDataFileName = ''#路径+文件名 语料文件
    rawLabelFileName = ''#路径+文件名 标签文件
    vocabularyFileName = ''#路径+文件名 词典文件
    goalDataFileName = ''#路径+文件名 处理后的data放入的文件
    goalLabelFileName = ''#路径+文件名 处理后的labels放入的文件
    embeddingsFileName = ''#路径+文件名 词向量文件
    lstmDataPerparer = DataPreparer(rawFileName,rawLabelFileName,goalDataFileName ,goalLabelFileName ,embeddingsFileName)
    lstmDataPerparer.Run()
    '''
    rawDataFileName = r'twitter-2016train-A.txt'#路径+文件名 语料文件
    rawLabelFileName = r'twitter-2016train-A.txt'#路径+文件名 标签文件
    
    curDir = os.getcwd() #获取当前目录
    vocabularyFileName = curDir + r'\\result\\vocabulay.txt'#路径+文件名 放入词典的文件
    goalDataFileName = curDir + r'\\result\\goal_data.txt'#路径+文件名 处理后的data放入的文件
    goalLabelFileName = curDir + r'\\result\\goal_label.txt'#路径+文件名 处理后的labels放入的文件
    embeddingsFileName = curDir + r'\\result\\vocabularyEmbedding'#路径+文件名 和词典对应的词向量文件
    DataPerparer = DataPreparer(rawDataFileName,rawLabelFileName,goalDataFileName ,goalLabelFileName ,embeddingsFileName)
    DataPerparer.Run()