from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from core.forms import BookForm, LoanForm
from core.models import Event, Book, Genre, Publisher, Loan


# Create your views here.
def index(request):
    events = Event.objects.all().order_by('pk')

    data = {
        'title': 'Главная страница',
        'events': events
    }
    return render(request, 'index.html', context=data)

def books_catalog(request):
    books = Book.objects.all().order_by('pk')

    # Фильтры
    selected_genre = request.GET.get('genre')
    publisher_id = request.GET.get('publisher')
    max_pages = request.GET.get('max_pages')

    # Поиск
    title_book_find = request.GET.get('books_find')

    if title_book_find:
        books = books_find = books.filter(title__unaccent__icontains=title_book_find)
    elif selected_genre:
        books = books.filter(genre_id=selected_genre)
    elif publisher_id:
        books = books.filter(publisher_id=publisher_id)
    elif max_pages:
        books = books.filter(pages__lte=max_pages)

    context = {
        'books': books,
        'genres': Genre.objects.all(),
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'books_catalog.html', context)

@login_required
def control_panel(request):


    return render(request, 'control_panel.html', {'title': 'Панель управления'})

def support(request):
    ...


class LibrarianBaseMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class BookCreateView(LibrarianBaseMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'librarian/book_form.html'
    success_url = '/books/'

class BookUpdateView(LibrarianBaseMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'librarian/book_form.html'
    success_url = '/books/'

class LoanCreateView(LibrarianBaseMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'librarian/loan_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        with transaction.atomic():
            loan = form.save(commit=False)

            if not loan.issue_date:
                loan.issue_date = timezone.now().date()

            if not loan.due_date:
                loan.due_date = loan.issue_date + timedelta(days=14)

            if loan.status.status == 'Завершен':
                loan.book_copy.is_available = True
                if not loan.return_date:
                    loan.return_date = timezone.now().date()
            else:
                loan.book_copy.is_available = False

            loan.book_copy.save()

            loan.save()

            self.object = loan
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(self.get_success_url())

class LoanListView(ListView):
    model = Loan
    template_name = 'librarian/loan_list_form.html'
    context_object_name = 'loans'

class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'librarian/loan_edit_form.html'
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        loan = form.save(commit=False)

        if loan.status.status == 'Завершён':
            loan.book_copy.is_available = True
            loan.book_copy.save()

            if not loan.return_date:
                from django.utils import timezone
                loan.return_date = timezone.now().date()
        else:
            loan.book_copy.is_available = False
            loan.book_copy.save()

        loan.save()

        return super().form_valid(form)
