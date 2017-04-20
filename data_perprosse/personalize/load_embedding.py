# -*- coding: utf-8 -*-
#===========================加载要用到的各类模块=========================#
#加载numpy，为了使用np.array和计算欧式距离
import numpy as np

#=============加载不同词向量=============#
'''     可定制      '''
####加载word embedding函数####
#输入：无
#输出：加载好的词向量字典，可通过model['s']来访问词向量，每一个词向量为50维的ndarray
def loadEmbedding():
    model = dict()
    #function: 按行读取大文件
    try:
        file = open(r'glove.twitter.27B.50d.txt', 'r')
        for line in file:
            vec = line.strip().split(' ')
            try:
                model[vec[0]] = np.array(map(float,vec[1:]))
            except UnicodeError:
                continue
    except IOError as err:
        print('File error: ' + str(err))
    finally:
        if 'file' in locals():
            file.close()
    return model
    
####计算vec与目标vec的欧式距离，排序用####
#输入：aim_vec:目标向量，vec:被比较的向量
#输出：两个向量的欧式距离
def calcuEuclidDist(aim_vec,vec):
    return np.linalg.norm(aim_vec - vec)
    
    
if __name__ == '__main__':
    #测试代码：测试通过
    model = loadEmbedding()
    '''
    print model['create']
    print model['sound']
    print model['/']
    print model['dear']
    print model['great']
    '''
    #打印出与bad最相近的50个词，老远才有一个better...说明这个词向量还是蛮好的...
    aim_vec = model['bad']
    sortedResult = sorted(model.items(),key = lambda item : cauEDist(aim_vec,item[1]))[0:51]
    for _tuple in sortedResult:
        print _tuple[0]
    
    