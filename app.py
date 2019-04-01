import os

from flask import Flask, render_template
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin

from core.models import db
from auth.models import User, Role
from auth.helpers import init_security

basedir = os.path.abspath(os.path.dirname(__file__))

security = Security()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wow change me daddy' or os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite') or \
                          os.environ.get('DATABASE_URL')
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['DEBUG'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'whysosalty'

admin = Admin(base_template='admin/master.html', template_mode='bootstrap3')

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, user_datastore)
admin.init_app(app)

# init flask-admin views
from auth.admin import init as init_auth_admin_models
init_auth_admin_models(admin)
from schedule.admin import init as init_schedule_models
init_schedule_models(admin)


@app.before_first_request
def before_first_request():
    init_security(user_datastore)


from core import core as core_blueprint
app.register_blueprint(core_blueprint)
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


@app.route('/')
def index():
    return render_template('modular.html', raised=True)
