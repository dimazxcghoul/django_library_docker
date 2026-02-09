from django.db import models
from core.models.book_model import Book
from core.models.book_copy_condition_model import BookCopyCondition

def get_next_number():
    max_num = BookCopy.objects.aggregate(models.Max('copy_number'))['copy_number__max']
    return (max_num or 0) + 1

class BookCopy(models.Model):
    bookcopy_id = models.AutoField(primary_key = True)
    copy_number = models.IntegerField(default=get_next_number, unique=True)
    is_available = models.BooleanField()
    book = models.ForeignKey(Book,
        on_delete=models.CASCADE,
        db_column='book_id'
        )
    condition = models.ForeignKey(BookCopyCondition,
        on_delete=models.CASCADE,
        db_column='condition_id'
    )

    def __str__(self):
        return f'Книга: {self.book.title}, экземпляр: {self.copy_number}'

    class Meta():
        db_table = 'bookcopy'

