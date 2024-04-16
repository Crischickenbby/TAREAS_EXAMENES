from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 


app = Flask(__name__)

#CONEXION A LA BASE DE DATOS(CUANDO NO HAY CONTRASEÑA NO SE PONE NADA)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

#RUTA NORMAL DONDE SE INICIA LA APLICACION WEB
@app.route('/')
def pagina_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """
    Función para verificar si un correo electrónico y contraseña coinciden con un usuario en la base de datos.

    Args:
        No hay argumentos.

    Returns:
        Redirecciona a la página de inicio ('index') si el usuario existe.
        Muestra un mensaje de error si el usuario no existe.
    """
    if request.method == 'POST':
        # **Obtener los datos del formulario**
        email_login = request.form['email_login']  # Correo electrónico del usuario
        password_login = request.form['password_login']  # Contraseña del usuario

        # **Verificar si el usuario existe en la base de datos**
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", 
                    (email_login, password_login))
        user = cur.fetchone()

        if user:
            # **El usuario existe, redirigir a la página de inicio**
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM crud")
            data = cur.fetchall()
            return render_template('index.html', user=data)

        else:
            # **El usuario no existe, mostrar un mensaje de error**
            cur.close()
            return render_template("login.html")

#RUTA PARA QUE EL USUARIO SE REGISTRE
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (fullname, phone, email, password) VALUES(%s, %s, %s, %s)', 
        (fullname, phone, email, password))#
        mysql.connection.commit()
        cur.close()#BUENA PRACTICA, CERRAR CURSOR LUEGO DE HACER UNA CONSULTA
        return redirect(url_for('pagina_login'))#otra forma de hacer el "return render_template('login.html')" el index es el nombre de la funcion de la principal ruta


#-------------------------------------------------

'''@app.route('/add_user_crud', methods=['POST'])
def add_user_crud():
    if request.method == 'POST':
        Nombres = request.form['Nombres']
        ApellidoP= request.form['Apellido Paterno']
        ApellidoM = request.form['Apellido Materno']
        Numero = request.form['Telefono']
        Area = request.form['Area']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO crud (Nombres, Apellido_paterno, Apellido_Materno, Telefono, Area) VALUES (%s, %s, %s, %s, %s)',
                    (Nombres, ApellidoP, ApellidoM, Numero, Area))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM crud")
        data = cur.fetchall()
        flash('Trabajador agregado correctamente')
        return render_template('index.html', user=data)'''

@app.route('/add_user_crud', methods=['POST'])
def add_user_crud():
    if request.method == 'POST':
        # Obtener datos del formulario
        Nombres = request.form['Nombres']
        ApellidoP = request.form['Apellido Paterno']
        ApellidoM = request.form['Apellido Materno']
        Numero = request.form['Telefono']
        Area = request.form['Area']
        
        # Iniciar cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Ejecutar la consulta para insertar el usuario en la base de datos
        cur.execute('INSERT INTO crud (Nombres, Apellido_paterno, Apellido_Materno, Telefono, Area) VALUES (%s, %s, %s, %s, %s)',
                    (Nombres, ApellidoP, ApellidoM, Numero, Area))
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()
         # Mostrar mensaje de éxito
        flash('Trabajador agregado correctamente')
        cur.close()
        # Obtener todos los usuarios de la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM crud")
        # Obtener los datos de la consulta
        data = cur.fetchall()
        # Cerrar el cursor
        cur.close()
        # Renderizar la plantilla 'index.html' y pasar los datos de los usuarios
        return render_template('index.html', user=data)


@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

@app.route('/index')
def Index():
    return render_template('index.html')

@app.route('/edit/<id>')
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM crud WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edid-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        Nombres = request.form['Nombres']
        ApellidoP = request.form['ApellidoP']
        ApellidoM = request.form['ApellidoM']
        Telefono = request.form['Telefono']
        Area = request.form['Area']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE crud SET Nombres = %s, Apellido_paterno = %s, Apellido_Materno = %s, Telefono = %s, Area = %s WHERE id = %s", (Nombres, ApellidoP, ApellidoM, Telefono, Area))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM crud")
        # Obtener los datos de la consulta
        data = cur.fetchall()
        # Cerrar el cursor
        cur.close()
        flash('Contacto Actualizado')
        return render_template('index.html', user=data)



@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM crud WHERE id = {0}'.format(id))
    mysql.connection.commit()
     # Obtener todos los usuarios de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM crud")
    # Obtener los datos de la consulta
    data = cur.fetchall()
    # Cerrar el cursor
    cur.close()
    flash('Trabajador eliminado exitosamente')
    return render_template('index.html', user=data)


#PARA EJECUTAR LA PLICACION WEB
if __name__ == '__main__':
    app.run(debug=True)
