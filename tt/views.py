# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse, render
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from extjs_lib.grid import ExtGrid, GridCol
from extjs_lib.form import ExtForm, Zone, ZBox
from tt.models import Action, ActionForm, STATUS_ACTION

import datetime, time

import pdb

## -----------------------
## La liste de depart
## -----------------------
def debug(request, action):
    print datetime.datetime.now(), "DEBUG"," - ACTION : %s" % action
    print request.POST
    obj = {
        'total' : 0,
        'message' : 'OK',
        'success' : True,
        'rows' : []
    }
    data = simplejson.dumps(obj)
    print "DEBUG", data
    return HttpResponse(data, mimetype='text/javascript')  

## -------------------------
## Mise a jour de la ligne
## -------------------------
def update(request, action):
    model = Action
    #form = ActionForm
    ## Debug
    print datetime.datetime.now(), "UPDATE"," - ACTION : %s" % action
    #pdb.set_trace()
    record = simplejson.loads(request.POST['rows'])
    print "Record = %s " % record
    ## 
    #record = record[0]
    enreg_id = record['id']
    print "enreg_id = %s" % enreg_id
    ## Si enreg_id = 0 alors creation
    enreg = model.objects.get(id=enreg_id)
    enreg.qui  = record['qui']
    #print "=== %s " % record['quand']
    t = time.strptime(record['quand'], '%d/%m/%y')
    dt = datetime.datetime(*t[:6])
    enreg.quand  = dt.strftime('%Y-%m-%d')
    #print "=== %s " % enreg.quand
    enreg.quoi  = record['quoi']
    enreg.temps  = record['temps']
    enreg.status  = record['status']
    ## Faire qq verif
    enreg.save()
    r = '{ success: true, msg: "OK" }'
    return HttpResponse(r, mimetype='application/json')

## ---------------------------------
## La liste = Grille editable
## ---------------------------------
def liste(request, action='read'):
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

        print obj_list

        ## Dans le cas d'une liste d'objets
        obj = [ob.to_json() for ob in obj_list]
        ## sinon obj tout seul
        ## obj = ob.to_json()

        root_name = 'rows'
        data = '{"total": %s, "%s": %s}' % (total, root_name, simplejson.dumps(obj))

        ## Pour debug
        print data
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
        g.add_col( GridCol('quand', text="Quand", width=150, sortable=True, xtype='datefield') )
        g.add_col( GridCol('temps', text="Temps", width=70, sortable=True, editor='textfield') )
        g.add_col( GridCol('status', text='Status', width=100, sortable=True, xtype='combo', store=STATUS_ACTION ))
        g.titre = "Liste des Actions"
        g.width = 1000
        g.height = 400 
        g.pageSize = 10
        g.data_url = '/tt'
        g.base_url = '/tt'
        g.button_new_url = '/tt/cr'
        g.button_home = '/'
        g.editing = True
        g.RowEditing = True
        g.modif = False
        S = g.render()
        #print S
        template = 'tt/liste.html'
        return render( request, template, { 'SCRIPT_EXTJS':S } ) 
