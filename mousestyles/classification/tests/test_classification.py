from mousestyles import data
from mousestyles.classification import classification


def test_prep_data():
    # check prep_data() returns approriate lists for classification
    df = data.load_mouseday_features()
    strain = df['strain']
    features = df.iloc[:, 3:]
    train_y, train_x, test_y, test_x = classification.prep_data(
        strain, features)
    assert train_y.shape == (1440, )
    assert train_x.shape == (1440, 99)
    assert test_y.shape == (481, )
    assert test_x.shape == (481, 99)


def test_RandomForest():
    # check RandomForest() returns approriate data frame with
    # prediction labels and true labels
    # labels are integers from 0 to 15
    df = data.load_mouseday_features()
    strain = df['strain']
    features = df.iloc[:, 3:]
    result = classification.RandomForest(strain, features)
    assert result.shape == (481, 2)
    assert all(result.iloc[:, 0] >= 0) & all(result.iloc[:, 0] <= 15)
    assert all(result.iloc[:, 1] >= 0) & all(result.iloc[:, 1] <= 15)
    assert all([i.is_integer() for i in result.iloc[:, 0]])
    assert all([i.is_integer() for i in result.iloc[:, 1]])


def test_GetSummary():
    # check GetSummary() returns approriate data frame of precision,
    # recall, f-1 measure, in terms of shape and range(0,1)
    df = data.load_mouseday_features()
    strain = df['strain']
    features = df.iloc[:, 3:]
    result = classification.RandomForest(strain, features)
    summary = classification.GetSummary(result)
    assert summary.shape == (16, 3)
    assert all(summary.iloc[:, 0] <= 1) & all(summary.iloc[:, 0] >= 0)
    assert all(summary.iloc[:, 1] <= 1) & all(summary.iloc[:, 1] >= 0)
    assert all(summary.iloc[:, 2] <= 1) & all(summary.iloc[:, 2] >= 0)
