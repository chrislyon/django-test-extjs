# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response('hello_extjs/index.html')

## Pour une page avec formulaire 
## Il faut : une fonction pour le rendu 
## Une fonction pour l'initialisation / chargement load
## Une fonction pour la sauvegarde et la verification
@csrf_exempt
def page1(request):
    if request.method == "POST":
        print request
        to_json = {
            'errmsg':"MESSAGE DE RETOUR"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    else:
        return render_to_response('hello_extjs/page1.html')
