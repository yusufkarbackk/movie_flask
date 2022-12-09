from flask import (Flask, render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection
import urllib.request
import json
from url import BASE_URL
petugas = Blueprint('petugas', __name__)


@petugas.route('/petugas')
def show_petugas():
    url = f"https://{BASE_URL}-139-192-155-189.ap.ngrok.io/perpustakaan/api/petugas/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return render_template('petugas.html', data=dict['results'])


@petugas.route('/tambah_petugas/', methods=['GET', 'POST'])
def tambah_petugas():
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        telpon = request.form['telfon']
        alamat = request.form['alamat']

        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO petugas (nama_petugas, jabatan_petugas, no_telp_petugas, alamat_petugas) VALUES('{nama}', '{jabatan}', '{telpon}', '{alamat}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('petugas.show_petugas'))
    return render_template('from_create_petugas.html')


@petugas.route('/update_petugas/<int:id_petugas>/', methods=['GET', 'POST'])
def update_petugas(id_petugas):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from petugas where id_petugas={id_petugas}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'POST':
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        telfon = request.form['telfon']
        alamat = request.form['alamat']

        if len(nama) == 0:
            nama = old_data[0][1]
        if len(jabatan) == 0:
            jabatan = old_data[0][2]
        if len(telfon) == 0:
            telfon = old_data[0][3]
        if len(alamat) == 0:
            alamat = old_data[0][4]

        try:
            cur = db.cursor()
            sqlstr = f"update petugas set nama_petugas = '{nama}', jabatan_petugas='{jabatan}', no_telp_petugas='{telfon}' where id_petugas={id_petugas}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('petugas.show_petugas'))
    return render_template('form_update_petugas.html', data=old_data)


@petugas.route('/delete_petugas/<int:id_petugas>', methods=['GET', 'POST'])
def deletePetugas(id_petugas):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from petugas where id_petugas={id_petugas}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('petugas.show_petugas'))
