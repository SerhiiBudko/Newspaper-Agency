from django.test import TestCase

from newspaper.forms import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    NewspaperSearchForm,
    TopicSearchForm,
    RedactorsSearchForm

)

from newspaper.models import Topic, Redactor


class NewspaperFormTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="name_topic"
        )

        self.redactor = Redactor.objects.create_user(
            username="user1",
            password="password",
            years_of_experience="10"
        )

    def test_newspaper_form_valid(self):
        form_data = {
            "title": "title",
            "content": "test_content",
            "topic": self.topic.id,
            "publishers": [self.redactor.id],
        }

        form = NewspaperForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "title": "",
            "topic": self.topic.id,
            "publishers": [self.redactor.id],
        }

        form = NewspaperForm(data=form_data)

        self.assertFalse(form.is_valid())


class RedactorCreationFormTest(TestCase):
    def test_redactor_creation_form_valid(self):

        form_data = {
            "username": "test_redactor",
            "password1": "test_password",
            "password2": "test_password",
            "years_of_experience": "10",
            "first_name": "test_first",
            "last_name": "test_last",
        }

        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_invalid(self):
        form_data = {
            "username": "",
            "password1": "test_password",
            "password2": "test_password",
            "years_of_experience": "10",
            "first_name": "",
            "last_name": "",
        }

        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class RedactorUpdateFormTest(TestCase):
    def test_redactor_username_form_invalid(self):
        form_data = {
            "username": "username_test"
        }

        form = RedactorUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_username_form_invalid(self):
        form_data = {
            "username": ""
        }

        form = RedactorUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestRedactorsSearchForm(TestCase):
    def test_redactors_search_form_valid(self):
        form_data = {
            "username": "username"
        }

        form = RedactorsSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestNewspaperSearchForm(TestCase):
    def test_newspapers_search_form_valid(self):
        form_data = {
            "title": "title"
        }

        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestTopicSearchForm(TestCase):
    def test_topic_search_form_valid(self):
        form_data = {
            "name": "name"
        }

        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
