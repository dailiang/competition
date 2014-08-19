# -*- coding: utf-8 -*-

"""
Competition:

2014 CIKM Competition
http://cikm2014.fudan.edu.cn/index.php/Index/info/id/29
http://openresearch.baidu.com/topic/71.jspx

Description:

Code provided here for creating a naive baseline for this competition by simply
predicting all the testing data as the major class. Nothing fancy but just to
get you started. It yields Macro F1-score = 0.0824 on the public leaderboard.

Python version: 2.7.6
Version: 1.0 at Jul 19 2014
Author: Chenglong Chen < yr@Kaggle >
Email: c.chenglong@gmail.com
"""

# all required modules
import numpy as np
from sklearn.cross_validation import KFold, StratifiedKFold
from sklearn.metrics import f1_score


def main():
    
    ###################################
    ## Map string classes to numbers ##
    ###################################
    # all allowed classes
    CLASSES = [ 'VIDEO', 'NOVEL', 'GAME', 'TRAVEL', 'LOTTERY', 'ZIPCODE', 'OTHER' ]
    # map classes to numbers
    CLASSES_map = dict()
    for i,c in enumerate( CLASSES ):
        CLASSES_map[c] = i
    
        
    #########################################
    ## Get the class for all training data ##
    #########################################
    print 'Get the class for all training data ...'
    # you should specify data_path that contains the following data
    # - train
    # - testData.txt
    # - sampleSubmission.txt
    data_path = '../Data/'
    train_file = data_path + 'train' 
    y_train = []
    with open( train_file, 'rb' ) as f:
        for e, line in enumerate(f):
            line = line.split( '\t' )
            # deal with \n at the end
            line[-1] = line[-1][:-1]
            # get the class
            c = line[0][6:]
            if c in CLASSES:
                y_train.append( CLASSES_map[c] )
            # verbose
            if (e+1)%10000000 == 0:
                print (e+1)
            
    # convert to numpy array            
    y_train = np.asarray(y_train, dtype=int)            
    print 'Done'
            
                
    ##############################
    ## Perform cross-validation ##
    ##############################    
    numTrain = len(y_train)
    numClass = len(CLASSES)
    n_folds = 10
#    # stratified k-fold
#    skf = StratifiedKFold(y=y_train, n_folds=n_folds)
    # standard k-fold
    kf = KFold(n=numTrain, n_folds=n_folds, random_state=1234)
    F_macro = np.zeros((n_folds,), dtype=float)
    fold = 0
    print 'Perform {0}-fold cross-validation ...'.format(n_folds)
    for train_index, valid_index in kf:
        # If we are using stratified k-fold, we can actually get the major class
        # from the whole training data and do not have to do the following for every
        # fold. If you are using other prediction method, it is the right way to go.
        major_class = None
        major_count = 0
        for i in xrange(numClass):
            this_count = np.sum( y_train[train_index] == i )
            if this_count > major_count:
                major_count = this_count
                major_class = i
        y_valid = y_train[valid_index]
        y_valid_pred = major_class*np.ones((len(valid_index),), dtype=int)
        F_macro[fold] = f1_score(y_valid, y_valid_pred, average='macro')
        fold += 1
        print 'Done for fold {0}'.format(fold)

    # compute mean macro F1-score of n-fold    
    F_macro_mean = np.mean(F_macro)
    F_macro_std = np.std(F_macro)
    print 'Macro F1-score of %d-fold CV: mean = %f, std = %f'%(
            n_folds, np.round(F_macro_mean,5), np.round(F_macro_std))
    print 'Done'

        
    #######################
    ## Create submission ##
    #######################
    # get the major class from the whole training data    
    major_class = None
    major_count = 0
    for i in xrange(numClass):
        this_count = np.sum( y_train == i )
        if this_count > major_count:
            major_count = this_count
            major_class = i
    print 'Major class of the whole training data is: {0} with count = {1}'.format(
            CLASSES[major_class], major_count)

#    # read in the sample submission for checking the file format
#    print 'Check file format of the sample submssion ...'
#    sample_file = data_path + 'sampleSubmission.txt'
#    with open( sample_file, 'rb' ) as f:
#        for e, line in enumerate(f):
#            if e == 0:
#                print line
#                break
#    line
#    print 'Done'

    # create naive baseline submission
    test_file = data_path + 'testData.txt'
    submission_file = data_path + 'CIKM2014_naive_baseline.txt'
    print 'Create naive baseline submission file %s ...' % submission_file
    with open( submission_file, 'wb' ) as sub_file:
        with open( test_file, 'rb' ) as f:
            for e, line in enumerate(f):
                # deal with \r\n at the end
                line = line[:-2]
                line += '\tCLASS=%s\r\n' % CLASSES[major_class]
                sub_file.write(line)
                # verbose
                if (e+1)%10000 == 0:
                    print (e+1)
    print 'Done'
    

if __name__ == '__main__':
    main()
    