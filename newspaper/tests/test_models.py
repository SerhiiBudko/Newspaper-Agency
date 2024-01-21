from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Topic, Newspaper


class TopicModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(
            name="test"
        )
        self.assertEqual(
            str(topic),
            f"{topic.name}"
        )


class RedactorModelTests(TestCase):
    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="test_username",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username}: {redactor.first_name} {redactor.last_name}"
        )

    def test_get_absolute_url(self):
        redactor = get_user_model().objects.create(
            username="test_username"
        )
        url = reverse("newspaper:redactors-detail", kwargs={"pk": redactor.pk})
        self.assertEqual(redactor.get_absolute_url(), url)


class NewspaperModelTests(TestCase):
    def test_newspaper_str(self):
        topic = Topic.objects.create(
            name="testname"
        )
        newspaper = Newspaper.objects.create(
            title="test_title",
            topic=topic
        )
        self.assertEqual(str(newspaper), newspaper.title)
