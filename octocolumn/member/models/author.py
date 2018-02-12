from django.db import models


__all__ = (
    'Author',
)


class Author(models.Model):
    author = models.ForeignKey('User', null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    intro = models.CharField(max_length=255,null=True)
    blog = models.CharField(max_length=255,null=True)
