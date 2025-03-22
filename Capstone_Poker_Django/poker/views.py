from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import poker
from . import bots as bots_dir
from django.shortcuts import redirect
from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.urls import reverse
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
from poker.forms import StudentBotForm
from poker.forms import BaseBotForm
from .models import StudentBot
from .models import BaseBot
from .models import TournamentData
from .models import Tournament
from django.db.models import Max
from django.db.models import Min
import importlib
import inspect
from .pokerstrat import Strategy

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
    discovered = discoverStrats(bots_dir)
    strategy_names = [cls.__name__ for cls in discovered]
    return render(request, 'custom.html', {'strategy_names': strategy_names})

def customgame(request):
    discovered = discoverStrats(bots_dir)
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

def admin_check(user):
    return user.is_superuser

@login_required
def profile(request):
   
        bots = BaseBot.objects.all()
        studentbots= StudentBot.objects.filter(user=request.user).order_by('uploaded_at')
        studentBotsOrdered=studentbots.reverse()
        if request.method == 'POST':
            bot= StudentBotForm(request.POST,request.FILES)
            if bot.is_valid():
                model_instance = bot.save(commit=False)
                if model_instance.user_id is None:
                     model_instance.user_id = "1"
                model_instance.user=  request.user
                model_instance.save()
              
            else:
                context={"bots": bot}
                return render(request, 'profile.html',context)
        context={"bots": BaseBotForm(), "botlist": bots, "studentbots":studentBotsOrdered}
        return render(request, 'profile.html',context)

def profilechoice(request):
    if request.user.is_superuser:
         return redirect(reverse('adminprofile'))
    else:
         return redirect(reverse('profile'))

@login_required
@user_passes_test(admin_check)
def adminprofile(request):
        
        seen= set()
        LATEST_BOT = StudentBot.objects.values('user_id')
        bots = []
        for bot in LATEST_BOT:
            recent_bot= StudentBot.objects.filter(user_id=bot['user_id']).latest('uploaded_at')
            if recent_bot and bot['user_id'] not in seen:
                bots.append(recent_bot)
                seen.add(bot['user_id'])
        if request.method == 'POST':
            if 1==1: #if tournament logic is valid
                pass#add tournament logic
              
            else:
               # context={"bots": bot} 
                #return render(request, 'admin.html',context) send data 
                pass
        context={"bots": StudentBotForm(), "botlist": bots}
        # request.session.aset('botlist', context['botlist'])
        return render(request, 'admin.html',context)

@login_required
def runstudent(request):
    basebots = BaseBot.objects.all()
    studentbots= StudentBot.objects.filter(user=request.user).order_by('uploaded_at')
    studentBotsOrdered=studentbots.reverse()
    num_games = 50
    num_players = 8
    latest_bot_qs = StudentBot.objects.filter(user=request.user)
    # raise Exception(str(latest_bot_qs))
    bots = []
    for bot in latest_bot_qs:
            bots.append(bot)
    
    # Prepare context with the form and  of bots.
    context = {
        "bots": BaseBotForm(),  # This form renders the bot selection checkboxes in your template.
        "botlist": basebots,
        "buttonclicked": False,
        "studentbots":studentBotsOrdered
    }
    
    if request.method == "POST":
        context["buttonclicked"] = True
        # Retrieve the selected bot IDs from the POST data (from checkboxes named "bot_ids")
        selected_base_ids = request.POST.getlist('bot_ids')
        selected_bot_ids= request.POST.getlist('studentbot_ids')
        
        # Build a custom configuration for the tournament.
        # This dictionary maps each bot's strategy (here, we use bot.name as a placeholder)
        # to the number of times it should appear.
        selected_bots = StudentBot.objects.filter(id__in=selected_bot_ids)
        selected_base_bots=BaseBot.objects.filter(id__in=selected_base_ids)
        custom_config = {}
        for bot in selected_bots:
            bot_info = (bot.user, bot) # student id and bot id, needed for tournament table
            bot_path = f"{bots_dir.__name__}.{bot.Bot_File}" 
            if len(bot_path) > 3 and bot_path[-3:] == '.py':
                bot_path = bot_path[:-3]
            module = importlib.import_module(bot_path)
            # raise Exception(bot_path)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure the class is a subclass of Strategy and not Strategy itself.
                if issubclass(obj, Strategy) and obj is not Strategy:
                    bot_class = obj.__name__
            # search by class name, not nickname
            custom_config[bot_class] = (custom_config.get(bot_class, (0, ()))[0] + 1, bot_info)
        for bot in selected_base_bots:
            bot_info = (bot) # student id and bot id, needed for tournament table
            bot_path = f"{bots_dir.__name__}.{bot.Bot_File}" 
            if len(bot_path) > 3 and bot_path[-3:] == '.py':
                bot_path = bot_path[:-3]
            module = importlib.import_module(bot_path)
            # raise Exception(bot_path)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure the class is a subclass of Strategy and not Strategy itself.
                if issubclass(obj, Strategy) and obj is not Strategy:
                    bot_class = obj.__name__
            # search by class name, not nickname
            custom_config[bot_class] = (custom_config.get(bot_class, (0, ()))[0] + 1, bot_info)
        
        if not custom_config:
            context["error"] = "No bots selected. Please select at least one bot."
        else:
            # Run the tournament using the new function.
            scores, tournament_log = poker.run_tournament(
                num_games=num_games,
                custom_config=custom_config,
                smallblind=10,
                stack=100,
                game_size=num_players,      # you can adjust this if needed
                min_players=2
            )
            if not scores:
                raise Exception("tournament returned empty scores dict\nlog:\n" + tournament_log)
            # Sort scores in descending order
            studentseen={}
            for winner, (num_wins, info) in scores.items():
                if type(info) is not BaseBot:
                     sid, bid = info
                     studentseen[sid]=0
            for winner, (num_wins, info) in scores.items():
                if type(info) is not BaseBot:
                    sid, bid = info
                    studentseen[sid]+=num_wins
            context["studentseen"]=studentseen
            scores = {k: v[0] for k, v in scores.items()}
            scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
            context["scores"] = scores
            context["num_games"] = num_games
            context["tournament_log"] = tournament_log
    print(scores)
    print(studentseen)
    
    return render(request, 'profile.html', context)


