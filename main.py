from flask import Flask, request, render_template, session, redirect, url_for
import pyodbc
from config import Config
from hash import check_password
from call_sql_quary import call


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/login', methods=['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        hash_pass = call('select [pass_hash] '
                         'from [РГР_ВАДИМ].[dbo].[Operator] '
                         'where [login] = ?', [username], commit=False, fetchall=False)

        if check_password(password, hash_pass[0]):
            operator = call('select * '
                            'from [РГР_ВАДИМ].[dbo].[Operator] '
                            'where [login] = ?', [username], commit=False, fetchall=False)
            session['loggedin'] = True
            session['id'] = operator[0]
            session['username'] = operator[1]

            return redirect(url_for('home'))
        else:
            msg = 'Неправильный логин/пароль'

    return render_template('login.html', title='Вход', msg=msg)


@app.route('/', methods=['GET'])
def home():
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('home.html',
                                   title='Главная',
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))


@app.route('/managers', methods=['GET'])
def managers():
    if 'loggedin' in session:
        if request.method == 'GET':

            managers = call('select *'
                 ' from [РГР_ГЛЕБ].[dbo].[МЕНЕДЖЕР]',
                 commit=False,
                 fetchall=True
                 )

            return render_template('managers.html', managers=managers)

    return redirect(url_for('login'))


@app.route('/free_rooms', methods=['GET'])
def free_rooms():
    if 'loggedin' in session:
        if request.method == 'GET':

            rooms = call("select *"
                         " from [РГР_ГЛЕБ].[dbo].[ГОСТИНИЧНЫЙ_КОМПЛЕКС]"
                         "where [Статус_номера] = 'не занято'",
                         commit=False,
                         fetchall=True)

            county = call("select count(Статус_номера)"
                          " from [РГР_ГЛЕБ].[dbo].[ГОСТИНИЧНЫЙ_КОМПЛЕКС]"
                          "where [Статус_номера] = 'не занято'",
                          commit=False,
                          fetchall=False)

            return render_template('free_rooms.html', rooms=rooms, county=county)

    return redirect(url_for('login'))


@app.route('/clients', methods=['GET'])
def clients():
    if 'loggedin' in session:
        if request.method == 'GET':

            clients = call('select * '
                           'from [РГР_ГЛЕБ].[dbo].[КЛИЕНТ]',
                           commit=False,
                           fetchall=True
                           )

            return render_template('clients.html', title='Клеинты', clients=clients)

    return redirect(url_for('login'))


@app.route('/history_of_service', methods=['GET'])
def history_of_service():
    if 'loggedin' in session:
        if request.method == 'GET':
            history = call('SELECT * from [РГР_ГЛЕБ].[dbo].[ДОГОВОР] inner join'
                           '[РГР_ГЛЕБ].[dbo].[ИСТОРИЯ_ОБСЛУЖИВАНИЯ] on '
                           '[РГР_ГЛЕБ].[dbo].[ДОГОВОР].Номер_договора '
                           '= [РГР_ГЛЕБ].[dbo].[ИСТОРИЯ_ОБСЛУЖИВАНИЯ].[Номер_договора]inner join '
                           'РГР_ГЛЕБ.dbo.ДОП_УСЛУГИ on '
                           '[РГР_ГЛЕБ].[dbo].[ИСТОРИЯ_ОБСЛУЖИВАНИЯ].Номер_услуги = '
                           'РГР_ГЛЕБ.dbo.ДОП_УСЛУГИ.Номер_услуги '
                           'ORDER by [РГР_ГЛЕБ].[dbo].[ДОГОВОР].Дата_заселения DESC',
                           commit=False,
                           fetchall=True)

            return render_template('history_of_service.html',
                                   title='История сервисов',
                                   history=history)

    return redirect(url_for('login'))


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('add_client.html', title='Добавить клиента')

        elif request.method == 'POST':

            surname = request.form['surname']
            name = request.form['name']
            patronomic = request.form['patronomic']
            bank_account = request.form['bank_account']

            max_id_in_db = call('select max([Номер_клиента])'
                                ' FROM [РГР_ГЛЕБ].[dbo].[КЛИЕНТ]',
                                commit=False,
                                fetchall=False)

            cl_id = int(max_id_in_db[0]) + 1

            call('insert into'
                 ' [РГР_ГЛЕБ].[dbo].[КЛИЕНТ] ('
                 '[Номер_клиента], [Фамилия_к], [Имя_к],'
                 '[Отчество_к], [Банковский_счет_к]'
                 ') values (?, ?, ?, ?, ?)',
                 [cl_id, surname, name, patronomic, bank_account],
                 commit=True,
                 fetchall=False
                 )

            return render_template('inf_add_client.html', surname=surname,
                                   name=name, patronomic=patronomic,
                                   title='Клиент добавлен'
                                   )

    return redirect(url_for('login'))


