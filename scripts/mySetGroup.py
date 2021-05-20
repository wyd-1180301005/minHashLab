import array as ar
import numpy as np

    
class setGroup():
    complete={}
    arr_temp=ar.array('b',())
    mat=[]

    num=0
    size=0
    dis=None

    hashFuncs=None
    jaccards=None

    # 初始化
    def __init__(self) -> None:
        self.complete={}
        self.arr_temp=ar.array('b',())
        self.mat=[]
        self.num=0
        self.size=0
        self.hashFuncs=None
        self.jaccards=None

    # 向集族中添加数据元素的方法
    def add_item(self,item,sizeIndex):
        # 如果不在全集内部
        if(not item in self.complete):
            self.complete[item]=self.num
            self.num+=1
            self.arr_temp.append(0)
            for index in range(0,self.size):
                self.mat[index].append(0)
        # 补全size
        if(sizeIndex>=self.size):
            for i in range(0,sizeIndex-self.size+1):
                self.mat.append(ar.array('b',self.arr_temp))
            self.size=sizeIndex+1
        # 设置标志位
        self.mat[sizeIndex][self.complete.get(item)]=1
        
    # 向集族中添加集合的方法
    def add(self,itemList):
        self.mat.append(ar.array('b',self.arr_temp))

        for item in itemList:
            # 如果已经在全集内部
            if(item in self.complete):
                position=self.complete.get(item)
                self.mat[self.size][position]=1
            # 不在全集内部
            else:
                self.complete[item]=self.num
                self.num+=1

                self.arr_temp.append(0)
                self.mat[self.size].append(1)
                for index in range(0,self.size):
                    self.mat[index].append(0)
        
        self.size+=1

    # 打印集族矩阵表示的方法
    def showMat(self):
        for i in range(0,self.size):
            for j in range(0,self.num):
                if(self.mat[i][j]>=1):
                    print(1,end=' ')
                else:
                    print(0,end=' ')
            print()

    # 设置hash函数族的方法
    def setHash(self,hashFuncs):
        self.hashFuncs=hashFuncs

    # 朴素的求取jaccard距离的方法
    def naive_jaccard(self,i,j):
        count_all=0
        count_eve=0
        for index in range(0,self.num):
            if(self.mat[i][index]>=1 or self.mat[j][index]>=1):
                count_all+=1
                if(self.mat[i][index]>=1 and self.mat[j][index]>=1):
                    count_eve+=1
        return count_eve/max(1,count_all)
    
    # 求得对应于sizeIndex的集合所具有的minHash数字指纹
    def minHash(self,input,hashUsed):
        mins=ar.array('l',())
        for h in range(0,hashUsed):
            mins.append(2147483647)
            for n in range(0,self.num):
                if(self.mat[input][n]>=1):
                    hashVal=self.hashFuncs.hashValue(n,self.num,h)
                    if(mins[h]>hashVal):
                        mins[h]=hashVal
        return mins

    # 求出通过minHash计算而得到的jaccard距离的估计
    def minHashJaccard(self,mins1,mins2):
        length=len(mins1)
        count_eval=0
        for index in range(0,length):
            if(mins1[index]==mins2[index]):
                count_eval+=1
        return count_eval/length

    # 求出集族的jaccard距离的分布
    def jaccardDistri(self,intervals):
        sum=0.0
        self.jaccards=np.ndarray((self.size,self.size),dtype=float)
        count_all=int(((self.size-1)*self.size)/2)
        ints_list=np.zeros((intervals,),dtype=float)
        ret_list=np.zeros((intervals,),dtype=float)
        for i in range(0,intervals):
            ints_list[i]+=(i+1)*(1.0/intervals)

        for i in range(0,self.size):
            for j in range(i+1,self.size):
                naive=self.naive_jaccard(i,j)
                self.jaccards[i][j]=naive
                self.jaccards[j][i]=naive
                sum+=naive
                for k in range(0,intervals):
                    if(naive<ints_list[k]):
                        break
                ret_list[k]+=1
        for i in range(0,intervals):
            ret_list[i]/=count_all

        self.dis=ret_list
        return ret_list

class distriHelper():
    @staticmethod
    def print_distri(distri,prec):
        intervals=len(distri)
        prec1="%."+str((intervals%10)+2)+"f"
        prec2="%."+str(prec)+"f"
        start=0.0
        ending=1.0/intervals
        for i in range(0,intervals):
            print('['+prec1%start,end=',')
            print(prec1%ending+"]",end=": ")
            print(prec2%distri[i])
            start+=1.0/intervals
            ending+=1.0/intervals
