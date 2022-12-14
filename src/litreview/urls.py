"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import reviews_app.views
import authentication.views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", reviews_app.views.home, name="home"),
    path("login/", authentication.views.LoginView.as_view(), name="login"),
    path("logout/", authentication.views.logout, name="logout"),
    path("signup/", authentication.views.SignUpView.as_view(), name="signup"),
    path("ticket_creation/", reviews_app.views.create_ticket, name="ticket_creation"),
    path(
        "review_creation/<int:ticket_id>/",
        reviews_app.views.create_review,
        name="review_creation",
    ),
    path(
        "review_creation_not_in_response_to_a_ticket/",
        reviews_app.views.create_review_not_in_response_to_a_ticket,
        name="review_creation_not_in_response_to_a_ticket",
    ),
    path("posts/", reviews_app.views.posts_view, name="posts"),
    path("ticket/<int:ticket_id>/", reviews_app.views.ticket_edit, name="ticket_edit"),
    path("review/<int:review_id>/", reviews_app.views.review_edit, name="review_edit"),
    path(
        "review/<int:review_id>/delete/",
        reviews_app.views.review_delete,
        name="review_delete",
    ),
    path(
        "ticket/<int:ticket_id>/delete/",
        reviews_app.views.ticket_delete,
        name="ticket_delete",
    ),
    path("subscriptions/", reviews_app.views.subscriptions, name="subscriptions"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
