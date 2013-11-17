# Create your views here.
from django.utils import simplejson
from django.shortcuts import render_to_response, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render_to_response('base/index.html')
