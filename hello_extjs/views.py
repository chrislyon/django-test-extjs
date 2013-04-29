# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from collections import OrderedDict
from extjs_lib.grid import ExtGrid, Champ


def index(request):
    return render_to_response('hello_extjs/index.html')

## Pour une page avec formulaire 
## Il faut : une fonction pour le rendu 
## Une fonction pour l'initialisation / chargement load
## Une fonction pour la sauvegarde et la verification
@csrf_exempt
def page1(request):
    if request.method == "POST":
        to_json = {
            'success': 'false',
            'errmsg': "MESSAGE ERREUR"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    else:
        return render_to_response('hello_extjs/page1.html')

def page5(request):
    return render_to_response('hello_extjs/page5.html')

def page41(request):
    return render_to_response('hello_extjs/page41.html')

def page42(request):
    champ = OrderedDict()
    champ['name'] = dict(
        text='Nom',
        dataIndex='name',
        width=100,
        hideable=False,
    )
    champ['email'] = dict(
        text='Email',
        dataIndex='email',
        width=150,
        hidden=True
    )
    champ['phone'] = dict(
        text='Telephone',
        dataIndex='phone',
        width=100,
    )
    champ['zipcode'] = dict(
        text='ZipCode',
        dataIndex='zipcode',
        width=50,
    )

    ## Pour Test
    data = [
        { 'name': 'Lisa', 'email': 'lisa@simpsons.com', 'phone': '555-111-1224' , 'zipcode':"010101" },
        { 'name': 'Bart', 'email': 'bart@simpsons.com', 'phone': '555-222-1234' , 'zipcode':"010101" },
        { 'name': 'Homer', 'email': 'home@simpsons.com', 'phone': '555-222-1244' , 'zipcode':"010101" },
        { 'name': 'Marge', 'email': 'marge@simpsons.com', 'phone': '555-222-1254' , 'zipcode':"010101" }
    ]

    S =  ext_grid( champ , titre="Liste des contacts", data=data )
    print S
    template = 'hello_extjs/page42.html'
    return render( request, template, { 'SCRIPT_EXTJS':S } )

def page43(request):
    g = ExtGrid()
    g.add_champ( Champ('name', text='Nom du Contact', width=150) )
    g.add_champ( Champ('email', text='E-Mail', width=200) )
    g.add_champ( Champ('phone', text="Telephone") )
    g.add_champ( Champ('zipcode', text='Code Postal', hidden=True) )
    g.titre = "Nouvelle Grille Auto"
    g.width = 600
    g.heigth = 300

    ## Pour Test
    g.data = [
        { 'name': 'Lisa', 'email': 'lisa@simpsons.com', 'phone': '555-111-1224' , 'zipcode':"010101" },
        { 'name': 'Bart', 'email': 'bart@simpsons.com', 'phone': '555-222-1234' , 'zipcode':"010101" },
        { 'name': 'Homer', 'email': 'home@simpsons.com', 'phone': '555-222-1244' , 'zipcode':"010101" },
        { 'name': 'Marge', 'email': 'marge@simpsons.com', 'phone': '555-222-1254' , 'zipcode':"010101" }
    ]
    S = g.render()

    template = 'hello_extjs/page42.html'
    return render( request, template, { 'SCRIPT_EXTJS':S } )
