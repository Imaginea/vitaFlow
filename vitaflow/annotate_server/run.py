#!flask/bin/python
import os

from flask import Flask, render_template, jsonify, request

import annotate
import config
import cropper
import image_manager

image_manager.GetNewImage.refresh()

app = Flask(__name__, static_folder='static', static_url_path='/static')

sample_data = {"url": "static/images/NoImage.png",
               "id": "NoImage.png",
               "folder": "collection_01/part_1",
               "annotations": [
                   {"tag": "Eagle", "x": 475, "y": 225, "width": 230.555555554, "height": 438.888888886}
               ]
               }


@app.route('/inc/validateTagsAndRegions', methods=['POST', 'GET'])
def _rest_validate_tags_and_regions():
    form_data = dict(request.form)
    # pprint(form_data)
    if 'sendInfo' in form_data.keys():
        annotate.validate_tags_and_regions(request.form)
    return _rest_get_new_image()


@app.route('/inc/getNewImage', methods=['POST', 'GET'])
@app.route('/inc/getNewImage/<image>', methods=['POST', 'GET'])
def _rest_get_new_image(image=None):
    if image:
        print('\n' + '=' * 54 + image + '\n' + '=' * 54)
        try:
            return jsonify(image_manager.GetNewImage.get_specific_image(image))
        except Exception as err:
            print("==" * 15)
            print(err)
            print(image)
            print(locals())
    image_manager.GetNewImage.refresh()
    return jsonify(image_manager.GetNewImage.get_new_image())
#
# @app.route('/data/<path:path>')
# def _rest_annotate_image(path=''):
#     print('Path is {}'.format(path))
#     return send_file('')


@app.route('/annotate_image')
def annotate_image():
    return render_template('index.html')


@app.route('/')
@app.route('/<image>')
def annotate_image2(image=None):
    if image:
        print('\n' + '-' * 54 + image + '\n' + '-' * 54)
    return render_template('index.html')


@app.route('/review_annotation')
# @app.route('/review_annotation/<image:image>')
def review_annotation():
    return render_template('index.html')


@app.route('/show_completed_images')
def show_completed_images():
    # Get data & show
    # show data nicely
    image_manager.GetNewImage.refresh()
    # print(image_manager.GetNewImage.PendingImages)
    return jsonify(image_manager.GetNewImage.completed_images)


def show_pending_images():
    pass


@app.route('/show_all_images')
def show_all_images():
    return jsonify(image_manager.GetNewImage.completed_images)


@app.route('/summary')
def show_summary():
    # data = jsonify({'completed': image_manager.GetNewImage.completed_images,
    #                 'pending': image_manager.GetNewImage.pending_images,
    #                 'inputs': list(image_manager.GetNewImage.receipt_images.keys()),
    #                 'xml': list(image_manager.GetNewImage.annotated_files.keys())})
    data = list(image_manager.GetNewImage.annotated_files.keys())
    return render_template('summary.html', data=data)


@app.route('/summary/<id>')
def rest_show_summary(id):
    id = 0
    receipt_images = image_manager.GetNewImage.receipt_images
    data_dict = dict([(key, receipt_images[key]) for key in image_manager.GetNewImage.pending_images[id:id + 10]])
    return jsonify({'receipt_images': data_dict})


def login_logout():
    pass


@app.route("/cropper/<image_name>")
def page_cropper(image_name=None):
    data = {'image_name': "/" + os.path.join(config.IMAGE_ROOT_DIR, image_name)}
    return render_template("Cropper_js.html", data=data)


@app.route("/cropper/upload", methods=['POST'])
@app.route("/upload", methods=['POST'])
def cropper_upload():
    data = dict(request.form)
    return cropper.cropper_upload(data)


if __name__ == '__main__':
    app.run(debug=True)
