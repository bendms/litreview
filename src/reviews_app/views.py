from urllib import request
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views import generic, View
from django.db.models import CharField, Value

from authentication.forms import FollowsUserForm
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from authentication.models import CustomUser, UserFollows
from .models import Ticket, Review
from itertools import chain

# Create your views here.

def get_users_viewable_reviews(request):
    """Return a queryset of reviews that the user can view."""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values("followed_user_id")
    list_id = [id["followed_user_id"] for id in users_followed]
    list_id.append(request.user.id)
    print("LIST_ID", list_id)
    users_objects = CustomUser.objects.filter(id__in=list_id)
    print("USERS_OBJECTS", users_objects)
    reviews_users_followed = Review.objects.filter(user__in=users_objects)
    print("=====REVIEWS_USER_FOLLOWED=====", reviews_users_followed)
    return reviews_users_followed

def get_users_viewable_tickets(request):
    """Return a queryset of a tickets that the user can view"""
    users_followed = UserFollows.objects.filter(user_id=request.user.id).values("followed_user_id")
    list_id = [id["followed_user_id"] for id in users_followed]
    list_id.append(request.user.id)
    users_objects = CustomUser.objects.filter(id__in=list_id)
    tickets_users_followed = Ticket.objects.filter(user__in=users_objects)
    print("TICKET_USERS_FOLLOWED", type(tickets_users_followed))
    return tickets_users_followed

@login_required(login_url=reverse_lazy('login'))
def home(request):
    """Home page view."""
    username = None
    if request.user.is_authenticated:
        reviews = get_users_viewable_reviews(request)  
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = get_users_viewable_tickets(request) 
        # returns queryset of tickets
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created, 
            reverse=True
        )
        return render(request, 'home.html', context={'posts': posts})
    else:
        return render(request, 'home.html')

@login_required(login_url=reverse_lazy('login'))
def create_ticket(request):
    """Create a new ticket."""
    if request.method == 'POST':
        form = forms.TicketForm(request.POST)
        # request.user = CustomUser.objects.get(id=request.user.id)
        if form.is_valid():
            form.cleaned_data
            ticket_instance = form.save(commit=False)
            ticket_instance.user = request.user
            ticket_instance.image = request.FILES.get('image')
            ticket_instance.save()
            return redirect('home')
    else:
        form = forms.TicketForm()
        request.user = CustomUser.objects.get(id=request.user.id)
        return render(request, 'ticket_creation.html', {'form': form})
    
@login_required(login_url=reverse_lazy('login'))
def create_review_not_in_response_to_a_ticket(request):
    if request.method == 'POST':
        form_ticket = forms.TicketForm(request.POST)
        print("FORM_TICKET", form_ticket)
        form_review = forms.ReviewForm(request.POST) #TODO: Passer le ticket de la requête POST en paramètre ici
        print("FORM_REVIEW", form_review)
        if form_review.is_valid() and form_ticket.is_valid():
            form_review.cleaned_data
            form_ticket.cleaned_data
            review_instance = form_review.save(commit=False)
            ticket_instance = form_ticket.save(commit=False)
            review_instance.user = request.user
            ticket_instance.user = request.user
            ticket_instance.save()
            review_instance.ticket = ticket_instance
            review_instance.save()
            return redirect('home')
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()
        review_form.ticket = ticket_form
        return render(request, 'review_creation_not_in_response_to_a_ticket.html', {'ticket_form': ticket_form, 'review_form': review_form})
            
    
@login_required(login_url=reverse_lazy('login'))
def create_review(request):
    """Create a new review."""
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        
        # request.user = CustomUser.objects.get(id=request.user.id)
        if form.is_valid():
            form.cleaned_data
            review_instance = form.save(commit=False)
            review_instance.user = request.user
            review_instance.save()
            return redirect('home')
    else:
        form = forms.ReviewForm()
        request.user = CustomUser.objects.get(id=request.user.id)
        return render(request, 'review_creation.html', {'form': form})
    
@login_required(login_url=reverse_lazy('login'))
def posts_view(request):
    """View all posts."""
    if request.user.is_authenticated:
        username = request.user.username
        reviews = Review.objects.filter(user=request.user)
        tickets = Ticket.objects.filter(user=request.user)
        print(reviews)
        print(tickets)
        return render (request, 'posts.html', {'username': username, 'reviews': reviews, 'tickets': tickets})
    else:
        return render(request, 'home.html')
    
@login_required(login_url=reverse_lazy('login'))
def ticket_edit(request, ticket_id):
    """Edit a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = forms.TicketForm(instance=ticket)
        return render(request, 'ticket_edit.html', {'form': form})
    
    
@login_required(login_url=reverse_lazy('login'))
def review_edit(request, review_id):
    """Edit a review."""
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = forms.ReviewForm(instance=review)
        return render(request, 'review_edit.html', {'form': form})

@login_required(login_url=reverse_lazy('login'))
def ticket_delete(request, ticket_id):
    """Delete a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'ticket_delete.html', {'ticket': ticket})

@login_required(login_url=reverse_lazy('login'))
def review_delete(request, review_id):
    """Delete a review."""
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_delete.html', {'review': review})


@login_required(login_url=reverse_lazy('login'))
def subscriptions(request):
    """View all subscriptions."""
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        if 'unsub' in request.POST:
            """Unsubscribe from a user."""
            UserFollows.objects.get(id=request.POST['unsub']).delete()
            return redirect('subscriptions')
        elif 'followed_user' in request.POST:
            """Get all users in the database. If the username is in the CustomUser table but not in the UserFollows table, add it to the UserFollows table."""
            users_in_db = CustomUser.objects.all()
            usernames = [user.username for user in users_in_db]
            users_followed = UserFollows.objects.filter(user=user)
            
            print("USERS_FOLLOWED", users_followed)
            if request.POST['followed_user'] in [user.followed_user.username for user in users_followed] or request.POST['followed_user'] == user.username:
                return redirect('subscriptions')
            elif request.POST['followed_user'] in usernames:
                user_to_follow = CustomUser.objects.get(username=request.POST['followed_user'])
                UserFollows.objects.create(user=user, followed_user=user_to_follow)
                return redirect('subscriptions')    
            else:
                return redirect('subscriptions')
        else:
            return redirect('subscriptions')
            
    else:
        """Get users that the current user is following and users that are following the current user."""
        form = FollowsUserForm(request.POST)
        users_followed = UserFollows.objects.filter(user_id=request.user.id)
        # users_followed = UserFollows.objects.all.exclude(user_id=request.user.id)
        users_who_follows = UserFollows.objects.filter(followed_user_id=request.user.id)
        return render(request, 'subscriptions.html', {'form': form, 'users_followed': users_followed, 'users_who_follows': users_who_follows})
