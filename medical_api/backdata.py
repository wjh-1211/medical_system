from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app=Flask(__name__)
CORS(app)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "33664399"
DATABASE = "backplotform"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class bakcdata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    request=db.Column(db.Text)
    answer=db.Column(db.Text)
    comment=db.Column(db.Text)
    satisfication=db.Column(db.Integer)
    time = db.Column(db.Text)
    username = db.Column(db.Text)
    
    def __repr__(self):
        return f"<bakcdata {self.id}>"


@app.route('/saverecord',methods=['POST'])
def handledata():
    with app.app_context():
        data = request.json
        print(data)
        new_record = bakcdata(
            request = data['request'],
            answer = data['answer'],
            comment = data['comment'],
            satisfication = data['satisfication'],
            time = data['time'],
            username = data['username']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': '保存成功'}),200
    
@app.route('/getrecord',methods=['GET'])
def getrecord():
    with app.app_context():
        records = bakcdata.query.all()
        records_dict = [{'id': record.id, 'request': record.request, 'answer': record.answer,
                     'time': record.time, 'comment': record.comment, 'satisfication': record.satisfication,
                     'username':record.username}
                    for record in records]
        return jsonify(records_dict)
    
@app.route('/deleterecord',methods=['POST'])
def deleterecord():
    with app.app_context():
        # 为什么需要json，因为post请求的数据往往会在request里，若前端是一个json格式，则调用json，然后通过字典的形式获取相应的值
        # 如果为整型数据，则直接从data项中获取即可
        data = request.json
        recordid = data.get('id')
        record = bakcdata.query.get(recordid)
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message':'删除成功'}),200

if __name__ == '__main__':
    app.run(port=5001)