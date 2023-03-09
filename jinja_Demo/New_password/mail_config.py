from flask_mail import Mail, Message

def get_config(app):
	mail = Mail()
	#CONFIGURING THA MAIL PROTOCOL 
	app.config['MAIL_SERVER'] = 'smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	#EMAIL Address used to send the email to the user 
	app.config['MAIL_USERNAME'] = 'confirmation.abacrops@gmail.com'
	# passsword of MAIL_PASSWORD
	app.config['MAIL_PASSWORD'] = 'cbct qkqd azml gkxl'
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail = mail.init_app(app);
	return mail

def send_recovery_key(email, app, Random_key):
	#Configure the flask plataform to use the parameters define in ["get_config"]
	mail = get_config(app)
	message = """ (Max Length)
		################################
		Here is the recovery key to change your password 
		key = {}
	""".format(Random_key)

	msg = Message(
		'Platform Recovery Key',
		body=message,
		sender='confirmation.abacrops@gmail.com',
		recipients=[email])
		
	mail.send(msg)
