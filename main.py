from flask import Flask, request, render_template, session, redirect, url_for
import pyodbc
from config import Config
from hash import check_password
from flask_mysqldb import MySQL
import MySQLdb.cursors
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)


def call(quarry, *args, commit, fetchall):

    cur = mysql.connection.cursor()

    cur.execute(quarry, *args)

    if commit:
        cur.close()

        mysql.connection.commit()

        result_of_procedure = None

    else:

        if fetchall:
            result_of_procedure = cur.fetchall()
            cur.close()
        else:
            result_of_procedure = cur.fetchone()
            cur.close()

    return result_of_procedure


@app.route('/login', methods=['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        hash_pass = call('select pass_hash '
                         'from Operator '
                         'where login = %s', [username], commit=False, fetchall=False)

        if check_password(password, hash_pass[0]):
            operator = call('select * '
                            'from Operator '
                            'where login = %s', [username], commit=False, fetchall=False)
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
                 ' from МЕНЕДЖЕР',
                 commit=False,
                 fetchall=True
                 )

            return render_template('managers.html', managers=managers,
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/free_rooms', methods=['GET'])
def free_rooms():
    if 'loggedin' in session:
        if request.method == 'GET':

            rooms = call("select *"
                         " from ГОСТИНИЧНЫЙ_КОМПЛЕКС"
                         " where Статус_номера = 'не занято'",
                         commit=False,
                         fetchall=True)

            county = call("select count(Статус_номера)"
                          " from ГОСТИНИЧНЫЙ_КОМПЛЕКС"
                          " where Статус_номера = 'не занято'",
                          commit=False,
                          fetchall=False)

            return render_template('free_rooms.html', rooms=rooms,
                                   county=county, title='Свободные номера',
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/busy_rooms', methods=['GET'])
def busy_rooms():
    if 'loggedin' in session:
        if request.method == 'GET':
            rooms  = call("select *"
                         " from ГОСТИНИЧНЫЙ_КОМПЛЕКС"
                         " where Статус_номера = 'занято'",
                         commit=False,
                         fetchall=True)

            county = call("select count(Статус_номера)"
                          " from ГОСТИНИЧНЫЙ_КОМПЛЕКС"
                          " where Статус_номера = 'занято'",
                          commit=False,
                          fetchall=False)

            return render_template('busy_rooms.html', rooms=rooms, county=county,
                                   title='Занятые номера', login=session['username'])

    return redirect(url_for('login'))


@app.route('/clients', methods=['GET'])
def clients():
    if 'loggedin' in session:
        if request.method == 'GET':

            clients = call('select * '
                           'from КЛИЕНТ',
                           commit=False,
                           fetchall=True
                           )

            return render_template('clients.html', title='Клеинты', clients=clients,
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/history_of_service', methods=['GET'])
def history_of_service():
    if 'loggedin' in session:
        if request.method == 'GET':
            history = call('SELECT * from ДОГОВОР inner join'
                           ' ИСТОРИЯ_ОБСЛУЖИВАНИЯ on '
                           ' ДОГОВОР.Номер_договора '
                           '= ИСТОРИЯ_ОБСЛУЖИВАНИЯ.Номер_договора inner join '
                           ' ДОП_УСЛУГИ on '
                           ' ИСТОРИЯ_ОБСЛУЖИВАНИЯ.Номер_услуги = '
                           ' ДОП_УСЛУГИ.Номер_услуги '
                           'ORDER by ДОГОВОР.Дата_заселения DESC',
                           commit=False,
                           fetchall=True)

            return render_template('history_of_service.html',
                                   title='История сервисов',
                                   history=history,
                                   login=session['username'])

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

            max_id_in_db = call('select max(Номер_клиента)'
                                ' FROM КЛИЕНТ',
                                commit=False,
                                fetchall=False)

            cl_id = int(max_id_in_db[0]) + 1

            call('insert into'
                 ' КЛИЕНТ ('
                 'Номер_клиента, Фамилия_к, Имя_к,'
                 'Отчество_к, Банковский_счет_к'
                 ') values (%s, %s, %s, %s, %s)',
                 [cl_id, surname, name, patronomic, bank_account],
                 commit=True,
                 fetchall=False
                 )

            return render_template('inf_add_client.html', surname=surname,
                                   name=name, patronomic=patronomic,
                                   title='Клиент добавлен',
                                   login=session['username']
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

            max_id_db = call('select max(Номер_организации)'
                             ' FROM ОРГАНИЗАЦИЯ',
                             commit=False,
                             fetchall=False
                             )

            company_id = int(max_id_db[0]) + 1

            call('insert into ОРГАНИЗАЦИЯ '
                 '(Номер_организации,'
                 'Название_орг,'
                 'Тип_орг,'
                 'Банковский_счет_о) values'
                 '(%s, %s, %s, %s)',
                 [company_id, name_company, type_company,
                  bank_account],
                 commit=True,
                 fetchall=False)

            return render_template('inf_add_company.html',
                                   title='Организация добавлена',
                                   name_company=name_company,
                                   login=session['username'])

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

            max_id_db = call('select max(Номер_менеджера) '
                             'FROM МЕНЕДЖЕР',
                             commit=False,
                             fetchall=False)

            manager_id = int(max_id_db[0]) + 1

            call('insert into МЕНЕДЖЕР '
                 '(Номер_менеджера,'
                 'Фамилия_м,'
                 'Имя_м,'
                 'Отчество_м) values'
                 '(%s, %s, %s, %s)',
                 [manager_id, manager_surname, manager_name,
                  manager_patronomic
                  ], commit=True, fetchall=False)

            return render_template('inf_add_manager.html',
                                   title='Менеджер добавлен',
                                   manager_surname=manager_surname,
                                   manager_name=manager_name,
                                   manager_patronomic=manager_patronomic,
                                   login=session['username']
                                   )

    return redirect(url_for('login'))


@app.route('/add_pact', methods=['GET', 'POST'])
def add_pact():
    if 'loggedin' in session:
        if request.method == 'GET':
            clients = call('select * from КЛИЕНТ', commit=False, fetchall=True)
            companys = call('select * from ОРГАНИЗАЦИЯ', commit=False, fetchall=True)
            managers = call('select * from МЕНЕДЖЕР', commit=False, fetchall=True)
            rooms = call("select *"
                         " from ГОСТИНИЧНЫЙ_КОМПЛЕКС"
                         " where Статус_номера = 'не занято'", commit=False, fetchall=True)
            serveces = call('select * from ДОП_УСЛУГИ', commit=False, fetchall=True)

            return render_template('add_pact.html', title='Добавить договор',
                                   clients=clients, companys=companys,
                                   managers=managers, rooms=rooms,
                                   serveces=serveces,
                                   login=session['username']
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

            pact_count = call('select count(Номер_договора) '
                              'from ДОГОВОР',
                              commit=False, fetchall=False)

            pact_count_id = int(pact_count[0]) + 1

            if len(str(pact_count_id)) == 1:
                pact_count_id = f'0{pact_count_id}'

            pact_code = f'{pact_count_id}-{str(check_in_date)[2]}{str(check_in_date)[3]}'

            rooms = rooms.replace('[', '')
            rooms = rooms.replace(']', '')
            rooms = rooms.replace(' ','')
            rooms = rooms.split(',')
            print(rooms)
            print(rooms[0])
            print(rooms[1])

            call('insert into ДОГОВОР '
                 '(Номер_договора, Номер_организации,'
                 'Номер_клиента, Номер_менеджера,'
                 'Количество_чел, Номер_здания,'
                 'Номер_комнаты, Дата_заселения,'
                 'Дата_выселения) values'
                 '(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                 [pact_code, companys, clients, managers, human_county,
                  rooms[0], rooms[1], check_in_date, check_out_date],
                 commit=True, fetchall=False)

            call('update гостиничный_комплекс set статус_номера = "занято" where номер_здания = %s and Номер_комнаты = %s',
                 [rooms[0], rooms[1]], commit=True, fetchall=False)

            code_service = 1

            if len(serveces) > 0:
                for s in serveces:
                    call("insert into ИСТОРИЯ_ОБСЛУЖИВАНИЯ "
                         "(Номер_договора, Номер_чека, Номер_услуги,"
                         "Статус_оплаты) values (%s, %s, %s, %s)",
                         [pact_code, code_service, s, 'оплачено'], commit=True, fetchall=False)
                    code_service = code_service + 1

            return render_template('inf_add_pact.html', pact_code=pact_code
                                   , title='Договор добавлен',
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/companys')
def companys():
    if 'loggedin' in session:
        if request.method == 'GET':

            companys = call('select * '
                            'from ОРГАНИЗАЦИЯ',
                            commit=False, fetchall=True)

            return render_template('companys.html', title='Организации',
                                   companys=companys, login=session['username'])

    return redirect(url_for('login'))


@app.route('/pacts')
def pacts():
    if 'loggedin' in session:
        if request.method == 'GET':
            pacts = call('SELECT Номер_договора'
                         ',Количество_чел'
                         ',Номер_здания'
                         ',Номер_комнаты'
                         ',Дата_заселения'
                         ',Дата_выселения'
                         ',КЛИЕНТ.Фамилия_к, '
                         'КЛИЕНТ.Имя_к, '
                         'КЛИЕНТ.Отчество_к, '
                         'МЕНЕДЖЕР.Фамилия_м, '
                         'МЕНЕДЖЕР.Имя_м, '
                         'МЕНЕДЖЕР.Отчество_м, '
                         'ОРГАНИЗАЦИЯ.Название_орг '
                         'FROM ДОГОВОР inner join КЛИЕНТ '
                         'on ДОГОВОР.Номер_клиента '
                         ' = КЛИЕНТ.Номер_клиента inner join '
                         ' МЕНЕДЖЕР '
                         'on ДОГОВОР.Номер_менеджера'
                         ' = МЕНЕДЖЕР.Номер_менеджера inner join '
                         ' ОРГАНИЗАЦИЯ'
                         ' on ДОГОВОР.Номер_организации'
                         ' = ОРГАНИЗАЦИЯ.Номер_организации',
                         commit=False,
                         fetchall=True)

            return render_template('pacts.html', title='Договоры', pacts=pacts,
                                   login=session['username'])

    return redirect(url_for('login'))


@app.route('/release_rooms', methods=['GET', 'POST'])
def release_rooms():
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('release_rooms.html', title='Освободить комнату', login=session['username'])

        elif request.method == 'POST':
            building = request.form['building']
            room = request.form['room']

            call(
                'update гостиничный_комплекс set статус_номера = "не занято" where номер_здания = %s and Номер_комнаты = %s',
                [int(building), room], commit=True, fetchall=False)

            return render_template('inf_release_room.html', title='Комната освобождена', building=building, room=room, login=session['username'])

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
