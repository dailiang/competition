import numpy as np
import sys
from scipy.sparse import *
from sklearn import *

# for test/train data loading
def loadfile(filename, istrain):
    ifile = open(filename)
    i = 0
    A = []
    B = []
    I = []
    cls = []
    Icls = []
    for s in ifile:
        try:
            # labels，features
            sbeg, send = s.split(" ", 1)
            if istrain:
                sbegsplit = sbeg.split(",")
                # column: cls = [label1, label2, label3, ...]
                cls.extend([(int(x)-1) for x in sbegsplit])
                # row: Icls = [0, 0, 1, 2, 2, ...]
                Icls.extend([i]*len(sbegsplit))
            send = send.rstrip()
            for ss in send.split(" "):
                a, b = ss.split(":")
                # colomn: A = [1122, 1132, 4509, ...]
                A.append(int(a)-1)
                # value: B = [0.2, 0.3, 0.4, ...]
                B.append(float(b))
                # row: I = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, ...]
                I.append(i)  
            i += 1
            if i % 10000 == 0:
                print str(i)+' lines'
        except ValueError:
            print 'Value Error: ', i + 1
    # feature value matrix: 65K rows, 300K columns
    S = csc_matrix((B, (I, A)))
    if istrain:
        # label matrix: 65K rows, 203 columns
        C = csc_matrix(([1]*len(cls), (Icls, cls)))
        return S, C
    return S

# to build model in a multi-label problem
def modelfit(S1, C1, S2, model, makeA1=False, verbosity=False):
    # S1: train set 
    # C1: train label
    # S2: valid set
    l = C1.shape[1]  # 203 column
    A2 = np.zeros((S2.shape[0], l)) # set all the valid labels to 0
    if makeA1:
        A1 = np.zeros((S1.shape[0], l)) # set all the train labels to 0
    if hasattr(model, 'predict_proba'):
        for j in range(l):
            if np.any(C1[:, j] > 0):  # if there's jth-class positive sample in train set
                model.fit(S1, C1[:, j]) # train jth-class
                A2[:, j] = model.predict_proba(S2)[:, 1] # predict valid set
                if makeA1:
                    A1[:, j] = model.predict_proba(S1)[:, 1] # predict train set
                if verbosity:
                    print j # jth_class done!
    else:
        for j in range(l):
            if np.any(C1[:, j] > 0):
                model.fit(S1, C1[:, j])
                A2[:, j] = model.predict(S2)
                if makeA1:
                    A1[:, j] = model.predict(S1)
                if verbosity:
                    print j
    if makeA1:
        return A2, A1
    return A2

# knn
def myknn(S, C, S2):
    Aknn  = np.zeros((S2.shape[0], C.shape[1]))
    Aknn1 = np.zeros((S2.shape[0], C.shape[1]))
    Aknn2 = np.zeros((S2.shape[0], C.shape[1]))
    Aknn3 = np.zeros((S2.shape[0], C.shape[1]))
    for i in range(S2.shape[0]):
        r = (S * S2[i, :].T).todense()
        indexessort = np.argsort(-np.array(r)[:, 0])
        Aknn[i, :]  = r[indexessort[0:50], :].T * C[indexessort[0:50], :]  # a = r.T * C
        Aknn1[i, :] = r[indexessort[0], :].T * C[indexessort[0], :]  # a = r.T * C
        Aknn2[i, :] = r[indexessort[1], :].T * C[indexessort[1], :]  # a = r.T * C
        Aknn3[i, :] = r[indexessort[2], :].T * C[indexessort[2], :]  # a = r.T * C
        if i % 1000 == 0:
            print str(i)+' nn'
    return Aknn, Aknn1, Aknn2, Aknn3

# MAIN CODE
########################
## Get All valid pred ##
########################
print 'the training set: loading'
S, C = loadfile(r'C:\Users\dailiang.dl\Desktop\CIKM\WISE2014\Data\wise2014-train.libsvm', True)
C = C.todense()
C = np.array(C)  # matrix -> array

m = 50000 # from m-th article - validation set

