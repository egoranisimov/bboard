from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import *

urlpatterns = [
    path('', AdvertsListView.as_view(), name='adverts_list'),
    path('add/', AdvertCreateView.as_view(), name='advert_add'),
    path('<int:pk>/', AdvertDetailView.as_view(), name='advert_detail'),
    path('<int:pk>/delete/', AdvertDeleteView.as_view(), name='advert_delete'),
    path('<int:pk>/update/', AdvertUpdateView.as_view(), name='advert_update'),
    path('<int:pk>/reply/', ReplyCreateView.as_view(), name='reply_add'),
    path('search/', AdvertsSearchView.as_view(), name='adverts_search'),
    path('index/', IndexView.as_view()),

]
