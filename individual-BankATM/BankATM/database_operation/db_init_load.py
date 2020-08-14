import pandas as pd
from datetime import datetime
from app import database, models


users = models.User.query.all()
for u in users:
    database.session.delete(u)
operations = models.Operation.query.all()
for op in operations:
    database.session.delete(op)
database.session.commit()
user_init = pd.read_csv('BankATM_user_init.csv', encoding='gbk')
for index, row in user_init.iterrows():
    user = models.User(id=row['id'], name=row['name'], phone_number=row['phone_number'],
                       balance=row['balance'], interest=row['interest'])
    user.set_password(row['password'])
    database.session.add(user)
operation_init = pd.read_csv('BankATM_operation_init.csv')
for index, row in operation_init.iterrows():
    operation = models.Operation(user_bank_id=row['user_id'], money=row['money'], type=row['type'],
                                 timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S.%f"),
                                 op_balance=row['op_balance'])
    database.session.add(operation)
database.session.commit()
'''
conn = sqlite3.connect("BankATM.db")
user_init = pd.read_csv('BankATM_user_init.csv', encoding='gbk')
for i in range(len(user_init['password_hash'])):
    user_init.ix[i, 'password_hash'] = generate_password_hash(user_init.ix[i, 'password_hash'])
user_init.to_sql('user', conn, if_exists='replace', index=False)
operation_init = pd.read_csv('BankATM_operation_init.csv')
for i in range(len(operation_init['timestamp'])):
    operation_init.ix[i, 'timestamp'] = datetime.strptime(operation_init.ix[i, 'timestamp'], "%Y-%m-%d %H:%M:%S.%f")
operation_init.to_sql('operation', conn, if_exists='replace', index=False)
'''
'''
if_exits有三个模式：
fail（默认），若表存在，则不输出
replace：若表存在，覆盖原来表里的数据
append：若表存在，将数据写到原表的后面
'''
print('ok')