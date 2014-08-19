#-*- coding=utf-8 -*-

import numpy as np
import sys
from scipy.sparse import *
from sklearn import *

train_file = r'train_part.txt'

def loadfile(train_file, istrain):
	ifile = open(train_file)
	i = 0
	feature_col = []
	feature_val = []
	feature_row = []
	label_col = []
	label_row = []
	for s in ifile:
		try:
			labels, features = s.split(" ", 1)
			if istrain:
				labels_split = labels.split(',')
				label_col.extend([int(x) for x in labels_split])
				label_row.extend([i] * len(labels_split))
			for feature in features.rstrip().split(' '):
				feature_col.append(int(feature))
				feature_val.append(1.0)
				feature_row.append(i)
			i += 1
			if i % 100000 == 0:
				print str(i) + 'lines'
		except ValueError:
			print 'Value Error: ', i + 1

	features = csc_matrix((feature_val, (feature_row, feature_col)))
	if istrain:
		labels = csc_matrix(([1]*len(label_col), (label_row, label_col)))
		return features, labels
	return features

def modelfit(train_set, train_label, valid_set, model, pred_train=False, verbosity=False):
	n_category = train_label.shape[1]
	valid_pred = np.zeros((valid_set.shape[0], n_category))
	if pred_train:
		train_pred = np.zeros((train_set.shape[0], n_category))
	if hasattr(model, 'predict_proba'):
		for category in range(n_category):
			if np.any(train_label[:, category] > 0):
				model.fit(train_set, train_label[:, category])
				valid_pred[:, category] = model.predict_proba(valid_set)[:, 1]
				if pred_train:
					train_pred[:, category] = model.predict_proba(train_set)[:, 1]
				if verbosity:
					print j, '-th category done!'
	else:
		for category in range(n_category):
			if np.any(train_label[:, category] > 0):
				model.fit(train_set, train_label[:, category])
				valid_pred[:, category] = model.predict(valid_set)
				if pred_train:
					train_pred[:, category] = model.predict(train_set)
				if verbosity:
					print j, '-th category done!'
	if pred_train:
		return valid_pred, train_pred
	return valid_pred

#########
# train #
#########
print 'loading train_set ...'
train_set, train_label = loadfile(train_file, istrain=True)
train_label = train_label.todense()
train_label = np.array(train_label)

# split the data into train set and vaild set
m = int(0.9 * train_label.shape[0])
valid_set = train_set[m:, :]
valid_label = train_label[m:, :]
train_set = train_set[:m, :]
train_label = train_label[:m, :]

#LR1_valid_pred, LR1_train_pred = modelfit(train_set, train_label, valid_set, linear_model.LogisticRegression(penalty='l1', C=6.0, tol=0.001), pred_train=True, verbosity=False)
LR1_valid_pred, LR1_train_pred = modelfit(train_set, train_label, valid_set, linear_model.SGDClassifier(loss='log', penalty='l1', alpha=1/6.0), pred_train=True, verbosity=False)
print 'test f1:', metrics.f1_score(np.argmax(valid_label, axis=1), np.argmax(LR1_valid_pred, axis=1))
print 'train f1:', metrics.f1_score(np.argmax(train_label, axis=1), np.argmax(LR1_train_pred, axis=1))
