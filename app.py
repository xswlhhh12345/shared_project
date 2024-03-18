import os
import sys
import click
# from flask import Flask
from flask import *
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

#这两条数据来初始化
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)   #初始化，传入实例app
@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项

#(env) $ flask initdb
#(env) $ flask initdb --drop
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

#(env) $ flask forge
def forge():
    db.create_all()
    name='xswlhhh'
    age='20'
    addr='JNU-T4'
    illness='none'
    gender=1
    user=User(name=name,age=age,addr=addr,illness=illness,gender=gender)
    db.session.add(user)
    db.session.commit()
    click.echo('Done!')

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.String(4))
    addr = db.Column(db.String(64))
    illness = db.Column(db.String(48))
    gender=db.Column(db.Boolean)

#设置上传文件的路径
UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message':'No file part in the request'}),400
    
    file=request.files['file']

    if file.filename == '':
        return jsonify({'message':'No selected file'}),400
    
    if file and allowed_file(file.filename):
        try:
            if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
        except Exception as e:
            return jsonify({'message': 'Failed to create upload directory'}), 500

        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        return jsonify({'message':'File uploaded successfully','filename':filename}),200

    return jsonify({'message': 'An unexpected error occurred'}), 500

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Page not found'}), 404

# 默认进入登录页面
@app.route('/')
def login():
    # 为了方便测试：暂时跳过登录，进入系统首页
    return redirect(url_for("index"))
    # return render_template('login_2.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/test',methods=['GET','POST'])
def test():
    user=User.query.first()
    return render_template('test.html',user=user)

if __name__ == '__main__':
    app.run(debug=True)
    