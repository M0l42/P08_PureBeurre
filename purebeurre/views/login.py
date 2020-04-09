from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from purebeurre.forms.login import SignUpForm, LogInForm
from django.views.generic.edit import FormView


class SignUpFormView(FormView):
    form_class = SignUpForm
    template_name = 'pure_beurre/form.html'

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

        return render(request=self.request, template_name=self.template_name, context=context)


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

        context = self.get_context_data()

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return render(request=self.request, template_name=self.template_name, context=context)