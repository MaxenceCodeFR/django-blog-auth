from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

class BlogHomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'
    login_url = 'login'

    def get(self, request):
        return render(request, self.template_name)
