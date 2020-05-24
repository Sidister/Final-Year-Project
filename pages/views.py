from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import urllib
from .face import pi_face

# Create your views here.

def index(request):
    if request.method == 'POST':
        canvasData = request.POST['canvasData']
        data = canvasData
        response = urllib.request.urlopen(data)
        with open('sawa/static/image.jpg', 'wb') as f:
            f.write(response.file.read())
        names=pi_face.process()

        context = {
            'names' : names
        }
        if len(names)>0:
            messages.success(request, 'Attendance was marked !')
        return render(request, 'pages/index.html', context)

    return render(request, 'pages/index.html')