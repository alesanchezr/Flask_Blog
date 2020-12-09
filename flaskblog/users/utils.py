
import os
import secrets
import requests
from PIL import Image
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    message = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    
    response = requests.post("https://api.mailgun.net/v3/nailasblog.com/messages",auth=("api", os.getenv("API_KEY")),data={"from": "<mailgun@nailasblog.com>","to": [user.email, "nailasblog.com"],"subject": "Request to reset password","text": message})
    if response.status_code == 200:
        return true
    else:
        print("There has been an error sending the email")
        print(response.data)
        raise Exception("There has been an error sending the email")
