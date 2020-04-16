from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from purebeurre.forms.login import SignUpForm, LogInForm
from django.views.generic.edit import FormView


class SignUpFormView(FormView):
    form_class = SignUpForm
    template_name = 'pure_beurre/form.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(SignUpFormView, self).get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

    def form_valid(self, form):
        user_name = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        context = self.get_context_data()

        if password == confirm_password:
            User.objects.create_user(username=user_name, first_name=first_name,
                                     email=email, password=password, last_name=last_name)
        else:
            context['error'] = 'The two password are not identical'

        return super().form_valid(form)


class LogInFormView(FormView):
    form_class = LogInForm
    template_name = 'pure_beurre/form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LogInFormView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


class LogOutView(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
