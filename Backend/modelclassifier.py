import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import tree, metrics

from Backend.model import Kmeans


# Read data

def decision_maker(kmeans : Kmeans):
    data = pd.read_csv(r"C:\Users\ASUS\PycharmProjects\fastApiProject\my_data.csv", sep=',')

    data = data.drop(columns=['CLIENT_PROFESSION','CLIENT_TYPE_DEPOSANT'])


    target_col = LabelEncoder()


    data['segment_numeric'] = target_col.fit_transform(data['SEGMENT_PCA'])

    target_association = data[['SEGMENT_PCA', 'segment_numeric']]

    data = data.drop(['SEGMENT_PCA'], axis="columns")

    inputs = data.drop(['segment_numeric'], axis="columns")
    np.nan_to_num(inputs)
    targets = data['segment_numeric']

    # X_train, X_test, Y_train, Y_test = train_test_split(inputs, targets, test_size=0.2, random_state=1)

    model = tree.DecisionTreeClassifier()
    model.fit(inputs, targets)

    Y_pred = model.predict([[kmeans.CLIENT_AGE, kmeans.CLIENT_ENCOURS_ENGAGEMENT, kmeans.CLIENT_MMM,
                             kmeans.CLIENT_NOMBRE_CARTES, kmeans.CLIENT_VRD_MOY, kmeans.TOTAL_PACK]])


    segment= ""

    for i in range(len(target_association['segment_numeric'])):
        if target_association['segment_numeric'][i] == Y_pred[0]:
            segment = target_association['SEGMENT_PCA'][i]
    return segment
