from django.shortcuts import render

def index(request):
    #template = loader.get_template('home.html') #for template stuff
    #return HttpResponse("Hello, world. You're at the homepage index.")
    #return HttpResponse(template.render())
    return render(request, "loginpage/login.html") 
