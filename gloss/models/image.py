"""Represent an image."""

from gloss import config
from random import random
import os


class Image(object):

    UPLOADS_FOLDER = '%s/%s' % (config.get('folder', 'static'), 'image/upload')
    EXT = 'png'

    def __init__(self, fname_or_id=None):
        if fname_or_id:
            if fname_or_id.endswith('.%s' % self.EXT):
                self.fname = fname_or_id
            else:
                self.fname = '%s.%s' % (fname_or_id, self.EXT)
        else:
            self.fname = self.random_filename()

    def remove(self):
        os.remove(self.path)

    @property
    def id_(self):
        return self.fname.replace('.%s' % self.EXT, '')

    def random_filename(self):
        """Generate random filename."""
        return '%s.%s' % (str(random())[2:], self.EXT)

    @property
    def img_tag(self):
        """
        """
        return '<img src="%s" ' \
               'alt="" ' \
               'style="width: 100%%; display: block; ' \
               'margin: 0 auto;"/>' % self.url

    @property
    def url(self):
        return '/image/%s' % self.fname

    @property
    def path(self):
        """
        """
        return '%s/%s' % (self.UPLOADS_FOLDER, self.fname)

    @classmethod
    def get_all_images(cls):
        files = []
        images = []

        # filter(os.path.isfile, os.listdir(search_dir))
        for f in os.listdir(cls.UPLOADS_FOLDER):
            print(f)
            if f.endswith('.%s' % cls.EXT):
                files.append(f)

        # First sort the files so we get a consistent ordering.
        files.sort(key=lambda x: os.path.getmtime(
            os.path.join(cls.UPLOADS_FOLDER, x)
        ))
        files.reverse()
        for f in files:
            image = cls(f)
            images.append(image)

        return images
