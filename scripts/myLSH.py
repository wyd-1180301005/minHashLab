import math as ma

from scripts.myHash import hashHelpers
from scripts.probHelpers import probFalseNegative,probFalsePositive

class LSH():

    hashNum=0
    hashFuncs=None
    setgroup=None
    minHashes=[]
    result_pairs=set()

    error=0.0
    crit=0
    step_taken=0

    false_posi=0
    false_nega=0
    true_posi=0
    true_nega=0
    correctness=0
    recall=0


    # 初始化
    def __init__(self,setgroup,error=0.001) -> None:
        self.setgroup=setgroup
        self.hashFuncs=hashHelpers()
        self.error=error

    # 生成评价的方法
    def evaluate(self):

        self.false_posi=0
        self.false_nega=0
        self.true_posi=0
        self.true_nega=0
        self.correctness=0
        self.recall=0

        count_all=0
        errorfn=0.0
        errorfp=0.0

        for i in range(0,self.setgroup.size):
            for j in range(i+1,self.setgroup.size):
                naive=self.setgroup.jaccards[i][j]
                if(naive>=self.crit or self.crit-naive<=self.error):
                    count_all+=1
                    if(not (j,i) in self.result_pairs):
                        self.false_nega+=1
                        errorfn+=ma.fabs(naive-self.setgroup.minHashJaccard(self.minHashes[i],self.minHashes[j]))
                else:
                    if((j,i) in self.result_pairs):
                        self.false_posi+=1
                        errorfp+=ma.fabs(naive-self.setgroup.minHashJaccard(self.minHashes[i],self.minHashes[j]))

        all=int((self.setgroup.size*(self.setgroup.size-1))/2)
        self.true_posi=count_all-self.false_nega
        self.true_nega=all-count_all-self.false_posi
        self.correctness= self.true_posi/max(1,count_all)
        self.recall=(len(self.result_pairs)-self.false_posi)/max(1,len(self.result_pairs))

        return [
            all,
            float(self.step_taken/all),
            count_all,
            len(self.result_pairs),
            self.false_posi,
            self.false_nega,
            self.correctness,
            self.recall,
            self.false_posi+self.false_nega,
            float(errorfp/max(self.false_posi,1)),
            float(errorfn/max(self.false_nega,1)),
            float(self.false_posi/all),
            float(self.false_nega/all),
            float(probFalsePositive(self.hashNum,self.crit,self.error,self.setgroup.dis)),
            float(probFalseNegative(self.hashNum,self.crit,self.error,self.setgroup.dis)),
            self.hashNum
            ]
    
    # 打印评价的方法
    def printEval(self,evalist,prec,choice,title):

        prec_float="%."+str(prec)+"f"

        print("#",end='\t')
        for i in range(0,len(title)):
            if(not i in choice):
                print(title[i],end='\t')

        print()

        for i in range(0,len(evalist)):
            print('#'+str(i+1),end='\t')
            for j in range(0,len(evalist[i])):
                if(j in choice):
                    continue
                if(LSH.isFloat(evalist[i][j]) or str(type(evalist[i][j])).__contains__("float")):    
                    print(prec_float%evalist[i][j],end='\t')
                else:
                    print("%d"%evalist[i][j],end='\t')
            print()

    # 判断一个数字是否是浮点数的方法
    @staticmethod
    def isFloat(v):
        if(v==int(v)):
            return False
        else:
            return True


