import numpy as np


from scripts.typicalLSH import typicalLSH
class typicalLSH_R(typicalLSH):
    
    select_max=0

    # 初始化
    def __init__(self,setgroup,error=0.001,select=1) -> None:
        super().__init__(setgroup,error)
        self.select_max=select

    #  并不是所有的桶内都要放入
    def getBucket(self,set_index):

        st=0
        ed=0
        index_base=0
        select=np.random.randint(0,self.row,(self.select_max,))
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
            # 只有随机选定的bucket中要放入该索引
            if(i in select):
                self.bucket[index+index_base].append(set_index)
            index_base+=self.row_base

            st+=self.row_length