from django.db import models

# Create your models here.

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
