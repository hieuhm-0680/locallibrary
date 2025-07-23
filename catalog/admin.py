from __future__ import annotations

from django.contrib import admin

from .models import Author
from .models import Book
from .models import BookInstance
from .models import Genre
from .models import Language


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ('title', 'summary', 'ISBN', 'language')
    readonly_fields = ('ISBN',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    list_filter = ('date_of_birth', 'date_of_death')
    search_fields = ('name',)
    date_hierarchy = 'date_of_birth'

    fieldsets = (
        (
            None, {
                'fields': ('name',),
            },
        ),
        (
            'Dates', {
                'fields': ('date_of_birth', 'date_of_death'),
                'classes': ('collapse',),
            },
        ),
    )

    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    fields = ('uniqueId', 'status', 'due_back')
    readonly_fields = ('uniqueId',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language', 'display_genre')
    list_filter = ('author', 'language', 'genre')
    search_fields = ('title', 'author__name', 'ISBN')
    filter_horizontal = ('genre',)

    fieldsets = (
        (
            None, {
                'fields': ('title', 'author'),
            },
        ),
        (
            'Details', {
                'fields': ('summary', 'ISBN', 'language', 'genre'),
            },
        ),
    )

    inlines = [BookInstanceInline]

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])
    display_genre.short_description = 'Genre'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'uniqueId')
    list_filter = ('status', 'due_back', 'book__language', 'borrower')
    search_fields = ('uniqueId', 'book__title', 'borrower__username')
    date_hierarchy = 'due_back'

    fieldsets = (
        (
            None, {
                'fields': ('book', 'uniqueId', 'imprint'),
            },
        ),
        (
            'Availability', {
                'fields': ('status', 'due_back', 'borrower'),
            },
        ),
    )

    readonly_fields = ('uniqueId',)
