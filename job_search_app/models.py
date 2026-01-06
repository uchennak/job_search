from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    company = models.TextField()
    location = models.TextField()
    description = models.TextField()
    apply_link = models.URLField()
    source = models.CharField(max_length=100)
    date_posted = models.DateTimeField(null=True)
    experience_required = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
