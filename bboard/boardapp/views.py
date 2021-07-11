from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, \
    UpdateView, View
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Advert, CUser, AdvertReply
from .forms import AdvertForm, ReplyForm, UserForm
from .filters import AdvertsFilter, RepliesFilter
from .tasks import *

# Create your views here.


class IndexView(View):

    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


class AdvertsListView(ListView):
    model = Advert
    template_name = 'adverts_list.html'
    context_object_name = 'adverts'
    queryset = Advert.objects.order_by('-datetime')


class AdvertsSearchView(ListView):
    model = Advert
    template_name = 'adverts_search.html'
    context_object_name = 'adverts'
    queryset = Advert.objects.order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdvertsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class AdvertDetailView(DetailView):
    model = Advert
    template_name = 'advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = AdvertReply.objects.filter(advert_id=self.kwargs['pk'])

        return context


class AdvertCreateView(LoginRequiredMixin, CreateView):
    form_class = AdvertForm
    template_name = 'advert_add.html'

    def form_valid(self, form):
        if CUser.objects.filter(cuser=self.request.user).exists():
            author = CUser.objects.get(cuser=self.request.user)
        else:
            author = CUser.objects.create(cuser=self.request.user)
        form.instance.author = author

        form.save()

        return super().form_valid(form)


class AdvertDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'advert_delete.html'
    context_object_name = 'advert'
    queryset = Advert.objects.all()
    success_url = '/'


class AdvertUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'advert_update.html'
    form_class = AdvertForm
    model = Advert


class ReplyCreateView(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    template_name = 'reply_add.html'

    def form_valid(self, form):
        if CUser.objects.filter(cuser=self.request.user).exists():
            author = CUser.objects.get(cuser=self.request.user)
        else:
            author = CUser.objects.create(cuser=self.request.user)
        form.instance.author = author
        form.instance.advert = Advert.objects.get(pk=self.kwargs.get('pk'))
        form.save()
        getting_reply.delay(reply_id=form.instance.id)

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        user = CUser.objects.get(cuser=self.request.user)
        advert = Advert.objects.get(id=self.kwargs.get('pk'))

        weekly_notify.delay()

        if user == advert.author:
            raise Http404('Вы не можете оставлять отклики к своим объявлениям')

        return super().get(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_profile.html'
    form_class = UserForm
    success_url = f'/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)


class RepliesSearchView(LoginRequiredMixin, ListView):
    model = AdvertReply
    template_name = 'replies.html'
    context_object_name = 'replies'
    queryset = AdvertReply.objects.order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RepliesFilter(self.request.GET,
                                          queryset=AdvertReply.objects.filter(advert__author__cuser=self.request.user),
                                          )
        return context


def reply_delete(request, pk):
    reply = AdvertReply.objects.get(id=pk)
    if request.user.pk == reply.advert.author.cuser.pk:
        reply.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def reply_accept(request, pk):
    reply = AdvertReply.objects.get(id=pk)

    if not reply.status:
        reply.status = True
        reply.save()
        accepting_reply.delay(reply_id=reply.id)

    return redirect(request.META.get('HTTP_REFERER'))
