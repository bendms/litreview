from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic, View
from . import forms


def logout(request):
    auth.logout(request)
    return render(request=request, template_name="logout.html")


class SignUpView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy("home")
    template_name = "signup.html"


class LoginView(View):
    template_name = "login.html"
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
        message = "Login failed!"
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )
