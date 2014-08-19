# -*- coding: utf-8 -*-
from string import strip

train_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\train.txt'

rows_empty_count = 0L
session_count = 0L
session_longest = 0L
query_longest = 0L
title_longest = 0L
class_one_count = 0L
class_two_count = 0L
titile_count = 0L

CLASSES = [ 'VIDEO', 'NOVEL', 'GAME', 'TRAVEL', 'LOTTERY', 'ZIPCODE', 'OTHER', 'TEST', 'UNKNOWN' ]
# map classes to numbers
classes_map = dict()
for i,c in enumerate( CLASSES ):
    classes_map[c] = i
    
with open( train_file, 'r' ) as f:
    session_count_tmp = 0
    for e, line in enumerate(f):
        if (e + 1) % 1000000 == 0:
            print e + 1

        # line is not empty
        if line.strip():
            session_count_tmp += 1
            if session_count_tmp > session_longest:
                session_longest = session_count_tmp
            line = line.split( '\t' )
            if '|' in line[0]:
                class_two_count += 1
                class_a, class_b = map(strip, line[0].split('|'))
                classes_map[class_a[6:]] += 1
                classes_map[class_b[6:]] += 1
            else:
                class_one_count += 1
                classes_map[line[0][6:]] += 1

            # deal with \n at the end
            line[-1] = line[-1][:-1]    
            if line[-1] != '-':
                titile_count += 1
                if len(line[-1].split(' ')) > title_longest:
                    title_longest = len(line[-1].split(' '))
            if len(line[1].split(' ')) > query_longest:
                query_longest = len(line[1].split(' '))

        else:
            rows_empty_count += 1
            session_count += 1
            session_count_tmp = 0
            
            
print "总行数：", e
print "空行数：", rows_empty_count
print "session数：", session_count
print "最长session：", session_longest
print "最长 query：", query_longest
print "最长 title：", title_longest
print "只有一个 class：", class_one_count
print "有两个 class：", class_two_count
print "总共有 titile：", titile_count
print classes_map

