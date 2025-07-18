from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

from catalog.constants import BOOKS_PER_PAGE
from catalog.constants import BORROWED_BOOKS_PER_PAGE
from catalog.constants import LoanStatusEnum
from catalog.models import Author
from catalog.models import Book
from catalog.models import BookInstance


def index(request):
    num_book = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatusEnum.AVAILABLE.code,
    ).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_book': num_book,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = BOOKS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Book.objects.select_related('author').all()


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book_detail.html'

    def get_queryset(self):
        return Book.objects.select_related(
            'author',
            'language',
        ).prefetch_related('genre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_instances = BookInstance.objects.filter(
            book=self.object,
        ).order_by('status', 'due_back')
        context['book_instances'] = book_instances
        context['has_copies'] = book_instances.exists()
        context['LoanStatusEnum'] = LoanStatusEnum
        context['book_genres'] = list(self.object.genre.all())
        context['book_author'] = self.object.author
        context['book_language'] = self.object.language
        return context

    def book_detail_view(request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'catalog/book_detail.html', {'book': book})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    context_object_name = 'bookinstance_list'
    paginate_by = BORROWED_BOOKS_PER_PAGE

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact=LoanStatusEnum.ON_LOAN.code,
        ).order_by('due_back')
