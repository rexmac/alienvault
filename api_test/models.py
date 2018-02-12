from django.db import models
import random
import string


# Taken from https://stackoverflow.com/a/2257449
def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in xrange(12)])


class User(models.Model):
    alien_vault_id = models.CharField(max_length=12, unique=True, default=generate_id)


class Visit(models.Model):
    user = models.ForeignKey(User, related_name='visits')
    address = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
