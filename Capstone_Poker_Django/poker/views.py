from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import poker
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
import time
from django.http import StreamingHttpResponse
import mimetypes
from wsgiref.util import FileWrapper
import os


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
    botnumber = request.POST.get('botnumber', '4')  # defaults to '4'
    output= poker.run_game(botnumber)
    context = {
       'log':output,
       
    }
    return render(request, 'log.html', context)

    # Wrap output in <pre> tags to maintain formatting.
    #return HttpResponse(f"<pre>{output}</pre>")

def download(request):
    base= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name="/poker/Poker_Bot_Template.py"
    filepath= base+file_name
    thefile= filepath
    file_name= os.path.basename(thefile)
    response= StreamingHttpResponse(FileWrapper(open(thefile, 'rb'),8192),
                                    content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s"% file_name
    return response

def logtext(request):
    log = request.POST.get("gamelog")
    response= HttpResponse(log,content_type='text/plain')
    response['Content-Disposition'] = 'Attachment;filename="logoutput.txt"'
    return response