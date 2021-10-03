from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '<user>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<passwd>'
app.config['MYSQL_DATABASE_DB'] = '<db>'
app.config['MYSQL_DATABASE_HOST'] = '<hostname>'
mysql.init_app(app)
