# the same model parameters as for original balanced model
# {'bootstrap': True, 'max_depth': 5, 'min_samples_split': 2, 'n_estimators': 100}
# the same model parameters as for original balanced model

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
np.random.seed(7)

###################### load the data ####################################

# load the real data
file_name = 'data/credit card fraud/data_creditcard.pkl'  # set working directory to MSc Project
real_data = pd.read_pickle(file_name)

# load synthetic fraud examples
file_name = 'data/credit card fraud/synthpop_fo_15000.pkl'
synthpop_fraud = pd.read_pickle(file_name)

file_name = '2) synthetic data generation/GAN/credit card fraud/GAN_fraud_5904.pkl'
GAN_fraud = pd.read_pickle(file_name)

file_name = '2) synthetic data generation/cGAN/credit card fraud/cGAN_fraud_5904.pkl'
cGAN_fraud = pd.read_pickle(file_name)

file_name = '2) synthetic data generation/WGAN/credit card fraud/WGAN_fraud_5904.pkl'
WGAN_fraud = pd.read_pickle(file_name)

file_name = '2) synthetic data generation/WcGAN/credit card fraud/WcGAN results/WcGAN_fraud_5904_Adam.pkl'
WcGAN_fraud = pd.read_pickle(file_name)

file_name = '2) synthetic data generation/tGAN/credit card fraud/tGAN_fraud_5000.pkl'
tGAN_fraud = pd.read_pickle(file_name)


####################### functions ######################################


def get_data(real_data, synthetic_data, nr_normal_training, nr_fraud_training, nr_synthetic_fraud_training, test_size):

    train_data, test_data, train_labels, test_labels = \
        train_test_split(real_data, real_data['class'], test_size=test_size, random_state=1)

    # even out the data set -> 1:1 ratio of 0 and 1 classes
    data_training = train_data.sample(frac=1)  # shuffle
    data_testing = test_data.sample(frac=1) # shuffle

    fraud_data_training = data_training.loc[data_training['class'] == 1][:nr_fraud_training]
    fraud_data_testing = data_testing.loc[data_testing['class'] == 1]

    non_fraud_data_training = data_training.loc[data_training['class'] == 0][:nr_normal_training]
    non_fraud_data_testing = data_testing.loc[data_testing['class'] == 0][:len(fraud_data_testing)]

    synthetic_data = synthetic_data.sample(frac=1)
    synthetic_fraud = synthetic_data.loc[synthetic_data['class']==1][:nr_synthetic_fraud_training]

    fraud_data_training = pd.concat([fraud_data_training,synthetic_fraud])

    even_data_training = pd.concat([fraud_data_training, non_fraud_data_training])
    even_data_testing = pd.concat([fraud_data_testing, non_fraud_data_testing])

    even_data_training = even_data_training.sample(frac=1, random_state=42)
    even_data_testing = even_data_testing.sample(frac=1, random_state=42)

    train_data = even_data_training.drop('class', axis=1)
    test_data = even_data_testing.drop('class', axis=1)
    train_labels = even_data_training['class']
    test_labels = even_data_testing['class']

    return train_data, test_data, train_labels, test_labels


def get_forest_model(real_data=real_data, synthetic_data=GAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='rf', nr_normal_training=213224, nr_fraud_training=0, nr_synthetic_fraud_training=0,
                     test_size=0.25):

    X_train, X_test, y_train, y_test = get_data(real_data, synthetic_data, nr_normal_training, nr_fraud_training,
                                                nr_synthetic_fraud_training, test_size)
    optimized_model = RandomForestRegressor(bootstrap=True, max_depth=10, max_features='auto', min_samples_split=20,
                                            n_estimators=100)
    model = optimized_model.fit(X_train, y_train)


    model_name = model_name +'_'+ model_type +'_'+ str(nr_normal_training) + '_'+str(nr_fraud_training) + '_' + \
                 str(nr_synthetic_fraud_training) +'_ts'+ str(test_size) + '.pkl'
    path = '4) performance improvement/credit card fraud/' + folder + '/' + model_name
    with open(path, 'wb') as file:
        pickle.dump(model, file)

    return

####################### get models ######################################


nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=synthpop_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='synthpop', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('synthpop done')

nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=GAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='GAN', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('GAN done')

nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=cGAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='cGAN', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('cGAN done')

nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=WGAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='WGAN', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('WGAN done')

nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=WcGAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='WcGAN', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('WcGAN done')

nr_normal_training = [5381, 5381, 5381, 5381, 5381, 5381, 5381]
nr_fraud_training = [381, 381, 381, 381, 381, 381, 381]
nr_synthetic_fraud_training = [0, 500, 1000, 2000, 3000, 4000, 5000]
for i in range(0, len(nr_normal_training)):
    get_forest_model(real_data=real_data, synthetic_data=tGAN_fraud, folder='real and synthetic/models', model_name='m1',
                     model_type='tGAN', nr_normal_training=nr_normal_training[i], nr_fraud_training=nr_fraud_training[i],
                     nr_synthetic_fraud_training=nr_synthetic_fraud_training[i], test_size=0.25)
print('tGAN done')