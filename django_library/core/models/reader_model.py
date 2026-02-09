from django.db import models

class Reader(models.Model):
    reader_id = models.AutoField(primary_key = True)
    ticket_number = models.CharField(max_length=30, unique=True, null=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    place_of_study = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    class Meta():
        db_table = 'reader'

    def __str__(self):
        return self.first_name