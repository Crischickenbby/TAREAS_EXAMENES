from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 


app = Flask(__name__)

#CONEXION A LA BASE DE DATOS(CUANDO NO HAY CONTRASEÑA NO SE PONE NADA)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'
mysql = MySQL(app)


#RUTA NORMAL DONDE SE INICIA LA APLICACION WEB
@app.route('/')
def index():
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
            return 'Tu correo y contraseña si existen en la base de datos!!!'

        else:
            # **El usuario no existe, mostrar un mensaje de error**
            cur.close()
            return "Error: El correo electrónico o la contraseña no coinciden."


    
#@app.router('/inicio_sesion', methods=['POST'])
#def iniciar_sesion():
 #  if request.method == 'POST':   
   #return ''

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
        return redirect(url_for('index'))#otra forma de hacer el "return render_template('login.html')" el index es el nombre de la funcion de la principal ruta

#PARA EJECUTAR LA PLICACION WEB
if __name__ == '__main__':
    app.run(debug=True)
