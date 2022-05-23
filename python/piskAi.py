def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from random import randint
import pandas as pd
from ai import GenerateModel

def place(set, value):
    while True:
        i = randint(0,8)
        if set[i] == 0:
            set[i] = value
            return

def display(set):
    print("\t", end="")
    for i in range(3):
        for j in range(3):
            print('\033[91mX\033[00m' if set[i*3+j] == 1 else ('\033[96mO\033[00m' if set[i*3+j] == 2 else (i *3 + j +1)) , end=" ")
        print("\n\t", end="")

def displaypred(set, predict):
    print("\t", end="")
    for i in range(3):
        for j in range(3):
            if i*3+j == predict:
                print('\033[93mX\033[00m' if set[i*3+j] == 1 else ('\033[93mO\033[00m' if set[i*3+j] == 2 else ("\033[93m"+str(i *3 + j +1)+"\033[00m")), end=" ")
            else:
                print('\033[91mX\033[00m' if set[i*3+j] == 1 else ('\033[96mO\033[00m' if set[i*3+j] == 2 else (i *3 + j +1)) , end=" ")
        print("\n\t", end="")

def replace(set):
    for i in range(9):
        if set[i]==1:
            set[i] = 2
        elif set[i] == 2:
            set[i]= 1
def isValid(set):
    for i in range(3):
        if set[i]*set[i + 3] *set[i+6] == 8 or set[i]*set[i + 3] *set[i+6] == 1:
            return False
        if set[i*3]*set[i*3+1] *set[i*3+2] == 8 or set[i*3]*set[i*3+1] *set[i*3+2] == 1:
            return False
    if set[0] == set[4] and set[8] == set[4]:
        return False
    if set[2] == set[4] and set[6] == set[4]:
        return False
    return True



dataset = pd.read_csv('data.csv')

model = GenerateModel()

while True:
    set = [0,0,0,0,0,0,0,0,0]
    isCross = 1
    for i in range(randint(0,8)):
        place(set, isCross)
        isCross = 1 + isCross % 2

    if (isCross == 2):
        replace(set)
        isCross = 1 + isCross % 2

    if not isValid(set):
        continue

    predict = int(model.predict([set])[0]) - 1
    print(predict + 1)
    displaypred(set,predict)
    inp = input("\npos")
    if inp== '':
        model.fit([set],[predict])
        continue

    if int(inp) == 0:
        break
    model.fit([set],[inp])
    dataset = pd.concat([dataset,pd.DataFrame({'a':set[0],'b':set[1],'c':set[2],'d':set[3],'e':set[4],'f':set[5],'g':set[6],'h':set[7],'i':set[8],'value':[inp]})])

dataset.to_csv('data.csv', sep=',', index=False)