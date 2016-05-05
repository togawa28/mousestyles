from mousestyles import data
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd 

def prep_data(strain, features, rseed = 222):
    """
    Returns a list of 4: [train_y, train_x, test_y, test_x]
        train_y: list of strain labels in train data sets,
        train_x: list of features in train data sets,
        test_y: list of strain labels in test data sets,
        test_x: list of features in train data sets
    Parameters
    ----------
    strain: ndarray, shape of (1921,)
            classification labels
    features: ndarray, shape of (1921, 99)
              classification features
    rseed: int, optional
           random seed for shuffling the data set to separate train and test
    Returns
    ----------
    The list as specified
    """
    #total: 21131 rows 
    index = np.arange(features.shape[0])
    np.random.seed(rseed)
    np.random.shuffle(index)
    #split the dataset to 75% training and 25% testing 
    sep = int(features.shape[0] * 0.75)
    #total 15848 rows 
    train_x = features.iloc[index[:sep]]
    train_y = strain.iloc[index[:sep]]
    #total 5283 rows 
    test_x = features.iloc[index[sep:]]
    test_y = strain.iloc[index[sep:]]
    return [train_y, train_x, test_y, test_x]


def RandomForest(strain, features, rseed = 222):
    """
    Returns a ndarray of RandomForest results, containing prediction strain 
    labels and true strain labels for test data set. Use cross validation 
    to tune Parameters.
    Parameters
    ----------
    strain: ndarray, shape of (1921,)
            classification labels 
    features: ndarray, shape of (1921, 99)
              classification features
    rseed: int, optional
           random seed for shuffling the data set to separate train and test
    Returns
    ----------
    ndarray of RandomForest results in test data set.
        Column 0: prediction strain labels
        Column 1: true strain labels
    """
    train_y, train_x, test_y, test_x = prep_data(strain, features, rseed)
    #creat RF model 
    scaler = StandardScaler()
    train_x = scaler.fit_transform(train_x)
    es = [500,1000]
    fs = [8,9]
    rf = RandomForestClassifier()
    clf = GridSearchCV(estimator=rf, param_grid=dict(n_estimators=es,
        max_features=fs))
    clf.fit(train_x, train_y) 
    clf = clf.best_estimator_ 
    #fit the best model 
    clf.fit(train_x, train_y)
    #predict the testing data and convert to data frame 
    prediction = clf.predict(scaler.fit_transform((test_x)))
    prediction = pd.DataFrame(prediction)
    #reindex test_y so that it starts from 0  
    test_y.index = range(test_y.shape[0])
    predict_true = pd.concat([prediction,test_y],axis=1)
    predict_true.columns = ['predict_strain','true_strain']
    return(predict_true)



def GetSummary(result) :
    """
    Returns a ndarray of classification result summary,
    including precision, recall, F1 measure in terms of different 
    strains.
    Parameters
    ----------
    result: classification results in test data set
        Column 0: prediction strain labels
        Column 1: true strain labels 
    Returns
    ----------
    ndarray of classification result summary, shape(16,3).
       16 rows, for each strain 0-15
       Column 0: precision
       Column 1: recall
       Column 2: F-1 measure

    """
    prediction_accurate_count_matrix = pd.crosstab(index=result.iloc[:,0],
        columns=result.iloc[:,1],margins=True)  
    prediction_accurate_count_matrix.rename(columns = {"All":"rowTotal"},inplace=True)
    prediction_accurate_count_matrix.rename(index ={"All":"colTotal"},inplace=True)
    prediction_accurate_rate_matrix = prediction_accurate_count_matrix.T / prediction_accurate_count_matrix["rowTotal"]
    #get the precision list 
    precision = [prediction_accurate_rate_matrix.T.iloc[i,i] for i in range(prediction_accurate_rate_matrix.shape[1]-1)]
    prediction_accurate_rate_matrix = prediction_accurate_count_matrix / prediction_accurate_count_matrix.ix["colTotal"]
    #get the recall list 
    recall = [prediction_accurate_rate_matrix.T.iloc[i,i] for i in range(prediction_accurate_rate_matrix.shape[1]-1)]
    #get the F1 list 
    f1= [2*precision[i]*recall[i]/(precision[i]+recall[i]) for i in range(prediction_accurate_rate_matrix.shape[1]-1)]
    summary = pd.concat([pd.DataFrame(precision),pd.DataFrame(recall),pd.DataFrame(f1)],axis=1)
    summary.columns = ['precision','recall',"F1_score"]
    return(summary)






