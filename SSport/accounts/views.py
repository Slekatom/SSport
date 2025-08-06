from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.shortcuts import render

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("main:training-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("main:training-list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class RegisterView(CreateView):
    model = CustomUser
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("main:training-list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


    def get_success_url(self):
        return reverse_lazy("main:training-list")

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

class Profile(DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile"

class MyProfile(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user
        return context

class MyProfileUpdate(UpdateView):
    model = CustomUser
    template_name = "accounts/update.html"
    fields = ["first_name", "last_name", "description", "birthdate", "image"]

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("accounts:my_profile")

class MyProfileDelete(DeleteView):
    model = CustomUser
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("main:training-list")

    def get_object(self, queryset=None):
        return self.request.user
