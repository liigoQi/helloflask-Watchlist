from operator import is_
from flask import Flask, url_for, render_template
# 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
from markupsafe import escape 
from flask_sqlalchemy import SQLAlchemy
import os 
import sys 
import click 

app = Flask(__name__)

# 对于这个变量值，不同的 DBMS 有不同的格式，对于 SQLite 来说，这个值的格式如下：
# sqlite:////数据库文件的绝对地址
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

'''
在flask shell里创建/删除表和数据库文件
>>> from app import db 
>>> db.create_all()
>>> db.drop_all()
'''

# flask initdb
# flask initdb --drop
@app.cli.command() # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    # 生成虚拟数据
    db.create_all()
    name = 'Liigo'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

# register a view function
@app.route('/home')
@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/usr/<name>')
def user_page(name):
    return f'<h2>{escape(name)}</h2>'

@app.route('/test')
def test_url_for():
    # url_for: 传入端点值（视图函数的名称）和参数，它会返回对应的 URL
    print(url_for('hello'))
    print(url_for('user_page', name='liigo'))
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面
    # /test?num=2&test=1
    print(url_for('test_url_for', num=2, test=1))
    return 'Test page'