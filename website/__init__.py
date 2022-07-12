from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''
    
    app.config['DEBUG'] = True #false for production
    app.config['TESTING'] = True #false for production
    app.config['MAIL_SERVER'] = '' #an email service that allows less secure access(gmail doesnt support anymore)
    app.config['MAIL_PORT'] = '' #email port for mail server
    app.config['MAIL_USERNAME'] = ' #email address
    app.config['MAIL_PASSWORD'] = '' #email pw
    app.config['MAIL_USE_TLS'] = True #depending on mail server
    app.config['MAIL_USE_SSL'] = False #depending on mail server
    app.config['MAIL_DEFAULT_SENDER'] = '' 
    
    mail.init_app(app)

    from .views import views
    app.register_blueprint(views,url_prefix="/")

    return app


