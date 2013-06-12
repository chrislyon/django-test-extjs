# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from django.utils.translation import ugettext_lazy as _

STATUS_ACTION = (
    ( 'EN_COURS', 'En cours'),
    ( 'FAIT', 'Fait'),
)

# Create your models here.
class Action(models.Model):
    qui = models.CharField(_(u'Titre'),max_length=50)
    quoi = models.TextField(_(u'Description'),blank=True)
    quand = models.DateTimeField(auto_now_add=True)
    temps = models.CharField(_(u'Tag1'),max_length=20, blank=True)
    status = models.CharField(_(u'Status'), max_length=5, choices=STATUS_ACTION, default='OK' )
    desc = models.TextField(_(u'Description'),blank=True)
    #date_cr = models.DateTimeField(auto_now_add=True)
    #date_mo = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s : %s" %  (self.id, self.qui, self.quoi)

    def to_json(self):
        return dict(
                        id = self.id,
                        qui = self.qui,
                        quoi = self.quoi,
                        quand = self.quand.strftime('%d/%m/%y %X'),
                        temps = self.temps,
                        status = self.status,
                        desc = self.desc,
                )

class ActionForm(ModelForm):
    class Meta:
        model = Action

