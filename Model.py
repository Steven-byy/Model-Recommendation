# -*- Coding UTF-8 -*-
# @Time: 2022/11/15 17:07
# @Author: Yiyang Bian
# @File: Model.py

# Extract the model structure information from the imported model
from keras.models import load_model


def myprint(s):
    with open('modelsummary.txt', 'a') as f:
        print(s, file=f)


class Model_Processing:
    def __int__(self, model_path, model_name, num_layers, num_total_params, num_trainable_params, num_non_params):
        self.model_path = model_path
        self.model_name = model_name
        self.num_layers = num_layers
        self.num_total_params = num_total_params
        self.num_trainable_params = num_trainable_params
        self.num_non_params = num_non_params

    def getModelInfo(self) -> list:
        summary = []
        model = load_model(self.model_path)
        model.summary(print_fn=lambda x: summary.append(x))
        return summary


def main():
    model = Model_Processing()
    model.model_path = './results/DenseNet121.h5'
    model_sum = model.getModelInfo()
    # print(model_sum)
    num_layers = 0
    for i in model_sum:
        if "None" in i:
            num_layers += 1

    model.num_total_params = model_sum[-4].split(':')[1].strip()
    model.num_trainable_params = model_sum[-3].split(':')[1].strip()
    model.num_non_params = model_sum[-2].split(':')[1].strip()
    model.num_layers = num_layers

    print(model.__dict__)


if __name__ == "__main__":
    main()
