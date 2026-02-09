from django.db import models

class Status(models.Model):
    status_id = models.AutoField(primary_key = True)
    status = models.CharField(max_length=20, unique=True)

    class Meta():
        db_table = 'status'

    def __str__(self):
        return self.status