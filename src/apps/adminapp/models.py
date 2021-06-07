from django.db import models


class Url(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=32, default="")
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'urls'
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'
