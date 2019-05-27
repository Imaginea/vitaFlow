#!flask/bin/python
import os

from flask import Flask, flash, render_template, request, redirect
from flask_cors import CORS
from werkzeug import secure_filename

import image_manager

image_manager.GetNewImage.refresh()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.urandom(24)
# TODO: remove below line
print('Print: {}'.format(app.secret_key))

# UPLOAD_FOLDER = "static/data/uploads/"
UPLOAD_FOLDER = "static/data/images/"

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'jpg', 'pdf', 'png'])


def allowed_filename(filename):
    print("Checking file extension validation for {}".format(filename))
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# @app.route('/upload_file/', methods=['GET', 'POST'])
# def page_upload_file():
#     print('--' * 15)
#     if request.method == 'POST':
#         submitted_file = request.files['file']
#         print('--' * 15)
#         if submitted_file and allowed_filename(submitted_file.filename):
#             filename = secure_filename(submitted_file.filename)
#             print('Saving File at {}'.format(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
#             submitted_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('page_upload_file', filename=filename))
#
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload_file/', methods=['GET', 'POST'])
def page_upload_form(filename=None):
    if request.method == 'GET':
        if filename:
            print('printing {}'.format(filename))
        return render_template('demo.html')
    # @app.route('/upload_file/', methods=['POST'])
    # def page_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print('POST')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File(s) successfully uploaded')
            # Run pipeline
            run_pipeline()
            # return redirect('/upload_file', filename=file.filename)
            return redirect('/upload_file/')


def show_uploaded_images():
    from glob import glob
    html_data = ''
    for url in glob(UPLOAD_FOLDER + '*.jpg'):
        filename = url.split('/')[-1]
        html_data += '<li><a href="/{}">{}</a>     <a href="/uploads/{}">ProcessingDetails</a>      </li>   '.format(
            url, filename, filename)
    html_data = "<html><body><ul>{}<ul></body></html>".format(html_data)
    return html_data


@app.route('/uploads/<filename>')
def show_uploaded_image_details(filename):
    import config
    from glob import glob
    image_data = "/{}/{}".format(UPLOAD_FOLDER, filename)
    bin_data = glob(os.path.join(config.BINARIZE_ROOT_DIR, '*' + filename))
    if bin_data:
        bin_data = bin_data[0]
    else:
        bin_data = ''
    text_data = glob(os.path.join(config.TEXT_IMAGES, filename.rsplit('.', 1)[-2] + '/*'))
    text_data.sort()
    text_data_images = sorted([_ for _ in text_data if '.png' in _],
                              key=lambda fn: int(fn.rsplit('/')[-1].split('.')[0]))
    text_data_tesseract = [_ for _ in text_data if '.tesseract' in _]
    text_data_calamari = [_ for _ in text_data if '.pred' in _]
    print(bin_data)
    data = {
        'image_data': image_data,
        'binarisation': bin_data,
        'text2Lines': text_data_images,
        'tesseract': text_data_tesseract,
        'calamari': text_data_calamari
    }
    return render_template('demo_result.html', image_data=image_data, data=data)


@app.route('/uploads/')
def page_show_uploads():
    return show_uploaded_images()


def run_pipeline():
    import subprocess
    # command = ['make', '-f', '../../Makefile', 'help']
    command = 'cd ../.. && make east_ocr_pipeline'.split(' ')
    print(' '.join(command))
    subprocess.check_call(command)

if __name__ == '__main__':
    app.run(debug=True)  # host='172.16.49.198'
