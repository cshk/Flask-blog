from flask import Flask, request
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_gravatar import Gravatar

basedir = path.dirname(__file__)
bootstarp = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
#保护cookie
login_manager.session_protection='strong'
#指定登录页面
login_manager.login_view='auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)
    bootstarp.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    #头像插件
    Gravatar(app, size=64)
    from .auth import auth as auth_bp
    from .main import main as main_bp

    #注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app


