from django.db import models
from django.contrib.auth.models import User


class CUser(models.Model):
    cuser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.cuser.username


class Advert(models.Model):
    TANKS = 'TS'
    HEALERS = 'HS'
    DAMAGE_DEALERS = 'DD'
    MERCHANTS = 'MS'
    GILD_MASTERS = 'GM'
    QUEST_GIVERS = 'QG'
    BLACKSMITHS = 'BS'
    LEATHERWORKERS = 'LW'
    POTION_MAKERS = 'PM'
    SPELLS_MASTERS = 'SM'

    CATEGORY_CHOICES = [
        (TANKS, 'Танки'),
        (HEALERS, 'Хилы'),
        (DAMAGE_DEALERS, 'ДД'),
        (MERCHANTS, 'Торговцы'),
        (GILD_MASTERS, 'Гилдмастеры'),
        (QUEST_GIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (LEATHERWORKERS, 'Кожевники'),
        (POTION_MAKERS, 'Зельевары'),
        (SPELLS_MASTERS, 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(CUser, on_delete=models.CASCADE,
                               verbose_name='Автор', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,
                                default=TANKS, verbose_name='Категория')
    datetime = models.DateTimeField(auto_now_add=True)
    post_rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f'/{self.pk}'


# class Categories(models):
#     pass
#
#


class AdvertReply(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE,
                               verbose_name='Объявление', blank=True,
                               null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CUser, on_delete=models.CASCADE,
                               verbose_name='Автор', blank=True, null=True)
    content = models.TextField(verbose_name='Содержание')
    status = models.BooleanField(default=False, verbose_name='Статус')

    def get_absolute_url(self):
        return f'/{self.advert.pk}'

# from django.db import models
# from django.contrib.auth.models import User
# from boardapp.models import *
# AdvertReply.objects.filter().order_by('-datetime')
# Advert.objects.all().values('id')
# CUser.objects.all().values('id')
# AdvertReply.objects.all().values('content', 'status')

#
#
# cuser = CUser.objects.get(id=1)
# Advert.objects.filter(author=cuser).values('id')
# advert = Advert.objects.get(id=4)
#
#
# reply = AdvertReply.objects.create(advert=advert, author=cuser, content='Отзыв 2 Объявление id4')
# reply.advert.author.id