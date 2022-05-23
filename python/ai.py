import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split 




def GenerateModel():
    model = MLPClassifier(hidden_layer_sizes=(9),random_state=1)
    data = pd.read_csv("data.csv")
    X_train, X_test, y_train, y_test =  train_test_split(data.drop(columns=["value"]).values, data["value"].values, stratify=data["value"])

    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(f"Počet chyb: {sum(y_test != pred)}")
    return model


if __name__== "__main__":
    model = GenerateModel()
    print( model)