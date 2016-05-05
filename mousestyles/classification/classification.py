from mousestyles import data
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd 

def RandomForest():
    df = data.load_all_features()
    #total: 21131 rows 
    index = np.arange(df.shape[0])
    np.random.seed(222)
    np.random.shuffle(index)
    #split the dataset to 75% training and 25% testing 
    sep = int(df.shape[0]*0.75)
    #total 15848 rows 
    train = df.iloc[index[:sep]]
    #total 5283 rows 
    test = df.iloc[index[sep:]]
    #select features starting from column 4. 
    #eliminate columns strain, mouse, day, hour
    train_x = train.iloc[:,4:]
    #label is the strain 
    train_y = train['strain']
    test_x = test.iloc[:,4:]
    test_y = test['strain']
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

#test with RF Model 
GetSummary(RandomForest())




