# Load libraries
import pandas as pd
from sklearn.model_selection import train_test_split # Import train_test_split function
import pickle
import numpy
from sklearn.model_selection import GridSearchCV
from sklearn import svm
numpy.random.seed(7)

# load the data
file_name = 'data/credit card fraud/data_creditcard.pkl'  # set working directory to MSc Project
data = pd.read_pickle(file_name)

train_data, test_data, train_labels, test_labels = \
    train_test_split(data, data['class'], test_size=0.25, random_state=1)

# even out the data set -> 1:1 ratio of 0 and 1 classes
data_training = train_data.sample(frac=1)  # shuffle

fraud_data_training = data_training.loc[data_training['class'] == 1]

non_fraud_data_training = data_training.loc[data_training['class'] == 0][:50000]

even_data_training = pd.concat([fraud_data_training, non_fraud_data_training])

even_data_training = even_data_training.sample(frac=1, random_state=42)

data = even_data_training


# # cross-validation and parameter optimisation
# parameters = [
#   {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#   {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
#  ]
# clf = GridSearchCV(svm.SVC(), parameters, n_jobs=4, cv=4, scoring='f1', verbose=2)
# clf.fit(X=X_train[1:25000], y=y_train[1:25000])
# SCM_model = clf.best_estimator_
# print(clf.best_score_, clf.best_params_)


def get_SVM_model(data=data, kernel='linear', gamma=0.0001, C=100, probability=True, verbose=2,
                  model_name='model_SVM_unbalanced.pkl'):

    X = data.drop('class', axis=1)
    y = data['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Create SVM classifer object
    clf = svm.SVC(kernel=kernel, gamma=gamma, C=C, probability=probability, verbose=verbose, cache_size=1500)

    # Train SVM classifer
    model = clf.fit(X_train, y_train)

    path = '1) classification algorithms/SVM/credit card fraud/'+model_name

    with open(path, 'wb') as file:
        pickle.dump(model, file)
    return


get_SVM_model()