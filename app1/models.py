# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils import timezone
import reversion


reversion.register(User)


@reversion.register
class ModelA(models.Model):
    user = models.ForeignKey(User, related_name='us')

    attr1 = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True, blank=True)

    updated_by_user = models.ForeignKey(User, related_name='uus')

    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now,
                                      editable=False)

    updated_at = models.DateTimeField(auto_now=True, default=timezone.now,
                                      editable=False)

    def save(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            if self.id:
                reversion.set_comment("updated ModelA")
            else:
                reversion.set_comment("created ModelA")
            reversion.set_user(self.updated_by_user)
            super(ModelA, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.user.username, self.attr1)
