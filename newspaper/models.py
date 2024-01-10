from django.contrib.auth.models import AbstractUser
from django.db import models


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()

    class Meta:
        ordering = ["username"]
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self) -> str:
        return f"{self.username}: {self.first_name} {self.last_name}"


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="newspapers"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
