from __future__ import annotations

import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .constants import AUTHOR_NAME_MAX_LENGTH
from .constants import BOOK_IMPRINT_MAX_LENGTH
from .constants import BOOK_INSTANCE_STATUS_HELP_TEXT
from .constants import BOOK_INSTANCE_STATUS_MAX_LENGTH
from .constants import BOOK_INSTANCE_UNIQUE_ID_HELP_TEXT
from .constants import BOOK_ISBN_HELP_TEXT
from .constants import BOOK_ISBN_MAX_LENGTH
from .constants import BOOK_SUMMARY_HELP_TEXT
from .constants import BOOK_SUMMARY_MAX_LENGTH
from .constants import BOOK_TITLE_MAX_LENGTH
from .constants import GENRE_NAME_HELP_TEXT
from .constants import GENRE_NAME_MAX_LENGTH
from .constants import LANGUAGE_NAME_HELP_TEXT
from .constants import LANGUAGE_NAME_MAX_LENGTH
from .constants import LoanStatusEnum


class Genre(models.Model):
    name = models.CharField(
        max_length=GENRE_NAME_MAX_LENGTH,
        help_text=GENRE_NAME_HELP_TEXT,
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=LANGUAGE_NAME_MAX_LENGTH,
        help_text=LANGUAGE_NAME_HELP_TEXT,
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=AUTHOR_NAME_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=BOOK_TITLE_MAX_LENGTH)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=BOOK_SUMMARY_MAX_LENGTH,
        help_text=BOOK_SUMMARY_HELP_TEXT,
    )
    ISBN = models.CharField(
        'ISBN',
        max_length=BOOK_ISBN_MAX_LENGTH,
        unique=True,
        help_text=BOOK_ISBN_HELP_TEXT,
    )
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})


class BookInstance(models.Model):
    uniqueId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=BOOK_INSTANCE_UNIQUE_ID_HELP_TEXT,
    )
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    due_back = models.DateField(null=True, blank=True)
    imprint = models.CharField(max_length=BOOK_IMPRINT_MAX_LENGTH, blank=True)
    status = models.CharField(
        max_length=BOOK_INSTANCE_STATUS_MAX_LENGTH,
        choices=LoanStatusEnum.choices(),
        blank=True,
        default=LoanStatusEnum.MAINTENANCE.value,
        help_text=BOOK_INSTANCE_STATUS_HELP_TEXT,
    )

    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['due_back']
        permissions = (
            ('can_mark_returned', 'Set book as returned'),
        )

    def __str__(self):
        return f"{self.uniqueId} ({self.book.title})"

    @property
    def is_overdue(self):
        return self.due_back and self.status == LoanStatusEnum.ON_LOAN.value
