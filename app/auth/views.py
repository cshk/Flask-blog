from flask import render_template, request, redirect, url_for, flash
from ..models import User
from . import auth
from .forms import LoginForm, RegisterForm
from app import db
from  flask_login import login_user, logout_user, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data, password=form.password.data).first()
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html', title=u'登录', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,name=form.username.data,password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=u'注册', form=form)
