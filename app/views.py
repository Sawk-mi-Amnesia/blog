#从app模块中即从__init__.py中导入创建的app应用
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from datetime import datetime
from werkzeug.urls import url_parse
from sqlalchemy import or_
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User,Post

#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            # flash('username:{},rememberme:{}'.format(form.username.data, form.remember_me.data))
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(url_for('index'))
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('welcome new user')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(db.desc(Post.timestamp)).all()
    return render_template('index.html', posts=posts)

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(db.desc(Post.timestamp))

    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seem = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('commited')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='personal data edit', form=form)

@app.route('/<index>/detail')
def detail(index):
    post = Post.query.filter_by(id=index).first()
    return render_template('detail.html', title='Detail', post=post)

@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('新博客已提交')
        return redirect(url_for('index'))
    return render_template('write.html', title='Write', form=form)

@app.route('/edit/<post_id>', methods=['GET'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.filter_by(id=post_id).first()
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form, post_id=post.id)

@app.route('/change/<post_id>', methods=['POST'])
@login_required
def change_post(post_id):
    form = PostForm()
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))

@app.route('/delete/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.filter_by(id=post_id).first()
	db.session.delete(post)
	db.session.commit()
	flash("delete post successful!")
	return redirect(url_for('user',username=current_user.username))

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    result = Post.query.filter(or_(Post.title.contains(keyword),
                                    Post.body.contains(keyword))).order_by(
                                    Post.timestamp.desc()).all()
    return render_template('index.html', posts=result)
