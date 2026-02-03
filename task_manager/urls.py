from django.urls import include, path

from task_manager.statuses import views as status_views
from task_manager.users import views as user_views

from . import views

urlpatterns = [
    # i18n
    path("i18n/", include("django.conf.urls.i18n")),
    # Index
    path("", views.index, name="index"),
    # Users
    path("users/", user_views.UsersListView.as_view(), name="users_list"),
    path(
        "users/create/", user_views.UserCreateView.as_view(), name="user_create"
    ),
    path(
        "users/<int:pk>/update/",
        user_views.UserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "users/<int:pk>/delete/",
        user_views.UserDeleteView.as_view(),
        name="user_delete",
    ),
    # Auth
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Statuses
    path(
        "statuses/", status_views.StatusListView.as_view(), name="statuses_list"
    ),
    path(
        "statuses/create/",
        status_views.StatusCreateView.as_view(),
        name="status_create",
    ),
    path(
        "statuses/<int:pk>/update/",
        status_views.StatusUpdateView.as_view(),
        name="status_update",
    ),
    path(
        "statuses/<int:pk>/delete/",
        status_views.StatusDeleteView.as_view(),
        name="status_delete",
    ),
    # Tasks
    path("tasks/", include("task_manager.tasks.urls")),
    # Labels
    path("labels/", include("task_manager.labels.urls")),
    # Rollbar test
    path("test-error/", views.test_rollbar_error, name="test_rollbar_error"),
]
