# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse, render
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from extjs_lib.grid import ExtGrid, GridCol
from extjs_lib.form import ExtForm, Zone, ZBox
from tt.models import Action, ActionForm, STATUS_ACTION

import datetime

import pdb

## -----------------------
## La liste de depart
## -----------------------
#@csrf_exempt
def debug(request):
        print datetime.datetime.now(), "DEBUG", request.POST
        obj = {
            'success' : True,
            'message' : 'OK'
        }
        data = '{"total": %s, "%s": %s}' % (0, 'rows', simplejson.dumps(obj))
        print "DEBUG", data
        return HttpResponse(data, mimetype='text/javascript')  

#@csrf_exempt
def liste(request):
    if request.method == 'POST':
        ## --------------------------------------
        ## c'est une demande de donnees (POST)
        ## --------------------------------------
        ztri = None
        ## A CHANGER
        model = Action
        def_limit = 10
        ## Pour debug ( Err 500 :( )
        #pdb.set_trace()
        print datetime.datetime.now(), 'LISTE', request.POST
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

        ## Pour debug
        #print data
        #print simplejson.dumps(data)

        return HttpResponse(data, mimetype='text/javascript')  
    else:
        ## ---------------------------------------
        ## Parametrage de la grille (request GET)
        ## ---------------------------------------
        g = ExtGrid()
        g.add_col( GridCol('id', text='Id', width=50, sortable=True) )
        g.add_col( GridCol('qui', text='Qui', width=100, sortable=True, editor='textfield') )
        g.add_col( GridCol('quoi', text="Quoi", width=300, sortable=True, editor='textfield') )
        g.add_col( GridCol('quand', text="Quand", width=150, sortable=True, editor='datetimefield') )
        g.add_col( GridCol('temps', text="Temps", width=70, sortable=True) )
        g.add_col( GridCol('status', text='Status', width=100, sortable=True) )
        g.titre = "Liste des Actions"
        g.width = 1000
        g.height = 400 
        g.pageSize = 10
        g.data_url = '/tt'
        g.base_url = '/tt'
        g.button_new_url = '/tt/cr'
        g.button_home = '/'
        g.editing = True
        S = g.render()
        #print S
        template = 'tt/liste.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } ) 

## ---------------------------------
## Constitution de la form de base
## ---------------------------------
def get_form():
    f = ExtForm()
    f.width = 1000
    f.height = 400 
    f.add_zone(Zone( 'titre', fieldLabel="Titre", width=500 ))
    ZB = ZBox( 'Tags', layout='hbox', xtype='fieldcontainer', hideLabel=True )
    ZB.add_zone(Zone( 'tag1', fieldLabel="Tag1" ))
    ZB.add_zone(Zone( 'tag2', fieldLabel="Tag2" ))
    ZB.add_zone(Zone( 'tag3', fieldLabel="Tag3" ))
    ZB.add_zone(Zone( 'tag4', fieldLabel="Tag4" ))
    ZB.add_zone(Zone( 'tag5', fieldLabel="Tag5" ))
    f.add_zone(ZB)
    f.add_zone(Zone( 'status', fieldLabel="Status", xtype = "combo", data = STATUS_NOTES, def_value='OK' ))
    f.add_zone(Zone( 'description', fieldLabel="Description", xtype = 'htmleditor', width=700, height=300 ))
    return f

## ---------------------------------
## La creation d'un enregistrement
## ---------------------------------
def create(request):
    form = NoteForm
    if request.method == 'POST':
        print request
        f = form(request.POST)
        if f.is_valid():
            f.save()
            r = '{ success: true, msg: "OK A VENIR " }'
        else:
            r = '{ success: false, msg: "Form Invalid" }'
        print r
        return HttpResponse(r, mimetype='application/json')
    else:
        f = get_form()
        f.url = '/notes/cr/'
        f.url_annul = '/notes/'
        f.titre = "Creation"
        S = f.render()

        template = 'notes/notes.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )

## -----------------
## L'effacement
## -----------------
def delete(request, enreg_id):
    model = Note
    if request.method == 'POST':
        print request
        #pdb.set_trace()
        if request.POST['DELETE'] == 'VALID':
            a = model.objects.get(id=enreg_id).delete()
            r = '{ success: true }'
        else:
            ## Bouton ANNUL
            r = '{ success: false }'
        print r
        return HttpResponse(r, mimetype='application/json')
    else:
        obj = model.objects.get(pk=enreg_id)
        f = get_form()
        f.url = '/notes/del/%s' % enreg_id
        f.url_annul = '/notes/'
        f.titre = "Annulation"
        f.mode = 'del'
        f.mod_zone( 'titre', 'def_value', obj.titre )
        f.mod_zone( 'titre', 'readOnly', True )
        f.mod_zone( 'tag1', 'def_value', obj.tag1 )
        f.mod_zone( 'tag1', 'readOnly', True )
        f.mod_zone( 'tag2', 'def_value', obj.tag2 )
        f.mod_zone( 'tag2', 'readOnly', True )
        f.mod_zone( 'tag3', 'def_value', obj.tag3 )
        f.mod_zone( 'tag3', 'readOnly', True )
        f.mod_zone( 'tag4', 'def_value', obj.tag4 )
        f.mod_zone( 'tag4', 'readOnly', True )
        f.mod_zone( 'tag5', 'def_value', obj.tag5 )
        f.mod_zone( 'tag5', 'readOnly', True )
        f.mod_zone( 'status', 'def_value', obj.status )
        f.mod_zone( 'status', 'readOnly', True )
        f.mod_zone( 'description', 'def_value', obj.description )
        f.mod_zone( 'description', 'readOnly', True )
        f.add_zone(Zone( 'DELETE', fieldLabel="VALID", xtype='hidden', def_value='VALID' ))

        S = f.render()

        template = 'notes/notes.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )

## -------------------
## La modification
## -------------------
def modif(request, enreg_id):
    model = Note
    form = NoteForm
    if request.method == 'POST':
        #print request
        #pdb.set_trace()
        if request.POST['MODIF'] == 'VALID':
            a = model.objects.get(id=enreg_id)
            f = form(request.POST, instance=a)
            if f.is_valid():
                f.save()
                r = '{ success: true, msg: "OK A VENIR " }'
            else:
                r = '{ success: false, msg: "Form Invalid" }'
        else:
            ## Bouton ANNUL
            r = '{ success: false }'
        print r
        return HttpResponse(r, mimetype='application/json')
    else:
        obj = model.objects.get(pk=enreg_id)
        f = get_form()
        f.url = '/notes/mod/%s/' % enreg_id
        f.url_annul = '/notes/'
        f.titre = "Modification de %s" % enreg_id
        f.mode = 'mod'
        f.mod_zone( 'titre', 'def_value', obj.titre )
        f.mod_zone( 'tag1', 'def_value', obj.tag1 )
        f.mod_zone( 'tag2', 'def_value', obj.tag2 )
        f.mod_zone( 'tag3', 'def_value', obj.tag3 )
        f.mod_zone( 'tag4', 'def_value', obj.tag4 )
        f.mod_zone( 'tag5', 'def_value', obj.tag5 )
        f.mod_zone( 'status', 'def_value', obj.status )
        f.mod_zone( 'description', 'def_value', obj.description )
        f.mod_zone( 'description', 'readOnly', True )
        f.add_zone(Zone( 'MODIF', fieldLabel="VALID", xtype='hidden', def_value='VALID' ))

        S = f.render()

        template = 'notes/notes.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } )
