# -*- coding: utf-8 -*-
# Create your views here.
from django.utils import simplejson
from django.shortcuts import render, render_to_response, HttpResponse
from django.shortcuts import HttpResponseRedirect

from extjs_lib.grid import ExtGrid, GridCol
from extjs_lib.form import ExtForm, Zone
from notes.models import Note, NoteForm, STATUS_NOTES

from django.views.decorators.csrf import csrf_exempt

import pdb

def liste(request):
    if request.method == 'POST':
        ## --------------------------------------
        ## c'est une demande de donnees (POST)
        ## --------------------------------------
        ztri = None
        ## A CHANGER
        model = Note
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
        g.add_col( GridCol('id', text='Id', width=50, sortable=True) )
        g.add_col( GridCol('titre', text='Titre', width=200, sortable=True) )
        g.add_col( GridCol('tag1', text="Tag1", width=100, sortable=True) )
        g.add_col( GridCol('tag2', text="Tag2", width=100, sortable=True) )
        g.add_col( GridCol('tag3', text="Tag3", width=100, sortable=True) )
        g.add_col( GridCol('tag4', text="Tag4", width=100, sortable=True) )
        g.add_col( GridCol('tag5', text="Tag5", width=100, sortable=True) )
        g.add_col( GridCol('status', text='Status', width=100) )
        g.titre = "Liste des Notes"
        g.width = 800 
        g.height = 400 
        g.pageSize = 10
        g.data_url = '/notes/'
        g.base_url = '/notes'
        g.button_new_url = '/notes/cr'
        g.button_home = '/'
        S = g.render()
        #print S
        template = 'notes/notes.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } ) 

#@csrf_exempt
def create(request):
    form = NoteForm
    if request.method == 'POST':
        print request
        f = form(request.POST)
        if f.is_valid():
            f.save()
            r = '{ success: true, msg: "OK A VENIR " }'
        else:
            r = '{ success: false, msg: "ERREUR DJANGO" }'
        print r
        return HttpResponse(r, mimetype='application/json')
    else:
        f = ExtForm()
        f.url = '/notes/cr/'
        f.url_annul = '/notes/'
        f.titre = "Creation"
        f.width = 800 
        f.height = 400 
        f.add_zone(Zone( 'titre', fieldLabel="Titre", width=500 ))
        f.add_zone(Zone( 'tag1', fieldLabel="Tag1" ))
        f.add_zone(Zone( 'tag2', fieldLabel="Tag1" ))
        f.add_zone(Zone( 'tag3', fieldLabel="Tag1" ))
        f.add_zone(Zone( 'tag4', fieldLabel="Tag1" ))
        f.add_zone(Zone( 'tag5', fieldLabel="Tag1" ))
        f.add_zone(Zone( 'status', fieldLabel="Status", xtype = "combo", data = STATUS_NOTES ))
        f.add_zone(Zone( 'description', fieldLabel="Description", xtype = 'htmleditor', width=700, height=300 ))
        S = f.render()

        template = 'notes/notes.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )

