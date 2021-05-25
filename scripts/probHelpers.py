import math as ma


# 求chernoff界的方法
# expect是期望,不是概率,expect=概率*个数
def chernoff(expect,delta,IsUp):
    exp_v=expect*delta*delta*-1
    if(IsUp):
        return ma.exp(exp_v/3)
    else:
        return ma.exp(exp_v/2) 



# 通过给定"偏心误差的概率上限",由chernoff不等式计算"泊松实验次数"的下限的方法
# 在minHash的角度,就是通过给定已知假阳性概率或者假阴性概率的情况下,求出假阳性/假阴性错误发生的概率的上限


# 算法说明:
# 
# 一:假阳性概率:
#  1.如果已知:
#       [a].选择的hash函数的个数为N
#       [b].接收阈值为c                    PS:也就是说jaccard值大于c的集合对是我们想要的解
#       [c].集族真实的jaccard值的分布dis()  PS:也就是说给定一个jaccard值范围range=[s0,t0],能够调用dis(range)得出这些值的集对在全体集对中的比例
#  2.由chernoff不等式得:
#       [a].假设f为估算后满足c,然而实际上是假阳性的集对,那么将区间[0,c]等分为k份,记为r1,r2,...,rk
#       [b].通过dis()函数,获得这些区间的占比,并且用区间的中位数代表区间的jaccard值的大小,分别记作d1,d2,...,dk;j1,j2,...,jk
#       [c].因为从属于第i个区间的集对,如果在估测后显示为假阳性,则估测的误差大小是c-ji,误差的程度是ei=(c-ji)/ji
#       [d].假设使用的hash函数的个数是N,则根据minHash原理,从属于第i个区间的集对在minHash中相等的hash个数的期望值为N*ji
#       [e].根据chernoff不等式,从属于第i个区间的集对被N个minHash估测后,显示为假阳性的概率小于chernoff(N*ji,ei)[0],记作pi
#       [f].那么对于任意一个集对pa,Pr[pa被N个minHash估计为假阳性]=Sum_i{Pr[pa属于ri;pa被估计为假阳性]}=Sum_i{Pr[pa被估计为假阳性|pa属于ri]*Pr[pa属于ri]}   
#       [g].综上所述,Pr[pa被N个minHash估计为假阳性]小于等于Sum_i{pi*di}
#  3.参数与返回值的说明:
#       dis是一个储存分布大小的数组 如果dis=[0.2,0.3,0.1,0.1,0.3],则说明dis刻画了五等分[0,1]区间的分布,每个区间长度为0.2
#       minAccuracy是所允许的最小精确度,比如当crit=0.3 minAccuracy=0.0001时,将jaccard=0.2999的集对判别为满足crit的集合是合法的
#       返回的概率值是全体集对中被错误地判断为阳性(假阳性)的集对的占比--假阳性的集对/所有可能的集对
#  4.可能出现的问题:
#       当crit太小的情况下,直接返回0

# 求出总体阳性中假阳性比例的方法
def probFalsePositive(hashNum,crit,minAccuracy,dis):
    res=0.0
    renderedCrit=crit-minAccuracy
    step=1.0/len(dis)
    ji=step/2
    for di in dis:
        #只考察那些小于renderedCrit的集对
        if(ji>renderedCrit):
            break
        else:
            ei=(crit-ji)/ji
            res+=chernoff(hashNum*ji,ei,True)*di
            ji+=step 
    return res

# 求出总体阴性中假阴性比例的方法
def probFalseNegative(hashNum,crit,minAccuracy,dis):
    res=0.0
    renderedCrit=crit+minAccuracy
    step=1.0/len(dis)
    ji=step/2
    for di in dis:
        #只考察那些大于renderedCrit的集对
        if(ji<renderedCrit):
            ji+=step
            continue
        ei=(ji-crit)/ji
        res+=chernoff(hashNum*ji,ei,False)*di
        ji+=step 
    return res


# 求出总体阳性中假阳性比例的方法
# 经过概率放大技术,一共amp次实验,需要至少pos次实验结果为阳性才能判别为阳性
# pi=chernoff(hashNum*ji,ei,True) 是实验成功一次的概率,
# 则放大后的概率应该是一个二项分布的k=pos 到 k=amp项值之和
def probFalsePositiveAmp(hashNum,crit,minAccuracy,dis,amp,pos):
    res=0.0
    renderedCrit=crit-minAccuracy
    step=1.0/len(dis)
    ji=step/2
    for di in dis:
        #只考察那些小于renderedCrit的集对
        if(ji>renderedCrit):
            break
        else:
            ei=(crit-ji)/ji
            pi=chernoff(hashNum*ji,ei,True)
            qi=probBinominalSum(amp,pos,pi)
            res+=qi*di
            ji+=step 
    return res

# 求出总体阴性中假阴性比例的方法
# 经过概率放大技术,一共amp次实验,需要至少pos次实验结果为阳性才能判别为阳性
# pi=chernoff(hashNum*ji,ei,True) 是实验失败一次的概率,失败的次数也要至少pos次
# 则放大后的概率应该是一个二项分布的k=amp-pos+1 到 k=amp项值之和
def probFalseNegativeAmp(hashNum,crit,minAccuracy,dis,amp,pos):
    res=0.0
    renderedCrit=crit+minAccuracy
    step=1.0/len(dis)
    ji=step/2
    for di in dis:
        #只考察那些大于renderedCrit的集对
        if(ji<renderedCrit):
            ji+=step
            continue
        ei=(ji-crit)/ji
        pi=chernoff(hashNum*ji,ei,False)
        pi=probBinominalSum(amp,amp-pos+1,pi)
        res+=pi*di
        ji+=step 
    return res

def probBinominalSum(n,st,p):
    pro_sum=0.0
    for i in range(st,n+1):
        pro_sum+=(ma.comb(n,i)*ma.pow(p,i))*ma.pow(1-p,n-i)
    return pro_sum

