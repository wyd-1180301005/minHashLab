import array as ar
import math as ma

from scripts.myLSH import LSH
class typicalLSH(LSH):

    hashRange=0
    bucket=None
    row=0
    col=0
    row_length=0
    col_length=0
    row_base=0

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
    "hash  ",     # 使用的hash函数的个数
    "row   ",      # LSH的每行包括的hash函数的个数
    "col   ",      # LSH列的个数
    "cost  "      # hash函数的值域
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
        "hash":15,
        "row":16,
        "col":17,
        "cost":18    
    }

    #  由minHash值找到bucket的方法
    # 比如有着8行,将行分为2组,则每组4行,又将列分为3种,那么:
    # 可以将每个minHash看作是2(组),长度为4的3进制数,从而总的bucket个数为:
    # 2*3*3*3*3=162 
    # 而每个组的index范围是0到2*27+2*9+2*3+2=80
    def getBucket(self,set_index):

        st=0
        ed=0
        index_base=0
        for i in range(0,self.row):

            ed=min(self.hashNum,st+self.row_length)
            index=0
            # 计算出列index
            for j in range(st,ed):
                index*=self.col
                index+=int(self.minHashes[set_index][j]/self.col_length)

            # 对于每个这样的桶都进行两个操作,先查看是否有minHash距离小于crit的对象,其次将本minHash记录放到桶中
            for k in self.bucket[index+index_base]:
                self.step_taken+=1
                jaccard=self.setgroup.minHashJaccard(self.minHashes[set_index],self.minHashes[k])
                if(jaccard>self.crit):
                    self.result_pairs.add((max(set_index,k),min(set_index,k)))
            self.bucket[index+index_base].append(set_index)
            index_base+=self.row_base

            st+=self.row_length

    # 计算亲近集对的方法
    def calc_pairs(self,crit,hashType,hashNumber,row,col):
        
        self.crit=crit

        self.hashNum=hashNumber
        self.hashFuncs.initHash(hashType,self.setgroup.num,10*hashNumber,hashNumber)
        self.hashRange=self.hashFuncs.getRange(hashNumber)
        self.setgroup.setHash(self.hashFuncs)

        self.minHashes=[]
        self.result_pairs=set()

        self.step_taken=0

        max_infact=0
        for i in range(0,self.setgroup.size):
            minhash=self.setgroup.minHash(i,hashNumber)
            max_infact=max(max(minhash),max_infact)
            self.minHashes.append(minhash)
        self.hashRange=min(max_infact,self.hashRange)

        self.row=int(row)
        self.col=int(col)
        self.row_length=int(hashNumber/self.row)
        self.col_length=ma.ceil(self.hashRange/col)+1

        self.bucket=[]
        self.row_base=int(ma.pow(self.col,self.row_length))
        for i in range(0,self.row_base*self.row):
            self.bucket.append(ar.array("I",()))
            self.bucket.append([])

        for i in range(0,self.setgroup.size):
            self.getBucket(i)

       

    # 生成评价的方法
    def evaluate(self):
        l0=super().evaluate()
        l0.append(self.row)
        l0.append(self.col)
        l0.append(len(self.bucket))
        return l0

    # 打印评价的方法
    def printEval(self,evalist,prec,choice,title=None):
        if(title==None):
            super().printEval(evalist,prec,choice,typicalLSH.printOut)
        else:
            super().printEval(evalist,prec,choice,title)
