# -*- coding:utf-8 -*-
import os
import re
import json

LOGS_DIR = r'D:\DeskTop\medical_system_qa\medical_api\utils\logs'

#实现多轮对话的关键
#将 Python 数据结构转换为 JSON 格式的字符串
def dump_user_dialogue_context(user,data):
    path = os.path.join(LOGS_DIR,'{}.json'.format(str(user)))#则是根据用户标识 user 构建的文件名（以用户标识为名的 JSON 文件）。
    with open(path,'w',encoding='utf8') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4, 
                separators=(', ', ': '),ensure_ascii=False))

def load_user_dialogue_context(user):
    path = os.path.join(LOGS_DIR,'{}.json'.format(str(user)))
    if not os.path.exists(path):
        return {"choice_answer":"非常抱歉，我不理解你的意思。","slot_values":None}
    else:
        with open(path,'r',encoding='utf8') as f:
            data = f.read()
            return json.loads(data)
