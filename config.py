#create table `rest_emp` ( `id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(255) NOT NULL, `email` varchar(255) NOT NULL,  `phone` varchar(16) DEFAULT NULL, `address` text DEFAULT NULL, PRIMARY KEY(`id`) );
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '<user>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<passwd>'
app.config['MYSQL_DATABASE_DB'] = '<db>'
app.config['MYSQL_DATABASE_HOST'] = '<hostname>'
mysql.init_app(app)
