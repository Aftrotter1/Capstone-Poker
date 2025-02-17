from django.shortcuts import render
from django.http import HttpResponse
from . import poker
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
import time


def index(request):
                
    if request.method == 'POST'and request.FILES['bot1'].name.endswith('.py'):
        uploaded_file = request.FILES['bot1']
        fs= FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        return render(request, 'game_choice.html')
    return render(request, 'upload_test.html')

def gamechoice(request):
   return render(request, 'game_choice.html')

def logtest(request):
    return render(request,'index.html')
def game(request):
    botnumber= request.POST.get('botnumber')
    context ={
       'log': poker.run_game(botnumber)

    }
    return render(request, 'log.html',context)
    # Wrap output in <pre> tags to maintain formatting.
    #return HttpResponse(f"<pre>{output}</pre>")