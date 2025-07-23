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

# Form constants
RENEWAL_DATE_LABEL = _('Renewal date')
RENEWAL_DATE_HELP_TEXT = _(
    'Enter a date between now and 4 weeks (default 3 weeks).',
)
RENEWAL_DATE_PAST_ERROR = _('Invalid date - renewal in past')
RENEWAL_DATE_FUTURE_ERROR = _('Invalid date - renewal more than 4 weeks ahead')

# Author constants for templates
AUTHOR_FORM_SUBMIT = _('Submit')
AUTHOR_DELETE_TITLE = _('Delete Author')
AUTHOR_DELETE_CONFIRM = _('Are you sure you want to delete this author?')
AUTHOR_DELETE_WARNING = _(
    'This action cannot be undone. '
    'Deleting this author may affect books that are associated with them.',
)
AUTHOR_DELETE_BUTTON = _('Yes, Delete Author')
AUTHOR_CANCEL_BUTTON = _('Cancel')
AUTHOR_DETAILS_TITLE = _('Author Details')
AUTHOR_BOOKS_TITLE = _('Books by this Author')
AUTHOR_NO_BOOKS = _('No books found for this author.')
AUTHOR_EDIT_BUTTON = _('Edit Author')
AUTHOR_DELETE_BUTTON_DETAIL = _('Delete Author')
AUTHOR_NAME_LABEL = _('Name:')
AUTHOR_DATE_OF_BIRTH_LABEL = _('Date of Birth:')
AUTHOR_DATE_OF_DEATH_LABEL = _('Date of Death:')
AUTHOR_GENRES_LABEL = _('Genres:')
AUTHOR_WARNING_LABEL = _('Warning:')


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
