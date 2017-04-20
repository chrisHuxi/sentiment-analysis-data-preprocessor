# -*- coding: UTF-8 -*-
#===========================加载要用到的各类模块=========================#
#加载正则表达式模块，为了清除文本中的无关成分
import re

#加载文本处理模块，为了分词用
import nltk

#加载停用词模块，为了去停用词用
from nltk.corpus import stopwords

#加载字符串模块，为了使用字符串中的符号：'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
import string
#=============根据不同语料进行预处理=============#
'''     可定制      '''


#def separateWordFromFile(fileName):

####读入文件进行清洗####
#输入：文件名（绝对路径）（string）
#输出：清洗结果 （list）：去除了各种符号
def clearText(fileName):
    cleared_text_list = []
    with open(fileName, 'r') as f:
        for line in f:
            tweet = line.split('	')[2]
            URL_pattern=re.compile(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',re.S)
            try:
                text_without_URL =URL_pattern.sub("",tweet)     #'http://example.com'
            except:
                print tweet
                return -1
            At_mentions_pattern =  re.compile(r'(?:@[\w_]+)',re.S)
            text_without_At_mentions = At_mentions_pattern.sub("",text_without_URL)   #'@marcobonzanini'
            
            hash_tags_pattern = re.compile(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",re.S)
            text_without_hash_tags = hash_tags_pattern.sub("",text_without_At_mentions)      # '#NLP'
            
            HTML_tags_pattern = re.compile(r'<[^>]+>',re.S)
            text_without_HTML_tags = HTML_tags_pattern.sub("",text_without_hash_tags)       #HTML
            
            emoticons_str_pattern = re.compile(r'(?:[:=;][oO\-]?[D\)\]\(\]/\\OpP])',re.S)
            text_without_emoticons = emoticons_str_pattern.sub("",text_without_HTML_tags)      #表情符
            
            RT_str_pattern = re.compile(r'RT :',re.S)   #RT符："RT :"
            text_without_RT = RT_str_pattern.sub("",text_without_emoticons)
            
            emoji_pattern = re.compile(ur"u[\'\"]\\[Uu]([\w\"]{9}|[\w\"]{5})",re.S);#emoji表情
            text_without_emoji = emoji_pattern.sub("",text_without_RT)
            
            reminder_text = text_without_emoji
            cleared_text_list.append(reminder_text.strip())
        return cleared_text_list
        
        
####对已经清洗过的文本列表进行分词####
#输入：清洗结果 （list）
#输出：分词结果列表（全转为小写，且将标点符号去除了）        
def separateWord(clearedTextList):
    regex_str = [
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    tokensList = []
    
    for sentence in clearedTextList:
        tokens = tokens_re.findall(sentence)
        tokens_lower = [token.lower() for token in tokens]
        tokensList.append(tokens_lower)
    return tokensList
 
####对已经清洗的分词列表进行去停用词####
#输入：分词结果 （list）
#输出：去停用词之后的结果列表（包括英文高频词以及常用符号，还加了一个via）      
def deStopWord(tokensList):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['via']
    deStopList = []
    for sentence in tokensList:
        sentence_deStop = [term for term in sentence if term not in stop]
        deStopList.append(sentence_deStop)
    return deStopList
  
 
####预处理整合####
#输入：需要预处理的文件名
#输出：经过清洗，分词，去停用词之后的按句子分好的符号列表（二维list） 
def preprocess(fileName):
    clearedTextList = clearText(fileName)#(r'D:\SCI_aim\experiment\training_set\twitter-2016train-A.txt')    #print clearedTextList[0:50]
    sepWordList = separateWord(clearedTextList)
    deStopList = deStopWord(sepWordList)
    return deStopList
    
#=============根据不同语料进行预处理=============#    
    
    
if __name__ == '__main__':
    #测试代码
    clearedTextList = clearText(r'twitter-2016train-A.txt')
    #print clearedTextList[0:50]
    sepWordList = separateWord(clearedTextList)
    #print sepWordList[0:50]
    deStopList = deStopWord(sepWordList)
    print deStopList[0:50]
    #pass
    
    
    
    