from datetime import datetime
from app import database, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, database.Model):  # 继承UserMixin，默认实现user-login的四个方法
    __tablename__ = 'user'
    bank_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    id = database.Column(database.String(18))
    name = database.Column(database.String(32), index=True)
    phone_number = database.Column(database.String(11), index=True)
    password_hash = database.Column(database.String(128))
    balance = database.Column(database.Float, default=0.0)
    interest = database.Column(database.Float, default=0.0)
    operations = database.relationship('Operation', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<用户#{}: {} {}>'.format(self.bank_id, self.name, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password + self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.id)

    def check_name(self, name):
        return self.name == name

    def check_phone_number(self, phone_number):
        return self.phone_number == phone_number

    def get_id(self):
        return self.bank_id

    def get_operations(self):
        return Operation.query.order_by(Operation.timestamp.desc()).filter_by(user_bank_id=self.bank_id)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Operation(database.Model):
    __tablename__ = 'operation'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    user_bank_id = database.Column(database.String, database.ForeignKey('user.bank_id'))
    money = database.Column(database.Float)
    type = database.Column(database.Integer)  # 1: save, 2: withdraw, 3: interest
    timestamp = database.Column(database.DateTime, index=True)
    op_balance = database.Column(database.Float, default=0.0)

    def get_money(self):
        if self.money < 0:
            return str(self.money)
        else:
            return '+' + str(self.money)

    def __repr__(self):
        return '<操作#{}: {} {}'.format(self.id, self.user_bank_id, self.get_money())
