from scripts.myHash import hashHelpers
from scripts.myLSH import LSH
class naiveLSH(LSH):

    printOut=[
    "total ",    # 总的可能的集对个数
    "step  ",     # 比较次数与naive算法的比较次数之比
    "posi  ",     # 真正的阳性个数
    "res   ",      # 算法给出的解的个数
    "FP    ",       # 假阳性的个数
    "FN    ",       # 假阴性的个数
    "prec  ",     # 准确率
    "recall",   # 召回率
    "miss  ",     # 总的错误个数
    "FPE   ",      # 假阳性的解的平均误差
    "FNE   ",      # 假阴性的解的平均误差
    "FPR   ",      # 将一个集对判别为假阳性的比率的真实值
    "FNR   ",      # 将一个集对判别为假阴性的比率的真实值
    "eFPR  ",     # 将一个集对判别为假阳性的比率的估计值
    "eFNR  ",     # 将一个集对判别为假阴性的比率的估计值
    "hash  "      # 使用的hash函数的个数
    ]
    # 注: 所谓的误差是指:使用minhash计算出的jaccard值相对于真实jaccard值之间的误差

    print_pos={
        "total":0,
        "step":1,    
        "posi":2,    
        "res":3,      
        "FP":4,     
        "FN":5,     
        "prec":6,
        "recall":7,
        "miss":8,   
        "FPE":9,     
        "FNE":10,      
        "FPR":11,    
        "FNR":12,    
        "eFPR":13,   
        "eFNR":14,
        "hash":15    
    }

    
    # 计算亲近集对的方法
    def calc_pairs(self,crit,hashType,hashNumber):
        
        self.crit=crit

        self.hashNum=hashNumber
        self.hashFuncs.initHash(hashType,self.setgroup.num,10*hashNumber,hashNumber)
        self.setgroup.setHash(self.hashFuncs)

        self.minHashes=[]
        self.result_pairs=set()
        
        self.step_taken=0

        for i in range(0,self.setgroup.size):
            minhash=self.setgroup.minHash(i,hashNumber)
            self.minHashes.append(minhash)
        for i in range(0,self.setgroup.size):
            for j in range(i+1,self.setgroup.size):
                self.step_taken+=1
                jaccard=self.setgroup.minHashJaccard(self.minHashes[i],self.minHashes[j])
                if(jaccard>crit):
                    self.result_pairs.add((j,i))

    # 打印评价的方法
    def printEval(self,evalist,prec,choice,title=None):
        if(title==None):
            super().printEval(evalist,prec,choice,self.printOut)
        else:
            super().printEval(evalist,prec,choice,title)

