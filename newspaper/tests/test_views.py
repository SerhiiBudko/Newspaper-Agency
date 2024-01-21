from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from newspaper.models import Topic, Redactor, Newspaper


URL_TOPIC_LIST = reverse("newspaper:topics-list")
URL_TOPIC_CREATE = reverse("newspaper:topics-create")
URL_NEWSPAPER_LIST = reverse("newspaper:newspaper-list")
URL_REDACTOR_LIST = reverse("newspaper:redactors-list")


class PublicTopicViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_TOPIC_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_all_topics(self):
        Topic.objects.create(
            name="name_topic"
        )
        Topic.objects.create(
            name="name_topic2"
        )
        response = self.client.get(URL_TOPIC_LIST)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(
            list(response.context["topics_list"]),
            list(topics),
        )
        self.assertTemplateUsed(response, "newspaper/topics_list.html")


class TopicSearchTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password"
        )
        self.client.force_login(self.user)

        Topic.objects.create(
            name="Crime"
        )
        Topic.objects.create(
            name="Fantastic"
        )

    def test_search_topics(self):
        url = reverse("newspaper:topics-list")
        response = self.client.get(url, {"name": "Cr"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crime")
        self.assertNotContains(response, "Fantastic")


class TopicCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_topic_create_view(self):
        data = {
            "name": "test_name",
        }
        url = reverse("newspaper:topics-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Topic.objects.filter(name="test_name").exists()
        )
        self.assertRedirects(
            response,
            reverse("newspaper:topics-list")
        )


class TopicUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

        self.topic_test_update = Topic.objects.create(
            name="test_topic_upda"
        )

    def test_topic_update_view(self):
        update_topic = {
            "name": "test_topic_update"
        }
        url = reverse(
            "newspaper:topics-update",
            kwargs={"pk": self.topic_test_update.id}
        )
        response = self.client.post(url, data=update_topic)

        self.assertEqual(response.status_code, 302)

        self.topic_test_update.refresh_from_db()

        self.assertNotEqual(self.topic_test_update.name, "test_topic_upda")
        self.assertEqual(self.topic_test_update.name, "test_topic_update")

        self.assertRedirects(
            response,
            reverse("newspaper:topics-list")
        )


class TopicDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

        self.topic_test_delete = Topic.objects.create(
            name="create_topic_test"
        )

    def test_topic_delete_view(self):
        url = reverse(
            "newspaper:topics-delete",
            kwargs={"pk": self.topic_test_delete.id}
        )
        count_topics_before_delete = Topic.objects.count()
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Topic.objects.count(),
            count_topics_before_delete - 1
        )

        self.assertFalse(
            Topic.objects.filter(
                pk=self.topic_test_delete.id
            ).exists())
        self.assertRedirects(
            response,
            reverse("newspaper:topics-list")
        )


class PublicNewspaperTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_NEWSPAPER_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_all_newspapers(self):
        topic = Topic.objects.create(
            name="test_topic"
        )
        Newspaper.objects.create(
            title="test_title",
            topic=topic
        )

        response = self.client.get(URL_NEWSPAPER_LIST)
        self.assertEqual(response.status_code, 200)
        list_of_newspapers = Newspaper.objects.all()
        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(list_of_newspapers)
        )
        self.assertTemplateUsed(
            response, "newspaper/newspaper_list.html"
        )


class NewspaperSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

        topic_test1 = Topic.objects.create(
            name="test_topic"
        )
        Newspaper.objects.create(
            title="Good_newspaper",
            topic=topic_test1
        )
        topic_test2 = Topic.objects.create(
            name="test_topic2"
        )
        Newspaper.objects.create(
            title="Perfect_magazine",
            topic=topic_test2
        )

    def test_newspapers_search(self):
        url = reverse("newspaper:newspaper-list")
        response = self.client.get(url, {"title": "Good"})
        self.assertContains(response, "Good_newspaper")
        self.assertNotContains(response, "Perfect_magazine")


class PublicRedactorTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_REDACTOR_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )

        self.client.force_login(self.user)

    def test_retrieve_all_redactors(self):
        response = self.client.get(URL_REDACTOR_LIST)
        self.assertEqual(response.status_code, 200)
        redactors = Redactor.objects.all()
        self.assertEqual(
            list(response.context["redactor_list"]),
            list(redactors)
        )
        self.assertTemplateUsed(
            response, "newspaper/redactor_list.html")


class RedactorSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password"
        )
        self.client.force_login(self.user)

        Redactor.objects.create(
            username="Carter_Perez",
            password="test_password1",
            years_of_experience="10"
        )
        Redactor.objects.create(
            username="test_redactor1",
            password="test_password2",
            years_of_experience="20"
        )
        Redactor.objects.create(
            username="redactor_test3",
            password="test_password3",
            years_of_experience="30"
        )

    def test_redactor_search(self):
        url = reverse("newspaper:redactors-list")
        response = self.client.get(url, {"username": "Carter"})
        self.assertContains(response, "Carter_Perez")
        self.assertNotContains(response, "test_redactor1")
        self.assertNotContains(response, "redactor_test3")
