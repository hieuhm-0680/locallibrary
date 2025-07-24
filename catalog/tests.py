from __future__ import annotations

import datetime

from django.test import TestCase
from django.urls import reverse

from catalog.forms import RenewBookForm
from catalog.models import Author


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='Test Author',
            date_of_birth=datetime.date(1970, 1, 1),
            date_of_death=datetime.date(2020, 12, 31),
        )

    def test_name_label(self):
        field_label = self.author._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_date_of_birth_label(self):
        field_label = self.author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'date of death')

    def test_name_max_length(self):
        max_length = self.author._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_date_of_birth_null_and_blank(self):
        date_of_birth_field = self.author._meta.get_field('date_of_birth')
        self.assertTrue(date_of_birth_field.null)
        self.assertTrue(date_of_birth_field.blank)

    def test_date_of_death_null_and_blank(self):
        date_of_death_field = self.author._meta.get_field('date_of_death')
        self.assertTrue(date_of_death_field.null)
        self.assertTrue(date_of_death_field.blank)

    def test_object_name_is_author_name(self):
        expected_object_name = self.author.name
        self.assertEqual(str(self.author), expected_object_name)

    def test_get_absolute_url(self):
        expected_url = f'/catalog/author/{self.author.pk}/'
        actual_url = self.author.get_absolute_url()
        self.assertTrue(actual_url.endswith(expected_url))

    def test_author_creation_with_minimal_data(self):
        minimal_author = Author.objects.create(name='Minimal Author')
        self.assertEqual(minimal_author.name, 'Minimal Author')
        self.assertIsNone(minimal_author.date_of_birth)
        self.assertIsNone(minimal_author.date_of_death)

    def test_author_creation_with_all_fields(self):
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(self.author.date_of_birth, datetime.date(1970, 1, 1))
        self.assertEqual(
            self.author.date_of_death,
            datetime.date(2020, 12, 31),
        )


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'Renewal date',
        )

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            'Enter a date between now and 4 weeks (default 3 weeks).',
        )

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + \
            datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max_valid(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_in_valid_range(self):
        date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_clean_renewal_date_past_error_message(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Invalid date - renewal in past',
            form.errors['renewal_date'],
        )

    def test_renew_form_clean_renewal_date_future_error_message(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + \
            datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Invalid date - renewal more than 4 weeks ahead',
            form.errors['renewal_date'],
        )

    def test_renew_form_empty_data(self):
        form = RenewBookForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['renewal_date'])


class AuthorListViewTest(TestCase):
    def setUp(self):
        # Create test authors
        self.author1 = Author.objects.create(
            name='Alice Smith',
            date_of_birth=datetime.date(1980, 1, 1),
        )
        self.author2 = Author.objects.create(
            name='Bob Johnson',
            date_of_birth=datetime.date(1975, 5, 15),
        )
        self.author3 = Author.objects.create(
            name='Charlie Brown',
            date_of_death=datetime.date(2010, 10, 10),
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_context_object_name(self):
        response = self.client.get(reverse('author-list'))
        self.assertTrue('author_list' in response.context)

    def test_all_authors_displayed(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)

        authors_in_context = response.context['author_list']
        self.assertEqual(len(authors_in_context), 3)

        author_names = [author.name for author in authors_in_context]
        self.assertEqual(
            author_names, ['Alice Smith', 'Bob Johnson', 'Charlie Brown'],
        )

    def test_authors_ordered_by_name(self):
        response = self.client.get(reverse('author-list'))
        authors = response.context['author_list']

        # Check ordering
        self.assertEqual(authors[0].name, 'Alice Smith')
        self.assertEqual(authors[1].name, 'Bob Johnson')
        self.assertEqual(authors[2].name, 'Charlie Brown')

    def test_pagination_is_ten(self):
        for i in range(15):
            Author.objects.create(name=f'Author {i:02d}')

        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_second_page(self):
        # Create additional authors to test pagination
        for i in range(15):
            Author.objects.create(name=f'Author {i:02d}')

        response = self.client.get(reverse('author-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        # Should have 8 items on second page
        # (3 original + 15 new = 18 total, 10 on first page)
        self.assertEqual(len(response.context['author_list']), 8)

    def test_view_returns_all_authors_queryset(self):
        response = self.client.get(reverse('author-list'))
        authors_from_view = list(response.context['author_list'])
        authors_from_db = list(
            Author.objects.all().order_by('name'),
        )

        self.assertEqual(authors_from_view, authors_from_db)

    def test_empty_author_list(self):
        # Delete all authors
        Author.objects.all().delete()

        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['author_list']), 0)

    def test_view_context_data(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)

        # Check context keys
        self.assertIn('author_list', response.context)
        self.assertIn('paginator', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('is_paginated', response.context)
