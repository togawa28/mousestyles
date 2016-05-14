from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm

import numpy as np
import pandas as pd


def prep_data(strain, features, rseed=222):
    """
    Returns a list of 4: [train_y, train_x, test_y, test_x]
        train_y: pandas.Series of strain labels in train data sets,
        train_x: pandas.DataFrame of features in train data sets,
        test_y: pandas.Series of strain labels in test data sets,
        test_x: pandas.DataFrame of features in train data sets
    Parameters
    ----------
    strain: pandas.Series
            classification labels
    features: pandas.DataFrame
              classification features
    rseed: int, optional
           random seed for shuffling the data set to separate train and test
    Returns
    ----------
    splitted data: list
        A list of 4 as explained above
    """
    # shuffle observations
    index = np.arange(features.shape[0])
    np.random.seed(rseed)
    np.random.shuffle(index)
    # split the dataset to 75% training and 25% testing
    sep = int(features.shape[0] * 0.75)
    train_x = features.iloc[index[:sep]]
    train_y = strain.iloc[index[:sep]]
    test_x = features.iloc[index[sep:]]
    test_y = strain.iloc[index[sep:]]
    return [train_y, train_x, test_y, test_x]


def fit_random_forest(train_y, train_x, test_x,
                      n_estimators=None, max_feature=None,
                      importance_level=None):
    """
    Returns a DataFrame of RandomForest results, containing prediction strain
    labels and printing the best model. The model's parameters will be tuned by
    cross validation, and accepts user-defined parameters.
    Parameters
    ----------
    train_y: pandas.Series
             labels of classification results, which are predicted strains.
    train_x: pandas.DataFrame
             features used to predict strains in training set
    test_x: pandas.DataFrame
            features used to predict strains in testing set
    n_estimators: list, optional
                  tuning parameter of RandomForest, which is the number of
                  trees in the forest
    max_feature: list, optional
                 tuning parameter of RandomForest, which is the number of
                 features to consider when looking for the best split
    importance_level: int, optional
                      the minimum importance of features
    Returns
    ----------
    RandomForest results: list
        The first element is the dataframe of prediction strain labels.
        The second element is the list of tuples of score and important
        features larger than the importance level.
    """
    # input validation
    if n_estimators is not None:
        if not isinstance(n_estimators, list):
            raise TypeError("n_estimators should be a list")
        if not all([isinstance(i, int) for i in n_estimators]):
            raise TypeError("All the n_estimators should be integers")
        if not all([i > 0 for i in n_estimators]):
            raise ValueError("All the n_estimators should be positive")
    if max_feature is not None:
        if not isinstance(max_feature, list):
            raise TypeError("max_feature should be a list")
        if not all([isinstance(i, int) for i in max_feature]):
            raise TypeError("All the max_feature should be integers")
        if not all([i > 0 for i in max_feature]):
            raise ValueError("max_features must be in (0, n_features]")
        if not all([i <= train_x.shape[1] for i in max_feature]):
            raise ValueError("max_features must be in (0, n_features]")
    # creat RF model
    scaler = StandardScaler()
    train_x = scaler.fit_transform(train_x)
    es = n_estimators
    fs = max_feature
    if n_estimators is None:
        es = [500, 100]
    if max_feature is None:
        fs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
    if importance_level is None:
        importance_level = 0.05
    rf = RandomForestClassifier()
    clf = GridSearchCV(
        estimator=rf, param_grid=dict(n_estimators=es, max_features=fs))
    clf.fit(train_x, train_y)
    clf = clf.best_estimator_
    imp = clf.feature_importances_
    important_feature = []
    names = test_x.columns
    for i in range(len(imp)):
        sorted_imp = sorted(zip(imp, names))
        if sorted_imp[i][0] >= importance_level:
            important_feature.append(sorted_imp[i])
    # fit the best model
    clf.fit(train_x, train_y)
    # predict the testing data and convert to data frame
    prediction = clf.predict(scaler.fit_transform((test_x)))
    prediction = pd.DataFrame(prediction)
    prediction.columns = ['predict_strain']
    print('The best RandomForest Model is:')
    print(clf)
    return(prediction, important_feature)


