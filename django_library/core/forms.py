from django import forms
from .models import Book, Loan, BookCopy

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['book_copy'].queryset = BookCopy.objects.filter(is_available=True)

            if self.instance.pk:
                self.fields['book_copy'].queryset = BookCopy.objects.filter(
                    models.Q(is_available=True) | models.Q(pk=self.instance.bookcopy.pk)
                )

            self.fields['loan_date'].input_formats = ['%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y']
            self.fields['return_date'].input_formats = ['%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y']