from werkzeug.security import check_password_hash
import routes
import scrape1

from app import app, auth
from config import users


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


if __name__ == "__main__":
    app.run(debug=True)
