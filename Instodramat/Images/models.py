from django.db import models
from django.utils import timezone
from Scripts.RenamePath import RenamePath


# Abstract base for other models
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text_content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Photo(Post):
    rename_path = RenamePath('Photos')
    image = models.ImageField(upload_to=rename_path, blank=False, null=True)

    def get_comments(self):
        return Photo.objects.comments.all().order_by('publish_date')

    """
    override delete method to delete file
    """


class Comment(Post):
    related_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
