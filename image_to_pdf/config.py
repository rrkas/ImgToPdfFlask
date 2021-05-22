import secrets


class Config:
    SECRET_KEY = secrets.token_hex(8)
    UPLOAD_FOLDER = 'static/uploads/'
    RESULT_FOLDER = 'static/pdfs/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
