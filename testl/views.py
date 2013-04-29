# -*- coding: utf-8 -*-
# Create your views here.
from django.utils import simplejson
from django.shortcuts import render, render_to_response, HttpResponse
from django.shortcuts import HttpResponseRedirect

from contact.models import Contact

# Plus besoin 
#from django.views.decorators.csrf import csrf_exempt

import pdb



## Pour une page avec formulaire
## Il faut : une fonction pour le rendu
## Une fonction pour l'initialisation / chargement load
## Une fonction pour la sauvegarde et la verification

## TODO : Le tri des colonnes qui n'est pas effectif

## Plus besoin
#@csrf_exempt
def liste(request):

    model = Contact
    def_limit = 10

    if request.method == "POST":
        ## Pour debug ( Err 500 :( )
        #pdb.set_trace()
        start = request.POST.get('start', 0)
        limit = request.POST.get('limit', def_limit)
        tri = request.POST.get('sort', 'id')
        sens = request.POST.get('dir', 'ASC')
        try:
            start = int(start)
        except:
            start = 0
        try:
            limit = int(limit)
        except:
            limit = def_limit

        total = model.objects.all().count()
        obj_list = model.objects.all()[start:start+limit]

        ## Dans le cas d'une liste d'objets
        obj = [ob.to_json() for ob in obj_list]
        ## sinon obj tout seul
        ## obj = ob.to_json()

        root_name = 'rows'
        data = '{"total": %s, "%s": %s}' % (total, root_name, simplejson.dumps(obj))

        #print data
        #print simplejson.dumps(data)

        return HttpResponse(data, mimetype='text/javascript')  
    else:
        return render_to_response('contact/liste.html')

def page42(request):
    SCRIPT_EXTJS = """
    Ext.onReady(function(){

    Ext.define('User', {
    extend: 'Ext.data.Model',
    fields:%s
    });

    var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
    { name: 'Lisa', email: 'lisa@simpsons.com', phone: '555-111-1224' },
    { name: 'Bart', email: 'bart@simpsons.com', phone: '555-222-1234' },
    { name: 'Homer', email: 'home@simpsons.com', phone: '555-222-1244' },
    { name: 'Marge', email: 'marge@simpsons.com', phone: '555-222-1254' }
    ]
    });

    Ext.create('Ext.grid.Panel', {
        renderTo: Ext.getBody(),
        store: userStore,
        width: 400,
        height: 200,
        title: '%s',
        columns: [
            {
                text: 'Name',
                width: 100,
                sortable: false,
                hideable: false,
                dataIndex: '%s'
            },
            {
                text: 'Email Address',
                width: 150,
                dataIndex: '%s',
                hidden: true
            },
            {
                text: 'Phone Number',
                flex: 1,
                dataIndex: '%s'
            }
        ]
        });

    });


    """
    f = ['name', 'email', 'phone']
    SCRIPTS_EXTJS = SCRIPT_EXTJS % ( simplejson.dumps(f), 'TITRE GRILLE', f[0], f[1], f[2] )
    template = 'hello_extjs/page42.html'
    return render( request, template, { 'SCRIPT_EXTJS':SCRIPTS_EXTJS } )
