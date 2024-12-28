# -*- coding:utf-8 -*-

import os
import pickle
import numpy as np
from sklearn import svm


class CLFModel(object):
    def __init__(self, model_save_path):
        super(CLFModel, self).__init__()
        self.model_save_path = model_save_path
        self.id2label = pickle.load(open(os.path.join(self.model_save_path,'id2label.pkl'),'rb'))
        self.vec = pickle.load(open(os.path.join(self.model_save_path,'vec.pkl'),'rb'))
        self.LR_clf = pickle.load(open(os.path.join(self.model_save_path,'LR.pkl'),'rb'))
        self.gbdt_clf = pickle.load(open(os.path.join(self.model_save_path,'gbdt.pkl'),'rb'))

    def predict(self,text):
        text = ' '.join(list(text.lower()))
        text = self.vec.transform([text])
        proba1 = self.LR_clf.predict_proba(text)# 这一行调用了一个逻辑回归分类器 LR_clf 该方法返回输入文本属于每个类别的概率。
        proba2 = self.gbdt_clf.predict_proba(text)#这一行调用了一个梯度提升决策树分类器 gbdt_clf，同样返回输入文本属于每个类别的概率。
        label = np.argmax((proba1+proba2)/2, axis=1)# 这一行计算了两个分类器预测概率的平均值，并取平均概率最高的索引作为最终的预测结果。np.argmax 函数用于找到数组中最大值的索引。在这里，axis=1 表示在第二个维度上进行计算，即沿着列的方向计算。
        return self.id2label.get(label[0])#最后一行根据最终预测的索引，从标签到 ID 的映射 id2label 中获取对应的标签，并将其返回作为预测结果。

if __name__ == '__main__':
    model = CLFModel('./model_file/')

    text='糖尿病有什么症状'
    label = model.predict(text)
    print(label)