
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import formset_factory
from django.contrib.auth.decorators import permission_required


from . import forms
from . import models


class BlogHomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'
    login_url = 'login'

    def get(self, request):
        photos = models.Photo.objects.all()
        blogs = models.Blog.objects.all()
        return render(request, self.template_name, {'photos': photos, 'blogs': blogs})

class PhotoUploadView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'blog/photo_upload.html'
    login_url = 'login'
    permission_required = 'blog.add_photo'
    raise_exception = True

    def get(self, request):
        PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
        formset = PhotoFormSet()
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('blog')
        return render(request, self.template_name, {'formset': formset})


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

class EditBlogView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'blog/edit_blog.html'
    login_url = 'login'
    permission_required = 'blog.change_blog'
    raise_exception = True

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