@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('add_company.html',
                                   title='Добавить организацию')

        elif request.method == 'POST':
            name_company = request.form['name_company']
            type_company = request.form['type_company']
            bank_account = request.form['bank_account']

            max_id_db = call('select max([Номер_организации])'
                             ' FROM [РГР_ГЛЕБ].[dbo].[ОРГАНИЗАЦИЯ]',
                             commit=False,
                             fetchall=False
                             )

            company_id = int(max_id_db[0]) + 1

            call('insert into [РГР_ГЛЕБ].[dbo].[ОРГАНИЗАЦИЯ] '
                 '([Номер_организации],'
                 '[Название_орг],'
                 '[Тип_орг],'
                 '[Банковский_счет_о] values'
                 '(?, ?, ?, ?))',
                 [company_id, name_company, type_company,
                  bank_account],
                 commit=True,
                 fetchall=False)

            return render_template('inf_add_company.html',
                                   title='Организация добавлена',
                                   name_company=name_company)

    return redirect(url_for('login'))


@app.route('/add_manager', methods=['GET', 'POST'])
def add_manager():
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('add_manager.html',
                                   title='Добавить менеджера')

        elif request.method == 'POST':
            manager_surname = request.form['manager_surname']
            manager_name = request.form['manager_name']
            manager_patronomic = request.form['manager_patronomic']

            max_id_db = call('select max([Номер_менеджера]) '
                             'FROM [РГР_ГЛЕБ].[dbo].[МЕНЕДЖЕР]',
                             commit=False,
                             fetchall=False)

            manager_id = int(max_id_db) + 1

            call('insert into [РГР_ГЛЕБ].[dbo].[МЕНЕДЖЕР] '
                 '([Номер_менеджера],'
                 '[Фамилия_м],'
                 '[Имя_м],'
                 '[Отчество_м]) values'
                 '(?, ?, ?, ?)',
                 [manager_id, manager_surname, manager_name,
                  manager_patronomic
                  ], commit=True, fetchall=False)

            return render_template('inf_add_manager.html',
                                   title='Менеджер добавлен',
                                   manager_surname=manager_surname,
                                   manager_name=manager_name,
                                   manager_patronomic=manager_patronomic
                                   )

    return redirect(url_for('login'))


@app.route('/add_pact', methods=['GET', 'POST'])
def add_pact():
    if 'loggedin' in session:
        if request.method == 'GET':
            clients = call('select * from [РГР_ГЛЕБ].[dbo].[КЛИЕНТ]', commit=False, fetchall=True)
            companys = call('select * from [РГР_ГЛЕБ].[dbo].[ОРГАНИЗАЦИЯ]', commit=False, fetchall=True)
            managers = call('select * from [РГР_ГЛЕБ].[dbo].[МЕНЕДЖЕР]', commit=False, fetchall=True)
            rooms = call("select *"
                         " from [РГР_ГЛЕБ].[dbo].[ГОСТИНИЧНЫЙ_КОМПЛЕКС]"
                         "where [Статус_номера] = 'не занято'", commit=False, fetchall=True)
            serveces = call('select * from [РГР_ГЛЕБ].[dbo].[ДОП_УСЛУГИ]', commit=False, fetchall=True)

            return render_template('add_pact.html', title='Добавить договор',
                                   clients=clients, companys=companys,
                                   managers=managers, rooms=rooms,
                                   serveces=serveces
                                   )

        elif request.method == 'POST':
            clients = request.form['clients']
            companys = request.form['companys']
            managers = request.form['managers']
            rooms = request.form['rooms']
            serveces = request.form['serveces']
            human_county = request.form['human_county']
            check_in_date = request.form['check_in_date']
            check_out_date = request.form['check_out_date']

            pact_count = call('select count([Номер_договора]) '
                              'from [РГР_ГЛЕБ].[dbo].[ДОГОВОР]',
                              commit=False, fetchall=False)

            pact_count_id = int(pact_count[0]) + 1

            if len(str(pact_count_id)) == 1:
                pact_count_id = f'0{pact_count_id}'



            print(clients, companys, managers,
                  rooms, serveces, human_county,
                  check_in_date, check_out_date
                  )

            print('pact_count_id:' + pact_count_id)
            print('data_for_id:' + str(check_in_date))

            pact_code = f'{pact_count_id}-{str(check_in_date)[2]}{str(check_in_date)[3]}'
            print('pact_code:'+pact_code)




    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
