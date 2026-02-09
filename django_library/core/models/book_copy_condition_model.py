from django.db import models

class BookCopyCondition(models.Model):
    condition_id = models.AutoField(primary_key = True)
    condition = models.CharField(30, null=True, unique=True)

    def __str__(self):
        return self.condition

    class Meta():
        db_table = 'bookcopycondition'

