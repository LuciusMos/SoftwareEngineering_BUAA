from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Regexp, Length
from app.models import User, Operation
from flask_login import current_user

DataRequired_Validator = DataRequired(message='请输入本字段')
ID_Reg_Validator = Regexp('^\d{17}(\d|X|x)$', 0, message='身份证号错误')
PhoneNum_Reg_Validator = Regexp('^\d{11}$', 0, message='手机号格式错误')
Password_MinLen_Validator = Length(min=6, message='密码至少为6位')


def ID_check_Validator(form, field):
    id = field.data
    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    Ti = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
    id_17sum = 0
    for i in range(17):
        id_17sum += int(id[i]) * Wi[i]
    check18 = Ti[id_17sum % 11]
    if id[17] != check18:
        raise ValidationError('身份证号错误')


class LoginForm(FlaskForm):
    id = StringField(u'身份证号', validators=[DataRequired_Validator, ID_Reg_Validator, ID_check_Validator])
    password = PasswordField(u'密码', validators=[DataRequired_Validator])
    submit = SubmitField(u'登录')


def ID_Register_Validator(form, field):
    user = User.query.filter_by(id=field.data).first()
    if user is not None:
        raise ValidationError('身份证号已注册，请登录或更换身份证')


class RegisterForm(FlaskForm):
    id = StringField('身份证号', validators=[DataRequired_Validator, ID_Reg_Validator, ID_Register_Validator,
                                         ID_check_Validator])
    name = StringField('姓名', validators=[DataRequired_Validator])
    phone_number = StringField('手机号', validators=[DataRequired_Validator, PhoneNum_Reg_Validator])
    password1 = PasswordField('密码（至少6位）', validators=[DataRequired_Validator, Password_MinLen_Validator])
    password2 = PasswordField('重复密码', validators=[DataRequired_Validator,
                                                  EqualTo('password1', message='两次密码不一致')])
    submit = SubmitField('注册')

    '''
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user = User.query.filter_by(id=self.id.data).first()
        if user is not None:
            self.id.errors.append('该身份证号已注册，请登录或更换身份证')
            # raise ValidationError('身份证号已注册，请登录或更换身份证')
            return False
        return True
    '''


class EditPersonalInformationForm(FlaskForm):
    # name = StringField('姓名')
    phone_number = StringField('手机号码')
    # password = StringField('Password (Selective)')
    submit = SubmitField('提交')


def Money_100_0_Validator(form, field):
    if field.data % 100 != 0:
        raise ValidationError('金额必须为100的整倍数')
    if field.data == 0:
        raise ValidationError('金额必须大于0')


class SaveMoneyForm(FlaskForm):
    money = IntegerField(u'存款金额', validators=[DataRequired_Validator, Money_100_0_Validator])
    submit = SubmitField(u'存款')


class WithdrawMoneyForm(FlaskForm):
    money = IntegerField(u'取款金额', validators=[DataRequired_Validator, Money_100_0_Validator])
    submit = SubmitField(u'取款')


def Old_Password_Check_Validator(form, field):
    if not current_user.check_password(field.data):
        raise ValidationError('原密码输入错误')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired(), Old_Password_Check_Validator])
    new_password1 = PasswordField('新密码（至少6位）', validators=[DataRequired(), Password_MinLen_Validator])
    new_password2 = PasswordField('重复新密码', validators=[DataRequired(),
                                                       EqualTo('new_password1', message='两次密码不一致')])
    submit = SubmitField('修改密码')


class ForgetPasswordForm(FlaskForm):
    id = StringField('身份证号', validators=[DataRequired_Validator, ID_Reg_Validator, ID_check_Validator])
    name = StringField('姓名', validators=[DataRequired_Validator])
    phone_number = StringField('手机号', validators=[DataRequired_Validator, PhoneNum_Reg_Validator])
    submit = SubmitField('获取密码')


class UserOperationsForm(FlaskForm):
    duration = RadioField('查询时间范围', choices=['全部', '一年内', '六个月内', '一个月内', '一周内'])
    submit = SubmitField('查询')
