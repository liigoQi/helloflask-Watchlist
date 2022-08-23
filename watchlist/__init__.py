# 构造文件

import os 
import sys 

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# 读取系统环境变量 SECRET_KEY 的值，如果没有获取到，则使用 dev
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Permission deny. Please login.'

@login_manager.user_loader 
def load_user(user_id):
    from watchlist.models import User 
    user = User.query.get(int(user_id))
    return user 

@app.context_processor
def inject_user():
    from watchlist.models import User 
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands 

