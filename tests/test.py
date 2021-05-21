# test1:
import sys

from minHashLab import scripts
from scripts.naiveLSH import naiveLSH
from scripts.myDataGenerator import setGenerator
from scripts.myHash import hashHelpers
from scripts.mySetGroup import setGroup,distriHelper
from scripts.typicalLSH import typicalLSH
from scripts.typicalLSH_R import typicalLSH_R

f = open("./docs/results.txt", "a")
sys.stdout=f

num=800
sets=[0,1,199]
hash=hashHelpers()
hash.initHash(1,num,200,100)
g=setGenerator()

m=setGroup()
g.refinedGenerate(m,sets,num,0.99)
dis=m.jaccardDistri(20)
distriHelper.print_distri(dis,4)

print("num:"+str(num))
print("sum:"+str(sum(sets)))


s=naiveLSH(setgroup=m)

crit=0.60
num=[4,8,16,32,64,128,256] 

print("naiveLSH")

l=[]
for n in num:
    s.calc_pairs(crit,2,n)
    l.append(s.evaluate())
s.printEval(l,3,[])



s1=typicalLSH(m)

print()
print("typicalLSH")
print()

col_num=[5,6,7,8,9,10]
for col in col_num:
    l1=[]
    for n in num:
        s1.calc_pairs(crit,2,n,n/4,col)
        l1.append(s1.evaluate())
    s1.printEval(l1,3,[])
    print()



s2=typicalLSH_R(m)

print()
print("typicalLSH_R:")
print()

col_num=[5,6,7,8,9,10]
for col in col_num:
    l2=[]
    for n in num:
        s2.calc_pairs(crit,2,n,n/4,col)
        l2.append(s2.evaluate())
    s2.printEval(l2,3,[])
    print()


