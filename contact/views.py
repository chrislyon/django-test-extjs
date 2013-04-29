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




BASE_RETOUR = '/contact/'

T_LISTE = 'Liste des Contacts'
T_MODIF = "Modification d'un contact"
T_CREATE = "Nouveau Contact"
T_ANNUL = "Annulation d'un Contact"

## --------------
## Creation
## --------------
def create(request, form, template):
    #pdb.set_trace()
    if request.method == 'POST':
            f = form(request.POST)
            if f.is_valid():
                f.save()
                #return HttpResponseRedirect(BASE_RETOUR+'cr')
                data = '{ "success": "true" }'
                return HttpResponse(data, mimetype='text/javascript')  
            ## SI c'est pas valide ca repart
    else:
        f = form()

    return render( request, template, { 'form' : f, 'TITRE_PAGE':T_CREATE } )

