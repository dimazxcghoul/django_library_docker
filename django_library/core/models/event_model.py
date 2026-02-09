from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    image = models.TextField()
    date_time = models.CharField(max_length=40)
    title = models.TextField()

    class Meta():
        db_table = 'event'

    def __str__(self):
        return self.title