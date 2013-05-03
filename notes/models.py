# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from django.utils.translation import ugettext_lazy as _

STATUS_NOTES = (
	( 'OK', 'Active'),
	( 'DEL', 'Deleted' ),
)

# Create your models here.
class Note(models.Model):
    titre = models.CharField(_(u'Titre'),max_length=50)
    description = models.TextField(_(u'Description'))
    tag1 = models.CharField(_(u'Tag1'),max_length=20)
    tag2 = models.CharField(_(u'Tag2'),max_length=20)
    tag3 = models.CharField(_(u'Tag3'),max_length=20)
    tag4 = models.CharField(_(u'Tag4'),max_length=20)
    tag5 = models.CharField(_(u'Tag5'),max_length=20)
    status = models.CharField(_(u'Status'), max_length=5, choices=STATUS_NOTES, default='OK' )
    date_cr = models.DateTimeField(auto_now_add=True)
    date_mo = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s : %s" %  (self.id, self.titre)

    def to_json(self):
        return dict(
                        id = self.id,
                        titre = self.titre,
                        description = self.description,
                        tag1 = self.tag1,
                        tag2 = self.tag2,
                        tag3 = self.tag3,
                        tag4 = self.tag4,
                        tag5 = self.tag5,
                        status = self.status,
                        date_cr = self.date_cr,
                        date_mo = self.date_mo
                )

class NoteForm(ModelForm):
    class Meta:
        model = Note

#class Contact(models.Model):
#    cod_contact = models.CharField(_(u'Code Contact'),max_length=20, unique=True)
#    nom_contact = models.CharField(_(u'Nom Contact'),max_length=40)
#    description = models.TextField(_(u'Description'))
#    tel_contact = models.CharField(_(u'Téléphone'), max_length=30)
#    typ_contact = models.CharField(_(u'Type Contact'), max_length=10, choices=TYPE_CONTACT, default='PRO' )
#
#    def __unicode__(self):
#        return "%s : %s" % (self.cod_contact, self.nom_contact)
#
#    def to_json(self):
#        return dict( id=self.id, cod_contact=self.cod_contact, nom_contact=self.nom_contact, description=self.description,
#                    tel_contact=self.tel_contact, typ_contact=self.typ_contact )
#
#class ContactForm(ModelForm):
#	class Meta:
#		model = Contact
