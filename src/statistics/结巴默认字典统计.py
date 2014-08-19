# coding=utf-8

import re

dict_jieba_file = r'C:\Users\dailiang.dl\Desktop\CIKM\Data\dict_jieba.txt'

with open(dict_jieba_file, 'r') as f:
	two = 0
	three = 0
	four = 0
        five = 0
	others = 0
	pattern = re.compile(r'\w+')
	for e, line in enumerate(f):
	    line = unicode(line.split()[0], "utf-8")
	    match = pattern.match(line)
	    line_len = len(line)
	    if match:
	    	line_len = 1 + len(line) - len(match.group())
	    	print line, line_len
	    if line_len == 2:
	    	two += 1
	    elif line_len == 3:
	    	three += 1
	    elif line_len == 4:
	    	four += 1
	    elif line_len == 5:
	        five += 1
	        print line
	    else:
	    	others += 1
	print two, three, four, five, others
