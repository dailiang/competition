# -*- coding: utf-8 -*-
##################
## 共有单词：630030253（6.3亿，不包含人为标注）
## 

import numpy as np
import matplotlib.pyplot as plt
from string import atoi
from math import log

wc_1_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_all.txt'

wc_2_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_2_trunk.txt'

wc_1 = [0] * 1500000
wc_e = 0
with open( wc_1_file, 'r') as f:
    for e, line in enumerate(f):
    	try:
            word, count = map(atoi, line.strip().split())
            wc_1[word] = count
        except:
            wc_e += atoi(line.strip().split()[1])
            continue     
    
with open( wc_2_file, 'r') as f:
	ratio = []
	for e, line in enumerate(f):
		try:
			word1, word2, count = map(atoi, line.strip().split())
			ratio.append(log(630030253 * count * \
			1.0 / (wc_1[word1] * wc_1[word2])))
		except:
			continue

#ratio = filter(lambda x: x > 4, np.asarray(ratio))
# x > 3: 18.7w
# x > 4: 14 w
print len(ratio)

################
## 画图
##############
num_bins = 100
n, bins, patches = plt.hist(ratio, num_bins, facecolor='green')
plt.show()