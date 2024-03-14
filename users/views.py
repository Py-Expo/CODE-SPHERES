from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse

from users.forms import CustomUserCreationForm


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
    context = {"form": form}
    return render(request, "registration/register.html", context=context)
