from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    migrate.init_app(app, db)
    
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    @app.route('/')
    def hello():
        # user  = User()
        return render_template("index.html")

    @app.route('/about')
    def about():
        return "about World!"

    # @app.route('/cart')
    # def cart():
    #     return render_template("cart.html")

    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     """Login Form"""
    #     if request.method == 'GET':
    #         return render_template('login_rawtest.html')
    #     else:
    #         name = request.form['user_id']
    #         passw = request.form['password']
    #         try:
    #             data = User.query.filter_by(user_id=name, password=passw).first()
    #             if data is not None:
    #                 session['logged_in'] = True
    #                 return redirect(url_for('index'))
    #             else:
    #                 return 'Dont Login'
    #         except:
    #             return "Dont Login"
    #     # email_address = request.args.get('email_address')
    #     # passwd = request.args.get('passwd')
    #     # print(email_address, passwd)

    #     # if email_address == 'dave@gmail.com' and passwd == '111':

    #     #     return_data = {'auth': 'success'}
    #     # else:
    #     #     return_data = {'auth': 'failed'}
    #     # return jsonify(return_data)
    #     # return render_template("login_rawtest.html")


    @app.route('/html_test')
    def hello_html():
        # html file은 templates 폴더에 위치해야 함
        return render_template('login_rawtest.html')

    from .views import control_views
    app.register_blueprint(control_views.test)

    return app