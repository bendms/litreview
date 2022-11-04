from urllib import request
from django.shortcuts import HttpResponse, render
from django.urls import reverse_lazy
from django.views import generic, View

from authentication.forms import FollowsUserForm
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from authentication.models import CustomUser, UserFollows
from .models import Ticket, Review
# Create your views here.

@login_required(login_url=reverse_lazy('login'))
def home(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        tickets = Ticket.objects.all()
        return render(request, 'home.html', {'username': username, 'tickets': tickets})
    else:
        return render(request, 'home.html')

@login_required(login_url=reverse_lazy('login'))
def create_ticket(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST)
        # request.user = CustomUser.objects.get(id=request.user.id)
        if form.is_valid():
            form.cleaned_data
            ticket_instance = form.save(commit=False)
            ticket_instance.user = request.user
            ticket_instance.image = request.FILES['image']
            ticket_instance.save()
            return redirect('home')
    else:
        form = forms.TicketForm()
        request.user = CustomUser.objects.get(id=request.user.id)
        return render(request, 'ticket_creation.html', {'form': form})
    
@login_required(login_url=reverse_lazy('login'))
def create_review(request):
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
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'ticket_delete.html', {'ticket': ticket})

@login_required(login_url=reverse_lazy('login'))
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'review_delete.html', {'review': review})

@login_required(login_url=reverse_lazy('login'))
def subscriptions(request):
    user = CustomUser.objects.get(id=request.user.id)
    # user_to_follow = CustomUser.objects.filter(id__in=UserFollows.objects.filter(follower=user))
    # users_followed = UserFollows.objects.filter(user=user)
    # users_to_follow = 
    if request.method == 'POST':
        if 'unsub' in request.POST:
            print("REQUEST.POST", request.POST)
            print("REQUEST.POST['unsub'] = ", request.POST['unsub'])
            UserFollows.objects.get(id=request.POST['unsub']).delete()
            return redirect('subscriptions')
        else:
            user_to_follow = CustomUser.objects.get(id=request.POST['followed_user'])
            UserFollows.objects.create(user=user, followed_user=user_to_follow)
            return redirect('subscriptions')
    else:
        form = FollowsUserForm(request.POST)
        users_followed = UserFollows.objects.filter(user_id=request.user.id)
        users_who_follows = UserFollows.objects.filter(followed_user_id=request.user.id)
        return render(request, 'subscriptions.html', {'form': form, 'users_followed': users_followed, 'users_who_follows': users_who_follows})
