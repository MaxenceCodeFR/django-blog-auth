"""
URL configuration for fotoblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import authentication.views
import blog.views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    # AUTH
    path('', LoginView.as_view(template_name='authentication/login.html',
                               redirect_authenticated_user=True,), name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='authentication/password_change.html'), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='authentication/password_change_done.html'), name='password_change_done'),
    path('sign-up/', authentication.views.sign_up, name='sign_up' ),
    path('upload-profile-photo/', authentication.views.upload_profile_photo, name='upload_profile_photo'),

    # BLOG
    path('blog/', blog.views.BlogHomeView.as_view(), name='blog'),
    path('upload-photo/', blog.views.PhotoUploadView.as_view(), name='upload_photo'),
    path('create-ticket/', blog.views.BlogAndPhotoView.as_view(), name='create_ticket'),
    path('blog/<int:blog_id>', blog.views.ShowBlogView.as_view(), name='view_blog'),
    path('blog/<int:blog_id>/edit/', blog.views.EditBlogView.as_view(), name='edit_blog'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
