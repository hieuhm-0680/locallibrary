from __future__ import annotations

import uuid

from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter a book genre (e.g. Science Fiction)',
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=100, help_text="Enter the book's language (e.g. English, French)",
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book',
    )
    imprint = models.CharField(max_length=200)
    ISBN = models.CharField(
        'ISBN', max_length=13, unique=True, help_text='13 Character ISBN number',
    )
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True,
    )

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    class LoanStatus(models.TextChoices):
        MAINTENANCE = 'm', ('Maintenance')
        ON_LOAN = 'o', ('On loan')
        AVAILABLE = 'a', ('Available')
        RESERVED = 'r', ('Reserved')

    uniqueId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library',
    )
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=LoanStatus.choices,
        blank=True,
        default=LoanStatus.MAINTENANCE,
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.uniqueId} ({self.book.title})"
