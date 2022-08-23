# 构造文件

import os 
import sys 

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
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

