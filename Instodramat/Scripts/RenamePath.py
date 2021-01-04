from uuid import uuid4
import os
from django.utils.deconstruct import deconstructible


@deconstructible
class RenamePath(object):
    """
    Use only with file Fields in models.

    Set path to upload folder and rename file with uuid4
    """

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)