import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import random
from generatedata import Function

from sklearn.model_selection import train_test_split 




def GenerateModel():
    model = DecisionTreeClassifier()
    data = pd.read_csv("data.csv")
    X_train, X_test, y_train, y_test =  train_test_split(data.drop(columns=["2"]).values, data["2"].values, stratify=data["2"])

    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    return model


if __name__== "__main__":
    model = GenerateModel()
    print( model)

    for point in range(1000):
        x = (random.random()-0.5) * 20
        y = (random.random()-0.5) * 20
        plt.scatter(x, y, color='green' if model.predict([[x,y]])[0] == 1 else 'red',s=2)
    
    x = np.linspace(-10, 10, 100)
    y = Function(x)

    plt.ylim([-10,10])
    plt.plot(x, y)
    plt.show()
