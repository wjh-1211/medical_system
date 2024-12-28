from flask_cors import CORS
from flask import Flask, request, jsonify

from modules import gossip_robot,medical_robot,classifier,get_disease_name,get_mult_disease
from utils.json_utils import dump_user_dialogue_context,load_user_dialogue_context

app = Flask(__name__)
CORS(app)

"""
问答流程：
1、用户输入文本
2、对文本进行解析得到语义结构信息
3、根据语义结构去查找知识,返回给用户

对文本进行解析的流程：
1、意图理解
    闲聊意图：问好、离开、肯定、拒绝
        问好、离开：需要有回复动作
        肯定、拒绝：需要执行动作
    诊断意图：
        当意图置信度达到一定阈值时(>=0.8)，可以查询该意图下的答案
        当意图置信度较低时(0.4~0.8)，按最高置信度的意图查找答案，询问用户是否问的这个问题
        当意图置信度更低时(<0.4)，拒绝回答
2、槽位填充
    如果输入是一个诊断意图，那么就需要语义槽的填充，得到结构化语义

"""


@app.route('/index',methods=['GET'])
def index():
    diseasename = []
    msg = request.args.get('sent')
    user_intent = classifier(msg)
    if user_intent in ["greet","goodbye","deny","isbot"]:
        reply = gossip_robot(user_intent)
    elif user_intent == "accept":
        reply = load_user_dialogue_context('wjh')
        reply = reply.get("choice_answer")
    else:
        reply = medical_robot(msg , 'wjh')#reply就是槽位模板，里面有已经填充好的模板信息
        # 用作数据库统计疾病提问的数量
        diseasename = get_disease_name(msg,'wjh')
        if reply["slot_values"]:#如果存在新的疾病实体，那么就需要重新写入日志，用于下一轮对话
            dump_user_dialogue_context('wjh',reply)
        reply = reply.get("replay_answer")
    
    print(reply,diseasename)
    return jsonify({'reply': reply , 'diseasename':diseasename}),200

@app.route('/getmutiword',methods=['GET'])
def getmutiword():
    msg = request.args.get('sent')
    answer = get_mult_disease(msg)
    return jsonify({'mutianswer':answer}),200
    

if __name__ == '__main__':
    app.run()