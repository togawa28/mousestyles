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


def test_fit_random_forest():
    # check fit_random_forest returns approriate data frame with
    # prediction labels
    # labels are integers from 0 to 15
    df = data.load_mouseday_features()
    df = df.iloc[:200, ]
    strain = df['strain']
    features = df.iloc[:, 3:]
    train_y, train_x, test_y, test_x = classification.prep_data(
        strain, features)
    result = classification.fit_random_forest(train_y, train_x, test_x, 1, 10)
    assert features.shape == (200, 99)
    assert result.shape == (50, 1)
    assert all(result.iloc[:, 0] >= 0) & all(result.iloc[:, 0] <= 15)
    assert all([i.is_integer() for i in result.iloc[:, 0]])


def test_get_summary():
    # check get_summary returns approriate data frame of precision,
    # recall, f-1 measure, in terms of shape and range(0,1)
    df = data.load_mouseday_features()
    strain = df['strain']
    features = df.iloc[:, 3:]
    train_y, train_x, test_y, test_x = classification.prep_data(
        strain, features)
    result = classification.fit_random_forest(train_y, train_x, test_x, 1, 10)
    summary = classification.get_summary(result, test_y)
    assert summary.shape == (16, 3)
    assert all(summary.iloc[:, 0] <= 1) & all(summary.iloc[:, 0] >= 0)
    assert all(summary.iloc[:, 1] <= 1) & all(summary.iloc[:, 1] >= 0)
    assert all(summary.iloc[:, 2] <= 1) & all(summary.iloc[:, 2] >= 0)


def test_fit_gradient_boosting():
    # check GradientBoosting() returns approriate data frame with
    # prediction labels and true labels
    # labels are integers from 0 to 15
    df = data.load_mouseday_features()
    strain = df['strain']
    features = df.iloc[:200, 3:]
    train_y, train_x, test_y, test_x = classification.prep_data(
        strain, features)
    result = classification.fit_gradient_boosting(
        train_y, train_x, test_x, 1, 0.15)
    assert features.shape == (200, 99)
    assert result.shape == (50, 1)
    assert all(result.iloc[:, 0] >= 0) & all(result.iloc[:, 0] <= 15)
    assert all([i.is_integer() for i in result.iloc[:, 0]])
