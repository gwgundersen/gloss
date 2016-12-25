"""Image uploading- and serving-related pages."""

from flask import Blueprint, request, send_file
import random

from glossary import app, db, models
from glossary.config import config


image_blueprint = Blueprint('image',
                            __name__,
                            url_prefix='%s/image' % config.get('url', 'base'))


UPLOADS_FOLDER = '%s/%s' % (app.static_folder, 'image/upload')


@image_blueprint.route('/<string:fname>', methods=['GET'])
def serve_image(fname):
    """Server all images by hash (randomly generated name)."""
    path = '%s/%s' % (UPLOADS_FOLDER, fname)
    return send_file(path, mimetype='image/png')


@image_blueprint.route('/upload', methods=['POST'])
def upload_image():
    """Uploads an image."""
    f = request.files.get('file')
    fname = random_filename()
    path = '%s/%s' % (UPLOADS_FOLDER, fname)
    f.save(path)
    url = 'image/%s' % fname
    img_html = '<img src="%s" alt="" style="width: 100%%; display: block; ' \
               'margin: 0 auto;"/>' % url
    return img_html


def random_filename():
    """Generate random filename."""
    return '%s.png' % str(random.random())[2:]
