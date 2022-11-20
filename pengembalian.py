from flask import (render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection

pengembalian = Blueprint('pengembalian', __name__)


@pengembalian.route('/pengembalian')
def show_pengembalian():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from pengembalian"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('pengembalian.html', data=output_json)


@pengembalian.route('/tambah_pengembalian/', methods=['GET', 'POST'])
def tambah_pengembalian():
    db = getMysqlConnection()

    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        petugas = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        anggota = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        tgl_kembali = request.form['tanggal_pengembalian']
        denda = request.form['denda']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO pengembalian (tanggal_pengembalian, denda, id_buku, id_anggota, id_petugas) VALUES('{tgl_kembali}', {denda}, {id_buku}, {id_anggota}, {id_petugas})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('pengembalian.show_pengembalian'))
    return render_template('form_pengembalian.html', buku=buku, anggota=anggota, petugas=petugas)


@pengembalian.route('/update_pengembalian/<int:id_pengembalian>/', methods=['GET', 'POST'])
def update_pengembalian(id_pengembalian):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from pengembalian where id_pengembalian={id_pengembalian}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        petugas = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        anggota = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        tgl_kembali = request.form['tanggal_pengembalian']
        denda = request.form['denda']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']

        if len(tgl_kembali) == 0:
            tgl_kembali = old_data[0][1]
        if len(denda) == 0:
            denda = old_data[0][2]
        if len(id_buku) == 0:
            id_buku = old_data[0][3]
        if len(id_anggota) == 0:
            id_anggota = old_data[0][4]
        if len(id_petugas) == 0:
            id_petugas = old_data[0][5]

        try:
            cur = db.cursor()
            sqlstr = f"update pengembalian set tanggal_pengembalian = '{tgl_kembali}', denda='{denda}', id_buku={id_buku}, id_anggota={id_anggota}, id_petugas={id_petugas} where id_pengembalian={id_pengembalian}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('pengembalian.show_pengembalian'))
    return render_template('update_form_pengembalian.html', data=old_data, buku=buku, anggota=anggota, petugas=petugas)


@pengembalian.route('/delete_pengembalian/<int:id_pengembalian>', methods=['GET', 'POST'])
def delete_pengembalian(id_pengembalian):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from pengembalian where id_pengembalian={id_pengembalian}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('pengembalian.show_pengembalian'))
