from flask import *
from .config import Config
from PIL import Image
import os, secrets


def save_picture(form_picture):
    upload_folder = os.path.join(current_app.root_path, Config.UPLOAD_FOLDER)
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(upload_folder, picture_name)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_name


def make_pdf_from_pics(files: list):
    upload_folder = os.path.join(current_app.root_path, Config.UPLOAD_FOLDER)
    result_folder = os.path.join(current_app.root_path, Config.RESULT_FOLDER)
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    secure_files = []
    for file in files:
        img = save_picture(file)
        path = os.path.join(upload_folder, img)
        if img.split('.')[-1] == 'png':
            png = Image.open(path)
            png.load()  # required for png.split()
            background = Image.new("RGB", png.size, (255, 255, 255))
            pngLayers = png.split()
            background.paste(png, mask=pngLayers[3] if len(pngLayers) > 3 else None)  # 3 is the alpha channel
            secure_files.append(background)
        else:
            temp = Image.open(path)
            temp.convert()
            secure_files.append(temp)
        os.remove(os.path.join(upload_folder, img))
    pdfname = secrets.token_hex(8) + '.pdf'
    secure_files[0].save(os.path.join(result_folder, pdfname), save_all=True, append_images=secure_files[1:])
    return pdfname


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def format_size(bytes: int):
    if bytes < 1024:
        return f'{bytes} Bytes'
    bytes //= 1024
    if bytes < 1024:
        return f'{bytes} KB'
    bytes //= 1024
    if bytes < 1024:
        return f'{bytes} MB'
    bytes //= 1024
    return f'{bytes} GB'
