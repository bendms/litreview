from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import CharField, Value

from authentication.forms import FollowsUserForm
from litreview.settings import MEDIA_ROOT
from . import forms

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from authentication.models import CustomUser, UserFollows
from .models import Ticket, Review
from itertools import chain

# Create your views here.


def get_users_viewable_reviews(request):
    """Return a queryset of reviews that the user can view."""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values(
        "followed_user_id"
    )
    reviews_to_my_tickets = Review.objects.filter(ticket__user_id=request.user.id)
    list_id = [id["followed_user_id"] for id in users_followed]
    list_id.append(request.user.id)
    users_objects = CustomUser.objects.filter(id__in=list_id)
    reviews_users_followed = Review.objects.filter(user__in=users_objects)
    reviews_users_followed = reviews_users_followed | reviews_to_my_tickets
    return reviews_users_followed


def get_users_viewable_tickets(request):
    """Return a queryset of a tickets that the user can view"""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values(
        "followed_user_id"
    )
    list_id = [id["followed_user_id"] for id in users_followed]
    list_id.append(request.user.id)
    users_objects = CustomUser.objects.filter(id__in=list_id)
    tickets_users_followed = Ticket.objects.filter(user__in=users_objects)
    return tickets_users_followed


@login_required(login_url=reverse_lazy("login"))
def home(request):
    """Home page view."""
    username = None
    if request.user.is_authenticated:
        reviews = get_users_viewable_reviews(request)
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
        tickets = get_users_viewable_tickets(request)
        # returns queryset of tickets
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )
        return render(request, "home.html", context={"posts": posts})
    else:
        return render(request, "home.html")


@login_required(login_url=reverse_lazy("login"))
def create_ticket(request):
    """Create a new ticket."""
    if request.method == "POST":
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            ticket_instance = form.save(commit=False)
            ticket_instance.user = request.user
            ticket_instance.image = request.FILES.get("image")
            ticket_instance.save()
            return redirect("home")
    else:
        form = forms.TicketForm()
        request.user = CustomUser.objects.get(id=request.user.id)
        return render(request, "ticket_creation.html", {"form": form})


@login_required(login_url=reverse_lazy("login"))
def create_review_not_in_response_to_a_ticket(request):
    """Create ticket form and review form at the same time and link ticket to review object."""
    user = request.user
    if request.method == "POST":
        form_ticket = forms.TicketForm(request.POST)
        form_review = forms.ReviewForm(
            request.POST
        )  # TODO: Passer le ticket de la requête POST en paramètre ici
        if form_review.is_valid() and form_ticket.is_valid():
            form_review.cleaned_data
            form_ticket.cleaned_data
            ticket_instance, created = Ticket.objects.get_or_create(
                title=form_ticket.cleaned_data["title"],
                description=form_ticket.cleaned_data["description"],
                image=form_ticket.cleaned_data["image"],
                user=user,
            )
            ticket_instance.has_review = True
            ticket_instance.save()

            review_instance = Review(
                ticket=ticket_instance,
                rating=form_review.cleaned_data["rating"],
                headline=form_review.cleaned_data["headline"],
                body=form_review.cleaned_data["body"],
                user=user,
            )
            review_instance.save()
            return redirect("home")
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()
        review_form.ticket = ticket_form
        return render(
            request,
            "review_creation_not_in_response_to_a_ticket.html",
            {"ticket_form": ticket_form, "review_form": review_form},
        )


@login_required(login_url=reverse_lazy("login"))
def create_review(request, ticket_id):
    """Create a new review."""
    ticket_instance = Ticket.objects.get(id=ticket_id)
    user = request.user
    if request.method == "POST":
        form_review = forms.ReviewForm(request.POST)
        if form_review.is_valid():
            form_review.cleaned_data
            review_instance = Review(
                ticket=ticket_instance,
                rating=form_review.cleaned_data["rating"],
                headline=form_review.cleaned_data["headline"],
                body=form_review.cleaned_data["body"],
                user=user,
            )
            review_instance.save()
            ticket_instance.has_review = True
            ticket_instance.save()
            return redirect("home")
    else:
        ticket_instance = Ticket.objects.get(id=ticket_id)
        review_form = forms.ReviewForm()
        review_form.ticket = ticket_instance
        return render(
            request,
            "review_creation.html",
            {"ticket_instance": ticket_instance, "review_form": review_form},
        )


@login_required(login_url=reverse_lazy("login"))
def posts_view(request):
    """View all posts."""
    if request.user.is_authenticated:
        username = request.user.username
        reviews = Review.objects.filter(user=request.user).order_by("-time_created")
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        return render(
            request,
            "posts.html",
            {"username": username, "reviews": reviews, "tickets": tickets},
        )
    else:
        return render(request, "home.html")


@login_required(login_url=reverse_lazy("login"))
def ticket_edit(request, ticket_id):
    """Edit a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.cleaned_data
            ticket_instance = form.save(commit=False)
            ticket_instance.image = request.FILES.get("image")
            ticket_instance.save()
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=ticket)
        return render(request, "ticket_edit.html", {"form": form})


@login_required(login_url=reverse_lazy("login"))
def review_edit(request, review_id):
    """Edit a review."""
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.ReviewForm(instance=review)
        return render(request, "review_edit.html", {"form": form})


@login_required(login_url=reverse_lazy("login"))
def ticket_delete(request, ticket_id):
    """Delete a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect("posts")
    return render(request, "ticket_delete.html", {"ticket": ticket})


@login_required(login_url=reverse_lazy("login"))
def review_delete(request, review_id):
    """Delete a review and change has_review to False for related_ticket"""
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        related_ticket_id = review.ticket_id
        related_ticket = Ticket.objects.get(id=related_ticket_id)
        related_ticket.has_review = False
        related_ticket.save()
        review.delete()
        return redirect("posts")
    return render(request, "review_delete.html", {"review": review})


@login_required(login_url=reverse_lazy("login"))
def subscriptions(request):
    """View all subscriptions."""
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        if "unsub" in request.POST:
            """Unsubscribe from a user."""
            UserFollows.objects.get(id=request.POST["unsub"]).delete()
            return redirect("subscriptions")
        elif "followed_user" in request.POST:
            """Get all users in the database. If the username is in the CustomUser table but not in the UserFollows table, add it to the UserFollows table."""
            users_in_db = CustomUser.objects.all()
            usernames = [user.username for user in users_in_db]
            users_followed = UserFollows.objects.filter(user=user)
            if (
                request.POST["followed_user"]
                in [user.followed_user.username for user in users_followed]
                or request.POST["followed_user"] == user.username
            ):
                return redirect("subscriptions")
            elif request.POST["followed_user"] in usernames:
                user_to_follow = CustomUser.objects.get(
                    username=request.POST["followed_user"]
                )
                UserFollows.objects.create(user=user, followed_user=user_to_follow)
                return redirect("subscriptions")
            else:
                return redirect("subscriptions")
        else:
            return redirect("subscriptions")

    else:
        """Get users that the current user is following and users that are following the current user."""
        form = FollowsUserForm(request.POST)
        users_followed = UserFollows.objects.filter(user_id=request.user.id)
        users_who_follows = UserFollows.objects.filter(followed_user_id=request.user.id)
        return render(
            request,
            "subscriptions.html",
            {
                "form": form,
                "users_followed": users_followed,
                "users_who_follows": users_who_follows,
            },
        )
