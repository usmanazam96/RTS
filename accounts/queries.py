from accounts.models import *
from django.db.models import Q
from django_private_chat.models import Dialog, Message
from django.contrib.auth.models import User


def is_email_already_exist(email):
    email_q = Q(email__iexact=email)
    count = User.objects.filter(email_q).count()
    if count > 0:
        return True
    return False


def is_email_already_exist_id(email, id):
    email_q = Q(email__iexact=email)
    id_q = Q(id=id)
    count = User.objects.filter(email_q & (~id_q)).count()
    if count > 0:
        return True
    return False


def get_unread_messages_count(user):
    owner_q = Q(owner=user)
    opponent_q = Q(opponent=user)
    dialogs = Dialog.objects.filter(owner_q | opponent_q)
    dialogs_q = Q(dialog__in=dialogs)

    sender_q = Q(sender=user)
    created_q = Q(created__gte=user.last_login)
    count = 0
    count = Message.objects.filter(dialogs_q & ~sender_q & created_q).count()
    return count

