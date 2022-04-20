from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'cris'
app.config['MYSQL_PASSWORD'] = 'C1007981420P'
app.config['MYSQL_DB'] = 'flasckcontacts'
mysql = MySQL(app)

#setting
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method =='POST':
        tipe = request.form['tipe']
        plate = request.form['plate']
        time = request.form['time']
        vehicle = request.form['vehicle']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (tipe, plate, time, vehicle ) VALUES (%s, %s, %s, %s)',
        (tipe, plate, time, vehicle))
        mysql.connection.commit()
        flash('Datos agregados correctamente')
        return redirect(url_for("Index"))

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        tipe= request.form['tipe']
        plate= request.form['plate']
        time= request.form['time']
        vehicle= request.form['vehicle']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET tipe = %s, plate = %s, time = %s, vehicle = %s  WHERE id = %s ', (tipe, plate, time, vehicle, id))
        mysql.connection.commit()
        flash('Datos actualizados correctamente')
        return redirect(url_for('Index'))



@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Datos removidos satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug = True)