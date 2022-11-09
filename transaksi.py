from flask import Blueprint, request, render_template, redirect, render_template, url_for
import mysql.connector


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='layar_tancep')


transaksi = Blueprint('transaksi', __name__)


@transaksi.route('/transactions')
def show_transaksi():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from transaksi"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('transaksi.html', data=output_json)


@transaksi.route('/update/<int:user_id>', methods=['POST'])
def update(user_id):
    db = getMysqlConnection()
    status = request.form['status']
    if request.method == 'POST':
        try:
            cur = db.cursor()
            sqlstr = f"update transaksi set status = '{status}' where id={user_id}"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('transaksi.show_transaksi'))


@transaksi.route('/transaksi_update_form/<int:user_id>')
def transaksi_update_form(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from transaksi"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('transaksi_update_form.html', data=output_json)
