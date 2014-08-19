# -*- coding: utf-8 -*-
from string import atoi

train_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\train_part.txt'

wc_query_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_all.txt'

wc_query_dict = dict()
with open( wc_query_file, 'r') as f:
    for e, line in enumerate(f):
        word, count = line.strip().split()
        try:
            wc_query_dict[word] = atoi(count)
        except:
            print e+1
            continue

print '原来query_wc有：{0}个'.format(len(wc_query_dict))

with open( train_file, 'r' ) as f:
    word_count = dict()
    for e, line in enumerate(f):
        if (e + 1) % 1000000 == 0:
            print e + 1, len(wc_query_dict)
        # blank line
        if not line.strip():
            for key in word_count.keys():
                if key in wc_query_dict and word_count[key] == wc_query_dict[key]:
                    del wc_query_dict[key]
            word_count = dict()
        # not blank line
        else:
            #line = line.split('\t')[1] # extract query
            for word in line.split():
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

print '现在query_wc有：{0}个'.format(len(wc_query_dict))

with 