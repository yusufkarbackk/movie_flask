from flask import Blueprint, request, render_template, redirect, render_template, url_for
import mysql.connector


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='layar_tancep')


auth = Blueprint('auth', __name__,)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO users (nama, email, password) VALUES('{nama}', '{email}', {password})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index'))
    else:
        return render_template('registration.html')
