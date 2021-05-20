from flask import *
from .forms import UploadFilesForm
from .util import *

main_route = Blueprint('main_route', __name__)
files = None


@main_route.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main_route.route('/', methods=['GET', 'POST'])
def home_func():
    if request.form.get('action') == 'preview':
        global files
        files = request.files
        return redirect(url_for('main_route.preview_func'))
    form = UploadFilesForm()
    return render_template('home.html', form=form)


@main_route.route('/preview')
def preview_func():
    if not files:
        abort(403)
    urls = []
    for file in files:
        print(file)
        print(dir(file))
        fname = save_picture(file)
        urls.append(url_for('static', filename='uploads/' + fname))
    return render_template('preview.html', title='Preview', urls=urls)


@main_route.route('/about')
def about_func():
    return render_template('about.html', title='About')


@main_route.route('/result')
def result_func():
    if not files:
        abort(403)
    print('result: args: ', request.args)
    print('result: files: ', request.files)
    return render_template('result.html', title='Result', files=files)
