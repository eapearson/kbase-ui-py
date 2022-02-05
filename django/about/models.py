from django.db import models


# Create your models here.

class About(models.Model):
    version = models.CharField('Release Version', max_length=20)
    git_commit = models.CharField('Git Commit Hash', max_length=40)
    built_at = models.DateTimeField('Built At')
    started_at = models.DateTimeField('Started At')

    def __str__(self):
        return f'version: {self.version}, commit: {self.git_commit}'
