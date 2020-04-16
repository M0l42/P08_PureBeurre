from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import requests

class HomeView(View):
    template_name = 'pure_beurre/home.html'

    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            return render(requests, 'pure_beurre/product.html')
        return render(self.request, self.template_name)


class AccountView(LoginRequiredMixin, View):
    template_name = 'pure_beurre/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Account'
        user = self.request.user
        context['user'] = user
        return context

    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            return render(requests, 'pure_beurre/product.html')
        return render(request, self.template_name)