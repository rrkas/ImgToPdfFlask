from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadFilesForm(FlaskForm):
    images = FileField(
        'Upload Images',
        render_kw={'multiple': True},
        validators=[
            FileAllowed(['jpg', 'png', 'jpeg']),
            FileRequired(),
        ]
    )


