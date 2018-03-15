from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from . import main
from os import path
from .forms import  PostForm, CommentForm
from app.models import Post, Comment
from app import db
from flask_login import login_required, current_user

@main.route('/')
def index():
    # #显示文章列表
    # posts = Post.query.all()
    #第一页 分页
    page_index = request.args.get('page', 1, type=int)
    #倒序排序文章
    query = Post.query.order_by(Post.created.desc())
    #分页
    pagination = query.paginate(page_index, per_page=20, error_out=False)

    posts = pagination.items

    return render_template(
                           'index.html',
                           title=u'Welcome',
                           posts=posts,
                           pagination=pagination)

@main.route('/about')
def about():
    return render_template('about.html', title=u'Test')

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # 获取文件绝对路径
        basepath = path.abspath(path.dirname(__file__))
        # 文件存放地址
        upload_path = path.join(basepath, 'static/uploads')
        # 保存文件
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


@main.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    #Detail
    post = Post.query.get_or_404(id)
    #评论窗体
    form = CommentForm()
    #保存评论
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if 0 == id:
        #新增
        post = Post(author_id=current_user.id)
    else:
        #修改
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body

    title = u'添加新文章'
    if id > 0:
        title = u'编辑 - {}'.format(post.title)
    return render_template('posts/edit.html',
                           title=title,
                           form = form,
                           post=post)
