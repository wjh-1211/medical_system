# -*- coding:utf-8 -*-
import os
import re
import json
import requests
import random
from py2neo import Graph

from nlu.sklearn_Classification.clf_model import CLFModel
from utils.json_utils import dump_user_dialogue_context,load_user_dialogue_context
from config import *
from nlu.bert_intent_recognition.app import bert_intent_recognize
from knowledge_extraction.bilstm_crf.app import medical_ner

graph = Graph("http://localhost:7474", auth=("neo4j", "xb000000"))

clf_model = CLFModel('./nlu/sklearn_Classification/model_file/')

def intent_classifier(text):
    result = bert_intent_recognize(text)
    if result != -1:
        print('intent:',result)
        return result['data']
    else:
        return -1

def slot_recognizer(text):
    result = medical_ner(text)
    if result != -1:
        print('slot:',result['data'])
        return result['data']
    else:
        return -1 
    
def mult_intent_classifier(text):
    result = bert_intent_recognize(text)
    if result != -1:
        print('intent:',result['data']['name'])
        return result['data']['name']
    else:
        return -1

def mult_slot_recognizer(text):
    result = medical_ner(text)
    if result != -1:
        print('slot:',result['data'][0]['entities'])
        return result['data'][0]['entities']
    else:
        return -1 

def entity_link(mention,etype):
    """
    对于识别到的实体mention,如果其不是知识库中的标准称谓
    则对其进行实体链指，将其指向一个唯一实体（待实现）
    """
    return mention

def classifier(text):
    """
    判断是否是闲聊意图，以及是什么类型闲聊
    """
    return clf_model.predict(text)

def neo4j_searcher(cql_list):
    ress = ""
    if isinstance(cql_list,list):#用于检查一个对象是否属于指定的类型或类，此处是用来检查cql_list是否是list的原型对象
        for cql in cql_list:
            rst = []
            data = graph.run(cql).data()
            if not data:
                continue
            for d in data:
                d = list(d.values())
                if isinstance(d[0],list):
                    rst.extend(d[0])
                else:
                    rst.extend(d)
            
            data = "、".join([str(i) for i in rst])
            ress += data+"\n"
    else:
        data = graph.run(cql_list).data()
        if not data:
            return ress
        rst = []
        for d in data:
            d = list(d.values())# 将每个数据项转换为字典的值组成的列表
            if isinstance(d[0],list):
                rst.extend(d[0])
            else:
                rst.extend(d)
        
        data = "、".join([str(i) for i in rst])#将结果列表 rst 中的每个元素转换为字符串，并用逗号连接成一个字符串。
        ress += data
    
    return ress

def semantic_parser(text,user):
    """
    对文本进行解析
    intent = {"name":str,"confidence":float}
    """
    intent_rst = intent_classifier(text)#会获取相应的名称和概率
    slot_rst = slot_recognizer(text)
    if intent_rst==-1 or slot_rst==-1 or intent_rst.get("name")=="其他":
        return semantic_slot.get("unrecognized")

    slot_info = semantic_slot.get(intent_rst.get("name"))

    # 填槽：实际上就是要去调用模型的一个过程，将从用户输入文本中提取的实体或信息填入预定义的槽位中
    slots = slot_info.get("slot_list")#从槽信息中获取槽列表，获取识别的实体疾病。
    print("我要看看你是谁",slots)
    slot_values = {}#创建一个空字典，用于存储槽的值
    for slot in slots:
        slot_values[slot] = None
        for ent_info in slot_rst:
            for e in ent_info["entities"]:
                if slot.lower() == e['type']:
                    slot_values[slot] = entity_link(e['word'],e['type'])

    last_slot_values = load_user_dialogue_context(user)["slot_values"]#将填充完的槽值存入槽信息中。
    
    print('slot_values',slot_values)
    
    for k in slot_values.keys():
        if slot_values[k] is None:
            slot_values[k] = last_slot_values.get(k,None)
        
    slot_info["slot_values"] = slot_values

    # 根据意图强度来确认回复策略
    conf = intent_rst.get("confidence")
    if conf >= intent_threshold_config["accept"]:
        slot_info["intent_strategy"] = "accept"
    elif conf >= intent_threshold_config["deny"]:
        slot_info["intent_strategy"] = "clarify"
    else:
        slot_info["intent_strategy"] = "deny"

    return slot_info


def get_answer(slot_info):
    """
    根据语义槽获取答案回复
    """
    cql_template = slot_info.get("cql_template")#知识图谱查询语句
    reply_template = slot_info.get("reply_template")
    ask_template = slot_info.get("ask_template")
    slot_values = slot_info.get("slot_values")
    strategy = slot_info.get("intent_strategy")

    if not slot_values:
        return slot_info

    if strategy == "accept":
        cql = []
        if isinstance(cql_template,list):
            for cqlt in cql_template:
                cql.append(cqlt.format(**slot_values))
        else:
            cql = cql_template.format(**slot_values)
        answer = neo4j_searcher(cql)
        if not answer:
            slot_info["replay_answer"] = "抱歉，未找到相关结果，请重新提问！"
        else:
            pattern = reply_template.format(**slot_values)
            slot_info["replay_answer"] = pattern + answer
    elif strategy == "clarify":
        # 澄清用户是否问该问题
        pattern = ask_template.format(**slot_values)
        slot_info["replay_answer"] = pattern
        # 得到肯定意图之后需要给用户回复的答案
        cql = []
        if isinstance(cql_template,list):
            for cqlt in cql_template:
                cql.append(cqlt.format(**slot_values))
        else:
            cql = cql_template.format(**slot_values)
        answer = neo4j_searcher(cql)
        if not answer:
            slot_info["replay_answer"] = "抱歉，未找到相关结果，请重新提问！"
        else:
            pattern = reply_template.format(**slot_values)
            slot_info["choice_answer"] = pattern + answer
    elif strategy == "deny":
        slot_info["replay_answer"] = slot_info.get("deny_response")
    
    return slot_info

def gossip_robot(intent):
    return random.choice(
                gossip_corpus.get(intent)
            )

def medical_robot(text,user):
    """
    如果确定是诊断意图则使用该方法进行诊断问答
    """
    semantic_slot = semantic_parser(text,user)
    answer = get_answer(semantic_slot)
    return answer

def get_disease_name(text,user):
    
    semantic_slot = semantic_parser(text,user)
    answer = get_answer(semantic_slot)
    print('answer',answer['slot_values'])
    return answer['slot_values']['Disease']

def get_mult_disease(text):
    word_list = []
    intent = ''
    answer = mult_slot_recognizer(text)
    intent = mult_intent_classifier(text)
    for entity in answer:
        word_list.append(entity['word'])
    print('我是wordlist',word_list)
    # 一个数组和一个字符串，应当使用括号返回，相当于向前端传递了一个数组回去
    return (word_list,intent)