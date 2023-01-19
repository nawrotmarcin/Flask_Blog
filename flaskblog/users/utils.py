import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskblog import mail
from flaskblog.users.gender import PredictGender


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics', picture_fn)
	output_size = (125, 125)
	img = Image.open(form_picture)
	img.thumbnail(output_size)
	img.save(picture_path)
	return picture_fn


def get_image():
	username = current_user.username
	gender = PredictGender(username).is_male()
	if current_user.image_file == 'default.jpg' and gender:
		return url_for('static', filename=f'images/profile_pics/m-{current_user.image_file}')
	elif current_user.image_file == 'default.jpg' and not gender:
		return url_for('static', filename=f'images/profile_pics/w-{current_user.image_file}')
	else:
		return url_for('static', filename=f'images/profile_pics/{current_user.image_file}')


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				  sender='nawrot_marcin@outlook.com',
				  recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore this email	
	'''
	mail.send(msg)
