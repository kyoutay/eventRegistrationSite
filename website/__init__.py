from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thunderNuggies reign supreme over seismic toss mosses'
    
    app.config['DEBUG'] = True #false for production
    app.config['TESTING'] = True #false for production
    app.config['MAIL_SERVER'] = 'smtp.zoho.com' #an email service that allows less secure access(gmail doesnt support anymore)
    app.config['MAIL_PORT'] = '587' #email port for mail server
    app.config['MAIL_USERNAME'] = 'extremetossdomination@zohomail.com' #email address
    app.config['MAIL_PASSWORD'] = 'P@ss5039!' #email pw
    app.config['MAIL_USE_TLS'] = True #depending on mail server
    app.config['MAIL_USE_SSL'] = False #depending on mail server
    app.config['MAIL_DEFAULT_SENDER'] = 'extremetossdomination@zohomail.com' 
    
    mail.init_app(app)

    from .views import views
    app.register_blueprint(views,url_prefix="/")

    return app


