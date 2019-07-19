from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Required
from app.models import User

class LoginForm(FlaskForm):

    username = StringField('用户名', validators=[DataRequired(message='input name')])
    password = PasswordField('密码', validators=[DataRequired(message='input password')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    #校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请重新换一个!')
    #校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复了，请重新换一个!')

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='input username')])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

class PostForm(FlaskForm):
	title = TextField('标题', validators = [Required(Length(min =0,max=120))])
	body = TextAreaField('内容', validators = [Length(min = 0, max=1200)])


