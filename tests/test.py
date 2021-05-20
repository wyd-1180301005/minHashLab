# test1:

from minHashLab import scripts
from scripts.naiveLSH import naiveLSH
from scripts.myDataGenerator import setGenerator
from scripts.myHash import hashHelpers
from scripts.mySetGroup import setGroup,distriHelper
from scripts.naiveAmpLSH import naiveAmpLSH

num=800
hash=hashHelpers()
hash.initHash(1,num,200,100)
g=setGenerator()

m=setGroup()
# g.naiveGenerate(m,100,num)
g.refinedGenerate(m,[0,1,299],num,0.90)
dis=m.jaccardDistri(20)
distriHelper.print_distri(dis,4)



s=naiveLSH(setgroup=m)

crit=0.6
num=[2,4,8,16,32,64] 
error=0.001


l=[]
for n in num:
    s.calc_pairs(crit,2,n)
    l.append(s.evaluate())
s.printEval(l,3,[])



s1=naiveAmpLSH(setgroup=m)


print()

l1=[]
for n in num:
    s1.calc_pairs(crit,2,n)
    l1.append(s1.evaluate())
s1.printEval(l1,3,[])

