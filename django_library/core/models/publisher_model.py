from django.db import models

class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=30)

    class Meta():
        db_table = 'publisher'

    def __str__(self):
        return self.name