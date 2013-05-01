# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, render
from extjs_lib.form import ExtForm, Zone

from contact.models import Contact, TYPE_CONTACT

def page1(request):
    if request.method == 'POST':
        print request
        r = '{ success: false, msg: "OK A VENIR " }'
        return HttpResponse(r, mimetype='application/json')
    else:
        f = ExtForm()
        f.url = '/formd/p1'
        f.add_zone(Zone( 'cod_contact', fieldLabel="Code Contact" ))
        f.add_zone(Zone( 'nom_contact', fieldLabel="Nom du Contact" ))
        f.add_zone(Zone( 'description', fieldLabel="Description" ))
        f.add_zone(Zone( 'tel_contact', fieldLabel="Telephone" ))
        f.add_zone(Zone( 'typ_contact', fieldLabel="Type de Contact", xtype = "combo", data = TYPE_CONTACT ))
        S = f.render()
        
        template = 'formd/formd.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )
