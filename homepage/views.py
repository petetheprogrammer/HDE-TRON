from django.http import HttpResponse
from django.template import loader


def index(request):
    #template = loader.get_template('home.html') #for template stuff
    return HttpResponse("Hello, world. You're at the homepage index.")