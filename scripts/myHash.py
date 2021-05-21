import math as ma
import numpy as np

class hashHelpers():

    @staticmethod
    def naive(input,range,index,):
        return (hashHelpers.primes[index]*input)%range

    @staticmethod
    def pair_independent(input,range,index):
        return ((hashHelpers.a[index]*input+hashHelpers.b[index])%hashHelpers.mod[-1])%range
        
    @staticmethod
    def strong_independent(input,range,index):
        return (hashHelpers.a[index]*input+hashHelpers.b[index])%hashHelpers.mod[-1]
    
    hashUsed=0
    hashCapacity=0
    primes=[19,23,41,47]
    a=None
    b=None
    mod=None
    leastStepSize=10
    hashFunc=None
    hashTypes=[]

    # 初始化
    def __init__(self) -> None:
        self.hashFunc=None
        self.hashTypes=[]
        self.hashTypes.append(hashHelpers.naive)
        self.hashTypes.append(hashHelpers.pair_independent)
        self.hashTypes.append(hashHelpers.strong_independent)
    
    # 检查v是否是素数的方法
    @staticmethod
    def isPrime(v):
        for index in range(2,int(ma.sqrt(v))+4):
            if(v%index==0):
                return False
        return True

    # 找到下一个素数的方法
    @staticmethod    
    def findNewPrime():
        target=hashHelpers.primes[-1]+1
        count_step=0
        while(not hashHelpers.isPrime(target) or count_step<hashHelpers.leastStepSize):
            target+=1
            count_step+=1
        hashHelpers.primes.append(target)
    
    # 初始化hash函数列表
    def initHash(self,hashType,minPrime,hashCapacity,hashUsed):


        while(len(hashHelpers.primes)<=hashCapacity or hashHelpers.primes[-1]<2*minPrime):
            self.findNewPrime()
            self.hashUsed=hashUsed


        hashHelpers.a=hashHelpers.primes.copy()
        np.random.shuffle(hashHelpers.a)
        hashHelpers.b=hashHelpers.primes.copy()
        np.random.shuffle(hashHelpers.b)


        # 准备一个求模的base的数组
        st=len(hashHelpers.primes)
        for i in range(0,hashUsed+5):
            hashHelpers.findNewPrime()
        hashHelpers.mod=hashHelpers.primes[st:]
        self.hashFunc=self.hashTypes[hashType]

    # 得到hash值域的方法
    def getRange(self,range):
        if(self.hashFunc==self.strong_independent):
            return self.mod[-1]
        else:
            return range
    
    # 查找对应于hashIndex的hashValue的方法
    def hashValue(self,input,range,hashIndex):
        return self.hashFunc(input,range,hashIndex)

