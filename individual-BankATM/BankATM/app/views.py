from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import application, database
from app.forms import LoginForm, RegisterForm, ForgetPasswordForm, EditPersonalInformationForm, ResetPasswordForm, \
    SaveMoneyForm, WithdrawMoneyForm, UserOperationsForm
from app.models import User, Operation
from config import Config


@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', title='Home')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 用户已经登录
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # 收到表单
        user = User.query.filter_by(id=form.id.data).first()
        # 处理登录信息错误
        if user is None or not user.check_password(form.password.data):
            if user is None:
                flash_string = '该身份证号尚未注册'
            else:
                flash_string = '密码错误'
            flash(flash_string, category='error')
            return redirect(url_for('login'))
        # 登录信息正确，登录并跳转
        login_user(user)
        flash('已登录', category='message')
        return redirect(url_for('user', bank_id=user.bank_id))
    return render_template('login.html', title='登录', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(id=form.id.data, name=form.name.data, phone_number=form.phone_number.data)
        user.set_password(form.password1.data)
        database.session.add(user)
        database.session.commit()
        flash('注册成功！请登录！', category='message')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@application.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        print(user, user.check_name(form.name.data), user.check_phone_number(form.phone_number))
        if user is None or not user.check_name(form.name.data) or not user.check_phone_number(form.phone_number.data):
            flash('输入信息有误，请仔细检查！', category='error')
            return redirect(url_for('forget_password'))
        flash('密码已通过短信发送至您的手机，请注意查收，成功登录后请及时删除！', category='message')
        return redirect(url_for('login'))
    return render_template('forget_password.html', title='忘记密码', form=form)


@application.route('/user/<int:bank_id>')
@login_required
def user(bank_id):
    user = User.query.filter_by(bank_id=bank_id).first_or_404()
    # print(user)
    return render_template('user.html', user=user)


@application.route('/user_operations/<int:page>', methods=['GET', 'POST'])
@login_required
def user_operations(page=1):
    # form = UserOperationsForm()
    # if form.validate_on_submit():
    #     print(form.duration.data)
    #     operations = current_user.get_operations().paginate(page, Config.OPERATIONS_PER_PAGE, False)
    #     for operation in operations.items:
    #         operation.timestamp = operation.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    #     next_url = url_for('user_operations', page=operations.next_num) if operations.has_next else None
    #     prev_url = url_for('user_operations', page=operations.prev_num) if operations.has_prev else None
    #     return redirect(url_for('user_operations', page=page,
    #                             operations=operations.items, next_url=next_url, prev_url=prev_url))
    # print(page)
    # print(form)
    # return render_template('user_operations.html', page=page, form=form)

    operations = current_user.get_operations().paginate(page, Config.OPERATIONS_PER_PAGE, False)
    for operation in operations.items:
        operation.timestamp = operation.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    next_url = url_for('user_operations', page=operations.next_num) if operations.has_next else None
    prev_url = url_for('user_operations', page=operations.prev_num) if operations.has_prev else None
    return render_template('user_operations.html', page=page, operations=operations.items,
                           next_url=next_url, prev_url=prev_url)


@application.route('/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info():
    form = EditPersonalInformationForm()
    if form.validate_on_submit():
        current_user.phone_number = form.phone_number.data
        database.session.commit()
        flash('信息编辑成功！', category='message')
        return redirect(url_for('user', bank_id=current_user.bank_id))
    elif request.method == 'GET':
        form.phone_number.data = current_user.phone_number
    # print(form)
    return render_template('edit_info.html', title='编辑个人信息', form=form)


@application.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password1.data)
        database.session.commit()
        flash('密码修改成功！请重新登陆！', category='message')
        logout_user()
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='修改密码', form=form)


@application.route('/save_money', methods=['GET', 'POST'])
@login_required
def save_money():
    form = SaveMoneyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(bank_id=current_user.bank_id).first()
        balance = user.balance + form.money.data
        balance = round(balance, 2)
        money = round(float(form.money.data), 2)
        cur_time = datetime.now()
        operation = Operation(type=1, user=current_user, money=money, op_balance=balance, timestamp=cur_time)
        database.session.add(operation)
        user.balance = balance
        database.session.commit()
        flash('已存款 ￥{} '.format("%.2f" % form.money.data), category='message')
        return redirect(url_for('user', bank_id=current_user.bank_id))
    flash('温馨提示：存款金额必须大于0，且为100的整倍数', category='error')
    return render_template('save_money.html', title='取款', form=form)


@application.route('/withdraw_money', methods=['GET', 'POST'])
@login_required
def withdraw_money():
    interest_rate = 0.0035 / 365
    form = WithdrawMoneyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(bank_id=current_user.bank_id).first()
        if form.money.data > user.balance:
            flash('取款金额超过当前余额，请重新输入', category='error')
            return redirect(url_for('withdraw_money'))
        cur_time = datetime.now()
        operations = user.operations.all()
        cur_balance = operations[-1].op_balance - form.money.data
        money = round(float(form.money.data), 2)
        operation1 = Operation(type=2, user=current_user, money=money * -1,
                               op_balance=round(cur_balance, 2), timestamp=cur_time)
        database.session.add(operation1)

        start = 0
        total_interest = 0
        for i in range(len(operations) - 1, -1, -1):
            if operations[i].money < 0:
                start = i + 1
                initial_balance = operations[i].op_balance
                delta_days = (cur_time - operations[i].timestamp).days
                total_interest += initial_balance * interest_rate * delta_days
                break
        for i in range(start, len(operations)):
            op_money = operations[i].money
            delta_days = (cur_time - operations[i].timestamp).days
            total_interest += op_money * interest_rate * delta_days
        cur_balance += total_interest
        cur_balance = round(cur_balance, 2)
        operation2 = Operation(type=3, user=current_user, money=round(total_interest, 2),
                               op_balance=cur_balance, timestamp=cur_time)
        database.session.add(operation2)

        user.balance += form.money.data * -1 + total_interest
        user.interest += total_interest
        user.balance = round(user.balance, 2)
        user.interest = round(user.interest, 2)
        database.session.commit()
        flash('已取款 ￥{} ，本次累计利息 ￥{}'.format("%.2f" % form.money.data, "%.2f" % total_interest),
              category='message')
        return redirect(url_for('user', bank_id=current_user.bank_id))
    flash('温馨提示：取款金额必须大于0，且为100的整倍数', category='error')
    return render_template('withdraw_money.html', title='存款', form=form)


@application.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_error(error):
    database.session.rollback()
    return render_template('500.html'), 500

