import random
import time as t
import sys

i = int(input())
o = int(input())
global l3
l3 = 0
while l3 != o:
    
    w1 = random.randint(0,1000)/100
    w2 = random.randint(0,1000)/100
    w3 = random.randint(0,1000)/100
    w4 = random.randint(0,1000)/100
    w5 = random.randint(0,10000)/100
    
    t1 = random.randint(0,1000)/100
    t2 = random.randint(0,1000)/100
    t3 = random.randint(0,1000)/100
    t4 = random.randint(0,1000)/100
    t5 = random.randint(0,1000)/100
    l1 = i*w1
    if(l1 < t1):
        l1 = 0

    l2 = i*w2
    if(l2 < t2):
        l2 = 0
    
    l3 = l1+l2*w3
    if(l3 < t3):
        l3 = 0
    
    print(l3,"=",w1," and ",w2)