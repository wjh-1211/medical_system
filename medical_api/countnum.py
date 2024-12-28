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

class diseasenum(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    diseasename=db.Column(db.Text)
    num=db.Column(db.Integer)
    
    def __repr__(self):
        return f"<diseasenum {self.id}>"
    
@app.route('/savenum',methods=['POST'])
def savenum():
    with app.app_context():
        data = request.json
        
        frontname = data.get('diseasename')
        # 左边为数据库表项，右边为当前变量
        # 通过查询，这是一个query对象，而不是单一的数据库表对象，因此需要调用first获得一个具体的对象
        existing_disease = diseasenum.query.filter_by(diseasename=frontname).first()
        if existing_disease:
            existing_disease.num += 1
        else:
            new_disease = diseasenum(diseasename=frontname,num=1)
            db.session.add(new_disease)
            
        db.session.commit()
        
    return jsonify({'reply':'保存成功'}),200
        
@app.route('/getnum',methods=['GET'])
def getnum():
    with app.app_context():
        # 这是一个列表
        diseases = diseasenum.query.all()
        disease_dict = [{'id':disease.id,'diseasename':disease.diseasename,'num':disease.num}for disease in diseases]
        return jsonify(disease_dict)
        
        
if __name__ == '__main__':
    app.run(port=5002)