def fit_gradient_boosting(train_y, train_x, test_x,
                          n_estimators=None, learning_rate=None):
    """
    Returns a DataFrame of Gradient Boosting results, containing
    prediction strain labels and printing the best model. The
    model's parameters will be tuned by cross validation, and
    accepts user-defined parameters.
    Parameters
    ----------
    train_y: pandas.Series
             labels of classification results, which are predicted strains.
    train_x: pandas.DataFrame
             features used to predict strains in training set
    test_x: pandas.DataFrame
            features used to predict strains in testing set
    n_estimators: list, optional
                  tuning parameter of GradientBoosting, which is the number of
                  boosting stages to perform
    learning_rate: list, optional
                   learning_rate shrinks the contribution of each tree
                   learning_rate
    Returns
    ----------
    GradientBoosting results: pandas.DataFrame
        Prediction strain labels
    """
    # input validation
    if n_estimators is not None:
        if not isinstance(n_estimators, list):
            raise TypeError("n_estimators should be a list")
        if not all([isinstance(i, int) for i in n_estimators]):
            raise TypeError("All the n_estimators should be integers")
        if not all([i > 0 for i in n_estimators]):
            raise ValueError("All the n_estimators should be positive")
    if learning_rate is not None:
        if not isinstance(learning_rate, list):
            raise TypeError("max_feature should be a list")
        if not all([i > 0 for i in learning_rate]):
            raise ValueError("max_features must be greater than 0")
    # creat GradientBoosting model
    scaler = StandardScaler()
    train_x = scaler.fit_transform(train_x)
    es = n_estimators
    ls = learning_rate
    if n_estimators is None:
        es = [100, 200, 300, 500]
    if learning_rate is None:
        ls = list(np.linspace(0.0001, 0.15, 10))
    gb = GradientBoostingClassifier()
    clf = GridSearchCV(
        estimator=gb, param_grid=dict(n_estimators=es, learning_rate=ls),
        n_jobs=-1)
    clf.fit(train_x, train_y)
    clf = clf.best_estimator_
    # fit the best model
    clf.fit(train_x, train_y)
    # predict the testing data and convert to data frame
    prediction = clf.predict(scaler.fit_transform((test_x)))
    prediction = pd.DataFrame(prediction)
    prediction.columns = ['predict_strain']
    print('The best GradientBoosting Model is:')
    print(clf)
    return(prediction)


def fit_svm(train_y, train_x, test_x, c=None, gamma=None):
    """
    Returns a DataFrame of svm results, containing
    prediction strain labels and printing the best model. The
    model's parameters will be tuned by cross validation, and
    accepts user-defined parameters.
    Parameters
    ----------
    train_y: pandas.Series
             labels of classification results, which are predicted strains.
    train_x: pandas.DataFrame
             features used to predict strains in training set
    test_x: pandas.DataFrame
            features used to predict strains in testing set
    c: list, optional
       tuning parameter of svm, which is penalty parameter of the error term
    gamma: list, optional
           tuning parameter of svm, which is kernel coefficient
    Returns
    ----------
    svm results: pandas.DataFrame
        Prediction strain labels
    """
    # input validation
    if c is not None:
        if not isinstance(c, list):
            raise TypeError("c should be a list")
    if gamma is not None:
        if not isinstance(gamma, list):
            raise TypeError("gamma should be a list")
    # creat svm model
    scaler = StandardScaler()
    train_x = scaler.fit_transform(train_x)
    Cs = c
    Gammas = gamma
    if c is None:
        Cs = list(np.logspace(-6, -1, 10))
    if gamma is None:
        Gammas = list(np.linspace(0.0001, 0.15, 10))
    svc = svm.SVC()
    clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs, gamma=Gammas),
                       n_jobs=-1)
    clf.fit(train_x, train_y)
    clf = clf.best_estimator_
    # fit the best model
    clf.fit(train_x, train_y)
    # predict the testing data and convert to data frame
    prediction = clf.predict(scaler.fit_transform((test_x)))
    prediction = pd.DataFrame(prediction)
    prediction.columns = ['predict_strain']
    print('The best SVM Model is:')
    print(clf)
    return(prediction)


def get_summary(predict_labels, true_labels):
    """
    Returns a DataFrame of classification result summary,
    including precision, recall, F1 measure in terms of different
    strains.
    Parameters
    ----------
    predict_labels: pandas.DataFrame
                    prediction strain labels
    true_labels: pandas.Series
                 true strain labels, used to measure the prediction
                 accuracy
    Returns
    ----------
    classification result summary: pandas.DataFrame, shape (16,3).
       16 rows, for each strain 0-15
       Column 0: precision
       Column 1: recall
       Column 2: F-1 measure
    """
    true_labels.index = range(true_labels.shape[0])
    result = pd.concat([predict_labels, pd.DataFrame(true_labels)], axis=1)
    result.columns = ['predict_strain', 'true_strain']
    prediction_accurate_count_matrix = pd.crosstab(index=result.iloc[:, 0],
                                                   columns=result.iloc[:, 1],
                                                   margins=True)
    prediction_accurate_count_matrix.rename(columns={"All": "rowTotal"},
                                            inplace=True)
    prediction_accurate_count_matrix.rename(index={"All": "colTotal"},
                                            inplace=True)
    prediction_accurate_rate_matrix = prediction_accurate_count_matrix.T /\
        prediction_accurate_count_matrix["rowTotal"]
    # get the precision list
    precision = [prediction_accurate_rate_matrix.T.iloc[i, i]
                 for i in range(prediction_accurate_rate_matrix.shape[1] - 1)]
    prediction_accurate_rate_matrix = prediction_accurate_count_matrix /\
        prediction_accurate_count_matrix.ix["colTotal"]
    # get the recall list
    recall = [prediction_accurate_rate_matrix.T.iloc[i, i]
              for i in range(prediction_accurate_rate_matrix.shape[1] - 1)]
    # get the F1 list
    f1 = [2 * precision[i] * recall[i] / (precision[i] + recall[i])
          for i in range(prediction_accurate_rate_matrix.shape[1] - 1)]
    summary = pd.concat([pd.DataFrame(precision),
                         pd.DataFrame(recall), pd.DataFrame(f1)], axis=1)
    summary.columns = ['precision', 'recall', "F1_score"]
    return(summary)
