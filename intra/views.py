from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    UserChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, RedirectView, FormView, \
    UpdateView, ListView
from intra.forms import IntraUserCreationForm, IntraUserChangeForm, \
    PasswordChangingForm
from intra.models import User


class Home(View):
    def get(self, request):
        return render(request, 'index.html', context={'login_form': AuthenticationForm})


class Profile(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    template_name = "detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context


class IntraPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')


class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "edit_user_profile.html"
    form_class = IntraUserChangeForm
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please submit the form carefully")
        return redirect('update_profile')


class ProfileList(ListView):
    model = User
    template_name = 'profile_list.html'


class Register(CreateView):
    template_name = "register.html"
    model = User
    form_class = IntraUserCreationForm
    success_url = reverse_lazy('chat')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('chat')
        resp = super().form_valid(form)
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, user)
        return resp

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class Logout(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('index')
    login_url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You are already logged in!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, "Invalid username or password.")
            return
        login(self.request, user)
        messages.info(self.request, f"You are now logged in as {username}.")
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'login'
    success_url = reverse_lazy('index')
