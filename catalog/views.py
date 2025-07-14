from __future__ import annotations

from django.shortcuts import render

from catalog.models import (
    Author,
    Book,
    BookInstance
)


def index(request):
    num_book = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact='a',
    ).count()
    num_authors = Author.objects.count()

    context = {
        'num_book': num_book,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'index.html', context=context)
