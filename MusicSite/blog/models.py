from django.db import models
from django.utils import timezone


class Singer(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=255)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='songs')
    image = models.CharField(max_length=255, blank=True)
    lyric = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name



class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments') # 外键关联到song模型
    comment_content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
