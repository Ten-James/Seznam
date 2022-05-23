import random
import numpy as np
import pandas as pd

def Function(x):
    return x * 2 / x**2 + 1


list = []


for i in range(10000):
    x = (random.random()-0.5) * 20
    y = (random.random()-0.5) * 20
    list.append([x,y,1 if y>=Function(x) else 0])

pd.DataFrame(data=list).to_csv("data.csv", index=False)

