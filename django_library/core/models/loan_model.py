from datetime import datetime

import django.utils.timezone
from django.db import models

from core.models.book_copy import BookCopy
from core.models.loan_status_model import Status
from core.models.reader_model import Reader


class Loan(models.Model):
    loan_id = models.AutoField(primary_key = True)
    issue_date = models.DateField(verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Дата к которой нужно вернуть книгу")
    return_date = models.DateField(verbose_name="Фактическая дата возврата", blank=True, null=True)
    status = models.ForeignKey(Status,
        on_delete=models.CASCADE,
        db_column='status_id',
        verbose_name="Статус")
    reader = models.ForeignKey(Reader,
        on_delete=models.CASCADE,
        db_column='reader_id',
        verbose_name="Читатель")
    book_copy = models.ForeignKey(BookCopy,
        on_delete=models.CASCADE,
        db_column='bookcopy_id',
        verbose_name="Номер экземпляра")

    class Meta():
        db_table = 'loan'

    def __str__(self):
        return (f'ID: {self.loan_id}, '
                f'книга:  {self.book_copy.book.title}, '
                f'дата выдачи: {self.issue_date}, '
                f'дата ожидаемого возврата: {self.due_date}, '
                f'фактическая дата возврата: {self.return_date if self.return_date else '---'}, '
                f'читатель: {self.reader.first_name} {self.reader.last_name} ')

    def delete(self, *args, **kwargs):
        if self.book_copy:
            self.book_copy.is_available = True
            self.book_copy.save()
        super().delete(*args, **kwargs)