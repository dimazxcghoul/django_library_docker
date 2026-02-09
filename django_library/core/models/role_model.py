from django.db import models

class Role(models.Model):
    role_id = models.AutoField(primary_key = True)
    role = models.CharField(max_length=20, unique=True, null=True)

    class Meta():
        db_table = 'role'

    def __str__(self):
        return self.role