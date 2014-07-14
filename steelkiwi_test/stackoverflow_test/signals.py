from django.core.mail import send_mail

from config import MAIL_CONFIG


def notify_author(instance, **kwargs):
    send_mail('Your question has been updated',
              "User has answered to your question '{0}'".format(instance.question.subject),
              MAIL_CONFIG['mail_from'],
              [instance.question.user.email])