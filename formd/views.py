# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, render
from extjs_lib.form import ExtForm, Zone

from contact.models import Contact, TYPE_CONTACT, ContactForm

def page1(request):
    form = ContactForm
    if request.method == 'POST':
        print request
        f = form(request.POST)
        if f.is_valid():
            f.save()
            r = '{ success: true, msg: "OK A VENIR " }'
        else:
            r = '{ success: false, msg: "ERREUR DJANGO" }'
        return HttpResponse(r, mimetype='application/json')
    else:
        f = ExtForm()
        f.url = '/formd/p1'
        f.url_annul = '/hello_extjs/p43'
        f.titre = "Mon Premier Formulaire dynamique"
        f.add_zone(Zone( 'cod_contact', fieldLabel="Code Contact" ))
        f.add_zone(Zone( 'nom_contact', fieldLabel="Nom du Contact" ))
        f.add_zone(Zone( 'tel_contact', fieldLabel="Telephone" ))
        f.add_zone(Zone( 'typ_contact', fieldLabel="Type de Contact", xtype = "combo", data = TYPE_CONTACT ))
        f.add_zone(Zone( 'description', fieldLabel="Description", xtype = 'htmleditor', width=500, height=200 ))
        S = f.render()
        
        template = 'formd/formd.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )
