from flask import *
from PIL import Image
import os, secrets


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_name)
    i = Image.open(form_picture)
    i.save(picture_path)
    print(current_app.root_path)
    return picture_name
