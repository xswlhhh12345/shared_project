# from flask import Flask
from flask import *

app = Flask(__name__)

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