@login_required
@user_passes_test(admin_check)
def runtourney(request):
    num_games = 50
    num_players = 8
    seen = set()
    # Get the latest StudentBot for each user
    latest_bot_qs = StudentBot.objects.values('user_id')
    # raise Exception(str(latest_bot_qs))
    bots = []
    for bot in latest_bot_qs:
        recent_bot = StudentBot.objects.filter(user_id=bot['user_id']).latest('uploaded_at')
        if recent_bot and bot['user_id'] not in seen:
            bots.append(recent_bot)
            seen.add(bot['user_id'])
    
    # Prepare context with the form and  of bots.
    context = {
        "bots": StudentBotForm(),  # This form renders the bot selection checkboxes in your template.
        "botlist": bots,
        "buttonclicked": False,
    }
    
    if request.method == "POST":
        context["buttonclicked"] = True
        # Retrieve the selected bot IDs from the POST data (from checkboxes named "bot_ids")
        selected_bot_ids = request.POST.getlist('bot_ids')
        
        # Build a custom configuration for the tournament.
        # This dictionary maps each bot's strategy (here, we use bot.name as a placeholder)
        # to the number of times it should appear.
        selected_bots = StudentBot.objects.filter(id__in=selected_bot_ids)
        custom_config = {}
        for bot in selected_bots:
            bot_info = (bot.user, bot) # student id and bot id, needed for tournament table
            bot_path = f"{bots_dir.__name__}.{bot.Bot_File}" 
            if len(bot_path) > 3 and bot_path[-3:] == '.py':
                bot_path = bot_path[:-3]
            module = importlib.import_module(bot_path)
            # raise Exception(bot_path)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure the class is a subclass of Strategy and not Strategy itself.
                if issubclass(obj, Strategy) and obj is not Strategy:
                    bot_class = obj.__name__
            # search by class name, not nickname
            custom_config[bot_class] = (custom_config.get(bot_class, (0, ()))[0] + 1, bot_info)
        if not custom_config:
            context["error"] = "No bots selected. Please select at least one bot."
        else:
            # Run the tournament using the new function.
            scores, tournament_log = poker.run_tournament(
                num_games=num_games,
                custom_config=custom_config,
                smallblind=10,
                stack=100,
                game_size=num_players,      # you can adjust this if needed
                min_players=2
            )
            if not scores:
                raise Exception("tournament returned empty scores dict\nlog:\n" + tournament_log)
            tourney = TournamentData.objects.create(NumberofPlayers=num_players, NumberofGames=num_games)
            tourney.save()
            studentseen=defaultdict(int)
            unique=set()

            for winner, (num_wins, info) in scores.items():
                sid, bid = info
                studentseen[sid]+=num_wins
            for winner, (num_wins, info) in scores.items():
                sid, bid = info
                if sid not in unique:
                    row = Tournament.objects.create(TournamentID=tourney, StudentID=sid, BotID=bid, NumberOfRounds=0, NumberOfWins=studentseen[sid])
                    row.save()
                unique.add(sid)
                



            # Sort scores in descending order
            scores = {k: v[0] for k, v in scores.items()}
            scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
            context["scores"] = scores
            context["num_games"] = num_games
            context["tournament_log"] = tournament_log
    
    return render(request, 'admin.html', context)
#INCOMPLETE TOURNEY HISTORY VIEW
@login_required
def tournament_history(request):

    data_list = (TournamentData.objects
                 .filter(Visible=True)
                 .order_by('-DateRun')          # show latest first
                 .prefetch_related('tournament_set',
                                   'tournament_set__StudentID',
                                   'tournament_set__BotID'))
    return render(request, 'tournament_history.html', {'data_list': data_list})

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

            return redirect(to='/')

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