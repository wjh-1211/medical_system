from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time

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

class loginlist(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    phone = db.Column(db.Text)
    isvalid = db.Column(db.Text)
    lasttime = db.Column(db.Text)
    
    def __repr__(self):
        return f"<loginlist {self.id}>"
    
# 登录实际上是在检索信息
@app.route('/login',methods=['POST'])
def login():
    with app.app_context():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        lasttime = data.get('lasttime')
        
        user = loginlist.query.filter_by(username=username).first()
        if user:
            if user.isvalid == '使用中':
                if user.password == password:
                    user.lasttime = lasttime
                    db.session.commit()
                    return jsonify({'message': '登录成功！'}),200
                else:
                    return jsonify({'message': '密码错误！'}), 401
            else:
                return jsonify({'message':'当前账户被禁用！'}),402
        else:
            return jsonify({'message':'用户不存在'}),401    
        
    
@app.route('/sign',methods=['POST'])
def sign():
    with app.app_context():
        data = request.get_json()
        username = data.get('username')
        
        user = loginlist.query.filter_by(username=username).first()
        if user:
            return jsonify({'message':'用户已存在'}),400
        else:
            new_user = loginlist(
                username = data['username'],
                password = data['password'],
                phone = data['phone'],
                isvalid = "使用中",
                lasttime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message':'注册成功'}),200
        
@app.route('/changestate',methods=['POST'])
def changestate():
    with app.app_context():
        data = request.get_json()
        username = data.get('username')
        state = data.get('state')
    
    user = loginlist.query.filter_by(username=username).first()
    
    if user:
        if state == '使用中':
            user.isvalid = '使用中'
        else:
            user.isvalid = '封禁中'
        db.session.commit()
        return jsonify({'message':'修改成功'}),200
    else:
        return jsonify({'message':'用户不存在'}),400

@app.route('/getuserlist',methods=['GET'])
def getuserlist():
    with app.app_context():
        users = loginlist.query.all()
        user_dict = [{'id':user.id,'username':user.username,'password':user.password,'phone':user.phone,'isvalid':user.isvalid,'lasttime':user.lasttime} 
                     for user in users]
        
        return jsonify(user_dict)
    
@app.route('/deleteuser',methods=['POST'])
def deleteuser():
    with app.app_context():
        data = request.get_json()
        id = data.get('id')
        record = loginlist.query.get(id)
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message':'删除成功'}),200

if __name__ == '__main__':
    app.run(port=5003)