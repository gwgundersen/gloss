"""Image uploading- and serving-related pages."""

from flask import Blueprint, request, send_file, render_template, redirect, \
    url_for

from gloss import models
from gloss.config import config


image_blueprint = Blueprint('image',
                            __name__,
                            url_prefix='%s/image' % config.get('url', 'base'))


@image_blueprint.route('/', methods=['GET'])
def render_image_page():
    """
    """
    images = models.Image.get_all_images()
    images = images[:9]
    return render_template('images.html', images=images)


@image_blueprint.route('/all', methods=['GET'])
def render_all_image_page():
    """
    """
    images = models.Image.get_all_images()
    return render_template('images.html', images=images)


@image_blueprint.route('/add', methods=['POST'])
def upload_image():
    """Uploads an image."""
    f = request.files.get('file')
    new_image = models.Image()
    f.save(new_image.path)
    return new_image.img_tag


@image_blueprint.route('/replace/<image_id>', methods=['POST'])
def replace_image(image_id):
    """
    """
    f = request.files.get('file')
    old_image = models.Image(image_id)
    f.save(old_image.path)
    return redirect(url_for('image.render_image_page'))


@image_blueprint.route('/delete/<image_id>', methods=['POST'])
def delete_image(image_id):
    """
    """
    image = models.Image(image_id)
    image.remove()
    return redirect(url_for('image.render_image_page'))


@image_blueprint.route('/<string:fname>', methods=['GET'])
def serve_image(fname):
    """Server all images by hash (randomly generated name)."""
    image = models.Image(fname)
    return send_file(image.path, mimetype='image/png')
