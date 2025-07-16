from __future__ import annotations

from django.shortcuts import render, get_object_or_404
from django.views import generic

from catalog.constants import LoanStatusEnum
from catalog.models import (
    Author,
    Book,
    BookInstance
)


def index(request):
    num_book = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatusEnum.AVAILABLE.code,
    ).count()
    num_authors = Author.objects.count()

    context = {
        'num_book': num_book,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def book_detail_view(request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'catalog/book_detail.html', {'book': book})
