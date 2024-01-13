from django.urls import path

from .views import (
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RedactorsListView,
    RedactorsDetailView,
    RedactorsCreateView,
    RedactorUpdateView,
    RedactorsDeleteView,
    assign_redactor_to_newspaper,

)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topics-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topics-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topics-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topics-delete"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspaper/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspaper/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path("redactors/", RedactorsListView.as_view(), name="redactors-list"),
    path("redactors/<int:pk>/", RedactorsDetailView.as_view(), name="redactors-detail"),
    path("redactors/create/", RedactorsCreateView.as_view(), name="redactors-create"),
    path("redactors/<int:pk>/update/", RedactorUpdateView.as_view(), name="redactors-update"),
    path("redactors/<int:pk>/delete/", RedactorsDeleteView.as_view(), name="redactors-delete"),
    path(
        "redactors/<int:pk>/assign/",
        assign_redactor_to_newspaper,
        name="assign-redactor"
    )
]
app_name = "newspaper"
