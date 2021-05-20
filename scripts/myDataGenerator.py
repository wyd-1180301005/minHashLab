import numpy as np

class setGenerator():

    # 生成集族的方法
    def naiveGenerate(self,setGroup,numberOfSets,numberOfItems):
        setGroup.num=numberOfItems
        setGroup.size=numberOfSets
        
        for i in range(0,numberOfSets):
            setGroup.mat.append(np.random.randint(0,2,numberOfItems))
    
    # 生成集族的方法
    def refinedGenerate(self,setGroup,proportion,numberOfItems,possibility):
        setGroup.num=numberOfItems
        setGroup.size=np.sum(proportion)
        pos=min(int(possibility),99)
        
        for i in range(0,proportion[1]):
            setGroup.mat.append(np.random.randint(0,2,numberOfItems))
        
        last=len(setGroup.mat)-1
        for i in range(0,proportion[0]):

            rnd_val=np.random.randint(1,1000)/4000.0

            rnd_proceed=np.random.randint(0,101)
            if(rnd_proceed>=pos):
                last=np.random.randint(0,len(setGroup.mat))
            setGroup.mat.append(self.setLowJaccard(setGroup.mat[last],rnd_val))

        for i in range(0,proportion[2]):

            rnd_val=np.random.randint(600,1000)/1000.0

            rnd_proceed=np.random.randint(0,101)
            if(rnd_proceed>=pos):
                last=np.random.randint(0,len(setGroup.mat))
            setGroup.mat.append(self.setHighJaccard(setGroup.mat[last],rnd_val))
    
    # 生成高相似度集合的方法
    # target 在[0.6-1.0)范围内
    def setHighJaccard(self,set,target):
        length=len(set)
        step=int(max(1,(1+target)/(1-target)-1))
        tmp=set.copy()
        for j in range(0,length,step):
            pos=np.random.randint(0,length)
            tmp[pos]=1-tmp[pos]
        return tmp

    # 生成低相似度集合的方法
    # target 在(0.0,0.25]范围内
    def setLowJaccard(self,set,target):
        length=len(set)
        i=int(max(1,(1+target)/(2*target)-1))
        tmp=1-set
        for j in range(0,length,i):
            pos=np.random.randint(0,length)
            tmp[pos]=1-tmp[pos]
        return tmp

    # 朴素的求取jaccard距离的方法
    @staticmethod
    def naive_jaccard(m,n):
        count_all=0
        count_eve=0
        num=len(m)
        for index in range(0,num):
            if(m[index]>=1 or n[index]>=1):
                count_all+=1
                if(m[index]>=1 and n[index]>=1):
                    count_eve+=1
        return count_eve/max(1,count_all)