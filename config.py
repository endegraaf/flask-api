from werkzeug.security import generate_password_hash
from flaskext.mysql import MySQL
from app import app

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'demo'
app.config['MYSQL_DATABASE_PASSWORD'] = 'demo'
app.config['MYSQL_DATABASE_DB'] = 'employees'
app.config['MYSQL_DATABASE_HOST'] = 'macmini.local'

mysql.init_app(app)

users = {
    "demo": generate_password_hash("demo")
}
