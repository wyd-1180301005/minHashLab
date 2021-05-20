from scripts.myHash import hashHelpers
from scripts.myLSH import LSH
from scripts.probHelpers import probFalseNegative,probFalsePositive, probFalsePositiveAmp,probFalseNegativeAmp

class naiveAmpLSH(LSH):

    distri=None
    rate=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.0]
    amp= [20,  15,  10,   10,  10,  10,  10,  10,   10,   10   ,10]
    amp_num=0
    pos_num=0

    printOut=[
    "total",    # 总的可能的集对个数
    "step",     # 比较次数与naive算法的比较次数之比
    "posi",     # 真正的阳性个数
    "res",      # 算法给出的解的个数
    "FP",       # 假阳性的个数
    "FN",       # 假阴性的个数
    "prec",     # 准确率
    "recall",   # 召回率
    "miss",     # 总的错误个数
    "FPE",      # 假阳性的解的平均误差
    "FNE",      # 假阴性的解的平均误差
    "FPR",      # 将一个集对判别为假阳性的比率的真实值
    "FNR",      # 将一个集对判别为假阴性的比率的真实值
    "eFPR",     # 将一个集对判别为假阳性的比率的估计值
    "eFNR",      # 将一个集对判别为假阴性的比率的估计值
    "amp",      # 进行的概率放大次数
    "pos"       # 概率放大的标准
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
        "amp":15,
        "pos":16    
    }



    # 计算放大倍数的方法
    @staticmethod
    def getAmp(rate_in):
        for i in range(0,len(naiveAmpLSH.rate)):
            if(naiveAmpLSH.rate[i]<=rate_in):
                return naiveAmpLSH.amp[i-1]

    # 使用概率放大技术的亲近集对计算方法
    # 使用这种方法用来避免出现过高的单边错误
    def calc_pairs(self,crit,hashType,hashNumber):
        
        self.crit=crit

        fp=probFalsePositive(hashNumber,crit,self.error,self.setgroup.dis)
        fn=probFalseNegative(hashNumber,crit,self.error,self.setgroup.dis)
        
        self.amp_num=naiveAmpLSH.getAmp(max(fp,fn))
        self.pos_num=int(max(1,(fp/(fp+fn))*self.amp_num))

        self.hashNum=hashNumber
        self.hashFuncs.initHash(hashType,self.setgroup.num,10*self.amp_num*hashNumber,self.amp_num*hashNumber)
        self.setgroup.setHash(self.hashFuncs)

        self.minHashes=[]
        self.result_pairs=set()
        
        self.step_taken=0

        for i in range(0,self.setgroup.size):
            minhash=self.setgroup.minHash(i,self.amp_num*hashNumber)
            self.minHashes.append(minhash)
        for i in range(0,self.setgroup.size):
            for j in range(i+1,self.setgroup.size):
                count_posi=0
                st=0
                for k in range(0,self.amp_num):
                    self.step_taken+=1
                    jaccard=self.setgroup.minHashJaccard(self.minHashes[i][st:st+hashNumber],self.minHashes[j][st:st+hashNumber])
                    st+=hashNumber
                    if(jaccard>crit):
                        count_posi+=1
                if(count_posi>=self.pos_num):
                    self.result_pairs.add((j,i))

    # 生成评价的方法
    def evaluate(self):
        l0=super().evaluate()
        l0[naiveAmpLSH.print_pos["eFPR"]]=probFalsePositiveAmp(self.hashNum,self.crit,self.error,self.setgroup.dis,self.amp_num,self.pos_num)
        l0[naiveAmpLSH.print_pos["eFNR"]]=probFalseNegativeAmp(self.hashNum,self.crit,self.error,self.setgroup.dis,self.amp_num,self.pos_num)
        l0.append(self.amp_num)
        l0.append(self.pos_num)
        return l0

    # 打印评价的方法
    def printEval(self,evalist,prec,choice,title=None):
        if(title==None):
            super().printEval(evalist,prec,choice,naiveAmpLSH.printOut)
        else:
            super().printEval(evalist,prec,choice,title)

