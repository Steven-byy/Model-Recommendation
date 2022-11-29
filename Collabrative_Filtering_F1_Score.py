# -*- Coding UTF-8 -*-
# @Time: 2022/11/27 12:56
# @Author: Yiyang Bian
# @File: Collabrative_Filtering_F1_Score.py
from numpy import *
from texttable import Texttable

dataset_Dict = {}
Model_Dict = {}
neighbors = []
cost = 0.0
n = 5


def load_rating_data(data_path):
    """
    load dataset
    :param data_path:
    :return: F1_Score.txt
    """
    with open(data_path, "r") as f:
        data_list = []
        data = f.readlines()
        for each_line in data:
            each_line = each_line.split("\t")
            each_line[0] = each_line[0].replace(")", "").replace("(", "")
            each_line[1] = each_line[1].replace("[", "").replace("]", "")
            data_list.append(each_line)
    f.close()
    with open("F1_Score.txt", "w") as f:
        for data in data_list:
            model_id = data[0].split(",")[0]
            dataset_id = data[0].split(",")[1]
            f1_score = data[1].split(",")[6].strip()
            f.write(dataset_id + "::" + model_id + "::" + f1_score + "\n")
        f.close()


def recommendByDataset(datasetId):
    formatRate()
    n = len(dataset_Dict[datasetId])
    getNearestNeighbor(datasetId, dataset_Dict, Model_Dict)
    getrecommandList()


def getrecommandList():
    recommandDict = {}
    recommandList = []
    for neighbor in neighbors:
        models = dataset_Dict[neighbor[1]]
        for model in models:
            if model[0] in recommandDict:
                recommandDict[model[0]] += neighbor[0]
            else:
                recommandDict[model[0]] = neighbor[0]
    for key in recommandDict:
        recommandList.append([recommandDict[key], key])
    print(recommandList)
    print("___________________")
    recommandList.sort(reverse=True)
    recommandList = recommandList[:n]
    return recommandList


def formatRate():
    with open("F1_Score.txt", "r") as f:
        data = f.readlines()
        for i in data:
            i = i.replace("\n", "")
            temp_list = i.split("::")
            temp = (temp_list[1], temp_list[2])
            if temp_list[0] in dataset_Dict:
                dataset_Dict[temp_list[0]].append(temp)
            else:
                dataset_Dict[temp_list[0]] = [temp]
            if temp_list[1] in Model_Dict:
                Model_Dict[temp_list[1]].append(temp_list[0])
            else:
                Model_Dict[temp_list[1]] = [temp_list[0]]


def getNearestNeighbor(dataset_Id, dataset_Dict, Model_Dict):
    neighbors_in = []
    for i in dataset_Dict[dataset_Id]:
        for j in Model_Dict[i[0]]:
            if j != dataset_Id and j not in neighbors_in:
                neighbors_in.append(j)
    for i in neighbors_in:
        dist = getCost(dataset_Id, i)
        neighbors.append([dist, i])
    # print(neighbors)
    neighbors.sort(reverse=True)
    # print(neighbors)


def getPrecision(datasetId,recommandList):
    dataset = [i[0] for i in dataset_Dict[datasetId]]
    recommand = [i[1] for i in recommandList]
    count = 0.0
    if len(dataset) >= len(recommand):
        for i in recommand:
            if i in dataset:
                count += 1.0
        cost = count / len(recommand)
    else:
        for i in dataset:
            if i in recommand:
                count += 1.0
        cost = count / len(recommand)
    return cost

def formatuserDict(userId, userDict, l):
    user = {}
    for i in userDict[userId]:
        user[i[0]] = [i[1], 0]
    for j in userDict[l]:
        if j[0] not in user:
            user[j[0]] = [0, j[1]]
        else:
            user[j[0]][1] = j[1]
    return user


def getCost(userId, l):
    user = formatuserDict(userId, dataset_Dict, l)
    x = 0.0
    y = 0.0
    z = 0.0
    for k, v in user.items():
        x += float(v[0]) * float(v[0])
        y += float(v[1]) * float(v[1])
        z += float(v[0]) * float(v[1])
    if z == 0.0:
        return 0
    return z / sqrt(x * y)


if __name__ == "__main__":
    recommendByDataset("0")
    recommandList = getrecommandList()
    cost = getPrecision("0",recommandList)
    print(cost)
