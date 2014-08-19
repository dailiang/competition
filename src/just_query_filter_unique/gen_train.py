import cPickle
from string import strip

train_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\train'#_part.txt'

map_file = r'C:\Users\dailiang.dl\Desktop\CIKM\src\just_query_filter_unique\map.pkl'

save_file = r'C:\Users\dailiang.dl\Desktop\CIKM\src\just_query_filter_unique\train.txt'

CLASSES = [ 'VIDEO', 'NOVEL', 'GAME', 'TRAVEL', 'LOTTERY', 'ZIPCODE', 'OTHER' ]
# map classes to numbers
classes_map = dict()
for i, c in enumerate( CLASSES ):
    classes_map[c] = i

f = open(map_file)
word_map = cPickle.load(f)
f.close()
f_save = open(save_file, 'w')

with open( train_file, 'r' ) as f:
    train_without_UNKNOWN = []
    for e, line in enumerate(f):
        if (e + 1) % 10000000 == 0:
            print e + 1
        if line.strip():
	        classes, query, title = line.split('\t')
	        if not classes[6:] in ('UNKNOWN', 'TEST'):
	        	try:
		            if '|' in classes:
		                class_a, class_b = map(strip, classes.split('|'))
		                class_a = classes_map[class_a[6:]]
		                class_b = classes_map[class_b[6:]]
		                label = str(class_a) + ',' + str(class_b)
		            else:
		            	label = str(classes_map[classes[6:]])
		            feature = ' '.join([str(word_map.get(item)) for item in query.split()])
		            if len(feature) > 0: 
		            	f_save.write(' '.join((label, feature, '\n')))
		        except:
		        	print 'error:', e + 1
		        	continue

f_save.close()
