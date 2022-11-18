from django import forms
from litreview.settings import AUTH_USER_MODEL
from reviews_app.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre", "description": "Description", "image": "Image"}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
        labels = {"rating": "Note", "headline": "Titre", "body": "Commentaire"}
        widgets = {
            "rating": forms.RadioSelect(
                choices=[(1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, "- 5")]
            )
        }
