from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length


class LoginForm(FlaskForm):
    username = StringField(label=u'用户名', validators=[DataRequired()])
    password = PasswordField(label=u'密码', validators=[DataRequired()])
    submit = SubmitField(label=u'提交')


class RegisterForm(FlaskForm):

    username = StringField(u'用户名', validators=[DataRequired(),
                                               Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                      u'用户名必须由字母数、字数、下划线或 . 组成')])

    password = PasswordField(u'密码', validators=[DataRequired(),
                                                EqualTo('password2', message=u'密码必须一至')])

    password2 = PasswordField(u'确认密码', validators=[DataRequired()])

    email = StringField(u'邮箱地址', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    submit = SubmitField(u'注册')
