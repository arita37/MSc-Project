# unbalanced parameters: {'bootstrap': True, 'max_depth': 5, 'min_samples_split': 2, 'n_estimators': 100}
import pandas as pd
from sklearn.model_selection import train_test_split
from dtreeplt import dtreeplt
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import confusion_matrix, classification_report
from global_functions import get_balanced_data, get_model_performance
from global_functions import plot_confusion_matrix, cm_analysis
np.random.seed(7)

# load the data
file_name = 'data/bioresponse/bio_clean.pkl'  # set working directory to MSc Project
data = pd.read_pickle(file_name)

# unbalanced data
X = data.drop('class',axis=1)
y = data['class']
X_train_unbalanced, X_test_unbalanced, y_train_unbalanced, y_test_unbalanced = train_test_split(X, y, test_size=0.25,
                                                                                                random_state=1)

# balanced data
# even out the data set -> 1:1 ratio of fraud and non fraud
X_train_balanced, X_test_balanced, y_train_balanced, y_test_balanced = get_balanced_data(data)

# unpack unbalanced model
path = '1) classification algorithms/random forest/bioresponse/model_forest_unbalanced_bio.pkl'
with open(path, 'rb') as file:
    unbalanced_model = pickle.load(file)

# unpack balanced model
path = '1) classification algorithms/random forest/bioresponse/model_forest_balanced_bio.pkl'
with open(path, 'rb') as file:
    balanced_model = pickle.load(file)

# predict labels
unbalanced_predictions = unbalanced_model.predict(X_test_unbalanced)
unbalanced_predictions = [int(round(x)) for x in unbalanced_predictions]
balanced_predictions = balanced_model.predict(X_test_balanced)
balanced_predictions = [int(round(x)) for x in balanced_predictions]

# print the confusion matrix, precision, recall, etc.
get_model_performance(unbalanced_model, 'unbalanced', X_test_unbalanced, y_test_unbalanced, 'RF','bioresponse dataset')
plt.savefig('1) classification algorithms/assess model performance/bioresponse/figures/PRcurve_rf_unbalanced_bio.png')
plt.close()
get_model_performance(balanced_model, 'balanced', X_test_balanced, y_test_balanced,'RF','bioresponse dataset')
plt.savefig('1) classification algorithms/assess model performance/bioresponse/figures/PRcurve_rf_balanced_bio.png')
plt.close()

cm_analysis(y_test_balanced, balanced_predictions, filename='1) classification algorithms/assess model performance/bioresponse/figures/cm_rf_balanced_bio.png',labels=[0, 1],
            ymap=['class0','class1'],title='RF performance on balanced data\nbioresponse dataset')

cm_analysis(y_test_unbalanced,unbalanced_predictions,filename='1) classification algorithms/assess model performance/bioresponse/figures/cm_rf_unbalanced_bio.png',labels=[0, 1],
            ymap=['class0','class1'],title='RF performance on unbalanced data\nbioresponse dataset')
