# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render_to_response('t2/index.html')

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

