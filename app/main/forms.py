from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    title = StringField(label=u'标题', validators=[DataRequired()])
    body = PageDownField(label=u'正文', validators=[DataRequired()])
    submit = SubmitField(u'发表')


class CommentForm(FlaskForm):
    body = PageDownField(label=u'评论', validators=[DataRequired()])
    submit = SubmitField(u'发表')