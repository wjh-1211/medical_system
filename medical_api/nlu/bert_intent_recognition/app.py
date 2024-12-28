# -*- coding:utf-8 -*-
import json
import flask
import pickle
import numpy as np
from gevent import pywsgi
import tensorflow as tf 
import keras
from keras.backend.tensorflow_backend import set_session
from bert4keras.backend import keras
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding

from .bert_model import build_bert_model

global graph,model,sess 


config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

class BertIntentModel(object):
    def __init__(self):
        super(BertIntentModel, self).__init__()
        self.dict_path = 'D:/DeskTop/roberta/vocab.txt'
        self.config_path='D:/DeskTop/roberta/bert_config_rbt3.json'
        self.checkpoint_path='D:/DeskTop/roberta/bert_model.ckpt'

        self.label_list = [line.strip() for line in open('D:/DeskTop/medical_system_qa/medical_api/nlu/bert_intent_recognition/label','r',encoding='utf8')]
        self.id2label = {idx:label for idx,label in enumerate(self.label_list)}

        self.tokenizer = Tokenizer(self.dict_path)
        self.model = build_bert_model(self.config_path,self.checkpoint_path,13)
        self.model.load_weights('D:/DeskTop/medical_system_qa/medical_api/nlu/bert_intent_recognition/checkpoint/best_model.weights')

    def predict(self,text):
        token_ids, segment_ids = self.tokenizer.encode(text, maxlen=60)
        proba = self.model.predict([[token_ids], [segment_ids]])#使用训练好的 BERT 模型 model 对输入进行预测
        rst = {l:p for l,p in zip(self.label_list,proba[0])}#创建了一个字典,label_list 是一个标签列表，而 proba[0] 是模型预测的概率结果。
        rst = sorted(rst.items(), key = lambda kv:kv[1],reverse=True)#对字典 rst 中的键值对按照概率值进行排序，从高到低排序。
        name,confidence = rst[0]#这一行获取排序后概率 最高的 标签名称和对应的概率值。
        return {"name":name,"confidence":float(confidence)}


BIM = BertIntentModel()

def bert_intent_recognize(text):
    data = {"success":0}
    result = None
    with graph.as_default():
        set_session(sess)
        result = BIM.predict(text)
    data = {"success": 1, "data": result}
    return data

# if __name__ == '__main__':

    # r = BIM.predict("两上肺炎性病变，是肺结核吗？已经服用消炎药十多天了")
    # r = BIM.predict("请问肺炎的症状有什么？")
    # print(r)
