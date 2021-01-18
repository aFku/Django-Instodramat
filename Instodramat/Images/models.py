from django.db import models
from django.utils import timezone
from Scripts.RenamePath import RenamePath
from django.conf import settings
from os import remove


# Abstract base for other models
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text_content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Photo(Post):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photos', null=True)
    rename_path = RenamePath('Photos')
    image = models.ImageField(upload_to=rename_path, blank=False, null=True)

    def get_comments(self):
        return self.comments.all().order_by('publish_date')

    def delete(self):
        """
        Delete file after deleting model
        """
        super().delete()
        remove(settings.MEDIA_ROOT + '/' + self.image.name)


class Comment(Post):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments')
    related_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
