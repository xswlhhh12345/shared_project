# from flask import Flask
from flask import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)