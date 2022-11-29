# -*- Coding UTF-8 -*-
# @Time: 2022/11/25 17:07
# @Author: Yiyang Bian
# @File: Collabrative_Filtering.py

import csv
import numpy as np


# %%
def load_data(file_path):
    """
    Input dataset
    :param file_path: Dataset path
    :return: data matrix
    """
    f = open(file_path, 'r')
    with f:
        reader = csv.reader(f)
        next(reader)
        data = []
        for row in reader:
            data.append(row)
    f.close()
    return np.mat(data)


def cos_sim(x, y):
    """
    Cosine Similarity
    :param x:
    :param y:
    :return: The Cosine Similarity of x and y
    """
    numerator = x * y.T
    denominator = np.sqrt(x * x.T) * np.sqrt(y * y.T)
    return (numerator / denominator)[0, 0]


def similarity(data):
    """
    Compute the Similarity between two lines
    :param data: data matirx
    :return: Similarity
    """

    m = np.shape(data)[0]

    w = np.mat(np.zeros((m, m)))
    for i in range(m):
        for j in range(i, m):
            if j != i:
                w[i, j] = cos_sim(data[i,], data[j,])
                w[j, i] = w[i, j]
            else:
                w[i, j] = 0
    return w


if __name__ == "__main__":
    data = load_data("datasets.csv")
    matrix = similarity(data)
    print(matrix)
