from django.views import View
from django.shortcuts import render
import requests

class HomeView(View):
    template_name = 'pure_beurre/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)