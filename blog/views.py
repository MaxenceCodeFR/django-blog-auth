from lib2to3.fixes.fix_input import context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


from . import forms
from . import models


class BlogHomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'
    login_url = 'login'

    def get(self, request):
        photos = models.Photo.objects.all()
        blogs = models.Blog.objects.all()
        return render(request, self.template_name, {'photos': photos, 'blogs': blogs})


class PhotoUploadView(LoginRequiredMixin, View):
    template_name = 'blog/photo_upload.html'
    login_url = 'login'

    def get(self, request):
        form = forms.PhotoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('blog')
        return render(request, self.template_name, {'form': form})


class BlogAndPhotoView(LoginRequiredMixin, View):
    template_name = 'blog/create_blog_post.html'
    login_url = 'login'

    def get(self, request):
        blog_form = forms.BlogForm()
        photo_form = forms.PhotoForm()

        context = {
            'blog_form': blog_form,
            'photo_form': photo_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)

        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()

            return redirect('blog')

        context = {
            'blog_form': blog_form,
            'photo_form': photo_form
        }
        return render(request, self.template_name, context)


class ShowBlogView(View):
    template_name = 'blog/view_blog.html'
    login_url = 'login'

    def get(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        return render(request, self.template_name, {'blog': blog})

class EditBlogView(View):
    template_name = 'blog/edit_blog.html'
    login_url = 'login'

    def get(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        edit_form = forms.BlogForm(instance=blog)
        delete_form = forms.DeleteBlogForm()

        context = {
            'edit_form': edit_form,
            'delete_form': delete_form
        }
        return render(request, self.template_name, context)

    def post(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        edit_form = forms.BlogForm(request.POST, instance=blog)
        delete_form = forms.DeleteBlogForm(request.POST)

        if edit_form.is_valid():
            edit_form.save()
            return redirect('blog')

        if delete_form.is_valid():
            blog.delete()
            return redirect('blog')

        context = {
            'edit_form': edit_form,
            'delete_form': delete_form
        }
        return render(request, self.template_name, context)

