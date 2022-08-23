from watchlist import app, db 
from watchlist.models import User, Movie 
from flask import render_template, request, url_for, redirect, flash 
from flask_login import login_user, login_required, logout_user, current_user
from markupsafe import escape 

@app.route('/home')
@app.route('/', methods=['GET', 'POST'])
# 两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存。
def index():
    # Flask 会在请求触发后把请求信息放到 request 对象里
    # 它包含请求相关的所有信息，比如请求的路径（request.path）、请求的方法（request.method）、表单数据（request.form）、查询字符串（request.args）等等。
    if request.method == 'POST':
        # 如果当前用户未认证
        if not current_user.is_authenticated:
            flash('Permission deny.')
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            # 在用户执行某些动作后，我们通常在页面上显示一个提示消息。最简单的实现就是在视图函数里定义一个包含消息内容的变量，传入模板，然后在模板里渲染显示它。因为这个需求很常用，Flask 内置了相关的函数。其中 flash() 函数用来在视图函数里向模板传递提示消息，get_flashed_messages() 函数则用来在模板中获取提示消息。
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

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

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    # get_or_404(): 它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        movie.title = title 
        movie.year = year 
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('edit', movie_id=movie_id))
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            # 登入用户
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name 
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')