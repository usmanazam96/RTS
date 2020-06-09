from accounts.models import *
from django.db.models import Q


def is_email_already_exist(email):
    email_q = Q(email__iexact=email)
    count = User.objects.filter(email_q).count()
    if count > 0:
        return True
    return False


def is_email_already_exist(email, id):
    email_q = Q(email__iexact=email)
    id_q = Q(id=id)
    count = User.objects.filter(email_q & (~id_q)).count()
    if count > 0:
        return True
    return False
