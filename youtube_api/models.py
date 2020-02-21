from django.db import models

# Create your models here.
class Youtube_Search_Api(models.Model):
    search_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    search_video_url = models.URLField()
    duration = models.IntegerField()
    thumbnail = models.URLField()
    date = models.CharField(max_length=100)
    view_count = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Youtube Search Api"
        verbose_name_plural = "Youtube Search Api"


    def __str__(self):
        return self.title

