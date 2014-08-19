# -*-coding=utf-8-*-
import cPickle

train_file = r'../../Data/train.txt'

wc_file = r'../../Data/wc_all.txt'

map_file = r'map.pkl'

## 将 query - count 导入字典
wc_dict = dict()
with open( wc_file, 'r') as f:
    for e, line in enumerate(f):
        word, count = line.strip().split()
        try:
            wc_dict[word] = int(count)
        except:
            print e+1
            continue

print '原来query_wc有：{0}个'.format(len(wc_dict))

with open( train_file, 'r' ) as f:
    word_count = dict()
    for e, line in enumerate(f):
        if (e + 1) % 10000000 == 0:
            print e + 1, len(wc_dict)
        # blank line
        if not line.strip():
            for key in word_count.keys():
                if key in wc_dict and word_count[key] == wc_dict[key]:
                    del wc_dict[key]
            word_count = dict()
        # not blank line
        else:
            line = line.split('\t')[1] # extract query
            for word in line.split():
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

print '现在query_wc有：{0}个'.format(len(wc_dict))

for e, word in enumerate(wc_dict.keys()):
	wc_dict[word] = e

for key, val in wc_dict.items():
	if val < 10:
		print key, val

with open(map_file, 'w') as f:
    cPickle.dump(wc_dict, f)
