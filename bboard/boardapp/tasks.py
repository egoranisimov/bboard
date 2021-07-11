import time

from celery import shared_task
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta

from .models import *


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def getting_reply(reply_id: int):
    reply = AdvertReply.objects.get(id=reply_id)
    user = User.objects.get(id=reply.advert.author.cuser.id)
    advert = Advert.objects.get(id=reply.advert.id)

    html_content = render_to_string('getting_reply.html',
                                    {'reply': reply,
                                     'username': user.username,
                                     'advert': advert,
                                     }
                                    )
    msg = EmailMultiAlternatives(
        subject=f'Новый отклик',
        from_email='epanisimov@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    time.sleep(10)


@shared_task
def accepting_reply(reply_id: int):
    reply = AdvertReply.objects.get(id=reply_id)
    user = User.objects.get(id=reply.author.cuser.id)
    advert = Advert.objects.get(id=reply.advert.id)

    html_content = render_to_string('accepting_reply.html',
                                    {'reply': reply,
                                     'username': user.username,
                                     'advert': advert,
                                     }
                                    )
    msg = EmailMultiAlternatives(
        subject=f'Ваш отклик принят',
        from_email='epanisimov@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    time.sleep(10)


@shared_task
def weekly_notify():
    post_datetime_filter = datetime.now() - timedelta(days=7)
    adverts_last_week = Advert.objects.filter(datetime__gte=post_datetime_filter)
    users = User.objects.all()

    for user in users:
        html_content = render_to_string('weekly_notify.html',
                                        {'adverts': adverts_last_week,
                                         'user': user,
                                         }
                                        )
        msg = EmailMultiAlternatives(
            subject='Подборка объявлений за неделю',
            from_email='epanisimov@yandex.ru',
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()
        time.sleep(10)