# -*- coding: utf-8 -*-
##################
## 共有单词：630030253（6.3亿，不包含人为标注）
## 

import numpy as np
import matplotlib.pyplot as plt
from string import atoi
from math import log

## 全局的统计

wc_1_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_all.txt'

wc_2_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_2_trunk.txt'

wc_3_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_3_trunk.txt'

with open( wc_1_file, 'r') as f:
    wc_1 = dict()
    for e, line in enumerate(f):
    	try:
            word, count = line.strip().split('\t')
            wc_1[word] = int(count)
        except:
            print 'error1:', e + 1
            continue     
    
with open( wc_2_file, 'r') as f:
	wc_2 = dict()
	for e, line in enumerate(f):
		try:
			word, count = line.strip().split('\t')
			wc_2[word] = int(count)
		except:
			print 'error2:', e + 1
			continue

with open( wc_3_file, 'r') as f:
	ratio = []
	for e, line in enumerate(f):
		try:
			word, count = line.strip().split('\t')
			word1, word2, word3 = word.split()
			count = int(count)
			ratio1 = log(630030253. * count / wc_1[word1] * wc_2[' '.join((word2, word3))])
			ratio2 = log(630030253. * count / wc_1[word3] * wc_2[' '.join((word1, word2))])
			ratio.append(min(ratio1, ratio2))
		except:
			print 'error3', e + 1
			continue

ratio = filter(lambda x: x > -21, ratio)

print len(ratio)



################
## 画图
##############
num_bins = 100
n, bins, patches = plt.hist(ratio, num_bins, facecolor='green')
plt.show()