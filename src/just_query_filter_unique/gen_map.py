import cPickle

train_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\train'#_part.txt'

wc_query_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\wc_query.txt'

map_file = r'C:\Users\dailiang.dl\Desktop\CIKM\src\just_query_filter_unique\map'

## 将 query - count 导入字典
wc_query_dict = dict()
with open( wc_query_file, 'r') as f:
    for e, line in enumerate(f):
        word, count = line.strip().split()
        try:
            wc_query_dict[word] = int(count)
        except:
            print e+1
            continue

print '原来query_wc有：{0}个'.format(len(wc_query_dict))

with open( train_file, 'r' ) as f:
    word_count = dict()
    for e, line in enumerate(f):
        if (e + 1) % 10000000 == 0:
            print e + 1, len(wc_query_dict)
        # blank line
        if not line.strip():
            for key in word_count.keys():
                if key in wc_query_dict and word_count[key] == wc_query_dict[key]:
                    del wc_query_dict[key]
            word_count = dict()
        # not blank line
        else:
            line = line.split('\t')[1] # extract query
            for word in line.split():
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

print '现在query_wc有：{0}个'.format(len(wc_query_dict))

for e, word in enumerate(wc_query_dict.keys()):
	wc_query_dict[word] = e

for key, val in wc_query_dict.items():
	if val < 100:
		print key, val

with open(map_file, 'w') as f:
    cPickle.dump(wc_query_dict, f)