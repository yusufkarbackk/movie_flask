from flask import (Flask, render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection

petugas = Blueprint('petugas', __name__)


@petugas.route('/petugas')
def show_petugas():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('petugas.html', data=output_json)


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
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('petugas.show_petugas'))
    return render_template('from_create_petugas.html')


@petugas.route('/update_user/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from anggota where id_anggota={user_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'POST':
        kode_anggota = request.form['kode_anggota']
        nama = request.form['nama']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        telpon = request.form['telpon']
        alamat = request.form['alamat']

        if len(kode_anggota) == 0:
            kode_anggota = old_data[0][1]
        if len(nama) == 0:
            nama = old_data[0][2]
        if len(jk_anggota) == 0:
            jk_anggota = old_data[0][3]
        if len(jurusan_anggota) == 0:
            jurusan_anggota = old_data[0][4]
        if len(telpon) == 0:
            telpon = old_data[0][5]
        if len(alamat) == 0:
            alamat = old_data[0][6]

        try:
            cur = db.cursor()
            sqlstr = f"update anggota set kode_anggota = '{kode_anggota}', nama_anggota='{nama}', jk_anggota='{jk_anggota}', jurusan_anggota='{jurusan_anggota}', no_telepon_anggota='{telpon}', alamat_anggota='{alamat}' where id_anggota={user_id}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('users'))


@petugas.route('/user_form/<int:user_id>')
def user_update_form(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from anggota where id_anggota={user_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('user_update_form.html', data=output_json)


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
