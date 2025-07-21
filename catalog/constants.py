from __future__ import annotations

from enum import Enum

from django.utils.translation import gettext_lazy as _

# Genre constants
GENRE_NAME_MAX_LENGTH = 200
GENRE_NAME_HELP_TEXT = _('Enter a book genre (e.g. Science Fiction)')

# Language constants
LANGUAGE_NAME_MAX_LENGTH = 100
LANGUAGE_NAME_HELP_TEXT = _("Enter the book's language (e.g. English, French)")

# Author constants
AUTHOR_NAME_MAX_LENGTH = 100

# Book constants
BOOK_TITLE_MAX_LENGTH = 200
BOOK_SUMMARY_MAX_LENGTH = 1000
BOOK_SUMMARY_HELP_TEXT = _('Enter a brief description of the book')
BOOK_IMPRINT_MAX_LENGTH = 200
BOOK_ISBN_MAX_LENGTH = 13
BOOK_ISBN_HELP_TEXT = _('13 Character ISBN number')

# BookInstance constants
BOOK_INSTANCE_STATUS_MAX_LENGTH = 1
BOOK_INSTANCE_UNIQUE_ID_HELP_TEXT = _(
    'Unique ID for this particular book across whole library',
)
BOOK_INSTANCE_STATUS_HELP_TEXT = _('Book availability')

# Pagination constants
BOOKS_PER_PAGE = 10
BORROWED_BOOKS_PER_PAGE = 10


class LoanStatusEnum(Enum):
    MAINTENANCE = ('m', _('Maintenance'))
    ON_LOAN = ('o', _('On loan'))
    AVAILABLE = ('a', _('Available'))
    RESERVED = ('r', _('Reserved'))

    @property
    def code(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]

    @classmethod
    def choices(cls):
        return [(item.code, item.label) for item in cls]
