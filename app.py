from flask import Flask, url_for, render_template
# 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
from markupsafe import escape 

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

app = Flask(__name__)

# register a view function
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)

@app.route('/usr/<name>')
def user_page(name):
    return f'<h2>{escape(name)}</h2>'

@app.route('/test')
def test_url_for():
    # url_for: 生成视图函数对应的 URL
    print(url_for('hello'))
    print(url_for('user_page', name='liigo'))
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面
    # /test?num=2&test=1
    print(url_for('test_url_for', num=2, test=1))
    return 'Test page'