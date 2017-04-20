# -*- coding: UTF-8 -*-
#===========================加载要用到的各类模块=========================#
import sys
sys.path.append("..")


#=============根据不同label标签进行预处理=============#
'''     可定制      '''

####从文件中读入01label####
#输入：文件名
#输出：labelList
def readLabel(fileName):
    #return Textrw.readFormFile1DList(fileName)
    cleared_label_list = []
    with open(fileName, 'r') as f:
        for line in f:
            label = line.split('	')[1]
            if label == 'negative':
                cleared_label_list.append(-1)
            elif label == 'neutral':
                cleared_label_list.append(0)
            elif label == 'positive':
                cleared_label_list.append(1)
            else:
                print "there are unexcepted label:" + label
                return -1
        return cleared_label_list
#=============根据不同label标签进行预处理=============#
        
        
        
if __name__ == '__main__':
    #测试代码
    labelList = readLabel(r'twitter-2016train-A.txt')
    print labelList.count(-1)
    print labelList.count(0)
    print labelList.count(1)
    print labelList
    #测试通过
    #pass