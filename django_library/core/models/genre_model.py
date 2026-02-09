from django.db import models

class Genre(models.Model):
    genre_id = models.AutoField(primary_key = True)
    genre = models.CharField(max_length=50)

    class Meta():
        db_table='genre'

    def __str__(self):
        return self.genre