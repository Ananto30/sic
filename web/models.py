from django.db import models

from django.utils.timezone import now


class Content(models.Model):
    TAGS = (
        ('Music', 'Music'),
        ('Game', 'Game'),
        ('Religion', 'Religion'),
        ('Nature', 'Nature'),
        ('Soothing', 'Soothing'),
        ('Funny', 'Funny'),
        ('Psychology', 'Psychology'),
    )
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True)
    image = models.CharField(max_length=500)
    note = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=20, choices=TAGS)
    created_at = models.DateTimeField(default=now)
