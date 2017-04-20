 # -*- coding: UTF-8 -*-

#=================读文件================#
 
####从文件中读入1维list（utf8格式）####
#输入：文件名（string）
#输出：1维list
def readFormFile1DList(fromFileName):	
	file = open(fromFileName,'r')
	lines = file.readlines()
	resultList = []
	for line in lines:
		resultList.append(line.strip())
	return resultList
    
####从文件中读入2维list（utf8格式）####
#输入：文件名（string）
#输出：2维list
def readFormFile1DList(fromFileName):	
    file = open(fromFileName,'r')
    lines = file.readlines()
    resultList = []
    for line in lines:
        rowList = line.strip().split(' ')
        resultList.append(rowList)
    return resultList
    
#=====================================#   
    
    
#=================写文件================#   
    
####将1维list输出到文件（utf8格式）####
#输入：文件名（string）， 1维list（list）
#输出：无
def output2File1DList(toFileName,list1D):
	f =  open(toFileName,'w')
	WriteText = []
	for everyone in list1D:
		WriteText.append((str(everyone).encode('utf-8')))
		WriteText.append('\n')
	f.writelines(WriteText)
	f.close()
    
    
####将2维list输出到文件（utf8格式）####
#输入：文件名（string），2维list （list）
#输出：无    
def output2File2DList(toFileName,list2D):	
	f =  open(toFileName,'w')
	WriteText = []
	for everyrow in list2D:
		for everycolumn in everyrow:
			WriteText.append((str(everycolumn).encode('utf-8')+' '))
		WriteText.append('\n')
	f.writelines(WriteText)
	f.close()
    
#=====================================#       
    
    
    
if __name__ == '__main__':
    #测试代码
    pass