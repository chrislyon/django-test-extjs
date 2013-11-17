# Create your views here.

from django.shortcuts import render_to_response, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

def index(request):
        return render_to_response('bry1/index.html')

def page(request, action='p2'):
        p = 'bry1/%s.html' % action
        return render_to_response(p)

