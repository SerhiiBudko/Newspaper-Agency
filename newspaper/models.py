from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.username}: {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("newspaper:redactors-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="newspapers"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
