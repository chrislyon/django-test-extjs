# -*- coding: utf-8 -*-
# Create your views here.
from django.utils import simplejson
from django.shortcuts import render, render_to_response, HttpResponse
from django.shortcuts import HttpResponseRedirect

from contact.models import Contact
from extjs_lib.grid import ExtGrid, Champ

# Plus besoin 
#from django.views.decorators.csrf import csrf_exempt

import pdb

## TODO : Le tri des colonnes qui n'est pas effectif (fait)

## Plus besoin
#@csrf_exempt
def liste(request):
    if request.method == 'POST':
        ## --------------------------------------
        ## c'est une demande de donnees (POST)
        ## --------------------------------------
        ztri = None
        model = Contact
        def_limit = 10
        ## Pour debug ( Err 500 :( )
        #pdb.set_trace()
        #print request.POST
        start = request.POST.get('start', 0)
        limit = request.POST.get('limit', def_limit)
        tri = request.POST.get('sort', None)
        try:
            start = int(start)
        except:
            start = 0
        try:
            limit = int(limit)
        except:
            limit = def_limit

        if tri:
            tri = simplejson.loads(tri)
            if tri:
                sens = tri[0]['direction']
                ztri = tri[0]['property']
                #print "tri = %s / sens = %s / ztri = %s " % (tri, sens, ztri)


        #pdb.set_trace()
        total = model.objects.all().count()
        if ztri:
            obj_list = model.objects.all().order_by(ztri)[start:start+limit]
            if sens != 'ASC':
                obj_list = obj_list.reverse()
        else:
            obj_list = model.objects.all()[start:start+limit]

        #print obj_list

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
        ## ---------------------------------------
        ## Parametrage de la grille (request GET)
        ## ---------------------------------------
        g = ExtGrid()
        g.add_champ( Champ('id', text='Id', width=50, sortable=True) )
        g.add_champ( Champ('cod_contact', text='Code', width=100, sortable=True) )
        g.add_champ( Champ('nom_contact', text="Nom", width=200, sortable=True) )
        g.add_champ( Champ('tel_contact', text='Telephone', width=200) )
        g.titre = "Nouvelle Grille Auto"
        g.width = 800 
        g.height = 400 
        g.pageSize = 10
        g.data_url = '/listed/'
        g.base_url = '/listed'
        g.button_new_url = '/listed/cr'
        g.button_home = '/'
        S = g.render()
        #print S
        template = 'listed/liste.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } ) 
        #return render_to_response('listed/liste.html')

