from flask_mail import Mail


def get_config(app):
    mail = Mail()
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    # Email address used to send the the email to the customers
    app.config['MAIL_USERNAME'] = 'confirmation.abacrops@gmail.com'
    # password of MAIL_PASSWORD
    app.config['MAIL_PASSWORD'] = 'cbct qkqd azml gkxl'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
