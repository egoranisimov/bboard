"""bboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from allauth.account.views import LogoutView
from django.urls import path, include
from boardapp.views import UserUpdateView, RepliesSearchView, reply_delete, \
    reply_accept
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boardapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user_profile'),
    path('profile/<int:pk>/replies/', RepliesSearchView.as_view(), name='replies'),
    path('reply/<int:pk>/delete', reply_delete, name='reply_delete'),
    path('reply/<int:pk>/accept', reply_accept, name='reply_accept'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
