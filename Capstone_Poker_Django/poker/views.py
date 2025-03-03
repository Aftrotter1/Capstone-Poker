from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import poker
from . import bots
from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
import time
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .pokerstrat import discoverStrats
from django.http import StreamingHttpResponse
import mimetypes
from wsgiref.util import FileWrapper
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from poker.forms import BotForm
from .models import Bot

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
    output = poker.run_game(botnumber=botnumber, smallblind=10, stack=1000)
    return render(request, 'log.html', {'log': output})



def custom(request):
    discovered = discoverStrats(bots)
    strategy_names = [cls.__name__ for cls in discovered]
    return render(request, 'custom.html', {'strategy_names': strategy_names})

def customgame(request):
    discovered = discoverStrats(bots)
    strategy_names = [cls.__name__ for cls in discovered]
    custom_config = {}
    for strat in strategy_names:
        count_str = request.POST.get(strat, '0')
        count = int(count_str) if count_str.isdigit() else 0
        if count > 0:
            custom_config[strat] = count

    smallblind = request.POST.get('smallBlind', '10') # defaults to '4'
    stacknumber = request.POST.get('stacknumber', '1000') # defaults to '4'

    output = poker.run_game(
        custom_config=custom_config,
        smallblind=smallblind,
        stack=stacknumber
    )
    return render(request, 'log.html', {'log': output})


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

@login_required
def profile(request):
        bots = Bot.objects.all()
        if request.method == 'POST':
            bot= BotForm(request.POST,request.FILES)
            if bot.is_valid():
                model_instance = bot.save(commit=False)
                if model_instance.user_id is None:
                     model_instance.user_id = "1"
                model_instance.user=  request.user
                model_instance.save()
              
            else:
                context={"bots": bot}
                return render(request, 'profile.html',context)
        context={"bots": BotForm(), "botlist": bots}
        return render(request, 'profile.html',context)

def begin(request):
    return render(request, 'begin.html')
    


def studentsgame(request):
    return render(request, 'start.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='')

        return render(request, self.template_name, {'form': form})
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)