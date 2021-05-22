import io
from flask import *
from .util import *

main_route = Blueprint('main_route', __name__)


@main_route.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@main_route.route('/', methods=['GET', 'POST'])
def home_func():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        allowed_files = []
        for file in files:
            if file and allowed_file(file.filename):
                allowed_files.append(file)
        pdfname = make_pdf_from_pics(allowed_files)
        flash('Images Converted Successfully!', 'success')
        return redirect(url_for('main_route.result_func', pdfname=pdfname.split('.')[0]))
    return render_template('home.html')


@main_route.route('/about')
def about_func():
    return render_template('about.html', title='About')


@main_route.route('/result/<string:pdfname>')
def result_func(pdfname: str):
    if not pdfname:
        abort(403)
    try:
        size = os.stat(path=os.path.join(current_app.root_path, Config.RESULT_FOLDER, pdfname + '.pdf')).st_size
        size = format_size(size)
    except:
        size = 'NA'
    return render_template('result.html', title='Result', pdfname=pdfname, size=size)


@main_route.route('/download/<string:filename>', methods=['GET', 'POST'])
def download(filename: str):
    result_path = os.path.join(current_app.root_path, Config.RESULT_FOLDER, filename + '.pdf')
    if not os.path.exists(result_path):
        abort(404)

    return_data = io.BytesIO()
    with open(result_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)

    os.remove(result_path)

    return send_file(
        return_data,
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='RRKA-img2pdf-converted.pdf'
    )