print 'knn - the validation set (the last articles in the training set)'
Aknnsmall, Aknn1small, Aknn2small, Aknn3small = myknn(S[:m, :], C[:m, :], S[m:, :])

print 'logistic regression - the validation set (the last articles in the training set)'
AL1small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.LogisticRegression(penalty='l1', C=2.0, tol=0.001), makeA1=False, verbosity=False)
AL2small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.LogisticRegression(penalty='l1', C=6.0, tol=0.001), makeA1=False, verbosity=False)
AL3small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.LogisticRegression(penalty='l1', C=10.0, tol=0.001), makeA1=False, verbosity=False)

print 'ridge regression - the validation set (the last articles in the training set)'
AR1small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.Ridge(alpha=0.4), makeA1=False, verbosity=False)
AR2small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.Ridge(alpha=0.8), makeA1=False, verbosity=False)
AR3small = modelfit(S[:m, :], C[:m, :], S[m:, :], linear_model.Ridge(alpha=1.2), makeA1=False, verbosity=False)

########################################
# Train on the train set and valid set #
# Get the test preds                   #
########################################

print 'the test set: loading'
Stest = loadfile(r'C:\Users\dailiang.dl\Desktop\CIKM\WISE2014\Data\wise2014-test.libsvm', False)

print 'knn - the test set'
Aknn, Aknn1, Aknn2, Aknn3 = myknn(S, C, Stest)

print 'logistic regression - the test set'
AL1 = modelfit(S, C, Stest, linear_model.LogisticRegression(penalty='l1', C=2.0, tol=0.001), makeA1=False, verbosity=False)
AL2 = modelfit(S, C, Stest, linear_model.LogisticRegression(penalty='l1', C=6.0, tol=0.001), makeA1=False, verbosity=False)
AL3 = modelfit(S, C, Stest, linear_model.LogisticRegression(penalty='l1', C=10.0, tol=0.001), makeA1=False, verbosity=False)

print 'ridge regression - the test set'
AR1 = modelfit(S, C, Stest, linear_model.Ridge(alpha=0.4), makeA1=False, verbosity=False)
AR2 = modelfit(S, C, Stest, linear_model.Ridge(alpha=0.8), makeA1=False, verbosity=False)
AR3 = modelfit(S, C, Stest, linear_model.Ridge(alpha=1.2), makeA1=False, verbosity=False)

################################
# Compute coeff using Ridge    #
# input: pred of ten estimator #
# label: the correct label     #
################################
print 'linear combinations...'
model = linear_model.Ridge(alpha=2.0)
AN = 0.65*AL2 + 0.35*AR2 # default

for j in range(C.shape[1]):
    if np.sum(C[m: , j])>0:
        Xsmall = np.vstack([AL1small[:, j], AL2small[:, j], AL3small[:, j],
                            AR1small[:, j], AR2small[:, j], AR3small[:, j],
                            Aknn1small[:, j], Aknn2small[:, j], Aknn3small[:, j],
                            Aknnsmall[:, j] ]).T
        X = np.vstack([AL1[:, j], AL2[:, j], AL3[:, j],
                            AR1[:, j], AR2[:, j], AR3[:, j],
                            Aknn1[:, j], Aknn2[:, j], Aknn3[:, j], Aknn[:, j] ]).T
        model.fit(Xsmall, C[m:, j])
        # each Ridge model for each class
        AN[:, j] = model.predict(X)
        # print 'done: ' + str(j)

#################
# Decision rule #
#################
print 'decision rule'
maxes = np.max(AN, axis=1)+0.000001
A = AN / maxes[:, np.newaxis]
A = 0 + (A > 0.55)

print 'solution - nonzero elements'
ofile = open(r'C:\Users\dailiang.dl\Desktop\CIKM\WISE2014\Data\big_solution2.csv', 'wb')
linecount = 64857
ofile.write('ArticleId,Labels\n')
for i in range(A.shape[0]):
    Aclasses = np.nonzero(A[i, :])[0] + 1
    strtowrite = ''.join([' %g' % num for num in Aclasses])
    ofile.write(str(64858+i) + ',' + strtowrite[1:] + '\n')
ofile.close()
